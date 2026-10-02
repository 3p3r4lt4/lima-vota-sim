// Filtros, cláusula WHERE parametrizada y CSV del panel /admin. Ningún valor del usuario se concatena al SQL.
// Las consultas usan el alias «v» para visitas_sesion (se cruza con ref_ubigeo y analytics_eventos).

export const DISPOSITIVOS = ["movil", "tablet", "escritorio", "desconocido"];
export const POR_PAGINA = 50;
export const MAX_DIAS = 92;
// Una sesión sin «fin» y sin latido en este plazo se da por cerrada en su última señal
export const ACTIVA_SEG = 120;
const FECHA = /^\d{4}-\d{2}-\d{2}$/;
const DIA_MS = 86_400_000;

export const hoyLima = (d = new Date()) => new Date(d.getTime() - 5 * 3600_000).toISOString().slice(0, 10);
// Perú no tiene horario de verano: UTC−5 fijo
export const fechaHoraLima = (d) => (d ? new Date(new Date(d).getTime() - 5 * 3600_000).toISOString().slice(0, 19).replace("T", " ") : null);
const sumarDias = (iso, n) => new Date(Date.parse(`${iso}T00:00:00Z`) + n * DIA_MS).toISOString().slice(0, 10);
const fechaValida = (s) => typeof s === "string" && FECHA.test(s) && !Number.isNaN(Date.parse(`${s}T00:00:00Z`))
  && new Date(`${s}T00:00:00Z`).toISOString().startsWith(s);
const texto = (params, k) => (params.get(k) ?? "").trim().slice(0, 60) || null;

export function leerFiltros(params, hoy = hoyLima()) {
  let hasta = fechaValida(params.get("hasta")) ? params.get("hasta") : hoy;
  let desde = fechaValida(params.get("desde")) ? params.get("desde") : sumarDias(hasta, -6);
  if (desde > hasta) [desde, hasta] = [hasta, desde];
  if (Date.parse(hasta) - Date.parse(desde) > (MAX_DIAS - 1) * DIA_MS) desde = sumarDias(hasta, -(MAX_DIAS - 1));
  const ambito = /^\d{4,6}$/.test(params.get("ambito") ?? "") ? params.get("ambito") : null;
  const dispositivo = DISPOSITIVOS.includes(params.get("dispositivo")) ? params.get("dispositivo") : null;
  const pagina = Math.min(Math.max(Number.parseInt(params.get("pagina") ?? "1", 10) || 1, 1), 10_000);
  return {
    desde, hasta, departamento: texto(params, "departamento"), provincia: texto(params, "provincia"),
    distrito: texto(params, "distrito"), ambito, dispositivo, bots: params.get("bots") === "1", pagina,
  };
}

// Fechas en hora de Lima: [desde 00:00, hasta+1 00:00)
export function construirWhere(f) {
  const valores = [f.desde, f.hasta];
  const partes = [
    "v.inicio >= ($1::date)::timestamp at time zone 'America/Lima'",
    "v.inicio < (($2::date) + 1)::timestamp at time zone 'America/Lima'",
  ];
  const agregar = (sql, x) => { valores.push(x); partes.push(sql.replace("?", `$${valores.length}`)); };
  if (f.departamento) agregar("v.departamento = ?", f.departamento);
  if (f.provincia) agregar("v.provincia = ?", f.provincia);
  if (f.distrito) agregar("v.distrito = ?", f.distrito);
  if (f.ambito) agregar("?::text = any(v.ambitos_visitados)", f.ambito);
  if (f.dispositivo) agregar("v.dispositivo_tipo = ?", f.dispositivo);
  if (!f.bots) partes.push("not v.es_bot");
  return { sql: partes.join(" and "), valores };
}

