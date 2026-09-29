# Lima vota informado · comparador de propuestas (ERM 2026)

Web para que cualquier vecino de Lima compare, desde el celular, lo que proponen las candidaturas a la
alcaldía antes de votar el domingo 4 de octubre de 2026.

## Qué datos contiene

| Ámbito | Contenido | Fuente |
|---|---|---|
| Lima Metropolitana | 26 listas y 96 propuestas en 8 temas, cada una enlazada a su fuente | Debate del JNE (21 y 22/09/2026) según RPP, Infobae, El Comercio y Perú Informa |
| 42 distritos | Relación completa de candidaturas (465) | Información del JNE difundida por Infobae (27/09/2026) |

Renovación Popular y Perú Libre participan sin candidato a alcalde; se muestran con su primer regidor y
esa condición indicada. En los distritos no se comparan propuestas: la cobertura de prensa distrital es
parcial y publicarla favorecería a unas candidaturas sobre otras. Se enlaza a Voto Informado del JNE.

Todos los datos están en `scripts/datos_reales.py` y `scripts/candidatos_distritales.txt`. Para corregir
algo, edita esos archivos y ejecuta `npm run datos`.

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

## Desarrollo

```bash
npm install
npm test              # pruebas del buscador
npm run datos         # regenera public/data desde scripts/
npm i -g netlify-cli && netlify dev
```

## Siguiente paso: planes de gobierno completos

`ingest/ingest.py` descarga los PDF oficiales de los planes, los indexa en pgvector y `ingest/precompute.py`
genera la matriz comparativa. Con eso se pueden añadir los distritos cuando se tengan los planes de todas
sus candidaturas.

Proyecto personal, independiente y sin afiliación política.
