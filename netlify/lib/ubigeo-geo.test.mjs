import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolverGeo, crearIndiceRef, DISTRITOS_LIMA, DEPARTAMENTOS, normalizar } from "./ubigeo-geo.mjs";

const pe = (subdivision, city) => ({ country: { code: "PE", name: "Peru" }, subdivision, city });
const LMA = { code: "LMA", name: "Lima Province" };

test("la tabla de distritos cubre public/data/ambitos.json con los mismos nombres", () => {
  const ambitos = JSON.parse(readFileSync(new URL("../../public/data/ambitos.json", import.meta.url), "utf8"));
  const porUbigeo = new Map(DISTRITOS_LIMA.map((d) => [d.ubigeo, d.nombre]));
  for (const a of ambitos.filter((x) => x.nivel === "distrital")) {
    assert.equal(porUbigeo.get(a.ubigeo), a.ambito, a.ubigeo);
  }
  assert.equal(DEPARTAMENTOS.length, 25);
});

test("distrito exacto con tildes y mayúsculas normalizadas", () => {
  assert.deepEqual(resolverGeo(pe(LMA, "JESUS MARIA")), {
    pais: "PE", departamento: "Lima", provincia: "Lima", distrito: "Jesús María", ubigeo_geo: "150113", precision_geo: "distrito",
  });
  assert.equal(resolverGeo(pe(LMA, "San Martin de Porres")).ubigeo_geo, "150135");
  assert.equal(resolverGeo(pe({ code: "LIM", name: "Lima" }, "Santiago De Surco")).ubigeo_geo, "150140");
  assert.equal(resolverGeo(pe(LMA, "Surco")).ubigeo_geo, "150140");
  assert.equal(resolverGeo(pe(LMA, "Lurigancho-Chosica")).ubigeo_geo, "150118");
});

test("«Lima» a secas queda en provincia, nunca en el Cercado", () => {
  const r = resolverGeo(pe(LMA, "Lima"));
  assert.equal(r.precision_geo, "provincia");
  assert.equal(r.ubigeo_geo, "1501");
  assert.equal(r.distrito, null);
  assert.equal(resolverGeo(pe(LMA, "Cercado de Lima")).ubigeo_geo, "150101");
});

test("ciudad desconocida baja la precisión", () => {
  assert.equal(resolverGeo(pe(LMA, "Distrito Inventado")).precision_geo, "provincia");
  const ar = resolverGeo(pe({ code: "ARE", name: "Arequipa" }, "Miraflores"));
  assert.deepEqual(ar, { pais: "PE", departamento: "Arequipa", provincia: null, distrito: null, ubigeo_geo: "04", precision_geo: "departamento" });
  // Región Lima (no metropolitana): Miraflores también existe en Yauyos
  assert.equal(resolverGeo(pe({ code: "LIM", name: "Lima" }, "Miraflores")).precision_geo, "departamento");
  assert.equal(resolverGeo(pe({ code: "LIM", name: "Lima" }, "Huaral")).ubigeo_geo, "1506");
});

test("Callao, subdivisión por nombre y otros países", () => {
  assert.equal(resolverGeo(pe({ code: "CAL", name: "Callao" }, "Ventanilla")).ubigeo_geo, "0701");
  assert.equal(resolverGeo(pe({ name: "Cusco Region" }, "Cusco")).ubigeo_geo, "08");
  assert.equal(resolverGeo(pe({ name: "Región Áncash" })).departamento, "Áncash");
  assert.equal(resolverGeo(pe({}, "Lima")).precision_geo, "pais");
  assert.deepEqual(resolverGeo({ country: { code: "US" }, city: "Miami" }),
    { pais: "US", departamento: null, provincia: null, distrito: null, ubigeo_geo: null, precision_geo: "pais" });
  assert.equal(resolverGeo(undefined).precision_geo, null);
});

// Extracto del catálogo INEI con los casos que importan (nombres como vienen de la fuente)
const REF = crearIndiceRef([
  { ubigeo: "04", departamento: "Arequipa", provincia: null, distrito: null },
  { ubigeo: "0401", departamento: "Arequipa", provincia: "Arequipa", distrito: null },
  { ubigeo: "040101", departamento: "Arequipa", provincia: "Arequipa", distrito: "Arequipa" },
  { ubigeo: "040103", departamento: "Arequipa", provincia: "Arequipa", distrito: "Cayma" },
  { ubigeo: "040110", departamento: "Arequipa", provincia: "Arequipa", distrito: "Miraflores" },
  { ubigeo: "0402", departamento: "Arequipa", provincia: "Camaná", distrito: null },
  { ubigeo: "040201", departamento: "Arequipa", provincia: "Camaná", distrito: "Camaná" },
  { ubigeo: "040202", departamento: "Arequipa", provincia: "Camaná", distrito: "José María Quimper" },
  { ubigeo: "040308", departamento: "Arequipa", provincia: "Caravelí", distrito: "José María Quimper" },
  { ubigeo: "1506", departamento: "Lima", provincia: "Huaral", distrito: null },
  { ubigeo: "150605", departamento: "Lima", provincia: "Huaral", distrito: "Chancay" },
  { ubigeo: "151017", departamento: "Lima", provincia: "Yauyos", distrito: "Miraflores" },
  { ubigeo: "", departamento: "x", provincia: "y" }, null,
]);
const AQP = { code: "ARE", name: "Arequipa" };

test("ref_ubigeo: distrito único en el departamento", () => {
  assert.deepEqual(resolverGeo(pe(AQP, "Cayma"), REF), {
    pais: "PE", departamento: "Arequipa", provincia: "Arequipa", distrito: "Cayma", ubigeo_geo: "040103", precision_geo: "distrito",
  });
  assert.equal(resolverGeo(pe(AQP, "MIRAFLORES"), REF).ubigeo_geo, "040110");
  assert.equal(resolverGeo(pe({ code: "LIM", name: "Lima" }, "Chancay"), REF).ubigeo_geo, "150605");
});

test("ref_ubigeo: nombre de provincia o repetido no baja a distrito", () => {
  const capital = resolverGeo(pe(AQP, "Arequipa"), REF);
  assert.equal(capital.precision_geo, "provincia");
  assert.equal(capital.ubigeo_geo, "0401");
  assert.equal(resolverGeo(pe(AQP, "Camana"), REF).ubigeo_geo, "0402");
  assert.equal(resolverGeo(pe(AQP, "José María Quimper"), REF).precision_geo, "departamento");
  assert.equal(resolverGeo(pe(AQP, "Inventado"), REF).precision_geo, "departamento");
  assert.equal(resolverGeo(pe({ code: "CUS", name: "Cusco" }, "Cusco"), REF).precision_geo, "departamento");
  // Región Lima: Miraflores sigue siendo ambiguo aunque el catálogo tenga una sola fila
  assert.equal(resolverGeo(pe({ code: "LIM", name: "Lima" }, "Miraflores"), REF).precision_geo, "departamento");
  // Lima Metropolitana no usa el catálogo: manda la tabla fija
  assert.equal(resolverGeo(pe(LMA, "Chancay"), REF).precision_geo, "provincia");
  assert.equal(resolverGeo(pe(LMA, "Jesús María"), REF).ubigeo_geo, "150113");
});

test("normalizar", () => {
  assert.equal(normalizar("  Breña-Rímac "), "brena rimac");
});
