#!/usr/bin/env node
// Genera (o rota) los secretos del panel /admin y los carga directamente, SIN imprimirlos:
//   - en Netlify, con la API vía `netlify api` (contexto production; las secretas, marcadas como secretas);
//   - en el .env local (ignorado por git), reemplazando las líneas anteriores de esas variables.
// En la terminal solo aparece el QR para la app autenticadora.
//
//   node scripts/admin-setup.mjs                 (Netlify + .env)
//   node scripts/admin-setup.mjs --sin-netlify   (solo .env, p. ej. para netlify dev)
//   node scripts/admin-setup.mjs --sin-env       (solo Netlify)
//
// Requisitos para Netlify: `npm i -g netlify-cli`, `netlify login` y `netlify link` en esta carpeta.
// Los valores se pasan al CLI dentro del JSON de --data, a un proceso hijo sin shell (sin expansión de «$»);
// durante ese segundo son visibles para otros procesos del mismo equipo, no fuera de él.
import { randomBytes } from "node:crypto";
import { spawnSync, execSync } from "node:child_process";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { hashPassword, base32Encode } from "../netlify/lib/auth-admin.mjs";

const RAIZ = fileURLToPath(new URL("..", import.meta.url));
const EMISOR = "Lima vota informado";
const SECRETAS = ["ADMIN_PASSWORD_HASH", "ADMIN_TOTP_SECRET", "ADMIN_SESSION_SECRET", "ANALYTICS_SALT"];
const args = new Set(process.argv.slice(2));
const usarNetlify = !args.has("--sin-netlify");
const usarEnv = !args.has("--sin-env");

// Lee una línea; con oculto=true no hay eco. Si stdin viene de una tubería, la lee tal cual.
function preguntar(texto, { oculto = false } = {}) {
  return new Promise((resolver, rechazar) => {
    const { stdin, stdout } = process;
    stdout.write(texto);
    if (!stdin.isTTY || !oculto) {
      let datos = "";
      stdin.setEncoding("utf8");
      const alDato = (c) => {
        datos += c;
        const i = datos.indexOf("\n");
        if (i >= 0) { stdin.off("data", alDato); stdin.pause(); if (oculto) stdout.write("\n"); resolver(datos.slice(0, i).replace(/\r$/, "")); }
      };
      stdin.on("data", alDato);
      stdin.once("end", () => resolver(datos.replace(/\r?\n$/, "")));
      stdin.resume();
      return;
    }
    let valor = "";
    stdin.setRawMode(true);
    stdin.setEncoding("utf8");
    stdin.resume();
    const alTecla = (s) => {
      for (const c of s) {
        if (c === "\r" || c === "\n") {
          stdin.setRawMode(false); stdin.pause(); stdin.off("data", alTecla); stdout.write("\n");
          return resolver(valor);
        }
        if (c === "\u0003") { stdin.setRawMode(false); stdout.write("\n"); return rechazar(new Error("Cancelado.")); }
        if (c === "\u007f" || c === "\b") { valor = valor.slice(0, -1); continue; }
        if (c >= " ") valor += c;
      }
    };
    stdin.on("data", alTecla);
  });
}

// ---------- Netlify CLI (se ejecuta su run.js con este mismo node: sin shell ni .cmd) ----------

