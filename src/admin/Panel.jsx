import { useCallback, useEffect, useMemo, useState } from "react";
import Login from "./Login.jsx";
import { Columnas, Ranking } from "./graficos.jsx";

const DISPOSITIVOS = { movil: "Móvil", tablet: "Tablet", escritorio: "Escritorio", desconocido: "Desconocido" };
const PRECISION = { pais: "País", departamento: "Departamento", provincia: "Provincia", distrito: "Distrito" };

const hoyLima = () => new Date(Date.now() - 5 * 3600_000).toISOString().slice(0, 10);
const sumarDias = (iso, n) => new Date(Date.parse(`${iso}T00:00:00Z`) + n * 86_400_000).toISOString().slice(0, 10);
const fmt = (n) => Number(n ?? 0).toLocaleString("es-PE");

function duracion(seg) {
  const s = Number(seg ?? 0);
  if (s < 60) return `${s} s`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m} min ${s % 60} s`;
  return `${Math.floor(m / 60)} h ${m % 60} min`;
}

const FILTROS_INICIALES = () => ({ desde: sumarDias(hoyLima(), -6), hasta: hoyLima(), departamento: "", ambito: "", dispositivo: "", bots: false, pagina: 1 });

function consulta(f, extra = {}) {
  const p = new URLSearchParams();
  for (const [k, v] of Object.entries({ ...f, ...extra })) {
    if (k === "bots") { if (v) p.set("bots", "1"); } else if (v !== "" && v !== null && v !== undefined) p.set(k, String(v));
  }
  return p.toString();
}

export default function Panel() {
  const [estado, setEstado] = useState("cargando");  // cargando | login | listo | error
  const [filtros, setFiltros] = useState(FILTROS_INICIALES);
  const [datos, setDatos] = useState(null);
  const [error, setError] = useState("");
  const [ambitos, setAmbitos] = useState(new Map());

  useEffect(() => {
    fetch("/data/ambitos.json").then((r) => r.json())
      .then((a) => setAmbitos(new Map(a.map((x) => [x.ubigeo, x.ambito])))).catch(() => {});
  }, []);

  const cargar = useCallback(async (f) => {
    setError("");
    try {
      const r = await fetch(`/api/admin/visitas?${consulta(f)}`, { credentials: "same-origin", cache: "no-store" });
      if (r.status === 401) { setEstado("login"); return; }
      const d = await r.json();
      if (!r.ok) { setError(d.error ?? "No se pudieron cargar los datos."); setEstado("error"); return; }
      setDatos(d);
      setEstado("listo");
    } catch {
      setError("Sin conexión con el servidor.");
      setEstado("error");
    }
  }, []);

  useEffect(() => { cargar(filtros); }, [filtros, cargar]);

  const cambiar = (k) => (e) => {
    const v = e.target.type === "checkbox" ? e.target.checked : e.target.value;
    setFiltros((f) => ({ ...f, [k]: v, pagina: 1 }));
  };

  async function salir() {
    await fetch("/api/admin/logout", { method: "POST", credentials: "same-origin" }).catch(() => {});
    setDatos(null);
    setEstado("login");
  }

  const nombreAmbito = useCallback((u) => (ambitos.get(u) ? `${ambitos.get(u)} (${u})` : u), [ambitos]);

  const porDia = useMemo(() => {
    if (!datos) return [];
    const m = new Map(datos.por_dia.map((d) => [d.k, d.n]));
    const out = [];
    for (let d = datos.filtros.desde; d <= datos.filtros.hasta; d = sumarDias(d, 1)) {
      out.push({ k: d, n: m.get(d) ?? 0, corto: d.slice(8) + "/" + d.slice(5, 7), etiqueta: d });
    }
    return out;
  }, [datos]);

  const porHora = useMemo(() => {
    if (!datos) return [];
    const m = new Map(datos.por_hora.map((d) => [d.k, d.n]));
    return Array.from({ length: 24 }, (_, h) => ({ k: h, n: m.get(h) ?? 0, corto: String(h), etiqueta: `${h}:00–${h}:59` }));
  }, [datos]);

  if (estado === "login") return <Login onEntrar={() => cargar(filtros)} />;

  const k = datos?.kpis;
  const ses = datos?.sesiones;
  const paginas = ses ? Math.max(1, Math.ceil(ses.total / ses.por_pagina)) : 1;

  return (
    <div className="adm">
      <header className="adm-cabecera">
        <h1>Visitas · Lima vota informado</h1>
        <div className="adm-acciones">
          <a className="adm-boton adm-boton-sec" href={`/api/admin/visitas?${consulta(filtros, { formato: "csv", pagina: "" })}`}>Exportar CSV</a>
          <button className="adm-boton adm-boton-sec" onClick={salir}>Salir</button>
        </div>
      </header>

      <p className="adm-nota" role="note">
        Ubicación estimada por IP; el distrito suele ser impreciso en redes móviles. Horas en America/Lima.
      </p>

      <form className="adm-filtros" onSubmit={(e) => e.preventDefault()}>
        <label>Desde<input type="date" value={filtros.desde} max={filtros.hasta} onChange={cambiar("desde")} /></label>
        <label>Hasta<input type="date" value={filtros.hasta} max={hoyLima()} onChange={cambiar("hasta")} /></label>
        <label>Departamento
          <select value={filtros.departamento} onChange={cambiar("departamento")}>
            <option value="">Todos</option>
            {(datos?.departamentos ?? []).map((d) => <option key={d} value={d}>{d}</option>)}
          </select>
        </label>
        <label>Ámbito consultado
          <select value={filtros.ambito} onChange={cambiar("ambito")}>
            <option value="">Todos</option>
            {[...ambitos].map(([u, n]) => <option key={u} value={u}>{n}</option>)}
          </select>
        </label>
        <label>Dispositivo
          <select value={filtros.dispositivo} onChange={cambiar("dispositivo")}>
            <option value="">Todos</option>
            {Object.entries(DISPOSITIVOS).map(([v, t]) => <option key={v} value={v}>{t}</option>)}
          </select>
        </label>
        <label className="adm-check"><input type="checkbox" checked={filtros.bots} onChange={cambiar("bots")} />Incluir bots</label>
      </form>

      {error && <p className="aviso" role="alert">{error}</p>}
      {estado === "cargando" && !datos && <p className="vacio">Cargando…</p>}

      {datos && (
        <>
          <section className="adm-kpis" aria-label="Indicadores">
            <div><span>Sesiones</span><strong>{fmt(k.sesiones)}</strong></div>
            <div><span>Visitantes únicos aprox.</span><strong>{fmt(k.unicos)}</strong></div>
            <div><span>Duración mediana</span><strong>{duracion(k.mediana_seg)}</strong></div>
            <div><span>Desde móvil</span><strong>{fmt(k.pct_movil)} %</strong></div>
          </section>

          <section className="adm-rejilla">
            <Columnas titulo="Sesiones por día" datos={porDia} etiquetaCada={Math.ceil(porDia.length / 10)} />
            <Columnas titulo="Sesiones por hora del día" datos={porHora} etiquetaCada={3} />
          </section>

          <section className="adm-rejilla adm-rejilla-3">
            <Ranking titulo="Departamentos" filas={datos.top.departamento} />
            <Ranking titulo="Provincias" filas={datos.top.provincia} />
            <Ranking titulo="Distritos" filas={datos.top.distrito} />
            <Ranking titulo="Ámbitos consultados" filas={datos.top.ambito} nombre={nombreAmbito} />
            <Ranking titulo="Dispositivo" filas={datos.dispositivo} nombre={(x) => DISPOSITIVOS[x] ?? x} />
            <Ranking titulo="Sistema operativo" filas={datos.so} />
            <Ranking titulo="Navegador" filas={datos.navegador} />
            <Ranking titulo="Precisión de la ubicación" filas={datos.precision} nombre={(x) => PRECISION[x] ?? x} />
          </section>

          <section className="adm-seccion" aria-labelledby="t-sesiones">
            <h2 id="t-sesiones">Sesiones ({fmt(ses.total)})</h2>
            <div className="adm-tabla-envoltura">
              <table className="adm-tabla">
                <thead>
                  <tr>
                    <th>Inicio</th><th>Fin / última señal</th><th>Duración</th><th>Dispositivo</th><th>SO</th><th>Navegador</th>
                    <th>Departamento</th><th>Provincia</th><th>Distrito</th><th>Ubigeo</th><th>Precisión</th><th>Ámbitos</th>
                  </tr>
                </thead>
                <tbody>
                  {ses.filas.map((s, i) => (
                    <tr key={i} className={s.es_bot ? "adm-bot" : ""}>
                      <td>{s.inicio}</td>
                      <td>{s.desconexion}{s.con_fin ? "" : " *"}</td>
                      <td>{duracion(s.duracion_seg)}</td>
                      <td>{DISPOSITIVOS[s.dispositivo_tipo] ?? "—"}{s.es_bot ? " (bot)" : ""}</td>
                      <td>{[s.so, s.so_version].filter(Boolean).join(" ")}</td>
                      <td>{[s.navegador, s.navegador_version].filter(Boolean).join(" ")}</td>
                      <td>{s.departamento ?? (s.pais && s.pais !== "PE" ? s.pais : "—")}</td>
                      <td>{s.provincia ?? "—"}</td>
                      <td>{s.distrito ?? "—"}</td>
                      <td>{s.ubigeo_geo ?? "—"}</td>
                      <td>{PRECISION[s.precision_geo] ?? "—"}</td>
                      <td>{(s.ambitos_visitados ?? []).map((u) => ambitos.get(u) ?? u).join(", ")}</td>
                    </tr>
                  ))}
                  {ses.filas.length === 0 && <tr><td colSpan={12} className="adm-vacio">Sin sesiones en el rango.</td></tr>}
                </tbody>
              </table>
            </div>
            <p className="adm-nota">* Sin evento de cierre: se muestra la última señal como hora de desconexión.</p>
            <nav className="adm-paginacion" aria-label="Paginación">
              <button className="adm-boton adm-boton-sec" disabled={ses.pagina <= 1}
                onClick={() => setFiltros((f) => ({ ...f, pagina: f.pagina - 1 }))}>Anterior</button>
              <span>Página {ses.pagina} de {paginas}</span>
              <button className="adm-boton adm-boton-sec" disabled={ses.pagina >= paginas}
                onClick={() => setFiltros((f) => ({ ...f, pagina: f.pagina + 1 }))}>Siguiente</button>
            </nav>
          </section>
        </>
      )}
    </div>
  );
}
