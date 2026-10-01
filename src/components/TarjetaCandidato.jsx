import { memo } from "react";
import { nombreCorto, propuestasClave, resumenCandidatura } from "../lib/temas.js";
import { etiquetaFuente, textoSinInfo, textoSinTema } from "../lib/fuente.js";

function TarjetaCandidato({ c, datos, tema, elegido, onComparar, onVerTodo, onCita }) {
  const r = resumenCandidatura(c, datos.temas);
  const clave = propuestasClave(c, datos.temas, tema);
  const idTitulo = `cand-${c.id}`;
  return (
    <article className={`tarjeta${elegido ? " tarjeta-elegida" : ""}`} aria-labelledby={idTitulo}>
      <header className="tarjeta-cabecera">
        <h3 id={idTitulo} className="tarjeta-nombre">{c.nombre}</h3>
        <p className="tarjeta-org">{c.organizacion}</p>
        {c.cargo_nota && <p className="nota-cargo">{c.cargo_nota}</p>}
        <p className="indicador">
          {r.total} {r.total === 1 ? "propuesta" : "propuestas"} · {r.conMeta} con meta concreta
        </p>
      </header>

      {clave.length ? (
        <ul className="claves">
          {clave.map((p, i) => (
            <li key={i} className="clave">
              {!tema && <span className="clave-tema">{nombreCorto(datos, p.tema)}</span>}
              <p className="clave-texto">{p.texto}</p>
              {p.meta && <p className="clave-meta">Meta: {p.meta}</p>}
              <button type="button" className="enlace enlace-fuente" onClick={() => onCita(c.id, p.pagina)}>
                {etiquetaFuente(datos, p)}<span className="sr"> — {c.nombre}</span>
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p className="sin-tema">{tema ? textoSinTema(datos.tipo_fuente) : "Sin propuestas registradas."}</p>
      )}

      {!tema && r.sinTema.length > 0 && (
        <div className="sin-info">
          <span className="sin-info-txt">{textoSinInfo(datos.tipo_fuente)}:</span>
          <ul className="etiquetas">
            {r.sinTema.map((t) => <li key={t} className="etiqueta-gris">{nombreCorto(datos, t)}</li>)}
          </ul>
        </div>
      )}

      <footer className="tarjeta-pie">
        <button type="button" className="btn btn-sec" aria-haspopup="dialog" onClick={() => onVerTodo(c.id)}>
          Ver todo<span className="sr"> de {c.nombre}</span>
        </button>
        <label className="comparar-check">
          <input type="checkbox" checked={elegido} onChange={() => onComparar(c.id)} />
          <span>Comparar<span className="sr"> a {c.nombre}</span></span>
        </label>
      </footer>
    </article>
  );
}

export default memo(TarjetaCandidato);
