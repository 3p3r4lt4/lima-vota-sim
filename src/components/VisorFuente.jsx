import { useEffect, useRef } from "react";

export default function VisorFuente({ candidato, seccion, fuentes, onClose }) {
  const ref = useRef(null);
  useEffect(() => { ref.current?.showModal(); }, []);
  const p = candidato.paginas.find((x) => x.pagina === seccion) ?? candidato.paginas[0];
  return (
    <dialog ref={ref} className="visor" onClose={onClose} aria-labelledby="t-visor">
      <header>
        <h2 id="t-visor">{candidato.nombre}</h2>
        <button className="cerrar" onClick={() => ref.current.close()} aria-label="Cerrar">×</button>
      </header>
      <p className="nota">{candidato.organizacion}</p>
      <h3>{p.titulo}</h3>
      <p className="texto-plan">{p.texto}</p>
      <p className="nota">Resumen con palabras propias. Léelo completo en la fuente:</p>
      <ul className="fuentes">
        {p.fuentes.map((f) => (
          <li key={f}>
            <a href={fuentes[f].url} target="_blank" rel="noreferrer">{fuentes[f].medio}: {fuentes[f].titulo}</a>
            <span> ({fuentes[f].fecha})</span>
          </li>
        ))}
      </ul>
    </dialog>
  );
}
