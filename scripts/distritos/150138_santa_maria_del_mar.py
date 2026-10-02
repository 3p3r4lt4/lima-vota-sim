"""Santa María del Mar (150138): propuestas principales de los planes de gobierno inscritos ante el JNE.

Cada propuesta está redactada con palabras propias y lleva:
  - pagina: la página del PDF oficial donde aparece.
  - ancla: un fragmento textual del PDF que DEBE aparecer en esa página. El generador lo verifica y
    falla si no lo encuentra, para que ninguna cita apunte a una página equivocada.
Mismo criterio para todas: entre 8 y 11 propuestas por plan, repartidas en los temas que el plan desarrolla.
"""

UBIGEO = "150138"

def P(tema, texto, pagina, ancla, meta=None):
    return {"tema": tema, "texto": texto, "meta": meta, "pagina": pagina, "ancla": ancla}

# (nombre, organización, archivo PDF, propuestas)
PLANES = [
    ("Marwan Zakharia Kahhat Abedrabbo", "Alianza para el Progreso", "alianza-para-el-progreso", [
        P("social", "Programa municipal de salud con convenios con el MINSA, campañas médicas, telemedicina y un Centro de Atención Médica Municipal", 4, "Programa Integral de Salud Municipal mediante convenios con el MINSA", "12 campañas médicas por año y más de 3,000 atenciones anuales"),
        P("social", "Construir e implementar un Policlínico Municipal que atienda las 24 horas", 8, "Construir e implementar un Policlínico Municipal 24 Horas"),
        P("social", "Centro Comunitario Integral con Wawa Wasi, espacios de integración vecinal y velatorio municipal", 8, "Construcción del Centro Comunitario Integral"),
        P("seguridad", "Base integral de seguridad en la zona de playa, cámaras en puntos estratégicos y nuevo equipamiento y unidades móviles para el serenazgo", 8, "Implementar una Base Integral de Seguridad en la zona de playa"),
        P("agua_riesgos", "Sistema de alerta temprana ante sismos, tsunamis y emergencias, con desfibriladores y botiquines en puntos estratégicos", 8, "Sistema de Alerta Temprana para sismos, tsunamis"),
        P("urbano", "Mejorar pistas, recuperar veredas, construir rampas de accesibilidad y mejorar los accesos a las zonas altas", 9, "Mejoramiento de accesos a zonas altas"),
        P("transporte", "Red de ciclovías del distrito junto con obras de accesibilidad universal", 9, "Red de Ciclovías y Accesibilidad Universal"),
        P("economia", "Construir un mercado municipal y promover la formalización y los emprendimientos locales", 9, "Construcción del Mercado Municipal Moderno"),
        P("economia", "Impulsar el turismo durante todo el año con eventos culturales, deportivos y gastronómicos", 5, "impulso del turismo durante todo el año", "20 eventos por año y 40 % más visitantes en temporada baja"),
        P("ambiente", "Mejorar la recolección de residuos e implementar la segregación en la fuente y el reciclaje", 6, "programas de segregación en la fuente", "40 % de residuos reciclables aprovechados y 70 % de viviendas en programas de segregación"),
        P("gestion", "Digitalizar los trámites municipales y reducir los tiempos de atención al ciudadano", 7, "Digitalizar el 90% de los trámites municipales", "90 % de trámites digitalizados y 50 % menos tiempo de atención"),
    ]),
    ("Yessica Rosselli Amuruz Dulanto", "Avanza País", "avanza-pais-partido-de-integracion-social", [
        P("seguridad", "Ampliar el serenazgo con capacitación y dotarlo de vehículos, drones y videovigilancia interconectada con la PNP", 2, "Incrementar el 40% de efectivos", "40 % más efectivos de serenazgo"),
        P("seguridad", "Registro digital obligatorio de vehículos y visitantes en temporada alta en las dos vías de ingreso, con datos compartidos con la PNP", 2, "registro digital obligatorio para vehículos y visitantes"),
        P("seguridad", "Brigada municipal de salvataje acuático en convenio con la PNP, con torres de vigilancia y personal certificado en rescate", 2, "Brigada municipal de salvataje Acuático"),
        P("economia", "Ventanilla única digital para licencias de funcionamiento y autorizaciones temporales", 3, "Ventanilla única digital para licencias de funcionamiento", "Respuesta en un máximo de 48 horas para mypes"),
        P("urbano", "Plan de recapeo de pistas y veredas priorizado por flujo vehicular, con publicación mensual de avance y gasto", 3, "Plan de recapeo de pistas y veredas", "95 % de pistas principales en estado bueno o regular"),
        P("agua_riesgos", "Mesa técnica permanente con Sedapal y el Ministerio de Vivienda para mejorar las redes y reducir pérdidas de agua", 3, "Mesa técnica permanente con Sedapal y MVCS"),
        P("social", "Convertir la posta médica Villa Mercedes en un centro de salud de categoría I-3", 3, "Convertir la posta médica"),
        P("agua_riesgos", "Gestionar ante el Gobierno central muros de contención y enrocados en las zonas críticas de los acantilados", 4, "muros de contención y enrocados en zonas críticas de acantilados"),
        P("ambiente", "Programa «Mar y Acantilado Limpio» con jornadas semestrales de limpieza submarina y de playas con voluntariado", 4, "Jornadas semestrales de limpieza submarina"),
        P("gestion", "Todo el personal técnico y administrativo ingresará por concurso público, con evaluaciones anuales de desempeño", 4, "ingresa por concurso público"),
        P("social", "Programa preuniversitario municipal gratuito para 4.º y 5.º de secundaria mediante convenios con la PUCP y la Cayetano Heredia", 5, "Programa Preuniversitario municipal"),
    ]),
    ("Jorge Patricio Vásquez Nemi", "PPC", "partido-popular-cristiano-ppc", [
        P("seguridad", "Ampliar la central distrital de monitoreo y videovigilancia", 2, "Ampliación de central distrital de monitoreo y videovigilancia", "Cobertura integral de videovigilancia en accesos y espacios públicos al 2030"),
        P("seguridad", "Incrementar progresivamente el personal de serenazgo durante la temporada alta", 2, "Incremento progresivo del personal de serenazgo"),
        P("seguridad", "Fortalecer el sistema de salvataje y primeros auxilios en las playas", 2, "sistema de salvataje y primeros auxilios en playas", "Cobertura total de salvataje en la playa principal al 2030"),
        P("urbano", "Programa de accesibilidad urbana y recuperación de veredas", 2, "Programa de accesibilidad urbana y recuperación de veredas"),
        P("economia", "Desarrollar un mercado municipal para el abastecimiento y el comercio local", 3, "Desarrollo de un mercado municipal"),
        P("gestion", "Actualizar el catastro urbano, fiscalizar los predios, modernizar la cobranza e incentivar el pronto pago", 3, "Actualización del catastro urbano y fiscalización predial", "100 % del catastro actualizado y 25 % más recaudación al 2030"),
        P("ambiente", "Riego tecnificado en parques y arborización con especies de bajo consumo de agua", 3, "Plan de arborización con especies de bajo consumo hídrico"),
        P("ambiente", "Franja verde paisajística en la avenida principal del distrito", 3, "franja verde paisajística en la avenida principal"),
        P("ambiente", "Controlar la contaminación sonora y los residuos durante la temporada alta", 4, "Control de contaminación sonora"),
        P("social", "Campeonatos y circuitos deportivos interdistritales con Punta Hermosa, Punta Negra y San Bartolo, y deportes de playa", 4, "circuitos deportivos interdistritales"),
        P("gestion", "Cabildos abiertos con rendición trimestral de cuentas, aplicación móvil municipal y presupuesto participativo vecinal", 5, "Cabildos abiertos y rendición trimestral de cuentas"),
    ]),
]
