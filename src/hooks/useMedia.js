import { useEffect, useState } from "react";

export function useMedia(consulta) {
  const [coincide, setCoincide] = useState(() => matchMedia(consulta).matches);
  useEffect(() => {
    const m = matchMedia(consulta);
    const f = () => setCoincide(m.matches);
    f();
    m.addEventListener("change", f);
    return () => m.removeEventListener("change", f);
  }, [consulta]);
  return coincide;
}
