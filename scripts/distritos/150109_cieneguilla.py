"""Cieneguilla (150109): propuestas principales de los planes de gobierno inscritos ante el JNE.

Cada propuesta está redactada con palabras propias y lleva:
  - pagina: la página del PDF oficial donde aparece.
  - ancla: un fragmento textual del PDF que DEBE aparecer en esa página. El generador lo verifica y
    falla si no lo encuentra, para que ninguna cita apunte a una página equivocada.
Mismo criterio para todas: entre 8 y 11 propuestas por plan, repartidas en los temas que el plan desarrolla.
"""

UBIGEO = "150109"

def P(tema, texto, pagina, ancla, meta=None):
    return {"tema": tema, "texto": texto, "meta": meta, "pagina": pagina, "ancla": ancla}

# (nombre, organización, archivo PDF, propuestas)
PLANES = [
    ("Wilber Jorge Ancco Mamani", "Alianza para el Progreso", "alianza-para-el-progreso", [
        P("seguridad", "Centros de Monitoreo y Videovigilancia sectoriales y fortalecimiento del serenazgo municipal", 2, "fortalecer el Serenazgo Municipal"),
        P("social", "Campañas médicas descentralizadas y convenios institucionales para la atención preventiva de salud", 2, "campañas médicas descentralizadas y convenios institucionales", "30 campañas (2027-2030)"),
        P("urbano", "Programa «Cieneguilla Ciudad Jardín» para recuperar parques y espacios públicos", 2, "Cieneguilla Ciudad Jardín", "10 parques (2027-2030)"),
        P("economia", "Corredores turísticos, gastronómicos y culturales para promover el turismo sostenible", 2, "corredores turísticos, gastronómicos y culturales"),
        P("economia", "Programa «Emprende Cieneguilla» de capacitación y formalización empresarial", 2, "Emprende Cieneguilla"),
        P("transporte", "Mantenimiento vial y construcción de infraestructura peatonal segura", 2, "programas de mantenimiento vial", "50 km de vías rehabilitadas (2027-2030)"),
        P("ambiente", "Gestión de residuos sólidos con programas de segregación y reciclaje", 3, "programas de segregación y reciclaje", "100 % de cobertura de recolección (2027-2030)"),
        P("ambiente", "Programas de conservación para recuperar y proteger el ecosistema del río Lurín", 3, "proteger el ecosistema del río Lurín", "4 campañas (2027-2030)"),
        P("ambiente", "Programa «Cieneguilla Verde» de recuperación de áreas verdes y arborización", 3, "Cieneguilla Verde"),
        P("gestion", "Portal de Gobierno Abierto con transmisión de sesiones y Gobierno Digital Municipal para los trámites", 3, "Portal de Gobierno Abierto", "100 % de sesiones transmitidas y 80 % de trámites digitalizados (2027-2030)"),
        P("gestion", "Audiencias públicas semestrales en cada sector, avance trimestral de obras y comités de vigilancia ciudadana", 4, "Audiencias Públicas Semestrales Descentralizadas"),
    ]),
    ("Ermelinda Lanazca Baltazar de Taype", "FREPAP", "frente-popular-agricola-fia-del-peru", [
        P("social", "Programa «Cieneguilla Crece Sana»: suplementación nutricional, alimentos ricos en hierro, huertos familiares y seguimiento de gestantes y niños", 10, "Cieneguilla Crece Sana", "Anemia infantil de 10,8 % a menos de 5 % al 2030"),
        P("social", "«Escuelas del Futuro para Cieneguilla»: mejora de infraestructura educativa, conectividad y equipamiento con MINEDU y PRONIED", 10, "Escuelas del Futuro para Cieneguilla", "Intervenir al menos el 60 % de instituciones educativas con mayores brechas al 2030"),
        P("seguridad", "«Cieneguilla Segura»: más videovigilancia, serenazgo modernizado, patrullaje integrado con la PNP e iluminación de espacios públicos", 11, "ampliación del sistema de videovigilancia", "Reducir en 20 % los delitos patrimoniales al 2030"),
        P("agua_riesgos", "Programa «Servicios Básicos para una Cieneguilla Digna»: proyectos de agua y alcantarillado con Sedapal y ampliación de redes eléctricas", 12, "Servicios Básicos para una Cieneguilla Digna", "+20 puntos porcentuales en agua y saneamiento y electrificación superior al 98 % al 2030"),
        P("economia", "«Emprende Cieneguilla»: asistencia para formalizar negocios, bolsa de empleo local, ferias laborales y capacitación", 12, "Emprende Cieneguilla", "Reducir la informalidad laboral en 15 puntos porcentuales al 2030"),
        P("economia", "Corredor turístico hacia el Qhapaq Ñan y el valle de Lurín, festivales gastronómicos y circuitos ecoturísticos", 13, "agenda anual de festivales gastronómicos y culturales", "+50 % de flujo turístico y duplicar la permanencia promedio al 2030"),
        P("transporte", "Plan de conectividad: mejorar vías de acceso a centros poblados y atractivos turísticos y ordenar zonas comerciales", 13, "Plan Integral de Conectividad y Competitividad Local", "30 km de vías estratégicas y accesos turísticos al 2030"),
        P("ambiente", "«Cieneguilla Limpia y Circular»: segregación en la fuente, formalización de recicladores, centros de acopio y planta de compostaje", 14, "Cieneguilla Limpia y Circular", "Valorizar al menos el 25 % de los residuos sólidos al 2030"),
        P("agua_riesgos", "Plan de gestión del riesgo: diques y defensas ribereñas, limpieza de quebradas, alerta temprana y rutas de evacuación", 14, "construcción de diques y defensas ribereñas", "Intervenir el 100 % de quebradas y zonas críticas priorizadas al 2030"),
        P("ambiente", "«Más Verde para Cieneguilla»: nuevos parques, arborización con especies nativas, corredores verdes y riego tecnificado", 15, "Más Verde para Cieneguilla", "De 3,3 m² a 6 m² de áreas verdes por habitante al 2030"),
        P("gestion", "«Municipalidad Digital y Cercana»: expediente electrónico, mesa de partes virtual, aplicativo y atención itinerante en zonas altas", 15, "Municipalidad Digital y Cercana", "Digitalizar el 100 % de los trámites prioritarios al 2030"),
    ]),
    ("Edwin Subileti Areche", "Somos Perú", "partido-democratico-somos-peru", [
        P("social", "Construir un pabellón de aulas en cada colegio del distrito", 6, "1 pabellón, con 18 aulas por cada colegio", "1 pabellón con 18 aulas por colegio"),
        P("social", "Gestionar la construcción de un hospital y mejorar los puestos de salud del distrito", 6, "Gestionar la construcción, de un hospital"),
        P("social", "Crear dos locales Cuna Más y el Instituto de Desarrollo Neurológico Infantil", 6, "Instituto de Desarrollo Neurológico Infantil", "2 Cuna Más"),
        P("agua_riesgos", "Mejorar la calidad del agua potable en todas las zonas del distrito", 6, "Sistema de calidad del Agua Potable"),
        P("economia", "Circuito Turístico Gastronómico, Festival Internacional de Cieneguilla y promoción del caballo de paso", 7, "Circuito Turístico Gastronómico de Cieneguilla"),
        P("transporte", "Rehabilitar y mejorar los sectores críticos de las carreteras vecinales", 7, "Rehabilitación y el mejoramiento de sectores críticos de las carreteras vecinales"),
        P("urbano", "Crear el Parque Lineal Metropolitano en Cieneguilla", 7, "Creación del Parque Lineal Metropolitano"),
        P("ambiente", "Construir una planta de tratamiento de residuos sólidos y programas de forestación y reforestación", 8, "construcción de la Planta de Tratamiento de Residuos Sólidos"),
        P("seguridad", "Sistema integral de videocámaras y central de alerta interconectados con la Policía Nacional", 9, "instalación de videocámaras y una central de alerta"),
        P("seguridad", "Casetas de control con cámaras y personal las 24 horas en la entrada y salida del distrito, y una nueva comisaría", 9, "casetas de control en la entrada y salida del distrito"),
        P("gestion", "Presupuesto participativo y participación ciudadana en el Plan de Desarrollo Concertado", 9, "esquemas de presupuesto participativo"),
    ]),
    ("Ortensia La Torre Cervantes", "Podemos Perú", "podemos-peru", [
        P("seguridad", "Programa AVISPA: drones de vigilancia municipal y patrullaje aéreo contra la microcomercialización de drogas, integrado con la central de monitoreo y la PNP", 23, "Implementación progresiva de drones de vigilancia municipal", "Reducir en al menos 20 % los puntos de comercialización de drogas (2027-2030)"),
        P("social", "Espacios públicos neuroinclusivos en parques («Espacios que conectan») y zonas de calma en patios escolares", 15, "Espacios que conectan"),
        P("social", "Programa «Noviazgo sin Violencia» en escuelas para prevenir la violencia contra la mujer desde temprana edad", 16, "Noviazgo sin Violencia"),
        P("social", "Reabrir la Academia Municipal con preparación preuniversitaria, reforzamiento escolar y orientación vocacional", 18, "Reapertura y fortalecimiento de la Academia Municipal de Cieneguilla"),
        P("gestion", "Oficinas de atención y gestión municipal descentralizadas en lugares estratégicos del distrito", 23, "crearemos oficinas de atención y gestión municipal en lugares estratégicos", "Reducir en 40 % el tiempo de respuesta a los expedientes (2027-2030)"),
        P("social", "Construir el Centro Integral de Desarrollo Social y liberar la Casa de la Cultura para actividades educativas y juveniles", 24, "Centro Integral de Desarrollo Social de Cieneguilla"),
        P("urbano", "Recuperar zonas críticas del malecón del río Lurín como espacios de comercio, turismo y esparcimiento", 26, "La recuperación del malecón Lurín en zonas críticas"),
        P("economia", "«Cieneguilla Emprende»: capacitación, preincubación, ventanilla única de formalización y fondos concursables Procompite", 26, "Cieneguilla Emprende: Programa integral"),
        P("economia", "Programa de asistencia técnica para la agricultura familiar con extensionistas locales y convenios con el Midagri", 30, "Implementación del Programa de Asistencia Técnica para la Agricultura familiar"),
        P("transporte", "Regular los paseos en cuatrimotos: rutas autorizadas, registro de operadores, protocolos de seguridad y fiscalización", 28, "especialmente los paseos en cuatrimotos y vehículos todoterreno"),
        P("ambiente", "Contenedores subterráneos en puntos estratégicos y puntos verdes de acopio de reciclables y electrónicos", 33, "colocación de contendores subterráneos", "Ampliar al 100 % la cobertura adecuada de recolección de residuos (2027-2030)"),
    ]),
    ("William Ronald Salazar Mateo", "Renovación Popular", "renovacion-popular-peru", [
        P("social", "Programa «Vecinos Saludables»: establecimiento tipo Hospital de la Solidaridad con rayos X, ecografía y laboratorio, y botica municipal", 9, "Vecinos Saludables"),
        P("social", "Nuevos establecimientos de salud en el Primer Sector y Río Seco y campañas médicas para niños y adultos mayores", 9, "zonas como el Primer Sector y Río Seco"),
        P("social", "«Educación con Oportunidades para Todos»: becas municipales, academias preuniversitarias y aulas digitales", 10, "Educación con Oportunidades para Todos"),
        P("seguridad", "Cámaras con reconocimiento facial, lectores de placas, drones y botones de pánico conectados a la central de monitoreo y la comisaría", 10, "cámaras de video vigilancia con reconocimiento facial"),
        P("seguridad", "Escuela de Serenazgo, patrullaje integrado con la PNP, unidades con GPS y planes operativos «Plan Cerco» y «Plan Telaraña»", 10, "creación de una Escuela de Serenazgo"),
        P("economia", "«Marca Cieneguilla», rutas turísticas con el Qhapaq Ñan y sitios arqueológicos, y ferias gastronómicas y artesanales", 10, "Marca Cieneguilla"),
        P("transporte", "Ampliar los cuatro carriles de acceso al distrito con vías auxiliares y ciclovías, en coordinación con la Municipalidad de Lima", 11, "mejoramiento y ampliación de los cuatro carriles"),
        P("urbano", "Ordenamiento territorial con formalización de predios y regulación del crecimiento urbano", 11, "la formalización de predios y la regulación del crecimiento urbano"),
        P("ambiente", "Segregación en la fuente, puntos limpios, maquinaria para el recojo, plantas de reciclaje y compostaje para el vivero municipal", 11, "instalación de puntos limpios"),
        P("gestion", "Gobierno digital con automatización de trámites, aplicativos móviles y plataformas virtuales", 12, "automatización de trámites"),
        P("gestion", "Plataformas para seguir la gestión en tiempo real y canales anónimos para reportar actos indebidos", 12, "canales anónimos para reportar actos indebidos"),
    ]),
]
