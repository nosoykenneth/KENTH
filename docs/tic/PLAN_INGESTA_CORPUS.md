# Procedimiento general de ingesta de corpus por sección (RAG)

Procedimiento reproducible para incorporar el corpus de una sección al índice RAG del tutor, con gates de seguridad. Primer caso ejecutado: Sección 0 (ver `INGESTA_SECCION_0_REPORTE.md`).

## Principios
- **Acotado por sección/lección.** Nunca `/documents/rebuild` (global/destructivo) para añadir una sección.
- **La política de flags manda.** `allowed_for_indexing:false` ⇒ nunca al índice. Los excluidos **no se colocan** en el árbol de ingesta (defensa en profundidad, porque el gate de markdown no atrapa el string `"false"`).
- **No inventar `lesson_id`.** Solo se indexa a scope lección cuando existe la lección real (match fuerte de título). Sin lección real ⇒ retener (`pending_lesson_mapping`) o, si se autoriza, scope sección sin `lesson_id`.
- **Identidad de sistema, no la humana.** Etiquetar los chunks con `moodle_section_id` / `section_number` reales (Moodle reserva `section_number=0` para el área general; la "Sección 0" pedagógica suele ser `section_number=1`).

## Arquitectura relevante
- Corpus canónico: `tesis-rag/documentos/oficial/curso_<id>/seccion_<NN>_<slug>/...` con frontmatter por archivo. **Horneado** en la imagen fastapi (`COPY . .`); `documentos/` NO está bind-mounteado.
- Ingesta: `ingest.add_single_document()` (incremental, delete-then-add por `source_path`) y `es_documento_aprobado_para_indexar()` (política). Metadata del chunk la arma `_metadata_base()`.
- Índice: ChromaDB en volumen `runtime/chroma` (persiste entre recreaciones del contenedor).

## Frontmatter requerido para indexar (por archivo)
`course_id`, `moodle_section_id`, `section_id`, `section_number`, `section_title`, `section_slug`, `lesson_id` (si aplica), `lesson_title`, `source_type`, `scope` (`section|lesson|block`), `visible_to_student`, `allowed_for_indexing`, `internal_context` (si vis=false & idx=true), `status`, `source_origin: course`. Provenance recomendado: `corpus_version`, `ingestion_batch_id`, `original_relative_path`.

## Flujo con gates
1. **AUDITAR** el corpus: 100% frontmatter válido, UTF-8, sin vacíos, sin placeholders reales, sin secretos, sin enlaces dudosos.
2. **CORREGIR** solo metadata/flags (nunca contenido): QA→`qa_report`, evaluación/QA/operativos→`false/false` + `excluded_*`, recursos externos no aprobados→`allowed_for_indexing:false`, guías del tutor→`internal_context:true`.
3. **GATES** (detener si): falta archivo, YAML irrecuperable, eval/QA/operativos marcados indexables, recursos externos indexables, secretos, no hay mapeo real de lección, no hay método acotado seguro, health no-ok, servidor dirty, backup falla.
4. **MANIFESTAR:** `INGEST_MANIFEST_SECCION_<N>.csv/.json` + `PLAN_INGESTA_SECCION_<N>.md`.
5. **MAPEAR** contra el sistema real: `db_service.list_lessons(course_id)` y la sección Moodle. Alinear la identidad de sección con un chunk existente si lo hay.
6. **RESPALDAR:** `cp -r runtime/chroma` con timestamp + `pre_index_state.json` (total/by_source/by_section/by_lesson/fuentes) en `reports/ingesta_seccion_<N>_<ts>/`.
7. **INGESTAR:** árbol server-ready (frontmatter de sistema) → host-repo → `docker cp` al contenedor → `ingest_seccionN.py` dry-run → `--commit`.
   - **Promoción autoría→canónico (versionada):** `tesis-rag/scripts/promote_seccion_corpus.py --manifest <INGEST_MANIFEST_SECCION_N.json> [--dry-run|--commit]` transforma el árbol de autoría (frontmatter humano) al árbol canónico `documentos/oficial/curso_<id>/seccion_<slug>/` inyectando el frontmatter de sistema y aplicando los flags por `action` del manifest. Es el driver antes no-versionado. Sólo reescribe metadata; el cuerpo del markdown se copia verbatim. La Sección 0 se consolidó con él (2026-07-05).
8. **CONSOLIDAR (durable):** `docker compose build fastapi && up -d fastapi` (Chroma persiste). Verificar health.
9. **VALIDAR:** gates de Chroma (excluidos=0, otras secciones intactas, retenidas=0) + pruebas de chat con token estudiante (grounded/rechazo/ambigua/guía-interna).
10. **REPORTAR:** `reports/INGESTA_SECCION_<N>_REPORTE.md` (+ copia en `docs/tic/`).

## Obtener un token de estudiante para pruebas
`mdl_external_tokens` (lectura permitida por el contrato SOA). Verificar `external_services.enabled=1` y `validuntil` (0 = sin expiración; >0 = epoch límite — **cuidado con tokens expirados**). Usar `MYSQL_PWD` para no exponer la clave en `ps`.

## Deuda técnica detectada (aplicar cuando se pueda)
- ~~`ingest.es_documento_aprobado_para_indexar`: cambiar `allowed_flag is False` por `_as_bool(...) is False`~~ **RESUELTO** (PR #10, `10c8b9f`): el gate ya normaliza el flag con `_as_bool` robusto; validado sobre el árbol consolidado de la Sección 0 (22 indexables, 0 fugas de eval/QA/manifest/HOLD).
- Frontend: filtrar el array `fuentes` de `/chat` por `visible_to_student` para el alumno (las guías internas se usan como conocimiento pero no deben citarse).
