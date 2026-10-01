// Textos que dependen del tipo de fuente: plan de gobierno (PDF) o cobertura del debate
export function etiquetaFuente(datos, p) {
  const f = datos.fuentes[p.fuente];
  return f?.pdf ? `Ver en el plan, p. ${p.pagina}` : `Ver fuente (${f?.medio ?? "prensa"})`;
}

export function textoSinInfo(tipoFuente) {
  return tipoFuente === "plan" ? "Sin propuesta destacada en" : "No aparece en la cobertura sobre";
}

export function textoSinTema(tipoFuente) {
  return tipoFuente === "plan" ? "Sin propuesta destacada en este tema." : "No aparece en la cobertura del debate sobre este tema.";
}

export const JNE = "https://votoinformado.jne.gob.pe";
