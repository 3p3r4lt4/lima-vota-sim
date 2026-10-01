// Piezas puras de /api/visita: validación del payload, hash de la IP y límite de eventos en memoria.
import { createHmac } from "node:crypto";

export const EVENTOS = ["inicio", "latido", "ambito", "fin"];
export const MAX_BODY = 1024;

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
const UBIGEO = /^\d{4,6}$/;
const PANTALLA = /^\d{2,5}x\d{2,5}$/;
const IDIOMA = /^[a-z]{2,3}(-[a-z0-9]{2,8}){0,2}$/i;
const HOST = /^(?=.{1,253}$)[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)*$/;
const PERMITIDOS = new Set(["e", "s", "a", "p", "i", "r"]);

// Payload compacto: { e: evento, s: sesion_id, a: ámbito, p: pantalla, i: idioma, r: host de referencia }.
// Devuelve { ok: true, evento } o { ok: false, motivo }; cualquier campo inesperado invalida el evento.
export function validarEvento(texto) {
  if (typeof texto !== "string" || texto.length === 0 || texto.length > MAX_BODY) return { ok: false, motivo: "tamaño" };
  let b;
  try { b = JSON.parse(texto); } catch { return { ok: false, motivo: "json" }; }
  if (!b || typeof b !== "object" || Array.isArray(b)) return { ok: false, motivo: "json" };
  if (Object.keys(b).some((k) => !PERMITIDOS.has(k))) return { ok: false, motivo: "campo" };

  const opcional = (v, re, max) => {
    if (v === undefined || v === null || v === "") return { ok: true, v: null };
    return typeof v === "string" && v.length <= max && re.test(v) ? { ok: true, v } : { ok: false };
  };
  if (!EVENTOS.includes(b.e)) return { ok: false, motivo: "evento" };
  if (typeof b.s !== "string" || !UUID.test(b.s.toLowerCase())) return { ok: false, motivo: "sesion" };
  const a = opcional(b.a, UBIGEO, 6), p = opcional(b.p, PANTALLA, 11), i = opcional(b.i, IDIOMA, 20);
  const r = opcional(typeof b.r === "string" ? b.r.toLowerCase() : b.r, HOST, 253);
  if (!a.ok) return { ok: false, motivo: "ambito" };
  if (!p.ok || !i.ok || !r.ok) return { ok: false, motivo: "formato" };
  if (b.e === "ambito" && !a.v) return { ok: false, motivo: "ambito" };

  return { ok: true, evento: { tipo: b.e, sesion_id: b.s.toLowerCase(), ambito: a.v, pantalla: p.v, idioma: i.v, referer_host: r.v } };
}

// Perú no tiene horario de verano: UTC−5 fijo.
export const fechaLima = (d = new Date()) => new Date(d.getTime() - 5 * 3600_000).toISOString().slice(0, 10).replaceAll("-", "");

// La sal cambia cada día: el mismo visitante no se puede seguir entre días ni revertir sin la sal.
export const hashIp = (ip, sal, d = new Date()) => createHmac("sha256", sal + fechaLima(d)).update(String(ip)).digest("hex");

// Ventana fija por clave. Vive mientras viva la instancia de la función; el límite de la plataforma
// (config.rateLimit) es el respaldo entre instancias.
export function crearLimitador({ max = 60, ventanaMs = 60_000, maxClaves = 10_000 } = {}) {
  const cubetas = new Map();
  return function permitir(clave, ahora = Date.now()) {
    let c = cubetas.get(clave);
    if (!c || ahora - c.desde >= ventanaMs) {
      if (cubetas.size >= maxClaves) for (const [k, v] of cubetas) if (ahora - v.desde >= ventanaMs) cubetas.delete(k);
      if (cubetas.size >= maxClaves) cubetas.clear();
      c = { desde: ahora, n: 0 };
      cubetas.set(clave, c);
    }
    c.n += 1;
    return c.n <= max;
  };
}

// El Origin, si viene, debe ser el del propio sitio (sendBeacon y fetch lo envían en POST)
export function mismoOrigen(req) {
  const origen = req.headers.get("origin");
  const sitio = req.headers.get("sec-fetch-site");
  if (sitio && !["same-origin", "none"].includes(sitio)) return false;
  if (!origen) return true;
  try { return new URL(origen).host === new URL(req.url).host; } catch { return false; }
}
