import { resumenCandidatura } from "../lib/temas.js";

export default function Fichas({ datos, candidatos, onCita }) {
  const nombre = (t) => datos.nombres_temas?.[t] ?? t;
  return (
    <div className="fichas">
      {candidatos.map((c) => {
        const r = resumenCandidatura(c, datos.temas);
        return (
          <article key={c.id} className="ficha">
            <h3>{c.nombre}</h3>
            <p className="org">{c.organizacion}</p>
            {c.cargo_nota && <p className="nota-cargo">{c.cargo_nota}</p>}
            <dl className="datos">
              <div><dt>Propuestas identificadas</dt><dd>{r.total}</dd></div>
              <div><dt>Con cifra o plazo</dt><dd>{r.conMeta} de {r.total}</dd></div>
              <div className="lista"><dt>Temas sin propuestas en la cobertura</dt>
                <dd>{r.sinTema.length ? r.sinTema.map(nombre).join(", ") : "Ninguno"}</dd></div>
            </dl>
            <h4>Propuesta principal por tema</h4>
            <ul className="propuestas">
              {r.principales.map((p) => (
                <li key={p.tema}>
                  <p className="tema">{nombre(p.tema)}</p>
                  <p>{p.texto}</p>
                  {p.meta && <p className="meta">Meta: {p.meta}</p>}
                  <button className="cita" onClick={() => onCita(c.id, p.pagina)}>Ver fuente ({datos.fuentes[p.fuente]?.medio})</button>
                </li>
              ))}
            </ul>
          </article>
        );
      })}
    </div>
  );
}
