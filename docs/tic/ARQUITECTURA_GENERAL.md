# Arquitectura general — TIC KENTH

> Documento vivo para la redacción del documento de tesis (Capítulo IV).
> Diagramas renderizables en `docs/tic/diagramas.md` (§1, §2, §9).
> Fuente autoritativa de diseño: `docs/arquitectura.md`.

## 1. Qué es el sistema

Plataforma de curso virtual (dominio piloto: **mezcla y masterización de audio**,
curso Moodle id=2) con un **tutor de IA pedagógico** que:

- responde **anclado a la evidencia del curso** (RAG sobre ChromaDB) — no es un
  chatbot genérico;
- entiende **dónde está parado el estudiante** (lección, momento del video,
  bloque activo);
- **se adapta al desempeño real** del estudiante en las actividades interactivas
  H5P (learning signals) y le recomienda minuto del video + recurso + micro-práctica;
- es **gobernado por el docente** desde la interfaz (contenido, tono, nivel de
  ayuda, momentos), sin tocar Markdown/YAML/Chroma.

## 2. Estilo arquitectónico

**SOA detrás de un API Gateway.** Tres codebases cooperan solo por contrato REST:

| Servicio | Tecnología | Rol |
|---|---|---|
| `frontend-tesis` | React 19 + Vite + Tailwind | SPA única (estudiante, profesor, admin) |
| `tesis-rag` | FastAPI + LangGraph (Python 3.11) | Servicio de IA: chat, RAG, authoring, learning signals |
| Moodle + `local_tesisai` + `api_persistente` | PHP / Moodle 5 | LMS: cursos, H5P (mod_hvp), auth, roles, pagos; dueño del esquema `mdl_local_tesisai_*` |
| Gateway | nginx | Un solo origen: `/api/ai/*`→FastAPI, `/api/lms/*`→Moodle; rate-limit y timeouts |

Infra de apoyo: **MariaDB** (BD operacional = BD de Moodle; las tablas del
proyecto son `mdl_local_tesisai_*`), **ChromaDB** (vector store, bind-mount
persistente), **Ollama** (LLM local: `llama3.1:8b` chat, `nomic-embed-text`
embeddings, `qwen3:14b` authoring), **Loki/Promtail/Grafana** (observabilidad:
cada request emite un log JSON).

## 3. Decisiones clave (defendibles en la sustentación)

1. **Moodle-first**: no se inventó un LMS; el sistema extiende Moodle
   (plugin `local_tesisai` define el esquema y los Web Services). El tutor lee
   solo `mdl_external_tokens` (auth) y `mdl_local_tesisai_*`; el resto vía WS.
2. **Modelos locales (Ollama)**: privacidad de datos de estudiantes y costo
   cero por token; el trade-off es calidad de modelo (mitigado con verificación
   post-generación y guidance determinística).
3. **Domain Pack**: el dominio (léxico, persona, FAQ, listas) vive en
   `domain_packs/<course_id>.json`, no en el código del agente — el agente es
   "lienzo en blanco" reutilizable para otros cursos.
4. **Inject-vs-index**: el conocimiento se INDEXA (Chroma, con fuentes); el
   comportamiento y el estado del alumno se INYECTAN al prompt. Nunca se indexan
   datos del estudiante.
5. **Identidad de lección anclada al `cmid`** de Moodle (`SEC2-R55` = cmid 55):
   reordenar lecciones no corrompe su metadata.
6. **Dos modos de ejecución, una sola base**: dev nativo (XAMPP/uvicorn/Vite) y
   deploy full-docker (`docker-compose.deploy.yml`); la paridad la garantiza el
   contrato de prefijos `/api/ai` y `/api/lms`.

## 4. Flujo de una pregunta del estudiante (resumen)

SPA → gateway `/api/ai/chat` (rate-limit) → FastAPI: auth por token Moodle →
armado de contexto (Capa 2: lección/bloque activo; Capa 3: señales H5P) →
LangGraph supervisor (routing determinista: rag / web / guardia / saludo /
perdido) → retrieval Chroma **pre-filtrado por curso y scope-aware**
(block > lesson > section > global > course) → Ollama → **verificación
post-generación** (citas inventadas, fugas de internos, atribuciones) →
respuesta + fuentes visibles → trazas a `mdl_local_tesisai_*` → log JSON a Loki.

Ver secuencia completa: `diagramas.md` §3; composición del prompt: §9.

## 5. Seguridad y roles

- **Auth**: `Authorization: Bearer <token Moodle>` validado contra
  `mdl_external_tokens` (obligatorio en producción; el bypass `X-User-Id` solo
  existe en dev aislado con SQLite).
- **Permisos**: fuente de verdad = WS `local_tesisai_get_permissions`
  (capabilities reales de Moodle por curso), con fallback por rol. Guards:
  `require_course_view`, `require_teacher`, `require_course_admin`,
  `require_rag_admin` (ver `diagramas.md` §5).
- El estudiante solo puede leer **sus** señales (`/learning-signals/.../me`
  deriva el usuario del token, nunca del payload).

## 6. Estado del despliegue (jul 2026)

- Producción full-docker en servidor compartido (gateway :8090), Ollama nativo
  con GPU, Moodle del proyecto en :8091.
- `main` = fuente de verdad; el servidor se edita solo en ramas de trabajo que
  terminan mergeadas y desplegadas (nunca queda en rama).
- Health: `GET /api/ai/health` (fastapi/moodle_db/moodle_ws/chroma/ollama).
- Smoke: `scripts/smoke_produccion.sh`.

## 7. Pendientes reales (no ocultar en la redacción)

- Solo la **Sección 0** (7 lecciones) está completamente poblada end-to-end.
- Esquema BD conserva residuales de la migración ejes→secciones (`axis_id`).
- El plugin `local_tesisai` y `api_persistente` viven en el runtime de Moodle
  del servidor (respaldados, pero fuera de este repositorio git).
- Evaluación longitudinal con estudiantes reales: fuera del alcance del piloto.
