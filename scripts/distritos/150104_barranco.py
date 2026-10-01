"""Barranco (150104): propuestas principales de los 8 planes de gobierno inscritos ante el JNE.

Cada propuesta está redactada con palabras propias y lleva:
  - pagina: la página del PDF oficial donde aparece.
  - ancla: un fragmento textual del PDF que DEBE aparecer en esa página. El generador lo verifica y
    falla si no lo encuentra, para que ninguna cita apunte a una página equivocada.
Mismo criterio para todas: entre 8 y 11 propuestas por plan, repartidas en los temas que el plan desarrolla.
"""

UBIGEO = "150104"

def P(tema, texto, pagina, ancla, meta=None):
    return {"tema": tema, "texto": texto, "meta": meta, "pagina": pagina, "ancla": ancla}

# (nombre, organización, archivo PDF, propuestas)
PLANES = [
    ("María Luisa Cardoso Serra", "Acción Popular", "accion-popular", [
        P("seguridad", "Programa «Barranco Seguro 360» con Centro de Monitoreo Inteligente, serenazgo reforzado, recuperación de espacios públicos y trabajo con juntas vecinales y PNP", 21, "Programa Barranco Seguro 360 con Centro de Monitoreo Inteligente", "30 % más de cobertura de videovigilancia y 100 % de juntas vecinales activas fortalecidas"),
        P("transporte", "Plan Integral de Movilidad Barranquina y gestiones ante la MML, la ATU y el MTC para intervenir puntos críticos de tránsito", 21, "Plan Integral de Movilidad Barranquina y gestión permanente", "100 % de los puntos críticos de movilidad priorizados intervenidos"),
        P("social", "Programa «Barranco Saludable» con campañas preventivas y actividades de salud mental comunitaria", 21, "Programa Barranco Saludable y Bienestar Comunitario orientado", "50 % más de campañas preventivas y 50 % más de acceso a salud mental comunitaria"),
        P("social", "Programa «Barranco Activo» con actividades deportivas y recreativas para todas las edades", 21, "Programa Barranco Activo para promover el deporte", "50 % más de actividades deportivas y recreativas municipales"),
        P("economia", "Programa «Barranco Destino Cultural y Turístico Inteligente» con circuitos turísticos, culturales y gastronómicos", 22, "Incrementar en 30% la oferta de actividades y circuitos turísticos", "30 % más de actividades y circuitos turísticos"),
        P("economia", "Programa «Barranco Emprende»: capacitación, transformación digital de negocios, ferias y ruedas de negocios", 22, "Incrementar en 30% la participación de micro y pequeñas empresas", "30 % más de mypes en programas de fortalecimiento empresarial"),
        P("ambiente", "Rutas de recolección optimizadas con tecnología, segregación en la fuente con incentivos, red de «Puntos Verdes» y compostaje municipal", 23, "Reducir en un 80% los puntos críticos", "80 % menos puntos críticos de acumulación de residuos"),
        P("urbano", "Programa «Patrimonio Vivo Barranquino»: identificar inmuebles patrimoniales en riesgo, elaborar expedientes técnicos e incentivar su conservación", 23, "Patrimonio Vivo Barranquino", "100 % de inmuebles patrimoniales en riesgo identificados"),
        P("ambiente", "Arborización con especies nativas y plan de protección y monitoreo del litoral y los acantilados", 24, "Plan de protección y monitoreo del litoral y acantilados", "25 % más de arbolado urbano y monitoreo permanente del 100 % del borde costero"),
        P("gestion", "«La Municipalidad en tus manos»: todos los trámites del TUPA desde el celular o la computadora, y consultas por teléfono y WhatsApp", 24, "100% de trámites TUPA digitalizados", "100 % de trámites TUPA digitalizados"),
        P("gestion", "Gobierno abierto: publicar contratos y concesiones, transmitir en vivo las sesiones del Concejo y atención semanal de autoridades a vecinos", 25, "100% de contratos y concesiones publicados", "100 % de contratos y concesiones publicados"),
    ]),
    ("Angélica María Noguerol Sueldo", "Avanza País", "avanza-pais-partido-de-integracion-social", [
        P("seguridad", "Modernizar la central de monitoreo con analítica avanzada e inteligencia artificial en las cámaras de seguridad", 4, "tecnología analítica avanzada e inteligencia artificial en las cámaras de seguridad", "100 % de las cámaras municipales integradas con inteligencia artificial al 2030"),
        P("seguridad", "Dotar al serenazgo de chalecos antibalas, gas pimienta, grilletes de nylon y varas tonfa, con capacitación continua", 5, "chalecos antibalas, gas pimienta, grilletes de nylon"),
        P("social", "Campañas integrales de salud con alianzas público-privadas, apoyo a niños con TDAH o TEA y una Veterinaria Municipal", 17, "48 campañas integrales de salud realizadas", "48 campañas de salud (12 por año) y 1 Veterinaria Municipal operativa"),
        P("social", "Semilleros deportivos municipales, incluida una Academia Municipal de Deportes de Contacto", 17, "1 semillero deportivo multidisciplinario funcionando", "1 semillero deportivo multidisciplinario permanente"),
        P("transporte", "Semaforización inteligente en las avenidas e intersecciones de mayor congestión", 17, "100% de las avenidas principales interconectadas", "100 % de las avenidas principales con semáforos inteligentes al 2030"),
        P("transporte", "Señalización vial preventiva en los perímetros de los colegios, con campañas de educación vial", 17, "100% de las zonas escolares públicas y privadas", "100 % de las zonas escolares públicas y privadas señalizadas"),
        P("economia", "Soporte técnico a emprendimientos tradicionales y formalización de artistas, vinculándolos a circuitos turísticos", 17, "Revalorizar la identidad barranquina insertando", "Al menos 6 actividades culturales o comerciales al año"),
        P("ambiente", "Riego tecnificado en las áreas verdes y fomento de muros y techos verdes", 17, "Incrementar la superficie vegetal urbana adoptando tecnologías", "100 % de espacios verdes con riego tecnificado y 20 muros o techos verdes piloto"),
        P("ambiente", "Campañas de desinfección, limpieza profunda y lavado de calles, plazas y mercados", 18, "100% de mercados y plazas principales desinfectados", "100 % de mercados y plazas principales desinfectados al menos una vez al mes"),
        P("urbano", "Planificación urbana participativa con mesas de diálogo vecinal y protección de las Zonas Monumentales", 18, "1 Plan de Desarrollo Urbano Participativo actualizado", "1 Plan de Desarrollo Urbano Participativo aprobado"),
        P("gestion", "Audiencias públicas semestrales de rendición de cuentas y tablero público de avance de metas, con respuesta a reclamos en 2 días hábiles", 18, "dos (2) audiencias públicas al año", "2 audiencias públicas al año"),
    ]),
    ("José Juan Rodríguez Cárdenas", "Libertad Popular", "libertad-popular", [
        P("social", "Red Cultural y Educativa con biblioteca y mediateca digital, auditorio, salas de exposición, talleres y laboratorios de innovación", 4, "Biblioteca moderna y mediateca digital"),
        P("social", "Ampliar los servicios del CIAM con programas de envejecimiento activo y actividades recreativas", 5, "servicios del Centro Integral del Adulto Mayor (CIAM)", "Duplicar la oferta de talleres y programas de 2026"),
        P("urbano", "Eliminar barreras arquitectónicas y adecuar espacios públicos con accesibilidad universal", 5, "Eliminación progresiva de barreras arquitectónicas", "100 % de locales municipales y 100 % de parques"),
        P("social", "Escuelas municipales deportivas y artísticas, y programas de reforzamiento educativo para niños y adolescentes", 5, "Escuelas municipales deportivas y artísticas", "Duplicar la oferta de talleres y programas de 2026"),
        P("seguridad", "Modernizar la central de monitoreo, ampliar la videovigilancia inteligente e incorporar análisis predictivo de incidentes", 6, "Implementación de herramientas de análisis predictivo"),
        P("seguridad", "Atender conflictos por actividades nocturnas, controlar la contaminación sonora y promover la mediación comunitaria", 6, "Atención de conflictos relacionados con actividades nocturnas"),
        P("economia", "Agilizar la emisión de licencias de funcionamiento", 10, "Agilizar emisión de licencias", "24 horas para emitir licencias de funcionamiento"),
        P("transporte", "Plan de Desarrollo Urbano y de Movilidad para el distrito", 10, "Plan de Desarrollo Urbano y de Movilidad para el distrito"),
        P("ambiente", "Incrementar la cobertura vegetal urbana con siembra de árboles", 10, "Incremento de la cobertura vegetal urbana", "Duplicar el número de árboles en el distrito"),
        P("urbano", "Mejorar los accesos a las playas y activar el borde costero con actividades culturales y recreativas", 11, "Activación cultural y recreativa del borde costero", "Recuperar el 100 % de los accesos peatonales"),
        P("gestion", "Digitalizar los principales trámites municipales y abrir módulos de trámite descentralizados", 11, "principales trámites municipales", "100 % de trámites digitalizados en línea y 6 módulos instalados"),
    ]),
    ("Felipe Antonio Mezarina Tong", "Somos Perú", "partido-democratico-somos-peru", [
        P("seguridad", "Programa «Barranco Seguro 24 Horas»: central con inteligencia artificial y nuevas cámaras en accesos, límites, playas, malecones y corredores gastronómicos", 9, "Instalar nuevas cámaras de videovigilancia en zonas críticas", "100 % de cámaras operativas integradas y respuesta a incidencias críticas en 5 minutos o menos"),
        P("transporte", "Nuevas conexiones viales en el entorno del ex cine Balta y Metro, y paso a desnivel en la Av. Bolognesi", 10, "Pase a desnivel en la Av. Bolognesi"),
        P("transporte", "Red continua de ciclovías conectada al sistema de transporte y a los distritos vecinos", 11, "Incrementar en un 40% la red de ciclovías", "40 % más de red de ciclovías"),
        P("social", "Policlínico Municipal con atención primaria, salud mental y especialidades a tarifas sociales, y campañas mensuales de salud", 12, "Policlínico Municipal de atención primaria", "12 campañas de salud preventiva al año"),
        P("social", "Remodelación integral del Complejo Deportivo Luis Gálvez Chipoco y reserva de turnos en línea", 14, "Complejo Deportivo Luis Gálvez Chipoco", "60 % de espacios deportivos y culturales recuperados"),
        P("economia", "Bolsa de empleo barranquino articulada con empresas del distrito y campañas de formalización progresiva", 15, "bolsa de empleo barranquino, articulada", "40 % de trabajadores colocados mediante la bolsa de empleo y 40 % más de negocios formalizados"),
        P("economia", "Corredores turísticos, culturales y gastronómicos seguros e iluminados, y alianza con PROMPERÚ", 17, "Implementar 04 corredores turísticos", "4 corredores turísticos con intervención integral"),
        P("ambiente", "Programa «Barranco Verde y Limpio»: plantas de tratamiento de aguas residuales para riego tecnificado, arborización y contenedores soterrados", 18, "Plantas de Tratamiento de Aguas Residuales para el riego", "40 % de áreas verdes con riego tecnificado y 70 % más de puntos críticos de residuos recuperados"),
        P("agua_riesgos", "Convertir el talud del acantilado en jardines estabilizados (andenería) y gestionar obras de protección de acantilados y malecones", 19, "sistema de jardines estabilizados (andenería)", "40 % más de intervenciones en accesos, malecones o zonas vulnerables"),
        P("urbano", "Óvalo en Av. Grau con Av. El Sol, mejoramiento del malecón Paul Harris y soterrado progresivo del cableado aéreo", 19, "soterrado del cableado"),
        P("gestion", "Programa «Municipalidad Digital y de Puertas Abiertas» con trámites en línea y tablero de control de metas", 21, "80% de trámites disponibles en línea", "80 % de trámites disponibles en línea"),
    ]),
    ("Enrique Fernando Delucchi Chueca", "Partido Morado", "partido-morado", [
        P("seguridad", "Centro de Comando Serenazgo–PNP que integre cámaras, GPS y radios, con patrullaje focalizado por zonas de mayor incidencia", 9, "patrullaje focalizado por hotspots"),
        P("social", "Ruta del Atletismo Barranquino en malecones y Bajada de Baños, y una Escuela Municipal de Running gratuita", 6, "Ruta del Atletismo Barranquino"),
        P("social", "DEMUNA itinerante con psicólogo y abogado que visiten cada semana los colegios públicos", 7, "equipos itinerantes de psicólogo y abogado"),
        P("economia", "Ventanilla Única de Formalización, padrón de comercios y ruta progresiva de orientación, advertencia, fiscalización y sanción", 11, "Ventanilla Única de Formalización"),
        P("economia", "Programa «Barranco Nocturno Ordenado» con horarios diferenciados, control de ruido y licencias condicionadas", 12, "Barranco Nocturno Ordenado"),
        P("urbano", "Plan Urbano Distrital 2027-2037 que actualice zonificación y alturas, y proteja la Zona Monumental y el borde costero", 15, "Plan Urbano Distrital 2027-2037"),
        P("transporte", "Gestión inteligente del tránsito con sensores, cámaras y sincronización semafórica en corredores como Av. Grau y San Martín", 17, "reducción estimada de 30% a 40% en tiempos de traslado", "Entre 30 % y 40 % menos tiempo de traslado en corredores priorizados"),
        P("ambiente", "Sistema «Barranco Separa en Casa, Edificio y Negocio» con reciclaje, compostaje y recicladores formales", 21, "incorporar hasta el 85% de viviendas", "Hasta 85 % de viviendas y edificios y 100 % de grandes generadores al 2030"),
        P("agua_riesgos", "Riego tecnificado por sectores y jardines de bajo consumo de agua", 22, "Tecnificar hasta el 80% de áreas verdes priorizadas", "Hasta 80 % de áreas verdes priorizadas con riego tecnificado y 50 % menos césped no funcional"),
        P("ambiente", "Red de Infraestructura Verde con corredores verdes y arbolado en malecones, parques y avenidas", 23, "Incorporar hasta 1,200 árboles nuevos", "Hasta 8 corredores verdes y 1 200 árboles nuevos"),
        P("gestion", "Diversificar los ingresos municipales con convenios y obras por impuestos, sin elevar los arbitrios", 28, "Conseguir una obra por impuestos por año", "1 obra por impuestos al año"),
    ]),
    ("Jorge Antonio Ruiz de Somocurcio Hidalgo", "PPC", "partido-popular-cristiano-ppc", [
        P("seguridad", "Más capacidad operativa del serenazgo con mejor equipamiento y capacitación, y patrullaje integrado con la PNP", 6, "Incrementar en 50% la capacidad operativa del Serenazgo", "50 % más de capacidad operativa del serenazgo y 30 % menos percepción de inseguridad"),
        P("seguridad", "Modernizar el sistema de videovigilancia con cámaras inteligentes y monitoreo permanente", 6, "Instalar o modernizar el 100% del sistema de videovigilancia", "100 % del sistema de videovigilancia distrital instalado o modernizado"),
        P("urbano", "Rehabilitación y mantenimiento de viviendas de adultos mayores vulnerables y asesoría gratuita para regularizar predios", 7, "al menos 200 viviendas de adultos mayores", "Al menos 200 viviendas de adultos mayores rehabilitadas"),
        P("social", "Casa de la Juventud de Barranco con talleres de capacitación, emprendimiento y becas", 8, "Beneficiar a más de 2,000 jóvenes", "Más de 2 000 jóvenes beneficiados y al menos 15 convenios educativos"),
        P("social", "Fortalecer las escuelas deportivas municipales y recuperar los espacios deportivos", 8, "Duplicar el número de participantes en escuelas deportivas", "Duplicar los participantes en escuelas deportivas municipales"),
        P("urbano", "Conservación y puesta en valor de inmuebles patrimoniales mediante gestión y convenios", 9, "al menos 10 espacios o inmuebles de interés patrimonial", "Al menos 10 espacios o inmuebles patrimoniales recuperados"),
        P("transporte", "Plan de Movilidad que evalúe trasladar el Metropolitano a la Vía Expresa Sur y deje la Av. Bolognesi para alimentadores", 14, "relocalización del recorrido del Metropolitano"),
        P("ambiente", "Programa de arbolado en las bermas laterales de vías locales y avenidas, con reposición de árboles retirados", 11, "programa de arbolado del distrito"),
        P("economia", "Plataforma «Barranco a tu Casa» para el delivery de los mercados y ferias de fin de semana para emprendedores del distrito", 18, "Barranco a tu Casa"),
        P("urbano", "Plan Urbano Distrital 2027-2037 por concurso, consensuado con vecinos y la Municipalidad de Lima", 19, "Plan Urbano Distrital 2027-2037"),
        P("gestion", "Contrataciones de personal por concurso o lista corta, con meritocracia y rendición de cuentas", 22, "convocatoria a Concurso o lista corta"),
    ]),
    ("Nicole Fiorella Muñoz Zevallos", "Progresemos", "progresemos", [
        P("seguridad", "Centro de Comando C4 integrado a la PNP y cámaras con reconocimiento facial y lectura de placas", 6, "Instalación de 300 cámaras de videovigilancia", "300 cámaras de videovigilancia"),
        P("seguridad", "Serenazgo 24/7 con patrullaje a pie y en bicicleta, y Unidad de Respuesta Rápida ante emergencias", 6, "Serenazgo 24/7, con 80 serenos operativos", "80 serenos, 15 motos y 4 camionetas; respuesta en menos de 5 minutos"),
        P("urbano", "Plan de asfaltado y mantenimiento de calles con sardineles y drenaje pluvial, y renovación de veredas con rampas", 8, "Intervención del 100% de calles, avenidas y pasajes", "100 % de calles, avenidas y pasajes intervenidos"),
        P("ambiente", "Sistema de recolección selectiva y reciclaje «Barranco Verde» con separación en origen y valorización", 9, "Meta: 40% de residuos reciclados al 2030", "40 % de residuos reciclados al 2030"),
        P("agua_riesgos", "Ejecutar el Plan Maestro de la Costa Verde en Barranco: malecones, paseos, ciclovías y obras contra la erosión costera", 9, "Obras de protección contra la erosión costera", "Intervención del 100 % del tramo de Barranco"),
        P("ambiente", "Programa «Más Árboles, Más Vida» de forestación de avenidas, parques y calles", 9, "Más Árboles, Más Vida", "6 m² de área verde por habitante"),
        P("economia", "Centro de Desarrollo Empresarial para mypes y artesanos, y modernización de mercados de abastos", 11, "Centro de Desarrollo Empresarial", "Al menos 500 mypes fortalecidas y 2 mercados modernizados"),
        P("social", "Centro de Atención Integral al Adulto Mayor y Centro de Protección a la Mujer con refugio temporal para víctimas de violencia", 13, "Centro de Protección a la Mujer y la Familia", "Al menos 2 000 personas atendidas y 3 centros especializados"),
        P("gestion", "Presupuesto participativo para que los vecinos decidan las obras prioritarias", 13, "no menos del 10% del presupuesto de inversiones", "Al menos 10 % del presupuesto de inversiones"),
        P("gestion", "Plataforma «Barranco Digital» con todos los trámites en línea, aplicativo de reportes y datos abiertos", 15, "100% de trámites y servicios municipales disponibles en línea", "100 % de trámites y servicios en línea"),
        P("transporte", "Conexiones seguras con Miraflores, San Isidro y la Costa Verde, con ciclovías y transporte sostenible", 16, "conexiones seguras con Miraflores, San Isidro y la Costa Verde"),
    ]),
    ("Manuel Milenco Espinoza Loarte", "Renovación Popular", "renovacion-popular-peru", [
        P("transporte", "Fiscalizadores de tránsito con capacidad de sanción, semáforos en zonas críticas y estudio del Plan Vial de Tránsito", 9, "Realizar el estudio del Plan Vial de Tránsito"),
        P("seguridad", "Serenazgo las 24 horas en puntos críticos, mejor alumbrado y videovigilancia integrada con la PNP y las juntas vecinales", 9, "Ampliar la cobertura de serenazgo en los puntos críticos"),
        P("social", "Policlínico Municipal de atención primaria y centro bromatológico para el control sanitario de restaurantes y mercados", 10, "centro bromatológico municipal"),
        P("social", "Complejo deportivo municipal en la playa Las Sombrillas y programas deportivos itinerantes", 11, "complejo deportivo municipal en Playa las Sombrillas"),
        P("economia", "Centro Municipal de Emprendimiento y Hub de Innovación con coworking y laboratorio de fabricación digital", 12, "Hub de Innovación Municipal"),
        P("economia", "«Pasaporte Barranco Cultural»: circuito turístico con premios que conecta puntos artísticos y gastronómicos con descuentos en comercios locales", 13, "un circuito turístico gamificado"),
        P("urbano", "Puesta en valor de espacios emblemáticos con MINCETUR y COPESCO, y poner en funcionamiento el Funicular", 14, "poner en funcionamiento el Funicular"),
        P("agua_riesgos", "Espigones en el litoral para mitigar la erosión marina y recuperar la franja de arena de las playas", 14, "construcción de espigones en el litoral de Barranco"),
        P("ambiente", "Programa RECICLA Barranco con empadronamiento de nuevos edificios y formalización de recicladores", 15, "incluir sociolaboralmente a 10 recicladores", "10 recicladores formalizados"),
        P("ambiente", "Arborizar la base del acantilado y declarar intangibles los humedales de las playas Los Yuyos y Las Sombrillas", 16, "plantación masiva de 500 árboles nativos", "500 árboles nativos"),
        P("gestion", "Sistema de gestión antisoborno ISO 37001, informes trimestrales de gestión y administración directa de la piscina y el estadio municipales", 17, "Implementar el ISO 37001"),
    ]),
]
