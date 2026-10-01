import { IconoCerrar, IconoColumnas } from "./Iconos.jsx";

// Barra flotante inferior: aparece al marcar la primera candidatura; compara con 2 o 3
export default function BarraComparar({ elegidos, max, onAbrir, onQuitar, onLimpiar }) {
  if (elegidos.length === 0) return null;
  const listo = elegidos.length >= 2;
  return (
    <div className="barra-comparar" role="region" aria-label="Candidaturas para comparar">
      <div className="barra-in">
        <ul className="barra-elegidos">
          {elegidos.map((c) => (
            <li key={c.id} className="barra-chip">
              <span className="barra-chip-nombre">{c.nombre}</span>
              <button type="button" className="barra-quitar" onClick={() => onQuitar(c.id)} aria-label={`Quitar a ${c.nombre} de la comparación`}>
                <IconoCerrar size={16} />
              </button>
            </li>
          ))}
        </ul>
        <div className="barra-info">
          <p className="barra-estado" aria-live="polite">
            {listo ? (elegidos.length >= max ? `Máximo ${max}.` : "Puedes sumar una más.") : "Elige al menos 2."}
          </p>
          <button type="button" className="enlace" onClick={onLimpiar}>Quitar todas</button>
        </div>
        <button type="button" className="btn btn-primario" disabled={!listo} onClick={onAbrir} aria-haspopup="dialog">
          <IconoColumnas size={18} /> Comparar ({elegidos.length})
        </button>
      </div>
    </div>
  );
}
