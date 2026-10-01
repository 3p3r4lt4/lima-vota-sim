#!/usr/bin/env node
// Genera los secretos del panel /admin. No escribe nada en disco: copia la salida a las variables de Netlify
// y cierra la terminal (o limpia el historial de la consola) al terminar.
//   node scripts/admin-setup.mjs
import { randomBytes } from "node:crypto";
import { hashPassword, base32Encode } from "../netlify/lib/auth-admin.mjs";

const EMISOR = "Lima vota informado";
const CUENTA = "admin";

// Lee una línea sin eco cuando hay terminal; si stdin viene de una tubería, la lee tal cual.
function preguntarOculto(texto) {
  return new Promise((resolver, rechazar) => {
    const { stdin, stdout } = process;
    stdout.write(texto);
    if (!stdin.isTTY) {
      let datos = "";
      stdin.setEncoding("utf8");
      const alDato = (c) => {
        datos += c;
        const i = datos.indexOf("\n");
        if (i >= 0) { stdin.off("data", alDato); stdin.pause(); stdout.write("\n"); resolver(datos.slice(0, i).replace(/\r$/, "")); }
      };
      stdin.on("data", alDato);
      stdin.on("end", () => resolver(datos.replace(/\r?\n$/, "")));
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
        if (c === "\u0003") { stdin.setRawMode(false); stdout.write("\n"); return rechazar(new Error("cancelado")); }
        if (c === "\u007f" || c === "\b") { valor = valor.slice(0, -1); continue; }
        if (c >= " ") valor += c;
      }
    };
    stdin.on("data", alTecla);
  });
}

try {
  const password = await preguntarOculto("Contraseña del panel (mín. 12 caracteres): ");
  if (password.length < 12 || password.length > 256) throw new Error("La contraseña debe tener entre 12 y 256 caracteres.");
  if (process.stdin.isTTY && (await preguntarOculto("Repítela: ")) !== password) throw new Error("Las contraseñas no coinciden.");

  const totpSecreto = base32Encode(randomBytes(20));
  const variables = {
    ADMIN_PASSWORD_HASH: await hashPassword(password),
    ADMIN_TOTP_SECRET: totpSecreto,
    ADMIN_SESSION_SECRET: randomBytes(32).toString("base64url"),
    ANALYTICS_SALT: randomBytes(32).toString("base64url"),
  };
  const uri = `otpauth://totp/${encodeURIComponent(`${EMISOR}:${CUENTA}`)}?secret=${totpSecreto}`
    + `&issuer=${encodeURIComponent(EMISOR)}&algorithm=SHA1&digits=6&period=30`;

  console.log("\nVariables para Netlify (Site configuration → Environment variables). Son secretas:");
  console.log("no las pegues en issues, chats ni commits.\n");
  for (const [k, v] of Object.entries(variables)) console.log(`${k}=${v}`);
  console.log("\nSi ANALYTICS_SALT ya existe en Netlify, conserva la actual (cambiarla solo reinicia el conteo de únicos).");
  console.log("En un archivo .env local, pon ADMIN_PASSWORD_HASH entre comillas simples por los signos $.");
  console.log("\nAgrega la cuenta en tu app autenticadora (Google Authenticator, Aegis, 1Password…) con esta URI");
  console.log("o escribiendo a mano el secreto ADMIN_TOTP_SECRET (tipo: basado en tiempo, 6 dígitos, 30 s):\n");
  console.log(uri);
  console.log("\nPara convertir la URI en QR sin enviarla a internet, usa un generador local (p. ej. `qrencode -t ansiutf8 '<URI>'`).");
} catch (e) {
  console.error(`\n${e.message}`);
  process.exitCode = 1;
}
