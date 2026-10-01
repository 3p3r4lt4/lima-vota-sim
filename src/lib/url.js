// Estado compartible en la URL: ?ambito=1501&vista=fichas|comparar&sel=12,45
// Se aceptan los enlaces antiguos (?vista=comparar sin sel muestra las tarjetas).
export function leerUrl() {
  const p = new URLSearchParams(location.search);
  const sel = (p.get("sel") ?? "").split(",").map(Number).filter((n) => Number.isInteger(n) && n > 0);
  return {
    ambito: p.get("ambito") ?? "1501",
    vista: p.get("vista") === "comparar" ? "comparar" : "fichas",
    sel: [...new Set(sel)].slice(0, 3),
  };
}

export function escribirUrl({ ambito, vista, sel }) {
  const p = new URLSearchParams({ ambito, vista });
  if (sel.length) p.set("sel", sel.join(","));
  history.replaceState(null, "", `?${p.toString().replace(/%2C/g, ",")}`);
}
