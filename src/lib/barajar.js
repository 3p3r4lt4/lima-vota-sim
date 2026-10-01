// Orden aleatorio estable durante la sesión: ninguna candidatura aparece siempre primero
const semilla = Math.floor(Math.random() * 2 ** 31);

export function barajar(lista) {
  let s = semilla;
  const a = [...lista];
  for (let i = a.length - 1; i > 0; i--) {
    s = (s * 1103515245 + 12345) % 2 ** 31;
    const j = s % (i + 1);
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
