"""Pachacámac (150123): propuestas principales de los planes de gobierno inscritos ante el JNE.

Cada propuesta está redactada con palabras propias y lleva:
  - pagina: la página del PDF oficial donde aparece.
  - ancla: un fragmento textual del PDF que DEBE aparecer en esa página. El generador lo verifica y
    falla si no lo encuentra, para que ninguna cita apunte a una página equivocada.
Mismo criterio para todas: entre 8 y 11 propuestas por plan, repartidas en los temas que el plan desarrolla.
"""

UBIGEO = "150123"

def P(tema, texto, pagina, ancla, meta=None):
    return {"tema": tema, "texto": texto, "meta": meta, "pagina": pagina, "ancla": ancla}

# (nombre, organización, archivo PDF, propuestas)
PLANES = [
    ("Pedro Quispe Galdos", "Avanza País", "avanza-pais-partido-de-integracion-social", [
        P("seguridad", "Centro de Monitoreo Inteligente 24/7 con cámaras fijas, PTZ, de reconocimiento facial y de placas clonadas, interconectadas", 6, "Instalación de 900 cámaras fijas", "900 cámaras fijas, 500 PTZ, 50 de reconocimiento facial y 50 de lectura de placas"),
        P("seguridad", "Patrullaje integrado con la PNP, aplicativo vecinal de alertas, programa Barrio Seguro y juntas vecinales fortalecidas", 7, "Aplicativo vecinal de alertas"),
        P("economia", "Centros municipales de Tecnología y de Innovación Empresarial, Escuela de Emprendedores y programa Primer Empleo Joven", 7, "Programa Primer Empleo Joven", "4 000 nuevos empleos formales al 2030"),
        P("economia", "Programa «Mercados Modernos y Seguros»: infraestructura, carnet de sanidad digital, manejo de residuos y defensa civil", 7, "MERCADOS MODERNOS Y SEGUROS", "80 % de los mercados formales modernizados y más de 5 000 comerciantes beneficiados al 2030"),
        P("economia", "Programa «Compre Pachac, consuma local»: plataforma digital de negocios, ferias itinerantes y marca «Hecho en Pachacamac»", 8, "Hecho en Pachacamac", "25 % más ventas de MYPES y productores locales al 2030"),
        P("urbano", "Formalización y titulación de predios con convenio permanente con COFOPRI, catastro digital y oficina municipal", 8, "Convenio permanente con COFOPRI"),
        P("social", "Plan distrital contra la tuberculosis y programa de prevención de la anemia infantil", 8, "Plan Distrital de Lucha contra la Tuberculosis", "Reducir en 30 % la anemia infantil"),
        P("ambiente", "Recuperar parques, arborizar el ornato y modernizar la limpieza pública", 8, "100 parques recuperados", "100 parques recuperados y cobertura total de limpieza pública al 2030"),
        P("ambiente", "Reciclaje desde los hogares articulado con recicladores formalizados", 11, "impulsar el reciclaje desde los hogares", "20 000 hogares en programas de reciclaje y segregación"),
        P("gestion", "Municipalidad digital, portal de transparencia en tiempo real, presupuesto participativo digital y gobierno abierto", 9, "Portal de Transparencia en Tiempo Real", "80 % de trámites digitalizados al 2030"),
        P("gestion", "Audiencias públicas, informes de cumplimiento, portal de seguimiento de compromisos y observatorio ciudadano", 9, "Observatorio Ciudadano de Transparencia", "Audiencias públicas semestrales e informes trimestrales"),
    ]),
    ("Johnny Walter Auris Olivares", "Partido Cívico Obras", "partido-civico-obras", [
        P("seguridad", "Equipamiento para el patrullaje preventivo e integrado con camionetas y motocicletas, y más presencia del serenazgo en zonas estratégicas", 10, "adquisición de 25 camionetas, 30 motocicletas", "25 camionetas y 30 motocicletas"),
        P("social", "Centro Municipal contra la Violencia de la Mujer y fortalecimiento del CIAM, la DEMUNA y la OMAPED", 12, "Implementación del Centro Municipal contra la Violencia de la Mujer"),
        P("social", "Casa de la Cultura en el pueblo tradicional, academia municipal de fútbol, ajedrez y atletismo y programa itinerante de música", 14, "Implementación de la Casa de la Cultura en el Pueblo Tradicional"),
        P("urbano", "Plan de Desarrollo Urbano, actualización de la zonificación, catastro urbano y rural digital y saneamiento físico-legal de predios", 18, "Implementar el Catastro Urbano y Rural del distrito"),
        P("agua_riesgos", "Gestionar ante SEDAPAL proyectos de agua y alcantarillado y obras de protección ribereña en el río", 19, "Gestionar ante SEDAPAL la ejecución de los proyectos de agua potable"),
        P("urbano", "Mejorar las calles internas de Huertos de Manchay, ampliar el Estadio Municipal y construir un complejo deportivo en la Zona 5", 20, "Mejoramiento de todas las Calles Internas del C.P.R. Huertos De Manchay"),
        P("transporte", "Vía Integradora con Lima Metropolitana para conectar Pachacámac, José Gálvez, Retamal y Villa María del Triunfo", 24, "conectividad entre Pachacámac, José Gálvez, Retamal y Villa María del Triunfo"),
        P("ambiente", "Nueva flota de compactadoras, formalización de recicladores, planta de compostaje y planta de transferencia de residuos", 27, "Habilitación de una planta de compostaje"),
        P("economia", "Hospedaje turístico municipal, Eco Mercado Municipal y nuevo Centro de Atención al Turista", 31, "CREACIÓN DEL ECO MERCADO MUNICIPAL"),
        P("economia", "Talleres trimestrales de gestión empresarial para MYPES, campañas de formalización con SUNAT y Oficina de Empleo", 31, "talleres trimestrales sobre gestión empresarial"),
        P("gestion", "Plataforma digital integrada de atención al ciudadano y sistema informático municipal integrado", 33, "Plataforma Digital Integrada de Atención al Ciudadano"),
    ]),
    ("Guillermo Elvis Pómez Cano", "Somos Perú", "partido-democratico-somos-peru", [
        P("seguridad", "Central de monitoreo con cámaras con IA y lectura de placas, patrullaje «Plan Cuadrante Seguro» con flota en renting y Serenazgo sin Fronteras", 8, "Serenazgo sin Fronteras", "90 % de alertas de emergencia atendidas en menos de 7 minutos"),
        P("social", "Red de postas médicas municipales en zonas periféricas con módulos de telemedicina, en convenio con la DIRIS Lima Sur", 9, "Red de Postas Médicas Municipales"),
        P("social", "Programa comunitario contra la anemia infantil con visitas domiciliarias de tamizaje y suplementos", 9, "programa comunitario de reducción de anemia infantil", "Reducir en 15 puntos porcentuales la anemia infantil"),
        P("social", "Internet de alta velocidad y aulas TIC renovadas en colegios públicos, en coordinación con PRONATEL y el MINEDU", 10, "renovación de aulas TIC", "90 % de colegios públicos con internet y equipamiento básico"),
        P("economia", "Zonas autorizadas para el comercio ambulatorio y capacitación certificada para formalizar a los comerciantes", 12, "formalización progresiva de un mínimo de 3,500 comerciantes", "Al menos 3 500 comerciantes formalizados"),
        P("economia", "Corredor turístico, marca «Pachacámac Ancestral y Vivo», Museo de la Cultura Viva y parque en las Lomas de Lúcumo", 13, "Lomas de Lúcumo", "40 % más turistas al 2030"),
        P("urbano", "Nuevo Plan Urbano Distrital, catastro con COFOPRI y SUNARP y habilitaciones urbanas de oficio", 14, "mínimo de 5,000 lotes familiares", "Al menos 5 000 lotes titulados"),
        P("transporte", "Av. Ferrocarril entre Quebrada Verde y José Gálvez, anillo vial Los Claveles Altos y puente entre Manchay Bajo y Cardal", 15, "Anillo Vial - Av. Los Claveles Altos", "Al menos 15 km de vías pavimentadas"),
        P("ambiente", "Planta de transferencia de residuos, segregación en la fuente con incentivos y aguas tratadas para riego de áreas verdes", 16, "Planta de Transferencia de Residuos Sólidos distrital", "95 % de cobertura de recolección y disposición adecuada"),
        P("agua_riesgos", "Descolmatación del río Lurín y primera estación de bomberos permanente en la Quebrada de Manchay", 16, "descolmatación, encauzamiento y limpieza preventiva"),
        P("gestion", "Gobierno electrónico para pago de tributos, seguimiento de expedientes y mesa de partes digital, con certificación ISO 9001", 17, "sistema integrado de Gobierno Electrónico (Smart City)", "80 % de los trámites de mayor demanda en línea al 2030"),
    ]),
    ("Giancarlos Enrique Zárate Quispe", "Frente de la Esperanza 2021", "partido-frente-de-la-esperanza-2021", [
        P("seguridad", "Central de videovigilancia con cámaras con IA, lectura de placas y monitoreo integrado con la PNP", 2, "Central de Videovigilancia Inteligente", "Cobertura total de videovigilancia en zonas urbanas"),
        P("seguridad", "Más serenos, patrullaje integrado con la PNP, motos, camionetas y drones de vigilancia", 2, "Implementación de drones de vigilancia", "Reducir la delincuencia en 40 % y respuesta en menos de 5 minutos"),
        P("urbano", "Reemplazo de luminarias por LED en parques, avenidas y zonas rurales", 2, "Reemplazo de luminarias antiguas por LED", "Cobertura total de iluminación LED"),
        P("ambiente", "Recolección con nuevos compactadores, rutas inteligentes, contenedores soterrados y eliminación de botaderos informales", 3, "Contenedores soterrados en zonas estratégicas", "Reducir 80 % los residuos informales y cobertura total de limpieza pública"),
        P("ambiente", "Arborización masiva, corredores ecológicos y recuperación de áreas verdes", 4, "Creación de corredores ecológicos", "Duplicar las áreas verdes públicas"),
        P("economia", "Circuito turístico que integre el Santuario, las Lomas de Lúcumo, restaurantes campestres, caballos de paso y turismo vivencial", 4, "Caballos de paso", "Duplicar los visitantes turísticos"),
        P("urbano", "Plan integral de pistas y veredas accesibles, parques con iluminación LED y losas deportivas techadas", 6, "Veredas accesibles para personas con discapacidad", "100 % de avenidas principales mejoradas"),
        P("agua_riesgos", "Gestionar ante el Gobierno Central y Sedapal la ampliación de las redes de agua y desagüe", 6, "Ampliación de redes de agua y desagüe"),
        P("transporte", "Semaforización inteligente, mejores accesos viales, ciclovías y transporte ordenado", 6, "Semaforización inteligente"),
        P("social", "Casa de la Juventud, Casa del Adulto Mayor y casa para las organizaciones sociales de base", 8, "Casa de la Juventud"),
        P("gestion", "Trámites virtuales, agencias municipales en las 5 zonas, publicación en línea de obras y gastos y veeduría ciudadana", 8, "Audiencias vecinales trimestrales", "Audiencias vecinales trimestrales"),
    ]),
    ("Jorge Alexander Ardiles Quin", "Partido Morado", "partido-morado", [
        P("seguridad", "Cámaras interconectadas con la PNP en puntos críticos y alarmas vecinales", 15, "250 cámaras nuevas con interconexión PNP", "250 cámaras al 2030, respuesta menor a 10 minutos y 80 % de juntas vecinales con alarma"),
        P("seguridad", "Plan Concertado de Seguridad Ciudadana con juntas vecinales activas por sector articuladas al CODISEC", 15, "1 junta vecinal por sector operando", "Reducir 25 % la victimización al 2030 y una junta vecinal por sector al 2028"),
        P("social", "Expedientes técnicos para modernizar puestos de salud y más ambulancias, en coordinación con la DIRIS Lima Sur", 16, "2 ambulancias adicionales operativas al 2028", "5 expedientes de puestos de salud y 2 ambulancias al 2028; 30 % más cobertura preventiva al 2030"),
        P("social", "Centros de reforzamiento escolar, capacitación docente y becas universitarias integrales", 16, "20 centros de reforzamiento escolar abiertos al 2030", "20 centros de reforzamiento al 2030 y 10 becas universitarias al año"),
        P("economia", "Empadronamiento de negocios formales e informales y reordenamiento de la zonificación comercial con los gremios", 18, "5 zonas estratégicas reordenadas", "5 zonas comerciales reordenadas y 80 % de negocios formales empadronados al 2030"),
        P("economia", "Plan Integral de Turismo y Desarrollo Recreacional, Parque del Río Verde y Parque de Aventura", 19, "Parque del Río Verde creado y operativo al 2030", "Plan de Turismo al 2028 y Parque del Río Verde al 2030"),
        P("transporte", "Plan vial distrital y ejecución de las vías que conectan las cinco zonas del distrito", 20, "Plan Vial Distrital aprobado al 2027", "Plan Vial al 2027 y 20 % de mejora del flujo vehicular al 2030"),
        P("agua_riesgos", "Plan Distrital de Gestión del Riesgo de Desastres con alerta temprana y simulacros por zona", 20, "4 simulacros anuales por zona", "4 simulacros anuales por zona y 60 % de la población sensibilizada al 2030"),
        P("agua_riesgos", "Acelerar el Esquema José Gálvez–Villa Alejandro de agua y alcantarillado con mesas técnicas mensuales con MVCS y SEDAPAL", 21, "12 526 conexiones de agua potable", "Apoyar 12 526 conexiones de agua y 2 604 de alcantarillado al 2030"),
        P("ambiente", "Plan Integral de Gestión de Residuos Sólidos actualizado, con segregación en origen y conservación de áreas verdes", 20, "40 % de calles y parques limpios", "40 % de calles y parques limpios y 50 % de áreas verdes conservadas al 2030"),
        P("gestion", "Sistema de Transparencia Digital y convenios con el Ministerio Público y la Contraloría", 23, "Sistema de Transparencia Digital al 2030", "80 % de procesos municipales registrados en el sistema al 2030"),
    ]),
    ("Javier Fernando Ramírez Guerra Guerra", "PPC", "partido-popular-cristiano-ppc", [
        P("social", "Atención integral para reducir la anemia y la desnutrición crónica infantil", 4, "erradicar la anemia y la desnutrición infantil crónicas", "Anemia ≤ 10 % y desnutrición crónica ≤ 8 %"),
        P("social", "Ampliar la cobertura y la calidad de la educación inicial", 4, "universalizar la educación inicial de calidad", "Cobertura de educación inicial ≥ 90 % y ratio niño/educador ≤ 25:1"),
        P("seguridad", "Modernización tecnológica, patrullaje integrado y juntas vecinales interconectadas a la central de monitoreo", 6, "Reducir la tasa de victimización delincuencial local en un 25.0%", "Reducir 25 % la victimización al 2030 y 100 % de juntas vecinales interconectadas al 2029"),
        P("transporte", "Formalizar y ordenar el transporte menor y extradistrital, mejorar las vías y gestionar rutas integradas ante la ATU y la MML", 6, "ordenamiento y formalización del transporte menor", "100 % de empresas de transporte menor formalizadas al 2029 y 80 % de corredores viales mejorados al 2030"),
        P("economia", "Tecnificar el riego del valle y conectar a los productores con ferias agroecológicas y mercados mayoristas", 7, "500 productores locales comercialicen directamente", "500 productores en venta directa y riego tecnificado en el 35 % de las parcelas al 2030"),
        P("economia", "Capacitación técnica, formalización y promoción turística para micro y pequeñas empresas", 7, "1,000 microempresas y emprendimientos turísticos", "1 000 microempresas y emprendimientos turísticos formalizados al 2030"),
        P("agua_riesgos", "Formalizar y asistir a las JASS rurales y viabilizar proyectos de agua y saneamiento con SEDAPAL y la ALA", 7, "Viabilizar e impulsar 3 proyectos integrales de redes de agua", "100 % de JASS rurales formalizadas y 3 proyectos de agua y saneamiento viabilizados"),
        P("urbano", "Aprobar e implementar el Plan de Desarrollo Urbano Sostenible y actualizar el catastro", 7, "Plan de Desarrollo Urbano Sostenible de Pachacámac", "Plan aprobado e implementado en el primer año de gestión (2027)"),
        P("ambiente", "Arborización masiva con especies nativas de bajo consumo de agua en avenidas, bermas y parques", 8, "40,000 árboles aptos para el clima local", "40 000 árboles al 2030"),
        P("ambiente", "Segregación en la fuente y formalización de asociaciones de recicladores", 8, "residuos sólidos aprovechables del distrito ingresen al circuito de reciclaje", "25 % de residuos aprovechables reciclados al 2030"),
        P("gestion", "Módulos de Atención al Vecino zonales con ventanilla única y trámites digitales bajo la política de «cero papeles»", 8, "siete Módulos de Atención al Vecino (MAVE)", "7 módulos operativos al 2028 y 85 % de trámites TUPA digitales al 2030"),
    ]),
    ("Luis Fernando Moreno Córdova", "Partido SíCreo", "partido-sicreo", [
        P("seguridad", "Modernizar la central de monitoreo y ampliar las cámaras con analítica de video e identificación de placas", 15, "Incremento de 69 a 200 cámaras de videovigilancia", "De 69 a 200 cámaras"),
        P("seguridad", "Serenazgo motorizado: más vehículos, motocicletas de respuesta rápida y más personal", 15, "Incrementar la flota operativa de 19 a 40 vehículos", "40 vehículos, 50 motocicletas y 220 serenos"),
        P("seguridad", "Programa Barrio Seguro y recuperación de espacios públicos identificados como focos de inseguridad", 15, "Incrementar las juntas vecinales de 35 a 70", "De 35 a 70 juntas vecinales activas"),
        P("urbano", "Saneamiento físico-legal de predios urbanos y rurales en coordinación con COFOPRI", 17, "Gestionar la formalización de más de 10,000 lotes", "Más de 10 000 predios formalizados al 2030"),
        P("transporte", "Pavimentación de vías estratégicas como Víctor Malásquez, Paul Poblet, La Unión y Quebrada Verde, con veredas accesibles", 17, "Construcción y mejoramiento de 80 kilómetros de pistas", "80 km de vías y 120 000 m² de veredas"),
        P("agua_riesgos", "Reservorios comunales en zonas altas, almacenamiento de agua para familias y drenaje pluvial en zonas vulnerables", 19, "Construcción de 10 reservorios comunales", "10 reservorios y cobertura de agua potable superior al 95 % al 2030"),
        P("economia", "Centro Municipal de Desarrollo Empresarial con capacitación gratuita y programas de formalización", 22, "Centro Municipal de Desarrollo Empresarial y Emprendimiento", "5 000 emprendedores capacitados y más de 3 000 negocios formalizados"),
        P("social", "Becas de capacitación técnica y tecnológica, bibliotecas virtuales comunitarias y nuevos complejos deportivos", 28, "Otorgamiento de 2,000 becas de capacitación técnica", "2 000 becas y 10 bibliotecas virtuales"),
        P("social", "Campañas de salud preventiva y consultorios psicológicos municipales descentralizados", 31, "Realizar 200 campañas de salud", "200 campañas de salud y más de 20 000 atenciones psicológicas"),
        P("ambiente", "Reforestación con viveros municipales y erradicación de los puntos críticos de residuos", 33, "Plantación de 100,000 árboles", "100 000 árboles y 100 % de puntos críticos erradicados"),
        P("gestion", "Municipalidad sin papeles: expediente electrónico, firma digital y trámites en línea las 24 horas", 36, "Municipalidad sin Papeles", "100 % de expedientes digitalizados y 50 % menos tiempo en trámites"),
    ]),
    ("Héctor Javier Quispe Salvador", "Renovación Popular", "renovacion-popular-peru", [
        P("seguridad", "Patrullaje preventivo del serenazgo en zonas críticas con mapas de riesgo y coordinación con dirigentes vecinales", 13, "Fortalecimiento del serenazgo municipal y patrullaje preventivo en zonas críticas"),
        P("seguridad", "Central de Operaciones Municipales para coordinar emergencias, seguridad y atención de reportes ciudadanos", 14, "Central de Operaciones Municipales"),
        P("social", "Fortalecer la DEMUNA, el CIAM, la OMAPED y los servicios de atención familiar con atención descentralizada", 15, "Fortalecimiento de la DEMUNA, CIAM, OMAPED"),
        P("social", "Campañas de salud preventiva, nutrición, lucha contra la anemia, salud mental y prevención del cáncer", 17, "Campañas de salud preventiva, nutrición, lucha contra la anemia"),
        P("urbano", "Recuperar espacios públicos, losas, parques y locales comunales con limpieza, iluminación y arborización", 19, "Recuperación de espacios públicos, losas, parques y locales comunales"),
        P("economia", "Capacitación técnica descentralizada para emprendedores, comerciantes, agricultores y jóvenes", 22, "Programas de capacitación técnica para emprendedores, comerciantes, agricultores"),
        P("economia", "Simplificar los procedimientos de licencias de funcionamiento y autorizaciones municipales", 24, "Simplificación de procedimientos para licencias de funcionamiento"),
        P("ambiente", "Identificar e intervenir puntos críticos de basura y desmonte en quebradas, vías y zonas de expansión", 31, "Identificación e intervención de puntos críticos de basura y desmonte"),
        P("agua_riesgos", "Gestionar muros de contención, defensas ribereñas, escaleras seguras y rutas de evacuación en zonas vulnerables", 34, "Gestión de obras preventivas frente a riesgos"),
        P("urbano", "Impulsar habilitaciones urbanas de oficio y regularizaciones para el saneamiento físico-legal", 39, "Impulso de habilitaciones urbanas de oficio"),
        P("gestion", "Plataforma digital de atención al vecino para consultas, reclamos y seguimiento de expedientes", 37, "Implementación de una plataforma digital de atención al vecino"),
    ]),
]
