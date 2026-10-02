// Utilidades compartidas por los scripts que cargan secretos en Netlify y en el .env local, sin imprimirlos.
//
// Se usa `netlify api` y no `netlify env:set`: en netlify-cli 27 env:set puede salir con código 0 sin guardar
// nada (p. ej. cuando el plan Free rechaza el scope). Los valores van dentro del JSON de --data, a un proceso
// hijo sin shell (sin expansión de «$»); durante ese segundo son visibles para otros procesos del mismo equipo.
import { spawnSync, execSync } from "node:child_process";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

export const RAIZ = fileURLToPath(new URL("..", import.meta.url));

export function rutaCli() {
  try {
    const prefijo = execSync("npm prefix -g", { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim();
    const ruta = `${prefijo}/node_modules/netlify-cli/bin/run.js`;
    return existsSync(ruta) ? ruta : null;
  } catch {
    return null;
  }
}

// ocultar(): valores que nunca deben aparecer en un mensaje de error
export function crearApi(cli, ocultar = () => []) {
  const limpiar = (s) => ocultar().reduce((t, v) => (v ? t.split(v).join("***") : t), String(s ?? ""))
    .replace(/\x1b\[[0-9;]*m/g, "").trim().split("\n").slice(-2).join(" | ");
  return function api(metodo, datos) {
    const r = spawnSync(process.execPath, [cli, "api", metodo, ...(datos ? ["--data", JSON.stringify(datos)] : [])], {
      cwd: RAIZ, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"], env: { ...process.env, NO_COLOR: "1" },
    });
    let json = null;
    try { json = JSON.parse(r.stdout); } catch { /* sin JSON */ }
    return { ok: r.status === 0, json, error: limpiar(r.stderr || r.error?.message) };
  };
}

// Devuelve { account_id, site_id } del sitio vinculado a esta carpeta
export function comprobarNetlify(api) {
  if (!api("getCurrentUser").ok) throw new Error("Netlify CLI sin sesión. Ejecuta `netlify login` y vuelve a intentarlo.");
  let siteId = null;
  try { siteId = JSON.parse(readFileSync(`${RAIZ}/.netlify/state.json`, "utf8")).siteId; } catch { /* sin vincular */ }
  if (!siteId) throw new Error("Esta carpeta no está vinculada a un sitio. Ejecuta `netlify link` y vuelve a intentarlo.");
  const sitio = api("getSite", { site_id: siteId });
  if (!sitio.ok) throw new Error(`No se pudo leer el sitio vinculado: ${sitio.error}`);
  return { account_id: sitio.json.account_id, site_id: siteId };
}

// Contexto production. Sin scope en las no secretas (el plan Free no permite elegirlo); las secretas no
// admiten post_processing, así que llevan los demás scopes, igual que hace la interfaz de Netlify.
export function publicarEnNetlify(api, base, valores, secretas) {
  for (const [k, v] of Object.entries(valores)) {
    api("deleteEnvVar", { ...base, key: k });  // si no existía, falla y no importa
    const secreta = secretas.includes(k);
    const r = api("createEnvVars", {
      ...base,
      body: [{ key: k, is_secret: secreta, ...(secreta ? { scopes: ["builds", "functions", "runtime"] } : {}), values: [{ context: "production", value: v }] }],
    });
    if (!r.ok) throw new Error(`Netlify rechazó ${k}: ${r.error || "sin detalle"}. Quedó a medias: corrige y vuelve a ejecutar.`);
  }
  // Verificación real: que cada variable exista con valor en production
  const lista = api("getEnvVars", base).json ?? [];
  const faltan = Object.keys(valores).filter((k) => !lista.some((x) => x.key === k && x.values.some((y) => y.context === "production")));
  if (faltan.length) throw new Error(`Netlify no muestra ${faltan.join(", ")} después de guardarlas. Revisa en la interfaz.`);
  for (const k of Object.keys(valores)) console.log(`✓ Netlify (production): ${k}${secretas.includes(k) ? " (secreta)" : ""}`);
}

// ---------- .env local ----------

export function leerEnv() {
  const ruta = `${RAIZ}/.env`;
  const out = {};
  if (!existsSync(ruta)) return out;
  for (const l of readFileSync(ruta, "utf8").split(/\r?\n/)) {
    const m = l.match(/^\s*([A-Z0-9_]+)\s*=(.*)$/);
    if (m) out[m[1]] = m[2].trim().replace(/^'(.*)'$|^"(.*)"$/, "$1$2");
  }
  return out;
}

// Reemplaza TODAS las líneas previas de estas variables (también duplicadas) y agrega un bloque al final.
// comillas: claves que van entre comillas simples (por los «$» del hash scrypt)
export function actualizarEnv(valores, titulo, comillas = []) {
  const ruta = `${RAIZ}/.env`;
  const gitignore = existsSync(`${RAIZ}/.gitignore`) ? readFileSync(`${RAIZ}/.gitignore`, "utf8") : "";
  if (!/^\.env$/m.test(gitignore)) throw new Error(".env no está en .gitignore: no se escribe nada en él.");
  const claves = new Set(Object.keys(valores));
  const previas = existsSync(ruta) ? readFileSync(ruta, "utf8").split(/\r?\n/) : [];
  const resto = previas.filter((l) => !claves.has((l.match(/^\s*([A-Z0-9_]+)\s*=/) ?? [])[1]));
  while (resto.length && resto.at(-1).trim() === "") resto.pop();
  const bloque = Object.entries(valores).map(([k, v]) => (comillas.includes(k) ? `${k}='${v}'` : `${k}=${v}`));
  writeFileSync(ruta, [...resto, "", `# ${titulo} (${new Date().toISOString().slice(0, 10)})`, ...bloque, ""].join("\n"));
}
