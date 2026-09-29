# Lima vota informado · comparador de propuestas (ERM 2026)

Aplicación web para que cualquier vecino de Lima compare, desde el celular, las propuestas de las
candidaturas de **su propio distrito** (o de Lima Metropolitana) antes de votar el 4 de octubre de 2026.

> Esta versión usa **datos simulados**: 43 ámbitos (Lima Metropolitana y 42 distritos) con 164
> candidaturas ficticias ("Candidatura Alfa", "Organización simulada Alfa"...). No hay nombres de
> personas ni organizaciones reales. El Cercado de Lima no aparece como distrito porque lo gobierna
> la Municipalidad de Lima Metropolitana.

## Qué puede hacer el usuario

| Función | Detalle |
|---|---|
| Elegir su distrito | Selector en el titular; la URL se puede compartir (`?ambito=150114`). |
| Comparar lado a lado | Tabla tema × candidatura, con metas y página citada. En móvil se reorganiza por tema. |
| Ficha por candidatura | Propuesta principal por tema, cuántas tienen cifra o plazo y qué temas no desarrolla. |
| Preguntar | Pregunta libre (RAG) restringida a las candidaturas marcadas, con citas clicables. |
| Ver el plan | Cada cita abre el plan en la página exacta. |
| Guía de voto | Criterios neutrales: metas verificables, competencias municipales, hoja de vida en el JNE. |

## Buenas prácticas aplicadas

**Neutralidad electoral.** Orden aleatorio de candidaturas en cada visita (también en las respuestas
de la IA), sin puntajes, rankings ni recomendaciones, "no desarrolla este tema" visible con el mismo
peso, recuperación balanceada (máximo de fragmentos por candidatura para no favorecer planes más
largos) y un prompt que rechaza preguntas de "¿por quién voto?".

**Trazabilidad.** Toda afirmación enlaza a su página del plan. En modo real, además, al PDF oficial.

**Resiliencia.** La comparación es JSON estático en CDN: soporta picos de tráfico sin costo. La
función de preguntas degrada con elegancia: pgvector → búsqueda léxica BM25; Claude → respuesta
extractiva con frases textuales. **Sin ninguna variable de entorno el sitio funciona completo.**

**Seguridad.** Usuario de base de datos de solo lectura, límite de 15 preguntas por minuto por IP,
validación de entradas, CSP estricta y cabeceras de seguridad.

**Accesibilidad.** Tabla semántica, `aria-pressed` en la cédula, foco visible, `<dialog>` nativo,
modo oscuro y `prefers-reduced-motion`.

**Calidad.** Pruebas del buscador (`npm test`) y CI que verifica que los datos simulados son
reproducibles, que los JSON son válidos y que el build pasa.

## Arquitectura

```
GitHub (main) ──push──► Netlify build ──► CDN
                                           ├─ React (Vite)
                                           ├─ /data/ambitos.json
                                           ├─ /data/comparaciones/<ubigeo>.json   matriz tema × candidatura
                                           └─ /data/planes/<ubigeo>.json          texto por página (corpus)
Usuario ──► /api/preguntar (Netlify Function, rate limit)
              ├─ recuperación: pgvector híbrido (Neon/Supabase + Voyage)  │ o BM25 sobre /data/planes
              └─ redacción:    Claude Haiku con citas                    │ o extractiva
```

## Despliegue en Netlify (5 minutos)

1. Sube el proyecto a un repositorio de GitHub.
2. En Netlify: **Add new site → Import from Git**, elige el repo. Build `npm run build`, publish `dist`
   (ya vienen en `netlify.toml`).
3. Deploy. Listo: funciona en modo léxico + extractivo.
4. Opcional, en **Site configuration → Environment variables**:
   - `ANTHROPIC_API_KEY` → respuestas redactadas con Claude (pon un tope de gasto en la consola).
   - `DATABASE_URL_READONLY` y `VOYAGE_API_KEY` → búsqueda semántica con pgvector (paso siguiente).

## Activar pgvector con los datos simulados

```bash
psql "$DATABASE_URL_ADMIN" -f db/schema.sql
pip install -r ingest/requirements.txt
python ingest/load_simulado.py          # 164 candidaturas, un embedding por página
# crear el usuario de solo lectura (ver final de db/schema.sql) y usarlo en DATABASE_URL_READONLY
```

## Desarrollo local

```bash
npm install
npm i -g netlify-cli
netlify dev          # web + función en http://localhost:8888
npm test
npm run datos:simular  # regenera los datos (determinista, semilla fija)
```

## Pasar a datos reales

1. Crear `ingest/candidatos.csv` con las URL oficiales de los planes del JNE
   (columnas: `nivel,ubigeo,ambito,cargo,nombre,organizacion,plan_url,hoja_vida_url`).
2. `python ingest/ingest.py ingest/candidatos.csv` (PDF → páginas → embeddings; avisa si requiere OCR).
3. `python ingest/precompute.py` genera `comparaciones/` y `planes/` con `simulado: false`.
4. Revisar las citas en un Pull Request antes de publicar. La franja de "datos simulados" desaparece sola.

Proyecto personal, independiente y sin afiliación política.
