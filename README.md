# Lima vota informado · comparador de propuestas (ERM 2026)

Web para que cualquier vecino de Lima compare, desde el celular, lo que proponen las candidaturas a la
alcaldía antes de votar el domingo 4 de octubre de 2026.

## Qué datos contiene

| Ámbito | Contenido | Fuente |
|---|---|---|
| Lima Metropolitana | 26 listas y 96 propuestas en 8 temas, cada una enlazada a su fuente | Debate del JNE (21 y 22/09/2026) según RPP, Infobae, El Comercio y Perú Informa |
| 42 distritos | Entre 8 y 11 propuestas principales por plan de gobierno, cada una con la página exacta del PDF | Planes inscritos ante el JNE (Voto Informado) |

En total, 518 candidaturas. La cobertura exacta de cada ámbito está en `public/data/ambitos.json`
(`con_propuestas`).

**Verificación de citas.** Cada propuesta distrital lleva un fragmento textual del PDF («ancla»).
`npm run datos` falla si ese fragmento no aparece en la página citada, así que ninguna cita puede apuntar
a una página equivocada. En los distritos, las preguntas libres buscan en el texto completo de todos sus planes.

## Cómo agregar otro distrito

1. `python scripts/descargar_planes.py <ubigeo>` descarga de Voto Informado los planes de **todas** las
   candidaturas a `scripts/.cache/planes/<ubigeo>/` (no se versionan; el sitio enlaza a la URL oficial del JNE)
   y escribe `scripts/planes/<ubigeo>/manifiesto.json` con candidato, organización, URL y SHA-256 de cada plan.
2. `python scripts/extraer_planes.py scripts/.cache/planes/<ubigeo>` (requiere Poppler; los PDF escaneados
   pasan por OCR con Tesseract).
3. Copia un módulo de `scripts/distritos/` como `scripts/distritos/<ubigeo>_<distrito>.py`, cambia `UBIGEO` y
   escribe las propuestas con su página y su ancla.
4. `python scripts/verificar_distrito.py scripts/distritos/<ubigeo>_<distrito>.py --muestra 3` comprueba anclas,
   temas, extensión y que nombres y organizaciones coincidan con el manifiesto.
5. Agrégalo a `MODULOS_DISTRITOS` en `scripts/datos_reales.py` y ejecuta `npm run datos`.
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

1. Base de datos: un Postgres propio de la analítica (p. ej. un proyecto gratuito de Neon en AWS US East 2, cerca
   de las funciones). Pega la cadena del dueño, **pooled** y con SSL, en `DATABASE_URL_ADMIN` del `.env` local.
2. `node scripts/analytics-db-setup.mjs` (con `netlify login` y `netlify link` hechos) hace todo sin imprimir secretos:
   aplica `db/analytics.sql` y `db/analytics_eventos.sql` (idempotentes), crea o rota `analytics_writer` y
   `analytics_reader` con contraseñas aleatorias, revoca a PUBLIC el esquema `public`, carga el catálogo INEI en
   `ref_ubigeo`, escribe `DATABASE_URL_ANALYTICS` y `DATABASE_URL_ANALYTICS_READER` (mismo host pooled,
   `sslmode=verify-full`) en el `.env` y en Netlify, y comprueba los permisos de cada rol. `--sin-netlify` no toca
   Netlify; `--verificar` solo repite las comprobaciones. Volver a ejecutarlo rota las contraseñas de los roles.
   Permisos resultantes: el writer solo hace INSERT/UPDATE en `visitas_sesion`, lee y escribe `admin_intentos`
   (el bloqueo), hace INSERT en `analytics_eventos` y `admin_login_log`, y SELECT en `ref_ubigeo`; el reader solo
   hace SELECT. Ninguno toca `candidatos`, `documentos` ni `chunks`, y no se reutiliza `DATABASE_URL_READONLY`.
   La purga borra mediante `purgar_visitas()` (SECURITY DEFINER), sin dar DELETE al writer.
3. El catálogo también se puede cargar aparte: `node scripts/cargar-ref-ubigeo.mjs --dry-run` lo descarga y valida.
4. Secretos del panel (también para rotarlos): con `netlify login` y `netlify link` hechos en esta carpeta,
   `node scripts/admin-setup.mjs` pide usuario y contraseña (sin eco), genera `ADMIN_PASSWORD_HASH`,
   `ADMIN_TOTP_SECRET`, `ADMIN_SESSION_SECRET` y `ANALYTICS_SALT` nuevos y los carga **sin imprimirlos** en Netlify
   (contexto production, como secretos, vía la API: en el plan Free no se pueden elegir scopes y `netlify env:set`
   puede fallar en silencio) y en el `.env` local. En la terminal solo muestra el QR
   para la app autenticadora. `--sin-netlify` solo toca el `.env`; `--sin-env`, solo Netlify.
5. Define en Netlify el resto de variables de la tabla y vuelve a desplegar: las variables no aplican sin redeploy.
6. Entra a `/admin`. La función programada `purgar-visitas` borra cada día lo que supere la retención.

Para cerrar todas las sesiones del panel, rota `ADMIN_SESSION_SECRET`. Para cambiar la contraseña o el TOTP,
vuelve a correr el script.

**Si el login falla**, la respuesta al navegador es siempre la misma, pero el motivo queda en
Netlify → Logs → Functions → `admin-login` como `admin-login: rechazo motivo=…`, sin valores:

| Motivo | Qué revisar |
|---|---|
| `missing_env:<VAR>` | La variable no existe en el contexto production o falta redeploy |
| `bad_config:<VAR>_quoted` | Se guardó entre comillas (en Netlify van sin comillas; las comillas son solo del `.env` local) |
| `bad_config:<VAR>_includes_name` | Se pegó la línea entera `NOMBRE=valor` como valor |
| `bad_config:ADMIN_PASSWORD_HASH_format` | Hash truncado, típico de un shell que expandió los `$`; usa el script |
| `bad_config:ADMIN_TOTP_SECRET_format` / `ADMIN_SESSION_SECRET_short` | Secreto mal copiado o corto |
| `bad_user` / `bad_password` | Usuario (`ADMIN_USER`, sin distinguir mayúsculas) o contraseña distintos |
| `bad_totp` / `bad_totp:clock_skew` / `bad_totp:reused` | Código de otra cuenta de la app, reloj del teléfono desfasado o código ya usado |
| `rate_limited` | 5 fallos en 15 min desde esa conexión: espera 15 min o borra su fila en `admin_intentos` |
| `bad_origin` / `bad_body` / `exception:<tipo>` | Petición que no viene del propio panel, cuerpo inválido o error interno |

## Desarrollo

```bash
npm install
npm test              # pruebas del buscador, analítica y panel admin
npm run datos         # regenera public/data desde scripts/
npm i -g netlify-cli && netlify dev
```

## Búsqueda semántica (opcional)

`ingest/ingest.py` indexa los planes en pgvector e `ingest/precompute.py` genera la matriz comparativa. Sin esa
base, las preguntas libres usan BM25 sobre `/data/planes`.

Proyecto personal, independiente y sin afiliación política.
