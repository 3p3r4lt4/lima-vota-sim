import type { Config } from "@netlify/functions";
import { buscar, respuestaExtractiva, esPreguntaDeLista, normalizar } from "../lib/busqueda.mjs";

// Modos automáticos según variables de entorno:
//   recuperación: pgvector (DATABASE_URL_READONLY + VOYAGE_API_KEY) o léxica BM25 sobre /data/planes
//   redacción:    Claude (ANTHROPIC_API_KEY) o extractiva (frases textuales de las fuentes)

const SISTEMA = `Ayudas a ciudadanos de Lima a comparar lo que propusieron los candidatos a la alcaldía.
Los fragmentos resumen lo que cada candidatura expuso en el debate del JNE, según medios de prensa. No son el plan completo.
Reglas estrictas:
- Usa exclusivamente los fragmentos. No agregues conocimiento externo ni opiniones sobre las personas.
- Una o dos oraciones por candidatura que sí tenga fragmentos, en el orden recibido y con el mismo nivel de detalle para todas.
- Empieza cada línea con **Nombre:** y cita cada afirmación así: [Nombre, p.N], copiando la referencia del fragmento.
- Al final, en una sola línea: **No mencionaron este tema en las fuentes revisadas:** y los nombres restantes.
- No recomiendes, no califiques, no compares calidad ni viabilidad, no digas por quién votar. Si te lo piden, explica que la herramienta solo describe propuestas y que la decisión es del votante.`;

let pool: any = null;
async function buscarPgvector(pregunta: string, ids: number[]) {
  const pg = (await import("pg")).default;
  pool ??= new pg.Pool({ connectionString: process.env.DATABASE_URL_READONLY, max: 3, ssl: { rejectUnauthorized: false } });
  const r = await fetch("https://api.voyageai.com/v1/embeddings", {
    method: "POST",
    headers: { "content-type": "application/json", authorization: `Bearer ${process.env.VOYAGE_API_KEY}` },
    body: JSON.stringify({ input: [pregunta], model: "voyage-3.5", input_type: "query" }),
  });
  if (!r.ok) throw new Error(`voyage ${r.status}`);
  const vector = `[${(await r.json()).data[0].embedding.join(",")}]`;
  const { rows } = await pool.query(
    `select b.candidato_id, b.pagina, b.contenido, c.nombre
       from buscar_chunks($1::vector, $2, $3::bigint[], $4) b join candidatos c on c.id = b.candidato_id`,
    [vector, pregunta, ids, ids.length * 2]);
  return rows.map((x: any) => ({ candidatoId: Number(x.candidato_id), nombre: x.nombre, pagina: x.pagina, texto: x.contenido }));
}

async function redactarConClaude(pregunta: string, fragmentos: any[], candidatos: any[]) {
  const orden = candidatos.map((c) => c.nombre).join(", ");
  const contexto = fragmentos.map((f) => `[${f.nombre}, p.${f.pagina}] ${f.texto}`).join("\n");
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "content-type": "application/json", "x-api-key": process.env.ANTHROPIC_API_KEY!, "anthropic-version": "2023-06-01" },
    body: JSON.stringify({
      model: process.env.CLAUDE_MODEL_QA ?? "claude-haiku-4-5-20251001",
      max_tokens: 1400,
      system: SISTEMA,
      messages: [{ role: "user", content: `Candidaturas (en este orden): ${orden}\n\nFragmentos:\n${contexto}\n\nPregunta: ${pregunta}` }],
    }),
  });
  if (!r.ok) throw new Error(`anthropic ${r.status}`);
  const d = await r.json();
  return d.content.filter((b: any) => b.type === "text").map((b: any) => b.text).join("\n");
}

const error = (msg: string, status = 400) => Response.json({ error: msg }, { status });
const json = (d: any) => Response.json(d, { headers: { "cache-control": "no-store" } });

