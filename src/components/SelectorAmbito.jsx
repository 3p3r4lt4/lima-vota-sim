import { useMemo, useRef, useState } from "react";
import { useDialogo } from "../hooks/useDialogo.js";
import { IconoBuscar, IconoCerrar } from "./Iconos.jsx";

const normalizar = (s) => s.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLowerCase().trim();

// Hoja inferior (móvil) o ventana centrada (escritorio) para elegir Lima Metropolitana o un distrito
export default function SelectorAmbito({ ambitos, actual, onElegir, onClose }) {
  const [dialogo, cerrar] = useDialogo(onClose);
  const [texto, setTexto] = useState("");
  const lista = useRef(null);

  const filtrados = useMemo(() => {
    const q = normalizar(texto);
    return ambitos.filter((a) => !q || normalizar(a.ambito).includes(q));
  }, [ambitos, texto]);
  const lima = filtrados.filter((a) => a.nivel === "provincial");
  const distritos = filtrados.filter((a) => a.nivel === "distrital");

  const elegir = (u) => { onElegir(u); cerrar(); };
  const botones = () => [...lista.current.querySelectorAll("button")];

  function teclaLista(e) {
    if (e.key !== "ArrowDown" && e.key !== "ArrowUp") return;
    e.preventDefault();
    const b = botones();
    const i = b.indexOf(document.activeElement);
    if (e.key === "ArrowUp" && i <= 0) return dialogo.ref.current.querySelector("input").focus();
    b[Math.min(b.length - 1, i + (e.key === "ArrowDown" ? 1 : -1))]?.focus();
  }

  const opcion = (a) => (
    <li key={a.ubigeo}>
      <button type="button" className="opcion-ambito" aria-current={a.ubigeo === actual ? "true" : undefined} onClick={() => elegir(a.ubigeo)}>
        <span>{a.ambito}</span>
        <span className="opcion-meta">
          {a.candidatos} candidaturas{a.con_propuestas ? " · con propuestas" : ""}
        </span>
      </button>
    </li>
  );

  return (
    <dialog {...dialogo} className="hoja hoja-selector" aria-labelledby="t-selector">
      <div className="hoja-in">
        <div className="hoja-cabecera">
          <h2 id="t-selector">¿Dónde votas?</h2>
          <button type="button" className="btn-icono" onClick={cerrar} aria-label="Cerrar"><IconoCerrar /></button>
        </div>
        <label htmlFor="buscar-ambito" className="etiqueta">Busca tu distrito</label>
        <div className="campo-buscar">
          <IconoBuscar size={18} />
          <input id="buscar-ambito" type="search" value={texto} autoComplete="off" placeholder="Ej.: Ate, La Molina, Surco"
            onChange={(e) => setTexto(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "ArrowDown") { e.preventDefault(); botones()[0]?.focus(); }
              if (e.key === "Enter" && filtrados.length) { e.preventDefault(); elegir(filtrados[0].ubigeo); }
            }} />
        </div>
        <p className="sr" aria-live="polite">{filtrados.length} resultados</p>
        <div className="hoja-lista" ref={lista} onKeyDown={teclaLista}>
          {lima.length > 0 && (<>
            <h3 className="grupo">Provincia</h3>
            <ul>{lima.map(opcion)}</ul>
          </>)}
          {distritos.length > 0 && (<>
            <h3 className="grupo">Distritos de Lima</h3>
            <ul>{distritos.map(opcion)}</ul>
          </>)}
          {filtrados.length === 0 && <p className="vacio">No encontramos «{texto}». Revisa cómo está escrito.</p>}
        </div>
      </div>
    </dialog>
  );
}
