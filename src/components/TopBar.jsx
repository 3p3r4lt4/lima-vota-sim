import { IconoChevron, IconoMarca, IconoUbicacion } from "./Iconos.jsx";

export default function TopBar({ ambito, onElegir, abierto }) {
  return (
    <header className="topbar">
      <div className="topbar-in">
        <a className="app-nombre" href="?ambito=1501">
          <IconoMarca />
          <span>Lima Vota <span className="app-anio">2026</span></span>
        </a>
        <button type="button" className="btn-ambito" onClick={onElegir} aria-haspopup="dialog" aria-expanded={abierto}>
          <IconoUbicacion size={18} />
          <span className="sr">Cambiar ámbito. Ahora: </span>
          <span className="btn-ambito-texto">{ambito?.ambito ?? "Elegir distrito"}</span>
          <IconoChevron size={18} />
        </button>
      </div>
    </header>
  );
}
