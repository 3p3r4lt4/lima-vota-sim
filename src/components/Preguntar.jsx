import { useState } from "react";
import Respuesta from "../lib/Respuesta.jsx";

const EJEMPLOS = ["¿Qué harán con el comercio ambulatorio?", "¿Cómo mejorarán el recojo de basura?", "¿Qué proponen para el adulto mayor?"];

export default function Preguntar({ ubigeo, ambito, candidatos, onCita }) {
  const [pregunta, setPregunta] = useState("");
  const [r, setR] = useState({ cargando: false, respuesta: "", modo: null, error: "" });

  async function enviar(q = pregunta) {
    if (q.trim().length < 5 || candidatos.length === 0) return;
    setPregunta(q);
    setR({ cargando: true, respuesta: "", modo: null, error: "" });
    try {
      const res = await fetch("/api/preguntar", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ pregunta: q, ubigeo, candidatoIds: candidatos.map((c) => c.id) }),
      });
      if (res.status === 429) throw new Error("Hiciste muchas preguntas seguidas. Espera un minuto y vuelve a intentar.");
      const d = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(d.error ?? "No se pudo responder. Intenta de nuevo.");
      setR({ cargando: false, respuesta: d.respuesta, modo: d.modo, error: "" });
    } catch (e) {
      setR({ cargando: false, respuesta: "", modo: null, error: e.message });
    }
  }

  return (
    <section className="preguntar" aria-labelledby="t-preg">
      <h2 id="t-preg" className="seccion">Pregunta sobre un tema específico</h2>
      <p className="nota">Se busca solo en los planes de las {candidatos.length} candidaturas marcadas de {ambito}.</p>
      <form className="fila" onSubmit={(e) => { e.preventDefault(); enviar(); }}>
        <label className="sr" htmlFor="q">Tu pregunta</label>
        <input id="q" value={pregunta} maxLength={300} onChange={(e) => setPregunta(e.target.value)}
          placeholder="Escribe tu pregunta" autoComplete="off" />
        <button type="submit" disabled={r.cargando || pregunta.trim().length < 5 || candidatos.length === 0}>
          {r.cargando ? "Buscando…" : "Preguntar"}
        </button>
      </form>
      <div className="ejemplos">
        {EJEMPLOS.map((e) => <button key={e} className="chip" onClick={() => enviar(e)}>{e}</button>)}
      </div>
      {r.error && <p className="aviso" role="alert">{r.error}</p>}
      <div aria-live="polite">
        {r.respuesta && (
          <div className="respuesta">
            <Respuesta texto={r.respuesta} candidatos={candidatos} onCita={onCita} />
            <p className="modo">
              {r.modo?.generacion === "claude"
                ? "Respuesta redactada con IA a partir de los fragmentos citados. Verifica en el plan."
                : "Respuesta compuesta con frases textuales de los planes."}
            </p>
          </div>
        )}
      </div>
    </section>
  );
}
