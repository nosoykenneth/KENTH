# CHROMA_POST_AUDIT — Sección 0 (curso 2)

Auditoría del índice vectorial **local** tras aplicar el flujo docente
(`scripts/teacher_flow_section0.py --apply`) para las lecciones presentes en la BD
local. Fecha: 2026-07-05. Backend embeddings: `nomic-embed-text` (Ollama local).

> Alcance local: el entorno local sólo tiene 2 de las 7 lecciones de la Sección 0
> (SEC2-R55, SEC2-R56); R57–R61 viven en el servidor. Esta auditoría certifica el
> estado local; la del servidor se genera con el mismo script tras el runbook.

## Estado del índice

| Métrica | Valor |
|---|---|
| Chroma total (curso 2) | 25 chunks |
| Sección 0 (`course_id=2` ∧ `moodle_section_id=2`) | **19 chunks** |
| SEC2-R55 (0.1) | 11 (9 transcripción + 2 teacher_approved_context) |
| SEC2-R56 (0.2) | 8 (8 transcripción + 0 teacher_context) |

### Distribuciones (Sección 0)

- **por `source`**: `transcript`=17, `authoring_profile`=2
- **por `source_type`**: `teacher_approved_context`=2, (transcripción sin source_type)=17
- **por `doc_type`**: `video_transcript`=17, `teacher_approved_context`=2
- **`visible_to_student`**: todos `true` (19/19)
- **`allowed_for_indexing`**: todos `true` (19/19)
- **`scope`**: todos `lesson` (19/19)
- **`section_number`**: todos `1` (19/19) — Sección 0 == section_number 1 (Moodle)

## Verificaciones (Fase 10) — resultado

| Debe cumplirse | Resultado |
|---|---|
| No chunks stale de Sección 0 antigua (path-form `transcription:*` en `source`) | ✅ 0 |
| No `scope=axis` / `axis_id` | ✅ 0 |
| No prompts de evaluación / QA / manifests / reportes | ✅ (fuentes DB-driven acotadas: transcript + authoring_profile) |
| Chunks de transcripción por cada lección presente | ✅ R55, R56 |
| Chunks `teacher_approved_context` por lección con perfil aprobado | ✅ R55 (R56 sin perfil aprobado → 0, correcto) |
| Metadata correcta (course/section/lesson/source/visible/allowed/internal) | ✅ |
| `lesson_title` humano (no ID técnico `SEC2-R…`) | ✅ "1 — Mezclar es decidir…", "Lección 2 — Tu oído miente…" |
| Fuentes no visibles no se exponen | ✅ (todos los chunks de Sec 0 son visibles por diseño; el filtro `visible_to_student=false` sigue activo en `/chat`) |

## Notas

- R56 no tiene `teacher_approved_context` porque aún no se ejecutó "Preparar tutor
  con IA" para esa lección en local (requiere `qwen2.5:14b-instruct`, ausente en
  local). En el servidor, el runbook ejecuta `ai_prepare` por lección y R56 tendrá
  su contexto aprobado. El comportamiento **es correcto**: sin perfil aprobado no se
  inventa evidencia.
- Backup del índice previo: `bd_vectorial_backup_teacherflow_20260705_142050`.
- JSON crudo de la corrida: `teacher_flow_run.json` (este directorio).
