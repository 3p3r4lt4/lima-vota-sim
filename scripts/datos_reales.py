"""Genera los datos públicos del comparador a partir de fuentes verificables.

- Lima Metropolitana: propuestas expuestas por las 26 listas en el debate del JNE (21 y 22 de septiembre
  de 2026), redactadas con palabras propias a partir de la cobertura de RPP e Infobae. Cada propuesta
  enlaza a su fuente.
- La Molina: propuestas de los 12 planes de gobierno oficiales (ver scripts/la_molina.py), cada una con
  la página exacta del PDF, verificada automáticamente.
- Resto de distritos: relación de candidatos a alcalde publicada por RPP (28/09/2026). Sin propuestas
  hasta contar con los planes de todas sus candidaturas.

Para corregir o añadir datos, edita este archivo y ejecuta: python scripts/datos_reales.py
"""
import json, pathlib, re, sys, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "public/data"
CORTE = "28 de septiembre de 2026"

FUENTES = {
    "rpp_d1": {"medio": "RPP", "titulo": "Debate municipal en Lima: principales propuestas (1.ª jornada)", "fecha": "22/09/2026",
               "url": "https://rpp.pe/politica/elecciones/debate-municipal-en-lima-estas-fueron-las-principales-propuestas-de-los-candidatos-y-candidatas-noticia-1708684"},
    "rpp_d2": {"medio": "RPP", "titulo": "Debate municipal Lima 2026: propuestas de la 2.ª jornada", "fecha": "22/09/2026",
               "url": "https://rpp.pe/politica/elecciones/debate-municipal-lima-2026-en-vivo-hoy-minuto-a-minuto-segunda-jornada-candidatos-a-alcaldia-live-3625"},
    "inf_d1": {"medio": "Infobae", "titulo": "Debate municipal Lima 2026: así fue la primera jornada", "fecha": "22/09/2026",
               "url": "https://www.infobae.com/peru/2026/09/21/debate-municipal-lima-2026-en-vivo-13-candidatos-confrontan-hoy-sus-propuestas-rumbo-a-las-elecciones-del-4-de-octubre/"},
    "pi_d2":  {"medio": "Perú Informa", "titulo": "Candidatos a la alcaldía de Lima en la segunda jornada del debate", "fecha": "23/09/2026",
               "url": "https://www.peruinforma.com/elecciones-2026-candidatos-a-la-alcaldia-de-lima-toman-parte-en-la-segunda-jornada-del-debate-municipal/"},
    "ec_d2":  {"medio": "El Comercio", "titulo": "Debate por Lima: qué propusieron los candidatos en la segunda fecha", "fecha": "23/09/2026",
               "url": "https://elcomercio.pe/politica/elecciones/debate-por-lima-que-propusieron-los-candidatos-y-cuales-fueron-sus-principales-cruces-apuesplan-noticia/"},
    "rpp_lista": {"medio": "RPP", "titulo": "Candidatos a alcalde en los distritos de Lima Metropolitana", "fecha": "28/09/2026",
               "url": "https://rpp.pe/politica/elecciones/elecciones-2026-conoce-a-los-candidatos-a-alcalde-en-los-distritos-de-lima-metropolitana-noticia-1709752"},
}

TEMAS = {
    "seguridad": "Seguridad ciudadana",
    "transporte": "Tránsito y transporte",
    "agua_riesgos": "Agua, saneamiento y desastres",
    "urbano": "Vivienda, obras y espacio público",
    "social": "Salud, educación y programas sociales",
    "economia": "Empleo y comercio",
    "ambiente": "Limpieza y ambiente",
    "gestion": "Transparencia y gestión",
}

# (tema, propuesta, meta o None, fuente)
P = lambda tema, texto, meta=None, f="rpp_d1": {"tema": tema, "texto": texto, "meta": meta, "fuente": f}

