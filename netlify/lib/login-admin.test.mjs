import { test } from "node:test";
import assert from "node:assert/strict";
import { randomBytes } from "node:crypto";
import { crearManejadorLogin, diagnosticarConfig } from "./login-admin.mjs";
import {
  hashPassword, base32Encode, base32Decode, totp, crearBloqueoMemoria, esAdmin, verificarSesion, leerCookie, COOKIE,
} from "./auth-admin.mjs";

// Secretos de prueba generados aquí; nada sale del test
const PASSWORD = `prueba-${randomBytes(9).toString("base64url")}`;
const TOTP = base32Encode(randomBytes(20));
const ENV = {
  ADMIN_USER: "admin",
  ADMIN_PASSWORD_HASH: await hashPassword(PASSWORD),  // parámetros de producción (N = 2^15)
  ADMIN_TOTP_SECRET: TOTP,
  ADMIN_SESSION_SECRET: randomBytes(32).toString("base64url"),
  ANALYTICS_SALT: randomBytes(32).toString("base64url"),
};
const SITIO = "https://lima-vota-informado.netlify.app";
const codigo = (ms = Date.now()) => totp(base32Decode(TOTP), ms);

function preparar() {
  const logs = [], intentos = [];
  const manejar = crearManejadorLogin({
    bloqueo: crearBloqueoMemoria(), registrarIntento: async (h, r) => { intentos.push(r); }, log: (m) => logs.push(m),
  });
  const login = (cuerpo, { env = ENV, ip = "200.1.2.3", headers = {} } = {}) => manejar(
    new Request(`${SITIO}/api/admin/login`, {
      method: "POST", body: typeof cuerpo === "string" ? cuerpo : JSON.stringify(cuerpo),
      headers: { origin: SITIO, "sec-fetch-site": "same-origin", "content-type": "application/json", ...headers },
    }), { ip }, env);
  return { login, logs, intentos };
}

const ultimoMotivo = (logs) => logs.at(-1).replace("admin-login: rechazo motivo=", "");

test("flujo completo: login correcto → cookie válida → la API admin la acepta", async () => {
  const { login, logs, intentos } = preparar();
  const r = await login({ usuario: "Admin", password: PASSWORD, codigo: codigo() });
  assert.equal(r.status, 204);
  const setCookie = r.headers.get("set-cookie");
  for (const a of ["HttpOnly", "Secure", "SameSite=Strict", "Path=/", "Max-Age=28800"]) assert.ok(setCookie.includes(a), a);
  assert.ok(!/Domain=/i.test(setCookie));
  assert.equal(r.headers.get("cache-control"), "no-store");

  const cookie = setCookie.split(";")[0];
  const pedido = new Request(`${SITIO}/api/admin/visitas`, { headers: { cookie } });
  assert.equal(verificarSesion(leerCookie(pedido), ENV.ADMIN_SESSION_SECRET).sub, "admin");
  const antes = process.env.ADMIN_SESSION_SECRET;
  process.env.ADMIN_SESSION_SECRET = ENV.ADMIN_SESSION_SECRET;
  try { assert.equal(esAdmin(pedido), true); } finally {
    if (antes === undefined) delete process.env.ADMIN_SESSION_SECRET; else process.env.ADMIN_SESSION_SECRET = antes;
  }
  assert.deepEqual(intentos, ["ok"]);
  assert.deepEqual(logs, ["admin-login: acceso concedido"]);
  assert.ok(cookie.startsWith(`${COOKIE}=`));
});

test("motivos codificados en el log, mismo mensaje al cliente", async () => {
  const { login, logs } = preparar();
  const casos = [
    [{ usuario: "root", password: PASSWORD, codigo: codigo() }, "bad_user"],
    [{ usuario: "admin", password: "mala", codigo: codigo() }, "bad_password"],
    [{ usuario: "admin", password: PASSWORD, codigo: "000000" === codigo() ? "111111" : "000000" }, "bad_totp"],
    [{ usuario: "admin", password: PASSWORD, codigo: codigo(Date.now() - 5 * 30_000) }, "bad_totp:clock_skew"],
  ];
  for (const [i, [cuerpo, motivo]] of casos.entries()) {
    const r = await login(cuerpo, { ip: `10.0.0.${i}` });
    assert.equal(r.status, 401, motivo);
    assert.equal((await r.json()).error, "No se pudo iniciar sesión. Revisa los datos o intenta más tarde.");
    assert.equal(ultimoMotivo(logs), motivo);
  }
  // Código ya usado en esta instancia
  const c = codigo();
  assert.equal((await login({ usuario: "admin", password: PASSWORD, codigo: c }, { ip: "10.1.1.1" })).status, 204);
  assert.equal((await login({ usuario: "admin", password: PASSWORD, codigo: c }, { ip: "10.1.1.1" })).status, 401);
  assert.equal(ultimoMotivo(logs), "bad_totp:reused");
  // Origen ajeno y cuerpo inválido
  assert.equal((await login({}, { headers: { origin: "https://evil.example", "sec-fetch-site": "cross-site" } })).status, 403);
  assert.equal(ultimoMotivo(logs), "bad_origin");
  await login("{no json");
  assert.equal(ultimoMotivo(logs), "bad_body");
  // Los logs nunca contienen lo que se escribió ni secretos
  const todo = logs.join("\n");
  for (const secreto of [PASSWORD, "mala", "root", TOTP, ENV.ADMIN_PASSWORD_HASH, ENV.ADMIN_SESSION_SECRET]) {
    assert.ok(!todo.includes(secreto));
  }
});

