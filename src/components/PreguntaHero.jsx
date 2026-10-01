import { useState } from "react";
import Respuesta from "../lib/Respuesta.jsx";
import { IconoAzar } from "./Iconos.jsx";

// soloLima: preguntas que solo tienen sentido para Lima Metropolitana
const BANCO = [
  { q: "¿Quiénes proponen armar al serenazgo?" }, { q: "¿Qué proponen para el Metropolitano, el metro o el tren?", soloLima: true },
  { q: "¿Qué harán con el agua en los cerros?" }, { q: "¿Quiénes hablan de cámaras con inteligencia artificial?" },
  { q: "¿Qué proponen sobre el comercio ambulatorio?" }, { q: "¿Qué proponen para la vivienda y la titulación?" },
  { q: "¿Quiénes proponen una Policía Municipal?" }, { q: "¿Qué dicen sobre hospitales y salud?" },
  { q: "¿Qué proponen contra la extorsión y el sicariato?" }, { q: "¿Qué harán con la ATU?", soloLima: true },
  { q: "¿Qué proponen para los jóvenes?" }, { q: "¿Qué proponen sobre los ríos y el ambiente?" }, { q: "¿Qué harán con el agua para regar los parques?" },
  { q: "¿Qué proponen para los adultos mayores?" }, { q: "¿Qué proponen sobre las mascotas?" }, { q: "¿Quiénes proponen usar drones?" },
  { q: "¿Quiénes proponen recompensas por delincuentes?" }, { q: "¿Qué harán ante un sismo o El Niño?" },
];
const SIN_RESULTADOS = /^Ninguna de las candidaturas/;

export default function PreguntaHero({ ubigeo, datos, candidatos, onCita, onCambiarAmbito }) {
  const banco = BANCO.filter((b) => !b.soloLima || datos.nivel === "provincial").map((b) => b.q);
  const alAzar = (n) => [...banco].sort(() => Math.random() - 0.5).slice(0, n);
  const [pregunta, setPregunta] = useState("");
  const [ejemplos, setEjemplos] = useState(() => alAzar(3));
  const [r, setR] = useState({ estado: "inicial", data: null, error: "" });
  const [validacion, setValidacion] = useState("");

  async function enviar(q = pregunta) {
    q = q.trim();
    if (q.length < 5) { setValidacion("Escribe una pregunta de al menos 5 letras."); return; }
    setValidacion("");
    setPregunta(q);
    setR({ estado: "cargando", data: null, error: "" });
    try {
      // Se busca en todas las candidaturas del ámbito: la selección para comparar no filtra la búsqueda
      const res = await fetch("/api/preguntar", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ pregunta: q, ubigeo, candidatoIds: candidatos.map((c) => c.id) }),
      });
      if (res.status === 429) throw new Error("Hiciste muchas preguntas seguidas. Espera un minuto y vuelve a intentar.");
      const d = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(d.error ?? "No se pudo responder. Intenta de nuevo.");
      setR({ estado: SIN_RESULTADOS.test(d.respuesta ?? "") ? "vacio" : "listo", data: d, error: "" });
    } catch (e) {
      const msg = e instanceof TypeError ? "No hay conexión con el servicio de preguntas. Revisa tu internet e intenta de nuevo." : e.message;
      setR({ estado: "error", data: null, error: msg });
    }
  }

  const d = r.data;
  const fuente = datos.tipo_fuente === "plan" ? "los planes de gobierno" : "las propuestas del debate";
  return (
    <section className="hero" aria-labelledby="t-hero">
      <h1 id="t-hero" className="hero-titulo">¿Qué proponen para {datos.ambito}?</h1>
      <form className="hero-form" onSubmit={(e) => { e.preventDefault(); enviar(); }} noValidate>
        <label htmlFor="q" className="hero-label">Pregunta sobre un tema que te importe</label>
        <div className="hero-campo">
          <input id="q" type="text" enterKeyHint="search" value={pregunta} maxLength={300} autoComplete="off"
            placeholder="Ej.: ¿Qué harán con el serenazgo?" aria-describedby="q-ayuda q-error"
            aria-invalid={validacion ? "true" : undefined}
            onChange={(e) => { setPregunta(e.target.value); if (validacion) setValidacion(""); }} />
          <button type="submit" className="btn btn-primario" disabled={r.estado === "cargando"}>
            {r.estado === "cargando" ? "Buscando…" : "Preguntar"}
          </button>
        </div>
        <p id="q-error" className="hero-validacion">{validacion}</p>
        <p id="q-ayuda" className="hero-ayuda">Buscamos en {fuente} de las {candidatos.length} candidaturas.</p>
      </form>

      <div className="sugeridas" role="group" aria-label="Preguntas sugeridas">
        {ejemplos.map((e) => (
          <button key={e} type="button" className="chip" onClick={() => enviar(e)}>{e}</button>
        ))}
        <button type="button" className="chip chip-azar" onClick={() => { const [q] = alAzar(1); setEjemplos(alAzar(3)); enviar(q); }}>
          <IconoAzar size={16} /> Pregunta al azar
        </button>
      </div>

      <div className="respuesta-zona" aria-live="polite" aria-busy={r.estado === "cargando"}>
        {r.estado === "cargando" && (
          <div className="skeleton" aria-label="Buscando respuesta">
            <span /><span /><span />
          </div>
        )}
        {r.estado === "error" && (
          <div className="estado estado-error" role="alert">
            <p>{r.error}</p>
            <button type="button" className="btn btn-sec" onClick={() => enviar()}>Reintentar</button>
          </div>
        )}
        {r.estado === "vacio" && (
          <div className="estado">
            <p><strong>No encontramos propuestas sobre eso.</strong></p>
            <p>Prueba con otras palabras (serenazgo, cámaras, agua, vivienda, comercio) o explora por tema más abajo.</p>
          </div>
        )}
        {r.estado === "listo" && d && (
          <div className="respuesta">
            <p className="respuesta-pregunta">{pregunta}</p>
            <Respuesta texto={d.respuesta} candidatos={candidatos} onCita={onCita} />
            {d.tipo === "otro_ambito" && (
              <button type="button" className="btn btn-sec" onClick={() => onCambiarAmbito(d.ubigeo)}>Ir a {d.ambito}</button>
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
