"""Genera datos SIMULADOS (candidaturas y planes ficticios) para Lima Metropolitana y sus 42 distritos.
No usa nombres de candidatos ni organizaciones reales.

Salida:
  public/data/ambitos.json
  public/data/comparaciones/<ubigeo>.json   matriz candidato x tema
  public/data/planes/<ubigeo>.json          texto de cada plan, por página (corpus del RAG)

Uso: python scripts/generar_simulacion.py
"""
import json, pathlib, random

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "public/data"
SEMILLA = 20261004
rng = random.Random(SEMILLA)

# El Cercado (150101) lo gobierna la Municipalidad de Lima Metropolitana: no tiene elección distrital propia
DISTRITOS = {
    "150102": "Ancón", "150103": "Ate", "150104": "Barranco", "150105": "Breña", "150106": "Carabayllo",
    "150107": "Chaclacayo", "150108": "Chorrillos", "150109": "Cieneguilla", "150110": "Comas",
    "150111": "El Agustino", "150112": "Independencia", "150113": "Jesús María", "150114": "La Molina",
    "150115": "La Victoria", "150116": "Lince", "150117": "Los Olivos", "150118": "Lurigancho",
    "150119": "Lurín", "150120": "Magdalena del Mar", "150121": "Pueblo Libre", "150122": "Miraflores",
    "150123": "Pachacámac", "150124": "Pucusana", "150125": "Puente Piedra", "150126": "Punta Hermosa",
    "150127": "Punta Negra", "150128": "Rímac", "150129": "San Bartolo", "150130": "San Borja",
    "150131": "San Isidro", "150132": "San Juan de Lurigancho", "150133": "San Juan de Miraflores",
    "150134": "San Luis", "150135": "San Martín de Porres", "150136": "San Miguel", "150137": "Santa Anita",
    "150138": "Santa María del Mar", "150139": "Santa Rosa", "150140": "Santiago de Surco",
    "150141": "Surquillo", "150142": "Villa El Salvador", "150143": "Villa María del Triunfo",
}
LETRAS = ["Alfa", "Beta", "Gamma", "Delta", "Épsilon", "Zeta", "Eta", "Theta"]

# (texto de la propuesta, plantilla de meta o None, rango numérico)
TEMAS = {
    "seguridad": ("Seguridad ciudadana", [
        ("Incorporar serenos adicionales y reorganizar el patrullaje por sectores en {d}", "{n} serenos nuevos al 2028", (30, 250)),
        ("Crear una central de videovigilancia integrada con las comisarías de la PNP", "{n} cámaras operativas", (80, 600)),
        ("Implementar un botón de alerta vecinal en una aplicación móvil municipal", "Operativa en el primer año", None),
        ("Recuperar espacios públicos con iluminación LED en parques y paraderos", "{n} puntos iluminados", (100, 900)),
        ("Fortalecer las juntas vecinales con capacitación y radios de comunicación", "{n} juntas vecinales activas", (20, 120)),
        ("Patrullaje integrado serenazgo-PNP en zonas de mayor incidencia delictiva", None, None),
    ]),
    "transporte": ("Tránsito y transporte", [
        ("Ordenar paraderos y retirar paraderos informales en las avenidas principales", "{n} paraderos formalizados", (20, 150)),
        ("Construir ciclovías conectadas con los distritos vecinos", "{n} km de ciclovías", (3, 25)),
        ("Instalar semáforos adaptativos en los cruces con mayor congestión", "{n} intersecciones", (10, 60)),
        ("Programa de mantenimiento y parchado de pistas con cronograma público", "{n} km rehabilitados", (10, 90)),
        ("Mejorar veredas y rampas para peatones y personas con discapacidad", None, None),
        ("Coordinar con la ATU rutas alimentadoras hacia corredores y estaciones", None, None),
    ]),
    "residuos": ("Limpieza y residuos", [
        ("Programa de segregación en la fuente casa por casa", "{n}% de viviendas participando", (15, 60)),
        ("Renovar la flota de compactadoras y ampliar el recojo nocturno", "{n} unidades nuevas", (4, 30)),
        ("Planta municipal de compostaje para residuos orgánicos y de parques", "{n} toneladas al mes", (20, 300)),
        ("Erradicar puntos críticos de acumulación de basura con vigilancia y multas", "{n} puntos críticos eliminados", (10, 80)),
        ("Incorporar recicladores formalizados al sistema municipal", None, None),
    ]),
    "areas_verdes": ("Áreas verdes y ambiente", [
        ("Riego de parques con agua tratada en lugar de agua potable", "{n}% del riego con agua tratada", (20, 80)),
        ("Arborización de avenidas y bermas centrales", "{n} árboles plantados", (1000, 15000)),
        ("Recuperar parques abandonados con participación vecinal", "{n} parques recuperados", (5, 40)),
        ("Monitoreo público de calidad del aire y ruido", None, None),
        ("Proteger lomas, ribera o zonas naturales del distrito frente a invasiones", None, None),
    ]),
    "desarrollo_urbano": ("Desarrollo urbano", [
        ("Actualizar el catastro urbano con tecnología de drones y GIS", "Catastro actualizado al 2028", None),
        ("Licencias de edificación y funcionamiento 100% digitales", "Plazo máximo de {n} días hábiles", (5, 15)),
        ("Plan de obras con priorización por presupuesto participativo", None, None),
        ("Muros de contención, escaleras y accesos en zonas de ladera", "{n} obras ejecutadas", (5, 60)),
        ("Revisar la zonificación para ordenar el crecimiento vertical", None, None),
    ]),
    "social": ("Programas sociales", [
        ("Ampliar el programa del adulto mayor con talleres y atención en casa", "{n} adultos mayores atendidos", (500, 6000)),
        ("Cunas y centros de cuidado infantil para madres trabajadoras", "{n} centros nuevos", (1, 8)),
        ("Transparentar el padrón del Vaso de Leche y focalizar beneficiarios", None, None),
        ("Campañas de salud preventiva y anemia en coordinación con el MINSA", "{n} campañas al año", (6, 40)),
        ("Becas y talleres para jóvenes en oficios y habilidades digitales", "{n} jóvenes capacitados", (200, 3000)),
    ]),
    "economia": ("Economía local", [
        ("Ventanilla única para emprendedores y formalización de negocios", "{n} negocios formalizados", (200, 4000)),
        ("Reordenar el comercio ambulatorio con zonas autorizadas y reubicación", None, None),
        ("Ferias municipales para productores y emprendedores del distrito", "{n} ferias al año", (4, 24)),
        ("Bolsa de empleo municipal con empresas del distrito", "{n} personas colocadas", (300, 5000)),
        ("Promover el turismo local con rutas culturales y gastronómicas", None, None),
    ]),
    "gestion": ("Transparencia y gestión", [
        ("Publicar en datos abiertos el gasto, contrataciones y avance de obras", None, None),
        ("Trámites en línea con seguimiento por expediente", "{n}% de trámites digitales", (50, 100)),
        ("Rendición de cuentas vecinal presencial dos veces al año", None, None),
        ("Oficina de integridad y canal de denuncias anónimas", None, None),
        ("Presupuesto participativo con votación vecinal en línea", None, None),
    ]),
}

