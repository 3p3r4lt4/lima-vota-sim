"""Pucusana (150124): propuestas principales de los planes de gobierno inscritos ante el JNE.

Cada propuesta está redactada con palabras propias y lleva:
  - pagina: la página del PDF oficial donde aparece.
  - ancla: un fragmento textual del PDF que DEBE aparecer en esa página. El generador lo verifica y
    falla si no lo encuentra, para que ninguna cita apunte a una página equivocada.
Mismo criterio para todas: entre 8 y 11 propuestas por plan, repartidas en los temas que el plan desarrolla.
"""

UBIGEO = "150124"

def P(tema, texto, pagina, ancla, meta=None):
    return {"tema": tema, "texto": texto, "meta": meta, "pagina": pagina, "ancla": ancla}

# (nombre, organización, archivo PDF, propuestas)
PLANES = [
    ("Pedro Pablo Florián Huari", "Alianza para el Progreso", "alianza-para-el-progreso", [
        P("seguridad", "Juntas vecinales capacitadas y equipadas, y patrullaje integrado con la PNP durante todo el año", 15, "Patrullaje integrado los 365 días", "Patrullaje integrado los 365 días del año"),
        P("seguridad", "Instalar más cámaras de seguridad en el casco urbano y los asentamientos humanos", 15, "Instalación adicional de 12 cámaras", "12 cámaras adicionales"),
        P("social", "Reparación y mantenimiento de la infraestructura educativa y deportiva del distrito, incluidos losas y estadio", 15, "losas y estadio", "Mesa de trabajo anual (4) en educación y deporte"),
        P("social", "Talleres municipales culturales, vacaciones útiles y escuelas deportivas para escolares y jóvenes", 15, "Creación de los Talleres Municipales Culturales"),
        P("social", "Contratar un profesional para atender la violencia familiar y otro para asesoría legal permanente en la DEMUNA", 15, "Asesoría Legal permanente en la oficina de DEMUNA", "1 profesional especializado y 1 asesor legal permanente en la DEMUNA"),
        P("urbano", "Saneamiento físico legal de predios urbanos y rurales, con gestiones ante COFOPRI para titular a las familias", 15, "Gestión ante COFOPRI de la MPL", "Gestión ante COFOPRI desde 2027-2030"),
        P("economia", "Ferias de alimentos naturales y ofertas laborales para residentes en coordinación con el Ministerio de Trabajo", 16, "Promover ofertas laborales para residentes"),
        P("economia", "Recuperar las zonas turísticas y crear un circuito turístico en Pucusana", 16, "Para impulsar el Turismo en el"),
        P("ambiente", "Crear la Comisión Ambiental Municipal de la Bahía y elaborar un estudio de contaminación ambiental", 16, "Creación del CAM"),
        P("agua_riesgos", "Capacitar a dirigentes, colegios y empresas para formar una brigada ante desastres naturales", 16, "para crear una brigada"),
        P("gestion", "Convenio con una universidad o instituto para capacitar de forma sostenida a los servidores municipales", 17, "Registro de capacitaciones Un Convenio", "1 convenio con universidad o instituto"),
    ]),
    ("Jhonny Edgardo Calagua Huambachano", "Avanza País", "avanza-pais-partido-de-integracion-social", [
        P("seguridad", "Módulos de auxilio rápido en los asentamientos humanos y una central de monitoreo para todo el distrito", 9, "Instalación de la central de monitoreo"),
        P("seguridad", "Aplicativo «Alerta Pucusana» para reportar incidencias de forma anónima, en coordinación con la PNP", 9, "Alerta Pucusana"),
        P("social", "Becas integrales de estudios superiores y laptops para los tres mejores alumnos de 5.º de secundaria de cada colegio nacional", 9, "Apoyo a los mejores 3 alumnos"),
        P("social", "Gestionar una ambulancia municipal que funcione las 24 horas en coordinación con los centros de salud", 12, "adquisición de una ambulancia", "1 ambulancia municipal"),
        P("transporte", "Aplicativo «Pucu Verano» para inscribir el ingreso de vehículos en verano y controlar el aforo en las playas", 13, "Pucu Verano"),
        P("urbano", "Construir el Coliseo Benjamín Doig Lossio para la práctica deportiva de niños de los asentamientos aledaños", 11, "Coliseo Benjamin Doig Lossio"),
        P("urbano", "Facilitar constancias de posesión y apoyar gestiones de alumbrado, agua y desagüe en los asentamientos humanos", 17, "Regularizar al 97%", "97 % de los habitantes de estas zonas con constancia de posesión"),
        P("agua_riesgos", "Programa municipal de agua y desagüe para todos los asentamientos humanos", 14, "programa municipal de agua y desagüe"),
        P("ambiente", "Plantar árboles en el distrito y regarlos con aguas residuales de la laguna de oxidación", 19, "regado con aguas residuales", "100 % más árboles que al inicio de la gestión"),
        P("economia", "Agencia municipal de bolsa de trabajo con convenios con las empresas públicas y privadas del distrito", 15, "Creación de la agencia de bolsa de trabajo"),
        P("gestion", "Rendición de cuentas mediante sesiones públicas y cabildos abiertos", 8, "Rendición de cuentas semestral y anual", "Semestral y anual"),
    ]),
    ("Luis Martín Koc Lem Moya", "Fuerza Popular", "fuerza-popular", [
        P("social", "Centro Médico Municipal con cinco especialidades: medicina familiar, interna, pediatría, ginecología y geriatría", 7, "Centro Médico Municipal de Especialidades"),
        P("social", "Flota de ambulancias equipadas las 24 horas para los asentamientos humanos de difícil acceso", 8, "Flota Descentralizada de Ambulancias 24 Horas"),
        P("social", "Gestionar el primer instituto tecnológico del distrito y un CETPRO en mecánica de embarcaciones, turismo y gastronomía", 9, "CETPRO Pucusana: Implementación"),
        P("economia", "Escuela Municipal del Pescador y convenios con FONDEPES y la banca estatal para créditos y seguros", 12, "Escuela Municipal del Pescador"),
        P("economia", "Convenios con la zona industrial para una cuota de empleo preferente para jóvenes del distrito", 15, "cuota de empleo preferente"),
        P("economia", "Ventanilla única de formalización con tasas cero temporales para licencias de nuevos emprendimientos", 15, "Ventanilla Única de Formalización Comercial"),
        P("transporte", "«Ecobús Municipal» de bajas emisiones para trasladar turistas entre el casco urbano, las playas y los miradores", 13, "Ecobús Municipal"),
        P("urbano", "Catastro distrital digital de todo el territorio, con zonificación y áreas de preservación", 16, "levantamiento catastral informático al 100%", "Catastro del 100 % del territorio"),
        P("agua_riesgos", "Impulsar la instalación y puesta en marcha de la Planta Desalinizadora de Pucusana con el Gobierno, SEDAPAL e inversión privada", 17, "Viabilización de la Planta Desalinizadora"),
        P("ambiente", "Camiones compactadores y contenedores subterráneos en las zonas comerciales y turísticas", 18, "Recolección Automatizada e Islas Subterráneas"),
        P("gestion", "Trámite documentario digital «Cero Papel» con firma digital y seguimiento desde el celular", 22, "Digitalización Integral"),
    ]),
    ("Edwin Freddy Cuya Espinoza", "Somos Perú", "partido-democratico-somos-peru", [
        P("agua_riesgos", "Impulsar con el Ministerio de Vivienda el proyecto de agua y alcantarillado y gestionar sus etapas 2 y 3", 2, "Esquema General Pucusana de Agua y Alcantarillado"),
        P("urbano", "Mesa de trabajo con Luz del Sur para la electrificación masiva de los sectores que la soliciten", 2, "mesa de trabajo con la empresa Luz del Sur"),
        P("urbano", "Entregar con rapidez planos, resoluciones y constancias para el saneamiento físico legal de las habilitaciones", 2, "saneamiento físico legal de las 45 habilitaciones"),
        P("social", "Convenio con el MINSA para ampliar los centros de salud de Pucusana y Benjamín Doig Lossio", 2, "la firma de un convenio para las ampliaciones"),
        P("seguridad", "Construir la central de videovigilancia aprobada en el presupuesto participativo y seguir instalando cámaras", 3, "Construiremos de manera inmediata la central de video vigilancia"),
        P("seguridad", "Comprar camionetas nuevas para el serenazgo mediante el presupuesto participativo", 3, "compra de 03 unidades nuevas", "3 camionetas en el presupuesto participativo 2028"),
        P("social", "Centro de estudios técnico-profesional en el ingreso a playa Naplo mediante obras por impuestos", 3, "centro de estudio técnico-profesional"),
        P("transporte", "Actualizar el estudio técnico de vehículos menores y hacer operativos al transporte público con la ATU", 5, "estudio técnico general de vehículos menores"),
        P("ambiente", "Programa «playas limpias y saludables» y limpieza pública en tres turnos con horarios fijos de recojo", 5, "playas limpias y saludables"),
        P("economia", "Asesoría municipal y entrega de licencias de funcionamiento en el menor tiempo para microempresarios", 6, "su licencia de funcionamiento deberá ser entregada en el menor tiempo posible"),
        P("gestion", "Sistema de registro de expedientes que interconecte las áreas y reduzca el uso del papel", 6, "sistema de registro de expedientes"),
    ]),
    ("Enrique Julio Manco Suni", "Frente de la Esperanza 2021", "partido-frente-de-la-esperanza-2021", [
        P("seguridad", "Central de monitoreo con presencia policial, cámaras de última generación y aplicaciones móviles de seguridad", 6, "Central de monitoreo con presencia de personal policial"),
        P("social", "Gestionar dos ambulancias: una para atención a domicilio y otra tipo II para pacientes críticos", 8, "Gestionar la adquisición y equipamiento de 2 ambulancias", "2 ambulancias"),
        P("social", "«Farmacia de la Esperanza» con la DIRIS Lima Sur para medicamentos genéricos a precios accesibles", 8, "Farmacia de la Esperanza"),
        P("social", "Oficina Municipal de Becas, academia preuniversitaria municipal y un centro técnico-productivo con talleres", 9, "Creación de la Oficina Municipal de Becas"),
        P("urbano", "Plan de Desarrollo Urbano concertado y proyecto de catastro del distrito", 10, "Proyecto de Elaboración del Catastro"),
        P("agua_riesgos", "Convenio con SEDAPAL para más agua gratuita en zonas sin servicio hasta que se ejecute el proyecto Esquema Pucusana", 10, "Convenio con SEDAPAL para el incremento"),
        P("agua_riesgos", "Gestionar muros de contención en zonas de riesgo y escaleras seguras diseñadas para evacuación", 10, "Gestión para la construcción de muros de contención"),
        P("economia", "Plan de ordenamiento del comercio ambulatorio con ferias ordenadas, capacitación y capital semilla", 11, "Plan de Ordenamiento del Comercio Ambulatorio"),
        P("economia", "Circuito turístico PUCUTUR, aplicativo «Pucusana Destino Turístico» y formación de guías", 11, "Pucusana Destino Turístico"),
        P("ambiente", "Red de contenedores de basura subterráneos y Comité Ambiental Municipal", 12, "red de contenedores de basura subterráneos"),
        P("gestion", "Transformación digital: aplicaciones para el vecino, certificados digitales e interoperabilidad con otras entidades", 13, "Transformación digital"),
    ]),
    ("Sandra Paola Canchanya Espinoza", "Perú Primero", "partido-politico-peru-primero", [
        P("social", "Escuela Municipal Deportiva y Cultural con acceso gratuito para niños y jóvenes", 53, "Crear la Escuela Municipal Deportiva y Cultural"),
        P("seguridad", "Programa «Pucusana Segura» con patrullaje preventivo y vigilancia en zonas estratégicas", 53, "Pucusana Segura"),
        P("seguridad", "Más cámaras de videovigilancia y un centro de monitoreo equipado con personal permanente", 53, "Centro de Monitoreo totalmente equipado"),
        P("seguridad", "Puntos de control y tranqueras en los accesos para registrar el ingreso y salida de vehículos", 53, "puntos de control y tranqueras seguras"),
        P("urbano", "Construir, recuperar y descentralizar complejos deportivos y canchas en distintos sectores, de uso gratuito para niños y jóvenes", 53, "Construir, recuperar y descentralizar complejos deportivos"),
        P("social", "Programa Municipal de Atención Integral para personas con habilidades distintas y trastorno del espectro autista", 54, "Programa Municipal de Atención Integral"),
        P("economia", "Modernizar embarcaciones y conservación pesquera, e impulsar plantas de procesamiento con valor agregado", 55, "Impulsar plantas de procesamiento y valor agregado"),
        P("economia", "Circuitos turísticos de pesca vivencial, paseos marítimos y observación de fauna marina", 56, "circuitos turísticos de pesca vivencial"),
        P("ambiente", "Programa integral de limpieza pública con reportes vecinales por WhatsApp sobre contenedores y puntos críticos", 57, "sistemas de reporte vía WhatsApp"),
        P("agua_riesgos", "Mapas de riesgo y mecanismos de alerta temprana ante sismos, tsunamis y erosión costera", 58, "Establecer mecanismos de alerta anticipada"),
        P("gestion", "Digitalizar servicios y procedimientos municipales y crear sistemas de monitoreo institucional", 59, "Digitalización de servicios y procedimientos"),
    ]),
    ("Rocío del Pilar del Valle Morales", "PRIN", "partido-politico-prin", [
        P("seguridad", "Cámaras de videovigilancia, patrullaje integrado, alarmas vecinales y capacitación de juntas vecinales", 5, "Instalación de alarmas vecinales", "Reducir en 30 % la percepción de inseguridad ciudadana"),
        P("ambiente", "Unidades compactadoras, puntos ecológicos y erradicación de puntos críticos de basura", 6, "Adquisición de unidades compactadoras", "95 % de cobertura eficiente del servicio de limpieza pública"),
        P("social", "Campañas médicas descentralizadas y programas sociales y alimentarios para población vulnerable", 7, "Campañas médicas descentralizadas", "40 % más cobertura de programas preventivos y sociales"),
        P("economia", "Ferias gastronómicas y turísticas, mejora de espacios turísticos y capacitación empresarial", 7, "Ferias gastronómicas y turísticas", "40 % más actividad turística y comercial"),
        P("economia", "Bolsa laboral municipal, talleres ocupacionales y capacitaciones certificadas para jóvenes", 8, "Bolsa laboral municipal", "1 000 jóvenes capacitados"),
        P("economia", "Fortalecer la pesca artesanal y las actividades productivas locales", 12, "Fortalecer la pesca artesanal y actividades productivas locales", "30 % más apoyo productivo"),
        P("ambiente", "Jornadas de limpieza de playas, contenedores y campañas de sensibilización ambiental", 9, "Jornadas de limpieza de playas", "Reducir en 50 % los puntos críticos de contaminación ambiental"),
        P("ambiente", "Mejorar la conservación de áreas verdes y recuperar espacios públicos prioritarios", 12, "Mejorar conservación de áreas verdes"),
        P("urbano", "Actualizar el catastro urbano, fiscalizar construcciones informales y mejorar vías", 9, "Actualización del catastro urbano", "100 % del catastro urbano actualizado"),
        P("gestion", "Audiencias públicas, plataformas virtuales de información y presupuesto participativo", 10, "Implementación de plataformas virtuales", "4 audiencias públicas por año e informes periódicos de gestión"),
    ]),
    ("Oswaldo Américo Salazar Quispe", "Renovación Popular", "renovacion-popular-peru", [
        P("seguridad", "Más cámaras e interconexión de las cámaras de negocios y vecinos con una central de monitoreo las 24 horas", 3, "interconexión de las cámaras de los negocios", "Reducir en 50 % la delincuencia"),
        P("seguridad", "Más iluminación en el malecón y recuperación de espacios públicos donde se consume licor y drogas", 2, "mayor iluminación en el malecón", "Reducir en 70 % ese problema en el malecón"),
        P("social", "Gestionar con la UNI clases de matemática y física los fines de semana para escolares que postulen", 4, "Gestionar con la Universidad Nacional de ingeniería", "30 % más estudiantes con acceso a educación superior"),
        P("social", "Modernizar los centros de salud con el MINSA y gestionar con Lima un Hospital Solidario en el distrito", 6, "creación de un Hospital solidario"),
        P("urbano", "Mesas de trabajo con COFOPRI y la Municipalidad de Lima para el saneamiento físico legal de predios", 5, "Seguir convocando a las autoridades de COFOPRI", "30 % más titulación"),
        P("transporte", "Nuevas zonas de estacionamiento y paraderos para facilitar la movilidad nocturna", 6, "Crear nuevas zonas de estacionamientos"),
        P("economia", "Diversificar la economía local y posicionar Pucusana como destino turístico permanente", 7, "Diversificar la economía local", "300 emprendimientos formalizados y 60 % más turismo"),
        P("economia", "Promover la pesca artesanal y los restaurantes del balneario mediante medios y plataformas digitales", 7, "Fortalecer la pesca artesanal y comercialización", "50 % más ingreso diario de pescadores y negocios culinarios; 1 000 beneficiarios"),
        P("ambiente", "Planta de segregación y reciclaje, y programa «Playas Limpias Todo el Año»", 9, "Planta de segregación y reciclaje", "70 % más reciclaje"),
        P("ambiente", "Retirar desmonte de calles y avenidas con maquinaria de la Municipalidad de Lima y ganar áreas verdes", 9, "Retirar más de 200 toneladas de desmonte al año", "Más de 200 t de desmonte retiradas al año"),
        P("gestion", "Municipalidad Digital, plataforma de gobierno abierto y presupuesto participativo digital", 10, "Municipalidad Digital", "50 % menos tiempo promedio de atención"),
    ]),
]
