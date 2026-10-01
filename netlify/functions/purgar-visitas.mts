import type { Config } from "@netlify/functions";

// Retención de 90 días (Ley 29733). Corre a diario; purgar_visitas() es SECURITY DEFINER,
// así que el rol de escritura no necesita DELETE sobre la tabla.
export default async () => {
  if (!process.env.DATABASE_URL_ANALYTICS) return new Response(null, { status: 204 });
  const pg = (await import("pg")).default;
  const cliente = new pg.Client({
    connectionString: process.env.DATABASE_URL_ANALYTICS, ssl: { rejectUnauthorized: false }, connectionTimeoutMillis: 5000,
  });
  try {
    await cliente.connect();
    const { rows } = await cliente.query("select purgar_visitas(90) as borradas");
    console.log(`purgar-visitas: ${rows[0].borradas} sesiones con más de 90 días borradas`);
  } catch (e: any) {
    console.error("purgar-visitas: falló", e?.code ?? e?.message);
  } finally {
    await cliente.end().catch(() => {});
  }
  return new Response(null, { status: 204 });
};

export const config: Config = { schedule: "@daily" };
