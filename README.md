# Lima vota informado · comparador de propuestas (ERM 2026)

Web para que cualquier vecino de Lima compare, desde el celular, lo que proponen las candidaturas a la
alcaldía antes de votar el domingo 4 de octubre de 2026.

## Qué datos contiene

| Ámbito | Contenido | Fuente |
|---|---|---|
| Lima Metropolitana | 26 listas y 96 propuestas en 8 temas, cada una enlazada a su fuente | Debate del JNE (21 y 22/09/2026) según RPP, Infobae, El Comercio y Perú Informa |
| La Molina | 12 planes de gobierno completos (PDF) y 122 propuestas principales con su página | Planes inscritos ante el JNE (Voto Informado) |
| Otros 41 distritos | Relación de candidaturas, incluidas las listas sin candidato a alcalde | Base electoral difundida por RPP (28/09/2026) |

**Verificación de citas.** Cada propuesta de La Molina lleva un fragmento textual del PDF («ancla»).
`npm run datos` falla si ese fragmento no aparece en la página citada, así que ninguna cita puede apuntar
a una página equivocada. En La Molina, las preguntas libres buscan en el texto completo de los 12 planes.

## Cómo agregar otro distrito

1. Descarga de Voto Informado los planes de **todas** las candidaturas del distrito y guárdalos en
   `public/planes/<ubigeo>/<organizacion>.pdf`.
2. `python scripts/extraer_planes.py public/planes/<ubigeo>` (requiere `pdftotext`).
3. Copia `scripts/la_molina.py` como `scripts/<distrito>.py`, cambia `UBIGEO` y escribe las propuestas con su ancla.
4. Regístralo en `PLANES_DISTRITALES` dentro de `scripts/datos_reales.py` y ejecuta `npm run datos`.
   El script exige un plan por cada candidatura de la lista oficial.

## Funciones

- **Comparar lado a lado**: tabla tema × candidatura, con meta (cifra o plazo) y enlace a la fuente.
- **Ficha por candidatura**: propuesta principal por tema, cuántas tienen cifra o plazo y en qué temas no hubo propuestas.
- **Preguntas libres** (RAG) sobre las candidaturas marcadas, con citas clicables y botón «Pregunta al azar».
  Detecta si preguntas por otro distrito o por quiénes postulan, y responde con la lista oficial.
- **Guía de voto** con criterios neutrales.

## Criterios de neutralidad

Orden aleatorio de candidaturas en cada visita (también en las respuestas), una misma fuente para todas
(el debate del JNE), sin puntajes ni rankings, «No aparece en la cobertura del debate» visible con el mismo
peso que una propuesta, recuperación balanceada por candidatura y un prompt que rechaza preguntas de
«¿por quién voto?». Las propuestas se redactan con palabras propias y enlazan al texto original.

## Arquitectura

```
GitHub (main) ──push──► Netlify build ──► CDN
                                           ├─ React (Vite)
                                           ├─ /data/ambitos.json
                                           ├─ /data/comparaciones/<ubigeo>.json
                                           └─ /data/planes/<ubigeo>.json   (corpus para las preguntas)
Usuario ──► /api/preguntar (Netlify Function, 15 preguntas/min por IP)
              ├─ recuperación: pgvector híbrido (opcional)  │ o BM25 sobre /data/planes
              └─ redacción:    Claude Haiku con citas        │ o extractiva
```

Sin variables de entorno funciona completo. Con `ANTHROPIC_API_KEY` en Netlify las respuestas se redactan
con Claude. Con `DATABASE_URL_READONLY` y `VOYAGE_API_KEY` la búsqueda pasa a ser semántica (ver `db/schema.sql`
e `ingest/`).

## Analítica y panel admin

Analítica propia, sin Google Analytics, cookies de rastreo ni scripts de terceros. Cada pestaña es una sesión
(`sessionStorage`) que envía `inicio`, `latido` cada 30 s con la pestaña visible, `ambito` al cambiar de distrito
y `fin` al salir, a `POST /api/visita`. El servidor deduce el dispositivo del user-agent y la ubicación de
`context.geo` (resuelta a ubigeo INEI con precisión país → departamento → provincia → distrito), y guarda solo
un HMAC diario de la IP. Con Do Not Track o GPC no se envía nada, y si falta configuración el sitio funciona igual.
El texto para el público está en `/privacidad`. La retención es de 90 días.

El panel está en `/admin` (no enlazado, `noindex`). Pide contraseña (scrypt) y un código TOTP. Tras 5 fallos
bloquea la IP 15 min.

**Despliegue**

1. Migración, con un usuario administrador: `psql "$DATABASE_URL_ADMIN" -f db/analytics.sql` (idempotente).
2. Crear los roles `analytics_writer` y `analytics_reader` con los `GRANT` comentados al final de `db/analytics.sql`.
3. `node scripts/admin-setup.mjs`: pide la contraseña sin eco, imprime `ADMIN_PASSWORD_HASH`,
   `ADMIN_TOTP_SECRET`, `ADMIN_SESSION_SECRET` y `ANALYTICS_SALT`, y la URI `otpauth://` para la app autenticadora.
4. En Netlify, definir esas cuatro variables más `DATABASE_URL_ANALYTICS` (rol writer) y
   `DATABASE_URL_ANALYTICS_READER` (rol reader), marcadas como secretas, y volver a desplegar.
5. Entrar a `/admin`. La función programada `purgar-visitas` borra cada día lo que tenga más de 90 días.

Para cerrar todas las sesiones del panel, rota `ADMIN_SESSION_SECRET`. Para cambiar la contraseña o el TOTP,
vuelve a correr el script y reemplaza las variables.

## Desarrollo

```bash
npm install
npm test              # pruebas del buscador, analítica y panel admin
npm run datos         # regenera public/data desde scripts/
npm i -g netlify-cli && netlify dev
```

## Siguiente paso: planes de gobierno completos

`ingest/ingest.py` descarga los PDF oficiales de los planes, los indexa en pgvector y `ingest/precompute.py`
genera la matriz comparativa. Con eso se pueden añadir los distritos cuando se tengan los planes de todas
sus candidaturas.

Proyecto personal, independiente y sin afiliación política.
