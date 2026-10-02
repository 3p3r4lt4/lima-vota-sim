// Autenticación del panel /admin: contraseña scrypt, TOTP (RFC 6238) y cookie de sesión firmada con HMAC.
// Solo node:crypto, sin dependencias. Todas las comparaciones de secretos son de tiempo constante.
import { scrypt as scryptCb, randomBytes, timingSafeEqual, createHmac, createHash } from "node:crypto";
import { promisify } from "node:util";

const scrypt = promisify(scryptCb);

export const COOKIE = "__Host-lv_admin";
export const DURACION_SEG = 8 * 3600;
export const MAX_FALLOS = 5;
export const BLOQUEO_MS = 15 * 60_000;
export const CABECERAS = { "cache-control": "no-store", "x-robots-tag": "noindex, nofollow" };

const iguales = (a, b) => a.length === b.length && timingSafeEqual(a, b);

// ---------- Contraseña: "scrypt$N$r$p$sal$hash" (sal y hash en base64) ----------

export async function hashPassword(password, { N = 2 ** 15, r = 8, p = 1 } = {}) {
  const sal = randomBytes(16);
  const h = await scrypt(String(password).normalize("NFKC"), sal, 32, { N, r, p, maxmem: 256 * N * r });
  return `scrypt$${N}$${r}$${p}$${sal.toString("base64")}$${h.toString("base64")}`;
}

export async function verificarPassword(password, guardado) {
  try {
    const partes = String(guardado ?? "").split("$");
    if (partes.length !== 6 || partes[0] !== "scrypt") return false;
    const [N, r, p] = partes.slice(1, 4).map(Number);
    // Parámetros acotados: un hash manipulado no puede forzar un cálculo gigante
    if (!Number.isInteger(Math.log2(N)) || N < 2 ** 14 || N > 2 ** 20 || r < 1 || r > 32 || p < 1 || p > 4) return false;
    const sal = Buffer.from(partes[4], "base64");
    const esperado = Buffer.from(partes[5], "base64");
    if (sal.length < 16 || esperado.length < 16 || typeof password !== "string" || password.length > 256) return false;
    const h = await scrypt(password.normalize("NFKC"), sal, esperado.length, { N, r, p, maxmem: 256 * N * r });
    return iguales(h, esperado);
  } catch {
    return false;
  }
}

// ---------- Usuario (opcional): sin ADMIN_USER configurado se acepta cualquiera ----------

// Se comparan los SHA-256 para que el tiempo no dependa de la longitud ni del prefijo
const sha = (s) => createHash("sha256").update(String(s).normalize("NFKC").trim().toLowerCase()).digest();
export const usuarioValido = (usuario, esperado) =>
  !esperado || (typeof usuario === "string" && usuario.length <= 64 && iguales(sha(usuario), sha(esperado)));

// ---------- TOTP (RFC 6238, HMAC-SHA1, 30 s, 6 dígitos) ----------

const B32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

export function base32Encode(buf) {
  let bits = 0, valor = 0, out = "";
  for (const byte of buf) {
    valor = (valor << 8) | byte;
    bits += 8;
    while (bits >= 5) { out += B32[(valor >>> (bits - 5)) & 31]; bits -= 5; }
  }
  if (bits > 0) out += B32[(valor << (5 - bits)) & 31];
  return out;
}

export function base32Decode(texto) {
  const limpio = String(texto ?? "").toUpperCase().replace(/[\s=-]/g, "");
  let bits = 0, valor = 0;
  const out = [];
  for (const c of limpio) {
    const i = B32.indexOf(c);
    if (i < 0) throw new Error("base32 inválido");
    valor = (valor << 5) | i;
    bits += 5;
    if (bits >= 8) { out.push((valor >>> (bits - 8)) & 255); bits -= 8; }
  }
  return Buffer.from(out);
}

export function hotp(clave, contador, { digitos = 6, algoritmo = "sha1" } = {}) {
  const msg = Buffer.alloc(8);
  msg.writeBigUInt64BE(BigInt(contador));
  const h = createHmac(algoritmo, clave).update(msg).digest();
  const o = h[h.length - 1] & 0x0f;
  const n = ((h[o] & 0x7f) << 24) | (h[o + 1] << 16) | (h[o + 2] << 8) | h[o + 3];
  return String(n % 10 ** digitos).padStart(digitos, "0");
}

export const totp = (clave, ahoraMs = Date.now(), opciones = {}) =>
  hotp(clave, Math.floor(ahoraMs / 1000 / 30), opciones);

// Devuelve el contador que coincide (para impedir reusar un código) o -1. Revisa toda la ventana sin cortar antes.
export function verificarTotp(codigo, secretoBase32, ahoraMs = Date.now(), ventana = 1) {
  if (typeof codigo !== "string" || !/^\d{6}$/.test(codigo)) return -1;
  let clave;
  try { clave = base32Decode(secretoBase32); } catch { return -1; }
  if (clave.length < 10) return -1;
  const actual = Math.floor(ahoraMs / 1000 / 30);
  let encontrado = -1;
  for (let d = -ventana; d <= ventana; d++) {
    if (iguales(Buffer.from(hotp(clave, actual + d)), Buffer.from(codigo)) && encontrado < 0) encontrado = actual + d;
  }
  return encontrado;
}

