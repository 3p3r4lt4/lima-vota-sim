import { useEffect, useMemo, useState } from "react";
import Cedula from "./components/Cedula.jsx";
import LadoALado from "./components/LadoALado.jsx";
import Fichas from "./components/Fichas.jsx";
import Preguntar from "./components/Preguntar.jsx";
import VisorFuente from "./components/VisorFuente.jsx";
import GuiaVoto from "./components/GuiaVoto.jsx";
import ListaDistrital from "./components/ListaDistrital.jsx";

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
  const [ubigeo, setUbigeo] = useState(params.get("ambito") ?? "1501");
  const [vista, setVista] = useState(VISTAS[params.get("vista")] ? params.get("vista") : "comparar");
  const [datos, setDatos] = useState(null);
  const [planes, setPlanes] = useState(null);
  const [marcados, setMarcados] = useState(new Set());
  const [visor, setVisor] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/data/ambitos.json").then((r) => r.json()).then((a) => {
      setAmbitos(a);
      if (!a.some((x) => x.ubigeo === ubigeo)) setUbigeo("1501");
    }).catch(() => setError("No se pudo cargar la lista de distritos. Revisa tu conexión y recarga la página."));
  }, []);

  useEffect(() => {
    if (!ubigeo) return;
    setDatos(null); setPlanes(null); setError(""); setVisor(null);
    fetch(`/data/comparaciones/${ubigeo}.json`)
      .then((r) => { if (!r.ok) throw new Error(); return r.json(); })
      .then((d) => { setDatos(d); setMarcados(new Set(d.candidatos.map((c) => c.id))); })
      .catch(() => setError("No hay datos publicados para este distrito."));
    history.replaceState(null, "", `?ambito=${ubigeo}&vista=${vista}`);
  }, [ubigeo]);

  useEffect(() => { history.replaceState(null, "", `?ambito=${ubigeo}&vista=${vista}`); }, [vista]);

  const candidatos = useMemo(() => (datos ? barajar(datos.candidatos) : []), [datos]);
  const visibles = candidatos.filter((c) => marcados.has(c.id));

  async function abrirFuente(candidatoId, seccion) {
    let p = planes;
    if (!p) {
      p = await fetch(`/data/planes/${ubigeo}.json`).then((r) => r.json()).catch(() => null);
      setPlanes(p);
    }
    const candidato = p?.candidatos.find((c) => c.id === candidatoId);
    if (candidato) setVisor({ candidato, seccion, fuentes: p.fuentes });
    else if (p) setError("No se encontró la fuente de esa cita.");
  }

  return (
    <div className="pagina">
      <header className="cabecera">
        <h1 className="titular">
          Voto en{" "}
          <label className="selector">
            <span className="sr">Elige Lima Metropolitana o tu distrito</span>
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
          Compara lo que proponen quienes postulan a la alcaldía, tema por tema y con la fuente de cada propuesta.
          Elecciones Regionales y Municipales, domingo 4 de octubre de 2026.
        </p>
      </header>

      {error && <p className="aviso" role="alert">{error}</p>}
      {!datos && !error && <p className="cargando" aria-live="polite">Cargando…</p>}

      {datos && (
        <main>
          <p className="franja" role="note">
            {datos.nota_fuente} Datos al {datos.corte}.
          </p>

          {datos.con_propuestas ? (
            <>
              <section aria-labelledby="t-cand">
                <h2 id="t-cand" className="seccion">
                  {candidatos.length} listas a la alcaldía de {datos.ambito}
                </h2>
                <p className="nota">Marca o desmarca para elegir a quiénes comparar. El orden es aleatorio en cada visita.
                  Consejo: pulsa «Desmarcar todas» y marca de 2 a 4 para leer la tabla con comodidad.</p>
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
                <LadoALado datos={datos} candidatos={visibles} onCita={abrirFuente} />
              ) : (
                <Fichas datos={datos} candidatos={visibles} onCita={abrirFuente} />
              )}

              <Preguntar ubigeo={ubigeo} ambito={datos.ambito} candidatos={visibles}
                onCita={abrirFuente} onCambiarAmbito={setUbigeo} tipoFuente={datos.tipo_fuente} />
            </>
          ) : (
            <ListaDistrital datos={datos} candidatos={candidatos} onVerLima={() => setUbigeo("1501")} />
          )}

          <GuiaVoto />
        </main>
      )}

      {visor && <VisorFuente {...visor} onClose={() => setVisor(null)} />}

      <footer className="pie">
        <p>
          Proyecto personal, independiente y sin afiliación política. No recomienda candidaturas ni asigna puntajes.
          Las propuestas están redactadas con palabras propias a partir de las fuentes citadas y pueden contener errores:
          verifica siempre en la fuente y en los planes de gobierno oficiales de{" "}
          <a href="https://votoinformado.jne.gob.pe" target="_blank" rel="noreferrer">Voto Informado del JNE</a>.
        </p>
      </footer>
    </div>
  );
}
