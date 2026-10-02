import type { Config, Context } from "@netlify/functions";
import { crearBloqueoMemoria, MAX_FALLOS } from "../lib/auth-admin.mjs";
import { crearManejadorLogin } from "../lib/login-admin.mjs";

// Login del panel: usuario (si ADMIN_USER está definido) + contraseña (scrypt) + código TOTP.
// Cualquier fallo responde el mismo mensaje. Cada intento queda en admin_login_log (solo ip_hash y resultado).
// Bloqueo: 5 fallos por ip_hash → 15 min, guardado en admin_intentos (respaldo en memoria si no hay base),
// más el rateLimit de la plataforma.

const memoria = crearBloqueoMemoria();

let pool: any = null;
async function db() {
  const pg = (await import("pg")).default;
  pool ??= new pg.Pool({
    connectionString: process.env.DATABASE_URL_ANALYTICS, max: 1, ssl: { rejectUnauthorized: false },
    connectionTimeoutMillis: 3000, statement_timeout: 3000,
  });
  return pool;
}

const SQL_FALLO = `
  insert into admin_intentos as t (ip_hash, fallos, primer_fallo) values ($1, 1, now())
  on conflict (ip_hash) do update set
    fallos = case when t.primer_fallo < now() - interval '15 minutes' then 1 else t.fallos + 1 end,
    primer_fallo = case when t.primer_fallo < now() - interval '15 minutes' then now() else t.primer_fallo end,
    bloqueado_hasta = case
      when t.primer_fallo >= now() - interval '15 minutes' and t.fallos + 1 >= $2 then now() + interval '15 minutes'
      else t.bloqueado_hasta end`;

// Con base: la tabla manda. Si la base falla, se usa la memoria (nunca se deja pasar sin control).
const bloqueo = {
  async bloqueado(ipHash: string) {
    if (await memoria.bloqueado(ipHash)) return true;
    if (!process.env.DATABASE_URL_ANALYTICS) return false;
    try {
      const { rows } = await (await db()).query(
        "select 1 from admin_intentos where ip_hash = $1 and bloqueado_hasta > now()", [ipHash]);
      return rows.length > 0;
    } catch (e: any) { console.error("admin-login: bloqueo sin base", e?.code ?? e?.message); return false; }
  },
  async fallo(ipHash: string) {
    await memoria.fallo(ipHash);
    if (!process.env.DATABASE_URL_ANALYTICS) return;
    try { await (await db()).query(SQL_FALLO, [ipHash, MAX_FALLOS]); }
    catch (e: any) { console.error("admin-login: no se registró el fallo", e?.code ?? e?.message); }
  },
  async limpiar(ipHash: string) {
    await memoria.limpiar(ipHash);
    if (!process.env.DATABASE_URL_ANALYTICS) return;
    try { await (await db()).query("delete from admin_intentos where ip_hash = $1", [ipHash]); }
    catch { /* el registro caduca solo */ }
  },
};

// Auditoría: nunca guarda lo que se escribió, solo el resultado. Si la base falla, el login sigue.
async function registrarIntento(ipHash: string, resultado: string) {
  if (!process.env.DATABASE_URL_ANALYTICS) return;
  try { await (await db()).query("insert into admin_login_log (ip_hash, resultado) values ($1, $2)", [ipHash, resultado]); }
  catch (e: any) { console.error("admin-login: no se registró el intento", e?.code ?? e?.message); }
}

// El motivo de cada rechazo (missing_env, bad_config, bad_user, bad_password, bad_totp, rate_limited,
// exception:<tipo>) se ve en Netlify → Logs → Functions → admin-login. Nunca se registran valores.
const manejar = crearManejadorLogin({ bloqueo, registrarIntento });

export default (req: Request, context: Context) => manejar(req, context);

export const config: Config = {
  path: "/api/admin/login",
  method: "POST",
  rateLimit: { windowLimit: 10, windowSize: 60, aggregateBy: ["ip", "domain"] },
};
