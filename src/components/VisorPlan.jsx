import { useEffect, useRef } from "react";

export default function VisorPlan({ candidato, pagina, simulado, onClose, onPagina }) {
  const ref = useRef(null);
  useEffect(() => { ref.current?.showModal(); }, []);
  if (!candidato) return null;
  const paginas = candidato.paginas;
  const i = Math.max(0, paginas.findIndex((p) => p.pagina === pagina));
  const p = paginas[i];
  return (
    <dialog ref={ref} className="visor" onClose={onClose} aria-labelledby="t-visor">
      <header>
        <h2 id="t-visor">Plan de gobierno de {candidato.nombre}</h2>
        <button className="cerrar" onClick={() => ref.current.close()} aria-label="Cerrar">×</button>
      </header>
      {simulado && <p className="nota">Documento simulado con fines de demostración.</p>}
      <p className="pag">Página {p.pagina} de {paginas.length}</p>
      <h3>{p.titulo}</h3>
      <p className="texto-plan">{p.texto}</p>
      {candidato.plan_url && (
        <p><a href={`${candidato.plan_url}#page=${p.pagina}`} target="_blank" rel="noreferrer">Abrir el PDF oficial en esta página</a></p>
      )}
      <nav className="paginador">
        <button disabled={i === 0} onClick={() => onPagina(paginas[i - 1].pagina)}>Página anterior</button>
        <button disabled={i === paginas.length - 1} onClick={() => onPagina(paginas[i + 1].pagina)}>Página siguiente</button>
      </nav>
    </dialog>
  );
}
