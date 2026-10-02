import { useState } from "react";

export default function Login({ onEntrar }) {
  const [usuario, setUsuario] = useState("");
  const [password, setPassword] = useState("");
  const [codigo, setCodigo] = useState("");
  const [error, setError] = useState("");
  const [enviando, setEnviando] = useState(false);

  async function enviar(e) {
    e.preventDefault();
    setEnviando(true);
    setError("");
    try {
      const r = await fetch("/api/admin/login", {
        method: "POST",
        credentials: "same-origin",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ usuario, password, codigo }),
      });
      if (r.ok) { setPassword(""); setCodigo(""); onEntrar(); return; }
      setError("No se pudo iniciar sesión. Revisa los datos o intenta más tarde.");
    } catch {
      setError("Sin conexión. Intenta de nuevo.");
    } finally {
      setEnviando(false);
    }
  }

  return (
    <main className="adm-login">
      <form className="adm-tarjeta" onSubmit={enviar}>
        <h1>Panel de visitas</h1>
        <label>
          Usuario
          <input autoComplete="username" maxLength={64} autoCapitalize="none" spellCheck={false}
            value={usuario} onChange={(e) => setUsuario(e.target.value)} />
        </label>
        <label>
          Contraseña
          <input type="password" autoComplete="current-password" required maxLength={256}
            value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        <label>
          Código de la app autenticadora
          <input inputMode="numeric" autoComplete="one-time-code" pattern="\d{6}" maxLength={6} required
            value={codigo} onChange={(e) => setCodigo(e.target.value.replace(/\D/g, ""))} />
        </label>
        {error && <p className="aviso" role="alert">{error}</p>}
        <button className="adm-boton" disabled={enviando}>{enviando ? "Verificando…" : "Entrar"}</button>
      </form>
    </main>
  );
}
