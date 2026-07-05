# Flujo docente RAG — cómo el profesor alimenta al tutor sin Markdown

> TIC KENTH · curso 2 (Mezcla y Masterización) · Sección 0 — El sistema de decisión.
> Este documento describe el flujo **teacher-driven** que reemplaza la ingesta
> manual de Markdown como vía principal para alimentar el RAG del tutor.

## 1. Antes vs ahora

**Antes (corpus técnico manual).** El conocimiento del tutor entraba desde
`tesis-rag/documentos/**` (archivos Markdown + YAML con `source_type`, `lesson_id`,
flags de indexación). Eso sirve como **corpus canónico técnico** y sigue siendo
válido, pero **no es defendible como flujo para un profesor real**: un docente de
mezcla no debería escribir Markdown, YAML ni tocar Chroma.

**Ahora (flujo docente).** El profesor trabaja **solo desde la interfaz**:

```
Profesor crea/abre la lección
  → video/H5P
  → transcripción (Whisper) → el profesor la revisa/aprueba
  → "Preparar tutor con IA"  → genera un borrador pedagógico
  → el profesor revisa/edita/acepta
  → el sistema materializa una FUENTE TEXTUAL INDEXABLE (teacher_approved_context)
  → el sistema actualiza el índice RAG de forma INCREMENTAL (esa lección)
  → el tutor responde con ese contenido.
```

El profesor nunca ve Chroma, embeddings, chunks ni `source_type`. Ve estados
humanos: *transcripción pendiente / aprobada*, *tutor actualizado / cambios
pendientes de publicar*, y un botón **"Publicar cambios del tutor"**.

## 2. Qué se INDEXA vs qué se INYECTA (la distinción que gobierna todo)

El perfil pedagógico canónico de la lección tiene **dos naturalezas** y el sistema
las trata distinto (arquitectura *inject-vs-index* del proyecto):

| Campo | Naturaleza | Destino |
|---|---|---|
| `learning_goal`, `lesson_summary` | conocimiento | **INDEXA** (evidencia) |
| `key_concepts`, `common_mistakes`, `probable_questions` | conocimiento | **INDEXA** |
| `moments.title / summary / pedagogical_intent` | conocimiento | **INDEXA** |
| transcripción **aprobada** | conocimiento | **INDEXA** (su propia fuente) |
| descripción de recursos **aprobados** | conocimiento | **INDEXA** |
| `tutor_tone`, `help_level` | comportamiento | **INYECTA** (prompt) |
| `lesson_rules` (directriz interna) | comportamiento | **INYECTA** |
| `tutor_must_not_do` / `attribution_constraints` | política privada | **INYECTA** (verificación) |
| `proactive_message`, `suggested_prompts` | mensajes al alumno | **INYECTA** |

**Regla:** el comportamiento NUNCA se materializa como evidencia RAG. Si el tutor
recuperara su propio tono/reglas como "conocimiento", contaminaría las respuestas y
podría filtrar directrices internas. Esto está fijado por pruebas
(`tests/test_teacher_flow.py::test_build_excluye_comportamiento`).

## 3. La transcripción: de cruda a aprobada (Fase 3)

Auditoría previa: la salida cruda de Whisper se indexaba **demasiado pronto**.

- Cuando Whisper transcribe automáticamente, la transcripción queda en estado
  **`generated_pending_review`** y, con el flag de producción activo, **NO se indexa**.
- Cuando el profesor **aprueba/edita** la transcripción (o se importa una
  transcripción verdadera), pasa a **`approved`/`edited`** y **sí se indexa** de
  forma incremental.

Feature flag: **`INDEX_TRANSCRIPT_ONLY_AFTER_APPROVAL`** (`config.py`).
- Producción / default: **`true`** (seguro: nada crudo entra al tutor).
- Test/dev: configurable a `false` (compatibilidad histórica: indexa de inmediato).

Los timestamps de la transcripción se **preservan** (segmentación operativa: el
tutor puede situar el minuto y la IA puede distribuir los momentos por la línea de
tiempo). No son contenido visible que el tutor recite por defecto.

## 4. `teacher_approved_context` (Fases 5 y 6)

`services/teacher_context.py::build_teacher_approved_context_document(lesson_id)`
genera un documento estructurado desde el perfil **aceptado** por el profesor:

