import { nombreTema } from "../lib/temas.js";

// Tabla real (accesible); en móvil se reorganiza en bloques por tema vía CSS
export default function LadoALado({ temas, candidatos, onCita }) {
  return (
    <div className="tabla-scroll" tabIndex={0} aria-label="Tabla comparativa, desplazable">
      <table className="comparativa" style={{ "--n": candidatos.length }}>
        <caption className="sr">Propuestas por tema de cada candidatura</caption>
        <thead>
          <tr>
            <th scope="col">Tema</th>
            {candidatos.map((c) => <th scope="col" key={c.id}>{c.nombre}</th>)}
          </tr>
        </thead>
        <tbody>
          {temas.map((t) => (
            <tr key={t}>
              <th scope="row">{nombreTema(t)}</th>
              {candidatos.map((c) => {
                const d = c.temas[t];
                return (
                  <td key={c.id} data-candidato={c.nombre} className={d?.sin_informacion ? "celda-vacia" : undefined}>
                    {d?.sin_informacion ? (
                      <p className="sin-info">El plan no desarrolla este tema.</p>
                    ) : (
                      <ul className="propuestas">
                        {d.propuestas.map((p, i) => (
                          <li key={i}>
                            <p>{p.texto}</p>
                            <p className="meta">{p.meta ? `Meta: ${p.meta}` : "Sin cifra ni plazo"}</p>
                            <button className="cita" onClick={() => onCita(c.id, p.pagina)}>Ver en el plan, p. {p.pagina}</button>
                          </li>
                        ))}
                      </ul>
                    )}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
