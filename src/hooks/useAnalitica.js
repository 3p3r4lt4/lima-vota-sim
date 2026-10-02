import { useEffect } from "react";
import { iniciarAnalitica, registrarAmbito, registrarVista, detenerAnalitica } from "../lib/analitica.js";

// Registra la visita al montar, cada cambio de ámbito y cada cambio de vista. Corre después del render y nunca lanza.
export function useAnalitica(ubigeo, vista) {
  useEffect(() => {
    iniciarAnalitica(ubigeo, vista);
    return detenerAnalitica;
  }, []);
  useEffect(() => { registrarAmbito(ubigeo); }, [ubigeo]);
  useEffect(() => { registrarVista(vista); }, [vista]);
}
