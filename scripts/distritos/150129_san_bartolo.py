"""San Bartolo (150129): propuestas principales de los planes de gobierno inscritos ante el JNE.

Cada propuesta está redactada con palabras propias y lleva:
  - pagina: la página del PDF oficial donde aparece.
  - ancla: un fragmento textual del PDF que DEBE aparecer en esa página. El generador lo verifica y
    falla si no lo encuentra, para que ninguna cita apunte a una página equivocada.
Mismo criterio para todas: entre 8 y 11 propuestas por plan, repartidas en los temas que el plan desarrolla.
"""

UBIGEO = "150129"

def P(tema, texto, pagina, ancla, meta=None):
    return {"tema": tema, "texto": texto, "meta": meta, "pagina": pagina, "ancla": ancla}

# (nombre, organización, archivo PDF, propuestas)
PLANES = [
    ("Yliana Elisa Castro Gregorio", "Alianza para el Progreso", "alianza-para-el-progreso", [
        P("seguridad", "Cámaras de videovigilancia con reconocimiento facial en puntos críticos, conectadas a una central de monitoreo las 24 horas", 7, "Instalación de al menos 30 cámaras de videovigilancia", "30 cámaras instaladas y 20 % menos denuncias en 2027–2030"),
        P("social", "Gestionar ante el MINSA la mejora y el equipamiento del Centro Materno Infantil (categoría I-4), con urgencias y sala de partos", 7, "Centro Materno Infantil, de Categoría I-4", "4 campañas anuales de especialidades médicas complementarias"),
        P("social", "Gestionar el reemplazo de las aulas prefabricadas del colegio Víctor Morón Muñoz por aulas de material noble", 9, "sustitución de las 13 aulas prefabricadas", "13 aulas nuevas construidas"),
        P("agua_riesgos", "Gestionar ante SEDAPAL más presión en la red y mayor almacenamiento para evitar cortes de agua en verano", 8, "Gestionar ante SEDAPAL la optimización de las presiones", "24 horas de continuidad del servicio de agua durante todo el año"),
        P("agua_riesgos", "Mapa de riesgos y plan de evacuación ante sismos y tsunamis, con rutas señalizadas, simulacros y brigadas vecinales", 11, "Plan de Evacuación Distrital ante sismos y tsunamis", "2 simulacros por año y 500 familias capacitadas al 2030"),
        P("transporte", "Oficina Municipal de Transporte Urbano, empadronamiento de mototaxis y formalización de rutas y paraderos", 8, "Creación de la Oficina Municipal de Transporte Urbano", "100 % de rutas formalizadas al 2030"),
        P("urbano", "Plan de rehabilitación de pistas y construcción de veredas, priorizando las avenidas de mayor circulación", 8, "Plan de mejoramiento de pistas y veredas", "5 km de pistas y veredas rehabilitadas"),
        P("ambiente", "Recuperar y crear parques y jardines con riego por goteo, y plantar árboles nativos de la costa", 10, "Plantación de al menos 500 árboles nativos", "4 m² de área verde por habitante al 2030 y al menos 500 árboles"),
        P("economia", "Reducir el plazo de las licencias de funcionamiento y crear una ventanilla única empresarial", 12, "reducción del plazo de emisión de licencias de funcionamiento de 30 días", "Licencias en un máximo de 7 días hábiles"),
        P("economia", "Ruta Turística Oficial (playas, Curayacu, Lomas, Mirador Cahuide) y sello de calidad «Sabor San Bartolo» para restaurantes", 12, "Creación de la Ruta Turística Oficial de San Bartolo", "20 % más visitantes y 30 establecimientos con sello al 2030"),
        P("gestion", "Publicación mensual de la información financiera, cabildos abiertos trimestrales y sistema de control interno", 14, "Cabildos abiertos trimestrales", "4 cabildos por año y 100 % de la información financiera publicada cada mes"),
    ]),
    ("Rufino Enciso Ríos", "Somos Perú", "partido-democratico-somos-peru", [
        P("seguridad", "Programa «San Bartolo Seguro 24 Horas»: capacitación y equipamiento del serenazgo y patrullaje preventivo con la PNP", 8, "Fortalecimiento del Serenazgo Municipal"),
        P("seguridad", "Más cámaras en puntos estratégicos y canal «Alerta San Bartolo» de comunicación rápida entre vecinos y autoridades", 8, "Programa Alerta San Bartolo"),
        P("agua_riesgos", "Simulacros, capacitación ciudadana y señalización de rutas de evacuación ante emergencias", 9, "señalización de rutas de evacuación"),
        P("economia", "Programa «San Bartolo Todo el Año»: calendario turístico anual con festivales gastronómicos, culturales y deportivos", 9, "Calendario Turístico Anual de San Bartolo"),
        P("economia", "Apoyo a la pesca artesanal y promoción de los productos marinos locales en la oferta turística", 10, "Promoción de productos hidrobiológicos locales"),
        P("urbano", "Programa «Tu Predio Seguro»: orientación gratuita en saneamiento físico legal y formalización de la propiedad", 11, "Orientación gratuita sobre saneamiento físico legal"),
        P("social", "Convenios con SISOL y jornadas médicas descentralizadas con campañas de salud preventiva", 13, "Gestión de convenios con SISOL"),
        P("social", "Casa de la Juventud con talleres de capacitación, orientación vocacional y programas culturales", 16, "Impulsaremos espacios destinados al desarrollo juvenil"),
        P("ambiente", "Programa «Playas limpias todo el año» con jornadas permanentes de limpieza y educación ambiental", 14, "PLAYAS LIMPIAS TODO EL AÑO"),
        P("ambiente", "Ruta Ecoturística de las Lomas de Cicasos con senderos y miradores, y voluntariado «Guardianes de las Lomas»", 19, "Guardianes de las Lomas de Cicasos"),
        P("gestion", "Mesa de partes virtual, consulta de expedientes en línea y atención municipal itinerante en los barrios", 18, "Consulta virtual de expedientes"),
    ]),
    ("Fernando Juan Amador Loayza Garate", "PPC", "partido-popular-cristiano-ppc", [
        P("urbano", "Acompañar la formalización y titulación de predios con COFOPRI y SUNARP, y actualizar el catastro", 9, "procesos de formalización y titulación con COFOPRI y SUNARP"),
        P("urbano", "Programa integral de pistas y veredas y mejoramiento de plazas, parques y áreas verdes", 9, "Programa integral de pistas y veredas"),
        P("transporte", "Estacionamientos regulados y accesibilidad universal", 9, "Implementación de estacionamientos regulados"),
        P("seguridad", "Fortalecer el serenazgo y modernizar el sistema de videovigilancia", 10, "Fortalecimiento operativo y tecnológico del Serenazgo"),
        P("seguridad", "Patrullaje integrado con la PNP, patrullaje a pie en zonas críticas y sectorización del distrito", 10, "Patrullaje integrado con la Policía Nacional"),
        P("agua_riesgos", "Escuadrón Municipal de Rescate con ambulancia y equipo para rescates en playas, y simulacros ante sismos y tsunamis", 10, "Escuadrón Municipal de Rescate"),
        P("economia", "Calendario anual de actividades deportivas, culturales y náuticas para atraer turismo todo el año", 11, "Calendario anual de actividades deportivas, culturales y náuticas"),
        P("ambiente", "Programa «Mar Limpio» con captura de residuos flotantes, mallas de retención y jornadas de limpieza", 12, "sistemas de captura de residuos flotantes"),
        P("ambiente", "Parque Forestal Loma Cicasos (1 380 ha) para conservación y ecoturismo, y protección de las bahías Norte y Sur", 12, "Parque Forestal Loma Cicasos"),
        P("gestion", "Reingeniería municipal y gobierno digital con trámites en línea y seguimiento de expedientes", 13, "seguimiento digital de expedientes", "Reducir sobrecostos y trámites innecesarios en al menos 20 % durante el período"),
        P("social", "Programa «San Bartolo Joven» (escuelas deportivas, talleres culturales, liderazgo) y apoyo al Grupo Scout Marino", 13, "Programa San Bartolo Joven"),
    ]),
    (None, "Podemos Perú", "podemos-peru", [
        P("seguridad", "Cámaras en todos los puntos críticos conectadas a la central de serenazgo y un aplicativo de seguimiento de la delincuencia", 7, "interconectados con la central de serenazgo"),
        P("seguridad", "Ejecutar el plan local de seguridad ciudadana con seguimiento mensual y coordinación con la PNP y el Ministerio Público", 10, "plan local de seguridad ciudadana con seguimiento mensual"),
        P("social", "Grupo de serenazgo femenino de apoyo a mujeres afectadas por maltrato y mayor atención a la DEMUNA", 9, "formar un grupo de serenazgo femenino"),
        P("ambiente", "Mejorar la limpieza pública, el recojo de desmonte y el barrido, extendiéndolos a playas y zonas periféricas", 7, "mejorara el sistema de limpieza pública y recojo de desmonte"),
        P("urbano", "Construir pistas y veredas en los grupos residenciales que aún no las tienen", 11, "Construcción de pistas y veredas en los grupos faltantes"),
        P("urbano", "Saneamiento físico legal de urbanizaciones de la ampliación urbana (Miguel Grau Seminario, Las Orquídeas, Javier Pérez de Cuéllar)", 14, "regularizaremos la propiedad de los centros poblados"),
        P("agua_riesgos", "Instalar o ampliar las redes de agua y desagüe en la ampliación urbana", 11, "ampliación de las redes de Agua y Desagüe"),
        P("agua_riesgos", "Gestionar ante el Gobierno central la remodelación de los malecones Sur, Norte y Peñascal y de sus muros de contención frente al oleaje", 14, "remodelación de los malecones sur y norte y peñascal"),
        P("social", "Equipar los colegios (laboratorios, bibliotecas virtuales, internet) y ampliar el área informática del colegio Víctor Morón Muñoz", 12, "Gestionar equipamiento de todos los centros educativos"),
        P("social", "Crear un albergue para los adultos mayores más necesitados", 12, "Crear e implementar un albergue"),
        P("economia", "Priorizar la contratación de mano de obra local, asesorar a microempresas y apoyar la mejora de los mercados de abastos", 11, "la contratación de mano de obra del distrito"),
    ]),
    ("Yolanda Chávez Rubio", "Renovación Popular", "renovacion-popular-peru", [
        P("agua_riesgos", "Ampliar el acceso a agua potable, luz y alcantarillado en coordinación con el Gobierno central", 2, "Ampliar el acceso a agua potable, luz y alcantarillado"),
        P("social", "Mejorar el Centro de Salud de San Bartolo (MINSA) con más infraestructura, médicos y equipamiento", 2, "Mejorar el Centro de Salud de San Bartolo"),
        P("social", "Crear un Hospital de la Solidaridad en convenio con el MINSA", 2, "Crear un Hospital de la Solidaridad"),
        P("seguridad", "Cámaras de vigilancia, patrullaje integrado de serenazgo y PNP y participación de las juntas vecinales", 2, "patrullaje integrado entre serenazgo y Policía Nacional"),
        P("social", "Academias gratuitas, talleres técnicos desde los 12 años y un Centro Superior de Estudios Municipales con carreras técnicas", 2, "Centro Superior de Estudios Municipales"),
        P("economia", "Formalizar mypes, con énfasis en mujeres, jóvenes y personas vulnerables", 2, "Formalizar MYPES, con énfasis en mujeres"),
        P("economia", "Impulsar el turismo sostenible: hospedajes, gastronomía, deportes acuáticos y ferias culturales", 2, "Impulsar turismo sostenible"),
        P("ambiente", "Ampliar el vivero municipal y la arborización con la campaña «Adopta un árbol»", 3, "Incrementar el vivero municipal"),
        P("ambiente", "Programas de reciclaje y manejo integral de residuos sólidos", 3, "Implementar programas de reciclaje y manejo integral"),
        P("gestion", "Trámites en plataformas digitales, portal de rendición de cuentas y auditorías externas", 3, "auditorías externas anuales", "Auditorías externas cada año"),
        P("gestion", "Actualizar el catastro en zonas periféricas, incentivos al buen contribuyente y fiscalización con drones y cámaras", 3, "Fiscalización inteligente con drones"),
    ]),
]
