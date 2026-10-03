import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";
import { analiticaHabilitada } from "./netlify/lib/visita.mjs";

const entrada = (f) => fileURLToPath(new URL(f, import.meta.url));

// LinkedIn y demás redes exigen URLs absolutas en og:url y og:image. Netlify define URL (dominio principal) al compilar.
const urlSitio = (process.env.URL || "").replace(/\/$/, "");
const metaSitio = { name: "meta-sitio", transformIndexHtml: (html) => html.replaceAll("__URL_SITIO__", urlSitio) };

// Entradas separadas: el panel /admin no agrega peso al bundle público.
export default defineConfig({
  plugins: [react(), metaSitio],
  // ANALYTICS_ENABLED=false en el entorno de build (Netlify o local) apaga la analítica también en el cliente
  define: { __ANALITICA__: JSON.stringify(analiticaHabilitada(process.env.ANALYTICS_ENABLED)) },
  build: {
    rollupOptions: {
      input: { main: entrada("index.html"), admin: entrada("admin.html"), privacidad: entrada("privacidad.html") },
    },
  },
});
