// Gráficos en SVG/HTML simple, sin librerías. Una sola serie por gráfico: color de acento para la marca,
// tokens de texto para las etiquetas y un tooltip nativo (<title>) por barra.

const fmt = (n) => Number(n ?? 0).toLocaleString("es-PE");

export function Columnas({ datos, titulo, etiquetaCada = 1, unidad = "sesiones" }) {
  const max = Math.max(1, ...datos.map((d) => d.n));
  const W = 600, H = 160, base = H - 22, alto = base - 14;
  const paso = W / Math.max(datos.length, 1);
  const ancho = Math.max(2, Math.min(28, paso - 2));
  return (
    <figure className="adm-grafico">
      <figcaption>{titulo}</figcaption>
      {datos.length === 0 ? <p className="adm-vacio">Sin datos en el rango.</p> : (
        <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`${titulo}. Máximo: ${fmt(max)} ${unidad}`}>
          <line x1="0" x2={W} y1={base} y2={base} className="adm-eje" />
          <text x="0" y="10" className="adm-eje-texto">{fmt(max)}</text>
          {datos.map((d, i) => {
            const h = d.n === 0 ? 0 : Math.max(2, (d.n / max) * alto);
            const x = i * paso + (paso - ancho) / 2;
            return (
              <g key={d.k}>
                <rect x={i * paso} y="0" width={paso} height={base} className="adm-hit"><title>{`${d.etiqueta ?? d.k}: ${fmt(d.n)} ${unidad}`}</title></rect>
                <rect x={x} y={base - h} width={ancho} height={h} rx="2" className="adm-barra" pointerEvents="none" />
                {i % etiquetaCada === 0 && (
                  <text x={i * paso + paso / 2} y={H - 6} textAnchor="middle" className="adm-eje-texto">{d.corto ?? d.k}</text>
                )}
              </g>
            );
          })}
        </svg>
      )}
    </figure>
  );
}

export function Ranking({ titulo, filas, nombre = (k) => k }) {
  const max = Math.max(1, ...filas.map((f) => f.n));
  return (
    <figure className="adm-grafico">
      <figcaption>{titulo}</figcaption>
      {filas.length === 0 ? <p className="adm-vacio">Sin datos.</p> : (
        <ol className="adm-ranking">
          {filas.map((f) => (
            <li key={f.k} title={`${nombre(f.k)}: ${fmt(f.n)}`}>
              <span className="adm-ranking-nombre">{nombre(f.k)}</span>
              <span className="adm-ranking-valor">{fmt(f.n)}</span>
              <span className="adm-ranking-pista"><span style={{ width: `${(f.n / max) * 100}%` }} /></span>
            </li>
          ))}
        </ol>
      )}
    </figure>
  );
}
