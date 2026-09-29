// Recuperación léxica (BM25) sobre el corpus simulado, sin dependencias.
// Se usa cuando no hay pgvector configurado; también sirve de respaldo si la base falla.

const STOP = new Set(("que para con por los las del una uno unos unas como mas pero sus este esta estos estas " +
  "hay son ser fue era muy sin sobre entre cual cuales quien donde cuando tiene tienen proponen propone " +
  "propuesta propuestas candidato candidatos candidatura candidaturas plan planes distrito lima dice hace debate").split(" "));

export const normalizar = (t) => t.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");

// Raíz aproximada: 6 primeros caracteres une singular/plural y derivaciones cercanas
export function terminos(texto) {
  return (normalizar(texto).match(/[a-z0-9ñ]+/g) ?? [])
    .filter((w) => w.length > 2 && !STOP.has(w))
    .map((w) => w.slice(0, 6));
}

export function buscar(planes, pregunta, ids, porCandidato = 2) {
  const q = [...new Set(terminos(pregunta))];
  if (q.length === 0) return [];
  const docs = [];
  for (const c of planes.candidatos) {
    if (!ids.includes(c.id)) continue;
    for (const p of c.paginas) {
      const tf = new Map();
      for (const t of terminos(`${p.titulo} ${p.texto}`)) tf.set(t, (tf.get(t) ?? 0) + 1);
      docs.push({ candidatoId: c.id, nombre: c.nombre, pagina: p.pagina, titulo: p.titulo, texto: p.texto, tf,
        largo: [...tf.values()].reduce((a, b) => a + b, 0) });
    }
  }
  if (docs.length === 0) return [];
  const prom = docs.reduce((a, d) => a + d.largo, 0) / docs.length;
  const df = new Map(q.map((t) => [t, docs.filter((d) => d.tf.has(t)).length]));
  const k1 = 1.2, b = 0.75, N = docs.length;
  for (const d of docs) {
    d.score = q.reduce((s, t) => {
      const f = d.tf.get(t) ?? 0;
      if (!f) return s;
      const idf = Math.log(1 + (N - df.get(t) + 0.5) / (df.get(t) + 0.5));
      return s + idf * (f * (k1 + 1)) / (f + k1 * (1 - b + (b * d.largo) / prom));
    }, 0);
  }
  // Balanceo: los mejores fragmentos de CADA candidato, para no favorecer a quien escribió más
  const porId = new Map();
  for (const d of docs.filter((d) => d.score > 0).sort((a, b) => b.score - a.score)) {
    const l = porId.get(d.candidatoId) ?? [];
    if (l.length < porCandidato) l.push(d);
    porId.set(d.candidatoId, l);
  }
  return [...porId.values()].flat().map(({ tf, largo, ...r }) => r);
}

// Respuesta sin IA generativa: frases textuales de las fuentes, con cita, mismo formato para todos.
// Quienes no mencionaron el tema se agrupan en una sola línea al final.
export function respuestaExtractiva(pregunta, fragmentos, candidatos) {
  const q = new Set(terminos(pregunta));
  const lineas = [], sinTema = [];
  for (const c of candidatos) {
    const frs = fragmentos.filter((f) => f.candidatoId === c.id);
    if (frs.length === 0) { sinTema.push(c.nombre); continue; }
    const oraciones = frs.flatMap((f) => f.texto.split(/(?<=\.)\s+/).map((o) => ({ o, p: f.pagina,
      s: terminos(o).filter((t) => q.has(t)).length })));
    const top = oraciones.filter((x) => x.s > 0).sort((a, b) => b.s - a.s).slice(0, 2);
    const usar = top.length ? top : oraciones.slice(0, 1);
    lineas.push(`**${c.nombre}:** ` + usar.map((x) => `${x.o.replace(/\.$/, "")} [${c.nombre}, p.${x.p}]`).join(". ") + ".");
  }
  if (sinTema.length) lineas.push(`**No mencionaron este tema en las fuentes revisadas:** ${sinTema.join(", ")}.`);
  return lineas.join("\n");
}

// Preguntas sobre quiénes postulan: se responden con la lista oficial, sin buscar en propuestas
export function esPreguntaDeLista(pregunta) {
  const t = normalizar(pregunta);
  return /(quien|quienes|lista|listame|listar|cuantos|cuales son|nombres?)/.test(t) &&
    /(candidat|postul|listas|partidos|organizaciones)/.test(t) &&
    !/(propon|propuesta|plantea|haran|hara|promete)/.test(t);
}
