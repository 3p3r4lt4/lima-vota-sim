"""San Isidro (150131): propuestas principales de los 9 planes de gobierno inscritos ante el JNE.

Cada propuesta está redactada con palabras propias y lleva:
  - pagina: la página del PDF oficial donde aparece.
  - ancla: un fragmento textual del PDF que DEBE aparecer en esa página. El generador lo verifica y
    falla si no lo encuentra, para que ninguna cita apunte a una página equivocada.
Mismo criterio para todas: entre 8 y 11 propuestas por plan, repartidas en los temas que el plan desarrolla.
"""

UBIGEO = "150131"

# Planes que no se resumen, con la razón que se muestra junto a la candidatura
NOTAS = {
    "avanza-pais-partido-de-integracion-social": "La organización no tiene un plan de gobierno publicado en Voto Informado del JNE, por lo que no hay propuestas que resumir.",
}

def P(tema, texto, pagina, ancla, meta=None):
    return {"tema": tema, "texto": texto, "meta": meta, "pagina": pagina, "ancla": ancla}

# (nombre, organización, archivo PDF, propuestas)
PLANES = [
    ("Carlomagno Chacón Gómez", "Acción Popular", "accion-popular", [
        P("seguridad", "Videovigilancia con analítica de IA (reconocimiento facial, lectura de placas, detección de armas) en todo el territorio distrital", 5, "sistema inteligente de videovigilancia con analítica de IA", "100 % del territorio monitoreado"),
        P("seguridad", "Más serenazgo distribuido en los 5 sectores, con patrullaje a pie mediante el programa «El sereno de tu parque»", 5, "Contar con 1,500 efectivos de serenazgo operativos", "1 500 efectivos de serenazgo"),
        P("social", "Polideportivo, piscina y gimnasio municipales para los sectores 4 y 5, con menor oferta deportiva", 7, "01 Polideportivo Municipal, 01 piscina municipal", "1 polideportivo, 1 piscina y 1 gimnasio"),
        P("urbano", "Programa «Bache Cero» de rehabilitación de pistas locales, con rampas y senderos podotáctiles en intersecciones residenciales", 7, "Bache Cero", "100 % de las pistas locales críticas rehabilitadas"),
        P("social", "Nuevas ambulancias de emergencia médica las 24 horas y una ambulancia para emergencias veterinarias", 8, "Adquisición de 02 nuevas ambulancias", "2 ambulancias nuevas (4 en total) y 1 ambulancia veterinaria"),
        P("economia", "Fiscalización del comercio ambulatorio con videovigilancia con IA y un escuadrón de drones", 9, "2 drones nuevos, para la fiscalización aérea", "100 % más intervenciones de fiscalización y 2 drones nuevos"),
        P("urbano", "Defender los parámetros urbanísticos de altura, zonificación y densidad, y reorganizar el servicio de fiscalización municipal", 10, "Defensa irrestricta de la residencialidad del distrito", "100 % de licencias que respeten los parámetros del distrito"),
        P("ambiente", "Corredores verdes, reforestación de zonas de calor urbano y riego tecnificado con aguas tratadas en El Olivar y parques principales", 12, "03 corredores verdes e infraestructuras peatonales", "3 corredores verdes"),
        P("transporte", "Ampliar el «Expreso San Isidro» con buses eléctricos y extender su horario", 13, "02 buses 100% eléctricos adquiridos", "2 buses eléctricos y horario hasta las 9:00 pm"),
        P("gestion", "Liquidaciones de predial y arbitrios prellenadas y una Billetera Digital Municipal con estados de cuenta, recibos y licencias", 15, "01 Billetera Digital Municipal creada", "100 % de liquidaciones prellenadas y 50 % más trámites en línea"),
        P("gestion", "Tablero público de datos abiertos sobre la inversión en seguridad, limpieza y áreas verdes, y audiencias «Tu Alcalde te escucha»", 16, "01 Dashboard Interactivo Público", "2 audiencias vecinales al mes como mínimo"),
    ]),
    ("Zuleika Vannessa Benel Zevallos", "Alianza para el Progreso", "alianza-para-el-progreso", [
        P("seguridad", "Programa «Escudo San Isidro»: videovigilancia, centro de monitoreo con IA, app de alertas, botón de emergencia y patrullaje integrado Serenazgo-PNP", 33, "Centro de monitoreo con inteligencia artificial", "30 % menos delitos de oportunidad y más de 85 % de percepción de seguridad"),
        P("social", "Proyecto «Sonrisa de Mujer»: centro de atención a la mujer con apoyo psicológico y legal, fondo semilla y bolsa de empleo", 17, "Centro Integral de Atención a la Mujer"),
        P("social", "Proyecto «Adulto Mayor Activo» con Casa Municipal del Adulto Mayor, acompañamiento domiciliario y red de voluntariado vecinal", 18, "Casa Municipal del Adulto Mayor"),
        P("social", "Programa «Huellitas por Siempre»: registro de mascotas con código QR, esterilización, veterinaria municipal y ambulancia veterinaria", 19, "Ambulancia Veterinaria de Emergencia"),
        P("gestion", "Gobierno digital con laboratorio de innovación pública, datos abiertos e inteligencia artificial aplicada a la gestión", 22, "Digitalizar el 100% de los trámites municipales", "100 % de trámites digitalizados al 2030"),
        P("economia", "Programa «Toca Mi Labor»: ferias temáticas itinerantes en parques y boulevares y sello «Hecho en San Isidro»", 23, "sistema permanente de ferias temáticas itinerantes"),
        P("economia", "«Laboratorio 360»: coworking municipal, laboratorio de fabricación digital y apoyo al primer negocio", 26, "Centro Municipal de Innovación, Tecnología, Emprendimiento y Primer Negocio"),
        P("transporte", "Movilidad sostenible, transporte compartido, infraestructura ciclista y gestión inteligente del tránsito", 33, "Reducir en 20% los tiempos promedio de desplazamiento interno", "20 % menos tiempo de desplazamiento interno"),
        P("ambiente", "«San Isidro Verde 365» con estándar único para los parques y control ecológico de roedores en El Olivar", 35, "44 parques modelo bajo un mismo estándar", "44 parques modelo"),
        P("urbano", "«San Isidro Ilumina 2030»: alumbrado LED con monitoreo remoto en calles, parques y malecones, y luminarias solares", 37, "Renovación total de luminarias convencionales por tecnología LED", "100 % del distrito con iluminación LED"),
        P("gestion", "Oficina de Alianzas y Cooperación Estratégica con bancos, embajadas, universidades y empresas para programas vecinales", 38, "Oficina de Alianzas y Cooperación Estratégica"),
    ]),
    ("César Augusto Combina Salvatierra", "Avanza País", "avanza-pais-partido-de-integracion-social", []),
    ("Víctor Hugo Bazán Pastor", "Somos Perú", "partido-democratico-somos-peru", [
        P("seguridad", "Videovigilancia inteligente en todo el distrito y un Centro Inteligente de Seguridad operativo las 24 horas", 29, "Implementar y mantener operativo un Centro Inteligente de Seguridad", "100 % del distrito con videovigilancia inteligente"),
        P("social", "Programa «Médico Municipal en Casa» y construcción de policlínicos municipales", 29, "Construir y poner en funcionamiento 2 Policlínicos Municipales", "2 policlínicos municipales"),
        P("social", "Construcción de polideportivos verticales", 29, "Construir 3 Polideportivos Verticales", "3 polideportivos verticales"),
        P("gestion", "App Vecino San Isidro con servicios integrados, gemelo digital del distrito e IA en la atención municipal", 30, "Digitalizar más del 80% de los trámites municipales", "Más del 80 % de trámites digitalizados"),
        P("economia", "Academia Municipal de Innovación y becas «San Isidro Global» con convenios internacionales", 30, "Capacitar a más de 8,000 vecinos durante la gestión", "Más de 8 000 vecinos capacitados"),
        P("social", "Gran Complejo Cultural Municipal con auditorio, Teatro Municipal y Casa de la Música", 30, "Construir un Auditorio para 2,000 personas", "Auditorio para 2 000 personas"),
        P("urbano", "Parque Costero San Isidro en la Costa Verde, con miradores, andenes paisajísticos y circuitos peatonales", 31, "Implementar el Parque Costero San Isidro"),
        P("transporte", "Estacionamientos inteligentes, red semafórica modernizada y ciclovías integradas con los distritos vecinos", 31, "Replantear e integrar las ciclovías con distritos vecinos"),
        P("ambiente", "Plantación de árboles y especies ornamentales, y riego inteligente en parques y jardines", 31, "Plantar 100,000 árboles y especies ornamentales", "100 000 árboles y especies ornamentales"),
        P("agua_riesgos", "Plantas de tratamiento de aguas residuales para reutilizar agua en riego, con sensores de humedad en áreas verdes", 31, "Construir dos Plantas de Tratamiento de Aguas Residuales", "2 PTAR"),
        P("ambiente", "Programa «Basura Cero» con biodigestores para residuos orgánicos y educación ambiental", 32, "Instalar biodigestores para el aprovechamiento de residuos orgánicos"),
    ]),
    ("César Enrique Stuart Alvarado", "PPC", "partido-popular-cristiano-ppc", [
        P("social", "Servicios de salud primaria para la población adulta mayor, que representa el 26 % del distrito", 1, "Brindar servicios de salud primaria", "75 % de la población atendida"),
        P("urbano", "Restringir los proyectos de vivienda de interés social (VIS) a sectores específicos del distrito", 1, "Restringir los proyectos de vivienda social a sectores especificos", "0 % de proyectos VIS fuera de zona"),
        P("seguridad", "Alinear la seguridad del distrito con las políticas estatales de seguridad ciudadana", 1, "Alineamiento a las politicias estatales de seguridad ciudadana", "Reducción en 50 % de la tasa de denuncias"),
        P("social", "Programas educativos con herramientas digitales, metodologías innovadoras y alianzas estratégicas", 1, "Fortalecer los programas educativos mediante innovación", "8 herramientas o metodologías y 10 000 participantes"),
        P("social", "Llevar actividades culturales a parques, plazas y otros espacios públicos de distintos sectores", 1, "Ampliar el acceso a actividades culturales", "120 actividades descentralizadas y 20 espacios públicos en el circuito cultural"),
        P("social", "Remodelación integral del centro cultural de la municipalidad", 1, "Remodelacion integral del centro cultural de la municipalidad", "100 % de la remodelación concluida"),
        P("economia", "Campañas de promoción de los atractivos culturales, históricos y naturales del distrito", 1, "Promover los atractivos culturales, históricos y naturales", "6 campañas de promoción por año"),
        P("transporte", "Reglamentar el uso de las veredas para que no circulen scooters ni bicicletas", 1, "Reglamentar uso de veredas", "Menos de 8 multas al mes por uso indebido de veredas"),
        P("ambiente", "Establecer y difundir horarios para fiestas en zonas residenciales, con control de decibeles", 1, "Establecer horarios y difundirlos entre los vecinos", "Menos de 4 multas al mes"),
        P("gestion", "Priorizar en el presupuesto las acciones que impacten en el bienestar del vecino", 1, "Priorizar acciones que impacten en el bienestar del ciudadano", "100 % de ejecución del presupuesto"),
        P("gestion", "Oficina de Cooperación al Desarrollo para gestionar recursos, alianzas y asistencia técnica", 1, "Implementar una Oficina de Cooperación al Desarrollo", "12 proyectos presentados y 15 convenios en el periodo"),
    ]),
    ("Charles Adrián Zapata Vega", "Podemos Perú", "podemos-peru", [
        P("seguridad", "Plan «Colibrí»: patrullaje aéreo con aeronave no tripulada con reconocimiento facial y de placas, y más serenos a pie", 9, "PATRULLAJE AEREO mediante el uso de una Aeronave No Tripulada"),
        P("seguridad", "Evaluación con polígrafo de todo el personal de seguridad ciudadana", 10, "Todo nuestro personal de seguridad ciudadana pasara por el polígrafo"),
        P("urbano", "Programa «SI Ilumina»: minicentrales solares para iluminar calles oscuras y parques, como en la Urb. Santa Cruz", 11, "Minicentrales solares fotovoltaica para iluminar calles oscuras"),
        P("social", "Servicios descentralizados a 15 minutos en cada sector: botica municipal, atención domiciliaria (PADOMI) y una ambulancia por sector", 12, "contara con una Botica municipal y un servicio de PADOMI"),
        P("social", "Clínica Digital Municipal con telemedicina y una historia clínica del vecino", 13, "primera HISTORIA CLINICA DEL VECINO"),
        P("transporte", "Cambiar a un solo sentido las calles colectoras que llegan a la Av. Javier Prado, hoy de doble sentido en su mayoría", 15, "iniciaremos un cambio sistemático de las calles en un solo sentido"),
        P("economia", "«Fondo San Isidro»: fideicomiso para que pequeños empresarios y startups del distrito accedan a nuevos mercados", 22, "dispondremos un fondo por fideicomiso"),
        P("agua_riesgos", "Planta desalinizadora de agua de mar con energía solar para regar parques y jardines, en lugar de cisternas desde Surco", 24, "Planta de desalinización de agua de mar mediante sistema Osmosis Inversa"),
        P("ambiente", "Planta recicladora que convierta plásticos en ladrillos para pistas, veredas y parques", 24, "reciclaremos nuestros plásticos y los convertiremos en ladrillos"),
        P("gestion", "Primer censo distrital sobre pobreza, edades, discapacidad, vehículos y mascotas, con la academia y las empresas", 25, "primer censo distrital que nos permitirá identificar"),
        P("gestion", "«Cero Colas / Cero Papel»: trámites TUPA automatizados, carpeta ciudadana y ficha única del vecino", 26, "cada vecino tendrá su propia Carpeta Ciudadana"),
    ]),
    ("Carla Meyling Peralta Hu", "Progresemos", "progresemos", [
        P("ambiente", "Nuevos parques y corredores verdes, e incentivos para techos verdes con exoneración de arbitrios", 17, "exoneración de arbitrios a cambio de techo ajardinado"),
        P("ambiente", "Plan de Arbolado Urbano con especies nativas, inventario anual, podas preventivas y reposición", 17, "Desarrollar un “Plan de Arbolado Urbano”", "1 000 árboles por año"),
        P("ambiente", "Programa distrital de reciclaje domiciliario con puntos de reciclaje y compostaje comunal de residuos de jardín", 17, "Lanzar un programa distrital de reciclaje domiciliario"),
        P("seguridad", "Ampliar el patrullaje integrado PNP–Serenazgo las 24 horas, con patrullas adicionales y rondas a pie en zonas críticas", 21, "asignar 2 patrullas adicionales", "2 patrullas adicionales"),
        P("seguridad", "Capacitar y aumentar el serenazgo, con turnos nocturnos especializados", 21, "objetivo +20% de agentes", "20 % más agentes"),
        P("seguridad", "Cámaras de alta definición en avenidas, cruces y parques integradas con la PNP, y botones de pánico", 22, "Colocar ~100 cámaras de alta definición", "Unas 100 cámaras"),
        P("urbano", "Renovar el alumbrado con LED en vías secundarias y parques tras mapear las zonas oscuras", 22, "Mapeo de zonas oscuras y ejecución rápida de mejoras"),
        P("gestion", "Ampliar el presupuesto participativo e incluir a jóvenes de 18 a 30 años en los comités de priorización", 26, "Aumentar el presupuesto destinado del 1% al 2%", "Del 1 % al 2 % del presupuesto municipal"),
        P("gestion", "Plataforma digital de participación con votación electrónica de proyectos, foros y audiencias virtuales", 26, "capacidad de votación electrónica para proyectos"),
        P("social", "Parques caninos y campañas gratuitas anuales de vacunación antirrábica y antiparasitaria", 26, "Construir y adecuar mínimo 3 parques caninos", "Al menos 3 parques caninos y cobertura de vacunación de 95 % o más"),
        P("social", "Talleres intergeneracionales que reúnan a niños y adultos mayores", 26, "Proponemos unos 50 talleres anuales", "50 talleres al año y 5 000 beneficiarios en 2027–2030"),
    ]),
    ("Javier Eduardo Paino Scarpati", "Renovación Popular", "renovacion-popular-peru", [
        P("seguridad", "Ampliar la videovigilancia con cámaras con IA que identifiquen rostros y placas vehiculares", 33, "contará con un mínimo de 1,500 cámaras de video vigilancia", "1 500 cámaras, 500 de ellas con IA, al 2030"),
        P("seguridad", "Ampliar el patrullaje integrado del Serenazgo con la Policía Nacional", 33, "mínimo de 200 efectivos policiales para el patrullaje integrado", "200 efectivos policiales al 2030"),
        P("social", "Programas de vida saludable e inclusión para adultos mayores y más especialidades en el centro médico municipal", 33, "aumentar el número de atenciones médicas en un 40%", "40 % más atenciones médicas"),
        P("social", "Servicios, espacios y programas accesibles para personas con discapacidad", 33, "duplicar el número de personas con discapacidad debidamente empadronada", "Duplicar las personas con discapacidad empadronadas al 2030"),
        P("economia", "Ferias itinerantes por sectores para las micro y pequeñas empresas locales", 33, "Realización de 12 ferias itinerantes al año", "12 ferias al año con 40 a 60 emprendedores cada una"),
        P("economia", "Inversiones con participación privada (Obras por Impuestos, APP) para cerrar brechas de infraestructura", 33, "Ejecutar al menos 4 inversiones mediante mecanismos", "Al menos 4 inversiones durante la gestión"),
        P("ambiente", "Arborización con especies nativas para aumentar la cobertura arbórea del distrito", 24, "INCREMENTAR EL ARBOLADO DISTRITAL HASTA 36,461", "36 461 árboles en el distrito al 2030"),
        P("agua_riesgos", "Riego tecnificado de áreas verdes para reducir la vulnerabilidad ante el estrés hídrico", 34, "Porcentaje de áreas verdes regadas con sistema de riego tecnificado", "50 % de las áreas verdes"),
        P("ambiente", "Monitoreo del ruido con IA y sensibilización a conductores en los puntos críticos de contaminación sonora", 34, "Reducir la cantidad a 31 puntos críticos", "Reducir a 31 los puntos críticos del mapa de ruido"),
        P("gestion", "Plataforma Integral de Inteligencia Municipal que integre datos de seguridad, limpieza, tránsito y fiscalización", 34, "Integrar el 100% de los sistemas estratégicos municipales", "100 % de los sistemas estratégicos integrados"),
        P("gestion", "Digitalizar los procedimientos TUPA con expediente electrónico, firma digital y pagos virtuales", 34, "Digitalizar el 100% de los procedimientos TUPA", "100 % de procedimientos TUPA viables y 50 % más atenciones digitales"),
    ]),
    ("Rigan Edward Valcárcel Salinas", "Visión Perú", "vision-peru", [
        P("seguridad", "Plataforma «SafeCity-SI»: centro de operaciones con IA predictiva, 100 cámaras adicionales y patrullaje según mapas de calor", 6, "Implementar la Plataforma SafeCity-SI", "40 % menos ocurrencias delictivas y respuesta en menos de 4 minutos al 2030"),
        P("social", "Modelo «San Isidro Envejece Bien»: gestor de caso para mayores de 80 años, telesalud y CEV abiertos los sábados", 7, "Asignar un gestor de caso a las 4,420 personas", "40 % de cobertura de mayores de 65 años (5 440 personas)"),
        P("social", "Programa «San Isidro Activo y Saludable» con actividad física por grupo de edad en parques y el gimnasio municipal", 8, "20,000 usuarios/año al 2030", "20 000 usuarios al año al 2030"),
        P("social", "Programa «San Isidro Pet-Friendly»: registro de mascotas con microchip, zonas caninas por sector y jornadas gratuitas de esterilización", 9, "Registro Único de Animales de Compañía (RUAC)", "7 000 o más mascotas registradas y 5 zonas caninas"),
        P("transporte", "Plan de Movilidad Sostenible, nuevos tramos de ciclovía protegida y sensores de estacionamiento con app", 10, "construcción de 6 km nuevos de ciclovía protegida", "30 % menos incidencias viales y 6 km nuevos de ciclovía"),
        P("economia", "Licencias de funcionamiento con análisis de riesgo automatizado, firma digital y expediente electrónico", 11, "máximo 3 días hábiles al 2028", "Licencias en un máximo de 3 días hábiles al 2028"),
        P("ambiente", "Relanzar «Recicla San Isidro» con separación en origen por edificio, eco-puntos y beneficios tributarios", 12, "Instalar 10 eco-puntos tecnológicos", "30 % menos residuos al relleno sanitario al 2030"),
        P("agua_riesgos", "Programa «Smart Green SI»: sensores de humedad, riego por goteo inteligente y Plan de Resiliencia Hídrica", 13, "Conversión del 30% de sistemas de riego a goteo inteligente", "35 % menos agua de riego y 600 000 m² con riego inteligente"),
        P("urbano", "Actualizar la norma de edificación sostenible y rebajar tasas de licencia a proyectos con certificación LEED/EDGE", 13, "reducción del 20% en tasas de licencia", "50 % de nuevas licencias con criterios sostenibles al 2030"),
        P("gestion", "Municipalidad «Trámite Cero»: plataformas informáticas integradas, cero papel y acompañamiento digital a adultos mayores", 14, "trámites 100% digitales al 2029", "100 % de trámites digitales al 2029"),
        P("gestion", "Presupuesto participativo digital decidido por vecinos registrados e informe trimestral de gestión", 15, "presupuesto participativo digital de S/ 5 millones anuales", "S/ 5 millones anuales"),
    ]),
]
