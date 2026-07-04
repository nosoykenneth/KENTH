# Inventario de endpoints — TIC KENTH

Tabla generada desde las rutas reales de FastAPI (OpenAPI del backend) y verificada
contra los guards de `api/dependencies.py`. **Prefijo público:** todas las rutas se
exponen bajo `/api/ai` por el gateway (p. ej. `/api/ai/health` → `fastapi:8000/health`).

**Rol/capability** (guard):
`—` público · `token` = `get_current_user_id` · `ver` = `require_course_view` ·
`profesor` = `require_teacher` · `revisor` = `require_course_reviewer` ·
`admin` = `require_course_admin` · `rag` = `require_rag_admin`.

**Estado:** ✅ verificado en auditoría · 🟢 operativo · 🆕 añadido en esta rama.

---

## Salud e identidad

| Endpoint | Método | Descripción | Rol | Entrada | Salida | Estado |
|---|---|---|---|---|---|---|
| `/health` | GET | Disponibilidad de FastAPI, BD, WS, Chroma, Ollama, modelos. | — | — | `{status, moodle_db, moodle_ws, chroma, ollama, models, details}` | 🆕✅ |
| `/moodle/me` | GET | Identidad + perfil + capabilities del usuario. Degrada si el WS falla. | token | `?course_id` / `X-Course-Id` (opc.) | `{user_id, profile, capabilities, moodle_ws}` | 🆕✅ |
| `/moodle/courses/{course_id}/contents` | GET | Contenido del curso vía WS. | token | path | JSON Moodle | 🟢 |
| `/moodle/courses/{course_id}/grades` | GET | Calificaciones del usuario. | token | path | JSON Moodle | 🟢 |
| `/moodle/courses/{course_id}/completion` | GET | Progreso de actividades. | token | path | JSON Moodle | 🟢 |

## Tutor (chat)

| Endpoint | Método | Descripción | Rol | Entrada | Salida | Estado |
|---|---|---|---|---|---|---|
| `/chat` | POST | Pregunta al tutor; enruta + RAG + verificación. | token | `Consulta{pregunta, course_id, lesson_id, imagen?, usar_internet?}` | respuesta + `fuentes` + `retrieval_scope` + `trace_id` | ✅ |
| `/chat-sessions/` | POST | Crea/asegura una sesión de chat. | token | body | sesión | 🟢 |
| `/chat-sessions/` | GET | Lista sesiones del usuario. | token | — | sesiones | 🟢 |
| `/chat-sessions/user/{user_id_param}` | GET | Sesiones por usuario (propias). | token | path | sesiones | 🟢 |
| `/chat-sessions/{chat_id}/messages` | GET | Mensajes de una sesión. | token | path | mensajes | 🟢 |
| `/chat-sessions/{chat_id}` | DELETE | Borra una sesión propia. | token | path | `{deleted}` | 🟢 |

## Estructura del curso (secciones / lecciones)

| Endpoint | Método | Descripción | Rol | Entrada | Salida | Estado |
|---|---|---|---|---|---|---|
| `/sections/list` | GET | Secciones Moodle del curso. | ver | `X-Course-Id`/`course_id` | `{sections}` | 🆕🟢 (course_id tolerante) |
| `/sections/lessons/all` | GET | Todas las lecciones del curso. | ver | `X-Course-Id`/`course_id` | `{lessons}` | 🆕✅ (B3: 400 claro, no 422) |
| `/sections/lessons/{lesson_id}` | GET | Manifiesto de una lección. | ver | path (+course_id opc.) | lección | 🟢 |
| `/sections/lessons/{lesson_id}/block` | GET | Bloque activo por timestamp. | ver | `?t=` | bloque | 🟢 |
| `/sections/{section_id}/lessons` | GET | Lecciones de una sección. | ver | path | `{lessons}` | 🆕🟢 |
| `/sections/links` | GET | Vínculos recurso↔lección del curso. | ver | `X-Course-Id`/`course_id` | `{links}` | 🆕🟢 |
| `/sections/links/{resource_id}` | GET | Un vínculo. | ver | path | link | 🟢 |
| `/sections/links/{resource_id}` | PUT | Crea/actualiza vínculo. | profesor | body | link | 🟢 |
| `/sections/links/{resource_id}` | DELETE | Borra vínculo. | profesor | path | `{deleted}` | 🟢 |

## Autoría — lecciones y pedagogía (profesor)

