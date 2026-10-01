import type { Config, Context } from "@netlify/functions";
import { validarEvento, hashIp, crearLimitador, mismoOrigen, MAX_BODY } from "../lib/visita.mjs";
import { analizarUA } from "../lib/ua.mjs";
import { resolverGeo } from "../lib/ubigeo-geo.mjs";

// Analítica propia. Siempre responde rápido y sin cuerpo; si falta configuración no hace nada.
// La IP nunca se guarda ni se registra en logs: solo su HMAC con sal diaria.

const permitir = crearLimitador({ max: 60, ventanaMs: 60_000 });
const NO_STORE = { "cache-control": "no-store" };
const vacio = (status = 204) => new Response(null, { status, headers: NO_STORE });

let pool: any = null;
async function db() {
  const pg = (await import("pg")).default;
  pool ??= new pg.Pool({
    connectionString: process.env.DATABASE_URL_ANALYTICS, max: 2, ssl: { rejectUnauthorized: false },
    connectionTimeoutMillis: 3000, idleTimeoutMillis: 10_000, statement_timeout: 3000,
  });
  return pool;
}

// Actualiza la señal y agrega el ámbito sin duplicar (máx. 50). Un latido tras un «fin» reabre la sesión
// (la pestaña volvió a estar visible).
const SQL_SENAL = `
  update visitas_sesion set
    ultima_senal = now(), fin = null,
    ambitos_visitados = case
      when $2::text is null or $2::text = any(ambitos_visitados) or cardinality(ambitos_visitados) >= 50
      then ambitos_visitados else array_append(ambitos_visitados, $2::text) end
  where sesion_id = $1 and inicio > now() - interval '2 days'`;

const SQL_FIN = `
  update visitas_sesion set fin = now(), ultima_senal = now()
  where sesion_id = $1 and inicio > now() - interval '2 days'`;

const SQL_INICIO = `
  insert into visitas_sesion (sesion_id, dispositivo_tipo, so, so_version, navegador, navegador_version, es_bot,
    pais, departamento, provincia, distrito, ubigeo_geo, precision_geo,
    ambito_inicial, ambitos_visitados, ip_hash, referer_host, idioma, pantalla)
  values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14::varchar, array[$14::text], $15, $16, $17, $18)
  on conflict (sesion_id) do nothing`;

async function registrar(ev: any, ipHash: string, req: Request, context: Context) {
  const p = await db();
  if (ev.tipo === "fin") return p.query(SQL_FIN, [ev.sesion_id]);
  if (ev.tipo !== "inicio") return p.query(SQL_SENAL, [ev.sesion_id, ev.ambito]);

  const ua = analizarUA(req.headers.get("user-agent"));
  const g = resolverGeo(context.geo);
  const r = await p.query(SQL_INICIO, [
    ev.sesion_id, ua.dispositivo_tipo, ua.so, ua.so_version, ua.navegador, ua.navegador_version, ua.es_bot,
    g.pais, g.departamento, g.provincia, g.distrito, g.ubigeo_geo, g.precision_geo,
    ev.ambito, ipHash, ev.referer_host, ev.idioma, ev.pantalla,
  ]);
  // Recarga en la misma pestaña (mismo sesion_id en sessionStorage): cuenta como señal
  if (r.rowCount === 0) await p.query(SQL_SENAL, [ev.sesion_id, ev.ambito]);
}

export default async (req: Request, context: Context) => {
  if (req.method !== "POST") return vacio(405);
  const sal = process.env.ANALYTICS_SALT;
  if (!process.env.DATABASE_URL_ANALYTICS || !sal) return vacio();
  if (!mismoOrigen(req)) return vacio(403);
  if (Number(req.headers.get("content-length") ?? 0) > MAX_BODY) return vacio(413);

  try {
    const v = validarEvento(await req.text());
    if (!v.ok) return vacio(400);
    if (!context.ip) return vacio();
    const ipHash = hashIp(context.ip, sal);
    if (!permitir(ipHash)) return vacio(429);

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

export const config: Config = {
  path: "/api/visita",
  method: "POST",
  rateLimit: { windowLimit: 120, windowSize: 60, aggregateBy: ["ip", "domain"] },
};