LIMA = [
    ("Carlos Alberto Tejada Noriega", "Acción Popular", None, [
        P("seguridad", "Central de inteligencia multipropósito (G5) que integre seguridad, defensa civil, SAMU y bomberos", None, "rpp_d2"),
        P("transporte", "Replantear los corredores existentes y crear nuevos, con ciclovías y semaforización inteligente", "Ciclovías de al menos 5 km", "rpp_d2"),
        P("transporte", "Priorizar el transporte público masivo frente al vehículo particular", None, "rpp_d2"),
        P("urbano", "Programa de vivienda de acción social con enfoque integral y planificación urbana", None, "rpp_d2"),
    ]),
    ("Susel Ana María Paredes Piqué", "Ahora Nación", None, [
        P("seguridad", "Unidad de élite e inteligencia dentro del serenazgo contra la extorsión, coordinada con la Policía", "En los primeros 30 días"),
        P("seguridad", "Alquiler (renting) de patrulleros para asegurar operatividad continua y equipo técnico con exmandos policiales"),
        P("social", "Reformar los Hospitales de la Solidaridad sin afán de lucro, con laboratorios más baratos y mayor horario", "Atención hasta las 9 p. m."),
        P("social", "Pedir al Gobierno Central la transferencia de competencias educativas a la Municipalidad"),
        P("transporte", "Erradicar mafias en el trámite de brevetes y facilitar la formalización de taxistas"),
        P("transporte", "Exigir un plan de transporte integrado (metro, tren, bus y teleférico)", "Operación las 24 horas"),
    ]),
    ("Juan Carlos Alvarado Mestanza", "Alianza Electoral Venceremos", None, [
        P("seguridad", "Crear la Central de Seguridad de Lima", None, "rpp_d2"),
        P("transporte", "Priorizar tres corredores, de los once que plantea la ATU, para integrar los conos", "3 corredores", "rpp_d2"),
        P("social", "Enseñanza de inteligencia artificial en colegios de las zonas periféricas", None, "rpp_d2"),
        P("social", "Reorientar parte del presupuesto social para necesidades sanitarias de las zonas altas", "S/ 45 millones", "pi_d2"),
        P("gestion", "Plataforma de datos abiertos de la ciudad y publicación de resultados verificables", None, "rpp_d2"),
    ]),
    ("Elio Fernando Riera Garro", "Alianza para el Progreso", None, [
        P("gestion", "Plan 43: reuniones semanales descentralizadas con los alcaldes distritales, prensa y Defensoría para rendir cuentas", "Semanal, en Lima Norte, Sur, Centro y Este"),
        P("seguridad", "Red metropolitana de flagrancia que conecte serenazgos, cámaras, Fiscalía y Poder Judicial"),
        P("economia", "Programas Empléate Joven, Impúlsate Joven y Hazlo por tu barrio para jóvenes que no estudian ni trabajan", "Población objetivo: medio millón de jóvenes"),
    ]),
    ("Francis James Allison Oyague", "Avanza País", None, [
        P("seguridad", "Intervenir los lugares de venta de objetos robados y las zonas de mayor incidencia delictiva", None, "rpp_d2"),
        P("seguridad", "Serenazgo Metropolitano con un policía armado en cada unidad, e iluminación LED y cámaras en zonas críticas", None, "rpp_d2"),
        P("seguridad", "Recompensas por información que permita capturar a sicarios y cabecillas", "S/ 25 000 por sicario", "rpp_d2"),
        P("urbano", "Titulación masiva y construcción de escaleras, muros, losas deportivas y juegos infantiles", None, "ec_d2"),
        P("agua_riesgos", "Ante sismos, trabajo con colegios, bomberos y Policía, y reparto de medicinas y alimentos", None, "rpp_d2"),
        P("gestion", "Medición pública de resultados de los programas municipales", None, "rpp_d2"),
    ]),
    ("Samir Frank Quispe Caballero", "Batalla Perú", None, [
        P("seguridad", "Grupo de élite «Chavín» con licenciados de las Fuerzas Armadas y armas letales en zonas de alta incidencia"),
        P("economia", "Reemplazar la Gerencia de Fiscalización por una de Asesoramiento y Formalización del Comerciante, con créditos de la Caja Metropolitana"),
        P("transporte", "«Telelima»: red integrada de teleféricos como sistema principal de transporte"),
        P("urbano", "Modificar la zonificación para agilizar la titulación de terrenos"),
    ]),
    ("Yehude Simon Munaro", "Coalición Transformadora Tierra Verde", None, [
        P("seguridad", "Combatir la delincuencia con inteligencia policial e investigación; rechaza armar al serenazgo", "Reducir la inseguridad en 40 %"),
        P("seguridad", "Mejorar la videovigilancia y recuperar espacios públicos", "Videovigilancia +80 %, espacios públicos 70 %", "inf_d1"),
        P("agua_riesgos", "Ampliar la cobertura de agua y saneamiento, priorizando la «Lima gris» periférica", "De 70 % a 90 % al 2030"),
        P("economia", "Aumentar la formalización de mypes y el empleo formal", "50 % al 2030"),
        P("social", "Programa de becas", "50 000 becas"),
    ]),
    ("Segundo Valdez Zavala", "FREPAP", None, [
        P("seguridad", "Centrales de videovigilancia en los conos conectadas con serenazgo, PNP, bomberos, Fiscalía y auxilio médico", "4 500 cámaras iniciales en la central C5", "inf_d1"),
        P("social", "Programa Lima Crece Sana contra la anemia, con suplementación y biohuertos junto a ollas comunes", "Anemia por debajo de 15 %"),
        P("social", "Centro de auxilio rápido para emergencias médicas", None, "inf_d1"),
        P("ambiente", "Arborización masiva para duplicar las áreas verdes por habitante", "De 3 a 6 m² por habitante al 2030"),
    ]),
    ("Rubén Daniel Bonilla Espinoza", "Fuerza Ciudadana", None, [
        P("seguridad", "Cámaras con transmisión permanente y una nube integrada de información de seguridad", "100 % de cámaras en línea", "rpp_d2"),
        P("gestion", "Sistema LIA (Lima Inteligente Asistida) de alerta temprana, control y supervisión", None, "rpp_d2"),
        P("agua_riesgos", "Redistribuir de forma eficiente los servicios de agua y saneamiento en coordinación con el Gobierno", None, "rpp_d2"),
    ]),
    ("Samuel Marcos Daza Taype", "Fuerza Popular", None, [
        P("urbano", "Escaleras iluminadas, muros de contención y losas deportivas en zonas altas", "1 000 de cada una", "rpp_d2"),
        P("urbano", "Espacios municipales y recuperación de parques zonales", "30 espacios y 14 parques zonales", "rpp_d2"),
        P("transporte", "Ejecutar la Línea 3 del Metro de Lima", None, "rpp_d2"),
        P("seguridad", "Equipos técnicos de respuesta inmediata con presencia policial", "1 000 equipos", "rpp_d2"),
        P("ambiente", "Recuperar la Costa Verde como área verde", None, "rpp_d2"),
    ]),
    ("Oswaldo Hernán Vargas Cuéllar", "Juntos por el Perú", None, [
        P("seguridad", "Central de monitoreo C5 conectada con las centrales de los distritos contra sicariato y extorsión"),
        P("agua_riesgos", "Programa de agua potable, alcantarillado y muros de contención, con prevención ante huaicos y El Niño", "Atender al 8 % de limeños sin agua", "inf_d1"),
        P("transporte", "Atender el problema del tiempo perdido en el transporte (sin detalle en el debate)"),
    ]),
    ("Mónica Yadira Yaya Luyo", "Partido Aprista Peruano", None, [
        P("transporte", "Ampliar la línea del tren eléctrico hasta Ancón y crear una red de transporte urbano masivo", None, "rpp_d2"),
        P("transporte", "Priorizar el transporte público frente al vehículo particular", None, "rpp_d2"),
        P("gestion", "Revisar las cuentas y el estado financiero que deja la gestión anterior", None, "rpp_d2"),
        P("gestion", "Enfrentar la corrupción y el tráfico de terrenos", None, "ec_d2"),
    ]),
    ("Ricardo Pablo Belmont Cassinelli", "Partido Cívico Obras", None, [
        P("social", "Centros de auxilio rápido y postas con médicos de familia cerca de cada hogar", "A no más de 8 minutos"),
        P("transporte", "Reducir los tiempos de traslado desde los distritos alejados"),
        P("seguridad", "Prevención con comités barriales organizados y formación en valores desde la escuela"),
    ]),
    ("Carlos Francisco Gallardo Neyra", "Partido del Buen Gobierno", None, [
        P("seguridad", "Software de monitoreo y acción rápida que integre a los 42 distritos con PNP, Reniec, Fiscalía, bomberos y serenazgo", None, "rpp_d2"),
        P("agua_riesgos", "Respuesta ante sismos coordinada con las Fuerzas Armadas y especialistas", None, "rpp_d2"),
    ]),
    ("Flor de María Hurtado Valdez", "Partido Demócrata Verde", None, [
        P("seguridad", "Reorientar el serenazgo hacia la prevención y usar cámaras inteligentes"),
        P("gestion", "App de Lima Metropolitana para trámites digitales las 24 horas", "Licencia de funcionamiento en 1 día"),
        P("economia", "Evitar abusos en la fiscalización a pequeños comerciantes y crear bolsas de trabajo para jóvenes"),
    ]),
    ("Carlos Ricardo Bruce Montes de Oca", "Somos Perú", None, [
        P("seguridad", "Policía Municipal con licenciados de las Fuerzas Armadas para delitos comunes y serenos con pistolas paralizantes"),
        P("urbano", "Programa Techo Propio Limeño de vivienda social y oficina de titulación acelerada", "10 000 viviendas"),
        P("urbano", "Programa Mi Barrio Metropolitano: pistas, veredas y muros de contención"),
        P("transporte", "Red de semáforos inteligentes con financiamiento del Banco Mundial y corredores segregados", "5 corredores"),
    ]),
    ("Elizabeth María del Rosario León Chinchay", "Frente de la Esperanza 2021", None, [
        P("seguridad", "Gran central de vigilancia (aire, playas, tierra y buses) que reúna a Municipalidad, Fiscalía, PNP, SAMU y bomberos", None, "rpp_d2"),
        P("gestion", "Transparentar el gasto en proyectos, supervisión y costo de obras, con rendición de cuentas", None, "rpp_d2"),
        P("agua_riesgos", "Reducir el riesgo e incentivar servicios de agua para familias en los cerros", None, "rpp_d2"),
        P("ambiente", "Calles limpias y reciclaje como parte de su visión de ciudad", None, "rpp_d2"),
    ]),
    ("Victoria Betzabé La Cruz Garcés", "Partido Morado", None, [
        P("seguridad", "Mancomunidad con alcaldes de Lima y Callao, con IA para vigilancia predictiva y reconocimiento facial"),
        P("social", "Escuelas Ciudadanas con APAFA y UGEL, plataformas de aprendizaje con IA y apoyo en salud mental en comités vecinales"),
        P("agua_riesgos", "Encauzar y proteger las cuencas del Chillón, Rímac y Lurín, y exigir drenajes en el plan urbano"),
    ]),
    ("Sandro Caller Gutiérrez", "Partido Patriótico del Perú", None, [
        P("seguridad", "Cámaras con inteligencia artificial en puntos estratégicos de las vías metropolitanas", "17 000 cámaras en 7 500 puntos"),
        P("seguridad", "Sistema de Seguridad Metropolitano que articule distritos, Municipalidad y PNP, con más serenos y vehículos", "18 000 serenos y 2 700 vehículos"),
    ]),
    ("Yuri César Castro Romero", "Perú Libre", "Primer regidor (la lista no tiene candidato a alcalde)", [
        P("seguridad", "Serenazgo capacitado y equipado, en coordinación con la Policía", None, "rpp_d2"),
        P("urbano", "Recuperar espacios públicos para la recreación familiar", None, "rpp_d2"),
        P("social", "Más proteína para las ollas comunes", None, "rpp_d2"),
        P("economia", "Ampliar la capacidad de la Caja Metropolitana para emprendedores", None, "rpp_d2"),
    ]),
    ("Luis Alberto Huette Tolentino", "Pueblo Consciente", None, [
        P("seguridad", "Cámaras inteligentes, Policía Municipal armada con licenciados y cierre de centros de receptación", "20 000 cámaras"),
        P("social", "Tres hospitales de nivel III-2 en Puente Piedra, Lurín y San Juan de Lurigancho con inversión privada", "300 camas cada uno"),
        P("transporte", "Ampliar el Metropolitano de Ancón a Lurín, construir puentes sobre el Chillón y el Rímac y transferir la ATU a la Municipalidad", "3 puentes"),
    ]),
    ("Edgardo Renán de Pomar Vizcarra", "Partido Popular Cristiano (PPC)", None, [
        P("seguridad", "Serenazgo con armas de fuego y facultad de arresto, y organización de rondas urbanas", None, "rpp_d2"),
        P("ambiente", "Coordinar con los alcaldes distritales la recuperación ambiental e intervenir las cuencas del Lurín, Chillón y Rímac", None, "rpp_d2"),
    ]),
    ("Daniel Belizario Urresti Elera", "Podemos Perú", None, [
        P("seguridad", "Contratar equipos policiales para capturas diarias", "100 equipos y 100 capturas al día"),
        P("seguridad", "Patrulleros en renting para la PNP y cuatro megacomplejos policiales con centros de flagrancia", "1 000 patrulleros y 4 complejos"),
        P("seguridad", "Cerrar los mercados donde se venden bienes robados", "En los primeros 6 meses"),
    ]),
    ("Luis Miguel Llanos Carrillo", "Progresemos", None, [
        P("seguridad", "Recompensas por información sobre delincuentes y una «ley del buen samaritano»", None, "rpp_d2"),
        P("transporte", "Pedir al Congreso habilitar «tres horarios» de tránsito para descongestionar la ciudad", None, "rpp_d2"),
    ]),
    ("Rafael Bernardo López Aliaga Cazorla", "Renovación Popular", "Primer regidor (la lista no tiene candidato a alcalde; el JNE no había definido si un primer regidor puede asumir la alcaldía)", [
        P("seguridad", "Inversión en inteligencia municipal para prevenir delitos", "Más de S/ 100 millones", "rpp_d2"),
        P("gestion", "Duplicar los ingresos municipales con recursos propios y aduaneros", None, "rpp_d2"),
        P("transporte", "Que la ATU vuelva a Lima, buses modernos, recuperar carriles de la Panamericana Norte y terminar la Vía Expresa Sur", "8 carriles en la Panamericana Norte", "rpp_d2"),
        P("economia", "Comprar espacios para trasladar el comercio informal a mercados", None, "rpp_d2"),
        P("ambiente", "Limpiar los ríos y eliminar químicos contaminantes", None, "rpp_d2"),
    ]),
    ("Santiago Rosendo Abarca León", "Visión Perú", None, [
        P("seguridad", "Oficina virtual para denuncias anónimas por celular y promoción de la legítima defensa", None, "rpp_d2"),
        P("agua_riesgos", "Ejecutar los planes estratégicos de gestión del riesgo de desastres", None, "rpp_d2"),
        P("transporte", "Ordenar el tránsito pesado nocturno", None, "pi_d2"),
        P("social", "Centro de atención especializado para menores con TDAH y autismo", None, "pi_d2"),
    ]),
]

