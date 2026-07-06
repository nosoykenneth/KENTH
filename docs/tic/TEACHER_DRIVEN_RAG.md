# Teacher-driven RAG — el docente alimenta el conocimiento del tutor

> Documento vivo para la redacción (Capítulos IV–V). Diagrama: `diagramas.md` §7.
> Justificación académica: `BUENAS_PRACTICAS_RAG_EDUCATIVO.md`.

## 1. Tesis del módulo

El tutor solo debe "saber" lo que el **docente aprueba desde la interfaz**.
No hay corpus oculto: la Sección 0 pasó de 208 chunks de Markdown canónico
(semilla técnica) a **0 chunks canónicos activos** (superseded), reemplazados
por material cargado por el flujo docente real.

## 2. Tipos de conocimiento indexado (source_type)

| source_type | Origen en la UI | Qué contiene |
|---|---|---|
| `transcript` (aprobada) | Aprobar transcripción Whisper | texto del video, revisado por el docente |
| `teacher_approved_context` | "Preparar tutor con IA" → aceptar → Publicar | perfil de contexto curado por lección |
| `resource_text` | Subir recurso PDF/TXT | texto extraído del recurso descargable |
| `resource_description` | Subir imagen/plantilla/audio + describir | descripción pedagógica del binario (el binario NUNCA se indexa) |

Flags por recurso (independientes): `allowed_for_indexing` (es evidencia RAG) y
`visible_to_student` (se puede mostrar/descargar). Un recurso puede ser
indexado-pero-no-visible (el tutor usa el texto, no expone el archivo).

## 3. Flujo del docente (sin Markdown, sin YAML, sin Chroma)

1. Sube el video → Whisper genera transcripción (`generated_pending_review`,
   **no indexa** — flag `INDEX_TRANSCRIPT_ONLY_AFTER_APPROVAL`).
2. Revisa/edita y **aprueba** la transcripción → se indexa.
3. **Preparar tutor con IA** (`/ai-prepare`): borrador de perfil pedagógico +
   momentos con tiempos; el docente edita y **acepta** (borrador aislado en
   `metadata.ai_prepare`; al aceptar se promueve; `requires_reindex=false`
   porque el perfil se inyecta, no se indexa).
4. Sube **recursos reales** (35 en Sección 0: bitácoras, plantillas FLP,
   capturas, audios de referencia) → `resource_text` / `resource_description`.
5. **Publicar cambios del tutor** (`/publish`): indexación incremental
   *delete-then-add* con id estable `teacher_context:<lesson_id>` — nunca un
   reindex global.

## 4. Supersesión del corpus canónico (Sección 0)

Driver versionado: `tesis-rag/scripts/` (supersede canonical_md por lección,
controlado por el flag `RAG_SECTION0_SOURCE_MODE`). La semilla `.md` queda en
disco como respaldo histórico pero fuera del índice. Resultado auditado:
canonical_md **208 → 0**, con 123 chunks `resource_text` + 21
`resource_description` + transcripciones + `teacher_approved_context`.

## 5. Estado del índice (producción, pre-cierre jul 2026)

- Chroma total: **241 chunks** (colección `langchain`, bind-mount persistente).
- Curso 2 por lección: SEC2-R55=30, R56=34, R57=38, R58=32, R59=36, R60=32,
  R61=33 (+ L1=6 de laboratorio de tests).
- Validación: batería de retrieval **21/21** + 6/6 de validación de recursos
  (reports `section0_teacher_driven_resources_*`); 0 fugas de material interno.

## 6. Reglas duras (guardas de regresión)

- **Nunca reindex global** en operación normal (es destructivo; existe backup).
- Ingesta solo desde rutas aprobadas (`es_documento_aprobado_para_indexar`,
  tests `test_ingest_public_policy.py` / `test_source_policy.py`).
- Material interno (`visible_to_student=false`) jamás se lista como fuente al
  alumno (filtro en `/chat` + contrato frontend `test:chat-sources`).
- Las señales de aprendizaje del alumno **no entran** a Chroma (ver
  `H5P_LEARNING_SIGNALS.md`).

## 7. Pendientes

- Secciones 1..N del curso aún usan el corpus semilla / están por poblar con el
  mismo flujo (el mecanismo ya está probado end-to-end en Sección 0).
- Subidas de recursos: respetar el rate-limit del gateway (20 req/min) en cargas
  masivas (usar `--sleep` en los drivers).
