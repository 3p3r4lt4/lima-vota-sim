"""Descarga los planes de gobierno distritales inscritos ante el JNE (ERM 2026) y su manifiesto.

Fuente: API pública que usa el frontend de Voto Informado (votoinformado.jne.gob.pe):
  POST /api/v1/candidatos/organizaciones              {dep, pro, dis}                    -> listas y rutaPlanGobierno
  POST /api/v1/candidatos/organizaciones/candidatos   {dep, pro, dis, idSolicitudLista}  -> candidatos de la lista
  GET  https://mpesije.jne.gob.pe/docs/<rutaPlanGobierno>                                 -> PDF del plan
El JNE usa ubigeo de RENIEC (Lima = 14), no el del INEI que usa este proyecto (Lima = 15): se mapea por nombre.

Los PDF NO se versionan: se guardan en scripts/.cache/planes/<ubigeo>/<clave>.pdf (solo para extraer el texto) y
el sitio enlaza a la URL oficial del JNE. El manifiesto scripts/planes/<ubigeo>/manifiesto.json registra candidato,
organización, URL de origen, fecha de descarga y SHA-256 de cada plan.

Uso:   python scripts/descargar_planes.py 150130 150141
Reglas: máx. 1 petición por segundo, User-Agent identificable, reintentos con backoff, caché local; si la respuesta
no es JSON/PDF (p. ej. un desafío anti-bots), se detiene sin reintentar.
"""
import datetime, hashlib, json, pathlib, re, sys, time, unicodedata, urllib.error, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE = ROOT / "scripts/.cache"
API = "https://votoinformado.jne.gob.pe/api"
DOCS = "https://mpesije.jne.gob.pe/docs/"
UA = "lima-vota-sim/1.0 (comparador ciudadano de planes de gobierno; +https://github.com/3p3r4lt4/lima-vota-sim)"
INTERVALO = 1.1
ALIAS_JNE = {"LURIGANCHO-CHOSICA": "LURIGANCHO"}

_ultima = 0.0


class Bloqueo(Exception):
    """La fuente respondió algo que no es el dato esperado: no se insiste."""


def norm(t):
    t = unicodedata.normalize("NFD", t).encode("ascii", "ignore").decode().upper()
    return re.sub(r"\s+", " ", t).strip()


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", norm(t).lower()).strip("-")


def pedir(url, cuerpo=None, tipo="json", intentos=4):
    global _ultima
    datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
    cab = {"User-Agent": UA, "Accept": "application/json" if tipo == "json" else "application/pdf"}
    if datos:
        cab["Content-Type"] = "application/json"
    for n in range(intentos):
        time.sleep(max(0.0, _ultima + INTERVALO - time.time()))
        _ultima = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=datos, headers=cab), timeout=60) as r:
                ctype = r.headers.get("Content-Type", "")
                cuerpo_r = r.read()
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise Bloqueo(f"{url}: HTTP {e.code}. Posible bloqueo: se detiene la descarga.")
            if n == intentos - 1:
                raise
            print(f"  HTTP {e.code}, reintento en {2 ** (n + 1)} s", file=sys.stderr)
        except (urllib.error.URLError, TimeoutError) as e:
            if n == intentos - 1:
                raise
            print(f"  {e}, reintento en {2 ** (n + 1)} s", file=sys.stderr)
        else:
            if tipo == "json" and "json" not in ctype:
                raise Bloqueo(f"{url}: se esperaba JSON y llegó «{ctype}». Posible desafío anti-bots: se detiene.")
            if tipo == "pdf" and not cuerpo_r.startswith(b"%PDF"):
                raise Bloqueo(f"{url}: se esperaba un PDF y llegó «{ctype}». Se detiene.")
            return json.loads(cuerpo_r) if tipo == "json" else cuerpo_r
        time.sleep(2 ** (n + 1))


