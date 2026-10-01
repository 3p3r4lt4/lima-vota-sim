import { lazy, Suspense, useCallback, useEffect, useRef, useState } from "react";
import TopBar from "./components/TopBar.jsx";
import SelectorAmbito from "./components/SelectorAmbito.jsx";
import PreguntaHero from "./components/PreguntaHero.jsx";
import AvisoSinPropuestas from "./components/AvisoSinPropuestas.jsx";
import ListaCandidaturas from "./components/ListaCandidaturas.jsx";
import ChipsTema from "./components/ChipsTema.jsx";
import TarjetaCandidato from "./components/TarjetaCandidato.jsx";
import BarraComparar from "./components/BarraComparar.jsx";
import Acordeon from "./components/Acordeon.jsx";
import GuiaVoto from "./components/GuiaVoto.jsx";
import Pie from "./components/Pie.jsx";
import { useAmbito } from "./hooks/useAmbito.js";
import { escribirUrl, leerUrl } from "./lib/url.js";

const DetalleCandidato = lazy(() => import("./components/DetalleCandidato.jsx"));
const VisorFuente = lazy(() => import("./components/VisorFuente.jsx"));
const VistaComparar = lazy(() => import("./components/VistaComparar.jsx"));

const inicial = leerUrl();
const MAX_COMPARAR = 3;

export default function App() {
  const { ambitos, ambito, ubigeo, setUbigeo, datos, candidatos, error, cargarPlanes } = useAmbito(inicial.ambito);
  const [selectorAbierto, setSelectorAbierto] = useState(false);
  const [tema, setTema] = useState("");
  const [sel, setSel] = useState([]);
  const [comparando, setComparando] = useState(false);
  const [detalleId, setDetalleId] = useState(null);
  const [visor, setVisor] = useState(null);
  const [aviso, setAviso] = useState("");

  useEffect(() => { setTema(""); setSel([]); setComparando(false); setVisor(null); setDetalleId(null); setAviso(""); }, [ubigeo]);

  // Enlaces compartidos: ?vista=comparar&sel=… restaura la comparación (solo ids de este ámbito)
  const restaurado = useRef(false);
  useEffect(() => {
    if (!datos || restaurado.current) return;
    restaurado.current = true;
    if (datos.ubigeo !== inicial.ambito) return;
    const validos = inicial.sel.filter((id) => datos.candidatos.some((c) => c.id === id));
    setSel(validos);
    if (inicial.vista === "comparar" && validos.length >= 2) setComparando(true);
  }, [datos]);

  useEffect(() => {
    escribirUrl({ ambito: ubigeo, vista: comparando ? "comparar" : "fichas", sel });
  }, [ubigeo, sel, comparando]);

  const alternarComparar = useCallback((id) => {
    setSel((s) => (s.includes(id) ? s.filter((x) => x !== id) : s.length >= MAX_COMPARAR ? s : [...s, id]));
  }, []);

  const abrirFuente = useCallback(async (candidatoId, seccion) => {
    try {
      const p = await cargarPlanes();
      const candidato = p.candidatos.find((c) => c.id === candidatoId);
      if (candidato) { setAviso(""); setVisor({ candidato, seccion, fuentes: p.fuentes }); }
      else setAviso("No se encontró la fuente de esa cita.");
    } catch {
      setAviso("No se pudo abrir la fuente. Revisa tu conexión e intenta de nuevo.");
    }
  }, [cargarPlanes]);

  const detalle = candidatos.find((c) => c.id === detalleId);
  const elegidos = candidatos.filter((c) => sel.includes(c.id));
  const abiertoComparar = comparando && elegidos.length >= 2;
  // Con un panel abierto, el aviso se muestra dentro del panel (la página queda detrás del modal)
  const avisoPagina = error || (detalle || abiertoComparar ? "" : aviso);

  return (
    <>
      <TopBar ambito={ambito} abierto={selectorAbierto} onElegir={() => setSelectorAbierto(true)} />
      <main className={`contenedor${elegidos.length ? " con-barra" : ""}`}>
        {avisoPagina && <p className="aviso" role="alert">{avisoPagina}</p>}
        {!datos && !error && <p className="vacio cargando-pagina" aria-live="polite">Cargando…</p>}
        {datos && (datos.con_propuestas ? (
          <>
            <PreguntaHero key={ubigeo} ubigeo={ubigeo} datos={datos} candidatos={candidatos}
              onCita={abrirFuente} onCambiarAmbito={setUbigeo} />
            <section className="seccion" aria-labelledby="t-cand">
              <h2 id="t-cand" className="seccion-titulo">{candidatos.length} candidaturas a la alcaldía</h2>
              <p className="seccion-nota">Orden aleatorio en cada visita. Marca «Comparar» en 2 o 3 para verlas lado a lado.</p>
              <ChipsTema datos={datos} tema={tema} onTema={setTema} />
              <div className="grid-tarjetas">
                {candidatos.map((c) => (
                  <TarjetaCandidato key={c.id} c={c} datos={datos} tema={tema} elegido={sel.includes(c.id)}
                    onComparar={alternarComparar} onVerTodo={setDetalleId} onCita={abrirFuente} />
                ))}
              </div>
            </section>
          </>
        ) : (
          <>
            <AvisoSinPropuestas ambito={datos.ambito} onVerLima={() => setUbigeo("1501")} />
            <ListaCandidaturas datos={datos} candidatos={candidatos} />
          </>
        ))}
        <Acordeon titulo="Antes de decidir tu voto"><GuiaVoto /></Acordeon>
        <Pie datos={datos} />
      </main>
      {selectorAbierto && (
        <SelectorAmbito ambitos={ambitos} actual={ubigeo} onElegir={setUbigeo} onClose={() => setSelectorAbierto(false)} />
      )}
      {datos?.con_propuestas && (
        <BarraComparar elegidos={elegidos} max={MAX_COMPARAR} onAbrir={() => setComparando(true)}
          onQuitar={alternarComparar} onLimpiar={() => setSel([])} />
      )}
      <Suspense fallback={null}>
        {detalle && (
          <DetalleCandidato key={detalle.id} c={detalle} datos={datos} tema={tema} elegido={sel.includes(detalle.id)}
            puedeAgregar={sel.length < MAX_COMPARAR} onComparar={alternarComparar} onCita={abrirFuente}
            aviso={aviso} onClose={() => { setDetalleId(null); setAviso(""); }} />
        )}
        {abiertoComparar && (
          <VistaComparar candidatos={elegidos} datos={datos} onCita={abrirFuente} aviso={aviso}
            onClose={() => { setComparando(false); setAviso(""); }} />
        )}
        {visor && <VisorFuente {...visor} onClose={() => setVisor(null)} />}
      </Suspense>
    </>
  );
}