DISTRITOS = {
    "150102": "Ancón", "150103": "Ate", "150104": "Barranco", "150105": "Breña", "150106": "Carabayllo",
    "150107": "Chaclacayo", "150108": "Chorrillos", "150109": "Cieneguilla", "150110": "Comas",
    "150111": "El Agustino", "150112": "Independencia", "150113": "Jesús María", "150114": "La Molina",
    "150115": "La Victoria", "150116": "Lince", "150117": "Los Olivos", "150118": "Lurigancho-Chosica",
    "150119": "Lurín", "150120": "Magdalena del Mar", "150121": "Pueblo Libre", "150122": "Miraflores",
    "150123": "Pachacámac", "150124": "Pucusana", "150125": "Puente Piedra", "150126": "Punta Hermosa",
    "150127": "Punta Negra", "150128": "Rímac", "150129": "San Bartolo", "150130": "San Borja",
    "150131": "San Isidro", "150132": "San Juan de Lurigancho", "150133": "San Juan de Miraflores",
    "150134": "San Luis", "150135": "San Martín de Porres", "150136": "San Miguel", "150137": "Santa Anita",
    "150138": "Santa María del Mar", "150139": "Santa Rosa", "150140": "Santiago de Surco",
    "150141": "Surquillo", "150142": "Villa El Salvador", "150143": "Villa María del Triunfo",
}

