import { test } from "node:test";
import assert from "node:assert/strict";
import {
  hashPassword, verificarPassword, hotp, totp, verificarTotp, base32Encode, base32Decode,
  firmarSesion, verificarSesion, cookieSesion, leerCookie, origenValido, crearBloqueoMemoria, COOKIE,
  usuarioValido, esAdmin, noAutorizado, evaluarLogin,
} from "./auth-admin.mjs";

const CLAVE_SHA1 = Buffer.from("12345678901234567890");

test("HOTP: vectores del RFC 4226", () => {
  const esperados = ["755224", "287082", "359152", "969429", "338314", "254676", "287922", "162583", "399871", "520489"];
  esperados.forEach((c, i) => assert.equal(hotp(CLAVE_SHA1, i), c));
});

test("TOTP: vectores del RFC 6238 (8 dígitos, SHA-1 y SHA-256)", () => {
  const sha256 = Buffer.from("12345678901234567890123456789012");
  const casos = [
    [59, "94287082", "46119246"], [1111111109, "07081804", "68084774"], [1111111111, "14050471", "67062674"],
    [1234567890, "89005924", "91819424"], [2000000000, "69279037", "90698825"], [20000000000, "65353130", "77737706"],
  ];
  for (const [t, s1, s256] of casos) {
    assert.equal(totp(CLAVE_SHA1, t * 1000, { digitos: 8 }), s1, `sha1 t=${t}`);
    assert.equal(totp(sha256, t * 1000, { digitos: 8, algoritmo: "sha256" }), s256, `sha256 t=${t}`);
  }
});

test("TOTP: ventana de ±1 paso y formato", () => {
  const secreto = base32Encode(CLAVE_SHA1);
  assert.equal(secreto, "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ");
  assert.deepEqual(base32Decode(secreto.toLowerCase()), CLAVE_SHA1);
  const t = 59_000;  // contador 1
  assert.equal(verificarTotp("287082", secreto, t), 1);
  assert.equal(verificarTotp("755224", secreto, t), 0);   // paso anterior
  assert.equal(verificarTotp("359152", secreto, t), 2);   // paso siguiente
  assert.equal(verificarTotp("969429", secreto, t), -1);  // fuera de la ventana
  for (const malo of ["28708", "2870821", "abcdef", 287082, null]) assert.equal(verificarTotp(malo, secreto, t), -1);
  assert.equal(verificarTotp("287082", "no es base32!", t), -1);
});

test("scrypt: formato, verificación y hashes manipulados", async () => {
  const h = await hashPassword("una contraseña larga y rara", { N: 2 ** 14 });
  assert.match(h, /^scrypt\$16384\$8\$1\$[A-Za-z0-9+/=]+\$[A-Za-z0-9+/=]+$/);
  assert.equal(await verificarPassword("una contraseña larga y rara", h), true);
  assert.equal(await verificarPassword("una contraseña larga y raro", h), false);
  assert.equal(await verificarPassword("", h), false);
  assert.equal(await verificarPassword("x", "texto-cualquiera"), false);
  assert.equal(await verificarPassword("una contraseña larga y rara", h.replace("$16384$", "$1073741824$")), false);
  assert.notEqual(await hashPassword("misma", { N: 2 ** 14 }), await hashPassword("misma", { N: 2 ** 14 }));
});

test("cookie: firma, manipulación y expiración a las 8 h", () => {
  const secreto = "s".repeat(43), t0 = Date.UTC(2026, 9, 1, 12);
  const token = firmarSesion(secreto, t0);
  assert.equal(verificarSesion(token, secreto, t0 + 1000).sub, "admin");
  assert.ok(verificarSesion(token, secreto, t0 + 8 * 3600_000 - 1000));
  assert.equal(verificarSesion(token, secreto, t0 + 8 * 3600_000), null);
  assert.equal(verificarSesion(token, "otro".repeat(11), t0), null);
  const [datos, firma] = token.split(".");
  const falso = Buffer.from(JSON.stringify({ sub: "admin", iat: 0, exp: 9e9 })).toString("base64url");
  assert.equal(verificarSesion(`${falso}.${firma}`, secreto, t0), null);
  assert.equal(verificarSesion(`${datos}.${firma}x`, secreto, t0), null);
  assert.equal(verificarSesion(`${datos}`, secreto, t0), null);
  assert.equal(verificarSesion(token, "", t0), null);

  const c = cookieSesion(token);
  for (const atributo of ["HttpOnly", "Secure", "SameSite=Strict", "Path=/", "Max-Age=28800"]) assert.ok(c.includes(atributo), atributo);
  const req = new Request("https://x.test/api/admin/visitas", { headers: { cookie: `otra=1; ${COOKIE}=${token}` } });
  assert.equal(leerCookie(req), token);
});

