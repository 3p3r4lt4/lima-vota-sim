import type { Config } from "@netlify/functions";
import { buscar, respuestaExtractiva } from "../lib/busqueda.mjs";

// Modos (se activan solos según las variables de entorno):
//   recuperación: pgvector (DATABASE_URL_READONLY + VOYAGE_API_KEY) o léxica BM25 sobre el corpus estático
//   generación:   Claude (ANTHROPIC_API_KEY) o extractiva (oraciones textuales del plan)

const SISTEMA = `Ayudas a ciudadanos peruanos a entender planes de gobierno municipales.
Reglas estrictas:
- Usa exclusivamente los fragmentos entregados. No agregues conocimiento externo.
- Responde en español sencillo, un párrafo corto por candidatura, en el orden recibido, con el mismo nivel de detalle para todas.
- Empieza cada párrafo con **Nombre:**. Si no hay fragmentos de una candidatura, escribe que su plan no menciona el tema.
- Cita cada afirmación así: [Nombre, p.N].
- No recomiendes, no califiques, no compares calidad, no digas por quién votar. Si te lo piden, explica que la herramienta solo describe lo que dicen los planes y que la decisión es del votante.`;

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
    [vector, pregunta, ids, ids.length * 3]);
  return rows.map((x: any) => ({ candidatoId: Number(x.candidato_id), nombre: x.nombre, pagina: x.pagina, texto: x.contenido }));
}

async function generarClaude(pregunta: string, fragmentos: any[], candidatos: any[]) {
  const orden = candidatos.map((c) => c.nombre).join(", ");
  const contexto = fragmentos.map((f) => `[${f.nombre}, p.${f.pagina}] ${f.texto}`).join("\n\n");
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "content-type": "application/json", "x-api-key": process.env.ANTHROPIC_API_KEY!, "anthropic-version": "2023-06-01" },
    body: JSON.stringify({
      model: process.env.CLAUDE_MODEL_QA ?? "claude-haiku-4-5-20251001",
      max_tokens: 800,
      system: SISTEMA,
      messages: [{ role: "user", content: `Candidaturas (en este orden): ${orden}\n\nFragmentos:\n${contexto}\n\nPregunta: ${pregunta}` }],
    }),
  });
  if (!r.ok) throw new Error(`anthropic ${r.status}`);
  const d = await r.json();
  return d.content.filter((b: any) => b.type === "text").map((b: any) => b.text).join("\n");
}

const error = (msg: string, status = 400) => Response.json({ error: msg }, { status });

export default async (req: Request) => {
  if (req.method !== "POST") return error("Método no permitido.", 405);
  const body = await req.json().catch(() => null);
  const pregunta = typeof body?.pregunta === "string" ? body.pregunta.trim() : "";
  const ubigeo = String(body?.ubigeo ?? "");
  const ids: number[] = Array.isArray(body?.candidatoIds) ? body.candidatoIds.map(Number).filter(Number.isInteger) : [];
  if (pregunta.length < 5 || pregunta.length > 300) return error("Escribe una pregunta de 5 a 300 caracteres.");
  if (!/^\d{4,6}$/.test(ubigeo)) return error("Distrito no válido.");
  if (ids.length === 0 || ids.length > 10) return error("Marca al menos una candidatura.");

  const res = await fetch(new URL(`/data/planes/${ubigeo}.json`, req.url));
  if (!res.ok) return error("No hay planes cargados para este distrito.", 404);
  const planes = await res.json();
  // Mismo orden (aleatorio) que ve el usuario en pantalla
  const candidatos = ids.map((id) => planes.candidatos.find((c: any) => c.id === id)).filter(Boolean);
  if (candidatos.length === 0) return error("Las candidaturas no pertenecen a este distrito.");

  let recuperacion = "léxica", fragmentos: any[] = [];
  if (process.env.DATABASE_URL_READONLY && process.env.VOYAGE_API_KEY) {
    try { fragmentos = await buscarPgvector(pregunta, ids); recuperacion = "pgvector"; }
    catch (e) { console.error("pgvector falló, uso léxica:", e); }
  }
  if (recuperacion === "léxica") fragmentos = buscar(planes, pregunta, ids);

  let generacion = "extractiva", respuesta = "";
  if (fragmentos.length && process.env.ANTHROPIC_API_KEY) {
    try { respuesta = await generarClaude(pregunta, fragmentos, candidatos); generacion = "claude"; }
    catch (e) { console.error("Claude falló, uso extractiva:", e); }
  }
  if (!respuesta) respuesta = respuestaExtractiva(pregunta, fragmentos, candidatos);

  const fuentes = [...new Map(fragmentos.map((f) => [`${f.candidatoId}-${f.pagina}`,
    { candidatoId: f.candidatoId, nombre: f.nombre, pagina: f.pagina }])).values()];
  return Response.json({ respuesta, fuentes, modo: { recuperacion, generacion } }, { headers: { "cache-control": "no-store" } });
};

export const config: Config = {
  path: "/api/preguntar",
  rateLimit: { windowLimit: 15, windowSize: 60, aggregateBy: ["ip", "domain"] },
};
