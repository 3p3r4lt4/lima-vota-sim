// Datos objetivos por candidatura; no son un puntaje ni se usan para ordenar
export function resumenCandidatura(c, temas) {
  const todas = temas.flatMap((t) => c.temas[t]?.propuestas ?? []);
  return {
    total: todas.length,
    conMeta: todas.filter((p) => p.meta).length,
    sinTema: temas.filter((t) => c.temas[t]?.sin_informacion),
    principales: temas.filter((t) => !c.temas[t]?.sin_informacion).map((t) => ({ tema: t, ...c.temas[t].propuestas[0] })),
  };
}
