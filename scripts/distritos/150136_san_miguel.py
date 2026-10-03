"""San Miguel (150136): propuestas principales de los 8 planes de gobierno inscritos ante el JNE.

Cada propuesta está redactada con palabras propias y lleva:
  - pagina: la página del PDF oficial donde aparece.
  - ancla: un fragmento textual del PDF que DEBE aparecer en esa página. El generador lo verifica y
    falla si no lo encuentra, para que ninguna cita apunte a una página equivocada.
Mismo criterio para todas: entre 8 y 11 propuestas por plan, repartidas en los temas que el plan desarrolla.
"""

UBIGEO = "150136"

def P(tema, texto, pagina, ancla, meta=None):
    return {"tema": tema, "texto": texto, "meta": meta, "pagina": pagina, "ancla": ancla}

# (nombre, organización, archivo PDF, propuestas)
PLANES = [
    ("Juan José Guevara Bonilla", "Acción Popular", "accion-popular", [
        P("seguridad", "Reactivar el «Grupo Sombra», personal municipal de inteligencia y operaciones encubiertas contra bandas y en puntos críticos", 5, "Reactivación del GRUPO SOMBRA"),
        P("seguridad", "Más serenos capacitados, cámaras con reconocimiento facial y de placas, y sectorización policial con un jefe de sector PNP", 5, "Sectorización operativa policial"),
        P("transporte", "Semáforos, señalización y dispositivos de control en intersecciones críticas, mediante convenios con la Municipalidad de Lima", 6, "intersecciones críticas del distrito"),
        P("transporte", "Fiscalizar los locales de espectáculos masivos, exigir planes de mitigación vial y restringir permisos ante riesgo de colapso vial", 6, "Regulación y fiscalización estricta de locales de espectáculos masivos"),
        P("urbano", "Reparación intensiva de pistas y veredas, y retiro de vehículos abandonados en la vía pública con la PNP", 10, "100% de pistas principales reparadas integralmente", "100 % de pistas principales reparadas"),
        P("social", "Construir y remodelar complejos deportivos y recuperar losas para uso gratuito de niños y jóvenes", 7, "losas deportivas para ser puestos a disposición del deporte"),
        P("social", "Reabrir la Cuna Jardín Municipal para madres trabajadoras y modernizar el CIAM, la OMAPED y Juventudes", 7, "Reapertura y equipamiento de la Cuna Jardín Municipal"),
        P("urbano", "Auditoría técnica de las licencias de construcción emitidas y paralización de obras ilegales", 7, "Auditoría técnica exhaustiva a todas las licencias de construcción"),
        P("economia", "Licencias sin trámites excesivos para mypes de bajo riesgo, mercados itinerantes y renovación del mobiliario del comercio autorizado", 8, "para licencias MYPE de bajo riesgo"),
        P("ambiente", "Retirar pantallas LED que iluminen viviendas, no autorizar megaconciertos junto a la Costa Verde y controlar el ruido con sonómetros", 8, "Prohibición absoluta de permisos para megaconciertos"),
        P("gestion", "Centro de Comando Vecinal 24/7 con tickets digitales para seguir cada queja y digitalización de los trámites más comunes", 9, "Centro de Comando Vecinal 24/7", "100 % de quejas atendidas y 100 % de trámites en línea"),
    ]),
    (None, "Avanza País", "avanza-pais-partido-de-integracion-social", [
        P("seguridad", "Programa «Geoseguridad & IA» con Centro de Control Inteligente y más cámaras de videovigilancia", 7, "Implementación integral del Centro de Control Inteligente", "80 % de cobertura de vigilancia inteligente y 40 % más cámaras"),
        P("seguridad", "Renovar la flota del serenazgo, con bodycams y GPS, y ampliar el patrullaje integrado con la PNP", 8, "Implementación de bodycams y GPS", "20 vehículos, 20 motocicletas y 20 % más patrullaje integrado"),
        P("social", "Centro Odontológico, Laboratorio y Centro de Rehabilitación Física municipales, con campañas de salud preventiva", 11, "01 Centro Odontológico Municipal", "50 campañas de salud preventiva"),
        P("social", "Campañas de salud veterinaria, ferias de adopción y nuevos espacios públicos para mascotas (Rocket Parks)", 12, "90% de mascotas empadronadas", "90 % de mascotas empadronadas y 02 nuevos Rocket Park"),
        P("social", "Academias deportivas municipales, becas deportivas y una piscina temperada adicional", 14, "4,000 jóvenes inscritos en las academias deportivas", "1 piscina temperada y 4 000 jóvenes inscritos en academias"),
        P("social", "Gran Centro del Vecino y del Adulto Mayor con piscina, canchas y salones, y fortalecimiento del CIAM", 16, "Gran Centro del Vecino y del Adulto Mayor", "4 000 adultos mayores participantes"),
        P("economia", "Casa del Emprendedor con coworking y aulas de capacitación, y ruedas de negocios anuales", 18, "3,000 emprendedores beneficiados", "3 000 emprendedores beneficiados y 2 ruedas de negocios al año"),
        P("economia", "Bolsa laboral digital municipal, ferias de empleo y certificación de competencias laborales", 19, "Bolsa laboral digital municipal", "2 000 personas insertadas laboralmente"),
        P("ambiente", "Programa «San Miguel Circular y Limpio 2030»: kits de segregación, campañas de reciclaje y convenios con recicladoras", 20, "Entrega de kits de segregación", "70 % de viviendas que segregan residuos"),
        P("transporte", "Semaforización inteligente, optimización de flujos vehiculares y gestión digital del tránsito", 22, "Implementación de semaforización inteligente", "20 % de tiempos promedio de desplazamiento"),
        P("gestion", "Digitalizar los trámites municipales con expediente electrónico y automatización de procesos", 24, "100% de trámites digitalizados", "100 % de trámites digitalizados"),
    ]),
    ("Santiago Nicolás Barreda Arias", "Partido Aprista Peruano", "partido-aprista-peruano", [
        P("seguridad", "Programa «Barrio seguro» con videovigilancia en tiempo real, patrullaje integrado, juntas vecinales y aplicativo «Mi distrito seguro»", 9, "Instalar y modernizar 200 cámaras de videovigilancia", "Reducir la delincuencia en 80 %, 200 cámaras y al menos 40 % menos tiempo de respuesta"),
        P("social", "Programas sociales inclusivos con capacitación laboral, talleres y atención a adultos mayores, jóvenes y población vulnerable", 10, "Implementar al menos 10 programas sociales sostenibles", "Al menos 10 programas sociales"),
        P("urbano", "Actualizar el plan urbano distrital, fiscalizar construcciones y uso del suelo, y recuperar espacios públicos", 10, "Reducir las construcciones informales en 25%", "25 % menos construcciones informales y al menos 50 espacios públicos recuperados"),
        P("economia", "Ferias comerciales permanentes y capacitación en gestión empresarial, marketing digital y finanzas para emprendedores", 11, "Capacitar a más de 1,000 emprendedores", "30 % más creación de negocios formales y más de 1 000 emprendedores capacitados"),
        P("economia", "Ventanilla única digital, eliminación de requisitos innecesarios y licencias rápidas para pequeños negocios", 12, "Implementar licencias en plazos cortos (fast track)", "50 % menos tiempo de trámite"),
        P("economia", "Bolsa de trabajo municipal, convenios con empresas locales y ferias laborales periódicas", 13, "Insertar laboralmente a al menos 2,000 vecinos", "Al menos 2 000 vecinos insertados laboralmente"),
        P("ambiente", "Monitoreo de ruido y aire en zonas críticas, incluida la contaminación sonora de los aviones del aeropuerto Jorge Chávez", 13, "resolver la contaminación sonora generada por los aviones", "20 % menos contaminación ambiental y sonora"),
        P("ambiente", "Recuperación de parques y jardines con riego tecnificado y adopción de parques por los vecinos", 14, "Recuperar y mantener al menos el 90% de áreas verdes", "Al menos 90 % de las áreas verdes"),
        P("ambiente", "Rutas inteligentes de recolección, nuevas compactadoras y segregación en la fuente con recicladores formalizados", 14, "Adquisición de compactadoras modernas", "100 % de cobertura de limpieza pública"),
        P("social", "Construcción y recuperación de losas deportivas, circuitos deportivos y zonas de actividad física", 14, "Construir o recuperar al menos 20 espacios deportivos", "Al menos 20 espacios deportivos"),
        P("gestion", "Gobierno Abierto Municipal con portal de transparencia en tiempo real y publicación mensual de la ejecución presupuestal", 15, "Implementación de un sistema de Gobierno Abierto Municipal", "100 % de la información relevante de gestión publicada"),
    ]),
    ("Michael Alberto Paredes Torres", "Partido del Buen Gobierno", "partido-del-buen-gobierno", [
        P("social", "Un policlínico municipal adicional, ampliar «El médico te visita» a población vulnerable y gestionar otra ambulancia", 6, "se implementará un policlínico municipal adicional"),
        P("social", "Programa municipal con el MINEDU y el sector privado para reducir la deserción escolar y los jóvenes que no estudian", 14, "se reduce a la mitad el porcentaje de niños que abandonan", "Reducir a la mitad la deserción escolar y los jóvenes que no estudian, frente a 2026"),
        P("seguridad", "Plan preventivo contra las extorsiones y prevención comunitaria en las zonas críticas del mapa delictivo", 8, "implementar un plan preventivo contra las extorsiones"),
        P("seguridad", "Más equipamiento del serenazgo, ampliación de cámaras, alarmas vecinales, nuevas bases de seguridad y herramientas de IA", 8, "se construirán nuevas bases de seguridad en zonas estratégicas"),
        P("agua_riesgos", "Revisar las concesiones a empresas de conciertos masivos en la Costa Verde para reducir riesgos", 8, "se revisarán los contratos de concesión con las empresas de espectáculos"),
        P("agua_riesgos", "Simulacros de sismo por urbanización, mantenimiento de pozos de agua de emergencia con Sedapal y tambos de emergencia", 9, "se instalarán tambos de emergencia en puntos estratégicos"),
        P("transporte", "Señalización, semaforización, campañas de seguridad vial, más ciclovías y planes para las intersecciones críticas", 9, "en las quince intersecciones y zonas críticas identificadas"),
        P("ambiente", "Recolección selectiva con recicladores formalizados, planta de compostaje y ecopuntos para residuos eléctricos, aceite y pilas", 16, "35% de viviendas priorizadas, incorporadas a segregación en fuente", "35 % de viviendas priorizadas segregando y al menos 8 ecopuntos o campañas móviles"),
        P("ambiente", "Plan Distrital de Arbolado con inventario georreferenciado, corredores verdes y especies de bajo consumo de agua", 16, "hay cinco mil árboles nuevos o repuestos", "5 000 árboles nuevos o repuestos y 20 000 m² de áreas verdes nuevas o rehabilitadas"),
        P("economia", "Centro de Promoción del Empleo con el Ministerio de Trabajo y un programa piloto para jóvenes que no estudian ni trabajan", 12, "Centro de Promoción del Empleo"),
        P("gestion", "Ventanilla virtual, carpeta ciudadana, TUPA en línea y pagos y seguimiento de expedientes por internet", 13, "se implementará una ventanilla virtual y una carpeta ciudadana municipal"),
    ]),
    ("Carolina Mannucci Arámbulo", "Somos Perú", "partido-democratico-somos-peru", [
        P("seguridad", "Vigilancia integrada con cámaras modernizadas en zonas críticas", 5, "Instalar y modernizar 100% de cámaras en zonas críticas", "30 % menos delitos menores y 100 % de cámaras en zonas críticas"),
        P("seguridad", "Juntas vecinales de seguridad en todos los sectores del distrito", 5, "Implementar juntas vecinales en todos los sectores del distrito"),
        P("social", "Programas deportivos y culturales permanentes en todos los sectores y recuperación de espacios recreativos", 5, "Recuperar y habilitar 20 espacios públicos recreativos", "20 espacios públicos recreativos"),
        P("social", "Campañas integrales de salud y campañas veterinarias gratuitas permanentes", 5, "Realizar campañas integrales trimestrales de salud", "Campañas de salud trimestrales"),
        P("economia", "Capacitación a emprendedores y ferias comerciales mensuales", 6, "Capacitar a más de 3,000 emprendedores", "Más de 3 000 emprendedores capacitados"),
        P("economia", "Formalizar el comercio informal y recuperar espacios públicos ocupados", 6, "Formalizar 40% de comercios informales", "40 % de comercios informales formalizados"),
        P("gestion", "Digitalizar los trámites prioritarios y crear una plataforma integral de atención virtual al vecino", 6, "Digitalizar el 100% de trámites prioritarios", "100 % de trámites prioritarios y 60 % menos tiempo de atención"),
        P("ambiente", "Programas de segregación de residuos en todos los sectores y campañas ambientales permanentes", 6, "Incrementar en 50% el reciclaje distrital", "50 % más reciclaje"),
        P("urbano", "Recuperar parques, ampliar áreas verdes por habitante y mantener los espacios públicos", 7, "Recuperar y mejorar el 100% de parques priorizados", "100 % de parques priorizados"),
        P("social", "Programa distrital permanente de bienestar animal con campañas masivas de esterilización", 7, "Ejecutar campañas masivas de esterilización"),
        P("gestion", "Rendiciones de cuentas trimestrales, audiencias públicas descentralizadas y mesas de trabajo por sector", 7, "Realizar rendiciones de cuentas trimestrales"),
    ]),
    ("Jorge Luis Moreno Morán", "Perú Moderno", "peru-moderno", [
        P("seguridad", "Sistema Inteligente de Seguridad Ciudadana con cámaras inteligentes, drones y Central de Monitoreo modernizada", 7, "Implementación de drones para vigilancia preventiva"),
        P("seguridad", "Plan Cerco con los distritos colindantes, patrullaje integrado con la PNP y renovación de la flota del serenazgo", 7, "Implementación del Plan Cerco con distritos colindantes"),
        P("social", "Atención domiciliaria para adultos mayores, campañas médicas descentralizadas y talleres de salud mental", 8, "Programa de atención domiciliaria para adultos mayores"),
        P("social", "Escuelas deportivas municipales, talleres culturales permanentes y programas de liderazgo juvenil", 8, "Escuelas deportivas municipales"),
        P("social", "Veterinaria Municipal, registro distrital de mascotas y campañas de esterilización y vacunación", 9, "Implementación de la Veterinaria Municipal de San Miguel"),
        P("economia", "Programa «San Miguel Emprende» con ferias, capacitaciones gratuitas y asistencia para la formalización", 10, "Beneficiar a más de 2,000 emprendedores", "Más de 2 000 emprendedores beneficiados"),
        P("economia", "Bolsa Laboral Municipal, ferias laborales descentralizadas y convenios con empresas para prácticas y empleo", 10, "Implementación de la Bolsa Laboral Municipal"),
        P("economia", "Ventanilla única y licencia de funcionamiento simplificada, con trámites empresariales digitales", 10, "Ventanilla única para emprendedores"),
        P("ambiente", "Programa «Recicla San Miguel» con tachos diferenciados para vecinos puntuales, recolección selectiva semanal y puntos ecológicos", 11, "Entrega progresiva de tachos diferenciados", "50 % más reciclaje domiciliario"),
        P("urbano", "Luminarias LED, cruces peatonales inteligentes y pasos peatonales a desnivel en zonas priorizadas", 12, "Construcción de pasos peatonales a desnivel"),
        P("gestion", "Programa «Martes y Jueves Democráticos», audiencias públicas trimestrales y portal de seguimiento de metas", 13, "Audiencias públicas trimestrales"),
    ]),
    ("Napoleón Roberto Martínez Merizalde Huatuco", "Progresemos", "progresemos", [
        P("seguridad", "Cámaras con IA, drones y un centro de control que integre casetas, patrullas y serenos, con patrullaje por cuadrantes", 11, "Diseño e Implementación de un Centro de Control Moderno"),
        P("social", "Fortalecer la DEMUNA y los convenios con Centros de Emergencia Mujer, con atención psicológica gratuita y orientación legal", 15, "Módulos municipales de orientación legal"),
        P("social", "Campañas de tamizaje de hipertensión, diabetes, anemia y salud mental en parques, colegios y espacios comunales", 18, "Implementar campañas periódicas de tamizaje"),
        P("social", "Complejo deportivo de alto rendimiento, losas con grass sintético e iluminación LED y remodelación del Skate Park", 23, "Remodelación integral del Skate Park de San Miguel"),
        P("transporte", "Semáforos inteligentes y modernización de la señalización vial para mejorar el flujo vehicular", 26, "Implementación de semáforos inteligentes y modernización del sistema de señalización vial"),
        P("urbano", "Fiscalizar el crecimiento inmobiliario para que respete los parámetros urbanísticos y la residencialidad", 27, "Fiscalización y ordenamiento del crecimiento inmobiliario"),
        P("social", "Atención médica domiciliaria para adultos mayores con movilidad reducida y fortalecimiento del CIAM", 31, "Implementación del Programa de Atención Médica Domiciliaria"),
        P("economia", "Bolsa laboral «Empleo San Miguel» y programa «Te Ayudo a Emprender» con capacitación gratuita", 40, "Creación del programa TE AYUDO A EMPRENDER"),
        P("economia", "Proyecto Costanera San Miguel: recuperar playas y crear malecones, ciclovías y miradores para el turismo", 43, "Ejecución del Proyecto Costanera San Miguel"),
        P("ambiente", "Plan de arborización «San Miguel Verde» con especies nativas y corredores ecológicos", 52, "Plan Distrital de Arborización Urbana"),
        P("gestion", "Plataforma «Decide San Miguel» para propuestas y consultas, y cabildos abiertos descentralizados", 59, "Plataforma Digital de Participación Ciudadana"),
    ]),
    ("Marcos Enrique Cabrera Porras", "Renovación Popular", "renovacion-popular-peru", [
        P("seguridad", "Centro de Alto Rendimiento Táctico para entrenar al serenazgo con simuladores, polígono virtual y formación jurídica", 17, "Centro de Alto Rendimiento Táctico para Seguridad Ciudadana", "Al menos 40 % menos delitos patrimoniales"),
        P("seguridad", "Red de videovigilancia con IA, lectura de placas en los accesos del distrito y cámaras corporales para todo el serenazgo", 18, "Despliegue de 1,200 cámaras IP de alta definición", "1 200 cámaras y lectura de placas en 12 accesos"),
        P("agua_riesgos", "Alerta temprana de sismos y tsunamis con sirenas en la Costa Verde, brigadistas y almacén de ayuda humanitaria", 19, "sistema de alerta temprana de sismos y tsunamis", "Kits de emergencia para al menos 5 000 familias en las primeras 72 horas"),
        P("social", "Hospitales de la Solidaridad con especialidades y laboratorio, y programa contra la anemia", 20, "Instalaremos 2 Hospitales de la Solidaridad", "2 hospitales"),
        P("economia", "Programa «Licencia rápida, digital y segura» para abrir empresas de riesgo bajo y medio", 22, "digitalizar al 100% el proceso de apertura de empresas", "100 % del proceso de apertura digitalizado"),
        P("social", "Dos cunas municipales, gimnasios municipales y espacios «club del vecino» en las siete zonas del distrito", 22, "Fomentaremos la creación de dos cuna municipales"),
        P("urbano", "Proponer en la Costa Verde un terminal de cruceros, un circuito peatonal y de ciclovías, y accesos a playas con ascensores y rampas", 23, "Terminal de Cruceros de San Miguel"),
        P("urbano", "Auditoría de licencias, control de alturas y catastro 3D con drones para detectar construcciones no declaradas", 24, "Catastro 3D y Predial Justo"),
        P("transporte", "Sincronización adaptativa de semáforos en La Marina, Universitaria, Faucett, Costanera y Riva Agüero, y zonas 30 junto a colegios", 25, "Sincronización adaptativa de semáforos"),
        P("ambiente", "Rutas de recolección optimizadas y puntos limpios con descuentos en arbitrios por reciclaje", 26, "Reducción del 25% del volumen de residuos", "25 % menos residuos al relleno sanitario"),
        P("gestion", "App «San Miguel Conmigo» con trámites, pagos y reporte georreferenciado de problemas", 28, "Garantizar que el 90% de los trámites municipales", "90 % de trámites en línea al cierre de la gestión"),
    ]),
]
