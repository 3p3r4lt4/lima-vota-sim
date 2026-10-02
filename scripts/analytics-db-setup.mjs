#!/usr/bin/env node
// Prepara (o rota) la base de analítica en un Postgres nuevo o existente, SIN imprimir secretos:
//   1. migraciones db/analytics.sql y db/analytics_eventos.sql (idempotentes; no tocan otras tablas);
//   2. roles analytics_writer y analytics_reader con contraseñas aleatorias nuevas y mínimo privilegio;
//      se revoca a PUBLIC el acceso al esquema public;
//   3. catálogo INEI en ref_ubigeo (scripts/cargar-ref-ubigeo.mjs);
//   4. DATABASE_URL_ANALYTICS y DATABASE_URL_ANALYTICS_READER en el .env local y en Netlify (production, secretas),
//      con el mismo host que DATABASE_URL_ADMIN (usa la URL «pooled» del proveedor) y sslmode=require;
//   5. comprueba con cada rol lo que puede y lo que no puede hacer.
//
//   node scripts/analytics-db-setup.mjs                 (todo)
//   node scripts/analytics-db-setup.mjs --sin-netlify   (sin publicar en Netlify)
//   node scripts/analytics-db-setup.mjs --verificar     (solo el paso 5, con las URLs del .env)
//
// Lee DATABASE_URL_ADMIN (dueño de la base) del .env. Volver a ejecutarlo rota las contraseñas de los dos roles:
// hasta que Netlify tenga las nuevas URLs y se vuelva a desplegar, producción no puede conectarse.
import { randomBytes } from "node:crypto";
import { readFileSync } from "node:fs";
import { RAIZ, leerEnv, actualizarEnv, rutaCli, crearApi, comprobarNetlify, publicarEnNetlify } from "./netlify-env.mjs";
import { FUENTE, filasCsv, construirCatalogo, validarCatalogo } from "./cargar-ref-ubigeo.mjs";

const args = new Set(process.argv.slice(2));
const ROLES = { analytics_writer: "DATABASE_URL_ANALYTICS", analytics_reader: "DATABASE_URL_ANALYTICS_READER" };
const pg = (await import("pg")).default;

const host = (url) => { try { return new URL(url).hostname.replace(/^([^.]{0,6})[^.]*/, "$1****"); } catch { return "?"; } };

async function conectar(url) {
  const c = new pg.Client({ connectionString: url, ssl: { rejectUnauthorized: true }, connectionTimeoutMillis: 15_000 });
  await c.connect();
  return c;
}

// URL de un rol: misma base, host y parámetros que la del dueño, con usuario y contraseña propios
function urlDeRol(urlAdmin, rol, password) {
  const u = new URL(urlAdmin);
  u.username = rol;
  u.password = password;
  u.searchParams.set("sslmode", "require");
  return u.toString();
}

// Las líneas «-- grant/revoke …» del bloque de roles de analytics.sql (allí van comentadas para ejecutarlas a mano)
function grantsDeAnalytics() {
  return readFileSync(`${RAIZ}/db/analytics.sql`, "utf8").split(/\r?\n/)
    .filter((l) => /^-- (revoke|grant) /.test(l)).map((l) => l.slice(3));
}

