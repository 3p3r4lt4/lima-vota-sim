import type { Config } from "@netlify/functions";
import { diasRetencion } from "../lib/visita.mjs";

// Retención (Ley 29733): ANALYTICS_RETENCION_DIAS, 180 por defecto. Corre a diario aunque ANALYTICS_ENABLED=false,
// para que lo ya guardado no se quede más tiempo del anunciado. purgar_visitas() es SECURITY DEFINER,
// así que el rol de escritura no necesita DELETE; los eventos se borran en cascada con su sesión.
export default async () => {
  if (!process.env.DATABASE_URL_ANALYTICS) return new Response(null, { status: 204 });
  const dias = diasRetencion();
  const pg = (await import("pg")).default;
  const cliente = new pg.Client({
    connectionString: process.env.DATABASE_URL_ANALYTICS, ssl: { rejectUnauthorized: false }, connectionTimeoutMillis: 5000,
  });
  try {
    await cliente.connect();
    const { rows } = await cliente.query("select purgar_visitas($1) as borradas", [dias]);
    console.log(`purgar-visitas: ${rows[0].borradas} sesiones con más de ${dias} días borradas`);
  } catch (e: any) {
    console.error("purgar-visitas: falló", e?.code ?? e?.message);
  } finally {
    await cliente.end().catch(() => {});
  }
  return new Response(null, { status: 204 });
};

export const config: Config = { schedule: "@daily" };