sys.path.insert(0, str(ROOT / "scripts"))
import la_molina  # noqa: E402
PLANES_DISTRITALES = {la_molina.UBIGEO: la_molina}

LISTA_DISTRITOS = (ROOT / "scripts/candidatos_distritales.txt").read_text(encoding="utf-8")

def parsear_distritos():
    nombre_a_ubigeo = {v: k for k, v in DISTRITOS.items()}
    salida, actual = {}, None
    for linea in LISTA_DISTRITOS.splitlines():
        linea = linea.strip()
        if linea.startswith("## "):
            actual = nombre_a_ubigeo[linea[3:].strip()]
            salida[actual] = []
        elif linea.startswith("- ") and actual:
            nombre, org = [x.strip() for x in linea[2:].split(" — ")]
            salida[actual].append((None if nombre == "SIN CANDIDATO" else nombre, org))
    faltan = set(DISTRITOS) - set(salida)
    assert not faltan, f"Faltan distritos: {faltan}"
    return salida

def norm(t):
    t = unicodedata.normalize("NFD", t.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", t).replace(" %", "%")

def generar_plan_distrital(modulo, cid, nombres_oficiales):
    """Comparación y corpus a partir de planes de gobierno en PDF, con verificación de cada cita."""
    ub = modulo.UBIGEO
    fuentes, comp_c, planes_c = {}, [], []
    oficiales = {norm(n) for n, _ in nombres_oficiales if n}
    assert len(modulo.PLANES) == len(nombres_oficiales), f"{ub}: faltan planes ({len(modulo.PLANES)} de {len(nombres_oficiales)})"
    for nombre, org, clave, props in modulo.PLANES:
        assert norm(nombre) in oficiales, f"{nombre} no está en la lista oficial de {ub}"
        paginas = json.loads((ROOT / f"scripts/planes/{ub}/{clave}.json").read_text(encoding="utf-8"))
        pn = [norm(p) for p in paginas]
        url = f"/planes/{ub}/{clave}.pdf"
        fk = f"plan_{clave}"
        fuentes[fk] = {"medio": "Plan de gobierno", "titulo": f"Plan de gobierno de {org} (JNE)", "fecha": "2026", "url": url, "pdf": True}
        temas = {t: {"sin_informacion": True, "propuestas": []} for t in TEMAS}
        for p in props:
            assert p["tema"] in TEMAS, p
            ancla = norm(p["ancla"])
            encontradas = [i + 1 for i, t in enumerate(pn) if ancla in t]
            assert encontradas, f"{org}: no se encontró «{p['ancla']}» en el plan"
            pag = p["pagina"] or next((x for x in encontradas if x > 2), encontradas[0])
            assert pag in encontradas, f"{org}: «{p['ancla']}» no está en la p. {pag} (sí en {encontradas})"
            temas[p["tema"]]["sin_informacion"] = False
            temas[p["tema"]]["propuestas"].append({"texto": p["texto"], "meta": p["meta"], "fuente": fk, "pagina": pag})
        comp_c.append({"id": cid, "nombre": nombre, "organizacion": org, "cargo_nota": None, "temas": temas})
        planes_c.append({"id": cid, "nombre": nombre, "organizacion": org, "pdf": url,
                         "paginas": [{"pagina": i + 1, "titulo": f"Página {i + 1} del plan", "texto": t, "fuentes": [fk]}
                                     for i, t in enumerate(paginas) if len(t) > 40]})
        cid += 1
    return comp_c, planes_c, fuentes, cid

def main():
    for d in ("comparaciones", "planes"):
        (DATA / d).mkdir(parents=True, exist_ok=True)
        for f in (DATA / d).glob("*.json"):
            f.unlink()

    cid = 1
    comp = {"ubigeo": "1501", "ambito": "Lima Metropolitana", "nivel": "provincial", "cargo": "Alcaldía de Lima Metropolitana",
            "con_propuestas": True, "corte": CORTE, "fuentes": FUENTES, "temas": list(TEMAS), "nombres_temas": TEMAS,
            "tipo_fuente": "debate",
            "nota_fuente": "Propuestas expuestas en el debate del JNE (21 y 22 de septiembre), según la cobertura de medios citada. No reemplazan el plan de gobierno completo.",
            "candidatos": []}
    planes = {"ubigeo": "1501", "ambito": "Lima Metropolitana", "fuentes": FUENTES, "candidatos": []}
    for nombre, org, cargo_nota, props in LIMA:
        assert all(p["tema"] in TEMAS for p in props), nombre
        temas, paginas = {}, []
        for i, t in enumerate(TEMAS, start=1):
            lista = [{"texto": p["texto"], "meta": p["meta"], "fuente": p["fuente"], "pagina": i} for p in props if p["tema"] == t]
            temas[t] = {"sin_informacion": not lista, "propuestas": lista}
            if lista:
                texto = " ".join(f"{p['texto']}." + (f" Meta: {p['meta']}." if p["meta"] else "") for p in lista)
                paginas.append({"pagina": i, "titulo": TEMAS[t], "texto": texto, "fuentes": sorted({p["fuente"] for p in lista})})
        comp["candidatos"].append({"id": cid, "nombre": nombre, "organizacion": org, "cargo_nota": cargo_nota, "temas": temas})
        planes["candidatos"].append({"id": cid, "nombre": nombre, "organizacion": org, "paginas": paginas})
        cid += 1
    escribir("1501", comp, planes)

    indice = [{"ubigeo": "1501", "ambito": "Lima Metropolitana", "nivel": "provincial", "candidatos": len(LIMA), "con_propuestas": True}]
    total = 0
    for ubigeo, lista in sorted(parsear_distritos().items(), key=lambda x: DISTRITOS[x[0]]):
        base = {"ubigeo": ubigeo, "ambito": DISTRITOS[ubigeo], "nivel": "distrital", "cargo": "Alcaldía distrital", "corte": CORTE}
        if ubigeo in PLANES_DISTRITALES:
            comp_c, planes_c, fuentes, cid = generar_plan_distrital(PLANES_DISTRITALES[ubigeo], cid, lista)
            d = {**base, "con_propuestas": True, "tipo_fuente": "plan", "fuentes": fuentes, "temas": list(TEMAS), "nombres_temas": TEMAS,
                 "nota_fuente": "Propuestas principales de los planes de gobierno inscritos ante el JNE, con la página exacta de cada una. Resumen con palabras propias: revisa siempre el plan completo.",
                 "candidatos": comp_c}
            escribir(ubigeo, d, {"ubigeo": ubigeo, "ambito": DISTRITOS[ubigeo], "fuentes": fuentes, "candidatos": planes_c})
        else:
            d = {**base, "con_propuestas": False, "fuentes": {"rpp_lista": FUENTES["rpp_lista"]}, "temas": [],
                 "nota_fuente": "Relación de candidatos según la base electoral difundida por RPP. Puede variar por exclusiones o renuncias: confirma en la plataforma del JNE.",
                 "candidatos": []}
            for nombre, org in lista:
                d["candidatos"].append({"id": cid, "nombre": nombre or "Sin candidato a alcalde", "organizacion": org,
                                        "cargo_nota": None if nombre else "La organización figura en competencia sin candidato a alcalde consignado.",
                                        "temas": {}})
                cid += 1
            escribir(ubigeo, d)
        n = sum(1 for x, _ in lista if x)
        total += n
        indice.append({"ubigeo": ubigeo, "ambito": DISTRITOS[ubigeo], "nivel": "distrital", "candidatos": n,
                       "con_propuestas": ubigeo in PLANES_DISTRITALES})
    (DATA / "ambitos.json").write_text(json.dumps(indice, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Lima Metropolitana: {len(LIMA)} listas, {sum(len(x[3]) for x in LIMA)} propuestas")
    for ub, m in PLANES_DISTRITALES.items():
        print(f"{DISTRITOS[ub]}: {len(m.PLANES)} planes, {sum(len(x[3]) for x in m.PLANES)} propuestas verificadas")
    print(f"Distritos: {len(indice) - 1}, {total} candidatos")

def escribir(ubigeo, comp, planes=None):
    (DATA / f"comparaciones/{ubigeo}.json").write_text(json.dumps(comp, ensure_ascii=False, indent=1), encoding="utf-8")
    if planes:
        (DATA / f"planes/{ubigeo}.json").write_text(json.dumps(planes, ensure_ascii=False), encoding="utf-8")

if __name__ == "__main__":
    main()
