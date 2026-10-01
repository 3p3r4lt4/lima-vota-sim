import type { Config } from "@netlify/functions";
import { cookieBorrar, origenValido, CABECERAS } from "../lib/auth-admin.mjs";

// Borra la cookie. Para invalidar todas las sesiones abiertas, rota ADMIN_SESSION_SECRET.
export default async (req: Request) => {
  if (req.method !== "POST" || !origenValido(req)) return new Response(null, { status: 403, headers: CABECERAS });
  return new Response(null, { status: 204, headers: { ...CABECERAS, "set-cookie": cookieBorrar() } });
};

export const config: Config = {
  path: "/api/admin/logout",
  method: "POST",
};
