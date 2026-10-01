// Filtros, cláusula WHERE parametrizada y CSV del panel /admin. Ningún valor del usuario se concatena al SQL.

export const DISPOSITIVOS = ["movil", "tablet", "escritorio", "desconocido"];
export const POR_PAGINA = 50;
export const MAX_DIAS = 92;
const FECHA = /^\d{4}-\d{2}-\d{2}$/;
const DIA_MS = 86_400_000;

export const hoyLima = (d = new Date()) => new Date(d.getTime() - 5 * 3600_000).toISOString().slice(0, 10);
const sumarDias = (iso, n) => new Date(Date.parse(`${iso}T00:00:00Z`) + n * DIA_MS).toISOString().slice(0, 10);
const fechaValida = (s) => typeof s === "string" && FECHA.test(s) && !Number.isNaN(Date.parse(`${s}T00:00:00Z`))
  && new Date(`${s}T00:00:00Z`).toISOString().startsWith(s);

export function leerFiltros(params, hoy = hoyLima()) {
  let hasta = fechaValida(params.get("hasta")) ? params.get("hasta") : hoy;
  let desde = fechaValida(params.get("desde")) ? params.get("desde") : sumarDias(hasta, -6);
  if (desde > hasta) [desde, hasta] = [hasta, desde];
  if (Date.parse(hasta) - Date.parse(desde) > (MAX_DIAS - 1) * DIA_MS) desde = sumarDias(hasta, -(MAX_DIAS - 1));
  const departamento = (params.get("departamento") ?? "").trim().slice(0, 40) || null;
  const ambito = /^\d{4,6}$/.test(params.get("ambito") ?? "") ? params.get("ambito") : null;
  const dispositivo = DISPOSITIVOS.includes(params.get("dispositivo")) ? params.get("dispositivo") : null;
  const pagina = Math.min(Math.max(Number.parseInt(params.get("pagina") ?? "1", 10) || 1, 1), 10_000);
  return { desde, hasta, departamento, ambito, dispositivo, bots: params.get("bots") === "1", pagina };
}

// Fechas en hora de Lima: [desde 00:00, hasta+1 00:00)
export function construirWhere(f) {
  const valores = [f.desde, f.hasta];
  const partes = [
    "inicio >= ($1::date)::timestamp at time zone 'America/Lima'",
    "inicio < (($2::date) + 1)::timestamp at time zone 'America/Lima'",
  ];
  const agregar = (sql, v) => { valores.push(v); partes.push(sql.replace("?", `$${valores.length}`)); };
  if (f.departamento) agregar("departamento = ?", f.departamento);
  if (f.ambito) agregar("?::text = any(ambitos_visitados)", f.ambito);
  if (f.dispositivo) agregar("dispositivo_tipo = ?", f.dispositivo);
  if (!f.bots) partes.push("not es_bot");
  return { sql: partes.join(" and "), valores };
}

export const COLUMNAS_SESION = `
  to_char(inicio at time zone 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') as inicio,
  to_char(coalesce(fin, ultima_senal) at time zone 'America/Lima', 'YYYY-MM-DD HH24:MI:SS') as desconexion,
  (fin is not null) as con_fin, duracion_seg, dispositivo_tipo, so, so_version, navegador, navegador_version,
  pais, departamento, provincia, distrito, ubigeo_geo, precision_geo, ambito_inicial, ambitos_visitados, es_bot`;

const CABECERA_CSV = [
  ["inicio", "inicio_lima"], ["desconexion", "desconexion_lima"], ["con_fin", "con_evento_fin"], ["duracion_seg", "duracion_seg"],
  ["dispositivo_tipo", "dispositivo"], ["so", "so"], ["so_version", "so_version"], ["navegador", "navegador"],
  ["navegador_version", "navegador_version"], ["pais", "pais"], ["departamento", "departamento"], ["provincia", "provincia"],
  ["distrito", "distrito"], ["ubigeo_geo", "ubigeo_geo"], ["precision_geo", "precision_geo"],
  ["ambito_inicial", "ambito_inicial"], ["ambitos_visitados", "ambitos_visitados"], ["es_bot", "es_bot"],
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
  return "﻿" + lineas.join("\r\n") + "\r\n";
}
