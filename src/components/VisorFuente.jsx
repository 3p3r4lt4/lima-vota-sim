import { useEffect, useRef, useState } from "react";

// Muestra la fuente de una cita: una página del plan de gobierno (PDF) o una sección con enlaces a prensa
export default function VisorFuente({ candidato, seccion, fuentes, onClose }) {
  const ref = useRef(null);
  const [actual, setActual] = useState(seccion);
  useEffect(() => { ref.current?.showModal(); }, []);
  const paginas = candidato.paginas;
  const i = Math.max(0, paginas.findIndex((x) => x.pagina === actual));
  const p = paginas[i];
  const esPdf = Boolean(candidato.pdf);
  return (
    <dialog ref={ref} className="visor" onClose={onClose} aria-labelledby="t-visor">
      <header>
        <h2 id="t-visor">{candidato.nombre}</h2>
        <button className="cerrar" onClick={() => ref.current.close()} aria-label="Cerrar">×</button>
      </header>
      <p className="nota">{candidato.organizacion}</p>
      <h3>{esPdf ? `Plan de gobierno, página ${p.pagina}` : p.titulo}</h3>
      <div className={esPdf ? "texto-plan texto-pdf" : "texto-plan"}>{p.texto}</div>
      {esPdf ? (
        <>
          <p><a className="boton-pdf" href={`${candidato.pdf}#page=${p.pagina}`} target="_blank" rel="noreferrer">Abrir el PDF oficial en esta página</a></p>
          <nav className="paginador">
            <button disabled={i === 0} onClick={() => setActual(paginas[i - 1].pagina)}>Página anterior</button>
            <button disabled={i === paginas.length - 1} onClick={() => setActual(paginas[i + 1].pagina)}>Página siguiente</button>
          </nav>
        </>
      ) : (
        <>
          <p className="nota">Resumen con palabras propias. Léelo completo en la fuente:</p>
          <ul className="fuentes">
            {p.fuentes.map((f) => (
              <li key={f}>
                <a href={fuentes[f].url} target="_blank" rel="noreferrer">{fuentes[f].medio}: {fuentes[f].titulo}</a>
                <span> ({fuentes[f].fecha})</span>
              </li>
            ))}
          </ul>
        </>
      )}
    </dialog>
  );
}
