// Manejador de POST /api/admin/login, separado de la función de Netlify para poder probar el flujo completo.
// Orden: Origin → configuración → cuerpo → bloqueo por ip_hash → usuario + contraseña + TOTP → cookie.
// Al cliente siempre se le responde el mismo mensaje; el motivo real va solo al log del servidor, codificado,
// sin valores de entrada ni secretos.
import {
  evaluarLogin, firmarSesion, cookieSesion, origenValido, base32Decode, CABECERAS,
} from "./auth-admin.mjs";
import { hashIp } from "./visita.mjs";

const OBLIGATORIAS = ["ADMIN_PASSWORD_HASH", "ADMIN_TOTP_SECRET", "ADMIN_SESSION_SECRET"];
const B64 = "[A-Za-z0-9+/]+=*";
const FORMATO_HASH = new RegExp(`^scrypt\\$\\d+\\$\\d+\\$\\d+\\$${B64}\\$${B64}$`);
const entreComillas = (v) => /^\s*['"]|['"]\s*$/.test(v);

// Problemas de configuración detectables sin revelar valores: ausente, con comillas, con «NOMBRE=» pegado,
// truncado (p. ej. un shell que expandió los «$» del hash) o demasiado corto.
export function diagnosticarConfig(env) {
  const problemas = [];
  const conProblema = new Set();  // una sola causa por variable
  const anotar = (k, motivo) => { problemas.push(motivo); conProblema.add(k); };
  for (const k of OBLIGATORIAS) if (!env[k]) anotar(k, `missing_env:${k}`);
  for (const k of [...OBLIGATORIAS, "ADMIN_USER"]) {
    const v = env[k];
    if (!v) continue;
    if (entreComillas(v)) anotar(k, `bad_config:${k}_quoted`);
    else if (v.trimStart().startsWith(`${k}=`)) anotar(k, `bad_config:${k}_includes_name`);
  }
  const hash = env.ADMIN_PASSWORD_HASH;
  if (hash && !conProblema.has("ADMIN_PASSWORD_HASH") && !FORMATO_HASH.test(hash.trim())) problemas.push("bad_config:ADMIN_PASSWORD_HASH_format");
  const totp = env.ADMIN_TOTP_SECRET;
  if (totp && !conProblema.has("ADMIN_TOTP_SECRET")) {
    let bytes = 0;
    try { bytes = base32Decode(totp).length; } catch { /* no es base32 */ }
    if (bytes < 10) problemas.push("bad_config:ADMIN_TOTP_SECRET_format");
  }
  const sesion = env.ADMIN_SESSION_SECRET;
  if (sesion && sesion.length < 32) problemas.push("bad_config:ADMIN_SESSION_SECRET_short");
  return problemas;
}

export const respuestaRechazo = (status = 401) =>
  Response.json({ error: "No se pudo iniciar sesión. Revisa los datos o intenta más tarde." }, { status, headers: CABECERAS });

// bloqueo: { bloqueado, fallo, limpiar }; registrarIntento(ipHash, resultado) guarda la auditoría.
export function crearManejadorLogin({ bloqueo, registrarIntento = async () => {}, log = console.warn } = {}) {
  let ultimoContador = -1;  // un código TOTP no se puede reutilizar mientras viva la instancia

  return async function manejarLogin(req, context = {}, env = process.env) {
    const rechazar = (motivo, status = 401) => {
      log(`admin-login: rechazo motivo=${motivo}`);
      return respuestaRechazo(status);
    };
    try {
      if (req.method !== "POST" || !origenValido(req)) return rechazar("bad_origin", 403);
      const problemas = diagnosticarConfig(env);
      if (problemas.length) return rechazar(problemas.join(","));

      const texto = await req.text().catch(() => "");
      if (texto.length > 1024) return rechazar("bad_body");
      let body = null;
      try { body = JSON.parse(texto); } catch { return rechazar("bad_body"); }
      const campo = (k) => (typeof body?.[k] === "string" ? body[k] : "");

      const ipHash = hashIp(context.ip ?? "sin-ip", env.ANALYTICS_SALT || env.ADMIN_SESSION_SECRET);
      const r = await evaluarLogin(
        { usuario: campo("usuario"), password: campo("password"), codigo: campo("codigo").replace(/\s/g, "") },
        { usuario: env.ADMIN_USER, passwordHash: env.ADMIN_PASSWORD_HASH, totpSecreto: env.ADMIN_TOTP_SECRET },
        bloqueo, ipHash, ultimoContador);
      await registrarIntento(ipHash, r.resultado);
      if (r.resultado !== "ok") return rechazar(r.motivos.join(","));

      ultimoContador = r.contador;
      log("admin-login: acceso concedido");
      return new Response(null, {
        status: 204, headers: { ...CABECERAS, "set-cookie": cookieSesion(firmarSesion(env.ADMIN_SESSION_SECRET)) },
      });
    } catch (e) {
      return rechazar(`exception:${e?.name ?? "Error"}`);
    }
  };
}