```
# Contexto aprobado de la lección
Lección: <título humano>
## Objetivo de aprendizaje
## Resumen de la clase
## Conceptos clave
## Errores comunes
## Preguntas probables
## Momentos de la clase
## Recursos aprobados relacionados
```

`publish_lesson_teacher_context(lesson_id)` lo **indexa de forma incremental**
(patrón *delete-then-add* por lección; **sin rebuild global**) y devuelve el estado
que muestra el frontend.

Metadata de cada chunk en Chroma (contrato del flujo docente):

| clave | valor |
|---|---|
| `course_id` | `2` |
| `moodle_section_id` / `section_number` / `section_title` | `2` / `1` / `SECCIÓN 0: …` |
| `lesson_id` / `lesson_title` | `SEC2-R55` / *título humano* (nunca el id) |
| `source` | `authoring_profile` |
| `source_type` | `teacher_approved_context` |
| `visible_to_student` | `true` |
| `allowed_for_indexing` | `true` |
| `internal_context` | `false` |
| `generated_from` | `ai_prepare_acceptance` |
| `status` | `teacher_approved` |
| `scope` | `lesson` |
| `corpus_version` | `teacher_flow_v1` |
| `updated_at`, `source_hash` | (frescos por publicación) |

## 5. Cómo se actualiza el tutor (Fase 6/12)

Al **aceptar** el borrador de "Preparar tutor con IA" (o al pulsar **"Publicar
cambios del tutor"**), el backend:

1. Guarda el perfil pedagógico canónico (lo lee `context_service` para inyectar).
2. Genera/actualiza `teacher_approved_context`.
3. Borra los chunks previos de **esa** lección (`source_path=teacher_context:<lid>`).
4. Indexa **solo** esa fuente nueva (incremental).
5. Devuelve estado: `tutor_updated`, `transcript_status`, `index_status`,
   `indexed_at`, `requires_reindex`.

Nunca hace rebuild global. Si el índice falla, `requires_reindex=true` y el profesor
puede reintentar con el botón.

Endpoints (`api/routes/authoring.py`, todos `require_teacher`):
- `POST /authoring/lessons/{id}/ai-prepare/accept` — acepta borrador + publica.
- `POST /authoring/lessons/{id}/publish` — "Publicar cambios del tutor".

## 6. Qué NO se indexa (nunca)

Prompts internos del sistema, `tutor_must_not_do` como política privada, tono/nivel
de ayuda, QA, sets de evaluación, manifests, reportes, IDs técnicos visibles
(`block_id`), y recursos externos **no aprobados**. La política de ingesta de
archivos (`ingest.es_documento_aprobado_para_indexar`) sigue vigente para el corpus
técnico; el flujo docente añade fuentes **DB-driven** con su propio contrato.

## 7. Cómo se defiende en la tesis

- **Precisión medible + grounding verificable (OE4):** el tutor responde desde la
  transcripción aprobada y el contexto aprobado por el profesor, con `scope=lesson`
  y sin heredar material de otra lección. Cada respuesta es trazable a la lección.
- **Autoría docente real:** el profesor alimenta el RAG desde la interfaz; no hay
  paso manual de Markdown/YAML/Chroma. Esto convierte al sistema en un producto
  usable por un profesor de dominio, no por un ingeniero.
- **Separación de responsabilidades:** conocimiento (evidencia) vs comportamiento
  (política inyectada) están separados por contrato y por pruebas; el tutor no puede
  presentar sus reglas internas como evidencia.
- **Seguridad del alumno:** las fuentes internas (`visible_to_student=false`) se
  filtran de las fuentes mostradas; el `teacher_approved_context` es visible por
  diseño (es material pedagógico que el profesor aprobó).
- **Reversibilidad operativa:** todo es *delete-then-add* por lección con backup de
  Chroma; no hay rebuild global destructivo.

## 8. Corpus Markdown: coexistencia

`tesis-rag/documentos/**` sigue siendo el **corpus técnico canónico** y no se borra.
Para la Sección 0, el flujo docente es la **fuente principal** por lección
(transcripción aprobada + `teacher_approved_context`). Si en el futuro se decide que
el Markdown de una lección quedó superseded, se marca `allowed_for_indexing:false` /
`status:superseded_by_teacher_flow` (conservando el archivo en git) o se retiran sus
chunks del índice con `scripts/teacher_flow_section0.py --supersede-canonical`.
Preferencia declarada: **no borrar archivos**; gestionar el índice.
