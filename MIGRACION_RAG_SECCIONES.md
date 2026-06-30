# Migración RAG: ejes → secciones / lecciones / bloques

Rama: `feat/rag-secciones-bloques` · Servidor: `kenneth@100.97.90.86` (`/srv/kenneth/tic-kenth`)
Fecha: 2026-06-30 · Estado: **implementado, desplegado y validado en el servidor**.

## 1. Objetivo cumplido

El tutor IA ya **no depende de la taxonomía por ejes** como fuente pedagógica. La
unidad del curso es ahora `course_id → moodle_section_id → lesson_id → block_id →
recursos`. ChromaDB es un índice derivado, reconstruible y purgable; la fuente
canónica son los documentos por sección + la estructura Moodle (MariaDB).

**Antes** (problema reportado): todo el corpus se indexaba por `axis_id="Eje N"` con
`moodle_section_id=""`. El retrieval daba `scope_affinity=+0.00 relation=same_course`
a todo → el tutor no localizaba por sección; Eje 6/7 competía con Eje 2 por mera
similitud. **Ahora**: cada chunk se ancla a su sección Moodle y el retrieval prioriza
bloque > lección > sección > global > curso, penaliza cruce de sección y declara
fallback.

## 2. Backups (antes de tocar nada)

`/srv/kenneth/backups/rag-migration-20260630-152111/` (puntero en
`/srv/kenneth/backups/LAST_RAG_BACKUP.txt`):
- `chroma_bd_vectorial.tgz` (índice viejo), `moodle_dump_*.sql.gz` (dump completo),
  `tesisai_tables_*.sql.gz`, `corpus_oficial_*.tgz`, `env.snapshot`, compose, nginx, domain_packs.
- Restore points Git en server: tag `pre-rag-secciones-20260630` + rama
  `backup/pre-rag-secciones-20260630` (HEAD desplegado previo `2ac9c3a`).

## 3. Nueva arquitectura de metadata del chunk

```
course_id, moodle_section_id, section_id, section_number, section_title, section_slug,
lesson_id, lesson_title, block_id, block_title, resource_id,
resource_type, content_type, layer (canonical|transcript|rubric|resource|global),
scope (block|lesson|section|course|global),
source (moodle|canonical_md|resource_file|transcript), source_path, source_hash,
version, index_status, + flags operativos (is_global, visible_to_student, allowed_for_indexing, media_type)
```
Reglas duras (validadas): `axis_id` **prohibido** en el índice; ningún chunk seccional
sin `moodle_section_id`; solo recursos realmente universales con `scope=global`; todo
chunk con `course_id`. `legacy_axis` se conserva SOLO como traza informativa de migración.

## 4. Corpus migrado

`tesis-rag/documentos/oficial/ejes/**` (76 archivos) → **purgado**.
Nuevo: `tesis-rag/documentos/oficial/curso_2/seccion_NN_<slug>/contenido_canonico.md`
con frontmatter (course_id, moodle_section_id, section_*, layer, scope, source). Mapa
(de MariaDB `mdl_course_sections`, log en `curso_2/_seccion_map.json`):

| Eje (viejo) | moodle_section_id | nº | Sección |
|---|---|---|---|
| 0 | 2 | 1 | SECCIÓN 0: El sistema de decisión |
| 1 | 3 | 2 | SECCIÓN 1: Leer la señal |
| 2 | 4 | 3 | SECCIÓN 2: Integridad de la señal |
| 3 | 5 | 4 | SECCIÓN 3: Identidad espectral |
| 4 | 20 | 5 | SECCIÓN 4: Energía y movimiento |
| 5 | 19 | 6 | SECCIÓN 5: Dimensión espacial |
| 6 | 18 | 7 | SECCIÓN 6: Integración global |
| 7 | 17 | 8 | SECCIÓN 7: Traducción y entrega |

Decisión registrada: se eliminó el **doble-indexado** de ejes 3/5/6/7 (existían
`KENTH_EjeN` y `eje_N/01_contenido` con el mismo contenido); se conservó una sola
fuente canónica por sección.

## 5. Cambios de código (resumen)

- `ingest.py`: metadata nueva; `_scope_chunk` sin 'axis'; `_section_meta_for_id` (resuelve
  sección desde Moodle); `source` vs `source_path`; corpus canónico bajo `oficial/curso_*`;
  **fix crítico**: `reindex_course_documents` borraba TODO el curso (aniquilaba el corpus
  canónico tras rebuild) → ahora borra solo lo DB-driven (`transcript`/`resource_file`).
  Eliminados `_section_id_for_axis`, `_metadata_axis`, `_normalizar_eje`, etc.
