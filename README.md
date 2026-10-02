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

Analítica propia, sin Google Analytics, cookies de rastreo ni scripts de terceros. Si falta configuración, o con
`ANALYTICS_ENABLED=false`, no se registra nada y el sitio funciona igual. El texto para el público está en `/privacidad`.

**Arquitectura**

```
navegador (src/lib/analitica.js)            Netlify Functions                     Postgres
 sessionStorage: id de sesión  ──POST──▶  /api/visita (alias /api/track)  ──▶  visitas_sesion   (1 fila por pestaña)
 inicio · latido 30 s · vista ·          valida (≤1 KB, campos cerrados),      analytics_eventos (vista, cambio_ambito,
 ambito · pregunta · fin (beacon)        Origin, límite por IP y sesión,          pregunta, salida)
                                         UA → dispositivo, context.geo →       ref_ubigeo       (catálogo INEI)
                                         ubigeo, IP → HMAC con sal diaria
 /admin (src/admin) ──cookie──▶  /api/admin/login · /api/admin/visitas  ──▶  (rol solo lectura)
                                 purgar-visitas (diaria)                ──▶  purgar_visitas(dias)
```

- **Sesión**: una por pestaña (`sessionStorage`), sin cookies. Con Do Not Track o GPC no se envía nada.
- **Desconexión**: el beacon de `pagehide`/pestaña oculta marca `fin`. Si no llega, la desconexión es el último latido.
  Una sesión sin latido por más de 2 min se da por cerrada. Volver a la pestaña la reabre.
- **Ubicación**: `context.geo` de Netlify, resuelto a ubigeo con `precision_geo` (país → departamento → provincia →
  distrito). Solo baja de nivel con coincidencias exactas y únicas; nunca inventa un distrito. Es aproximada.
- **Preguntas**: solo se cuentan (`preguntas_count`); el texto no se guarda.
- **IP**: nunca en claro; `ip_hash = HMAC-SHA256(ip, ANALYTICS_SALT + fecha de Lima)`. Sirve para contar únicos por
  día sin poder seguir a nadie entre días.
- **Bots**: se marcan con `es_bot` por user-agent (incluidos los headless) y el panel los excluye por defecto.
  Los que no ejecutan JS nunca llegan.
- **Retención**: `ANALYTICS_RETENCION_DIAS` (180 por defecto). Si lo cambias, actualiza también `/privacidad`.

El panel está en `/admin` (no enlazado, `noindex`, `no-store` y la CSP del sitio: sin scripts externos ni en línea). Pide usuario (si `ADMIN_USER` está
definido), contraseña (scrypt) y un código TOTP, y emite una cookie `__Host-` `HttpOnly; Secure; SameSite=Strict`
firmada con HMAC por 8 h. Cada endpoint de `/api/admin/*` la valida en el servidor; el HTML no trae datos.
Tras 5 fallos bloquea la IP 15 min, y cada intento queda en `admin_login_log`, que se ve en el propio panel.

**Variables de entorno** (Netlify → Site configuration → Environment variables, todas marcadas como secretas)

| Variable | Para qué |
|---|---|
| `DATABASE_URL_ANALYTICS` | Rol `analytics_writer`: `/api/visita`, login y purga |
| `DATABASE_URL_ANALYTICS_READER` | Rol `analytics_reader`: `/api/admin/visitas` |
| `ANALYTICS_SALT` | Sal del HMAC de la IP. Cambiarla solo reinicia el conteo de únicos |
| `ANALYTICS_ENABLED` | `false` apaga el registro (endpoint y, en el build, el cliente) |
| `ANALYTICS_RETENCION_DIAS` | Días de conservación (30–730, por defecto 180) |
| `ADMIN_USER` | Usuario del panel (opcional) |
| `ADMIN_PASSWORD_HASH` | Hash scrypt de la contraseña |
| `ADMIN_TOTP_SECRET` | Secreto TOTP en base32 |
| `ADMIN_SESSION_SECRET` | Firma de la cookie (mín. 32 caracteres). Rotarlo cierra todas las sesiones |

`ANALYTICS_ENABLED` se lee también al compilar: después de cambiarla, vuelve a desplegar.

**Despliegue**

1. Migraciones, con un usuario administrador (ambas idempotentes, en este orden):
   ```bash
   psql "$DATABASE_URL_ADMIN" -f db/analytics.sql
   psql "$DATABASE_URL_ADMIN" -f db/analytics_eventos.sql
   ```
2. Roles con permisos mínimos. Ninguno puede leer ni escribir `candidatos`, `documentos` ni `chunks`, y no se reutiliza
   `DATABASE_URL_READONLY`. Con contraseñas largas y aleatorias:
   ```sql
   create role analytics_writer login password '...';
   create role analytics_reader login password '...';
   revoke all on all tables in schema public from analytics_writer, analytics_reader;
   grant usage on schema public to analytics_writer, analytics_reader;
   ```
   Luego aplica los `GRANT` comentados al final de `db/analytics.sql`. Vuelve a ejecutar `db/analytics_eventos.sql`,
   que concede lo de las tablas nuevas cuando los roles ya existen. En resumen: el writer solo hace INSERT/UPDATE en
   `visitas_sesion`, lee y escribe `admin_intentos` (el bloqueo), hace INSERT en `analytics_eventos` y `admin_login_log`, y SELECT en `ref_ubigeo`;
   el reader solo hace SELECT. Para comprobarlo: `\dp visitas_sesion` y `\dp candidatos`.
3. Catálogo INEI: `node scripts/cargar-ref-ubigeo.mjs --dry-run` lo descarga y valida. Sin `--dry-run` y con
   `DATABASE_URL_ADMIN`, lo carga. La fuente está documentada en la cabecera del script.
4. Secretos del panel: `node scripts/admin-setup.mjs` pide la contraseña sin eco (en PowerShell o Git Bash, no en una
   tubería) e imprime `ADMIN_PASSWORD_HASH`, `ADMIN_TOTP_SECRET`, `ADMIN_SESSION_SECRET`, `ANALYTICS_SALT` y la URI
   `otpauth://` para la app autenticadora. No escribe nada en disco.
5. Define las variables de la tabla en Netlify y vuelve a desplegar.
6. Entra a `/admin`. La función programada `purgar-visitas` borra cada día lo que supere la retención.

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
