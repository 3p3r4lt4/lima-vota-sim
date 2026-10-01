import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { fileURLToPath } from "node:url";

const entrada = (f) => fileURLToPath(new URL(f, import.meta.url));

// Entradas separadas: el panel /admin no agrega peso al bundle público.
export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      input: { main: entrada("index.html"), admin: entrada("admin.html") },
    },
  },
});
