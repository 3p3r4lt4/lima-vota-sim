export const TEMAS = {
  seguridad: "Seguridad ciudadana",
  transporte: "Tránsito y transporte",
  residuos: "Limpieza y residuos",
  areas_verdes: "Áreas verdes y ambiente",
  desarrollo_urbano: "Desarrollo urbano",
  social: "Programas sociales",
  economia: "Economía local",
  gestion: "Transparencia y gestión",
};
export const nombreTema = (t) => TEMAS[t] ?? t;

// Datos objetivos por candidatura; no son un puntaje ni se usan para ordenar
export function resumenCandidatura(c, temas) {
  const todas = temas.flatMap((t) => c.temas[t]?.propuestas ?? []);
  return {
    total: todas.length,
    conMeta: todas.filter((p) => p.meta).length,
    sinDesarrollar: temas.filter((t) => c.temas[t]?.sin_informacion),
    principales: temas.filter((t) => !c.temas[t]?.sin_informacion)
      .map((t) => ({ tema: t, ...c.temas[t].propuestas[0] })),
  };
}
