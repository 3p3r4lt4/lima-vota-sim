import { nombreCorto, nombreTema } from "../lib/temas.js";

// Fila de chips desplazable (solo la fila se desplaza, nunca la página)
export default function ChipsTema({ datos, tema, onTema }) {
  const opciones = [["", "Todos"], ...datos.temas.map((t) => [t, nombreCorto(datos, t)])];
  return (
    <div className="chips-tema" role="group" aria-label="Filtrar propuestas por tema">
      {opciones.map(([t, etiqueta]) => (
        <button key={t || "todos"} type="button" className="chip chip-tema" aria-pressed={tema === t}
          title={t ? nombreTema(datos, t) : undefined} onClick={() => onTema(t)}>
          {etiqueta}
        </button>
      ))}
    </div>
  );
}
