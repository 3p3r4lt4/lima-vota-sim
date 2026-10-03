const CORREO = "lowcodeperu24@gmail.com";

// Enlace mailto con asunto y cuerpo prellenados para que el reporte llegue con su contexto.
export function enlaceReporte({ ambito, candidato } = {}) {
  const donde = [ambito, candidato && `${candidato.nombre} (${candidato.organizacion})`].filter(Boolean).join(" · ");
  const asunto = `Error en Lima vota informado${donde ? `: ${donde}` : ""}`;
  const cuerpo = `${donde ? `Ámbito o candidatura: ${donde}\n\n` : ""}Qué dice la web:\n\n\nQué debería decir (y dónde lo viste, si puedes):\n\n`;
  return `mailto:${CORREO}?subject=${encodeURIComponent(asunto)}&body=${encodeURIComponent(cuerpo)}`;
}
