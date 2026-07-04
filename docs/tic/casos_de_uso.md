# Casos de uso — TIC KENTH

Cada caso de uso (CU) indica actor, precondición, flujo principal, flujo alterno,
postcondición y endpoints relacionados (prefijo público `/api/ai`). La autorización
se resuelve por capabilities de Moodle (WS `local_tesisai_get_permissions`).

---

## CU-01 — El estudiante ve una lección

- **Actor:** Estudiante (matriculado).
- **Precondición:** Token Moodle válido; curso visible/matriculado.
- **Flujo principal:**
  1. La SPA carga la estructura del curso (secciones/lecciones).
  2. El estudiante abre una lección; se muestra el vídeo H5P, la línea de tiempo de momentos y los recursos visibles.
  3. La app resuelve el bloque activo según el timestamp del vídeo.
- **Flujo alterno:** Sin acceso al curso → 403 “No tienes acceso a este curso”. Sin `X-Course-Id`/`course_id` → 400 con mensaje claro.
- **Postcondición:** El estudiante ve la lección y su contexto de actividad queda disponible para el tutor.
- **Endpoints:** `GET /sections/list`, `GET /sections/lessons/all`, `GET /sections/lessons/{id}`, `GET /sections/lessons/{id}/block`, `GET /lessons/{id}/resources`.

---

## CU-02 — El estudiante pregunta al tutor

- **Actor:** Estudiante.
- **Precondición:** Token válido; lección abierta (contexto de actividad).
- **Flujo principal:**
  1. El estudiante escribe una pregunta (opcionalmente adjunta una imagen).
  2. `POST /chat` con `pregunta`, `course_id`, `lesson_id` y contexto de actividad.
  3. El supervisor enruta la intención; se recupera evidencia y se genera la respuesta en español.
  4. Se devuelve la respuesta con `retrieval_scope`, `fuentes` y `trace_id`.
- **Flujo alterno:** Sin token → 401. Pregunta ambigua → el tutor pide precisión. Rate-limit del gateway superado → 429.
- **Postcondición:** Respuesta mostrada; interacción persistida (`interaction_traces`).
- **Endpoints:** `POST /chat`; historial `GET/POST /chat-sessions`, `GET /chat-sessions/{id}/messages`.

---

## CU-03 — El tutor responde con RAG (grounding)

- **Actor:** Sistema (agente LangGraph), disparado por CU-02.
- **Precondición:** Índice Chroma disponible; Ollama con el modelo de chat.
- **Flujo principal:**
  1. `nodo_supervisor` clasifica la intención (determinista) → `agente_rag`.
  2. Retrieval pre-filtrado por curso, con afinidad de scope (block>lesson>section>global>course).
  3. Generación con Ollama + **verificación post-generación** (elimina citas/lugares inventados, repara “sin evidencia” desde metadata).
  4. Respuesta con nivel de evidencia y fuentes.
- **Flujo alterno:** Sin evidencia suficiente → responde “fuera del contexto de la lección” (no alucina). Usuario fuerza web → `agente_web` (DuckDuckGo).
- **Postcondición:** Respuesta fundamentada y trazada.
- **Endpoints:** interno a `POST /chat` (servicios `agent`, `retrieval`, `verification`).

---

## CU-04 — El tutor bloquea una pregunta fuera de dominio

- **Actor:** Sistema (nodo `guardia`).
- **Precondición:** Pregunta recibida por `POST /chat`.
- **Flujo principal:**
  1. El gate de dominio evalúa la **pregunta** (no el contexto).
  2. Si es ajena al dominio (p. ej. cálculo puro), se enruta a `bloqueo`.
  3. Se devuelve un rechazo cortés sin exponer internos ni alucinar.
- **Flujo alterno:** Saludo → nodo `saludo` (sin LLM). “Estudiante perdido” → nodo `perdido` (orientación).
- **Postcondición:** Interacción trazada con `blocked_by=out_of_domain`.
- **Endpoints:** interno a `POST /chat`.

---

## CU-05 — El profesor prepara el tutor con IA

- **Actor:** Profesor editor (`es_profesor`).
- **Precondición:** Token + capability de profesor en el curso; lección con transcripción.
- **Flujo principal:**
  1. El profesor abre la Vista Profesor (3 pasos: recursos → generar borrador → revisión).
  2. `POST …/ai-prepare` genera un borrador pedagógico (momentos con tiempos/tipo, bienvenida, preguntas sugeridas) aislado en `metadata.ai_prepare`.
  3. El profesor edita la línea de tiempo/tarjetas y `POST …/ai-prepare/accept` promueve el borrador a los campos vivos del tutor.
