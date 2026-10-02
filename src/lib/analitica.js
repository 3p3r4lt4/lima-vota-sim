// Analítica propia, sin cookies ni terceros. Fire-and-forget: nada de esto puede romper la página.
// La sesión vive en sessionStorage y muere al cerrar la pestaña. Se respeta Do Not Track y GPC.
// El user-agent no se envía: el servidor lo lee del header. De las preguntas solo se envía que hubo una.
// ANALYTICS_ENABLED=false en el build (vite.config.js → __ANALITICA__) deja todo esto inerte.

const API = "/api/visita";
const CLAVE = "lv_sesion";
const LATIDO_MS = 30_000;
const UBIGEO = /^\d{4,6}$/;
const VISTAS = ["fichas", "comparar"];
const RUTA = /^\/[A-Za-z0-9/._-]{0,80}$/;
const UTM = /^[A-Za-z0-9 ._+-]{1,80}$/;

let activo = false;
let sesion = null;
let ambitoActual = null;
let vistaActual = null;
let temporizador = null;
let finEnviado = false;
let quitar = [];

// Se leen al cargar el módulo, antes de que la app reescriba la URL
const utmInicial = (() => {
  try {
    const q = new URLSearchParams(location.search);
    const out = {};
    for (const [k, c] of [["utm_source", "us"], ["utm_medium", "um"], ["utm_campaign", "uc"]]) {
      const v = (q.get(k) ?? "").trim().slice(0, 80);
      if (UTM.test(v)) out[c] = v;
    }
    return out;
  } catch {
    return {};
  }
})();

const ruta = () => (RUTA.test(location.pathname) ? location.pathname : undefined);

function permitido() {
  try {
    if (!__ANALITICA__) return false;
    if (navigator.doNotTrack === "1" || window.doNotTrack === "1" || navigator.globalPrivacyControl === true) return false;
    return !navigator.webdriver && typeof crypto?.randomUUID === "function";
  } catch {
    return false;
  }
}

function idSesion() {
  try {
    let id = sessionStorage.getItem(CLAVE);
    if (!/^[0-9a-f-]{36}$/.test(id ?? "")) {
      id = crypto.randomUUID();
      sessionStorage.setItem(CLAVE, id);
    }
    return id;
  } catch {
    return crypto.randomUUID();  // sessionStorage bloqueado: sesión solo en memoria
  }
}

function referente() {
  try {
    if (!document.referrer) return undefined;
    const host = new URL(document.referrer).hostname;
    return host && host !== location.hostname ? host : undefined;
  } catch {
    return undefined;
  }
}

function enviar(e, extra = {}, alSalir = false) {
  try {
    const cuerpo = JSON.stringify({ e, s: sesion, ...(ambitoActual ? { a: ambitoActual } : {}), ...extra });
    // text/plain: sendBeacon no admite otros tipos sin preflight; el servidor parsea el JSON igual
    if (alSalir && navigator.sendBeacon?.(API, cuerpo)) return;
    fetch(API, { method: "POST", body: cuerpo, keepalive: true, credentials: "omit", headers: { "content-type": "text/plain" } })
      .catch(() => {});
  } catch {
    /* sin analítica */
  }
}

function programarLatido() {
  clearInterval(temporizador);
  temporizador = setInterval(() => { if (!document.hidden) enviar("latido"); }, LATIDO_MS);
}

function salir() {
  if (finEnviado) return;
  finEnviado = true;
  clearInterval(temporizador);
  enviar("fin", {}, true);
}

function alCambiarVisibilidad() {
  if (document.hidden) return salir();
  if (finEnviado) {  // volvió a la pestaña: se reabre la sesión
    finEnviado = false;
    enviar("latido");
  }
  programarLatido();
}

export function iniciarAnalitica(ambito, vista) {
  try {
    if (activo || !permitido()) return;
    activo = true;
    sesion = idSesion();
    ambitoActual = UBIGEO.test(ambito ?? "") ? ambito : null;  // ?ambito= viene de la URL
    vistaActual = VISTAS.includes(vista) ? vista : null;
    finEnviado = false;
    const pantalla = `${Math.round(screen.width)}x${Math.round(screen.height)}`;
    enviar("inicio", {
      p: pantalla, i: (navigator.language ?? "").slice(0, 20) || undefined, r: referente(),
      v: vistaActual ?? undefined, t: ruta(), ...utmInicial,
    });
    if (!document.hidden) programarLatido();
    document.addEventListener("visibilitychange", alCambiarVisibilidad);
    addEventListener("pagehide", salir);
    addEventListener("pageshow", alCambiarVisibilidad);  // vuelta desde el bfcache
    quitar = [
      () => document.removeEventListener("visibilitychange", alCambiarVisibilidad),
      () => removeEventListener("pagehide", salir),
      () => removeEventListener("pageshow", alCambiarVisibilidad),
    ];
  } catch {
    activo = false;
  }
}

export function registrarAmbito(ubigeo) {
  try {
    if (!activo || !UBIGEO.test(ubigeo ?? "") || ubigeo === ambitoActual) return;
    ambitoActual = ubigeo;
    enviar("ambito");
  } catch {
    /* sin analítica */
  }
}

export function registrarVista(vista) {
  try {
    if (!activo || !VISTAS.includes(vista) || vista === vistaActual) return;
    vistaActual = vista;
    enviar("vista", { v: vista, t: ruta() });
  } catch {
    /* sin analítica */
  }
}

// Solo cuenta la pregunta; su texto nunca sale de /api/preguntar
export function registrarPregunta() {
  try {
    if (activo) enviar("pregunta");
  } catch {
    /* sin analítica */
  }
}

export function detenerAnalitica() {
  clearInterval(temporizador);
  quitar.forEach((f) => f());
  quitar = [];
  activo = false;
}
