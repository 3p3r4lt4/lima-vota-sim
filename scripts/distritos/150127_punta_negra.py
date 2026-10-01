"""Punta Negra (150127): propuestas principales de los planes de gobierno inscritos ante el JNE.

Cada propuesta está redactada con palabras propias y lleva:
  - pagina: la página del PDF oficial donde aparece.
  - ancla: un fragmento textual del PDF que DEBE aparecer en esa página. El generador lo verifica y
    falla si no lo encuentra, para que ninguna cita apunte a una página equivocada.
Mismo criterio para todas: entre 8 y 11 propuestas por plan, repartidas en los temas que el plan desarrolla.
"""

UBIGEO = "150127"

def P(tema, texto, pagina, ancla, meta=None):
    return {"tema": tema, "texto": texto, "meta": meta, "pagina": pagina, "ancla": ancla}

# (nombre, organización, archivo PDF, propuestas)
PLANES = [
    ("Mónica Alicia Huyhua Limachi", "Acción Popular", "accion-popular", [
        P("seguridad", "Patrullaje integrado diario PNP–Serenazgo priorizando las playas en verano y erradicación del cobro informal de parqueos", 14, "Patrullaje integrado intensivo"),
        P("seguridad", "Modernizar el Centro de Monitoreo con software de alertas automáticas las 24 horas y luminarias LED en parques, pasajes y malecón", 14, "Modernización del Centro de Monitoreo"),
        P("social", "Gestionar ante el MINSA la atención 24 horas del puesto de salud y su elevación a centro de salud, y abrir una botica municipal", 15, "Implementar, mediante convenios interinstitucionales la Botica Municipal"),
        P("social", "Campañas médicas gratuitas de descarte de diabetes, hipertensión, cáncer de cuello uterino, salud bucal y mental", 15, "campañas médicas gratuitas trimestrales", "Campañas trimestrales"),
        P("social", "Donar un terreno saneado al Ministerio de Educación para un colegio emblemático y gestionar su construcción ante el PRONIED", 15, "colegio emblemático"),
        P("transporte", "Pavimentación y rehabilitación de pistas y veredas, con mejor señalización y seguridad vial", 17, "Mejorar la señalización vial y la seguridad del tránsito"),
        P("urbano", "Actualizar el catastro urbano y llevar un registro semiautomatizado de licencias y fiscalización para seguir el crecimiento urbano", 17, "Actualizar el catastro urbano del distrito"),
        P("ambiente", "Censo de predios de los 10 sectores con código QR para el reciclaje y planta municipal de compostaje de residuos orgánicos", 17, "Planta Municipal de Valorización de Orgánicos"),
        P("ambiente", "GPS en los camiones compactadores y cámaras de foto denuncia contra el arrojo de desmonte en la Antigua Panamericana", 18, "Monitoreo Satelital (GPS)", "100 % de la flota de compactadoras con GPS"),
        P("agua_riesgos", "Convenios con industrias del distrito para regar bermas y parques con sus aguas residuales tratadas", 19, "Convenios para el Riego con Aguas Tratadas"),
        P("gestion", "Plataforma «Punta Negra en Línea» para hacer trámites en línea, con pagos electrónicos y app de reportes vecinales", 19, "Punta Negra en Línea", "100 % de los trámites municipales virtualizados"),
    ]),
    (None, "Fe en el Perú", "fe-en-el-peru", [
        P("urbano", "Construcción de pistas y veredas con titulación de predios", 3, "Construcción pistas y veredas con titulación"),
        P("seguridad", "Centro de Monitoreo y Videovigilancia Distrital", 3, "Centro de Monitoreo y Videovigilancia Distrital"),
        P("seguridad", "Más patrullaje integrado entre el Serenazgo y la Policía Nacional", 3, "Incremento del patrullaje integrado entre Serenazgo"),
        P("social", "Club de Vecinos para talleres, reactivación de la cuna municipal y construcción de una biblioteca municipal", 3, "Activación la cuna Municipal"),
        P("social", "Cine y karaoke en los parques y actividades familiares los domingos", 3, "cine en tu parque"),
        P("social", "Campañas médicas integrales para personas y mascotas", 4, "campaña medica integral"),
        P("economia", "Marca Turística Punta Negra y calendario anual de eventos turísticos, culturales y deportivos", 5, "Creación de la Marca Turística Punta Negra"),
        P("economia", "Ferias gastronómicas y comerciales, capacitación de emprendedores y asistencia para formalizar empresas", 5, "Implementación de ferias gastronómicas y comerciales"),
        P("ambiente", "Programa de limpieza con segregación en la fuente, puntos ecológicos y campañas permanentes de limpieza de playas", 6, "Campañas permanentes de limpieza de playas"),
        P("agua_riesgos", "Actualizar el plan distrital de gestión del riesgo y señalizar rutas de evacuación ante sismos y tsunamis", 6, "rutas de evacuación ante sismos y tsunamis"),
        P("gestion", "Plataforma de gobierno digital, digitalización de trámites y audiencias públicas de rendición de cuentas", 7, "Implementación de la plataforma de gobierno digital municipal"),
    ]),
    ("Javier Vicente Bustamante Villafuerte", "Partido Aprista Peruano", "partido-aprista-peruano", [
        P("seguridad", "Observatorio de la criminalidad y aplicativos «Punta Negra Emergencias» y «Vecino Vigilante» para reportes vecinales", 2, "Vecino Vigilante - Watch and Report"),
        P("seguridad", "Geolocalización de serenos con radios Tetra-GPS, cámaras corporales e integración de las centrales de radio y video con la PNP", 2, "radios Tetra-GPS"),
        P("seguridad", "Brigada aérea de drones con videovigilancia para lugares de difícil acceso", 2, "Brigada Aérea: Drones"),
        P("agua_riesgos", "Continuar los muros de contención y el reforzamiento de pircas, y recuperar los cauces de huaicos", 3, "muros de contención y el reforzamiento de pircas"),
        P("transporte", "Semaforización inteligente y mejora de las ciclovías con bicicletas interconectadas", 3, "semaforización inteligente perfeccionando"),
        P("urbano", "Rampas de accesibilidad en todo el cercado y alamedas con palmeras en las avenidas principales", 4, "Construir rampas de accesibilidad universal"),
        P("urbano", "Plan «Casa Titulada» de apoyo técnico para el saneamiento físico-legal y la titulación con COFOPRI", 4, "apoyo técnico en saneamiento físico-legal y titulación"),
        P("social", "Programa «Mi Barrio Progresa» con medicina, psicología, DEMUNA, asesoría legal y bibliotecas infantiles en centros vecinales", 4, "Mi Barrio Progresa"),
        P("economia", "Bolsa de trabajo distrital digital y capacitación técnica a jóvenes en las Casas de la Juventud", 5, "bolsa de trabajo distrital interactiva y digital"),
        P("ambiente", "Plantas de reciclaje de plástico y Tetra Pak y plantas de tratamiento de aguas residuales para regar áreas verdes", 5, "Crear plantas de reciclaje"),
        P("gestion", "Modificar el TUPA para atender trámites en 24 horas y transmitir en línea la adjudicación de contratos", 6, "plazo de 24 horas", "Servicios en un plazo de 24 horas"),
    ]),
    ("Luis Lizandro Alvitez Asalde", "Somos Perú", "partido-democratico-somos-peru", [
        P("gestion", "Software municipal de gestión integrada con marcación biométrica del personal y trazabilidad de los insumos de obra", 3, "Software Municipal de Gestión Integrada (SMGI)", "100 % de procesos críticos automatizados y 15 % de ahorro anual en gasto corriente"),
        P("economia", "Obras por administración directa con obreros del distrito, convenio con el sindicato local y maquinaria municipal propia", 4, "Punta Negra Construye", "100 % de la mano de obra no calificada en obras públicas asignada a vecinos"),
        P("urbano", "Oficina Municipal de Formalización para titular predios con COFOPRI, priorizando La Merced y Las Lomas", 5, "Oficina Municipal de Formalización"),
        P("gestion", "Catastro digital multifinalitario y un Fondo de Obras Distritales con lo que aumente la recaudación", 5, "Catastro Multifinalitario", "40 % más de recaudación propia"),
        P("agua_riesgos", "Mesa técnica permanente con el Ministerio de Vivienda y SEDAPAL para ampliar las redes de agua y desagüe", 6, "Mesa Técnica Permanente", "100 % de cobertura en servicios básicos de saneamiento"),
        P("social", "Policlínico municipal con urgencias 24 horas y programa «Punta Negra sin Anemia» con tamizaje a menores de 5 años y gestantes", 7, "Punta Negra sin Anemia", "Anemia infantil en 0 % y 1 ambulancia Tipo II activa 24/7"),
        P("social", "Centro «Mentes Brillantes» para niños con TDAH y síndrome de Down, y guardería municipal «Madre Trabajadora»", 7, "Mentes Brillantes", "1 centro y 1 guardería implementados"),
        P("transporte", "Plan «Verano Seguro y Ordenado»: cocheras municipales en la periferia y parqueo exclusivo para residentes cerca de las playas", 9, "Cocheras municipales en áreas periféricas"),
        P("seguridad", "Central de monitoreo C-360 con lectura de placas, drones y botón de pánico, y un policía en cada patrulla de serenazgo", 10, "Central de Monitoreo Inteligente (C-360)", "100 % de accesos monitoreados y 100 % de patrullas con presencia policial"),
        P("economia", "Terminal pesquero del sector sur con cadena de frío y formalización de embarcaciones ante FONDEPES", 10, "Terminal Pesquero del Sector Sur", "1 terminal pesquero operativo y 100 % de embarcaciones locales formalizadas"),
        P("ambiente", "Tasa de compensación vial y fiscalización ambiental de aire y ruido para las canteras", 11, "Tasa de Compensación Vial Obligatoria", "100 % de empresas mineras no metálicas reguladas y fiscalizadas"),
    ]),
    ("Miguel Ángel Saman Ballarta", "Frente de la Esperanza 2021", "partido-frente-de-la-esperanza-2021", [
        P("social", "Reforzamiento escolar, becas municipales, capacitación técnica y orientación vocacional", 4, "programas de reforzamiento escolar y becas municipales"),
        P("social", "Policlínico municipal, Farmacia Solidaria y campañas de salud preventiva", 4, "Policlínico Municipal, Farmacia Solidaria"),
        P("social", "Casa del Adulto Mayor y Centro Integral para Personas con Discapacidad, fortaleciendo el CIAM y la OMAPED", 4, "Fortalecer programas sociales, CIAM y OMAPED"),
        P("economia", "Bolsa de trabajo municipal y ferias laborales permanentes", 5, "ferias laborales permanentes"),
        P("economia", "Asesoría y formalización para emprendedores y pequeños comerciantes", 5, "Promover emprendimiento, formalización y asistencia técnica"),
        P("economia", "Mejorar el borde costero y los espacios turísticos del distrito", 5, "Mejoramiento del borde costero"),
        P("ambiente", "Proyecto integral de residuos sólidos: renovar la flota y ampliar la cobertura de recolección", 5, "renovar flota y ampliar cobertura de recolección"),
        P("ambiente", "Programa «Punta Negra Verde»: recuperar parques, arborizar y fortalecer el vivero municipal", 5, "fortalecer el vivero municipal"),
        P("agua_riesgos", "Plan distrital de adaptación al cambio climático y monitoreo ambiental", 5, "Plan Distrital de Adaptación al Cambio Climático"),
        P("seguridad", "Central de monitoreo, serenazgo motorizado y nuevas casetas de serenazgo, con patrullaje integrado", 5, "serenazgo motorizado y nuevas casetas"),
        P("gestion", "Audiencias públicas e informes periódicos de avance del plan, con seguimiento digital de obras y proyectos", 6, "audiencias públicas semestrales", "Audiencias semestrales e informes trimestrales"),
    ]),
    ("José Rubén Delgado Heredia", "Perú Moderno", "peru-moderno", [
        P("social", "Construir locales para los comedores populares y el Vaso de Leche, y comprar sus alimentos con estándares nutricionales", 5, "locales de los Comedores Populares"),
        P("social", "Convenio para instalar una universidad o un instituto técnico en el distrito", 5, "universidad y/o instituto técnico"),
        P("social", "Farmacia municipal con medicamentos a precios accesibles las 24 horas, gestionada ante el MINSA y la DIRIS Lima Sur", 5, "Farmacia Municipal"),
        P("social", "Casa de la Mujer y el Adulto Mayor con talleres de emprendimiento, protección de derechos y soporte social", 5, "Casa de la Mujer y el Adulto Mayor"),
        P("social", "Expediente técnico para recategorizar, ampliar y remodelar el Centro de Salud", 6, "recategorización del Centro de Salud"),
        P("economia", "Expedientes de obras en las playas Punta Rocas, La Pocita y Santa Rosa: accesos, iluminación y malecón", 6, "playa Punta Rocas"),
        P("economia", "Mejorar e implementar un mercado municipal de abastos formal", 6, "Mejoramiento e implementación de un mercado"),
        P("economia", "Cursos productivos y de formación de empresas, y apoyo a la pesca artesanal y a las asociaciones de emprendedores", 6, "Se impulsará la pesca artesanal"),
        P("agua_riesgos", "Gestionar ante SEDAPAL el expediente de ampliación de redes de agua, conexiones domiciliarias y alcantarillado", 7, "ampliación de redes de agua"),
        P("ambiente", "Contenedores de basura para mejorar la recolección y campañas de reciclaje y cuidado ambiental", 7, "adquiriendo contenedores de basura"),
        P("urbano", "Gestionar un programa integral de pavimentación que priorice la accesibilidad peatonal y vehicular", 7, "programa integral de pavimentación"),
    ]),
    ("Guillermo Eduardo Saco Vértiz Schwarz", "Progresemos", "progresemos", [
        P("social", "Centro Municipal de Atención Primaria con tarifas sociales y ambulancia municipal Tipo II", 8, "Centro Municipal de Atención Primaria"),
        P("social", "Puestos de salud básicos en los sectores norte, sur y este del distrito", 9, "sector norte, sur y este del distrito"),
        P("social", "Campañas de esterilización, vacunación y desparasitación, registro de mascotas y adopción responsable", 10, "Se esterilizará un mínimo de 100 animales por año", "Al menos 4 campañas; 100 animales esterilizados al año y 30 % menos animales abandonados al final de la gestión"),
        P("social", "Acondicionar la Casa de la Juventud con salas multiuso, música, arte y zona de estudio", 11, "Acondicionamiento de la Casa de la Juventud"),
        P("social", "Recuperar el Estadio Municipal Joaquín Ormeño como complejo deportivo, tras su saneamiento legal", 12, "Estadio Municipal Joaquín Ormeño"),
        P("economia", "Programa «Trabaja Punta Negra Todo el Año» con bolsa de trabajo y prioridad para vecinos en obras municipales", 13, "Trabaja Punta Negra Todo el Año"),
        P("economia", "Simplificar licencias, asesoría gratuita para formalizarse y ferias gastronómicas y artesanales todo el año", 15, "Simplificación de licencias de funcionamiento"),
        P("ambiente", "Proteger las Lomas de Caringa y Jime con un comité de gestión y rutas de ecoturismo", 15, "Lomas de Caringa y Jime"),
        P("ambiente", "Flota adecuada de recolectores, compostaje y biochar de residuos, y vivero municipal para reforestar", 16, "compostaje y biochar"),
        P("seguridad", "Centros de Auxilio Rápido integrados a la central de monitoreo y serenazgo descentralizado con patrullaje 24 horas", 14, "Centros de Auxilio Rápido (CAR)"),
        P("gestion", "Catastro, depuración del padrón de contribuyentes y digitalización del archivo municipal", 18, "Padrón Municipal de contribuyentes"),
    ]),
    ("Josué Jefferson de la Torre Bramón", "Renovación Popular", "renovacion-popular-peru", [
        P("seguridad", "Más equipamiento y capacitación anual de serenos, casetas de auxilio rápido, GPS en los vehículos y botón de pánico", 26, "Implementación de Casetas de Auxilio Rápido", "Todos los vehículos de serenazgo y rondas con GPS"),
        P("social", "Registro de jóvenes sin educación superior y becas mediante convenios con instituciones educativas", 17, "Mapeo y registro de jóvenes sin educación superior"),
        P("social", "Campaña «Muni Salud» contra la anemia y la desnutrición, focalizada en poblaciones vulnerables", 23, "CAMPAÑA INTEGRAL DE SALUD"),
        P("social", "«Hambre Cero»: ampliar los comedores populares, las ollas comunes y el Programa Articulado Nutricional", 31, "HAMBRE CERO"),
        P("social", "Casa Vecinal para actividades culturales y difusión de los servicios municipales de salud, educación y deporte", 33, "CASA VECINAL"),
        P("transporte", "Formalizar los estacionamientos y aprobar un plan regulador del transporte menor con empadronamiento de unidades", 35, "ESTACIONAMIENTOS FORMALES"),
        P("urbano", "Mantenimiento y construcción de pistas y veredas con el programa Mejoramiento Integral de Barrios y el FONCOMUN", 36, "Programa Mejoramiento Integral de Barrios"),
        P("economia", "Mirador turístico de Villa Mercedes, recorrido a las Lomas de Caringa, ferias culturales y concursos de surf", 42, "Mirador turístico de Villa Mercedes"),
        P("ambiente", "Más equipamiento de recolección, reciclaje en espacios públicos y manejo de residuos de la crianza de animales en el este", 47, "POR UNA PUNTA NEGRA SOSTENIBLE"),
        P("agua_riesgos", "Plan «Punta Negra Resiliente» ante El Niño: zonas vulnerables, plan de contingencia y simulacros", 50, "Punta Negra Resiliente"),
        P("gestion", "Sección «Punta Negra Informado» en la web con personal, contratos, montos y avance de proyectos", 56, "PUNTA NEGRA INFORMADO"),
    ]),
]