// Requiere: from visitas_sesion v left join ref_ubigeo ra on ra.ubigeo = v.ambito_inicial
export const COLUMNAS_SESION = `
  v.inicio, v.ultima_senal, v.fin, v.dispositivo_tipo, v.so, v.so_version, v.navegador, v.navegador_version,
  v.pais, v.departamento, v.provincia, v.distrito, v.ubigeo_geo, v.precision_geo,
  v.ambito_inicial, ra.departamento as ambito_departamento, ra.provincia as ambito_provincia, ra.distrito as ambito_distrito,
  v.ambitos_visitados, v.preguntas_count, v.utm_source, v.utm_medium, v.utm_campaign, v.referer_host, v.es_bot,
  array(select distinct e.vista from analytics_eventos e
        where e.sesion_id = v.sesion_id and e.vista is not null order by 1) as vistas`;
export const FROM_SESIONES = "visitas_sesion v left join ref_ubigeo ra on ra.ubigeo = v.ambito_inicial";

// Desconexión = «fin» si llegó el beacon; si no, el último latido. Sin latido en ACTIVA_SEG, la sesión está cerrada.
export function estadoSesion({ inicio, ultima_senal, fin }, ahora = new Date()) {
  const ms = (x) => (x === null || x === undefined ? null : new Date(x).getTime());
  const i = ms(inicio), f = ms(fin);
  const u = ms(ultima_senal) ?? i;
  const activa = f === null && ahora.getTime() - u <= ACTIVA_SEG * 1000;
  const corte = f ?? u;
  return {
    activa,
    con_fin: f !== null,
    desconexion: activa ? null : new Date(corte),
    duracion_seg: Math.max(0, Math.round((corte - i) / 1000)),
  };
}

// Fila de la base → fila del panel/CSV con horas de Lima y duración calculada
export function prepararSesion(fila, ahora = new Date()) {
  const { inicio, ultima_senal, fin, ...resto } = fila;
  const e = estadoSesion({ inicio, ultima_senal, fin }, ahora);
  return {
    ...resto, inicio: fechaHoraLima(inicio), desconexion: fechaHoraLima(e.desconexion),
    activa: e.activa, con_fin: e.con_fin, duracion_seg: e.duracion_seg,
  };
}

const CABECERA_CSV = [
  ["inicio", "inicio_lima"], ["desconexion", "desconexion_lima"], ["activa", "en_curso"], ["con_fin", "con_evento_fin"],
  ["duracion_seg", "duracion_seg"], ["dispositivo_tipo", "dispositivo"], ["so", "so"], ["so_version", "so_version"],
  ["navegador", "navegador"], ["navegador_version", "navegador_version"], ["pais", "pais"],
  ["departamento", "departamento_ip"], ["provincia", "provincia_ip"], ["distrito", "distrito_ip"],
  ["ubigeo_geo", "ubigeo_ip"], ["precision_geo", "precision_ip"],
  ["ambito_inicial", "ambito_inicial"], ["ambito_departamento", "ambito_departamento"],
  ["ambito_provincia", "ambito_provincia"], ["ambito_distrito", "ambito_distrito"], ["ambitos_visitados", "ambitos_visitados"],
  ["vistas", "vistas"], ["preguntas_count", "preguntas"], ["referer_host", "referer"],
  ["utm_source", "utm_source"], ["utm_medium", "utm_medium"], ["utm_campaign", "utm_campaign"], ["es_bot", "es_bot"],
];

// Escapa comillas y separadores, y neutraliza fórmulas (=, +, -, @) para hojas de cálculo
export function celdaCsv(v) {
  if (v === null || v === undefined) return "";
  let s = Array.isArray(v) ? v.join(" ") : String(v);
  if (/^[=+\-@\t\r]/.test(s)) s = `'${s}`;
  return /[",\r\n]/.test(s) ? `"${s.replaceAll('"', '""')}"` : s;
}

export function aCsv(filas) {
  const lineas = [CABECERA_CSV.map(([, t]) => t).join(",")];
  for (const f of filas) lineas.push(CABECERA_CSV.map(([k]) => celdaCsv(f[k])).join(","));
  return "\uFEFF" + lineas.join("\r\n") + "\r\n";
}