// ---------- Cookie de sesión: base64url(payload).base64url(HMAC-SHA256) ----------

const firmar = (datos, secreto) => createHmac("sha256", secreto).update(datos).digest("base64url");

export function firmarSesion(secreto, ahoraMs = Date.now(), duracionSeg = DURACION_SEG) {
  const iat = Math.floor(ahoraMs / 1000);
  const datos = Buffer.from(JSON.stringify({ sub: "admin", iat, exp: iat + duracionSeg })).toString("base64url");
  return `${datos}.${firmar(datos, secreto)}`;
}

export function verificarSesion(token, secreto, ahoraMs = Date.now()) {
  try {
    if (!secreto || typeof token !== "string" || token.length > 512) return null;
    const [datos, firma, ...resto] = token.split(".");
    if (!datos || !firma || resto.length) return null;
    if (!iguales(Buffer.from(firma), Buffer.from(firmar(datos, secreto)))) return null;
    const p = JSON.parse(Buffer.from(datos, "base64url").toString("utf8"));
    const ahora = Math.floor(ahoraMs / 1000);
    if (p.sub !== "admin" || !Number.isInteger(p.exp) || p.exp <= ahora || p.iat > ahora + 60) return null;
    return p;
  } catch {
    return null;
  }
}

export const cookieSesion = (token) =>
  `${COOKIE}=${token}; Path=/; Max-Age=${DURACION_SEG}; HttpOnly; Secure; SameSite=Strict`;
export const cookieBorrar = () => `${COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Strict`;

export function leerCookie(req, nombre = COOKIE) {
  for (const parte of (req.headers.get("cookie") ?? "").split(";")) {
    const i = parte.indexOf("=");
    if (i > 0 && parte.slice(0, i).trim() === nombre) return parte.slice(i + 1).trim();
  }
  return null;
}

const secretoSesion = () => {
  const s = process.env.ADMIN_SESSION_SECRET ?? "";
  return s.length >= 32 ? s : null;
};

// Usado por todos los endpoints admin. Sin secreto configurado nadie entra.
export function esAdmin(req, ahoraMs = Date.now()) {
  const secreto = secretoSesion();
  return Boolean(secreto && verificarSesion(leerCookie(req), secreto, ahoraMs));
}

export const noAutorizado = () => new Response(null, { status: 401, headers: CABECERAS });

// CSRF: los POST del panel deben venir del propio sitio
export function origenValido(req) {
  const sitio = req.headers.get("sec-fetch-site");
  if (sitio && sitio !== "same-origin") return false;
  const origen = req.headers.get("origin");
  if (!origen) return false;
  try { return new URL(origen).origin === new URL(req.url).origin; } catch { return false; }
}

// ---------- Decisión de un intento de login ----------
// cfg: { usuario?, passwordHash, totpSecreto }. Se verifican todos los factores siempre, para no revelar
// cuál falló por el tiempo de respuesta. Devuelve { resultado: "ok" | "fallo" | "bloqueado", contador?, motivos? }.
// «motivos» es solo para el log del servidor; al cliente siempre se le responde lo mismo.
export async function evaluarLogin({ usuario, password, codigo }, cfg, bloqueo, clave, ultimoContador = -1, ahoraMs = Date.now()) {
  if (await bloqueo.bloqueado(clave)) return { resultado: "bloqueado", motivos: ["rate_limited"] };
  const okUsuario = usuarioValido(usuario, cfg.usuario);
  const okPassword = await verificarPassword(password, cfg.passwordHash);
  const contador = verificarTotp(codigo, cfg.totpSecreto, ahoraMs);
  if (!okUsuario || !okPassword || contador < 0 || contador <= ultimoContador) {
    const motivos = [];
    if (!okUsuario) motivos.push("bad_user");
    if (!okPassword) motivos.push("bad_password");
    if (contador >= 0 && contador <= ultimoContador) motivos.push("bad_totp:reused");
    else if (contador < 0) {
      // ¿Coincide con una ventana más amplia? Entonces el reloj del teléfono está desfasado
      motivos.push(verificarTotp(codigo, cfg.totpSecreto, ahoraMs, 10) >= 0 ? "bad_totp:clock_skew" : "bad_totp");
    }
    await bloqueo.fallo(clave);
    return { resultado: "fallo", motivos };
  }
  await bloqueo.limpiar(clave);
  return { resultado: "ok", contador };
}

// ---------- Bloqueo por intentos fallidos (versión en memoria; admin-login usa la tabla si hay base) ----------

export function crearBloqueoMemoria({ maxFallos = MAX_FALLOS, bloqueoMs = BLOQUEO_MS } = {}) {
  const m = new Map();
  return {
    async bloqueado(clave, ahora = Date.now()) {
      return (m.get(clave)?.hasta ?? 0) > ahora;
    },
    async fallo(clave, ahora = Date.now()) {
      let e = m.get(clave);
      if (!e || ahora - e.desde >= bloqueoMs) e = { desde: ahora, fallos: 0, hasta: 0 };
      e.fallos += 1;
      if (e.fallos >= maxFallos) e.hasta = ahora + bloqueoMs;
      m.set(clave, e);
      if (m.size > 5000) for (const [k, v] of m) if (v.hasta < ahora && ahora - v.desde >= bloqueoMs) m.delete(k);
    },
    async limpiar(clave) {
      m.delete(clave);
    },
  };
}
