import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { barajar } from "../lib/barajar.js";

// Carga la lista de ámbitos y la comparación del ámbito elegido.
// Los planes completos (planes/{ubigeo}.json, hasta ~740 KB) solo se piden al abrir una fuente.
export function useAmbito(ubigeoInicial) {
  const [ambitos, setAmbitos] = useState([]);
  const [ubigeo, setUbigeo] = useState(ubigeoInicial);
  const [datos, setDatos] = useState(null);
  const [error, setError] = useState("");
  const planes = useRef(new Map());

  useEffect(() => {
    fetch("/data/ambitos.json")
      .then((r) => { if (!r.ok) throw new Error(); return r.json(); })
      .then((a) => {
        setAmbitos(a);
        if (!a.some((x) => x.ubigeo === ubigeoInicial)) setUbigeo("1501");
      })
      .catch(() => setError("No se pudo cargar la lista de distritos. Revisa tu conexión y recarga la página."));
  }, []);

  useEffect(() => {
    let vigente = true;
    setDatos(null);
    setError("");
    fetch(`/data/comparaciones/${ubigeo}.json`)
      .then((r) => { if (!r.ok) throw new Error(); return r.json(); })
      .then((d) => { if (vigente) setDatos(d); })
      .catch(() => { if (vigente) setError("No hay datos publicados para este distrito."); });
    return () => { vigente = false; };
  }, [ubigeo]);

  const candidatos = useMemo(() => (datos ? barajar(datos.candidatos) : []), [datos]);

  const cargarPlanes = useCallback(() => {
    const cache = planes.current;
    if (!cache.has(ubigeo)) {
      cache.set(ubigeo, fetch(`/data/planes/${ubigeo}.json`)
        .then((r) => { if (!r.ok) throw new Error(); return r.json(); })
        .catch((e) => { cache.delete(ubigeo); throw e; }));
    }
    return cache.get(ubigeo);
  }, [ubigeo]);

  const ambito = ambitos.find((a) => a.ubigeo === ubigeo);
  return { ambitos, ambito, ubigeo, setUbigeo, datos, candidatos, error, cargarPlanes };
}
