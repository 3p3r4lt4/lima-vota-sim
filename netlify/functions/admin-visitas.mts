import type { Config } from "@netlify/functions";
import { esAdmin, noAutorizado, CABECERAS } from "../lib/auth-admin.mjs";
import {
  leerFiltros, construirWhere, prepararSesion, aCsv, COLUMNAS_SESION, FROM_SESIONES, POR_PAGINA, ACTIVA_SEG,
} from "../lib/admin-consultas.mjs";

// Métricas del panel. Solo lectura (DATABASE_URL_ANALYTICS_READER) y solo con cookie de admin válida.

let pool: any = null;
async function db() {
  const pg = (await import("pg")).default;
  pool ??= new pg.Pool({
    connectionString: process.env.DATABASE_URL_ANALYTICS_READER, max: 3, ssl: { rejectUnauthorized: false },
    connectionTimeoutMillis: 5000, statement_timeout: 10_000,
  });
  return pool;
}

const MAX_CSV = 50_000;

async function resumen(p: any, w: { sql: string; valores: any[] }, pagina: number) {
  const q = async (sql: string, extra: any[] = []) => (await p.query(sql, [...w.valores, ...extra])).rows;
  const n = w.valores.length;
  const top = (col: string, limite = 10) => q(
    `select coalesce(v.${col}, 'Sin dato') as k, count(*)::int as n from visitas_sesion v where ${w.sql}
     group by 1 order by 2 desc, 1 limit ${limite}`);

  const [kpis, activas, porDia, porHora, departamento, provincia, distrito, ambito, vistas, dispositivo, so, navegador, filas, precision] =
    await Promise.all([
      q(`select count(*)::int as sesiones,
                count(distinct ((v.inicio at time zone 'America/Lima')::date, v.ip_hash))::int as unicos,
                coalesce(percentile_cont(0.5) within group (order by v.duracion_seg), 0)::int as mediana_seg,
                coalesce(avg(v.duracion_seg), 0)::int as media_seg,
                coalesce(round(100.0 * avg((v.dispositivo_tipo = 'movil')::int), 1), 0)::float as pct_movil,
                coalesce(sum(v.preguntas_count), 0)::int as preguntas
           from visitas_sesion v where ${w.sql}`),
      // «Ahora» no depende del rango de fechas elegido
      p.query(`select count(*)::int as n from visitas_sesion
                where fin is null and not es_bot and ultima_senal > now() - make_interval(secs => ${ACTIVA_SEG})`),
      q(`select to_char(v.inicio at time zone 'America/Lima', 'YYYY-MM-DD') as k, count(*)::int as n
           from visitas_sesion v where ${w.sql} group by 1 order by 1`),
      q(`select extract(hour from v.inicio at time zone 'America/Lima')::int as k, count(*)::int as n
           from visitas_sesion v where ${w.sql} group by 1 order by 1`),
      top("departamento"), top("provincia"), top("distrito"),
      q(`select a as k, count(*)::int as n from visitas_sesion v, unnest(v.ambitos_visitados) as a
           where ${w.sql} group by 1 order by 2 desc, 1 limit 15`),
      q(`select e.vista as k, count(*)::int as n from analytics_eventos e join visitas_sesion v using (sesion_id)
           where e.tipo = 'vista' and e.vista is not null and ${w.sql} group by 1 order by 2 desc`),
      top("dispositivo_tipo"), top("so"), top("navegador"),
      q(`select ${COLUMNAS_SESION} from ${FROM_SESIONES} where ${w.sql}
           order by v.inicio desc limit $${n + 1} offset $${n + 2}`, [POR_PAGINA, (pagina - 1) * POR_PAGINA]),
      top("precision_geo", 5),
    ]);

  const ahora = new Date();
  return {
    kpis: { ...kpis[0], activas: activas.rows[0].n }, por_dia: porDia, por_hora: porHora,
    top: { departamento, provincia, distrito, ambito }, vistas, dispositivo, so, navegador, precision,
    sesiones: { filas: filas.map((f: any) => prepararSesion(f, ahora)), pagina, por_pagina: POR_PAGINA, total: kpis[0].sesiones },
  };
}

// Opciones de los filtros de ubicación por IP (últimos 92 días, sin datos personales)
async function opciones(p: any) {
  const lista = async (col: string) => (await p.query(
    `select distinct ${col} as x from visitas_sesion
      where ${col} is not null and inicio > now() - interval '92 days' order by 1`)).rows.map((r: any) => r.x);
  const [departamentos, provincias, distritos] = await Promise.all([lista("departamento"), lista("provincia"), lista("distrito")]);
  return { departamentos, provincias, distritos };
}

// Últimos accesos al panel. Si la migración aún no corrió, el panel funciona igual.
async function accesos(p: any) {
  try {
    const { rows } = await p.query(
      `select to_char(creado_en at time zone 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') as fecha,
              left(ip_hash, 8) as huella, resultado
         from admin_login_log order by creado_en desc limit 20`);
    return rows;
  } catch {
    return [];
  }
}

export default async (req: Request) => {
  if (!esAdmin(req)) return noAutorizado();
  if (!process.env.DATABASE_URL_ANALYTICS_READER) {
    return Response.json({ error: "La base de analítica no está configurada." }, { status: 503, headers: CABECERAS });
  }
  const params = new URL(req.url).searchParams;
  const filtros = leerFiltros(params);
  const w = construirWhere(filtros);

  try {
    const p = await db();
    if (params.get("formato") === "csv") {
      const { rows } = await p.query(
        `select ${COLUMNAS_SESION} from ${FROM_SESIONES} where ${w.sql} order by v.inicio desc limit ${MAX_CSV}`, w.valores);
      const ahora = new Date();
      return new Response(aCsv(rows.map((f: any) => prepararSesion(f, ahora))), {
        headers: {
          ...CABECERAS, "content-type": "text/csv; charset=utf-8",
          "content-disposition": `attachment; filename="visitas_${filtros.desde}_${filtros.hasta}.csv"`,
        },
      });
    }
    const [ops, datos, ultimosAccesos] = await Promise.all([opciones(p), resumen(p, w, filtros.pagina), accesos(p)]);
    return Response.json({ filtros, ...ops, ...datos, accesos: ultimosAccesos }, { headers: CABECERAS });
  } catch (e: any) {
    console.error("admin-visitas: consulta falló", e?.code ?? e?.message);
    return Response.json({ error: "No se pudieron cargar los datos." }, { status: 500, headers: CABECERAS });
  }
};

export const config: Config = {
  path: "/api/admin/visitas",
  method: "GET",
  rateLimit: { windowLimit: 60, windowSize: 60, aggregateBy: ["ip", "domain"] },
};
