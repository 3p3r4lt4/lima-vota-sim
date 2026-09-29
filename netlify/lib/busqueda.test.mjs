import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { buscar, respuestaExtractiva, terminos, esPreguntaDeLista } from "./busqueda.mjs";

const planes = JSON.parse(readFileSync(new URL("../../public/data/planes/1501.json", import.meta.url)));
const ids = planes.candidatos.map((c) => c.id);

test("normaliza tildes y plurales", () => {
  assert.deepEqual(terminos("Cámaras de VIGILANCIA"), terminos("camara vigilancia"));
});

test("recupera propuestas de serenazgo", () => {
  const r = buscar(planes, "¿Qué proponen para el serenazgo?", ids);
  assert.ok(r.length >= 3);
  assert.ok(r.every((f) => /seren/i.test(f.texto)));
});

test("balancea: máximo 2 fragmentos por candidatura", () => {
  const r = buscar(planes, "cámaras agua metro teleférico vivienda", ids);
  for (const id of ids) assert.ok(r.filter((f) => f.candidatoId === id).length <= 2);
});

test("solo busca en las candidaturas marcadas", () => {
  const r = buscar(planes, "seguridad cámaras", [ids[0], ids[1]]);
  assert.ok(r.every((f) => [ids[0], ids[1]].includes(f.candidatoId)));
});

test("la respuesta extractiva menciona a todas las candidaturas", () => {
  const frs = buscar(planes, "metro tren transporte", ids);
  const txt = respuestaExtractiva("metro tren transporte", frs, planes.candidatos);
  for (const c of planes.candidatos) assert.ok(txt.includes(c.nombre), c.nombre);
});

test("detecta preguntas sobre quiénes postulan", () => {
  assert.ok(esPreguntaDeLista("¿Lístame los candidatos de La Molina?"));
  assert.ok(esPreguntaDeLista("¿Quiénes postulan?"));
  assert.ok(!esPreguntaDeLista("¿Qué proponen los candidatos sobre el agua?"));
});

test("La Molina: busca en los planes completos y cita la página del PDF", () => {
  const lm = JSON.parse(readFileSync(new URL("../../public/data/planes/150114.json", import.meta.url)));
  const ids = lm.candidatos.map((c) => c.id);
  const r = buscar(lm, "¿Quiénes proponen drones de vigilancia?", ids);
  assert.ok(r.length >= 3);
  assert.ok(r.every((f) => Number.isInteger(f.pagina) && f.pagina >= 1));
  const txt = respuestaExtractiva("drones de vigilancia", r, lm.candidatos);
  assert.match(txt, /\[.+, p\.\d+\]/);
});
