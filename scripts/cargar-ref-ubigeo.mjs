#!/usr/bin/env node
// Carga el catálogo de ubigeos INEI en ref_ubigeo: departamentos (2 dígitos), provincias (4) y distritos (6).
//
// Fuente: ubigeo_distrito.csv de https://github.com/jmcastagnetto/ubigeo-peru-aumentado (columna «inei»),
// una compilación de los códigos y nombres de INEI. Revisa su licencia antes de redistribuir el archivo.
// Los nombres vienen en mayúsculas y sin tildes; se pasan a «Título» y se usan los nombres con tildes
// de netlify/lib/ubigeo-geo.mjs donde existen (departamentos, provincias de Lima, distritos de Lima).
//
//   node scripts/cargar-ref-ubigeo.mjs --dry-run              (descarga y valida, no escribe)
//   DATABASE_URL_ADMIN=... node scripts/cargar-ref-ubigeo.mjs [ruta/local.csv]
//
// Es idempotente (upsert por ubigeo). Requiere haber ejecutado db/analytics_eventos.sql.
import { readFile } from "node:fs/promises";
import { pathToFileURL } from "node:url";
import { DEPARTAMENTOS, PROVINCIAS, DISTRITOS_LIMA } from "../netlify/lib/ubigeo-geo.mjs";

export const FUENTE = "https://raw.githubusercontent.com/jmcastagnetto/ubigeo-peru-aumentado/main/ubigeo_distrito.csv";

// CSV con comillas dobles (RFC 4180)
export function filasCsv(texto) {
  const filas = [];
  let fila = [], campo = "", comillas = false;
  for (let i = 0; i < texto.length; i++) {
    const c = texto[i];
    if (comillas) {
      if (c === '"' && texto[i + 1] === '"') { campo += '"'; i++; }
      else if (c === '"') comillas = false;
      else campo += c;
    } else if (c === '"') comillas = true;
    else if (c === ",") { fila.push(campo); campo = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && texto[i + 1] === "\n") i++;
      fila.push(campo); campo = "";
      if (fila.some((x) => x !== "")) filas.push(fila);
      fila = [];
    } else campo += c;
  }
  fila.push(campo);
  if (fila.some((x) => x !== "")) filas.push(fila);
  return filas;
}

const MINUSCULAS = new Set(["de", "del", "la", "las", "los", "y", "e"]);
export const titulo = (s) => String(s).trim().toLowerCase().replace(/\s+/g, " ").split(" ")
  .map((p, i) => (i > 0 && MINUSCULAS.has(p) ? p : p.charAt(0).toUpperCase() + p.slice(1))).join(" ");

const NOMBRE_DEP = new Map(DEPARTAMENTOS.map((d) => [d.ubigeo, d.nombre]));
const NOMBRE_PROV = new Map(PROVINCIAS.map((p) => [p.ubigeo, p.nombre]));
const NOMBRE_DIST = new Map(DISTRITOS_LIMA.map((d) => [d.ubigeo, d.nombre]));

