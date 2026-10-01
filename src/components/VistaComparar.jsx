import { useRef, useState } from "react";
import { useDialogo } from "../hooks/useDialogo.js";
import { useMedia } from "../hooks/useMedia.js";
import { nombreTema, resumenCandidatura } from "../lib/temas.js";
import { etiquetaFuente, textoSinTema } from "../lib/fuente.js";
import { IconoCerrar } from "./Iconos.jsx";

function Celda({ c, t, datos, onCita }) {
  const d = c.temas[t];
  if (!d || d.sin_informacion) return <p className="sin-tema">{textoSinTema(datos.tipo_fuente)}</p>;
  return (
    <ul className="det-lista">
      {d.propuestas.map((p, i) => (
        <li key={i}>
          <p>{p.texto}</p>
          <p className="clave-meta-completa">{p.meta ? `Meta: ${p.meta}` : "Sin cifra ni plazo"}</p>
          <button type="button" className="enlace enlace-fuente" onClick={() => onCita(c.id, p.pagina)}>
            {etiquetaFuente(datos, p)}<span className="sr"> — {c.nombre}</span>
          </button>
        </li>
      ))}
    </ul>
  );
}

// Escritorio/tablet: columnas por candidatura y filas por tema. Móvil: una pestaña por candidatura.
export default function VistaComparar({ candidatos, datos, onCita, aviso, onClose }) {
  const [dialogo, cerrar] = useDialogo(onClose);
  const ancho = useMedia("(min-width: 768px)");
  const [activa, setActiva] = useState(0);
  const tabs = useRef([]);

  function teclaTabs(e) {
    const n = candidatos.length;
    const destino = { ArrowRight: (activa + 1) % n, ArrowLeft: (activa - 1 + n) % n, Home: 0, End: n - 1 }[e.key];
    if (destino === undefined) return;
    e.preventDefault();
    setActiva(destino);
    tabs.current[destino]?.focus();
  }

  const cabecera = (c) => {
    const r = resumenCandidatura(c, datos.temas);
    return (<>
      <span className="cmp-nombre">{c.nombre}</span>
      <span className="cmp-org">{c.organizacion}</span>
      <span className="cmp-ind">{r.total} propuestas · {r.conMeta} con meta</span>
    </>);
  };

  return (
    <dialog {...dialogo} className="panel panel-comparar" aria-labelledby="t-comparar">
      <div className="panel-cabecera">
        <h2 id="t-comparar">Comparar propuestas</h2>
        <button type="button" className="btn-icono" onClick={cerrar} aria-label="Cerrar"><IconoCerrar /></button>
      </div>
      {aviso && <p className="aviso aviso-panel" role="alert">{aviso}</p>}

      {ancho ? (
        <div className="panel-cuerpo">
          <div className="cmp-fila cmp-encabezado" style={{ "--n": candidatos.length }}>
            {candidatos.map((c) => <div key={c.id} className="cmp-cab">{cabecera(c)}</div>)}
          </div>
          {datos.temas.map((t) => (
            <section key={t} className="det-tema" aria-labelledby={`cmp-${t}`}>
              <h3 id={`cmp-${t}`}>{nombreTema(datos, t)}</h3>
              <div className="cmp-fila" style={{ "--n": candidatos.length }}>
                {candidatos.map((c) => (
                  <div key={c.id} className="cmp-celda">
                    <p className="sr">{c.nombre}</p>
                    <Celda c={c} t={t} datos={datos} onCita={onCita} />
                  </div>
                ))}
              </div>
            </section>
          ))}
        </div>
      ) : (
        <>
          <div className="cmp-tabs" role="tablist" aria-label="Candidaturas" onKeyDown={teclaTabs}>
            {candidatos.map((c, i) => (
              <button key={c.id} ref={(el) => (tabs.current[i] = el)} type="button" role="tab" id={`tab-${c.id}`}
                aria-selected={activa === i} aria-controls={`tabpanel-${c.id}`} tabIndex={activa === i ? 0 : -1}
                className="cmp-tab" onClick={() => setActiva(i)}>
                {c.nombre}
              </button>
            ))}
          </div>
          {candidatos.map((c, i) => (
            <div key={c.id} role="tabpanel" id={`tabpanel-${c.id}`} aria-labelledby={`tab-${c.id}`} hidden={activa !== i}
              className="panel-cuerpo" tabIndex={0}>
              <p className="cmp-cab cmp-cab-movil">{cabecera(c)}</p>
              {datos.temas.map((t) => (
                <section key={t} className="det-tema">
                  <h3>{nombreTema(datos, t)}</h3>
                  <Celda c={c} t={t} datos={datos} onCita={onCita} />
                </section>
              ))}
            </div>
          ))}
        </>
      )}
    </dialog>
  );
}
