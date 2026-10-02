import { test } from "node:test";
import assert from "node:assert/strict";
import {
  validarEvento, hashIp, fechaLima, crearLimitador, mismoOrigen, analiticaHabilitada, diasRetencion,
  EVENTOS, TIPO_EVENTO, MAX_BODY,
} from "./visita.mjs";

const S = "3f2b8c1e-9a4d-4c6b-8e2f-1a2b3c4d5e6f";
const ev = (o) => JSON.stringify(o);

test("acepta un inicio completo y normaliza", () => {
  const r = validarEvento(ev({ e: "inicio", s: S.toUpperCase(), a: "150114", p: "390x844", i: "es-PE", r: "WWW.Google.com" }));
  assert.equal(r.ok, true);
  assert.deepEqual(r.evento, {
    tipo: "inicio", sesion_id: S, ambito: "150114", pantalla: "390x844", idioma: "es-PE", referer_host: "www.google.com",
    vista: null, ruta: null, utm_source: null, utm_medium: null, utm_campaign: null,
  });
});

test("inicio con vista, ruta y UTM", () => {
  const r = validarEvento(ev({ e: "inicio", s: S, v: "comparar", t: "/", us: "facebook", um: "social", uc: "erm 2026_lima" }));
  assert.equal(r.ok, true);
  assert.equal(r.evento.vista, "comparar");
  assert.equal(r.evento.ruta, "/");
  assert.deepEqual([r.evento.utm_source, r.evento.utm_medium, r.evento.utm_campaign], ["facebook", "social", "erm 2026_lima"]);
});

test("vista y pregunta: solo el tipo, nunca texto libre", () => {
  assert.equal(validarEvento(ev({ e: "vista", s: S, v: "fichas" })).ok, true);
  assert.equal(validarEvento(ev({ e: "vista", s: S })).motivo, "vista");
  assert.equal(validarEvento(ev({ e: "vista", s: S, v: "mapa" })).motivo, "vista");
  assert.equal(validarEvento(ev({ e: "pregunta", s: S, a: "150114" })).ok, true);
  assert.equal(validarEvento(ev({ e: "pregunta", s: S, q: "¿serenazgo?" })).motivo, "campo");
  for (const [k, v] of [["t", "no-empieza-con-barra"], ["t", "/a?b=1"], ["us", "<script>"], ["uc", "x".repeat(81)], ["um", 5]]) {
    assert.equal(validarEvento(ev({ e: "inicio", s: S, [k]: v })).motivo, "formato", `${k}=${v}`);
  }
});

test("cada evento con fila en analytics_eventos usa un tipo válido de la tabla", () => {
  const TIPOS_TABLA = ["vista", "cambio_ambito", "pregunta", "latido", "salida"];
  for (const e of EVENTOS) {
    if (e === "latido") assert.equal(TIPO_EVENTO[e], undefined);
    else assert.ok(TIPOS_TABLA.includes(TIPO_EVENTO[e]), e);
  }
});

test("interruptor ANALYTICS_ENABLED y días de retención", () => {
  for (const v of [undefined, "", "true", "1", "sí"]) assert.equal(analiticaHabilitada(v), true, String(v));
  for (const v of ["false", "FALSE", "0", "no", " off "]) assert.equal(analiticaHabilitada(v), false, v);
  assert.equal(diasRetencion(undefined), 180);
  assert.equal(diasRetencion("abc"), 180);
  assert.equal(diasRetencion("90"), 90);
  assert.equal(diasRetencion("5"), 30);
  assert.equal(diasRetencion("9999"), 730);
});

test("latido y fin no exigen ámbito", () => {
  assert.equal(validarEvento(ev({ e: "latido", s: S })).ok, true);
  assert.equal(validarEvento(ev({ e: "fin", s: S, a: "1501" })).ok, true);
});

test("rechaza eventos, uuid y ubigeo inválidos", () => {
  assert.equal(validarEvento(ev({ e: "click", s: S })).motivo, "evento");
  assert.equal(validarEvento(ev({ e: "latido", s: "no-es-uuid" })).motivo, "sesion");
  assert.equal(validarEvento(ev({ e: "ambito", s: S })).motivo, "ambito");
  assert.equal(validarEvento(ev({ e: "inicio", s: S })).evento.ambito, null);
  assert.equal(validarEvento(ev({ e: "ambito", s: S, a: "1501" })).ok, true);
  for (const a of ["123", "1501144", "15a114", "150114 ", 150114]) {
    assert.equal(validarEvento(ev({ e: "ambito", s: S, a })).ok, false, String(a));
  }
});

test("rechaza campos extra, formatos raros y cuerpos grandes", () => {
  assert.equal(validarEvento(ev({ e: "latido", s: S, ua: "Mozilla" })).motivo, "campo");
  assert.equal(validarEvento(ev({ e: "latido", s: S, p: "390*844" })).motivo, "formato");
  assert.equal(validarEvento(ev({ e: "latido", s: S, i: "<script>" })).motivo, "formato");
  assert.equal(validarEvento(ev({ e: "latido", s: S, r: "evil.com/path?x=1" })).motivo, "formato");
  assert.equal(validarEvento("x".repeat(MAX_BODY + 1)).motivo, "tamaño");
  assert.equal(validarEvento("").motivo, "tamaño");
  assert.equal(validarEvento("[1,2]").motivo, "json");
  assert.equal(validarEvento("{no json").motivo, "json");
  assert.equal(validarEvento(undefined).motivo, "tamaño");
});

test("hash de IP: HMAC estable en el día, distinto entre días y sin la IP en claro", () => {
  const d1 = new Date("2026-10-01T15:00:00Z"), d1b = new Date("2026-10-02T04:59:59Z"), d2 = new Date("2026-10-02T05:00:00Z");
  assert.equal(fechaLima(d1b), "20261001");
  assert.equal(fechaLima(d2), "20261002");
  const h = hashIp("181.65.1.2", "sal", d1);
  assert.match(h, /^[0-9a-f]{64}$/);
  assert.equal(h, hashIp("181.65.1.2", "sal", d1b));
  assert.notEqual(h, hashIp("181.65.1.2", "sal", d2));
  assert.notEqual(h, hashIp("181.65.1.2", "otra", d1));
  assert.ok(!h.includes("181"));
});

test("limitador: 60 por minuto por clave", () => {
  const permitir = crearLimitador({ max: 60, ventanaMs: 60_000 });
  for (let i = 0; i < 60; i++) assert.equal(permitir("a", 1000), true);
  assert.equal(permitir("a", 1000), false);
  assert.equal(permitir("b", 1000), true);
  assert.equal(permitir("a", 61_000), true);
});

test("mismo origen", () => {
  const req = (h) => new Request("https://lima-vota-informado.netlify.app/api/visita", { method: "POST", headers: h });
  assert.equal(mismoOrigen(req({ origin: "https://lima-vota-informado.netlify.app" })), true);
  assert.equal(mismoOrigen(req({})), true);
  assert.equal(mismoOrigen(req({ origin: "https://evil.example" })), false);
  assert.equal(mismoOrigen(req({ "sec-fetch-site": "cross-site" })), false);
});