test("CSRF: Origin obligatorio y del mismo sitio", () => {
  const req = (h) => new Request("https://lima-vota-informado.netlify.app/api/admin/login", { method: "POST", headers: h });
  assert.equal(origenValido(req({ origin: "https://lima-vota-informado.netlify.app", "sec-fetch-site": "same-origin" })), true);
  assert.equal(origenValido(req({})), false);
  assert.equal(origenValido(req({ origin: "https://evil.example" })), false);
  assert.equal(origenValido(req({ origin: "http://lima-vota-informado.netlify.app" })), false);
  assert.equal(origenValido(req({ origin: "https://lima-vota-informado.netlify.app", "sec-fetch-site": "same-site" })), false);
});

test("bloqueo: 5 fallos → 15 min", async () => {
  const b = crearBloqueoMemoria();
  for (let i = 0; i < 4; i++) await b.fallo("ip", 1000);
  assert.equal(await b.bloqueado("ip", 1000), false);
  await b.fallo("ip", 1000);
  assert.equal(await b.bloqueado("ip", 1000 + 14 * 60_000), true);
  assert.equal(await b.bloqueado("otra", 1000), false);
  assert.equal(await b.bloqueado("ip", 1000 + 15 * 60_000), false);
  await b.fallo("ip", 1000 + 16 * 60_000);
  assert.equal(await b.bloqueado("ip", 1000 + 16 * 60_000), false);  // contador reiniciado
});

test("usuario: opcional, sin distinguir mayúsculas y con largo acotado", () => {
  assert.equal(usuarioValido("cualquiera", undefined), true);
  assert.equal(usuarioValido("", ""), true);
  assert.equal(usuarioValido("Admin ", "admin"), true);
  assert.equal(usuarioValido("otro", "admin"), false);
  assert.equal(usuarioValido(undefined, "admin"), false);
  assert.equal(usuarioValido("a".repeat(65), "a".repeat(65)), false);
});

test("API admin: sin cookie o con cookie inválida → 401", () => {
  const secreto = "k".repeat(40);
  const antes = process.env.ADMIN_SESSION_SECRET;
  process.env.ADMIN_SESSION_SECRET = secreto;
  try {
    const req = (cookie) => new Request("https://x.test/api/admin/visitas", { headers: cookie ? { cookie } : {} });
    const valida = firmarSesion(secreto);
    assert.equal(esAdmin(req(null)), false);
    assert.equal(esAdmin(req(`${COOKIE}=basura`)), false);
    assert.equal(esAdmin(req(`${COOKIE}=${firmarSesion("otro-secreto".repeat(4))}`)), false);
    assert.equal(esAdmin(req(`${COOKIE}=${firmarSesion(secreto, Date.now() - 9 * 3600_000)}`)), false);  // vencida
    assert.equal(esAdmin(req(`lv_admin=${valida}`)), false);  // otro nombre de cookie
    assert.equal(esAdmin(req(`${COOKIE}=${valida}`)), true);
    process.env.ADMIN_SESSION_SECRET = "corto";
    assert.equal(esAdmin(req(`${COOKIE}=${firmarSesion("corto")}`)), false);  // secreto débil: nadie entra
    const r = noAutorizado();
    assert.equal(r.status, 401);
    assert.equal(r.headers.get("cache-control"), "no-store");
  } finally {
    if (antes === undefined) delete process.env.ADMIN_SESSION_SECRET; else process.env.ADMIN_SESSION_SECRET = antes;
  }
});

test("login: fallos → bloqueo aunque después las credenciales sean correctas", async () => {
  const secretoTotp = base32Encode(Buffer.from("12345678901234567890"));
  const cfg = { usuario: "admin", passwordHash: await hashPassword("contraseña-larga-de-prueba", { N: 2 ** 14 }), totpSecreto: secretoTotp };
  const ahora = Date.UTC(2026, 9, 1, 12);
  const codigo = totp(base32Decode(secretoTotp), ahora);
  const bien = { usuario: "admin", password: "contraseña-larga-de-prueba", codigo };
  const b = crearBloqueoMemoria();

  const ok = await evaluarLogin(bien, cfg, b, "ip-a", -1, ahora);
  assert.equal(ok.resultado, "ok");
  // El mismo código no sirve dos veces
  assert.equal((await evaluarLogin(bien, cfg, b, "ip-a", ok.contador, ahora)).resultado, "fallo");
  assert.equal((await evaluarLogin({ ...bien, usuario: "root" }, cfg, b, "ip-b", -1, ahora)).resultado, "fallo");

  for (let i = 0; i < 5; i++) {
    assert.equal((await evaluarLogin({ ...bien, password: "mala" }, cfg, b, "ip-c", -1, ahora)).resultado, "fallo");
  }
  assert.equal((await evaluarLogin(bien, cfg, b, "ip-c", -1, ahora)).resultado, "bloqueado");
  assert.equal((await evaluarLogin(bien, cfg, b, "ip-d", -1, ahora)).resultado, "ok");
});
