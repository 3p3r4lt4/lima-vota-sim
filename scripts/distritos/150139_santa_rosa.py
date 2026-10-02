"""Santa Rosa (150139): propuestas principales de los planes de gobierno inscritos ante el JNE.

Cada propuesta está redactada con palabras propias y lleva:
  - pagina: la página del PDF oficial donde aparece.
  - ancla: un fragmento textual del PDF que DEBE aparecer en esa página. El generador lo verifica y
    falla si no lo encuentra, para que ninguna cita apunte a una página equivocada.
Mismo criterio para todas: entre 8 y 11 propuestas por plan, repartidas en los temas que el plan desarrolla.
"""

UBIGEO = "150139"

def P(tema, texto, pagina, ancla, meta=None):
    return {"tema": tema, "texto": texto, "meta": meta, "pagina": pagina, "ancla": ancla}

# (nombre, organización, archivo PDF, propuestas)
PLANES = [
    ("Tanus Barraza Calvo", "Acción Popular", "accion-popular", [
        P("seguridad", "Sistema integral de seguridad con central de monitoreo, cámaras, puestos de auxilio rápido y unidades móviles conectados por fibra óptica con la PNP", 19, "puestos de auxilio rápido, unidades móviles"),
        P("seguridad", "Profesionalizar al serenazgo según la Ley 31297 e incrementar progresivamente el número de serenos", 12, "profesionalización del personal de serenazgo", "80 % más serenos operativos al 2030"),
        P("social", "Mejorar y equipar las 3 postas médicas actuales y construir un Policlínico Municipal", 6, "construcción del nuevo Policlínico Municipal para su inauguración en 2029", "Policlínico inaugurado en 2029"),
        P("social", "Casa de la Mujer con protocolo de respuesta inmediata ante violencia familiar, articulada con la Comisaría de Santa Rosa", 6, "inauguración y equipamiento de la Casa de la Mujer en 2027", "Casa de la Mujer en funcionamiento en 2027"),
        P("agua_riesgos", "Acelerar con el Ministerio de Vivienda y SEDAPAL el proyecto de agua y desagüe en Profam, Adesesep y otros sectores", 22, "Celeridad de la Ejecución del Proyecto de Agua y Desagüe"),
        P("agua_riesgos", "Gestionar muros de contención en la Parcela H, Portales de Santa Rosa y Adesesep con fondos de inversión y el programa Lurawi", 20, "muros de contención en la Parcela H"),
        P("urbano", "Saneamiento físico-legal y titulación de los asentamientos humanos, en coordinación con Sedapal, Pluz Enel y COFOPRI", 5, "saneamiento físico-legal al 100% de los Asentamientos Humanos", "100 % de los asentamientos humanos viables saneados"),
        P("economia", "Plan de Desarrollo Turístico Local con circuitos de festivales playeros, gastronomía y caballos de paso", 8, "Plan de Desarrollo Turístico Local (PDTL)", "Duplicar el flujo de visitantes de Lima Norte al 2030"),
        P("transporte", "Registro de unidades de transporte público y empadronamiento obligatorio de vehículos menores mediante ordenanza", 25, "empadronamiento obligatorio de vehículos menores"),
        P("ambiente", "Red de contenedores soterrados en los puntos críticos de acumulación de basura, empezando por las zonas comerciales", 9, "primera red de contenedores soterrados", "100 % de los puntos soterrados previstos al 2030"),
        P("gestion", "Catastro municipal integral y georreferenciado mediante convenios con el Ministerio de Vivienda o SUNARP", 11, "levantamiento cartográfico y catastral del 25% del territorio", "25 % del territorio en 2027 y 100 % del catastro al 2030"),
    ]),
    (None, "Avanza País", "avanza-pais-partido-de-integracion-social", [
        P("seguridad", "Sistema integrado de seguridad con central de monitoreo y videovigilancia inteligente, integrado con el serenazgo y la Policía", 139, "Implementación del Sistema Integrado de Seguridad Ciudadana", "Implementado entre 2027 y 2028"),
        P("seguridad", "Red distrital de alarmas comunitarias, escuelas de seguridad vecinal e iluminación preventiva de espacios públicos", 130, "Red Distrital de Alarmas Comunitarias"),
        P("economia", "Gran Malecón Turístico y Recreativo con paseo costero, miradores, ciclovías y espacios culturales y gastronómicos", 140, "Malecón Turístico y Recreativo. Meta temporal: 2029–2030", "Ejecución entre 2029 y 2030"),
        P("economia", "Corredor gastronómico costero, ruta turística del distrito y ferias de emprendimiento y producción local", 131, "Corredor Gastronómico Costero"),
        P("ambiente", "Parque Metropolitano Costero con áreas verdes, bosques urbanos, espacios recreativos e infraestructura deportiva", 139, "Parque Metropolitano Costero. Meta temporal: 2029", "Ejecución en 2029"),
        P("social", "Centro de Innovación, Juventud y Emprendimiento con laboratorios digitales, coworking e incubadora de emprendimientos", 139, "Implementación del Centro de Innovación, Juventud y Emprendimiento", "Implementado en 2028"),
        P("social", "Programas Adulto Mayor Activo, Santa Rosa Inclusiva y Deporte para Todos", 130, "Adulto Mayor Activo"),
        P("agua_riesgos", "Planes distritales ante sismos y tsunami, rutas de evacuación señalizadas, zonas seguras, alerta temprana y simulacros comunitarios", 132, "Plan distrital de preparación ante tsunami"),
        P("urbano", "Programa de mejoramiento urbano con pavimentación de vías, veredas, accesibilidad universal y renovación de parques", 84, "PROGRAMA DE MEJORAMIENTO URBANO INTEGRAL"),
        P("gestion", "Programa «Santa Rosa Digital» con trámites digitales, mesa de partes virtual, gobierno abierto y transparencia digital", 62, "Mesa de partes virtual"),
    ]),
    ("Ever Félix Rojas Caja", "Partido Demócrata Verde", "partido-democrata-verde", [
        P("economia", "Ruta turística que una las playas de Santa Rosa y Ancón, con restaurantes y zonas de comercio local", 9, "integre las playas de Santa Rosa y Ancón"),
        P("economia", "Mesa técnica público-privada para captar empleo y servicios vinculados al Parque Industrial de Ancón y al Puerto de Chancay", 9, "Parque Industrial de Ancón y del Puerto de Chancay"),
        P("seguridad", "Gestionar con el MININTER la construcción de una comisaría en el sector de PROFAM", 10, "construcción de la Comisaría de PROFAM"),
        P("seguridad", "Cámaras de videovigilancia en puntos críticos con una central de monitoreo que usa inteligencia artificial para generar alertas", 11, "herramientas de inteligencia artificial para identificar alertas"),
        P("transporte", "Formalizar las mototaxis con registro, rutas definidas, paraderos autorizados, identificación vehicular y fiscalización", 12, "Formalizar el servicio de mototaxis"),
        P("transporte", "Promover una línea de transporte público que conecte Coovitiomar, La Arboleda, PROFAM y Pachacútec con Ventanilla", 12, "Promover una línea de transporte que conecte Coovitiomar"),
        P("urbano", "Asistencia técnica a los asentamientos humanos para su titulación y saneamiento físico-legal, y actualización del catastro", 12, "agilizar su formalización, titulación y acceso a servicios básicos"),
        P("ambiente", "Segregación en la fuente, puntos limpios y formalización de los recicladores", 14, "implementar puntos limpios y formalizar a los recicladores"),
        P("social", "Gestionar ante el MINSA un Centro Materno Infantil en PROFAM", 14, "CENTRO MATERNO INFANTIL DE PROFAM"),
        P("social", "Promover un centro comunitario de salud mental para jóvenes, mujeres y adultos mayores", 15, "CENTRO DE SALUD MENTAL COMUNITARIO"),
        P("gestion", "Plataforma digital para trámites, pagos, consultas y seguimiento de expedientes", 12, "plataforma digital para realizar trámites, pagos"),
    ]),
    (None, "Somos Perú", "partido-democratico-somos-peru", [
        P("gestion", "Programa «Muni móvil»: llevar los servicios municipales a zonas de difícil acceso", 5, "Una vez al mes la municipalidad se apersonará", "Una vez al mes"),
        P("seguridad", "Patrullaje integrado e interconexión de cámaras para un centro C4 de monitoreo conjunto con la PNP", 7, "para contar finalmente con un C4"),
        P("seguridad", "Promover la creación e implementación de una nueva comisaría en PROFAM", 8, "nueva comisaría en PROFAM"),
        P("agua_riesgos", "Dar seguimiento a los esquemas de agua Pachacútec-Profam y Santa Rosa-Ancón para iniciar las obras pendientes con SEDAPAL", 5, "esquemas Pachacutec-Profam"),
        P("urbano", "Convenios con COFOPRI para oficinas descentralizadas de titulación y saneamiento de predios en la Parcela H", 9, "oficinas descentralizadas dentro de la municipalidad"),
        P("urbano", "Gestionar con el Ministerio de Cultura rescates arqueológicos en los sectores 4, 5, 6 y 10 de Profam para acceder a servicios básicos", 6, "rescates arqueológicos en zonas donde ya se ha consolidado"),
        P("economia", "Circuito turístico de Playa Grande con alameda, zonas deportivas, estacionamiento, camping y zona de conciertos", 9, "circuito turístico de playa grande"),
        P("social", "Crear el primer policlínico municipal del distrito con servicios a costo social", 6, "primer policlínico municipal del distrito"),
        P("social", "Academia municipal de fútbol y Casa de la Juventud para deporte, arte y cultura", 6, "academia municipal de futbol"),
        P("ambiente", "Adquirir una máquina rastrilladora de arena para limpiar las playas e instalar tachos de basura y reciclaje", 11, "maquina de rastrillaje de arena"),
        P("ambiente", "Comprar compactadoras de 17 a 21 toneladas e incentivos tributarios para quienes se sumen al reciclaje", 11, "adquisición de 2 unidades de compactadoras", "2 compactadoras"),
    ]),
    (None, "Podemos Perú", "podemos-peru", [
        P("seguridad", "Sistema integral de seguridad con central de monitoreo, cámaras y puestos de auxilio rápido; más serenazgo con patrullaje a pie y en bicicleta", 9, "Creación de Sistema Integral de Seguridad Ciudadana con una central de monitoreo"),
        P("agua_riesgos", "Convenios para dotar de agua y desagüe a Profam, Productiva, Adesep y otros asentamientos humanos con SEDAPAL", 14, "Reducir la brecha de falta de acceso a agua y saneamiento en un 50%", "Reducir en 50 % la brecha de acceso a agua y saneamiento"),
        P("agua_riesgos", "Sistema de alerta temprana ante tsunamis y sismos en el litoral y simulacros comunitarios en las zonas más vulnerables", 17, "Sistema de Alerta Temprana ante Tsunamis", "100 % del sistema de alerta y 4 simulacros por año"),
        P("urbano", "Gestionar con la MML la Vía Metropolitana por las avenidas Playa Hondable, Revolución y El Carmen", 12, "construcción de la Vía Metropolitana"),
        P("social", "Crear el Centro Materno Infantil en Arboleda y mejorar la posta médica de Profam", 11, "Creación del Centro Materno Infantil en Arboleda"),
        P("social", "Reducir la anemia infantil reforzando la atención primaria y la vigilancia nutricional", 14, "Reducir la prevalencia de anemia infantil", "Menos del 20 % de anemia infantil al final del periodo"),
        P("economia", "Proyecto de centro comercial y bancario en la Av. Colectora y parque industrial en Profam", 12, "Creación del Parque Industrial en Profam"),
        P("economia", "Mercado Modelo Municipal Central con inversión público-privada para reordenar el comercio de abastos", 16, "Mercado Modelo Municipal Central"),
        P("ambiente", "Programa «Basura Cero» para mejorar el recojo diario y formalizar asociaciones de recicladores locales", 16, "Basura Cero", "95 % de cobertura de recojo diario y al menos 3 asociaciones de recicladores formalizadas"),
        P("ambiente", "Plantar árboles para zonas áridas (huarango, molle) en parques y avenidas, regados con aguas residuales tratadas", 17, "plantación de 10,000 árboles aptos para zonas áridas", "10,000 árboles"),
        P("gestion", "Plataforma web y aplicativo móvil para digitalizar los trámites de mayor demanda", 17, "Digitalizar el 80% de los trámites con mayor demanda", "80 % de trámites digitalizados al segundo año"),
    ]),
    ("Óscar Alex Dolorier Mori", "Renovación Popular", "renovacion-popular-peru", [
        P("seguridad", "Central de monitoreo con fibra óptica a la Comisaría y al MININTER, y cámaras con analítica en los accesos del Km 39 y zonas de usurpación", 3, "Central de Monitoreo y Video vigilancia del distrito"),
        P("seguridad", "Patrullaje integrado por sectores con más serenazgo, patrullas y unidades ligeras para Campamento, El Golf y La Arboleda", 4, "Patrullaje Integrado Sectorizado", "45 % menos denuncias por robo y usurpación en 24 meses"),
        P("gestion", "Oficina de atención municipal permanente en el Km 39 (Villa Estela, Los Rosales, Carlos Manuel Cox, Bahía Blanca)", 4, "oficina de atención municipal permanente y descentralizada en el Km 39"),
        P("urbano", "Programa de pistas y veredas en los AA.HH. El Golf y La Arboleda con señalización vial y de zonas escolares", 5, "Programa Integral de Pistas y Veredas"),
        P("agua_riesgos", "Mesa técnica con el Ministerio de Vivienda y SEDAPAL para culminar el agua y desagüe de PROFAM, Productiva y Adesep", 6, "mesa técnica permanente con el Ministerio de Vivienda", "90 % de conexiones domiciliarias al 2030"),
        P("urbano", "Sanear terrenos del Estado para construir el primer cementerio municipal de Santa Rosa", 6, "primer Cementerio Municipal de Santa Rosa", "100 % del terreno saneado y primera etapa construida al 2030"),
        P("social", "Gestionar ante el MINSA un Centro Materno Infantil en La Arboleda con urgencias 24 horas y mejorar la posta de PROFAM", 8, "Centro Materno Infantil en La Arboleda"),
        P("ambiente", "Optimizar las rutas de compactadoras para cubrir la recolección en PROFAM y Adesep e instalar contenedores en playas, plazas y colegios", 8, "cubrir el 100% de la recolección domiciliaria", "100 % de recolección diaria de las 15 toneladas"),
        P("transporte", "Empadronamiento obligatorio de mototaxis, paraderos autorizados, señalización de cruces escolares y educación vial con la PNP", 11, "empadronamiento general obligatorio", "98 % de asociaciones de vehículos menores formalizadas"),
        P("economia", "Plan «Circuito Turístico Seguro» en Playa Grande, Playa Chica y Playa Hondable, con eventos deportivos y ferias gastronómicas todo el año", 11, "Circuito Turístico Seguro Santa Rosa"),
        P("economia", "Red de mercados de abastos municipales que agrupe y formalice a los comerciantes locales", 11, "Red de Mercados de Abastos Municipales", "50 % de avance físico de la red de mercados al 2030"),
    ]),
]
