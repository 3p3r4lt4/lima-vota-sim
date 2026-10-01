"""San Borja (150130): propuestas principales de los 8 planes de gobierno inscritos ante el JNE.

Cada propuesta está redactada con palabras propias y lleva:
  - pagina: la página del PDF oficial donde aparece.
  - ancla: un fragmento textual del PDF que DEBE aparecer en esa página. El generador lo verifica y
    falla si no lo encuentra, para que ninguna cita apunte a una página equivocada.
Mismo criterio para todas: entre 8 y 11 propuestas por plan, repartidas en los temas que el plan desarrolla.
"""

UBIGEO = "150130"

def P(tema, texto, pagina, ancla, meta=None):
    return {"tema": tema, "texto": texto, "meta": meta, "pagina": pagina, "ancla": ancla}

# (nombre, organización, archivo PDF, propuestas)
PLANES = [
    ("Alberto Tejada Conroy", "Acción Popular", "accion-popular", [
        P("seguridad", "Programa «San Borja Seguro 360»: patrullaje integrado, analítica de video, centros descentralizados, participación vecinal y articulación con la PNP", 73, "Desarrollar San Borja Seguro 360", "Reducir la victimización a 21,39 % y superar el 80 % de percepción de seguridad"),
        P("social", "Programa «San Borja Salud 360» con tamizajes preventivos, vida saludable, atención comunitaria y seguimiento digital", 72, "Implementar San Borja Salud 360", "80 % de cobertura anual de tamizajes y 50 % más de participación en actividades saludables"),
        P("social", "Red «San Borja Cardioprotegida» con desfibriladores, brigadas comunitarias y capacitación en RCP en espacios públicos", 73, "Implementar San Borja Cardioprotegida"),
        P("economia", "Programa «San Borja Emprende e Innova»: capacitación, mentoría, digitalización, ventanilla empresarial y promoción comercial para emprendedores y mypes", 74, "Impulsar San Borja Emprende e Innova", "Más de 3 000 emprendedores y pequeñas empresas beneficiados"),
        P("economia", "Bolsa laboral, escuela de capacitación e inclusión laboral para jóvenes, mujeres, adultos mayores y personas con discapacidad", 74, "Capacitar y vincular laboralmente a", "Más de 5 000 vecinos capacitados y vinculados laboralmente en 2027-2030"),
        P("gestion", "Modernizar el catastro, rentas y finanzas con información georreferenciada y gestión tributaria digital", 74, "municipal de 72.85% a 90% al 2030", "Eficacia de recaudación de 72,85 % a 90 % al 2030"),
        P("transporte", "Movilidad inteligente y «Urbanito Seguro»: transporte de proximidad, integración modal, ciclovías, rutas seguras y cultura vial", 75, "Incrementar en 40% el uso de movilidad sostenible", "40 % más uso de movilidad sostenible y 20 % menos tiempo de viaje en corredores priorizados"),
        P("urbano", "Programa «Barrios Integrados y Convivencia Vecinal»: intervenciones barriales y recuperación de espacios comunitarios en sectores residenciales", 77, "Implementar Barrios Integrados y"),
        P("agua_riesgos", "Programa «Agua y Energía para el Futuro»: riego tecnificado, Canal Surco, luminarias eficientes, energías renovables y soterramiento", 76, "Alcanzar 60% de cobertura de riego tecnificado", "60 % de riego tecnificado, 20 % menos consumo de agua y 25 % menos energía municipal"),
        P("ambiente", "Plan Distrital de Adaptación Climática y sistema de medición de la huella de carbono municipal", 76, "Implementar San Borja Carbono Neutral"),
        P("gestion", "Plataforma «Mi San Borja» con gobierno digital, datos abiertos e innovación pública", 76, "Digitalizar al menos 90% de", "Al menos 90 % de trámites digitalizados y 50 % menos tiempo de atención"),
    ]),
    ("Roberth Edwuard Montoya Puente", "Avanza País", "avanza-pais-partido-de-integracion-social", [
        P("seguridad", "Plan «San Borja Muy Seguro»: central de videovigilancia con IA predictiva, botones de pánico, drones y patrullaje con civiles armados", 33, "San Borja Muy Seguro", "100 % de cámaras con IA y respuesta a emergencias en menos de 3 minutos"),
        P("social", "Ambulancias municipales Tipo I y II y preventorios itinerantes de salud en los 12 sectores vecinales", 33, "preventorios itinerantes de salud", "2 ambulancias nuevas en el primer año de gestión"),
        P("social", "Casas del Adulto Mayor (CIAM) sectoriales para descentralizar la atención", 33, "de 04 nuevas Casas CIAM", "4 nuevas Casas CIAM equipadas"),
        P("economia", "Reubicar el comercio informal en ferias itinerantes formales y crear una plataforma digital de formalización de microemprendedores", 34, "800 microemprendedores formalizados", "0 puntos de comercio ambulante no autorizado y 800 microemprendedores formalizados"),
        P("economia", "Reestructurar la Bolsa de Trabajo y vincular los talleres municipales con lo que piden las empresas del distrito", 34, "2,500 vecinos vulnerables insertados", "2 500 vecinos insertados en empleos formales"),
        P("transporte", "Fiscalización permanente con la ATU y la Policía de Tránsito para erradicar paraderos informales, en especial en el nodo Javier Prado–Aviación", 34, "paraderos informales de transporte", "0 paraderos informales en el distrito"),
        P("ambiente", "Monitoreo del arbolado con tecnología Tree-Radar y tomógrafos sónicos para detectar daños y programar podas", 34, "Tree-Radar (TRU)", "100 % del arbolado con ficha digital y 0 accidentes por caída de árboles en parques"),
        P("agua_riesgos", "Riego tecnificado de parques con aguas residuales tratadas y sistemas automatizados", 34, "Tecnificar el riego de los parques", "90 % de las áreas verdes con riego tecnificado"),
        P("ambiente", "Sonómetros en zonas comerciales, renovación de contenedores soterrados y rutas de recolección con GPS", 35, "renovar los contenedores soterrados de residuos", "50 % menos contaminación sonora en ejes críticos y 80 % de familias reciclando"),
        P("gestion", "Tambos Municipales y Muni-Agencias descentralizadas por sector, con atención digital unificada y transparencia activa", 35, "12 Tambos Municipales operativos", "12 Tambos Municipales y 100 % de cumplimiento del Portal de Transparencia"),
        P("urbano", "Protocolo de reparación rápida de baches en las vías urbanas", 35, "sin baches en menos de 72 horas", "100 % de vías reparadas en menos de 72 horas"),
    ]),
    ("Edgard Núñez Quipuzco", "Libertad Popular", "libertad-popular", [
        P("seguridad", "Más cámaras de videovigilancia con inteligencia artificial", 15, "de video vigilancia con IA", "50 % más cámaras, con un aumento de 25 % anual"),
        P("seguridad", "Centro de control C5 para gestionar la seguridad pública y las emergencias urbanas", 15, "100% en 24 meses del centro de control C5", "C5 implementado al 100 % en 24 meses"),
        P("seguridad", "Mejorar la app «SOS San Borja» y crear una línea segura para denunciar extorsión y violencia familiar", 15, "de la app SOS", "App en 6 meses y línea segura en 12 meses"),
        P("social", "Teleconsulta municipal para consultas de salud que no son de emergencia", 13, "Prestaciones de salud por teleconsulta", "80 % de las consultas no de emergencia por teleconsulta"),
        P("social", "Atención primaria de salud con horarios ampliados y actividades fuera del establecimiento", 16, "Reducir el tiempo de espera a menos de 2", "Cobertura del 90 % de la población objetivo y citas en menos de 2 días hábiles"),
        P("gestion", "Revisar el TUPA y digitalizar todos los trámites municipales", 13, "Tramites 100 % digitales", "100 % de trámites digitales al final de la gestión"),
        P("gestion", "Publicar indicadores de gestión en formato abierto para auditoría ciudadana", 12, "publicados en formato abierto", "Actualización cada 15 días como máximo"),
        P("transporte", "Reducir la congestión vehicular y la contaminación, con más uso de transporte público, bicicletas y ciclovías", 14, "Reducir 25% vehicular en horas punta", "25 % menos flujo vehicular en horas punta"),
        P("ambiente", "Ampliar las áreas verdes urbanas y reducir los contaminantes del aire", 14, "5. Incrementar un 15%", "15 % más de áreas verdes urbanas"),
        P("ambiente", "Empadronar y formalizar a los recicladores que trabajan de noche, y usar cámaras con IA contra el arrojo de basura y desmonte", 3, "empadronados, capacitados y formalizados"),
        P("economia", "Programa «Nuestros jubilados son jóvenes con experiencia» para reinsertar a profesionales jubilados en el mercado laboral", 10, "NUESTROS JUBILADOS SON JOVENES CON EXPERIENCIA"),
    ]),
    ("Juan Fernando Pilco Castañeda", "Partido Aprista Peruano", "partido-aprista-peruano", [
        P("seguridad", "Ampliar la videovigilancia inteligente, integrar serenazgo y PNP, y botones de pánico con alerta vecinal", 3, "inseguridad en un 30%", "Reducir en 30 % la percepción de inseguridad"),
        P("seguridad", "Corredores seguros en zonas comerciales, educativas y recreativas", 3, "corredores seguros en zonas comerciales"),
        P("social", "Salud mental comunitaria, atención preventiva al adulto mayor y jornadas gratuitas de despistaje", 4, "Programas de salud mental comunitaria"),
        P("social", "Escuelas municipales deportivas y modernización de espacios deportivos", 4, "Escuelas municipales deportivas"),
        P("economia", "Centro Municipal de Desarrollo Empresarial con asistencia técnica y capacitación digital para mypes", 5, "Centro Municipal de Desarrollo Empresarial"),
        P("economia", "Ordenar el comercio ambulatorio e incentivar la formalización con trámites simplificados", 6, "Ordenamiento del comercio ambulatorio"),
        P("transporte", "Gestión inteligente del tránsito con monitoreo de tráfico y ampliación de ciclovías", 8, "sistemas de monitoreo de"),
        P("ambiente", "Reciclaje con segregación en origen, puntos ecológicos e incentivos a prácticas sostenibles", 8, "programas de reciclaje"),
        P("agua_riesgos", "Simulacros distritales, capacitación vecinal en primeros auxilios y sistemas de alerta temprana", 9, "Simulacros distritales"),
        P("gestion", "Observatorio ciudadano de obras y servicios, portal de datos abiertos y audiencias públicas", 10, "Observatorio ciudadano de obras"),
        P("gestion", "Informes trimestrales de gestión y tablero digital de seguimiento de metas", 11, "Informes trimestrales"),
    ]),
    ("Gina Valeria Casanova Mera", "Somos Perú", "partido-democratico-somos-peru", [
        P("seguridad", "Programa «San Borja Seguro e Inteligente 24/7» con IA, reconocimiento facial y vehicular, y cámaras corporales", 54, "San Borja Seguro e Inteligente 24/7", "Más de 1 000 cámaras inteligentes y 30 % menos percepción de inseguridad al 2030"),
        P("seguridad", "Programa «Identifica tu Delivery» con carné municipal y registro digital de repartidores", 54, "con carnet municipal y registro digital de repartidores"),
        P("social", "Nuevo Centro Integral del Adulto Mayor y una OMAPED modernizada con rehabilitación y terapias", 54, "modernizar integralmente la OMAPED", "1 CIAM nuevo y más de 10 000 vecinos vulnerables beneficiados"),
        P("urbano", "Recuperar espacios deportivos y parques recreativos, con campañas de salud preventiva en los 12 sectores", 54, "Recuperar y modernizar 15 espacios deportivos", "15 espacios deportivos y 30 parques recreativos"),
        P("agua_riesgos", "Alerta temprana ante sismos en parques y plazas que son puntos de reunión, y contenedores soterrados con equipos de respuesta", 54, "Servicio de Alerta Temprana ante Sismos", "100 % de puntos de reunión cubiertos y activación en 15 segundos o menos"),
        P("transporte", "Rehabilitación de vías locales y programa «San Borja Ciudad Ciclable» con señalización y regulación de vehículos eléctricos", 55, "San Borja Ciudad Ciclable", "100 % de vías locales en mal estado rehabilitadas"),
        P("ambiente", "Recuperar áreas verdes con riego tecnificado y convertir parques en nodos de sostenibilidad", 55, "Recuperar 50,000 m", "50 000 m² de áreas verdes recuperadas"),
        P("ambiente", "Programa «Bono Verde» de segregación de residuos con incentivos", 55, "incrementar en 25% la cobertura de", "25 % más cobertura de segregación al 2030"),
        P("economia", "Alianzas público-privadas y Obras por Impuestos para proyectos distritales", 55, "mecanismos de Obras por Impuestos"),
        P("gestion", "Programa «Municipalidad Digital y Gobierno Inteligente» con trámites de inicio a fin en línea", 56, "Reducir en un 40% el tiempo de respuesta", "100 % de trámites digitales al 2030 y 40 % menos tiempo en licencias de edificación"),
        P("gestion", "Audiencias públicas descentralizadas, tablero de control ciudadano e indicadores trimestrales", 56, "tablero de control ciudadano"),
    ]),
    ("Joel Edmundo Miranda Villanueva", "Partido Político ADP", "partido-politico-adp", [
        P("seguridad", "Programa de seguridad ciudadana inteligente con videovigilancia, patrullaje integrado y participación vecinal", 4, "Reducir en 30% de los delitos reportados", "30 % menos delitos reportados al 2030"),
        P("gestion", "Plataforma digital de gobierno abierto y fortalecimiento de las juntas vecinales", 4, "20,000 usuarios registrados", "20 000 usuarios registrados y 100 % de juntas vecinales fortalecidas al 2030"),
        P("urbano", "Recuperar y modernizar parques y espacios públicos seguros e inclusivos", 4, "Recuperar y modernizar parques", "30 espacios públicos recuperados o mejorados"),
        P("gestion", "Plataforma única de trámites digitales y simplificación administrativa", 4, "Digitalizar el 90% de los", "90 % de trámites municipales digitalizados"),
        P("economia", "Programas de innovación, capacitación y emprendimiento", 4, "Beneficiar a 2,000 emprendedores", "2 000 emprendedores beneficiados durante la gestión"),
        P("economia", "Programas y ferias de promoción comercial e inversión local", 5, "menos 20 programas o ferias", "Al menos 20 programas o ferias"),
        P("transporte", "Movilidad sostenible y semaforización inteligente contra la congestión", 5, "Reducir en 20% los tiempos de", "20 % menos tiempo de congestión vehicular"),
        P("transporte", "Ampliar y modernizar la red de ciclovías", 5, "Incrementar en 20 km la infraestructura ciclista", "20 km más de infraestructura ciclista"),
        P("ambiente", "Programas de reciclaje, arborización y monitoreo ambiental", 5, "Plantar 10,000", "10 000 árboles y 30 % más de reciclaje"),
        P("agua_riesgos", "Tecnificar el riego de áreas verdes con aguas tratadas", 3, "riego con aguas de tratamiento"),
        P("gestion", "Dos audiencias públicas al año transmitidas en vivo y un «semáforo de cumplimiento» del plan en línea", 5, "dos (2) audiencias", "2 audiencias públicas al año"),
    ]),
    ("Willyans José Soriano Cabrera", "PPC", "partido-popular-cristiano-ppc", [
        P("seguridad", "Central Inteligente de Seguridad con analítica de video, lectura de placas, Red Vecino Seguro y patrullaje integrado", 12, "Reducir en 30% los robos al paso", "30 % menos robos al paso, 40 % menos robo de vehículos y 35 % menos robos domiciliarios"),
        P("seguridad", "Escuela Municipal de Formación y Capacitación de Serenos", 11, "Crearemos la Escuela Municipal de"),
        P("social", "Programas «Médico en tu Barrio» y teleorientación municipal en salud", 16, "Incrementar en 60% las atenciones preventivas", "60 % más atenciones preventivas y más de 20 000 vecinos al año en campañas"),
        P("social", "Ampliar la atención psicológica municipal y los programas para adultos mayores", 16, "Duplicar la cobertura de", "Duplicar la atención psicológica y 50 % más adultos mayores en programas"),
        P("social", "Escuelas Deportivas Municipales y formación de talentos", 20, "25 disciplinas deportivas", "Más de 25 disciplinas"),
        P("economia", "Centro de Innovación y Emprendimiento, Ventanilla Única Empresarial y bolsa laboral", 23, "5,000 emprendedores", "70 % menos tiempo en licencias y más de 5 000 emprendedores capacitados"),
        P("transporte", "Programa «San Borja en Bici 2.0»: bicicletas públicas con estaciones inteligentes, app y registro digital", 25, "PROGRAMA 3 SAN BORJA EN BICI 2.0"),
        P("ambiente", "Programa de arborización, Eco Parque San Borja y reciclaje", 29, "Plantar 10,000 nuevos", "10 000 árboles nuevos y 30 % más de reciclaje"),
        P("urbano", "Programa «San Borja Iluminada» de alumbrado LED y catastro digital georreferenciado", 31, "SAN BORJA ILUMINADA"),
        P("gestion", "Programa «Municipalidad Digital 100 %» con expediente electrónico, firma digital y «San Borja App»", 34, "Digitalizar el 100% de los procedimientos", "100 % de procedimientos digitalizados y 70 % menos tiempo de atención"),
        P("gestion", "Portal de transparencia, observatorio ciudadano y presupuesto participativo digital", 36, "Publicar el 100% de la", "100 % de la información obligatoria publicada"),
    ]),
    ("Javier Martín Diez Gaspard", "Renovación Popular", "renovacion-popular-peru", [
        P("seguridad", "Programa «Mi Sector Seguro»: patrullas fijas por cuadrante, patrullaje integrado con la PNP y cámaras con reconocimiento facial y de placas", 6, "Sectorizar el distrito en cuadrantes", "Reducir en 50 % la tasa de delitos por cada 10 000 habitantes"),
        P("seguridad", "«Serenazgo Comunitario a Pie» y redes «Vecinos Alerta» conectadas al Centro de Monitoreo por app", 7, "Serenazgo Comunitario a Pie", "80 % de percepción positiva de seguridad"),
        P("social", "Casa del Adulto Mayor y Centro de Día, atención médica domiciliaria y telemedicina", 7, "nueva Casa del Adulto Mayor y Centro de", "100 % de adultos mayores vulnerables identificados atendidos"),
        P("social", "Casa de la Juventud con coworking, laboratorios de innovación y Academia Preuniversitaria Municipal gratuita", 8, "Fundar la Academia Preuniversitaria Municipal", "50 % de la población juvenil"),
        P("social", "Clínica Municipal con pediatría, ginecología, cardiología y odontología a tarifas sociales", 10, "consultorios especializados de alta demanda", "50 % de la población con atención preventiva y especializada"),
        P("economia", "Ferias, ruedas de negocios y plataforma «San Borja Compra Local» para los negocios del distrito", 11, "San Borja Compra Local", "100 % más ferias y ruedas de negocios"),
        P("ambiente", "Programa «Recicla San Borja» con educación ambiental puerta por puerta", 11, "Recicla San Borja", "100 % de hogares en el programa de reciclaje"),
        P("transporte", "Ampliar y mantener la red de ciclovías y controlar las emisiones vehiculares con la PNP", 12, "segregar y realizar el mantenimiento mayor de la red", "50 % menos emisiones vehiculares y 100 % más operativos"),
        P("agua_riesgos", "Riego tecnificado por goteo y aspersión conectado a redes de agua tratada", 13, "conectada directamente a las redes de agua tratada", "100 % de áreas verdes regadas con agua tratada"),
        P("urbano", "Actualizar los parámetros urbanísticos para proteger las zonas residenciales", 6, "blindando las zonas residenciales"),
        P("gestion", "Certificación ISO 37001 antisoborno, control concurrente de la Contraloría en licitaciones y denuncias anónimas", 15, "ISO 37001 (Sistema de", "100 % de política de prevención de la corrupción"),
    ]),
]
