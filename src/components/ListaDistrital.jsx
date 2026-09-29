export default function ListaDistrital({ datos, candidatos, onVerLima }) {
  return (
    <section aria-labelledby="t-dist">
      <h2 id="t-dist" className="seccion">{candidatos.length} candidaturas a la alcaldía de {datos.ambito}</h2>
      <p className="nota">El orden es aleatorio en cada visita.</p>
      <ul className="cedula lista-distrital">
        {candidatos.map((c) => (
          <li key={c.id} className="casilla">
            <span className="marca" aria-hidden="true" />
            <span className="casilla-texto"><strong>{c.nombre}</strong><span>{c.organizacion}</span></span>
          </li>
        ))}
      </ul>
      <div className="aviso-distrito">
        <p>
          <strong>Aún no comparamos propuestas distritales.</strong> La cobertura de prensa en los distritos es parcial
          (suele incluir solo a dos o tres candidaturas), y mostrarla favorecería a unas sobre otras.
        </p>
        <p>
          Para comparar, abre los planes de gobierno y las hojas de vida oficiales en{" "}
          <a href="https://votoinformado.jne.gob.pe" target="_blank" rel="noreferrer">Voto Informado del JNE</a>.
          Mientras tanto, puedes <button className="enlace" onClick={onVerLima}>comparar las propuestas para Lima Metropolitana</button>, que también se votan el domingo.
        </p>
      </div>
    </section>
  );
}
