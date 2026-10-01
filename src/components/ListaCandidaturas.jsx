// Lista simple para distritos sin propuestas comparables
export default function ListaCandidaturas({ datos, candidatos }) {
  const alcaldia = candidatos.filter((c) => !c.cargo_nota).length;
  return (
    <section className="seccion" aria-labelledby="t-lista">
      <h2 id="t-lista" className="seccion-titulo">{alcaldia} candidaturas a la alcaldía</h2>
      <p className="seccion-nota">El orden es aleatorio en cada visita.</p>
      <ul className="lista-simple">
        {candidatos.map((c) => (
          <li key={c.id} className="lista-item">
            <strong>{c.nombre}</strong>
            <span>{c.organizacion}</span>
            {c.cargo_nota && <span className="nota-cargo">{c.cargo_nota}</span>}
          </li>
        ))}
      </ul>
    </section>
  );
}
