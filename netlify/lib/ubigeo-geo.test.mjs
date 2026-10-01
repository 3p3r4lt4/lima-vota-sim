import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolverGeo, DISTRITOS_LIMA, DEPARTAMENTOS, normalizar } from "./ubigeo-geo.mjs";

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

test("normalizar", () => {
  assert.equal(normalizar("  Breña-Rímac "), "brena rimac");
});
