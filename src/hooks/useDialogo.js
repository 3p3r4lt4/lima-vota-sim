import { useEffect, useRef } from "react";

// Abre un <dialog> modal al montarse (atrapa el foco y cierra con Esc de forma nativa),
// lo cierra al pulsar fuera y devuelve el foco al elemento que lo abrió.
export function useDialogo(onClose) {
  const ref = useRef(null);
  useEffect(() => {
    const d = ref.current;
    const previo = document.activeElement;
    if (!d.open) d.showModal();
    return () => { if (previo?.isConnected) previo.focus(); };
  }, []);
  const cerrar = () => ref.current?.close();
  const props = {
    ref,
    onClose,
    onClick: (e) => { if (e.target === e.currentTarget) cerrar(); },
  };
  return [props, cerrar];
}
