"""Ancón (150102): propuestas principales de los planes de gobierno inscritos ante el JNE.

Cada propuesta está redactada con palabras propias y lleva:
  - pagina: la página del PDF oficial donde aparece.
  - ancla: un fragmento textual del PDF que DEBE aparecer en esa página. El generador lo verifica y
    falla si no lo encuentra, para que ninguna cita apunte a una página equivocada.
Mismo criterio para todas: entre 8 y 11 propuestas por plan, repartidas en los temas que el plan desarrolla.
Los planes de Fuerza Popular y Somos Perú son escaneados: su texto proviene de OCR y las metas se
contrastaron con la imagen de la página.
"""

UBIGEO = "150102"

def P(tema, texto, pagina, ancla, meta=None):
    return {"tema": tema, "texto": texto, "meta": meta, "pagina": pagina, "ancla": ancla}

# (nombre, organización, archivo PDF, propuestas)
PLANES = [
    ("Lauro Cristóbal Muñoz Soldevilla", "Fuerza Popular", "fuerza-popular", [
        P("social", "Academia Municipal Preuniversitaria gratuita", 20, "Preuniversitaria gratuita", "1 000 estudiantes beneficiados por año"),
        P("social", "Programa «Ancón sin Anemia» contra la anemia infantil", 20, "Ancón sin Anemia", "Reducir en 50 % la anemia infantil"),
        P("seguridad", "Centrales de videovigilancia inteligente y nuevas cámaras en Villas de Ancón, Cercado y km 39", 22, "Cámaras de videovigilancia", "150 cámaras operativas y 3 centrales de videovigilancia"),
        P("seguridad", "Gestionar ante el Ministerio del Interior la construcción de la Comisaría Los Rosales – Ancón Norte (km 39)", 22, "Los Rosales"),
        P("urbano", "Programa «Titulación para Todos» y actualización del catastro digital del distrito", 22, "Titulación para Todos", "4 000 predios y 70 % de cobertura catastral"),
        P("economia", "Bolsa de Trabajo Municipal y convenios con empresas del corredor logístico e industrial del norte", 24, "Bolsa de Trabajo Municipal implementada", "1 000 nuevos empleos formales al 2030"),
        P("economia", "Licencias de funcionamiento emitidas en 24 horas", 24, "Licencias de funcionamiento emitidas en 24 horas", "90 % de cumplimiento"),
        P("ambiente", "Planta de valorización de residuos sólidos y programa de segregación y reciclaje en la fuente", 26, "Planta de Valorización de Residuos Sólidos implementada", "1 planta y 8 000 hogares incorporados a la segregación"),
        P("agua_riesgos", "Proyecto de atrapanieblas en Pasamayo y laderas de Ancón para recuperar áreas verdes", 26, "Proyecto Atrapanieblas para Pasamayo", "3 proyectos ejecutados"),
        P("transporte", "Programa «Ancón en Bicicleta» con construcción de ciclovías y gestión de rutas integradas con la ATU", 27, "Programa Ancón en Bicicleta implementado"),
        P("gestion", "Municipalidad digital con expediente electrónico, mesa de partes virtual y plataforma de seguimiento de obras", 30, "Municipalidad Digital 90%"),
    ]),
    ("Pedro John Barrera Bernui", "Somos Perú", "partido-democratico-somos-peru", [
        P("social", "Campañas de salud y apoyo social en los distintos sectores del distrito", 5, "Realizar campañas de salud y apoyo social"),
        P("social", "Talleres educativos, culturales y deportivos para niños y jóvenes", 5, "Implementar talleres educativos, culturales y deportivos"),
        P("social", "Programas de apoyo para adultos mayores y madres de familia", 5, "Fortalecer programas de apoyo para adultos mayores y madres de familia"),
        P("urbano", "Recuperar y mejorar espacios recreativos y comunitarios", 5, "Recuperar y mejorar espacios recreativos y comunitarios"),
        P("economia", "Ferias y capacitaciones para emprendedores y comerciantes locales", 6, "Realizar ferias para emprendedores y comerciantes locales"),
        P("economia", "Programas y convenios para generar oportunidades laborales", 6, "Gestionar programas y convenios para fomentar oportunidades laborales"),
        P("economia", "Espacios adecuados para un comercio formal y ordenado", 6, "Promover espacios adecuados para el comercio formal y ordenado"),
        P("ambiente", "Campañas de limpieza y reciclaje, y programas de arborización y recuperación de áreas verdes", 6, "Ejecutar campañas de limpieza y reciclaje"),
        P("ambiente", "Fortalecer el servicio de recolección de residuos sólidos", 7, "Fortalecer el servicio de recolección de residuos sólidos"),
        P("gestion", "Digitalizar y modernizar los trámites municipales", 7, "Impulsar la digitalización y modernización de trámites municipales"),
        P("gestion", "Reuniones descentralizadas con dirigentes y vecinos, y mecanismos de participación vecinal", 7, "Realizar reuniones descentralizadas con dirigentes y vecinos"),
    ]),
    ("Óscar Enrique Aliaga Abanto", "Partido País para Todos", "partido-pais-para-todos", [
        P("social", "Brigadas de salud en zonas periféricas como Villas de Ancón y telemedicina en comedores populares", 14, "brigadas de salud semanales", "Brigadas semanales"),
        P("social", "Padrón nominal de niños con anemia y canastas con alimentos ricos en hierro para familias focalizadas", 14, "Entregar canastas con alimentos ricos en hierro"),
        P("agua_riesgos", "Pastillas potabilizadoras y tanques de almacenamiento en sectores sin red pública de agua", 14, "Distribuir pastillas potabilizadoras"),
        P("urbano", "Titulación de asentamientos humanos con los procedimientos simplificados de COFOPRI y actualización del catastro", 16, "Utilizar los procedimientos simplificados de COFOPRI"),
        P("seguridad", "Ampliar la red de cámaras con reconocimiento facial e IA y botones de pánico conectados a la central", 18, "ampliar la red de cámaras con reconocimiento facial"),
        P("seguridad", "GPS en unidades de serenazgo y patrulleros, y puntos de control fijos en los ingresos del distrito", 19, "Instalar sistemas GPS en las unidades de Serenazgo"),
        P("economia", "Ventanilla única para formalizar negocios y bolsa de trabajo digital con ofertas para residentes", 21, "Bolsa de trabajo municipal: Crear una plataforma digital"),
        P("ambiente", "Rutas de recojo optimizadas con mapas digitales, horarios fijos y bolsas de colores para separar residuos", 27, "Usar programas de mapas (sistemas SIG)"),
        P("ambiente", "Riego tecnificado, plantas nativas de poco consumo de agua y compost para los parques", 28, "Plantar especies nativas"),
        P("transporte", "Buses alimentadores desde Villas de Ancón y las partes altas, y gestionar una ruta troncal permanente del Metropolitano", 30, "Plan de Rutas Vecinales"),
        P("gestion", "Portal de transparencia actualizado a diario en lenguaje claro y solicitudes de información por internet", 33, "Publicar presupuestos, gastos, obras y sueldos todos los días", "Actualización diaria"),
    ]),
    ("Felipe Arakaki Shapiama", "Podemos Perú", "podemos-peru", [
        P("seguridad", "Central de Monitoreo Inteligente con IA para lectura de placas, reconocimiento facial y mapas del delito", 5, "Central de Monitoreo Inteligente"),
        P("seguridad", "Cámaras con analítica de video conectadas por fibra óptica en puntos críticos", 5, "interconectadas por fibra óptica en los puntos críticos"),
        P("urbano", "Convenios con COFOPRI y la Municipalidad de Lima para titular predios en asentamientos humanos", 6, "convenios interinstitucionales y asistencia técnica especializada con COFOPRI"),
        P("agua_riesgos", "Coejecutar con SEDAPAL y el Ministerio de Vivienda la ampliación de redes de agua y desagüe en sectores sin servicio", 6, "ampliación de redes matrices de agua y desagüe"),
        P("urbano", "«Plan Distrital de Pavimentación 100 %» de pistas y veredas con convenios del Ministerio de Vivienda", 7, "cobertura total de transitabilidad", "Cobertura total de transitabilidad en las zonas con déficit"),
        P("social", "Centros de refuerzo escolar y alfabetización digital en sectores vulnerables, y academia preuniversitaria municipal", 9, "nodos de refuerzo escolar"),
        P("social", "Monitoreo de niños menores de 5 años y gestantes con suplementación oportuna contra la anemia", 9, "Entrega de suplementación oportuna"),
        P("economia", "Programa de capacitación y formalización de MYPE en alianza con PRODUCE", 10, "programa de capacitación y formalización empresarial"),
        P("ambiente", "Programa «Ancón Recicla» y protección de las Lomas de Ancón y del ecosistema marino", 14, "Protección activa de la Zona de Reserva de las Lomas de Ancón"),
        P("transporte", "Ciclovías seguras y estaciones de micromovilidad que conecten zonas residenciales con servicios", 15, "estaciones de micromovilidad"),
        P("gestion", "Ventanilla única virtual con todos los trámites del TUPA, firma digital y aplicativo ciudadano", 16, "Digitalización del 100% de los procedimientos", "100 % de los trámites del TUPA digitalizados"),
    ]),
    ("Víctor Hernán Medina Zúñiga", "Progresemos", "progresemos", [
        P("social", "Campañas de descarte de anemia, diabetes, hipertensión y salud visual en zonas alejadas", 10, "campañas de descarte de anemia"),
        P("social", "Vehículo acondicionado para trasladar a adultos mayores y personas con discapacidad a los centros de salud", 10, "adquisición de un vehículo acondicionado"),
        P("social", "Biblioteca municipal con computadoras e internet y espacios de reforzamiento escolar", 11, "Modernizar la biblioteca municipal"),
        P("seguridad", "Más serenos y unidades de patrullaje integrado con la Policía Nacional", 12, "incrementando el número de serenos"),
        P("seguridad", "Más cámaras en zonas de mayor incidencia y centro de monitoreo permanente con reconocimiento facial", 12, "centro de monitoreo moderno"),
        P("urbano", "Orientación técnica y legal para formalizar predios y agilizar la titulación", 13, "Impulsar la formalización de la propiedad"),
        P("agua_riesgos", "Gestionar con las entidades responsables la ampliación de redes de agua y alcantarillado en zonas sin cobertura", 14, "Gestionar la ampliación de redes de agua y alcantarillado"),
        P("economia", "Programa «Emprende Ancón»: asesoría para formalizar negocios, bolsa de trabajo y capacitación laboral", 16, "EMPRENDE ANCÓN"),
        P("transporte", "Renovar la señalización vial, campañas de educación vial y mantenimiento de pistas locales", 18, "instalando y renovando señalización horizontal"),
        P("ambiente", "«Plan Ancón Verde»: mantenimiento de parques, nuevos parques en zonas con déficit y arborización", 20, "PLAN ANCÓN VERDE"),
        P("gestion", "Ventanillas únicas de atención y plataformas virtuales para pagos, consultas y servicios", 22, "implementar ventanillas únicas de atención"),
    ]),
    ("Pablo César Ramos Ocaña", "Renovación Popular", "renovacion-popular-peru", [
        P("seguridad", "Videovigilancia en puntos críticos, más capacidad del serenazgo y patrullaje integrado permanente", 3, "Implementar cámaras en el 100% de puntos críticos", "Cámaras en el 100 % de puntos críticos priorizados y el doble de capacidad operativa del serenazgo"),
        P("social", "Campañas trimestrales de salud, repotenciación de centros de salud y programas contra la anemia", 3, "Reducir progresivamente la anemia infantil", "20 campañas, 70 % de niños tamizados y 10 % menos anemia infantil"),
        P("social", "Gestionar el proyecto del Hospital de Ancón o una sede tipo Hospital de la Solidaridad", 3, "Hospital de la Solidaridad"),
        P("social", "Biblioteca municipal en los sectores alejados y convenios con universidades e institutos técnicos", 3, "Biblioteca Municipal en los sectores alejados"),
        P("social", "Red municipal de soporte social y deporte para adultos mayores, personas con discapacidad y jóvenes", 3, "red municipal de soporte social", "Más de 200 adultos mayores y personas con discapacidad beneficiados"),
        P("economia", "Capacitación y acompañamiento a emprendedores, y ferias productivas y comerciales", 3, "10 ferias comerciales realizadas", "10 ferias comerciales"),
        P("economia", "Plan de repotenciación del Parque Industrial y alianzas con empresas para empleo local", 4, "Parque Industrial como polo de inversión", "Plan de repotenciación del Parque Industrial"),
        P("economia", "Mercados zonales en sectores priorizados y reglas de ordenamiento comercial acordadas con comerciantes", 4, "3 mercados zonales promovidos", "3 mercados zonales y 10 mesas de trabajo con comerciantes"),
        P("ambiente", "Sistema integrado de recojo con horarios, renovación de la flota y contenedores en puntos críticos", 4, "3 camiones recolectores", "3 camiones recolectores y 100 % de cobertura de recojo"),
        P("ambiente", "Segregación en la fuente y recolección selectiva, con formalización de recicladores", 4, "segregación en la fuente y la recolección selectiva", "40 % de viviendas incorporadas al programa"),
        P("gestion", "Reorganizar las gerencias municipales para simplificar procesos y reducir los tiempos de trámite", 5, "Reorganizar las gerencias municipales", "10 procesos simplificados, más del 90 % de servidores capacitados y 60 % de satisfacción ciudadana"),
    ]),
]