def api_cacheada(nombre, ruta, cuerpo):
    f = CACHE / "api" / f"{nombre}.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    d = pedir(API + ruta, cuerpo)
    if not d.get("success"):
        raise RuntimeError(f"{ruta} {cuerpo}: {d.get('message')}")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8", newline="\n")
    return d


def lista_local():
    """scripts/candidatos_distritales.txt -> {distrito: [(nombre | None, organización)]}"""
    salida, actual = {}, None
    for linea in (ROOT / "scripts/candidatos_distritales.txt").read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if linea.startswith("## "):
            actual = linea[3:].strip()
            salida[actual] = []
        elif linea.startswith("- ") and actual:
            nombre, org = [x.strip() for x in linea[2:].split(" — ")]
            salida[actual].append((None if nombre == "SIN CANDIDATO" else nombre, org))
    return salida


def codigo_jne(distrito):
    f = CACHE / "api" / "distritos_14_01.json"  # GET sin envoltorio {success, data}: se cachea aparte
    if not f.exists():
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(pedir(API + "/v1/departamentos/14/provincias/01/distritos"), ensure_ascii=False), encoding="utf-8", newline="\n")
    jne = json.loads(f.read_text(encoding="utf-8"))
    buscado = ALIAS_JNE.get(norm(distrito), norm(distrito))
    return next(x["id"] for x in jne if norm(x["nombre"]) == buscado)


