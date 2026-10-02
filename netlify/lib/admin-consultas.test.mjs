import { test } from "node:test";
import assert from "node:assert/strict";
import {
  leerFiltros, construirWhere, celdaCsv, aCsv, hoyLima, fechaHoraLima, estadoSesion, prepararSesion, ACTIVA_SEG,
} from "./admin-consultas.mjs";

const P = (q) => new URLSearchParams(q);

test("filtros por defecto: últimos 7 días de Lima, sin bots", () => {
  assert.equal(hoyLima(new Date("2026-10-02T03:00:00Z")), "2026-10-01");
  assert.deepEqual(leerFiltros(P(""), "2026-10-01"), {
    desde: "2026-09-25", hasta: "2026-10-01", departamento: null, provincia: null, distrito: null,
    ambito: null, dispositivo: null, bots: false, pagina: 1,
  });
});

test("filtros inválidos se ignoran y el rango se acota", () => {
  const f = leerFiltros(P("desde=2026-02-30&hasta=2026-10-01&ambito=15x&dispositivo=nevera&pagina=-3"), "2026-10-01");
  assert.equal(f.desde, "2026-09-25");
  assert.equal(f.ambito, null);
  assert.equal(f.dispositivo, null);
  assert.equal(f.pagina, 1);
  const largo = leerFiltros(P("desde=2025-01-01&hasta=2026-10-01"), "2026-10-01");
  assert.equal(largo.desde, "2026-07-02");
  const invertido = leerFiltros(P("desde=2026-10-01&hasta=2026-09-01"), "2026-10-01");
  assert.deepEqual([invertido.desde, invertido.hasta], ["2026-09-01", "2026-10-01"]);
  assert.equal(leerFiltros(P(`distrito=${"x".repeat(100)}`), "2026-10-01").distrito.length, 60);
});

test("WHERE parametrizado: los valores nunca entran al SQL", () => {
  const f = leerFiltros(P("departamento=Lima'; drop table x;--&provincia=Lima&distrito=Jesús María&ambito=150114&dispositivo=movil&bots=1"), "2026-10-01");
  const w = construirWhere(f);
  assert.ok(!w.sql.includes("drop"));
  assert.ok(!w.sql.includes("Jesús"));
  assert.match(w.sql, /v\.departamento = \$3 and v\.provincia = \$4 and v\.distrito = \$5 and \$6::text = any\(v\.ambitos_visitados\) and v\.dispositivo_tipo = \$7$/);
  assert.deepEqual(w.valores, ["2026-09-25", "2026-10-01", "Lima'; drop table x;--", "Lima", "Jesús María", "150114", "movil"]);
  assert.ok(construirWhere(leerFiltros(P(""), "2026-10-01")).sql.endsWith("not v.es_bot"));
});

test("desconexión y duración: beacon, último latido y sesión en curso", () => {
  const inicio = "2026-10-01T15:00:00Z";
  const ahora = new Date("2026-10-01T16:00:00Z");
  // Con beacon de salida: manda «fin»
  assert.deepEqual(estadoSesion({ inicio, ultima_senal: "2026-10-01T15:04:00Z", fin: "2026-10-01T15:05:30Z" }, ahora),
    { activa: false, con_fin: true, desconexion: new Date("2026-10-01T15:05:30Z"), duracion_seg: 330 });
  // Sin beacon y sin latido hace más de 2 min: cerrada en el último latido
  assert.deepEqual(estadoSesion({ inicio, ultima_senal: "2026-10-01T15:10:00Z", fin: null }, ahora),
    { activa: false, con_fin: false, desconexion: new Date("2026-10-01T15:10:00Z"), duracion_seg: 600 });
  // Latido reciente: en curso, la duración llega hasta el último latido
  const reciente = new Date(ahora.getTime() - (ACTIVA_SEG - 1) * 1000);
  const enCurso = estadoSesion({ inicio, ultima_senal: reciente, fin: null }, ahora);
  assert.equal(enCurso.activa, true);
  assert.equal(enCurso.desconexion, null);
  assert.equal(enCurso.duracion_seg, 3600 - (ACTIVA_SEG - 1));
  // Justo en el límite de 2 min todavía cuenta; un segundo después ya no
  assert.equal(estadoSesion({ inicio, ultima_senal: new Date(ahora - ACTIVA_SEG * 1000), fin: null }, ahora).activa, true);
  assert.equal(estadoSesion({ inicio, ultima_senal: new Date(ahora - ACTIVA_SEG * 1000 - 1000), fin: null }, ahora).activa, false);
  // Sin ningún latido: dura 0 s; relojes cruzados nunca dan negativo
  assert.equal(estadoSesion({ inicio, ultima_senal: null, fin: null }, ahora).duracion_seg, 0);
  assert.equal(estadoSesion({ inicio, ultima_senal: "2026-10-01T14:59:00Z", fin: null }, ahora).duracion_seg, 0);
});

test("prepararSesion: horas en America/Lima", () => {
  assert.equal(fechaHoraLima("2026-10-02T03:30:05Z"), "2026-10-01 22:30:05");
  assert.equal(fechaHoraLima(null), null);
  const f = prepararSesion({ inicio: new Date("2026-10-01T15:00:00Z"), ultima_senal: new Date("2026-10-01T15:02:00Z"), fin: null, so: "Android" },
    new Date("2026-10-01T18:00:00Z"));
  assert.deepEqual(f, { so: "Android", inicio: "2026-10-01 10:00:00", desconexion: "2026-10-01 10:02:00", activa: false, con_fin: false, duracion_seg: 120 });
});

test("CSV: escapado, fórmulas neutralizadas y BOM", () => {
  assert.equal(celdaCsv('a,"b"'), '"a,""b"""');
  assert.equal(celdaCsv("=HYPERLINK(1)"), "'=HYPERLINK(1)");
  assert.equal(celdaCsv(null), "");
  assert.equal(celdaCsv(["150114", "1501"]), "150114 1501");
  const csv = aCsv([{ inicio: "2026-10-01 10:00:00", distrito: "Jesús María", ambitos_visitados: ["1501"], vistas: ["comparar", "fichas"], preguntas_count: 2, es_bot: false }]);
  assert.ok(csv.startsWith("\uFEFFinicio_lima,"));
  assert.ok(csv.includes("Jesús María"));
  assert.ok(csv.includes("comparar fichas,2,"));
  assert.equal(csv.trim().split("\r\n").length, 2);
});
