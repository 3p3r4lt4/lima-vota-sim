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

// Nombres cortos para chips y etiquetas; el nombre completo sigue en nombres_temas
const CORTOS = {
  seguridad: "Seguridad", transporte: "Transporte", agua_riesgos: "Agua y riesgos", urbano: "Vivienda y obras",
  social: "Salud y educación", economia: "Empleo y comercio", ambiente: "Limpieza y ambiente", gestion: "Gestión",
};
export const nombreCorto = (datos, t) => CORTOS[t] ?? datos.nombres_temas?.[t] ?? t;
export const nombreTema = (datos, t) => datos.nombres_temas?.[t] ?? t;

const conMetaPrimero = (a, b) => Boolean(b.meta) - Boolean(a.meta);

// Hasta n propuestas para la tarjeta: las del tema filtrado, o una por tema
// (dentro de cada candidatura se priorizan las que tienen meta; no compara candidaturas)
export function propuestasClave(c, temas, filtro, n = 3) {
  if (filtro) {
    return (c.temas[filtro]?.propuestas ?? []).map((p) => ({ tema: filtro, ...p })).sort(conMetaPrimero).slice(0, n);
  }
  return temas
    .filter((t) => !c.temas[t]?.sin_informacion && c.temas[t]?.propuestas?.length)
    .map((t) => ({ tema: t, ...[...c.temas[t].propuestas].sort(conMetaPrimero)[0] }))
    .sort(conMetaPrimero)
    .slice(0, n);
}
