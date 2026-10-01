"""Miraflores (150122): propuestas principales de los planes de gobierno inscritos ante el JNE.

Cada propuesta está redactada con palabras propias y lleva:
  - pagina: la página del PDF oficial donde aparece.
  - ancla: un fragmento textual del PDF que DEBE aparecer en esa página. El generador lo verifica y
    falla si no lo encuentra, para que ninguna cita apunte a una página equivocada.
Mismo criterio para todas: entre 8 y 11 propuestas por plan, repartidas en los temas que el plan desarrolla.
"""

UBIGEO = "150122"

def P(tema, texto, pagina, ancla, meta=None):
    return {"tema": tema, "texto": texto, "meta": meta, "pagina": pagina, "ancla": ancla}

# (nombre, organización, archivo PDF, propuestas)
PLANES = [
    ("Carlos Alcides Zúñiga Arce", "Acción Popular", "accion-popular", [
        P("seguridad", "Escuela de Serenos, más serenos, renovación de la flota y drones; comité distrital de seguridad semanal liderado por el alcalde", 19, "Escuela de Serenos de Miraflores creada", "Escuela de Serenos desde el primer año y 20 % más serenos"),
        P("agua_riesgos", "Almacenes soterrados de ayuda humanitaria, una brigada comunal por zona, centro de operaciones de emergencia y sala de crisis conectados con Lima e INDECI", 23, "14 Nuevos Almacenes Soterrados de Ayuda Humanitaria", "14 almacenes soterrados nuevos y 14 brigadas comunales, una por zona"),
        P("transporte", "Bus vecinal ecológico con dos rutas, nuevas ciclovías conectadas a la red metropolitana y estaciones de bicicletas en parques y óvalos", 28, "Rutas del Sistema de Transporte Vecinal Ecológico", "2 rutas de bus vecinal ecológico y 9 km de nuevas ciclovías"),
        P("transporte", "Reordenar intersecciones eliminando giros a la izquierda, centralizar los semáforos con la MML y construir un puente peatonal y ciclista hacia Barranco", 28, "Puente Peatonal y Ciclista de Interconexión Miraflores - Barranco", "30 intersecciones reordenadas y 100 % de la red semafórica conectada a la central de la MML"),
        P("social", "Farmacia municipal con medicamentos básicos a precio de costo, centro de salud mental comunitario y plataforma de telemedicina", 35, "Centro de Salud Mental Comunitario (CSMC) instalado", "1 farmacia municipal y 1 centro de salud mental comunitario operativos"),
        P("social", "Programa «Salud en tu Barrio»: campañas gratuitas de despistaje y prevención en las 14 zonas del distrito, con clínicas privadas y servicios públicos", 35, "28 Campañas Macro de Salud Preventiva", "28 campañas gratuitas al año (2 por cada una de las 14 zonas)"),
        P("economia", "Incubadora de negocios «Miraflores Innova», licencias digitalizadas y bolsa de trabajo inteligente que conecta a vecinos con empresas del distrito", 56, "inserción formal de un mínimo de 3,000 vecinos", "Al menos 3 000 vecinos insertados en empleos formales al 2030"),
        P("urbano", "Red de baños públicos inteligentes y accesibles, y uso temporal de lotes en desuso como huertos, parklets o zonas de descanso", 62, "BAÑOS PÚBLICOS INTELIGENTES"),
        P("ambiente", "Riego tecnificado en más parques, inventario digital del arbolado y programa vecinal de siembra «Árboles para Miraflores»", 71, "Trece (13) parques adicionales implementados con sistema de riego tecnificado", "13 parques más con riego tecnificado"),
        P("ambiente", "Ordenanza de segregación obligatoria en edificios, recojo selectivo en todo el distrito y recolección de aparatos electrónicos y aceite usado", 74, "el 90% de las juntas de propietarios", "Segregación en la fuente en el 100 % de comercios y el 90 % de edificios multifamiliares"),
        P("gestion", "Audiencias vecinales «Gobernando con el Vecino», rendición de cuentas anual y un visor web del avance del plan de gobierno", 76, "Cincuenta (50) Audiencias Vecinales", "50 audiencias vecinales al año y 4 rendiciones de cuentas en la gestión"),
    ]),
    ("Ricardo Enrique Giesecke Sara Lafosse", "Ahora Nación", "ahora-nacion-an", [
        P("seguridad", "Fortalecer el serenazgo con más cámaras, programas preventivos en colegios y una Casa de las Familias para atención emocional", 5, "Incrementar en 30% el número de cámaras de videovigilancia", "30 % más cámaras operativas y 20 % menos percepción de inseguridad"),
        P("social", "Unidades de serenazgo especializadas en violencia de género, campañas educativas y asesoría legal y psicológica", 5, "Reducir en 20% los reportes de acoso callejero", "20 % menos reportes de acoso callejero en zonas críticas"),
        P("social", "Programa de Renacimiento Cultural con circuitos turísticos y artísticos, Casa del Artista y recuperación del Estadio Bonilla", 5, "Recuperar integralmente el Estadio Bonilla", "Estadio Bonilla recuperado antes de terminar el segundo año y al menos 5 circuitos turísticos y culturales"),
        P("social", "Guardería municipal con horarios adaptados a las familias, en especial a las mujeres que trabajan", 6, "Beneficiar a por lo menos 500 familias por año", "Guardería en el primer año, para al menos 500 familias al año"),
        P("transporte", "Semaforización inteligente, más fiscalización del tránsito, ampliación de ciclovías y una ruta especial del Urbanito", 5, "Implementar 34 intersecciones con semaforización inteligente", "34 intersecciones con semáforos inteligentes, 15 km de ciclovías y 25 % menos tiempo de desplazamiento"),
        P("urbano", "Ascensores y accesos peatonales seguros desde el malecón hacia las playas para adultos mayores y personas con discapacidad", 5, "Construir al menos 3 sistemas de acceso vertical", "Al menos 3 sistemas de acceso vertical a las playas"),
        P("ambiente", "Normativa para preservar áreas verdes en nuevas edificaciones y recuperación de espacios residuales con arborización", 5, "Plantar 5,000 árboles y especies ornamentales", "10 % más áreas verdes y 5 000 árboles plantados"),
        P("ambiente", "Modernizar la gestión de residuos con reciclaje, segregación en origen y recolección selectiva", 6, "Incrementar en 50% la tasa de reciclaje distrital", "50 % más reciclaje y recolección selectiva en el 100 % de sectores"),
        P("ambiente", "Servicio veterinario municipal con vacunación, esterilización y adopción responsable", 6, "Realizar 20,000 vacunaciones durante la gestión", "20 000 vacunaciones y 10 000 esterilizaciones en la gestión"),
        P("gestion", "Vigilancia ciudadana, acceso a la información y cabildos abiertos semestrales", 5, "Realizar 2 Cabildos Abiertos por año", "2 cabildos abiertos al año y ejecución presupuestal publicada cada trimestre"),
        P("gestion", "Gobierno electrónico para digitalizar trámites y reducir tiempos de atención", 6, "Digitalizar el 100% de los principales trámites municipales", "100 % de los principales trámites digitalizados y 50 % menos tiempo de atención"),
    ]),
    ("Jorge Vicente Martín Muñoz Wells", "Avanza País", "avanza-pais-partido-de-integracion-social", [
        P("seguridad", "Seguridad integral basada en información: patrullaje y monitoreo permanentes en sectores priorizados y sistema integrado de vigilancia en zonas críticas", 7, "Reducir en 25% el tiempo promedio de respuesta", "25 % menos tiempo de respuesta y patrullaje permanente en el 100 % de sectores priorizados"),
        P("social", "Programas permanentes de actividad física y deporte en parques, malecones y losas deportivas para todas las edades", 9, "Beneficiar a más de 30,000 vecinos mediante programas municipales de actividad física", "Más de 30 000 vecinos en programas de actividad física y deporte"),
        P("social", "Mejor iluminación y seguridad en zonas priorizadas, prevención del acoso y programas de capacitación y empleo para mujeres", 17, "Beneficiar a 3,000 mujeres mediante programas de capacitación", "3 000 mujeres en programas de capacitación y empleo; 25 % más percepción de seguridad de las mujeres"),
        P("urbano", "Recuperar y poner en valor parques, plazas, malecones y áreas recreativas con accesibilidad universal", 10, "Recuperar, renovar o poner en valor al menos 100 espacios públicos", "Al menos 100 espacios públicos recuperados"),
        P("transporte", "Proyectos de movilidad sostenible y caminabilidad, y campañas de educación vial", 12, "Reducir en 30% los puntos críticos de congestión", "30 % menos puntos críticos de congestión y al menos 30 proyectos de movilidad sostenible"),
        P("economia", "Capacitación, mentoría y espacios de innovación o coworking para emprendedores del distrito", 27, "Beneficiar a más de 3000 emprendedores", "Más de 3 000 emprendedores capacitados y al menos 5 espacios de innovación o coworking"),
        P("ambiente", "Ampliar el arbolado y aplicar riego eficiente en las áreas verdes priorizadas", 31, "Incrementar en 20% la cobertura arbórea distrital", "20 % más cobertura arbórea y riego eficiente en el 100 % de áreas verdes priorizadas"),
        P("ambiente", "Ampliar el reciclaje y la valorización de residuos con educación ambiental para vecinos y comercios", 32, "Incrementar en 50% el volumen de residuos valorizados", "50 % más residuos valorizados o reciclados respecto a 2026"),
        P("agua_riesgos", "Simulacros y ejercicios de preparación ciudadana ante emergencias e intervenciones preventivas para reducir riesgos", 44, "Desarrollar al menos 40 simulacros", "Al menos 40 simulacros y ejercicios de preparación al año"),
        P("gestion", "Digitalizar trámites y servicios municipales priorizados", 37, "Digitalizar al menos el 90% de los trámites y servicios municipales priorizados", "90 % de trámites priorizados digitales y 50 % menos tiempo de atención"),
        P("gestion", "Espacios de diálogo y rendición de cuentas con vecinos y organizaciones", 41, "Realizar al menos 20 espacios de diálogo y rendición de cuentas por año", "20 espacios de diálogo y rendición de cuentas al año"),
    ]),
    ("Daniel Rodríguez Zanabria", "Libertad Popular", "libertad-popular", [
        P("seguridad", "Corredores de alta vigilancia en Larco, Kennedy, Pardo, Costa Verde y zonas turísticas, con patrullaje integrado de serenazgo, PNP y juntas vecinales", 49, "Implementación de corredores de alta vigilancia", "100 % de zonas turísticas protegidas"),
        P("social", "Campañas preventivas de salud «Miraflores Saludable» y atención domiciliaria «Médico en Casa» para adultos mayores y personas con movilidad reducida", 28, "Meta 2030: 5,000 visitas domiciliarias anuales", "5 000 visitas domiciliarias al año y 40 000 atenciones preventivas acumuladas"),
        P("social", "Servicio municipal de salud mental «Miraflores Te Escucha», presencial, telefónico y virtual", 28, "Miraflores Te Escucha", "20 000 atenciones psicológicas acumuladas"),
        P("transporte", "Plan Maestro de Movilidad 2030 y semaforización inteligente con sensores y monitoreo en tiempo real", 39, "Reducción del 25% del tiempo promedio de desplazamiento", "25 % menos tiempo de desplazamiento y 100 % de intersecciones principales monitoreadas"),
        P("transporte", "Red de estacionamientos subterráneos, automatizados o concesionados en Kennedy, Larco, Pardo y el sector turístico", 40, "Meta 1,500 nuevas plazas de estacionamiento", "1 500 nuevas plazas de estacionamiento"),
        P("urbano", "Plan «Cero Huecos» de pavimentación, bacheo y mantenimiento preventivo de vías", 40, "Plan Cero Huecos Programa permanente", "100 % de vías principales en estado óptimo"),
        P("agua_riesgos", "Protección de acantilados de la Costa Verde con monitoreo geotécnico, estabilización de taludes y drenajes", 41, "Protección Integral de Acantilados", "100 % de zonas críticas monitoreadas"),
        P("economia", "Ventanilla rápida «Formaliza Miraflores» con licencia digital, inspección programada y asesoría a emprendedores", 34, "Formaliza Miraflores", "50 % menos tiempo en trámites empresariales"),
        P("economia", "Programa «Empleo Joven Turismo»: capacitación en atención turística, inglés, marketing digital y gastronomía", 35, "Meta 2030: 4,000 jóvenes capacitados", "4 000 jóvenes capacitados"),
        P("ambiente", "Programa «Basura Cero» con segregación, reciclaje, planta de reciclaje y contenedores inteligentes en zonas turísticas", 44, "Basura Cero Miraflores", "Duplicar la tasa de reciclaje y contenedores inteligentes en el 100 % de zonas turísticas"),
        P("gestion", "Municipalidad digital: licencias, certificados, pagos y expedientes en línea, con expediente electrónico único", 51, "Municipalidad Digital 100%", "90 % de trámites digitales"),
    ]),
    ("José Ricardo Portugal Quiroz", "Partido del Buen Gobierno", "partido-del-buen-gobierno", [
        P("seguridad", "Cinco módulos de seguridad descentralizados, cámaras con analítica de video conectadas por fibra óptica y drones de vigilancia", 5, "163 cámaras fijas de alta definición", "5 módulos y 163 cámaras operativos; respuesta ante emergencias en menos de 3 minutos"),
        P("urbano", "Ampliar el alumbrado público en todo el distrito mediante inversión pública", 5, "servicio de iluminación en el distrito de Miraflores", "100 % del distrito iluminado al 2030"),
        P("social", "Policonsultorios municipales descentralizados en las casas del adulto mayor, con telesalud, laboratorio básico y atención psicológica", 6, "Implementación de Centros Médicos Municipales Preventivos"),
        P("social", "Flota municipal de ambulancias tipo II y III con geolocalización, en convenio con el SAMU", 6, "flota de ambulancias tipo II y III", "Respuesta médica prehospitalaria en menos de 5 minutos"),
        P("economia", "Licenciamiento y formalización comercial digitalizados, con apoyo a micro y pequeñas empresas", 12, "más de 3,000 nuevos microemprendimientos", "Licencias en máximo 24 horas y más de 3 000 microemprendimientos formalizados"),
        P("economia", "Bolsa de trabajo municipal conectada con empresas aliadas para empleo y prácticas de jóvenes", 14, "más de 2,500 jóvenes en puestos profesionales", "Más de 2 500 jóvenes insertados en empleos o prácticas"),
        P("transporte", "Catastro digital conectado con fiscalización y control de tránsito, y parqueo regulado para frenar el estacionamiento informal", 16, "erradicando por completo el estacionamiento informal en zonas rígidas residenciales", "Catastro digital al 100 % y cero estacionamiento informal en zonas rígidas residenciales"),
        P("ambiente", "Planta municipal de valorización y compostaje, y estaciones de reciclaje inteligentes en parques y zonas turísticas", 17, "Planta Municipal de Valorización y Compostaje Automatizado", "100 % de residuos aprovechables reciclados o valorizados"),
        P("ambiente", "Sensores de ruido en ejes saturados, retiro de cables aéreos en desuso y regulación de paneles publicitarios", 19, "sensores IoT de medición de ruido", "100 % de puntos críticos con monitoreo de ruido y sin cableado aéreo en desuso en avenidas principales"),
        P("ambiente", "Nueva veterinaria municipal, registro de mascotas con microchip y zonas exclusivas para mascotas en parques", 11, "nueva Veterinaria Municipal", "Veterinaria operativa y registro de todas las mascotas residentes"),
        P("gestion", "Ventanilla única digital de trámites y canal de denuncias anónimas en convenio con la PCM", 22, "Canal Seguro de Denuncias Anónimas", "100 % de trámites y servicios municipales automatizados"),
    ]),
    ("Alexander Enrique Von Ehren Campos", "Somos Perú", "partido-democratico-somos-peru", [
        P("seguridad", "Reforzar el patrullaje integrado de serenazgo y PNP, modernizar las cámaras y activar comités vecinales de seguridad", 5, "Incremento en 30% del patrullaje integrado", "30 % más patrullaje integrado y 30 % menos delitos al cierre de la gestión"),
        P("seguridad", "Personal operativo en colegios, centros comerciales y parques con mayor afluencia", 4, "Implementar personal operativo en áreas de confluencia vecinal"),
        P("urbano", "Plan de mantenimiento y rehabilitación de pistas y veredas, y mejor iluminación en puntos críticos", 5, "Atender el 90% de las calles y avenidas en mal estado", "90 % de calles y avenidas en mal estado atendidas"),
        P("urbano", "Recuperar y crear espacios públicos con mejor mobiliario, iluminación y seguridad para actividades vecinales", 7, "Activar al menos cinco espacios más en el distrito"),
        P("social", "Agenda permanente de actividades culturales, deportivas y recreativas, con talleres y festivales descentralizados en las 14 zonas", 6, "al menos cuatro actividades semanales"),
        P("transporte", "Reordenar el tránsito, revisar semáforos, señalización y zonas de carga, y fijar puntos de embarque en zonas turísticas", 6, "Reducir en 20% el tiempo promedio de circulación", "20 % menos tiempo de circulación en las vías más congestionadas y 20 % más vías de movilidad sostenible"),
        P("economia", "Mesas de trabajo con comercios y vecinos, y simplificación de trámites municipales", 7, "Agilizar en un 30% la atención de los trámites municipales", "30 % más rapidez en la atención de trámites"),
        P("ambiente", "Mantenimiento integral de parques: bancas, juegos infantiles, riego, poda y tratamiento fitosanitario", 8, "Mejorar el riego, la poda, y el tratamiento fitosanitario"),
        P("ambiente", "Campañas de reciclaje vecinal y escolar, jornadas de limpieza y arborización, y premios a buenas prácticas", 9, "Ejecución de campañas bimensuales", "Campañas bimensuales"),
        P("gestion", "Difundir el gasto, realizar audiencias públicas de balance y crear canales de denuncia de corrupción", 9, "Realizar reportes bimensuales", "Reportes bimensuales y audiencias públicas periódicas"),
        P("gestion", "Intervención obligatoria de delegados vecinales en el Concejo y mejor presupuesto participativo", 9, "intervenciones de los delegados vecinales de forma obligatoria"),
    ]),
    ("Mario Renato Otiniano Buquich", "Partido Morado", "partido-morado", [
        P("seguridad", "Serenazgo modernizado con drones, inteligencia artificial y cámaras particulares integradas, en coordinación con PNP, Fiscalía y juntas vecinales", 11, "Reducir en 20% la percepción de inseguridad", "20 % menos percepción de inseguridad y cobertura del 100 % de zonas identificadas"),
        P("transporte", "Rutas internas gratuitas con buses eléctricos accesibles, geolocalizados e integrados con ciclovías y corredores metropolitanos", 20, "Adquisición de buses eléctricos", "4 buses eléctricos y más de 1 millón de viajes acumulados"),
        P("social", "Tamizajes, actividad física y voluntariado para adultos mayores con la red de atención preventiva", 14, "Tamizar al 50% de la población adulta mayor", "Tamizaje al 50 % de los adultos mayores y 20 % menos sedentarismo"),
        P("social", "Renovar las bibliotecas de los CIAM con nuevos títulos, clubes de lectura y el programa «Abuelos Cuentacuentos»", 15, "Renovación integral de bibliotecas CIAM", "100 % de bibliotecas CIAM renovadas y 5 000 libros físicos y digitales"),
        P("agua_riesgos", "Gestión del riesgo con almacenes estratégicos, capacitación por zonas vecinales y simulacros masivos", 38, "Realizar al menos 4 simulacros masivos anuales", "Al menos 4 simulacros masivos al año y 20 000 vecinos capacitados"),
        P("urbano", "Programa «Veredas Inclusivas» con rampas, pisos podotáctiles e intersecciones más seguras para peatones", 45, "Construir 45 km de infraestructura peatonal accesible", "45 km de infraestructura peatonal accesible"),
        P("urbano", "Concurso internacional para modernizar el Complejo Deportivo Manuel Bonilla con un parque costero sobre las instalaciones deportivas", 56, "Consolidación de 20,000 m² de parque costero", "Concurso de diseño en 2027 y obra entregada al 2030 con 20 000 m² de parque costero"),
        P("ambiente", "Microbosques urbanos Miyawaki y reforestación de áreas críticas", 52, "Instalar 50 micro bosques urbanos", "Cobertura arbórea del 18 % al 35 % y 50 microbosques"),
        P("ambiente", "Limpieza pública con rutas monitoreadas por GPS y nuevas barredoras y compactadoras", 44, "12 nuevas barredoras. 8 nuevas compactadoras", "12 barredoras y 8 compactadoras nuevas; 100 % de rutas con GPS"),
        P("economia", "Ferias de emprendedores ordenadas y descentralizadas, censo y red de comerciantes, y licencias nuevas 100 % digitales", 74, "Censo de emprendedores miraflorinos", "2 ferias al mes en cada espacio y censo de emprendedores en el primer año"),
        P("gestion", "Modernización tributaria con trámites virtuales y Cuenta Única Municipal para cada contribuyente", 60, "80% de trámites virtuales", "80 % de trámites tributarios virtuales y Cuenta Única Municipal para el 100 % de contribuyentes"),
    ]),
    ("María Soledad Ferreyros Castañeda", "PPC", "partido-popular-cristiano-ppc", [
        P("seguridad", "Proyecto «Smart City Miraflores»: cámaras con inteligencia artificial, reconocimiento de placas y biometría integradas con la Central 105 de la PNP", 1, "Smart City Miraflores", "50 % menos delitos contra el patrimonio, 100 % de cámaras operativas (70 % con IA) y respuesta en 5 minutos o menos"),
        P("seguridad", "Plan Cuadrante con operativos permanentes, pórticos inteligentes, botón de pánico, drones y programa escolar «Mi Cole seguro»", 1, "Mi Cole seguro", "40 % menos percepción de inseguridad y 30 % más serenos operativos"),
        P("transporte", "Semaforización inteligente, señalización, rediseño de cruces peatonales y red de ciclovías seguras", 2, "Implementar 20 intersecciones semaforizadas", "20 intersecciones con semáforos inteligentes, 9 km más de ciclovías y 30 % menos tiempo de viaje en hora punta"),
        P("transporte", "Circuitos de buses eléctricos gratuitos y estacionamientos rotativos y de carga y descarga", 2, "circuitos de buses eléctricos gratuitos en el distrito", "3 circuitos de buses eléctricos gratuitos"),
        P("agua_riesgos", "Alerta temprana ante sismos y tsunamis, almacenes soterrados equipados, brigadas vecinales y mejores salidas de evacuación de la Costa Verde", 3, "sistema de alerta temprana para sismos y tsunamis", "100 % de almacenes soterrados equipados y 60 % de accesos de la Costa Verde adaptados para evacuación"),
        P("social", "Programa PADOMI Municipal de atención a adultos mayores y más campañas de salud preventiva y mental", 3, "PADOMI Municipal", "Al menos el 80 % de los adultos mayores identificados en el programa"),
        P("social", "Recuperar el Complejo Deportivo Manuel Bonilla, construir un gimnasio municipal y mejorar el skate park de la Costa Verde", 4, "Recuperar el Complejo Deportivo Manuel Bonilla", "40 % más capacidad de la infraestructura deportiva municipal"),
        P("economia", "Licencias de funcionamiento rápidas, fiscalización preventiva, ferias de emprendimiento y bolsa de trabajo con empresas", 6, "Simplificar el trámite de licencias de funcionamiento", "Reducir en 3 puntos porcentuales la tasa de desempleo"),
        P("ambiente", "Arborización, segregación en la fuente, compostaje y contenedores soterrados en puntos críticos", 7, "Implementar contenedores soterrados en los puntos críticos", "15 m² de área verde por habitante y 40 % más vecinos que segregan en la fuente"),
        P("urbano", "Mejoramiento de pistas y veredas con cronograma informado a los vecinos, recuperación de parques y piscina temperada municipal", 8, "piscina temperada", "80 % más pistas y veredas reparadas y parques recuperados"),
        P("gestion", "Sistema antisoborno ISO 37001, trámites digitales y atención multicanal, y reuniones semanales «El alcalde te escucha»", 9, "Sistema de Gestión Antisoborno", "90 % más trámites con atención multicanal"),
    ]),
    ("Amílcar Alessio Cantella Vega", "Renovación Popular", "renovacion-popular-peru", [
        P("seguridad", "Escuela de Serenos para seleccionar y formar al personal, y más serenos en el distrito", 21, "Incrementar número de serenos"),
        P("seguridad", "Centro Inteligente de Seguridad Distrital con análisis predictivo, que integre cámaras de comercios y la participación de vigilantes y conserjes", 23, "Centro Inteligente de Seguridad Distrital"),
        P("agua_riesgos", "Almacenes de emergencia soterrados y en contenedores con víveres, agua y herramientas para las primeras 72 horas", 26, "Almacenes de Emergencia Soterrados", "Al menos un almacén por sector y distribución inicial de ayuda en menos de 1 hora"),
        P("social", "Policlínico municipal con medicina general, geriatría, pediatría, psicología y laboratorio básico", 27, "Creación del Policlínico Municipal"),
        P("social", "Ambulancias tipo II con geolocalización articuladas con serenazgo, bomberos y PNP, y telemedicina para adultos mayores", 29, "Servicio de emergencia de ambulancias Tipo II"),
        P("transporte", "Centro de gestión inteligente del tránsito con semaforización adaptativa, cámaras y sensores", 30, "Centro de Gestión Inteligente de Tránsito"),
        P("urbano", "Alumbrado LED inteligente con monitoreo remoto en avenidas, calles y el circuito de playas", 51, "Iluminación led e inteligente de avenidas"),
        P("economia", "Centro municipal de formación y emprendimiento, becas educativas y bolsa de trabajo", 54, "Centro de Formación y Emprendimiento Municipal"),
        P("economia", "Consolidar el eje Larco–Kennedy como corredor turístico e integrar el circuito de playas con la ciudad", 69, "Generar experiencias turísticas permanentes cada 100 metros", "Experiencias turísticas permanentes cada 100 metros del recorrido"),
        P("ambiente", "Modernizar los sistemas de riego de parques, bermas y jardines, y programa de segregación de residuos", 58, "Mejoramiento de los sistemas de riego de las áreas verdes"),
        P("gestion", "Aplicación móvil única con todos los servicios municipales y eliminación progresiva del expediente físico", 39, "Eliminar progresivamente expedientes físicos"),
    ]),
]
