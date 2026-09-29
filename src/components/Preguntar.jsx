import { useMemo, useState } from "react";
import Respuesta from "../lib/Respuesta.jsx";

const BANCO = [
  "¿Quiénes proponen armar al serenazgo?", "¿Qué proponen para el Metropolitano, el metro o el tren?",
  "¿Qué harán con el agua en los cerros?", "¿Quiénes hablan de cámaras con inteligencia artificial?",
  "¿Qué proponen sobre el comercio ambulatorio?", "¿Qué proponen para la vivienda y la titulación?",
  "¿Quiénes proponen una Policía Municipal?", "¿Qué dicen sobre hospitales y salud?",
  "¿Qué proponen contra la extorsión y el sicariato?", "¿Qué harán con la ATU?",
  "¿Qué proponen para los jóvenes?", "¿Qué proponen sobre los ríos y el ambiente?",
  "¿Quiénes proponen recompensas por delincuentes?", "¿Qué harán ante un sismo o El Niño?",
];
const alAzar = (n) => [...BANCO].sort(() => Math.random() - 0.5).slice(0, n);

export default function Preguntar({ ubigeo, ambito, candidatos, onCita, onCambiarAmbito }) {
  const [pregunta, setPregunta] = useState("");
  const [ejemplos, setEjemplos] = useState(() => alAzar(3));
  const [r, setR] = useState({ cargando: false, data: null, error: "" });

  async function enviar(q = pregunta) {
    if (q.trim().length < 5 || candidatos.length === 0) return;
    setPregunta(q);
    setR({ cargando: true, data: null, error: "" });
    try {
      const res = await fetch("/api/preguntar", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ pregunta: q, ubigeo, candidatoIds: candidatos.map((c) => c.id) }),
      });
      if (res.status === 429) throw new Error("Hiciste muchas preguntas seguidas. Espera un minuto y vuelve a intentar.");
      const d = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(d.error ?? "No se pudo responder. Intenta de nuevo.");
      setR({ cargando: false, data: d, error: "" });
    } catch (e) {
      setR({ cargando: false, data: null, error: e.message });
    }
  }

  const d = r.data;
  return (
    <section className="preguntar" aria-labelledby="t-preg">
      <h2 id="t-preg" className="seccion">Pregunta sobre un tema</h2>
      <p className="nota">Se busca en las propuestas de las {candidatos.length} candidaturas marcadas de {ambito}.</p>
      <form className="fila" onSubmit={(e) => { e.preventDefault(); enviar(); }}>
        <label className="sr" htmlFor="q">Tu pregunta</label>
        <input id="q" value={pregunta} maxLength={300} onChange={(e) => setPregunta(e.target.value)}
          placeholder="Escribe tu pregunta" autoComplete="off" />
        <button type="submit" disabled={r.cargando || pregunta.trim().length < 5 || candidatos.length === 0}>
          {r.cargando ? "Buscando…" : "Preguntar"}
        </button>
      </form>
      <div className="ejemplos">
        {ejemplos.map((e) => <button key={e} className="chip" onClick={() => enviar(e)}>{e}</button>)}
        <button className="chip chip-azar" onClick={() => { const [q] = alAzar(1); setEjemplos(alAzar(3)); enviar(q); }}>
          Pregunta al azar
        </button>
      </div>
      {r.error && <p className="aviso" role="alert">{r.error}</p>}
      <div aria-live="polite">
        {d && (
          <div className="respuesta">
            <Respuesta texto={d.respuesta} candidatos={candidatos} onCita={onCita} />
            {d.tipo === "otro_ambito" && (
              <button className="enlace" onClick={() => onCambiarAmbito(d.ubigeo)}>Ir a {d.ambito}</button>
            )}
            {d.tipo === "respuesta" && (
              <p className="modo">
                {d.modo?.generacion === "claude"
                  ? "Respuesta redactada con IA a partir de las fuentes citadas. Verifica en la fuente."
                  : "Respuesta compuesta con frases de las fuentes citadas."}
              </p>
            )}
          </div>
        )}
      </div>
    </section>
  );
}
