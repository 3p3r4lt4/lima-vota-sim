import { useEffect } from "react";
import { iniciarAnalitica, registrarAmbito, detenerAnalitica } from "../lib/analitica.js";

// Registra la visita al montar y cada cambio de ámbito. Corre después del render y nunca lanza.
export function useAnalitica(ubigeo) {
  useEffect(() => {
    iniciarAnalitica(ubigeo);
    return detenerAnalitica;
  }, []);
  useEffect(() => { registrarAmbito(ubigeo); }, [ubigeo]);
}