def descargar(ubigeo, ambitos, local):
    distrito = next(a["ambito"] for a in ambitos if a["ubigeo"] == ubigeo)
    dis = codigo_jne(distrito)
    print(f"\n== {ubigeo} {distrito} (JNE 14-01-{dis})")
    orgs = api_cacheada(f"org_{ubigeo}", "/v1/candidatos/organizaciones", {"dep": "14", "pro": "01", "dis": dis})
    bloque = next(b for b in orgs["data"] if "DISTRITAL" in b["tipoEleccion"])
    carpeta = CACHE / "planes" / ubigeo
    carpeta.mkdir(parents=True, exist_ok=True)
    nuestra = local[distrito]
    por_nombre = {norm(n): (n, o) for n, o in nuestra if n}
    manifiesto, emparejados, avisos = [], set(), []

    for o in bloque["organizaciones"]:
        lista = o["listas"][0]
        org_jne = o["organizacionPolitica"]
        clave = slug(org_jne)
        cands = api_cacheada(f"cand_{ubigeo}_{lista['idSolicitudLista']}", "/v1/candidatos/organizaciones/candidatos",
                             {"dep": "14", "pro": "01", "dis": dis, "idSolicitudLista": lista["idSolicitudLista"]})
        todos = [c for b in cands["data"] for org in b["organizaciones"] for l in org["listas"] for c in l.get("candidatos", [])]
        alcalde = next((c for c in todos if "ALCALDE" in c["cargoEleccion"]), None)
        nombre_jne = " ".join(alcalde[k] for k in ("nombres", "apellidoPaterno", "apellidoMaterno") if alcalde.get(k)) if alcalde else None

        # Cruce con nuestra lista: solo coincidencias exactas (sin tildes ni mayúsculas); el resto se reporta
        nombre_local = org_local = None
        if nombre_jne and norm(nombre_jne) in por_nombre:
            nombre_local, org_local = por_nombre[norm(nombre_jne)]
            emparejados.add(norm(nombre_jne))
        elif nombre_jne:
            avisos.append(f"Nombre distinto o ausente en nuestra lista: «{nombre_jne}» ({org_jne}). No se empareja automáticamente.")
        else:
            sin = [org for n, org in nuestra if n is None]
            avisos.append(f"Lista sin candidato a alcalde en el JNE: {org_jne}. En nuestra lista figuran sin candidato: {sin or 'ninguna'}.")
        if alcalde and alcalde["estadoCandidato"] != "INSCRITO":
            avisos.append(f"{nombre_jne or 'Candidatura a alcalde'} ({org_jne}) figura como {alcalde['estadoCandidato']}.")

        item = {"clave": clave, "organizacion_jne": org_jne, "organizacion": org_local, "candidato": nombre_local,
                "candidato_jne": nombre_jne, "estado_candidato": alcalde["estadoCandidato"] if alcalde else None,
                "id_solicitud_lista": lista["idSolicitudLista"], "expediente": lista["codigoExpediente"]}
        ruta = lista.get("rutaPlanGobierno")
        if not ruta:
            avisos.append(f"SIN PLAN publicado en el JNE: {org_jne} ({nombre_jne or 'sin candidato'}).")
            manifiesto.append({**item, "url": None, "plan": False})
            continue
        url = DOCS + ruta
        pdf = carpeta / f"{clave}.pdf"
        anterior = next((m for m in leer_manifiesto(ubigeo) if m["clave"] == clave), None)
        if pdf.exists() and anterior and anterior.get("url") == url and anterior.get("sha256") == sha256(pdf.read_bytes()):
            datos, fecha = pdf.read_bytes(), anterior["descargado"]
            print(f"  = {clave}.pdf (ya descargado, mismo hash)")
        else:
            datos, fecha = pedir(url, tipo="pdf"), datetime.date.today().isoformat()
            pdf.write_bytes(datos)
            print(f"  ↓ {clave}.pdf ({len(datos) / 1e6:.2f} MB)")
        manifiesto.append({**item, "url": url, "plan": True, "descargado": fecha, "sha256": sha256(datos),
                           "bytes": len(datos), "ocr": (anterior or {}).get("ocr", False)})

    # Listas sin candidato a alcalde: solo se emparejan si hay exactamente una en cada lado (no se adivina)
    sin_jne = [m for m in manifiesto if not m["candidato_jne"]]
    sin_local = [org for n, org in nuestra if n is None]
    if len(sin_jne) == 1 and len(sin_local) == 1:
        sin_jne[0]["organizacion"] = sin_local[0]
    elif sin_jne or sin_local:
        avisos.append(f"Listas sin candidato a alcalde sin emparejar: JNE {[m['organizacion_jne'] for m in sin_jne]}, nuestra lista {sin_local}.")

    for n, org in nuestra:
        if n and norm(n) not in emparejados:
            avisos.append(f"De nuestra lista sin pareja exacta en el JNE: «{n}» ({org}). Revisar si cambió de nombre o fue excluido.")
    if len(bloque["organizaciones"]) != len(nuestra):
        avisos.append(f"Número de listas distinto: JNE {len(bloque['organizaciones'])}, nuestra lista {len(nuestra)}.")

    salida = ROOT / "scripts/planes" / ubigeo
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "manifiesto.json").write_text(json.dumps(
        {"ubigeo": ubigeo, "ambito": distrito, "ubigeo_jne": f"1401{dis}", "fuente": API + "/v1/candidatos/organizaciones",
         "planes": manifiesto, "avisos": avisos}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    con_plan = sum(m["plan"] for m in manifiesto)
    print(f"  {con_plan} de {len(manifiesto)} listas con plan · {sum(m.get('bytes', 0) for m in manifiesto) / 1e6:.1f} MB")
    for a in avisos:
        print("  ! " + a)


def leer_manifiesto(ubigeo):
    f = ROOT / "scripts/planes" / ubigeo / "manifiesto.json"
    return json.loads(f.read_text(encoding="utf-8"))["planes"] if f.exists() else []


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def main(ubigeos):
    if not ubigeos:
        sys.exit(__doc__)
    ambitos = json.loads((ROOT / "public/data/ambitos.json").read_text(encoding="utf-8"))
    local = lista_local()
    try:
        for u in ubigeos:
            descargar(u, ambitos, local)
    except Bloqueo as e:
        sys.exit(f"\nDETENIDO: {e}")


if __name__ == "__main__":
    main(sys.argv[1:])
