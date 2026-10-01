import { useState } from "react";
import { useDialogo } from "../hooks/useDialogo.js";
import { IconoCerrar, IconoDocumento } from "./Iconos.jsx";

// Muestra la fuente de una cita: una página del plan de gobierno (PDF) o una sección con enlaces a prensa
export default function VisorFuente({ candidato, seccion, fuentes, onClose }) {
  const [dialogo, cerrar] = useDialogo(onClose);
  const [actual, setActual] = useState(seccion);
  const paginas = candidato.paginas;
  const i = Math.max(0, paginas.findIndex((x) => x.pagina === actual));
  const p = paginas[i];
  const esPdf = Boolean(candidato.pdf);
  return (
    <dialog {...dialogo} className="hoja visor" aria-labelledby="t-visor">
      <div className="hoja-in">
        <div className="hoja-cabecera">
          <div>
            <h2 id="t-visor">{candidato.nombre}</h2>
            <p className="tarjeta-org">{candidato.organizacion}</p>
          </div>
          <button type="button" className="btn-icono" onClick={cerrar} aria-label="Cerrar"><IconoCerrar /></button>
        </div>
        <h3 className="visor-titulo">{esPdf ? `Plan de gobierno, página ${p.pagina}` : p.titulo}</h3>
        <div className={esPdf ? "texto-plan texto-pdf" : "texto-plan"} tabIndex={esPdf ? 0 : undefined}
          aria-label={esPdf ? `Texto de la página ${p.pagina}` : undefined}>{p.texto}</div>
        {esPdf ? (
          <>
            <a className="btn btn-primario visor-pdf" href={`${candidato.pdf}#page=${p.pagina}`} target="_blank" rel="noreferrer">
              <IconoDocumento size={18} /> Abrir el PDF oficial en esta página<span className="sr"> (se abre en otra pestaña)</span>
            </a>
            <nav className="paginador" aria-label="Páginas del plan">
              <button type="button" className="btn btn-sec" disabled={i === 0} onClick={() => setActual(paginas[i - 1].pagina)}>Página anterior</button>
              <button type="button" className="btn btn-sec" disabled={i === paginas.length - 1} onClick={() => setActual(paginas[i + 1].pagina)}>Página siguiente</button>
            </nav>
          </>
        ) : (
          <>
            <p className="seccion-nota">Resumen con palabras propias. Léelo completo en la fuente:</p>
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
      </div>
    </dialog>
  );
}
