"""Verifica un módulo de scripts/distritos/ antes de registrarlo en datos_reales.py.

Uso: python scripts/verificar_distrito.py scripts/distritos/150130_san_borja.py [--muestra 3]

Comprueba, para cada plan: que exista el texto extraído, que cada ancla aparezca en la página indicada (misma
normalización que datos_reales.py), que haya entre 8 y 11 propuestas con temas válidos, que los textos sean breves
(≤ 30 palabras) y que nombre y organización coincidan con el manifiesto del JNE. Con --muestra N imprime N
propuestas al azar de cada plan con su página, para contrastarlas a mano con el PDF.
"""
import importlib.util, json, pathlib, random, re, sys, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMAS = {"seguridad", "transporte", "agua_riesgos", "urbano", "social", "economia", "ambiente", "gestion"}


def norm(t):
    t = unicodedata.normalize("NFD", t.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", t).replace(" %", "%")


def main(ruta, muestra=0):
    spec = importlib.util.spec_from_file_location("m", ruta)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    ub = m.UBIGEO
    manifiesto = {x["clave"]: x for x in json.loads((ROOT / f"scripts/planes/{ub}/manifiesto.json").read_text(encoding="utf-8"))["planes"]}
    errores, total = [], 0
    claves = [p[2] for p in m.PLANES]
    for falta in set(manifiesto) - set(claves):
        errores.append(f"Falta el plan «{falta}» del manifiesto")
    for nombre, org, clave, props in m.PLANES:
        man = manifiesto.get(clave)
        if not man:
            errores.append(f"{clave}: no está en el manifiesto")
            continue
        if (nombre or None) != man["candidato"]:
            errores.append(f"{clave}: candidato «{nombre}» ≠ manifiesto «{man['candidato']}»")
        if org != man["organizacion"]:
            errores.append(f"{clave}: organización «{org}» ≠ manifiesto «{man['organizacion']}»")
        paginas = json.loads((ROOT / f"scripts/planes/{ub}/{clave}.json").read_text(encoding="utf-8"))
        pn = [norm(p) for p in paginas]
        if not 8 <= len(props) <= 11:
            errores.append(f"{clave}: {len(props)} propuestas (deben ser 8–11)")
        temas = {p["tema"] for p in props}
        for p in props:
            total += 1
            if p["tema"] not in TEMAS:
                errores.append(f"{clave}: tema inválido «{p['tema']}»")
            palabras = len(p["texto"].split())
            if palabras > 30:
                errores.append(f"{clave}: texto de {palabras} palabras: «{p['texto'][:60]}…»")
            a = norm(p["ancla"])
            if len(a) < 8:
                errores.append(f"{clave}: ancla demasiado corta «{p['ancla']}»")
            encontradas = [i + 1 for i, t in enumerate(pn) if a in t]
            if not encontradas:
                errores.append(f"{clave}: ancla no encontrada «{p['ancla']}»")
            elif p["pagina"] not in encontradas:
                errores.append(f"{clave}: «{p['ancla']}» no está en p. {p['pagina']} (sí en {encontradas})")
        print(f"{clave}: {len(props)} propuestas · {sum(1 for p in props if p['meta'])} con meta · temas: {', '.join(sorted(temas))}")
        if muestra:
            for p in random.sample(props, min(muestra, len(props))):
                print(f"    p. {p['pagina']} [{p['tema']}] {p['texto']}" + (f" — Meta: {p['meta']}" if p["meta"] else ""))
                print(f"        ancla: «{p['ancla']}»")
    print(f"\n{len(m.PLANES)} planes, {total} propuestas, {len(errores)} errores")
    for e in errores:
        print("  ✗ " + e)
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    args = sys.argv[1:]
    n = int(args[args.index("--muestra") + 1]) if "--muestra" in args else 0
    main(args[0], n)
