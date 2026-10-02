import type { Config, Context } from "@netlify/functions";
import {
  validarEvento, hashIp, crearLimitador, mismoOrigen, analiticaHabilitada, TIPO_EVENTO, MAX_BODY,
} from "../lib/visita.mjs";
import { analizarUA } from "../lib/ua.mjs";
import { resolverGeo, crearIndiceRef } from "../lib/ubigeo-geo.mjs";

// Analítica propia. Siempre responde rápido y sin cuerpo; si falta configuración no hace nada.
// La IP nunca se guarda ni se registra en logs: solo su HMAC con sal diaria.

const permitir = crearLimitador({ max: 60, ventanaMs: 60_000 });
const NO_STORE = { "cache-control": "no-store" };
const vacio = (status = 204) => new Response(null, { status, headers: NO_STORE });
const MAX_EVENTOS = 500;  // por sesión; pasado el tope solo se actualiza la sesión

let pool: any = null;
async function db() {
  const pg = (await import("pg")).default;
  pool ??= new pg.Pool({
    connectionString: process.env.DATABASE_URL_ANALYTICS, max: 2, ssl: { rejectUnauthorized: false },
    connectionTimeoutMillis: 3000, idleTimeoutMillis: 10_000, statement_timeout: 3000,
  });
  return pool;
}

// Catálogo INEI para la geo por IP fuera de Lima. Se lee una vez por instancia; si falla
// (tabla vacía o sin migrar) se sigue con la tabla fija y se reintenta en 10 min.
let ref: { indice: Map<string, any> | null; hasta: number } = { indice: null, hasta: 0 };
async function indiceRef(p: any) {
  if (Date.now() < ref.hasta) return ref.indice;
  try {
    const { rows } = await p.query("select ubigeo, provincia, distrito from ref_ubigeo where length(ubigeo) >= 4");
    ref = { indice: crearIndiceRef(rows), hasta: Date.now() + 6 * 3600_000 };
  } catch (e: any) {
    console.error("visita: ref_ubigeo no disponible", e?.code ?? e?.message);
    ref = { indice: null, hasta: Date.now() + 10 * 60_000 };
  }
  return ref.indice;
}

const AGREGAR_AMBITO = `
  ambitos_visitados = case
    when $2::text is null or $2::text = any(ambitos_visitados) or cardinality(ambitos_visitados) >= 50
    then ambitos_visitados else array_append(ambitos_visitados, $2::text) end`;

// Latido: actualiza la señal sin crear fila de evento. Un latido tras un «fin» reabre la sesión
// (la pestaña volvió a estar visible).
const SQL_SENAL = `
  update visitas_sesion set ultima_senal = now(), fin = null, ${AGREGAR_AMBITO}
  where sesion_id = $1 and inicio > now() - interval '2 days'`;

// Resto de eventos: actualiza la sesión y agrega la fila en analytics_eventos en una sola sentencia.
// «salida» cierra la sesión; cualquier otro evento la deja abierta.
const SQL_EVENTO = `
  with s as (
    update visitas_sesion set
      ultima_senal = now(),
      fin = case when $3::text = 'salida' then now() else null end,
      ${AGREGAR_AMBITO},
      preguntas_count = preguntas_count + case when $3::text = 'pregunta' then 1 else 0 end,
      eventos_count = least(eventos_count + 1, ${MAX_EVENTOS + 1})
    where sesion_id = $1 and inicio > now() - interval '2 days'
    returning sesion_id, eventos_count)
  insert into analytics_eventos (sesion_id, tipo, ruta, vista, ambito_ubigeo)
  select sesion_id, $3::text, $4::text, $5::text, $2::text from s where eventos_count <= ${MAX_EVENTOS}`;

const SQL_INICIO = `
  insert into visitas_sesion (sesion_id, dispositivo_tipo, so, so_version, navegador, navegador_version, es_bot,
    pais, departamento, provincia, distrito, ubigeo_geo, precision_geo,
    ambito_inicial, ambitos_visitados, ip_hash, referer_host, idioma, pantalla, utm_source, utm_medium, utm_campaign)
  values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14::varchar,
    case when $14::text is null then '{}'::text[] else array[$14::text] end, $15, $16, $17, $18, $19, $20, $21)
  on conflict (sesion_id) do nothing`;

async function registrar(ev: any, ipHash: string, req: Request, context: Context) {
  const p = await db();
  if (ev.tipo === "latido") return p.query(SQL_SENAL, [ev.sesion_id, ev.ambito]);

  if (ev.tipo === "inicio") {
    const ua = analizarUA(req.headers.get("user-agent"));
    const g = resolverGeo(context.geo, await indiceRef(p));
    // Si ya existía (recarga en la misma pestaña, mismo sesion_id), no se duplica: cuenta como vista
    await p.query(SQL_INICIO, [
      ev.sesion_id, ua.dispositivo_tipo, ua.so, ua.so_version, ua.navegador, ua.navegador_version, ua.es_bot,
      g.pais, g.departamento, g.provincia, g.distrito, g.ubigeo_geo, g.precision_geo,
      ev.ambito, ipHash, ev.referer_host, ev.idioma, ev.pantalla, ev.utm_source, ev.utm_medium, ev.utm_campaign,
    ]);
  }
  return p.query(SQL_EVENTO, [ev.sesion_id, ev.ambito, TIPO_EVENTO[ev.tipo], ev.ruta, ev.vista]);
}

export default async (req: Request, context: Context) => {
  if (req.method !== "POST") return vacio(405);
  const sal = process.env.ANALYTICS_SALT;
  if (!analiticaHabilitada() || !process.env.DATABASE_URL_ANALYTICS || !sal) return vacio();
  if (!mismoOrigen(req)) return vacio(403);
  if (Number(req.headers.get("content-length") ?? 0) > MAX_BODY) return vacio(413);

  try {
    const v = validarEvento(await req.text());
    if (!v.ok) return vacio(400);
    if (!context.ip) return vacio();
    const ipHash = hashIp(context.ip, sal);
    // Por IP (seudonimizada) y también por sesión, que se mantiene aunque la IP cambie (redes móviles)
    if (!permitir(ipHash) || !permitir(v.evento.sesion_id)) return vacio(429);

    const tarea = registrar(v.evento, ipHash, req, context)
      .catch((e: any) => console.error("visita: no se pudo registrar", e?.code ?? e?.message));
    // Responde sin esperar a la base cuando la plataforma lo permite
    const waitUntil = (context as any).waitUntil;
    if (typeof waitUntil === "function") waitUntil(tarea); else await tarea;
  } catch (e: any) {
    console.error("visita: error", e?.message);
  }
  return vacio();
};

// /api/track es un alias; el cliente usa /api/visita porque los bloqueadores de anuncios filtran «track»
export const config: Config = {
  path: ["/api/visita", "/api/track"],
  method: "POST",
  rateLimit: { windowLimit: 120, windowSize: 60, aggregateBy: ["ip", "domain"] },
};
