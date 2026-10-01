import type { Config } from "@netlify/functions";
import { esAdmin, noAutorizado, CABECERAS } from "../lib/auth-admin.mjs";
import { leerFiltros, construirWhere, aCsv, COLUMNAS_SESION, POR_PAGINA } from "../lib/admin-consultas.mjs";

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
    `select coalesce(${col}, 'Sin dato') as k, count(*)::int as n from visitas_sesion where ${w.sql}
     group by 1 order by 2 desc, 1 limit ${limite}`);

  const [kpis, porDia, porHora, departamento, provincia, distrito, ambito, dispositivo, so, navegador, filas, precision] =
    await Promise.all([
      q(`select count(*)::int as sesiones,
                count(distinct ((inicio at time zone 'America/Lima')::date, ip_hash))::int as unicos,
                coalesce(percentile_cont(0.5) within group (order by duracion_seg), 0)::int as mediana_seg,
                coalesce(round(100.0 * avg((dispositivo_tipo = 'movil')::int), 1), 0)::float as pct_movil
           from visitas_sesion where ${w.sql}`),
      q(`select to_char(inicio at time zone 'America/Lima', 'YYYY-MM-DD') as k, count(*)::int as n
           from visitas_sesion where ${w.sql} group by 1 order by 1`),
      q(`select extract(hour from inicio at time zone 'America/Lima')::int as k, count(*)::int as n
           from visitas_sesion where ${w.sql} group by 1 order by 1`),
      top("departamento"), top("provincia"), top("distrito"),
      q(`select a as k, count(*)::int as n from visitas_sesion, unnest(ambitos_visitados) as a
           where ${w.sql} group by 1 order by 2 desc, 1 limit 15`),
      top("dispositivo_tipo"), top("so"), top("navegador"),
      q(`select ${COLUMNAS_SESION} from visitas_sesion where ${w.sql}
           order by visitas_sesion.inicio desc limit $${n + 1} offset $${n + 2}`, [POR_PAGINA, (pagina - 1) * POR_PAGINA]),
      top("precision_geo", 5),
    ]);

  return {
    kpis: kpis[0], por_dia: porDia, por_hora: porHora,
    top: { departamento, provincia, distrito, ambito }, dispositivo, so, navegador, precision,
    sesiones: { filas, pagina, por_pagina: POR_PAGINA, total: kpis[0].sesiones },
  };
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
        `select ${COLUMNAS_SESION} from visitas_sesion where ${w.sql} order by visitas_sesion.inicio desc limit ${MAX_CSV}`, w.valores);
      return new Response(aCsv(rows), {
        headers: {
          ...CABECERAS, "content-type": "text/csv; charset=utf-8",
          "content-disposition": `attachment; filename="visitas_${filtros.desde}_${filtros.hasta}.csv"`,
        },
      });
    }
    const departamentos = (await p.query(
      `select distinct departamento as d from visitas_sesion
        where departamento is not null and inicio > now() - interval '92 days' order by 1`)).rows.map((r: any) => r.d);
    return Response.json({ filtros, departamentos, ...(await resumen(p, w, filtros.pagina)) }, { headers: CABECERAS });
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
