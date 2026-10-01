"""Surquillo (150141): propuestas principales de los 9 planes de gobierno inscritos ante el JNE.

Cada propuesta está redactada con palabras propias y lleva:
  - pagina: la página del PDF oficial donde aparece.
  - ancla: un fragmento textual del PDF que DEBE aparecer en esa página. El generador lo verifica y
    falla si no lo encuentra, para que ninguna cita apunte a una página equivocada.
Mismo criterio para todas: entre 8 y 11 propuestas por plan, repartidas en los temas que el plan desarrolla.
Fuente de los PDF y metadatos: scripts/planes/150141/manifiesto.json (descargados del JNE el 30/09/2026).
"""

UBIGEO = "150141"

def P(tema, texto, pagina, ancla, meta=None):
    return {"tema": tema, "texto": texto, "meta": meta, "pagina": pagina, "ancla": ancla}

# (nombre, organización, archivo PDF, propuestas)
PLANES = [
    ("Phil Dempster Barriga Vásquez", "Acción Popular", "accion-popular", [
        P("ambiente", "Publicar la programación de limpieza por zonas e intervenir los puntos críticos de residuos", 3, "publicada o comunicada desde 2027", "Programación de limpieza publicada desde 2027"),
        P("urbano", "Plan de mantenimiento de parques y recuperación por etapas de parques y espacios públicos priorizados", 3, "Plan de mantenimiento de parques aprobado y operativo en 2027", "Plan aprobado en 2027; primera fase de recuperación al 2028"),
        P("urbano", "Mantenimiento progresivo de veredas, pistas locales y mobiliario urbano, según competencia y presupuesto", 3, "de veredas, pistas locales y mobiliario urbano"),
        P("seguridad", "Patrullaje preventivo de serenazgo en zonas priorizadas por horario, coordinado con la PNP en el CODISEC", 4, "Fortalecer el patrullaje preventivo de serenazgo en zonas priorizadas"),
        P("seguridad", "Evaluar analítica de video, lectura de placas y drones, y fortalecer un observatorio municipal de monitoreo y respuesta", 4, "lectura de placas y monitoreo situacional"),
        P("seguridad", "Canal de reporte vecinal de incidencias con seguimiento", 4, "Canal de reporte vecinal operativo desde 2027", "Operativo desde 2027"),
        P("economia", "Programa de orientación al comerciante y jornadas sobre licencias de funcionamiento y trámites municipales", 5, "sobre licencias de funcionamiento", "Mínimo 4 jornadas de orientación comercial por año"),
        P("economia", "Bolsa laboral distrital con empresas del distrito y formación en empleabilidad y emprendimiento para jóvenes de 18 a 30 años", 5, "bolsa laboral distrital articulada con empresas del distrito"),
        P("social", "Actualizar el padrón de adultos mayores, fortalecer el CIAM y el Club del Adulto Mayor y hacer campañas preventivas de salud", 6, "Club del Adulto Mayor como espacio", "Mínimo 4 campañas preventivas por año"),
        P("social", "Escuelas deportivas formativas y programa para detectar talentos, con clubes, ligas e instituciones educativas", 8, "Impulsar programas para detectar", "Escuelas formativas desde 2027"),
        P("gestion", "Tablero público de seguimiento de los compromisos del plan, registro de solicitudes vecinales y rendiciones de cuentas", 9, "Tablero de seguimiento publicado durante 2027", "Tablero en 2027; mínimo 2 rendiciones de cuentas por año"),
    ]),
    ("Dennis Alvarado Carrasco", "Ahora Nación", "ahora-nacion-an", [
        P("seguridad", "Centro de Operaciones Municipal que integre cámaras, serenazgo, alertas vecinales, comisarías y postas", 2, "Centro de Operaciones Municipal que integre"),
        P("seguridad", "Usar inteligencia artificial para mapas de riesgo por zona, horario y tipo de incidencia, y orientar el patrullaje", 3, "Crear mapas distritales de riesgo por zonas, horarios y tipos de incidencia", "100 % de las zonas críticas identificadas con patrullaje preventivo y monitoreo"),
        P("seguridad", "Aplicativo «Alerta 24/7» para reportar delitos, emergencias, luminarias dañadas, vehículos abandonados o basura", 3, "para reportar en tiempo real actos delictivos"),
        P("social", "Becas municipales en deporte, arte y excelencia académica, con registro de talentos y convenios con academias y la liga de fútbol", 3, "Otorgar becas municipales en tres", "Becas anuales con seguimiento semestral y publicación de resultados"),
        P("ambiente", "Centro Municipal de Bienestar Animal, campañas de vacunación y esterilización, dispensadores de bolsas y registro voluntario de mascotas", 4, "Crear un Centro Municipal de Bienestar Animal"),
        P("gestion", "Digitalizar los principales trámites, con plataforma única, identidad digital y seguimiento de expedientes en línea", 4, "Digitalizar progresivamente los principales procedimientos municipales"),
        P("economia", "Ventanilla de orientación para licencias y formalización, ferias distritales de emprendimiento y capacitación en marketing digital", 5, "Realizar ferias distritales de emprendimiento"),
        P("economia", "Ordenar el comercio ambulatorio con mapas de fiscalización, operativos proporcionales y alternativas de formalización o reubicación", 5, "Identificar zonas de mayor desorden mediante mapas"),
        P("ambiente", "Optimizar rutas de limpieza, colocar contenedores en zonas priorizadas, fiscalizar el arrojo de residuos y crear rutas piloto de reciclaje", 6, "Optimizar rutas de limpieza"),
        P("urbano", "Mantenimiento permanente de parques y jardines, arborización, mejor iluminación y adopción vecinal de áreas verdes", 6, "Realizar mantenimiento permanente de parques y jardines"),
        P("gestion", "Publicar cada trimestre el avance de metas, la ejecución presupuestal, contrataciones y obras", 7, "Publicar informes trimestrales y realizar", "Informes trimestrales y una rendición pública anual"),
    ]),
    ("José Luis Huamaní Gonzales", "Avanza País", "avanza-pais-partido-de-integracion-social", [
        P("seguridad", "Nuevas cámaras en puntos críticos con identificación de placas y un serenazgo integrado con los distritos vecinos", 9, "de placas en unidades vehiculares", "Reducir en 90 % los niveles de inseguridad al 2030"),
        P("social", "«Casa de la Mujer Surquillana»: refugio, capacitación y apoyo legal y policial para familias en situación de violencia", 9, "CASA DE LA MUJER SURQUILLANA", "Bajar en 80 % los casos de violencia familiar al 2030"),
        P("social", "«Clínica Municipal Surquillo» con la empresa privada y campañas de salud mensuales descentralizadas", 10, "CLINICA MUNICIPAL SURQUILLO", "Clínica al 100 % y atención al 60 % de la población"),
        P("economia", "«Bolsa de Trabajo» y programas «A Trabajar Surquillo», «Jóvenes a Trabajar» y «Familias Productivas»", 12, "BOLSA DE TRABAJO", "Reducir en 35 % el desempleo local"),
        P("economia", "Subgerencia de desarrollo comercial para mypes y una «Guía Comercial Surquillana» impresa y virtual", 13, "Sub Gerencia Local de desarrollo comercial", "Aumentar 30 % los pequeños negocios y mypes al 2030"),
        P("urbano", "Plan de Desarrollo Urbano Local a 10 años; las inmobiliarias deberán mejorar pistas, veredas y áreas verdes en su entorno", 15, "se tiene que hacer cargo de los colaterales"),
        P("agua_riesgos", "Observatorio local ante desastres, escuadrones municipales de rescate y contenedores de apoyo en los parques más grandes", 15, "los escuadrones de rescate municipal", "Al 2030"),
        P("gestion", "«Catastro General Surquillo 2028», actualizado mensualmente, para regularizar predios y mejorar la recaudación", 16, "CATASTRO GENERAL SURQUILLO 2028", "Catastro completo, ejecutado en el segundo año de gestión"),
        P("ambiente", "Contenedores subterráneos en mercados y programa «Surquillo Recicla»", 17, "SURQUILLO RECICLA", "80 % del distrito en el programa al 2030"),
        P("gestion", "Sistematizar todos los procesos administrativos y reducir los tiempos de espera en trámites", 19, "reducir en 90% los tiempos de espera", "100 % de procesos sistematizados y 90 % menos de espera al 2030"),
        P("transporte", "No tercerizar el servicio de grúas y adquirir una grúa municipal propia", 20, "No tercerizaremos el servicio de"),
    ]),
    ("Sandra Liz Gutiérrez Cuba", "Somos Perú", "partido-democratico-somos-peru", [
        P("seguridad", "Ampliar la Central de Monitoreo y Videovigilancia con reconocimiento facial e inteligencia artificial, conectada con vecinos y PNP", 8, "Central de Monitoreo y Video Vigilancia", "Renovar el sistema de videovigilancia al segundo año"),
        P("seguridad", "Comprar motos y vehículos equipados para patrullaje integrado, siempre con un efectivo de la PNP", 8, "perfectamente equipados para cumplir el servicio de patrullaje integrado obligatorio", "15 motos y 6 vehículos"),
        P("seguridad", "Aumentar el personal de serenazgo uniformado y capacitado", 8, "no menor de 300 el personal de serenazgo", "Al menos 300 serenos más"),
        P("seguridad", "Unidad de inteligencia con serenos y policías de franco para identificar zonas rojas y actualizar el mapa del delito", 9, "Mapa del Delito en forma permanente", "Respuesta a emergencias en máximo 5 minutos"),
        P("transporte", "Semáforo en el cruce de las avenidas Sergio Bernales y República de Panamá, señalización vial y reglas para scooters", 9, "intersecciones de la Av. Sergio Bernales y Av. Rep", "Semáforo en el primer año"),
        P("social", "Escuela municipal gratuita de arte, danza, música (con orquesta sinfónica) y teatro para niños y jóvenes", 10, "Escuela municipal gratuita de arte, danza"),
        P("social", "Policlínico Municipal con tarifa especial para adultos mayores y campañas médicas gratuitas en todos los sectores", 11, "tarifario especial para los adultos mayores"),
        P("economia", "Remodelar y reabrir el Mercado de Abastos N.° 1, revisando el proyecto de inversión existente", 13, "y la reapertura del Mercado de Abasto"),
        P("economia", "Asesoría con COFIDE para emprender, ferias y simplificación administrativa para formalizar mypes", 13, "asesoraremos a todo vecino que desee emprender"),
        P("agua_riesgos", "Regar áreas verdes por inundación con agua del río Surco en lugar de agua potable", 14, "(rio Surco) y no al uso del agua potable"),
        P("ambiente", "Prohibir de forma progresiva bolsas plásticas, tecnopor y sorbetes, y más unidades de recojo en zonas de alta demanda", 15, "Tecnopor y sorbetes"),
    ]),
    ("Jessica Ofelia Barrera Mendoza", "Partido País para Todos", "partido-pais-para-todos", [
        P("seguridad", "«Plan Centinela»: nuevas cámaras en zonas de alta incidencia, repotenciación de las existentes y central de monitoreo", 7, "videovigilancia con software exclusivo", "200 cámaras operativas al 2030"),
        P("seguridad", "Oficina de inteligencia municipal articulada con la PNP para sustentar arrestos de delincuentes identificados", 7, "OFICINA DE INTELIGENCIA MUNICIPAL", "Reducir los delitos en 40 % al 2030"),
        P("social", "Capacitación a madres, suplementación nutricional y brigadas de salud móviles contra la anemia infantil", 8, "Anemia infantil reducida al 5% al 2030", "Anemia infantil de más de 20 % a 5 % al 2030"),
        P("social", "Botica municipal con medicamentos básicos y una ambulancia para emergencias", 8, "botica municipal distrital para garantizar acceso a medicamentos", "Botica y ambulancia operativas al 2028"),
        P("economia", "Convenios con institutos y universidades para capacitar en oficios e incubadora de negocios con mentoría y financiamiento", 10, "100 emprendimientos formalizados al 2030", "1 000 personas capacitadas al año; 100 emprendimientos formalizados al 2030"),
        P("economia", "Cuatro ferias de empleo al año y simplificación de licencias municipales en 60 %", 10, "4 ferias anuales de empleo con empresas privadas", "500 colocaciones laborales al año; 70 % de negocios formalizados"),
        P("ambiente", "Segregación en la fuente, formalización de recicladores, volquete para desmonte y mejores horarios de recojo", 11, "Volquete para residuos de", "95 % de cobertura y 0 puntos críticos al 2030"),
        P("urbano", "Servicios higiénicos en los parques principales del distrito", 11, "SSHH operativos en parques principales al 2028", "Al 2028"),
        P("transporte", "Señalización de avenidas, semaforización y habilitación de estacionamientos en todo el distrito", 11, "estacionamientos en todo el distrito", "100 % de avenidas principales señalizadas"),
        P("gestion", "Digitalizar trámites en plataforma y app, ventanilla única virtual y eliminar requisitos innecesarios", 13, "tiempo reducido 60%", "80 % de trámites digitales al 2030 y 60 % menos de tiempo"),
        P("gestion", "Presupuesto participativo con proyectos elegidos por los vecinos y audiencias públicas semestrales", 13, "10% del presupuesto a proyectos elegidos por los vecinos", "10 % del presupuesto; 2 audiencias al año"),
    ]),
    ("María Teresa Maestre Mejía", "PRIN", "partido-politico-prin", [
        P("social", "Brigadas médicas descentralizadas, telemedicina y un Centro Municipal de Bienestar Emocional para la salud mental", 3, "Centro Municipal de Bienestar Emocional de Surquillo", "60 % más de atención psicológica"),
        P("social", "Clínica Veterinaria Municipal 24 horas, unidad veterinaria móvil e identificación de mascotas con microchip", 4, "mascotas mediante microchip", "80 % de cobertura de registro animal"),
        P("social", "Brigadas médicas itinerantes en todos los sectores y un centro médico municipal de urgencias las 24 horas", 12, "50,000 atenciones anuales", "50 000 atenciones preventivas al año"),
        P("economia", "Licencias de funcionamiento rápidas y digitales", 13, "a menos de 48 horas", "Emisión de licencias en menos de 48 horas"),
        P("economia", "Modernizar los mercados del distrito como espacios seguros y atractivos", 13, "80% de mercados intervenidos", "80 % de mercados intervenidos"),
        P("ambiente", "Limpieza pública permanente en todo el distrito y lavado programado de vías con camiones cisterna", 15, "4 lavados semanales en zonas", "100 % de cobertura diaria; 4 lavados semanales en zonas críticas"),
        P("gestion", "Digitalizar todos los trámites municipales y simplificar procedimientos administrativos", 16, "Simplificar procedimientos administrativos para mejorar eficiencia", "100 % de trámites digitalizados y 60 % menos de tiempo de atención"),
        P("seguridad", "Patrullaje por cuadrantes con serenazgo permanente y patrullaje motorizado de respuesta rápida las 24 horas", 17, "Implementar patrullaje por cuadrantes con presencia permanente de serenazgo", "100 % del distrito cubierto; respuesta en menos de 5 minutos"),
        P("seguridad", "Modernizar la videovigilancia con tecnología inteligente conectada a la central de monitoreo", 17, "Modernizar el sistema de videovigilancia con", "300 cámaras operativas"),
        P("transporte", "Programa «Estaciona Surquillo»: playa de estacionamiento subterránea para liberar calles y veredas", 8, "Estaciona Surquillo", "50 % más de capacidad de estacionamiento formal"),
        P("urbano", "Programa «Veredas para Todos» con accesibilidad para personas con discapacidad y adultos mayores, y alumbrado LED", 8, "Veredas para Todos", "80 % de espacios públicos con accesibilidad universal"),
    ]),
    ("Renzo Jesús Gutiérrez Portillo", "PPC", "partido-popular-cristiano-ppc", [
        P("seguridad", "Plan de seguridad con distritos vecinos e inteligencia artificial predictiva, y luminarias LED en calles oscuras del Surquillo Antiguo", 6, "Plan de seguridad integrado con distritos vecinos", "Percepción de inseguridad al 65 % y 1 500 denuncias al año"),
        P("social", "Brigadas itinerantes de atención psicológica y legal para prevenir la violencia familiar y proteger a la infancia", 6, "itinerantes para prevenir la violencia familiar"),
        P("social", "Servicio de ambulancias y una clínica municipal en alianza con EsSalud u organizaciones privadas", 7, "Implementar servicio de ambulancias"),
        P("social", "Ejecutar la «Villa Olímpica Municipal» con piscinas techadas de tarifa social y programa «Deporte Nocturno Seguro» en losas de barrio", 9, "Deporte Nocturno Seguro", "Duplicar los beneficiarios de las escuelas deportivas gratuitas (meta: 200 %)"),
        P("ambiente", "«Parques de Bolsillo», jardines verticales y ordenanza de protección del arbolado urbano", 11, "Parques de Bolsillo", "4,5 m² de áreas verdes por habitante"),
        P("ambiente", "Contenedores soterrados con sensores de llenado y ampliación de «Surquillo Recicla» a edificios y zonas comerciales", 12, "contenedores soterrados y sensores de llenado", "3 asociaciones de recicladores formalizadas y 30 % de residuos procesados"),
        P("ambiente", "Regular el polvo en obras de construcción y crear una red municipal de sensores de calidad del aire", 13, "Red Municipal de Sensores de Calidad del Aire"),
        P("transporte", "Olas verdes con análisis de tráfico por IA y ciclovías segregadas conectadas con San Borja, Miraflores y San Isidro", 14, "que se conecten con las redes de San Borja, Miraflores y San Isidro", "S/ 5 millones anuales para transitabilidad y movilidad no motorizada"),
        P("economia", "«Agencia Municipal de Desarrollo» descentralizada para licencias y asesoría, exoneraciones temporales y sello «Hecho en Surquillo»", 15, "Agencia Municipal de Desarrollo", "Pobreza al 9 % y 10 % de pequeñas unidades de negocio rentables"),
        P("economia", "«Instituto Municipal del Emprendedor» con formación gratuita para comerciantes informales", 16, "Instituto Municipal del Emprendedor", "Capacitar y formalizar al 30 % de los trabajadores informales"),
        P("gestion", "Delegados por zona y cabildos abiertos trimestrales de rendición de cuentas en cada sector", 17, "descentralizada de Cabildos Abiertos", "50 % más de asistencia vecinal a los cabildos"),
    ]),
    ("Miguel Ángel Ccamac Ortiz", "Podemos Perú", "podemos-peru", [
        P("seguridad", "Patrullaje 24 horas por cuadrantes, alarmas vecinales y botones de pánico en 2 o 3 viviendas por cuadra conectados a la central", 9, "alarmas vecinales, las cuales"),
        P("seguridad", "Videovigilancia con reconocimiento facial e inteligencia artificial conectada a las bases de datos de la PNP", 11, "con las bases de datos de la PNP y del Ministerio del Interior"),
        P("seguridad", "Aplicativo municipal para denunciar hechos irregulares o delictivos, con opción anónima y seguimiento", 12, "dentro de las 24 horas siguientes a la denuncia", "Respuesta o acción verificable en 24 horas"),
        P("social", "Preventorio de Surquillo para detección temprana de cáncer y campañas de análisis de laboratorio", 12, "Preventorio de Surquillo"),
        P("social", "«La Pre de Surquillo»: academia preuniversitaria gratuita para postular a universidades públicas", 15, "LA PRE DE SURQUILLO"),
        P("gestion", "Audiencias vecinales semanales con el alcalde y portal de rendición de cuentas y gobierno abierto", 17, "Audiencias Vecinales semanales de acceso libre", "Rendición de cuentas a los 100 días y balance anual"),
        P("urbano", "Programa gratuito «Mi Casa, Mi Derecho» de saneamiento y formalización de predios hasta su inscripción en SUNARP", 20, "formalizar al menos el 30% de los predios informales", "Formalizar al menos el 30 % de los predios informales identificados"),
        P("urbano", "Mejoramiento de pistas y veredas por administración directa, con trabajadores que residen en Surquillo", 21, "Mejoramiento de pistas y veredas con mano de obra surquillana"),
        P("transporte", "Centro de Control de Tráfico con olas verdes adaptativas, semáforos modernos y estudio de estacionamientos subterráneos", 21, "olas verdes adaptativas"),
        P("economia", "Reformar el régimen de sanciones: multas más bajas para comerciantes que son personas naturales y advertencia previa antes de sancionar", 26, "en un 50% para personas naturales comerciantes", "50 % menos en la multa base de infracciones leves"),
        P("social", "Piscina temperada semiolímpica de uso público en el Parque Héroes de la Paz", 29, "una piscina temperada de uso"),
    ]),
    ("Ruth Haydee Meza Saldarriaga", "Renovación Popular", "renovacion-popular-peru", [
        P("seguridad", "Más patrullaje integrado de serenazgo y PNP y videovigilancia modernizada en zonas críticas", 12, "Incrementaremos el patrullaje integrado Serenazgo", "Reducir en 90 % la percepción de inseguridad"),
        P("social", "Ampliar los programas sociales municipales, priorizando a niños, adultos mayores y familias en riesgo", 12, "Ampliaremos los programas sociales municipales", "Cobertura del 85 % de la población vulnerable"),
        P("urbano", "Recuperar parques y espacios públicos como lugares seguros e iluminados", 12, "Devolveremos los parques y espacios", "10 espacios públicos recuperados"),
        P("social", "Campañas de salud preventiva y apoyo psicológico comunitario con brigadas de atención", 12, "comunitario y brigadas de", "20 campañas anuales"),
        P("economia", "Formalización progresiva del comercio local, acompañando al comerciante y eliminando trabas burocráticas", 13, "Ordenaremos y dignificaremos el comercio local", "70 % de formalización de mypes"),
        P("economia", "Alianzas con empresas, capacitación técnica para jóvenes y bolsas de trabajo locales", 13, "bolsas de trabajo locales", "5 000 personas capacitadas"),
        P("economia", "Capacitación, digitalización de negocios y mejora de espacios comerciales, con ferias y economía digital", 13, "Modernizaremos el comercio local con programas de", "12 ferias anuales"),
        P("ambiente", "Recuperar y ampliar las áreas verdes, convirtiendo áreas abandonadas en parques", 13, "Recuperaremos y ampliaremos los espacios verdes del distrito", "4 m² de áreas verdes por habitante"),
        P("ambiente", "Limpieza pública con rutas optimizadas, mayor frecuencia de recolección y campañas de cultura ambiental", 13, "rutas optimizadas, mayor frecuencia de", "95 % de cobertura"),
        P("ambiente", "Fiscalizar establecimientos ruidosos, controlar el tránsito en zonas críticas y aplicar zonificación acústica", 14, "a establecimientos ruidosos"),
        P("gestion", "Simplificar y digitalizar trámites y servicios municipales", 14, "digitalizaremos los servicios municipales", "90 % de digitalización y 90 % menos de tiempo en trámites"),
    ]),
]
