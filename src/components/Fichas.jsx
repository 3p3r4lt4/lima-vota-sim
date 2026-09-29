import { nombreTema, resumenCandidatura } from "../lib/temas.js";

export default function Fichas({ temas, candidatos, onCita }) {
  return (
    <div className="fichas">
      {candidatos.map((c) => {
        const r = resumenCandidatura(c, temas);
        return (
          <article key={c.id} className="ficha">
            <h3>{c.nombre}</h3>
            <p className="org">{c.organizacion}</p>
            <dl className="datos">
              <div><dt>Propuestas identificadas</dt><dd>{r.total}</dd></div>
              <div><dt>Con cifra o plazo</dt><dd>{r.conMeta} de {r.total}</dd></div>
              <div className="lista"><dt>Temas que no desarrolla</dt>
                <dd>{r.sinDesarrollar.length ? r.sinDesarrollar.map(nombreTema).join(", ") : "Ninguno de los 8"}</dd></div>
            </dl>
            <h4>Propuesta principal por tema</h4>
            <ul className="propuestas">
              {r.principales.map((p) => (
                <li key={p.tema}>
                  <p className="tema">{nombreTema(p.tema)}</p>
                  <p>{p.texto}</p>
                  {p.meta && <p className="meta">Meta: {p.meta}</p>}
                  <button className="cita" onClick={() => onCita(c.id, p.pagina)}>Ver en el plan, p. {p.pagina}</button>
                </li>
              ))}
            </ul>
          </article>
        );
      })}
    </div>
  );
}
