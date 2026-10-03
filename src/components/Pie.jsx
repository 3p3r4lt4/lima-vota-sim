import { JNE } from "../lib/fuente.js";
import { enlaceReporte } from "../lib/reporte.js";

const LINKEDIN = "https://www.linkedin.com/in/eduardo-peralta-quica%C3%B1o-a53766b8/";

export default function Pie({ datos }) {
  return (
    <footer className="pie">
      {datos && <p>{datos.nota_fuente} Datos al {datos.corte}.</p>}
      <p>
        Elecciones Regionales y Municipales, domingo 4 de octubre de 2026. Proyecto personal, independiente y sin
        afiliación política: no recomienda candidaturas ni asigna puntajes. Las propuestas están redactadas con palabras
        propias a partir de las fuentes citadas y pueden contener errores; verifica siempre en la fuente y en{" "}
        <a href={JNE} target="_blank" rel="noreferrer">Voto Informado del JNE</a>.
      </p>
      <p>
        Autor: Eduardo Peralta ·{" "}
        <a href={LINKEDIN} target="_blank" rel="noreferrer">LinkedIn</a> ·{" "}
        <a href={enlaceReporte({ ambito: datos?.ambito })}>Reportar un error</a> ·{" "}
        <a href="/privacidad">Privacidad</a>
      </p>
    </footer>
  );
}
