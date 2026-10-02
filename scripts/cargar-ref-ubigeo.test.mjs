import { test } from "node:test";
import assert from "node:assert/strict";
import { filasCsv, titulo, construirCatalogo, validarCatalogo } from "./cargar-ref-ubigeo.mjs";

const CSV = `inei,reniec,departamento,provincia,distrito,capital
150113,140113,LIMA,LIMA,JESUS MARIA,"Jesús María"
150605,140605,LIMA,HUARAL,CHANCAY,"Chancay, ""puerto"""
040101,040101,AREQUIPA,AREQUIPA,AREQUIPA,Arequipa\r
070101,240101,CALLAO,CALLAO,CALLAO,Callao
10101,010101,AMAZONAS,CHACHAPOYAS,CHACHAPOYAS,Chachapoyas
NA,170107,MOQUEGUA,MARISCAL NIETO,SAN ANTONIO,San Antonio
`;

test("CSV con comillas, comas internas y CRLF", () => {
  const f = filasCsv(CSV);
  assert.equal(f.length, 7);
  assert.equal(f[2][5], 'Chancay, "puerto"');
  assert.equal(f[3][5], "Arequipa");
});

test("títulos con partículas en minúscula", () => {
  assert.equal(titulo("SAN JUAN DE LURIGANCHO"), "San Juan de Lurigancho");
  assert.equal(titulo("LA  VICTORIA"), "La Victoria");
  assert.equal(titulo("VILLA EL SALVADOR"), "Villa El Salvador");
});

test("catálogo: niveles derivados, tildes conocidas y ceros a la izquierda", () => {
  const { catalogo: c, omitidas } = construirCatalogo(filasCsv(CSV));
  assert.deepEqual(omitidas, ["San Antonio"]);
  assert.ok(!c.some((x) => x.ubigeo.startsWith("17")));
  const por = new Map(c.map((x) => [x.ubigeo, x]));
  assert.deepEqual(por.get("150113"), { ubigeo: "150113", departamento: "Lima", provincia: "Lima", distrito: "Jesús María" });
  assert.deepEqual(por.get("1506"), { ubigeo: "1506", departamento: "Lima", provincia: "Huaral", distrito: null });
  assert.deepEqual(por.get("04"), { ubigeo: "04", departamento: "Arequipa", provincia: null, distrito: null });
  assert.equal(por.get("010101").provincia, "Chachapoyas");
  assert.equal(por.get("0701").provincia, "Callao");
  assert.deepEqual(c.map((x) => x.ubigeo).slice(0, 3), ["01", "0101", "010101"]);
});

test("catálogo: rechaza ubigeos inválidos o repetidos y valida el tamaño", () => {
  assert.throws(() => construirCatalogo(filasCsv("inei,departamento,provincia,distrito\n15A113,LIMA,LIMA,X")), /inválido/);
  assert.throws(() => construirCatalogo(filasCsv("inei,departamento,provincia,distrito\n150113,LIMA,LIMA,X\n150113,LIMA,LIMA,Y")), /repetido/);
  assert.throws(() => construirCatalogo(filasCsv("ubigeo,departamento\n150113,LIMA")), /columna «inei»/);
  const errores = validarCatalogo(construirCatalogo(filasCsv(CSV)).catalogo);
  assert.ok(errores.some((e) => e.includes("25 departamentos")));
  assert.ok(errores.includes("falta 150101"));
});
