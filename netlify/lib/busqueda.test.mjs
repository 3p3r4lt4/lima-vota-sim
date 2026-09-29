import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { buscar, respuestaExtractiva, terminos } from "./busqueda.mjs";

const planes = JSON.parse(readFileSync(new URL("../../public/data/planes/150114.json", import.meta.url)));
const ids = planes.candidatos.map((c) => c.id);

test("normaliza tildes y plurales", () => {
  assert.deepEqual(terminos("Cámaras de VIGILANCIA"), terminos("camara vigilancia"));
});

test("recupera fragmentos del tema consultado", () => {
  const r = buscar(planes, "¿Qué proponen sobre seguridad y serenazgo?", ids);
  assert.ok(r.length > 0);
  assert.ok(r.some((f) => /seguridad|seren/i.test(f.texto)));
});

test("balancea: máximo 2 fragmentos por candidatura", () => {
  const r = buscar(planes, "parques áreas verdes basura reciclaje pistas", ids);
  for (const id of ids) assert.ok(r.filter((f) => f.candidatoId === id).length <= 2);
});

test("solo busca en las candidaturas marcadas", () => {
  const r = buscar(planes, "seguridad", [ids[0]]);
  assert.ok(r.every((f) => f.candidatoId === ids[0]));
});

test("la respuesta extractiva incluye a todos, con cita o aviso", () => {
  const frs = buscar(planes, "seguridad ciudadana", ids);
  const txt = respuestaExtractiva("seguridad ciudadana", frs, planes.candidatos);
  for (const c of planes.candidatos) assert.ok(txt.includes(`**${c.nombre}:**`));
  assert.match(txt, /\[Candidatura \S+, p\.\d+\]|no menciona/);
});