export default async (req: Request) => {
  if (req.method !== "POST") return error("Método no permitido.", 405);
  const body = await req.json().catch(() => null);
  const pregunta = typeof body?.pregunta === "string" ? body.pregunta.trim() : "";
  const ubigeo = String(body?.ubigeo ?? "");
  const ids: number[] = Array.isArray(body?.candidatoIds) ? body.candidatoIds.map(Number).filter(Number.isInteger) : [];
  if (pregunta.length < 5 || pregunta.length > 300) return error("Escribe una pregunta de 5 a 300 caracteres.");
  if (!/^\d{4,6}$/.test(ubigeo)) return error("Distrito no válido.");
  if (ids.length === 0 || ids.length > 30) return error("Marca al menos una candidatura.");

  const base = new URL(req.url);
  const comp = await fetch(new URL(`/data/comparaciones/${ubigeo}.json`, base)).then((r) => (r.ok ? r.json() : null));
  if (!comp) return error("No hay datos para este ámbito.", 404);

  // 1. ¿Pregunta por otro distrito?
  const ambitos = await fetch(new URL("/data/ambitos.json", base)).then((r) => r.json()).catch(() => []);
  const q = normalizar(pregunta);
  const otro = ambitos.find((a: any) => a.ubigeo !== ubigeo && q.includes(normalizar(a.ambito)));
  if (otro) return json({ tipo: "otro_ambito", ubigeo: otro.ubigeo, ambito: otro.ambito,
    respuesta: `Tu pregunta menciona ${otro.ambito}, pero estás viendo ${comp.ambito}. Cambia de distrito en el titular para ver sus candidaturas.` });

  // 2. ¿Pregunta quiénes postulan?
  if (esPreguntaDeLista(pregunta)) {
    const lista = comp.candidatos.map((c: any) => `**${c.nombre}:** ${c.organizacion}${c.cargo_nota ? ` (${c.cargo_nota})` : ""}.`);
    return json({ tipo: "lista", respuesta: `Candidaturas a la alcaldía de ${comp.ambito} (${lista.length}):\n` + lista.join("\n") });
  }

  if (!comp.con_propuestas) return json({ tipo: "sin_propuestas",
    respuesta: `Todavía no hay propuestas cargadas para ${comp.ambito}. Puedes revisar los planes de gobierno oficiales en Voto Informado del JNE.` });

  const planes = await fetch(new URL(`/data/planes/${ubigeo}.json`, base)).then((r) => r.json());
  const candidatos = ids.map((id) => planes.candidatos.find((c: any) => c.id === id)).filter(Boolean);
  if (candidatos.length === 0) return error("Las candidaturas no pertenecen a este ámbito.");

  let recuperacion = "léxica", fragmentos: any[] = [];
  if (process.env.DATABASE_URL_READONLY && process.env.VOYAGE_API_KEY) {
    try { fragmentos = await buscarPgvector(pregunta, ids); recuperacion = "pgvector"; }
    catch (e) { console.error("pgvector falló, uso léxica:", e); }
  }
  if (recuperacion === "léxica") fragmentos = buscar(planes, pregunta, ids);

  let generacion = "extractiva", respuesta = "";
  if (fragmentos.length && process.env.ANTHROPIC_API_KEY) {
    try { respuesta = await redactarConClaude(pregunta, fragmentos, candidatos); generacion = "claude"; }
    catch (e) { console.error("Claude falló, uso extractiva:", e); }
  }
  if (!respuesta) respuesta = fragmentos.length
    ? respuestaExtractiva(pregunta, fragmentos, candidatos)
    : "Ninguna de las candidaturas marcadas mencionó este tema en las fuentes revisadas. Prueba con otras palabras (por ejemplo: serenazgo, cámaras, metro, agua, vivienda, comercio).";

  return json({ tipo: "respuesta", respuesta, modo: { recuperacion, generacion } });
};

export const config: Config = {
  path: "/api/preguntar",
  rateLimit: { windowLimit: 15, windowSize: 60, aggregateBy: ["ip", "domain"] },
};
