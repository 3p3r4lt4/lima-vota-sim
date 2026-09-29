export default function Cedula({ candidatos, marcados, setMarcados }) {
  const alternar = (id) => {
    const s = new Set(marcados);
    s.has(id) ? s.delete(id) : s.add(id);
    setMarcados(s);
  };
  const todos = marcados.size === candidatos.length;
  return (
    <>
      <div className="cedula" role="group" aria-label="Candidaturas a comparar">
        {candidatos.map((c) => (
          <button key={c.id} className="casilla" aria-pressed={marcados.has(c.id)} onClick={() => alternar(c.id)}>
            <span className="marca" aria-hidden="true" />
            <span className="casilla-texto">
              <strong>{c.nombre}</strong>
              <span>{c.organizacion}</span>
            </span>
          </button>
        ))}
      </div>
      <button className="enlace" onClick={() => setMarcados(new Set(todos ? [] : candidatos.map((c) => c.id)))}>
        {todos ? "Desmarcar todas" : "Marcar todas"}
      </button>
    </>
  );
}