async function migrarYRoles(admin) {
  const tablas = async () => (await admin.query(
    "select table_name from information_schema.tables where table_schema = 'public' order by 1")).rows.map((r) => r.table_name);
  const antes = await tablas();
  console.log(`Tablas previas en public: ${antes.length ? antes.join(", ") : "ninguna"}`);

  await admin.query(readFileSync(`${RAIZ}/db/analytics.sql`, "utf8"));

  const passwords = {};
  for (const rol of Object.keys(ROLES)) {
    passwords[rol] = randomBytes(24).toString("base64url");
    const existe = (await admin.query("select 1 from pg_roles where rolname = $1", [rol])).rowCount > 0;
    // CREATE/ALTER ROLE no admiten parámetros: format(%L) del propio servidor cita la contraseña
    const { rows } = await admin.query(
      `select format('${existe ? "alter" : "create"} role %I with login password %L', $1::text, $2::text) as q`, [rol, passwords[rol]]);
    await admin.query(rows[0].q);
    console.log(`✓ rol ${rol} ${existe ? "rotado" : "creado"}`);
  }

  // Esquema: nadie más que el dueño y estos dos roles
  await admin.query("revoke all on schema public from public");
  for (const sql of grantsDeAnalytics()) await admin.query(sql);
  // analytics_eventos.sql concede lo suyo cuando los roles ya existen
  await admin.query(readFileSync(`${RAIZ}/db/analytics_eventos.sql`, "utf8"));
  const nuevas = (await tablas()).filter((t) => !antes.includes(t));
  console.log(`✓ migraciones aplicadas${nuevas.length ? ` (tablas nuevas: ${nuevas.join(", ")})` : " (sin tablas nuevas)"}`);
  return passwords;
}

async function cargarCatalogo(admin) {
  const r = await fetch(FUENTE);
  if (!r.ok) throw new Error(`No se pudo descargar el catálogo INEI (${r.status})`);
  const { catalogo } = construirCatalogo(filasCsv((await r.text()).replace(/^﻿/, "")));
  const errores = validarCatalogo(catalogo);
  if (errores.length) throw new Error(`Catálogo incompleto: ${errores.join("; ")}`);
  const col = (k) => catalogo.map((x) => x[k]);
  await admin.query(
    `insert into ref_ubigeo (ubigeo, departamento, provincia, distrito)
     select * from unnest($1::varchar[], $2::text[], $3::text[], $4::text[])
     on conflict (ubigeo) do update set
       departamento = excluded.departamento, provincia = excluded.provincia, distrito = excluded.distrito`,
    [col("ubigeo"), col("departamento"), col("provincia"), col("distrito")]);
  const { rows } = await admin.query(
    "select length(ubigeo) as n, count(*)::int as c from ref_ubigeo group by 1 order by 1");
  console.log(`✓ ref_ubigeo: ${rows.map((x) => `${x.c} de ${x.n} dígitos`).join(", ")}`);
}

// Cada prueba: [rol, descripción, sql, debe funcionar]
const PRUEBAS = [
  ["analytics_writer", "insertar una sesión", "insert into visitas_sesion (sesion_id) values ('00000000-0000-4000-8000-000000000000') on conflict do nothing", true],
  ["analytics_writer", "actualizar su señal", "update visitas_sesion set ultima_senal = now() where sesion_id = '00000000-0000-4000-8000-000000000000'", true],
  ["analytics_writer", "leer ref_ubigeo", "select count(*) from ref_ubigeo", true],
  ["analytics_writer", "leer sesiones completas", "select * from visitas_sesion limit 1", false],
  ["analytics_writer", "leer ip_hash", "select ip_hash from visitas_sesion limit 1", false],
  ["analytics_writer", "borrar sesiones", "delete from visitas_sesion", false],
  ["analytics_writer", "borrar eventos", "delete from analytics_eventos", false],
  ["analytics_writer", "leer accesos al panel", "select * from admin_login_log limit 1", false],
  ["analytics_writer", "crear tablas", "create table lv_prueba_permisos (x int)", false],
  ["analytics_reader", "leer sesiones", "select count(*) from visitas_sesion", true],
  ["analytics_reader", "leer eventos y catálogo", "select (select count(*) from analytics_eventos) + (select count(*) from ref_ubigeo)", true],
  ["analytics_reader", "insertar", "insert into visitas_sesion (sesion_id) values ('00000000-0000-4000-8000-000000000001')", false],
  ["analytics_reader", "actualizar", "update visitas_sesion set so = 'x'", false],
  ["analytics_reader", "borrar", "delete from ref_ubigeo where ubigeo = '99'", false],
  ["analytics_reader", "crear tablas", "create table lv_prueba_permisos (x int)", false],
];