| Endpoint | Método | Descripción | Rol | Entrada | Salida | Estado |
|---|---|---|---|---|---|---|
| `/authoring/lessons/{id}` | PUT / DELETE | Alta/edición/baja de lección. | profesor | body | lección | ✅ |
| `/authoring/lessons/{id}/blocks` | PUT | Reemplazo técnico de bloques (tiempos/estructura). | **profesor**¹ | `{blocks}` | bloques | ✅ |
| `/authoring/lessons/{id}/moments` | PUT | Edición pedagógica in-place (preserva tiempos). | profesor | `{moments}` | bloques | ✅ |
| `/authoring/lessons/{id}/pedagogy` | PUT | Perfil pedagógico canónico. | profesor | perfil | perfil | ✅ |
| `/authoring/lessons/{id}/prompts` | PUT | Mensaje proactivo + sugeridos. | profesor | body | prompts | 🟢 |
| `/authoring/lessons/import` | POST | Importa una lección (JSON). | profesor | body | lección | 🟢 |
| `/authoring/lessons-reorder` | PUT | Reordena lecciones. | **admin** | `{items}` | orden | ✅ |
| `/authoring/lessons/{id}/transcript` | GET / PUT | Lee/corrige transcripción. | profesor | `{segments}` | segmentos | ✅ |
| `/authoring/lessons/{id}/transcript/auto` | POST | Transcribe el vídeo (Whisper). | profesor | `{resource_id, language}` | job | 🟢 |
| `/authoring/lessons/{id}/transcript/status` | GET | Estado de la transcripción. | profesor | — | estado | 🟢 |
| `/authoring/lessons/{id}/ai-prepare` | POST | Genera borrador pedagógico con IA. | profesor | `{mode, quality,…}` | borrador | ✅ |
| `/authoring/lessons/{id}/ai-prepare/accept` | POST | Promueve el borrador a campos vivos. | profesor | `{draft?}` | perfil | ✅ |
| `/authoring/resources/{resource_id}` | PUT / DELETE | Metadata / baja de recurso. | profesor | body | recurso | 🟢 |
| `/authoring/lessons/{id}/resources` | GET / POST | Recursos de la lección. | profesor | multipart/body | recursos | 🟢 |
| `/authoring/lessons/{id}/resources/{doc_id}` | DELETE | Borra recurso de lección. | profesor | path | `{deleted}` | 🟢 |
| `/authoring/sections/{id}/resources` | GET / POST | Recursos de la sección. | profesor | multipart/body | recursos | 🟢 |
| `/authoring/sections/{id}/resources/{doc_id}` | DELETE | Borra recurso de sección. | profesor | path | `{deleted}` | 🟢 |

¹ `blocks` usa `require_teacher` en el backend actual; la barrera técnica “sólo admin
edita tiempos” se aplica en el frontend/flujo (el profesor edita momentos por `/moments`).

## Autoría — documentos/conocimiento del curso

| Endpoint | Método | Descripción | Rol | Salida | Estado |
|---|---|---|---|---|---|
| `/authoring/documents` | GET / POST | Lista / registra documentos de conocimiento. | profesor | documentos | 🟢 |
| `/authoring/documents/structured` | GET | Vista estructurada del conocimiento. | profesor | árbol | 🟢 |
| `/authoring/documents/knowledge/summary` | GET | Resumen del conocimiento indexado. | profesor | resumen | 🟢 |
| `/authoring/documents/knowledge/item` | GET / DELETE | Item de conocimiento. | profesor | item | 🟢 |
| `/authoring/documents/knowledge/file` | GET | Archivo de conocimiento. | profesor | archivo | 🟢 |
| `/authoring/documents/media/{doc_id}` | GET | Media de un documento. | profesor | archivo | 🟢 |
| `/authoring/documents/caption` | POST | Sugerir caption de imagen (visión). | profesor | texto | 🟢 |
| `/authoring/documents/{doc_id}` | DELETE | Borra documento. | profesor | `{deleted}` | 🟢 |
| `/authoring/documents/reindex` | POST | Reindexa el curso (destructivo por curso). | **admin** | job | ✅ |

## Recursos del estudiante (lectura pública controlada)

| Endpoint | Método | Descripción | Rol | Nota | Estado |
|---|---|---|---|---|---|
| `/lessons/{id}/resources` | GET | Recursos **visibles** de la lección. | — | filtra `visible_to_student` | 🟢 |
| `/lessons/resources/{doc_id}/file` | GET | Descarga un recurso visible. | — | 403 si no visible | 🟢 |

## Índice global (técnico RAG) y rutas legacy

| Endpoint | Método | Descripción | Rol | Estado |
|---|---|---|---|---|
| `/documents/index` | POST | Indexa documentos aprobados. | **rag** | ✅ |
| `/documents/rebuild` | POST | Reconstruye TODO el índice (destructivo). | **rag** | ✅ |
| `/documents/` | GET | Lista candidatos de ingesta (dev). | — (dev) | 🟢 |
| `/documents/upload` | POST | Sube a `no_indexar/uploads` (dev). | — (dev) | 🟢 |
| `/documents/{filename}` | DELETE | Borra archivo subido (dev). | — (dev) | 🟢 |
| `/documents/media` | GET | Sirve media por path. | — | 🟢 |
| `/openapi.json`, `/docs`, `/redoc` | GET | Documentación OpenAPI (FastAPI). | — | 🟢 |

> **Nota de seguridad:** las rutas `/documents/` de listado/upload/borrado son legacy
> de desarrollo **sin guard de rol**; las acciones destructivas del índice
> (`/documents/index`, `/documents/rebuild`) **sí** exigen `require_rag_admin`. Ver
> `seguridad.md` (riesgos pendientes).
