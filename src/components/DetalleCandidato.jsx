import { useEffect } from "react";
import { useDialogo } from "../hooks/useDialogo.js";
import { nombreTema, resumenCandidatura } from "../lib/temas.js";
import { etiquetaFuente, textoSinTema } from "../lib/fuente.js";
import { enlaceReporte } from "../lib/reporte.js";
import { IconoCerrar } from "./Iconos.jsx";

// Panel lateral (escritorio) u hoja a pantalla completa (móvil) con todas las propuestas por tema.
// Usa solo los datos de comparaciones/{ubigeo}.json; el plan completo se carga al abrir una fuente.
export default function DetalleCandidato({ c, datos, tema, elegido, puedeAgregar, onComparar, onCita, aviso, onClose }) {
  const [dialogo, cerrar] = useDialogo(onClose);
  const r = resumenCandidatura(c, datos.temas);

  useEffect(() => {
    if (tema) dialogo.ref.current?.querySelector(`#det-${tema}`)?.scrollIntoView({ block: "start" });
  }, []);

  return (
    <dialog {...dialogo} className="panel" aria-labelledby="t-detalle">
      <div className="panel-cabecera">
        <div>
          <h2 id="t-detalle">{c.nombre}</h2>
          <p className="tarjeta-org">{c.organizacion}</p>
          <p className="indicador">{r.total} propuestas · {r.conMeta} con meta concreta</p>
        </div>
        <button type="button" className="btn-icono" onClick={cerrar} aria-label="Cerrar"><IconoCerrar /></button>
      </div>
      {aviso && <p className="aviso aviso-panel" role="alert">{aviso}</p>}
      <div className="panel-cuerpo">
        {c.cargo_nota && <p className="nota-cargo">{c.cargo_nota}</p>}
        {datos.temas.map((t) => {
          const d = c.temas[t];
          return (
            <section key={t} id={`det-${t}`} className="det-tema" aria-labelledby={`det-t-${t}`}>
              <h3 id={`det-t-${t}`}>{nombreTema(datos, t)}</h3>
              {!d || d.sin_informacion ? (
                <p className="sin-tema">{textoSinTema(datos.tipo_fuente)}</p>
              ) : (
                <ul className="det-lista">
                  {d.propuestas.map((p, i) => (
                    <li key={i}>
                      <p>{p.texto}</p>
                      <p className="clave-meta-completa">{p.meta ? `Meta: ${p.meta}` : "Sin cifra ni plazo"}</p>
                      <button type="button" className="enlace enlace-fuente" onClick={() => onCita(c.id, p.pagina)}>
                        {etiquetaFuente(datos, p)}
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </section>
          );
        })}
        <p className="nota-reporte">
          ¿Ves algo que no coincide con la fuente?{" "}
          <a href={enlaceReporte({ ambito: datos.ambito, candidato: c })}>Repórtalo por correo</a>
        </p>
      </div>
      <div className="panel-pie">
        <button type="button" className="btn btn-sec" disabled={!elegido && !puedeAgregar} onClick={() => onComparar(c.id)}>
          {elegido ? "Quitar de comparar" : puedeAgregar ? "Agregar a comparar" : "Ya elegiste 3 para comparar"}
        </button>
        <button type="button" className="btn btn-primario" onClick={cerrar}>Cerrar</button>
      </div>
    </dialog>
  );
}