def minusc(t):
    return t[0].lower() + t[1:]

def generar_candidatura(cid, letra, ambito, escala):
    temas, paginas = {}, []
    paginas.append({"pagina": 1, "titulo": "Presentación y diagnóstico", "texto":
        f"Plan de gobierno simulado de la candidatura {letra} para {ambito}, periodo 2027-2030. "
        f"Documento ficticio generado para demostrar un sistema de consulta. Identifica como problemas "
        f"prioritarios de {ambito} la inseguridad, el tránsito, la limpieza pública y la gestión municipal."})
    orden = list(TEMAS)
    rng.shuffle(orden)
    pag = 2
    for tema in orden:
        nombre_tema, pool = TEMAS[tema]
        if rng.random() < 0.15:
            temas[tema] = {"sin_informacion": True, "resumen": "", "propuestas": []}
            continue
        elegidas = rng.sample(pool, rng.randint(1, 3))
        props, frases = [], []
        for texto, meta_t, rango in elegidas:
            texto = texto.format(d=ambito)
            if escala > 1:
                texto = texto.replace("del distrito", "de la ciudad")
            meta = None
            if meta_t and rng.random() < 0.75:
                escalable = "%" not in meta_t and "días" not in meta_t
                n = rng.randint(*rango) * (escala if escalable else 1) if rango else None
                meta = meta_t.format(n=f"{n:,}".replace(",", " ") if n else "")
            props.append({"texto": texto, "meta": meta, "pagina": pag})
            frases.append(f"{texto}." + (f" Meta: {meta}." if meta else ""))
        resumen = "Propone " + minusc(props[0]["texto"])
        if len(props) > 1:
            resumen += " y " + minusc(props[1]["texto"])
        palabras = resumen.split()
        resumen = " ".join(palabras[:40]) + ("…" if len(palabras) > 40 else ".")
        temas[tema] = {"sin_informacion": False, "resumen": resumen, "propuestas": props}
        paginas.append({"pagina": pag, "titulo": f"Eje: {nombre_tema}", "texto":
            f"En materia de {nombre_tema.lower()}, la candidatura {letra} plantea para {ambito}: " + " ".join(frases)})
        pag += 1
    paginas.append({"pagina": pag, "titulo": "Financiamiento y seguimiento", "texto":
        "Las propuestas se financiarán con recursos ordinarios, canon y transferencias, y su avance "
        "se reportará en un tablero público de indicadores. Contenido ficticio."})
    return {"id": cid, "nombre": f"Candidatura {letra}", "organizacion": f"Organización simulada {letra}",
            "temas": temas}, {"id": cid, "nombre": f"Candidatura {letra}", "paginas": paginas}

def main():
    (DATA / "comparaciones").mkdir(parents=True, exist_ok=True)
    (DATA / "planes").mkdir(parents=True, exist_ok=True)
    ambitos = [("1501", "Lima Metropolitana", "provincial", "Alcaldía de Lima Metropolitana", 6, 8)]
    ambitos += [(u, n, "distrital", "Alcaldía distrital", rng.randint(3, 5), 1) for u, n in DISTRITOS.items()]
    indice, cid = [], 1
    for ubigeo, ambito, nivel, cargo, n_cand, escala in ambitos:
        comp = {"ubigeo": ubigeo, "ambito": ambito, "nivel": nivel, "cargo": cargo,
                "simulado": True, "temas": list(TEMAS), "candidatos": []}
        planes = {"ubigeo": ubigeo, "ambito": ambito, "simulado": True, "candidatos": []}
        for letra in LETRAS[:n_cand]:
            c, p = generar_candidatura(cid, letra, ambito, escala)
            comp["candidatos"].append(c)
            planes["candidatos"].append(p)
            cid += 1
        for carpeta, obj in (("comparaciones", comp), ("planes", planes)):
            (DATA / carpeta / f"{ubigeo}.json").write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        indice.append({"ubigeo": ubigeo, "ambito": ambito, "nivel": nivel, "candidatos": n_cand})
    (DATA / "ambitos.json").write_text(json.dumps(indice, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(indice)} ámbitos, {cid - 1} candidaturas simuladas")

if __name__ == "__main__":
    main()
