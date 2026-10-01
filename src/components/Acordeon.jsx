import { IconoChevron } from "./Iconos.jsx";

// <details> nativo: accesible por teclado y lector de pantalla sin JavaScript extra
export default function Acordeon({ titulo, children }) {
  return (
    <details className="acordeon">
      <summary>
        <h2 className="acordeon-titulo">{titulo}</h2>
        <IconoChevron />
      </summary>
      <div className="acordeon-cuerpo">{children}</div>
    </details>
  );
}
