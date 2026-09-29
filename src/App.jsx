import { useEffect, useMemo, useState } from "react";
import Cedula from "./components/Cedula.jsx";
import LadoALado from "./components/LadoALado.jsx";
import Fichas from "./components/Fichas.jsx";
import Preguntar from "./components/Preguntar.jsx";
import VisorPlan from "./components/VisorPlan.jsx";
import GuiaVoto from "./components/GuiaVoto.jsx";

const GRUPOS = { provincial: "Lima Metropolitana", distrital: "Distritos de Lima" };
const VISTAS = { comparar: "Comparar lado a lado", fichas: "Ficha de cada candidatura" };

// Orden aleatorio estable durante la sesión: ninguna candidatura aparece siempre primero
const semilla = Math.floor(Math.random() * 2 ** 31);
function barajar(lista) {
  let s = semilla;
  const a = [...lista];
  for (let i = a.length - 1; i > 0; i--) {
    s = (s * 1103515245 + 12345) % 2 ** 31;
    const j = s % (i + 1);
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

const params = new URLSearchParams(location.search);

export default function App() {
  const [ambitos, setAmbitos] = useState([]);
  const [ubigeo, setUbigeo] = useState(params.get("ambito") ?? "");
  const [vista, setVista] = useState(VISTAS[params.get("vista")] ? params.get("vista") : "comparar");
  const [datos, setDatos] = useState(null);
  const [planes, setPlanes] = useState(null);
  const [marcados, setMarcados] = useState(new Set());
  const [visor, setVisor] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/data/ambitos.json").then((r) => r.json()).then((a) => {
      setAmbitos(a);
      if (!a.some((x) => x.ubigeo === ubigeo)) setUbigeo(a[0]?.ubigeo ?? "");
    }).catch(() => setError("No se pudo cargar la lista de distritos. Revisa tu conexión y recarga la página."));
  }, []);

  useEffect(() => {
    if (!ubigeo) return;
    setDatos(null); setPlanes(null); setError("");
    fetch(`/data/comparaciones/${ubigeo}.json`)
      .then((r) => { if (!r.ok) throw new Error(); return r.json(); })
      .then((d) => { setDatos(d); setMarcados(new Set(d.candidatos.map((c) => c.id))); })
      .catch(() => setError("Este distrito todavía no tiene comparación publicada."));
  }, [ubigeo]);

  useEffect(() => {
    if (ubigeo) history.replaceState(null, "", `?ambito=${ubigeo}&vista=${vista}`);
  }, [ubigeo, vista]);

  const candidatos = useMemo(() => (datos ? barajar(datos.candidatos) : []), [datos]);
  const visibles = candidatos.filter((c) => marcados.has(c.id));

  async function abrirPlan(candidatoId, pagina) {
    let p = planes;
    if (!p) {
      p = await fetch(`/data/planes/${ubigeo}.json`).then((r) => r.json()).catch(() => null);
      setPlanes(p);
    }
    if (p) setVisor({ candidato: p.candidatos.find((c) => c.id === candidatoId), pagina });
  }

  return (
    <div className="pagina">
      {datos?.simulado && (
        <p className="franja" role="note">
          Demostración con datos simulados: las candidaturas y propuestas son ficticias y no corresponden a personas ni organizaciones reales.
        </p>
      )}

      <header className="cabecera">
        <h1 className="titular">
          Voto en{" "}
          <label className="selector">
            <span className="sr">Elige tu distrito</span>
            <select value={ubigeo} onChange={(e) => setUbigeo(e.target.value)}>
              {Object.entries(GRUPOS).map(([nivel, etiqueta]) => (
                <optgroup key={nivel} label={etiqueta}>
                  {ambitos.filter((a) => a.nivel === nivel).map((a) => (
                    <option key={a.ubigeo} value={a.ubigeo}>{a.ambito}</option>
                  ))}
                </optgroup>
              ))}
            </select>
          </label>
          <br />¿qué propone cada candidatura?
        </h1>
        <p className="bajada">
          Compara las propuestas de los planes de gobierno de tu distrito, tema por tema, con la página exacta donde
          aparece cada una. Elecciones Regionales y Municipales, domingo 4 de octubre de 2026.
        </p>
      </header>

      {error && <p className="aviso" role="alert">{error}</p>}
      {!datos && !error && <p className="cargando" aria-live="polite">Cargando propuestas…</p>}

      {datos && (
        <main>
          <section aria-labelledby="t-cand">
            <h2 id="t-cand" className="seccion">
              {candidatos.length} candidaturas a la {datos.cargo.toLowerCase()}
            </h2>
            <p className="nota">Marca o desmarca para elegir a quiénes comparar. El orden es aleatorio en cada visita.</p>
            <Cedula candidatos={candidatos} marcados={marcados} setMarcados={setMarcados} />
          </section>

          <div className="vistas" role="tablist" aria-label="Forma de ver las propuestas">
            {Object.entries(VISTAS).map(([k, v]) => (
              <button key={k} role="tab" aria-selected={vista === k} onClick={() => setVista(k)}>{v}</button>
            ))}
          </div>

          {visibles.length === 0 ? (
            <p className="vacio">Marca al menos una candidatura para ver sus propuestas.</p>
          ) : vista === "comparar" ? (
            <LadoALado temas={datos.temas} candidatos={visibles} onCita={abrirPlan} />
          ) : (
            <Fichas temas={datos.temas} candidatos={visibles} onCita={abrirPlan} />
          )}

          <Preguntar ubigeo={ubigeo} ambito={datos.ambito} candidatos={visibles} onCita={abrirPlan} />
          <GuiaVoto />
        </main>
      )}

      {visor && <VisorPlan {...visor} simulado={datos?.simulado} onClose={() => setVisor(null)}
        onPagina={(pagina) => setVisor({ ...visor, pagina })} />}

      <footer className="pie">
        <p>
          Proyecto personal, independiente y sin afiliación política. No recomienda candidaturas ni asigna puntajes.
          Los resúmenes pueden contener errores: verifica siempre en la página citada del plan de gobierno oficial.
        </p>
      </footer>
    </div>
  );
}