export function construirCatalogo(filas) {
  const [cab, ...datos] = filas;
  const col = (n) => {
    const i = cab.findIndex((x) => x.trim().toLowerCase() === n);
    if (i < 0) throw new Error(`Falta la columna «${n}» en el CSV`);
    return i;
  };
  const [cU, cDep, cProv, cDist] = ["inei", "departamento", "provincia", "distrito"].map(col);
  const deps = new Map(), provs = new Map(), dists = new Map();
  const fijar = (m, k, v) => {
    if (m.has(k) && m.get(k) !== v) throw new Error(`Nombres distintos para el ubigeo ${k}: «${m.get(k)}» y «${v}»`);
    m.set(k, v);
  };

  const omitidas = [];
  for (const f of datos) {
    // La fuente marca con NA los distritos sin código INEI asignado todavía
    if (/^(na)?$/i.test((f[cU] ?? "").trim())) { omitidas.push(titulo(f[cDist] ?? "?")); continue; }
    const u = (f[cU] ?? "").trim().padStart(6, "0");
    if (!/^\d{6}$/.test(u)) throw new Error(`Ubigeo inválido: «${f[cU]}»`);
    const dep = NOMBRE_DEP.get(u.slice(0, 2)) ?? titulo(f[cDep]);
    const prov = NOMBRE_PROV.get(u.slice(0, 4)) ?? titulo(f[cProv]);
    fijar(deps, u.slice(0, 2), dep);
    fijar(provs, u.slice(0, 4), prov);
    if (dists.has(u)) throw new Error(`Ubigeo repetido: ${u}`);
    dists.set(u, NOMBRE_DIST.get(u) ?? titulo(f[cDist]));
  }

  const out = [];
  for (const [u, d] of deps) out.push({ ubigeo: u, departamento: d, provincia: null, distrito: null });
  for (const [u, p] of provs) out.push({ ubigeo: u, departamento: deps.get(u.slice(0, 2)), provincia: p, distrito: null });
  for (const [u, d] of dists) {
    out.push({ ubigeo: u, departamento: deps.get(u.slice(0, 2)), provincia: provs.get(u.slice(0, 4)), distrito: d });
  }
  out.sort((a, b) => a.ubigeo.localeCompare(b.ubigeo));
  return { catalogo: out, omitidas };
}

// Comprobaciones de cordura: el catálogo debe estar completo antes de tocar la base
export function validarCatalogo(c) {
  const n = (len) => c.filter((x) => x.ubigeo.length === len).length;
  const errores = [];
  if (n(2) !== 25) errores.push(`se esperaban 25 departamentos y hay ${n(2)}`);
  if (n(4) < 190) errores.push(`muy pocas provincias (${n(4)})`);
  if (n(6) < 1800) errores.push(`muy pocos distritos (${n(6)})`);
  for (const u of ["150101", "150143", "070101"]) if (!c.some((x) => x.ubigeo === u)) errores.push(`falta ${u}`);
  return errores;
}

async function principal() {
  const args = process.argv.slice(2);
  const seco = args.includes("--dry-run");
  const ruta = args.find((a) => !a.startsWith("--"));
  const texto = ruta ? await readFile(ruta, "utf8") : await (async () => {
    const r = await fetch(FUENTE);
    if (!r.ok) throw new Error(`No se pudo descargar la fuente (${r.status})`);
    return r.text();
  })();

  const { catalogo, omitidas } = construirCatalogo(filasCsv(texto.replace(/^﻿/, "")));
  const errores = validarCatalogo(catalogo);
  if (errores.length) throw new Error(`Catálogo incompleto: ${errores.join("; ")}`);
  const n = (len) => catalogo.filter((x) => x.ubigeo.length === len).length;
  console.log(`Catálogo válido: ${n(2)} departamentos, ${n(4)} provincias, ${n(6)} distritos.`);
  if (omitidas.length) console.log(`Omitidos por no tener código INEI en la fuente: ${omitidas.join(", ")}.`);
  if (seco) return;

  const url = process.env.DATABASE_URL_ADMIN;
  if (!url) throw new Error("Falta DATABASE_URL_ADMIN (usuario con permiso de escritura en ref_ubigeo).");
  const pg = (await import("pg")).default;
  const cliente = new pg.Client({ connectionString: url, ssl: { rejectUnauthorized: false } });
  await cliente.connect();
  try {
    await cliente.query("begin");
    const col = (k) => catalogo.map((x) => x[k]);
    const r = await cliente.query(
      `insert into ref_ubigeo (ubigeo, departamento, provincia, distrito)
       select * from unnest($1::varchar[], $2::text[], $3::text[], $4::text[])
       on conflict (ubigeo) do update set
         departamento = excluded.departamento, provincia = excluded.provincia, distrito = excluded.distrito`,
      [col("ubigeo"), col("departamento"), col("provincia"), col("distrito")]);
    await cliente.query("commit");
    console.log(`ref_ubigeo: ${r.rowCount} filas cargadas.`);
  } catch (e) {
    await cliente.query("rollback").catch(() => {});
    throw e;
  } finally {
    await cliente.end();
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  principal().catch((e) => { console.error(e.message); process.exitCode = 1; });
}
