// Convierte **Nombre:** en negrita y [Nombre, p.N] en botones que abren el plan en esa página
export default function Respuesta({ texto, candidatos, onCita }) {
  const porNombre = new Map(candidatos.map((c) => [c.nombre, c.id]));
  return texto.split("\n").filter((l) => l.trim()).map((linea, i) => (
    <p key={i}>
      {linea.split(/(\*\*[^*]+\*\*|\[[^\]]+?, p\.\d+\])/g).map((parte, j) => {
        const negrita = parte.match(/^\*\*(.+)\*\*$/);
        if (negrita) return <strong key={j}>{negrita[1]}</strong>;
        const cita = parte.match(/^\[(.+?), p\.(\d+)\]$/);
        if (cita && porNombre.has(cita[1]))
          return <button key={j} className="cita" onClick={() => onCita(porNombre.get(cita[1]), Number(cita[2]))}>p. {cita[2]}</button>;
        return parte;
      })}
    </p>
  ));
}