function rutaCli() {
  try {
    const prefijo = execSync("npm prefix -g", { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim();
    const ruta = `${prefijo}/node_modules/netlify-cli/bin/run.js`;
    return existsSync(ruta) ? ruta : null;
  } catch {
    return null;
  }
}

// Se usa `netlify api` y no `netlify env:set`: en netlify-cli 27 env:set puede salir con código 0 sin guardar
// nada (p. ej. cuando el plan Free rechaza el scope). La salida del CLI nunca se muestra tal cual.
function crearApi(cli, ocultar) {
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

// Devuelve { account_id, site_id } del sitio vinculado
function comprobarNetlify(api) {
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
function publicarEnNetlify(api, base, valores) {
  for (const [k, v] of Object.entries(valores)) {
    api("deleteEnvVar", { ...base, key: k });  // si no existía, falla y no importa
    const secreta = SECRETAS.includes(k);
    const r = api("createEnvVars", {
      ...base,
      body: [{ key: k, is_secret: secreta, ...(secreta ? { scopes: ["builds", "functions", "runtime"] } : {}), values: [{ context: "production", value: v }] }],
    });
    if (!r.ok) throw new Error(`Netlify rechazó ${k}: ${r.error || "sin detalle"}. La rotación quedó a medias: corrige y vuelve a ejecutar.`);
  }
  // Verificación real: que cada variable exista con valor en production
  const lista = api("getEnvVars", base).json ?? [];
  const faltan = Object.keys(valores).filter((k) => !lista.some((x) => x.key === k && x.values.some((y) => y.context === "production")));
  if (faltan.length) throw new Error(`Netlify no muestra ${faltan.join(", ")} después de guardarlas. Revisa en la interfaz.`);
  for (const k of Object.keys(valores)) console.log(`✓ Netlify (production): ${k}${SECRETAS.includes(k) ? " (secreta)" : ""}`);
}

// ---------- .env local ----------

function actualizarEnv(valores) {
  const ruta = `${RAIZ}/.env`;
  const gitignore = existsSync(`${RAIZ}/.gitignore`) ? readFileSync(`${RAIZ}/.gitignore`, "utf8") : "";
  if (!/^\.env$/m.test(gitignore)) throw new Error(".env no está en .gitignore: no se escribe nada en él.");
  const claves = new Set(Object.keys(valores));
  const previas = existsSync(ruta) ? readFileSync(ruta, "utf8").split(/\r?\n/) : [];
  // Se quitan TODAS las líneas previas de estas variables (también duplicadas)
  const resto = previas.filter((l) => !claves.has((l.match(/^\s*([A-Z0-9_]+)\s*=/) ?? [])[1]));
  while (resto.length && resto.at(-1).trim() === "") resto.pop();
  const bloque = Object.entries(valores).map(([k, v]) => (k === "ADMIN_PASSWORD_HASH" ? `${k}='${v}'` : `${k}=${v}`));
  writeFileSync(ruta, [...resto, "", `# Panel /admin (rotado el ${new Date().toISOString().slice(0, 10)} con scripts/admin-setup.mjs)`, ...bloque, ""].join("\n"));
}

// ---------- Principal ----------

try {
  if (!usarNetlify && !usarEnv) throw new Error("Con --sin-netlify y --sin-env no habría dónde guardar los secretos.");
  if (!process.stdin.isTTY) {
    throw new Error("Hace falta una terminal interactiva para escribir la contraseña. Ejecútalo directamente en PowerShell o Git Bash.");
  }

  let secretos = [];
  let netlify = null;
  let base = null;
  if (usarNetlify) {
    const cli = rutaCli();
    if (!cli) throw new Error("No encuentro netlify-cli. Instálalo con `npm i -g netlify-cli` o usa --sin-netlify.");
    netlify = crearApi(cli, () => secretos);
    base = comprobarNetlify(netlify);
  }

  const usuario = ((await preguntar("Usuario del panel [admin]: ")).trim() || "admin");
  if (!/^[\w.@-]{1,64}$/.test(usuario)) throw new Error("Usuario inválido: hasta 64 letras, números o . _ @ -");
  const password = await preguntar("Contraseña nueva (mín. 12 caracteres): ", { oculto: true });
  if (password.length < 12 || password.length > 256) throw new Error("La contraseña debe tener entre 12 y 256 caracteres.");
  if ((await preguntar("Repítela: ", { oculto: true })) !== password) throw new Error("Las contraseñas no coinciden.");

  const totpSecreto = base32Encode(randomBytes(20));
  const valores = {
    ADMIN_USER: usuario,
    ADMIN_PASSWORD_HASH: await hashPassword(password),
    ADMIN_TOTP_SECRET: totpSecreto,
    ADMIN_SESSION_SECRET: randomBytes(32).toString("base64url"),
    ANALYTICS_SALT: randomBytes(32).toString("base64url"),
  };
  secretos = [password, ...SECRETAS.map((k) => valores[k])];

  if (netlify) publicarEnNetlify(netlify, base, valores);
  if (usarEnv) {
    actualizarEnv(valores);
    console.log(`✓ .env local: ${Object.keys(valores).join(", ")}`);
  }

  const uri = `otpauth://totp/${encodeURIComponent(`${EMISOR}:${usuario}`)}?secret=${totpSecreto}`
    + `&issuer=${encodeURIComponent(EMISOR)}&algorithm=SHA1&digits=6&period=30`;
  const QRCode = (await import("qrcode")).default;
  console.log("\nEscanea este código con tu app autenticadora (Google Authenticator, Aegis, 1Password…):\n");
  console.log(await QRCode.toString(uri, { type: "terminal", small: true }));

  const pasos = [
    "Borra de la app autenticadora la cuenta ANTERIOR de «Lima vota informado».",
    netlify && "Vuelve a desplegar: Netlify → Deploys → Trigger deploy → Deploy project (sin redeploy no aplican).",
    "Revoca la ANTHROPIC_API_KEY expuesta en console.anthropic.com → API keys, crea una nueva y cárgala en\n"
      + "     Netlify como secreta (Site configuration → Environment variables). Luego vuelve a desplegar.",
    "Entra a /admin con el usuario, la contraseña y el código de la app. Si falla, mira el motivo en\n"
      + "     Netlify → Logs → Functions → admin-login (líneas «admin-login: rechazo motivo=…»).",
  ].filter(Boolean);
  console.log("Pendiente, en este orden:");
  pasos.forEach((p, i) => console.log(`  ${i + 1}. ${p}`));
  console.log("\nCierra esta terminal o limpia la pantalla: el QR contiene el secreto del segundo factor.");
} catch (e) {
  console.error(`\n${e.message}`);
  process.exitCode = 1;
}
