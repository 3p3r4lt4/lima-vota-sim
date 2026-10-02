import type { Config, Context } from "@netlify/functions";
import {
  evaluarLogin, firmarSesion, cookieSesion, origenValido, crearBloqueoMemoria,
  CABECERAS, MAX_FALLOS,
} from "../lib/auth-admin.mjs";
import { hashIp } from "../lib/visita.mjs";

// Login del panel: usuario (si ADMIN_USER está definido) + contraseña (scrypt) + código TOTP.
// Cualquier fallo responde el mismo mensaje. Cada intento queda en admin_login_log (solo ip_hash y resultado).
// Bloqueo: 5 fallos por ip_hash → 15 min, guardado en admin_intentos (respaldo en memoria si no hay base),
// más el rateLimit de la plataforma.

const memoria = crearBloqueoMemoria();
let ultimoContador = -1;  // un código TOTP no se puede reutilizar mientras viva la instancia

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
async function registrarIntento(ipHash: string, resultado: "ok" | "fallo" | "bloqueado") {
  if (!process.env.DATABASE_URL_ANALYTICS) return;
  try { await (await db()).query("insert into admin_login_log (ip_hash, resultado) values ($1, $2)", [ipHash, resultado]); }
  catch (e: any) { console.error("admin-login: no se registró el intento", e?.code ?? e?.message); }
}

const rechazo = (status = 401) =>
  Response.json({ error: "No se pudo iniciar sesión. Revisa los datos o intenta más tarde." }, { status, headers: CABECERAS });

export default async (req: Request, context: Context) => {
  if (req.method !== "POST" || !origenValido(req)) return rechazo(403);
  const { ADMIN_PASSWORD_HASH, ADMIN_TOTP_SECRET, ADMIN_SESSION_SECRET } = process.env;
  if (!ADMIN_PASSWORD_HASH || !ADMIN_TOTP_SECRET || !ADMIN_SESSION_SECRET || ADMIN_SESSION_SECRET.length < 32) return rechazo();

  const texto = await req.text().catch(() => "");
  if (texto.length > 1024) return rechazo();
  let body: any = null;
  try { body = JSON.parse(texto); } catch { /* cuerpo inválido */ }
  const password = typeof body?.password === "string" ? body.password : "";
  const codigo = typeof body?.codigo === "string" ? body.codigo.replace(/\s/g, "") : "";
  const usuario = typeof body?.usuario === "string" ? body.usuario : "";

  const ipHash = hashIp(context.ip ?? "sin-ip", process.env.ANALYTICS_SALT || ADMIN_SESSION_SECRET);
  const r = await evaluarLogin(
    { usuario, password, codigo },
    { usuario: process.env.ADMIN_USER, passwordHash: ADMIN_PASSWORD_HASH, totpSecreto: ADMIN_TOTP_SECRET },
    bloqueo, ipHash, ultimoContador);
  await registrarIntento(ipHash, r.resultado);
  if (r.resultado !== "ok") return rechazo();

  ultimoContador = r.contador;
  return new Response(null, { status: 204, headers: { ...CABECERAS, "set-cookie": cookieSesion(firmarSesion(ADMIN_SESSION_SECRET)) } });
};

export const config: Config = {
  path: "/api/admin/login",
  method: "POST",
  rateLimit: { windowLimit: 10, windowSize: 60, aggregateBy: ["ip", "domain"] },
};