async function verificar(urls, urlAdmin) {
  let fallos = 0;
  for (const [rol, variable] of Object.entries(ROLES)) {
    const c = await conectar(urls[variable]);
    try {
      for (const [r, desc, sql, debe] of PRUEBAS.filter((p) => p[0] === rol)) {
        // Cada prueba en una transacción que se deshace: no deja datos
        await c.query("begin");
        let ok = true;
        try { await c.query(sql); } catch { ok = false; }
        await c.query("rollback");
        const bien = ok === debe;
        if (!bien) fallos++;
        console.log(`${bien ? "✓" : "✗"} ${r}: ${debe ? "puede" : "NO puede"} ${desc}${bien ? "" : ` (resultado inesperado: ${ok ? "pudo" : "no pudo"})`}`);
      }
    } finally {
      await c.end();
    }
  }
  // Tablas ajenas a la analítica: ninguno de los dos roles debe tener privilegios
  const admin = await conectar(urlAdmin);
  try {
    const { rows } = await admin.query(
      `select table_name, grantee from information_schema.role_table_grants
        where grantee in ('analytics_writer','analytics_reader') and table_schema = 'public'
          and table_name not in ('visitas_sesion','analytics_eventos','ref_ubigeo','admin_intentos','admin_login_log')`);
    if (rows.length) { fallos += rows.length; console.log("✗ privilegios en tablas ajenas:", rows.map((r) => `${r.grantee}→${r.table_name}`).join(", ")); }
    else console.log("✓ ningún rol de analítica tiene privilegios en otras tablas");
  } finally {
    await admin.end();
  }
  return fallos;
}

try {
  const env = leerEnv();
  const urlAdmin = env.DATABASE_URL_ADMIN;
  if (!urlAdmin) throw new Error("Falta DATABASE_URL_ADMIN en el .env (cadena del dueño de la base, sin comillas).");
  let parsed;
  try { parsed = new URL(urlAdmin); } catch { throw new Error("DATABASE_URL_ADMIN no es una URL válida."); }
  if (!/^postgres(ql)?:$/.test(parsed.protocol)) throw new Error("DATABASE_URL_ADMIN debe empezar por postgresql://");
  console.log(`Base: host ${host(urlAdmin)} | pooled: ${/-pooler\./.test(parsed.hostname)} | base ${parsed.pathname.slice(1)}`);

  if (args.has("--verificar")) {
    const fallos = await verificar(env, urlAdmin);
    process.exitCode = fallos ? 1 : 0;
  } else {
    let netlify = null, base = null, secretos = [];
    if (!args.has("--sin-netlify")) {
      const cli = rutaCli();
      if (!cli) throw new Error("No encuentro netlify-cli. Instálalo con `npm i -g netlify-cli` o usa --sin-netlify.");
      netlify = crearApi(cli, () => secretos);
      base = comprobarNetlify(netlify);  // antes de tocar la base: si falla, no se rota nada
    }

    const admin = await conectar(urlAdmin);
    let passwords;
    try {
      passwords = await migrarYRoles(admin);
      await cargarCatalogo(admin);
    } finally {
      await admin.end();
    }

    const urls = Object.fromEntries(Object.entries(ROLES).map(([rol, v]) => [v, urlDeRol(urlAdmin, rol, passwords[rol])]));
    secretos = [...Object.values(passwords), ...Object.values(urls), urlAdmin];
    actualizarEnv(urls, "Base de analítica, roles rotados con scripts/analytics-db-setup.mjs");
    console.log(`✓ .env local: ${Object.keys(urls).join(", ")}`);
    if (netlify) publicarEnNetlify(netlify, base, urls, Object.keys(urls));

    const fallos = await verificar(urls, urlAdmin);
    if (fallos) throw new Error(`${fallos} comprobaciones de permisos fallaron. Revisa antes de desplegar.`);
    console.log(`\nListo. ${netlify ? "Vuelve a desplegar en Netlify para que las funciones usen las URLs nuevas." : "Netlify no se tocó (--sin-netlify)."}`);
  }
} catch (e) {
  console.error(`\n${String(e.message ?? e).replace(/postgres(ql)?:\/\/[^\s]+/g, "postgresql://***")}`);
  process.exitCode = 1;
}