- **Flujo alterno:** Profesor **sin edición** → 403. `quality=max` (deepseek-r1) tarda varios minutos (timeout gateway 600 s). Falla del modelo → error controlado.
- **Postcondición:** Perfil pedagógico actualizado; **no** se reindexa (`requires_reindex=false`).
- **Endpoints:** `POST /authoring/lessons/{id}/ai-prepare`, `POST /authoring/lessons/{id}/ai-prepare/accept`, `PUT /authoring/lessons/{id}/pedagogy`, `PUT /authoring/lessons/{id}/moments`.

---

## CU-06 — El profesor corrige la transcripción

- **Actor:** Profesor editor.
- **Precondición:** Token + capability de profesor; lección con vídeo H5P.
- **Flujo principal:**
  1. `POST …/transcript/auto` lanza la transcripción (Whisper) del vídeo.
  2. `GET …/transcript/status` consulta el progreso.
  3. El profesor edita los segmentos y `PUT …/transcript` guarda las correcciones.
- **Flujo alterno:** Vídeo no localizable por contenthash → 422. Sin capability → 403.
- **Postcondición:** Segmentos de transcripción actualizados (fuente para el RAG al reindexar).
- **Endpoints:** `POST /authoring/lessons/{id}/transcript/auto`, `GET /authoring/lessons/{id}/transcript`, `PUT /authoring/lessons/{id}/transcript`, `GET /authoring/lessons/{id}/transcript/status`.

---

## CU-07 — El profesor sube un recurso

- **Actor:** Profesor editor.
- **Precondición:** Token + capability de profesor.
- **Flujo principal:**
  1. El profesor sube un recurso (PDF/imagen/audio/plantilla) y define `allowed_for_indexing` y `visible_to_student`.
  2. `POST /authoring/documents` (o por sección/lección) registra el recurso y su metadata.
  3. Opcional: enlaza el recurso a una lección/sección.
- **Flujo alterno:** Recurso indexado-pero-no-visible → el tutor usa el texto pero no muestra el archivo. Sin capability → 403.
- **Postcondición:** Recurso disponible; queda `pending` de indexación hasta un reindex.
- **Endpoints:** `POST /authoring/documents`, `POST /authoring/lessons/{id}/resources`, `POST /authoring/sections/{id}/resources`, `PUT /sections/links/{resource_id}`, `PUT /authoring/resources/{resource_id}`.

---

## CU-08 — El admin edita bloques/timestamps (editor avanzado)

- **Actor:** Administrador del curso / gestor (`puede_administrar_curso`).
- **Precondición:** Token + capability de admin de curso.
- **Flujo principal:**
  1. El admin abre el editor avanzado (pestañas Lección/Bloques/Transcripción/Recursos).
  2. `PUT …/blocks` reemplaza la estructura técnica (tiempos, alta/baja/reorden de bloques).
  3. Opcional: `PUT /authoring/lessons-reorder` reordena lecciones; `POST …/documents/reindex` reindexa por curso.
- **Flujo alterno:** Un **profesor editor** NO pasa este gate (edita momentos por el endpoint pedagógico, no tiempos) → 403.
- **Postcondición:** Estructura técnica actualizada; identidad de bloque preservada.
- **Endpoints:** `PUT /authoring/lessons/{id}/blocks`, `PUT /authoring/lessons-reorder`, `POST /authoring/documents/reindex`.

---

## CU-09 — El técnico valida el RAG

- **Actor:** Técnico IA/RAG (site admin, `es_tecnico_rag`).
- **Precondición:** Token + site admin.
- **Flujo principal:**
  1. El técnico ejecuta validadores del índice (coherencia, sin `axis_id`, cobertura por sección).
  2. Consulta `GET /api/ai/health` para el estado de Chroma/Ollama/modelos.
  3. Si procede (destructivo), `POST /documents/rebuild` reconstruye el índice.
- **Flujo alterno:** Rebuild sin site admin → 401/403. `reindex` por curso lo hace el admin de curso, no el profesor.
- **Postcondición:** Índice validado / reconstruido; disponibilidad confirmada.
- **Endpoints:** `GET /health`, `POST /documents/index`, `POST /documents/rebuild` (`require_rag_admin`); scripts `validate_rag_index.py`, `verify_rag_index_clean.py`.

---

## CU-10 — El sistema guarda trazas

- **Actor:** Sistema (middleware + servicios de persistencia).
- **Precondición:** Cualquier request al backend.
- **Flujo principal:**
  1. El middleware emite un log JSON por request (`request_id`, ruta, estado, latencia, user_id).
  2. En `POST /chat`, se persiste la interacción (`interaction_traces`, `message_traces`).
  3. Promtail recolecta los logs → Loki → Grafana.
- **Flujo alterno:** Fallo de request → log `request_failed` con excepción; la traza de error se conserva.
- **Postcondición:** Interacción auditable (BD + logs centralizados).
- **Endpoints:** transversal (middleware `log_requests`; `save_interaction_trace`, `save_trace`).
