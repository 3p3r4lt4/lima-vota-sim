import { JNE } from "../lib/fuente.js";

export default function AvisoSinPropuestas({ ambito, onVerLima }) {
  return (
    <section className="hero aviso-distrito" aria-labelledby="t-hero">
      <h1 id="t-hero" className="hero-titulo">Candidaturas en {ambito}</h1>
      <p>
        Aún no comparamos propuestas en este distrito: solo las mostramos cuando tenemos los planes de
        <strong> todas</strong> las candidaturas, para no favorecer a ninguna.
      </p>
      <div className="acciones">
        <a className="btn btn-primario" href={JNE} target="_blank" rel="noreferrer">
          Ver planes en Voto Informado (JNE)<span className="sr"> (se abre en otra pestaña)</span>
        </a>
        <button type="button" className="btn btn-sec" onClick={onVerLima}>Ver Lima Metropolitana</button>
      </div>
    </section>
  );
}
