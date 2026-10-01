// Íconos SVG inline, decorativos (aria-hidden); el texto accesible va en el control
const Svg = ({ children, size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
    strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">{children}</svg>
);

export const IconoUbicacion = (p) => <Svg {...p}><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z" /><circle cx="12" cy="9.5" r="2.5" /></Svg>;
export const IconoChevron = (p) => <Svg {...p}><path d="m6 9 6 6 6-6" /></Svg>;
export const IconoCerrar = (p) => <Svg {...p}><path d="M18 6 6 18M6 6l12 12" /></Svg>;
export const IconoBuscar = (p) => <Svg {...p}><circle cx="11" cy="11" r="7" /><path d="m20 20-3.5-3.5" /></Svg>;
export const IconoAzar = (p) => <Svg {...p}><path d="M16 3h5v5M4 20 21 3M21 16v5h-5M15 15l6 6M4 4l5 5" /></Svg>;
export const IconoDocumento = (p) => <Svg {...p}><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" /><path d="M14 3v6h6M8 13h8M8 17h5" /></Svg>;
export const IconoColumnas = (p) => <Svg {...p}><rect x="3" y="4" width="18" height="16" rx="2" /><path d="M9 4v16M15 4v16" /></Svg>;
export const IconoMarca = (p) => (
  <svg width="28" height="28" viewBox="0 0 32 32" aria-hidden="true" focusable="false">
    <rect x="3" y="3" width="26" height="26" rx="6" fill="var(--accent)" />
    <path d="M10 10l12 12M22 10L10 22" stroke="var(--accent-contrast)" strokeWidth="3.5" strokeLinecap="round" />
  </svg>
);
