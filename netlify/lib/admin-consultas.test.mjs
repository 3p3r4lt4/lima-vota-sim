import { test } from "node:test";
import assert from "node:assert/strict";
import { leerFiltros, construirWhere, celdaCsv, aCsv, hoyLima } from "./admin-consultas.mjs";

const P = (q) => new URLSearchParams(q);

test("filtros por defecto: últimos 7 días de Lima, sin bots", () => {
  assert.equal(hoyLima(new Date("2026-10-02T03:00:00Z")), "2026-10-01");
  assert.deepEqual(leerFiltros(P(""), "2026-10-01"),
    { desde: "2026-09-25", hasta: "2026-10-01", departamento: null, ambito: null, dispositivo: null, bots: false, pagina: 1 });
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
});

test("WHERE parametrizado: los valores nunca entran al SQL", () => {
  const f = leerFiltros(P("departamento=Lima'; drop table x;--&ambito=150114&dispositivo=movil&bots=1"), "2026-10-01");
  const w = construirWhere(f);
  assert.ok(!w.sql.includes("drop"));
  assert.match(w.sql, /departamento = \$3 and \$4::text = any\(ambitos_visitados\) and dispositivo_tipo = \$5$/);
  assert.deepEqual(w.valores, ["2026-09-25", "2026-10-01", "Lima'; drop table x;--", "150114", "movil"]);
  assert.ok(construirWhere(leerFiltros(P(""), "2026-10-01")).sql.endsWith("not es_bot"));
});

test("CSV: escapado, fórmulas neutralizadas y BOM", () => {
  assert.equal(celdaCsv('a,"b"'), '"a,""b"""');
  assert.equal(celdaCsv("=HYPERLINK(1)"), "'=HYPERLINK(1)");
  assert.equal(celdaCsv(null), "");
  assert.equal(celdaCsv(["150114", "1501"]), "150114 1501");
  const csv = aCsv([{ inicio: "2026-10-01 10:00:00", distrito: "Jesús María", ambitos_visitados: ["1501"], es_bot: false }]);
  assert.ok(csv.startsWith("﻿inicio_lima,"));
  assert.ok(csv.includes("Jesús María"));
  assert.equal(csv.trim().split("\r\n").length, 2);
});