test("5 fallos → rate_limited aunque luego las credenciales sean correctas", async () => {
  const { login, logs, intentos } = preparar();
  for (let i = 0; i < 5; i++) await login({ usuario: "admin", password: "mala", codigo: codigo() });
  const r = await login({ usuario: "admin", password: PASSWORD, codigo: codigo() });
  assert.equal(r.status, 401);
  assert.equal(ultimoMotivo(logs), "rate_limited");
  assert.deepEqual(intentos, ["fallo", "fallo", "fallo", "fallo", "fallo", "bloqueado"]);
  // Otra IP no está bloqueada
  assert.equal((await login({ usuario: "admin", password: PASSWORD, codigo: codigo() }, { ip: "200.9.9.9" })).status, 204);
});

test("configuración mal cargada: se detecta sin revelar valores", async () => {
  const { login, logs } = preparar();
  const bien = { usuario: "admin", password: PASSWORD, codigo: codigo() };
  const casos = [
    [{ ADMIN_PASSWORD_HASH: `'${ENV.ADMIN_PASSWORD_HASH}'` }, "bad_config:ADMIN_PASSWORD_HASH_quoted"],
    [{ ADMIN_PASSWORD_HASH: `ADMIN_PASSWORD_HASH=${ENV.ADMIN_PASSWORD_HASH}` }, "bad_config:ADMIN_PASSWORD_HASH_includes_name"],
    // Lo que deja un shell que expandió $32768, $8, $1…: el hash queda truncado
    [{ ADMIN_PASSWORD_HASH: "scrypt" + ENV.ADMIN_PASSWORD_HASH.split("$").slice(4).join("") }, "bad_config:ADMIN_PASSWORD_HASH_format"],
    [{ ADMIN_TOTP_SECRET: `"${TOTP}"` }, "bad_config:ADMIN_TOTP_SECRET_quoted"],
    [{ ADMIN_TOTP_SECRET: "no-es-base32!" }, "bad_config:ADMIN_TOTP_SECRET_format"],
    [{ ADMIN_SESSION_SECRET: "corto" }, "bad_config:ADMIN_SESSION_SECRET_short"],
    [{ ADMIN_USER: "'admin'" }, "bad_config:ADMIN_USER_quoted"],
    [{ ADMIN_PASSWORD_HASH: "", ADMIN_TOTP_SECRET: undefined }, "missing_env:ADMIN_PASSWORD_HASH,missing_env:ADMIN_TOTP_SECRET"],
  ];
  for (const [cambio, motivo] of casos) {
    const r = await login(bien, { env: { ...ENV, ...cambio } });
    assert.equal(r.status, 401, motivo);
    assert.equal(ultimoMotivo(logs), motivo);
    for (const v of Object.values(cambio)) if (v) assert.ok(!logs.at(-1).includes(v));
  }
  assert.deepEqual(diagnosticarConfig(ENV), []);
  // El TOTP con espacios o en minúsculas (como lo muestran algunas apps) es válido
  assert.deepEqual(diagnosticarConfig({ ...ENV, ADMIN_TOTP_SECRET: TOTP.toLowerCase().replace(/(.{4})/g, "$1 ") }), []);
});

test("una excepción interna se registra por tipo y responde el mensaje genérico", async () => {
  const logs = [];
  const manejar = crearManejadorLogin({
    bloqueo: { bloqueado: async () => { throw new TypeError("base caída"); } }, log: (m) => logs.push(m),
  });
  const r = await manejar(new Request(`${SITIO}/api/admin/login`, {
    method: "POST", body: JSON.stringify({ password: PASSWORD, codigo: codigo() }),
    headers: { origin: SITIO, "sec-fetch-site": "same-origin" },
  }), { ip: "1.1.1.1" }, ENV);
  assert.equal(r.status, 401);
  assert.deepEqual(logs, ["admin-login: rechazo motivo=exception:TypeError"]);
});