- `services/db_service.py`: `derive_scope`/`validate_scope`/`DOC_SCOPES` sin 'axis'
  (legacy 'axis' → 'section').
- `services/agent/retrieval.py`: afinidad `same_block +1.00 / same_lesson +0.85 /
  same_section +0.60 / global +0.25 / same_course +0.10 / other_section −0.25`;
  progresión curricular por `section_number`; log `[RETRIEVAL SCOPE]` + `retrieval_scope`/
  `retrieval_fallback` en estado.
- `services/agent/graph.py`, `prompts.py`, `context_service.py`: prompts/trazas hablan de
  sección/lección/bloque; observabilidad de scope propagada a la respuesta y a la traza.
- `models/schemas.py`: `EstadoAgente` −`current_axis_id`; +`moodle_section_id`,
  `current_section_name/order`, `retrieval_scope`, `retrieval_fallback`.
- `api/routes/chat.py`: persiste `retrieval_scope`/`retrieval_fallback` en `trace_data` y respuesta.
- Frontend: labels "eje" → "sección" (KnowledgeHub, LessonResourcesPanel, AssignLessonDialog).
  El payload del chat ya enviaba `moodle_section_id`/`current_lesson_id`/`current_timestamp`
  (el bloque lo resuelve el backend por timestamp).
- Scripts: `reindex_rag_clean.py` reescrito (init_db → purga+rebuild+transcripts+validate);
  `validate_rag_index.py` (nuevo, reporte JSON/MD + chequeos duros); `migrate_corpus_ejes_to_secciones.py`.
- Tests: `test_rag_secciones.py` (nuevo); `test_source_policy`/`test_ingest_public_policy` a secciones;
  contrato `same_section=0.60`; baseline phase0 regenerado (scoring sin boost por eje).

## 6. Evidencia de validación (en el servidor)

- **Índice**: 405 chunks. Por sección: SECCIÓN 0=47, 1=36, 2=50, 3=50, 4=61, 5=52, 6=51,
  7=58; transcripciones (scope lesson) SEC2-R55=8, SEC2-R56=7. Scopes: `section`=390,
  `lesson`=15. **Violaciones = 0** (sin axis_id, sin scope=axis, sin seccional-sin-sección,
  sin no-global-sin-curso). Reporte: `tesis-rag/scripts/_out/rag_index_report.(json|md)`.
- **Afinidad por sección (prueba directa)**: alumno en `moodle_section_id=4` → top
  `same_section aff=+0.60`, `retrieval_scope=section`, `fallback=False`. Mismo query desde
  sección 17 → la evidencia de la 4 cae a `other_section aff=−0.25`, `retrieval_scope=course`,
  `fallback=True` (ampliación declarada).
- **End-to-end** (Ollama GPU): alumno en SECCIÓN 2, pregunta in-domain → ruta `teoria`,
  evidence `alto`, las 3 top evidencias de "SECCIÓN 2", `retrieval_scope='section'`,
  respuesta fundamentada sin alucinaciones.
- **Tests**: `pytest tests/` = **114 passed, 1 skipped**.
- **Build**: imágenes `frontend` y `fastapi` reconstruidas; gateway SPA responde 200.

## 7. Comandos clave

```bash
# (server) reindex limpio + validación
docker exec tic-fastapi python scripts/reindex_rag_clean.py
docker exec tic-fastapi python scripts/validate_rag_index.py
# tests
docker exec tic-fastapi python -m pytest tests/ -q
# rebuild de imágenes tras pull
docker compose -f docker-compose.deploy.yml build frontend fastapi && \
docker compose -f docker-compose.deploy.yml up -d frontend fastapi
```

## 8. Pendientes reales (no bloquean el piloto)

1. **Gate de dominio por vocabulario de ejes** (`routing.py`: `COURSE_AXES`,
   `_eje_fuerte_pregunta`, `_inferir_modulo_categoria`; `domain_packs/2.json` keywords
   `eje0..7`). Es **detección de dominio + categoría de evaluación**, NO taxonomía RAG, y
   tiene baseline de regresión propio. Decisión: se mantiene tal cual; reescribirlo a un
   detector por sección/concepto es un cambio aparte (post-piloto) que debe hacerse con su
   baseline en foco. No afecta el retrieval ni la localización por sección.
2. **Transcripciones**: `SEC2-R55`/`R56` viven en `moodle_section_id=2`; al poblar más
   lecciones/secciones, el reindex las ancla solo (sin tocar código).
3. **Merge a `main`**: la rama está desplegada y validada en el server; el merge/PR a `main`
   queda como decisión de release del dueño.
