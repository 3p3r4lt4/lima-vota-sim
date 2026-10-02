import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";
import { analiticaHabilitada } from "./netlify/lib/visita.mjs";

const entrada = (f) => fileURLToPath(new URL(f, import.meta.url));

// Entradas separadas: el panel /admin no agrega peso al bundle público.
export default defineConfig({
  plugins: [react()],
  // ANALYTICS_ENABLED=false en el entorno de build (Netlify o local) apaga la analítica también en el cliente
  define: { __ANALITICA__: JSON.stringify(analiticaHabilitada(process.env.ANALYTICS_ENABLED)) },
  build: {
    rollupOptions: {
      input: { main: entrada("index.html"), admin: entrada("admin.html"), privacidad: entrada("privacidad.html") },
    },
  },
});
