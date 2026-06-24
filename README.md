# TIC KENTH — Tutor IA para un curso virtual de Mezcla y Masterización

Plataforma tipo Udemy integrada con **Moodle**, con interfaz **React** y un **tutor
de IA local (Ollama)** que da retroalimentación **personalizada y anclada al
material del curso** (RAG). Proyecto de titulación (ESPE). Casi todo lo
user-facing está en **español**.

> **Importante (alcance):** el tutor trabaja con **contenido textual** del curso
> (lecciones, actividades, preguntas/respuestas, criterios pedagógicos). **NO
> escucha, NO analiza y NO califica archivos de audio**, y está diseñado para
> nunca afirmar que lo hace. El análisis de señal de audio es **trabajo futuro**.

## Arquitectura (resumen)

SOA detrás de un **API Gateway**. El frontend solo llama dos prefijos, mapeados
igual en dev (proxy de Vite) y en prod (nginx):

- `/api/ai/*` → **FastAPI + LangGraph** (`tesis-rag/`) — el tutor RAG.
- `/api/lms/*` → **Moodle** (Apache/PHP) — LMS + plugin `local_tesisai`.

| Pieza | Carpeta |
|---|---|
| Backend IA (FastAPI + LangGraph + Chroma) | `tesis-rag/` |
| Frontend (React 19 + Vite + Tailwind) | `frontend-tesis/` |
| Plugin Moodle (tablas propias + WS) | `C:\Moodle\server\moodle\local\tesisai` |
| Endpoints PHP (login/onboarding/pagos) | `C:\Moodle\server\moodle\proyecto_curso\api_persistente` |

Detalle arquitectónico: `docs/arquitectura.md`. Guía para Claude Code: `CLAUDE.md`.

## Cómo levantar el sistema

### Opción A — Desarrollo nativo (Windows / XAMPP)
Requisitos: Python 3.11+ (venv en `tesis-rag/.venv`), Node 18+, Ollama, Moodle
(XAMPP) corriendo en `:80`.

```bash
# 1) Ollama (modelos locales)
ollama pull llama3.2:3b
ollama pull qwen3-vl:4b-instruct
ollama pull nomic-embed-text

# 2) Backend IA  ->  http://localhost:8000
cd tesis-rag
.venv/Scripts/python -m pip install -r requirements.txt   # primera vez
.venv/Scripts/python main.py

# 3) Frontend  ->  http://localhost:5173  (proxy /api/ai->8000, /api/lms->80)
cd frontend-tesis
npm install
npm run dev
```

### Opción B — Docker Compose (modo despliegue)
Gateway (nginx) + frontend estático + FastAPI + Ollama + Loki/Grafana. Moodle
queda **externo** (host nativo o servidor).

```bash
cp .env.example .env     # editar secretos (changeme_*)
docker compose up -d     # primer arranque de Ollama descarga modelos (5-15 min)
```

Migración al servidor con GPU: ver `docs/MIGRATION-SERVER.md` y
`docker-compose.server.yml`.

## Cómo correr los tests

La suite del backend corre en **un solo comando** (SQLite temporal aislado por
test; no toca Moodle real):

```bash
cd tesis-rag
.venv/Scripts/python -m pip install -r requirements-dev.txt   # primera vez (pytest)
.venv/Scripts/python -m pytest
```

Estado esperado: **verde** (107 passed, 1 skipped — el skip es un *drift* de
política de ingesta de `course_runtime/` documentado en el propio test).

Contrato de sección Moodle (frontend): `cd frontend-tesis && npm run test:moodle-section`.

## Cómo correr la evaluación del tutor (OE4)

Mide la **precisión** del tutor sobre 36 casos etiquetados (12 categorías). Ver
`tesis-rag/evaluation/README.md`.

```bash
cd tesis-rag
# Mock (determinista, sin Ollama): valida las compuertas responder/rechazar/aclarar.
.venv/Scripts/python evaluation/run_tutor_eval.py

# Real (agente completo, requiere Ollama + índice del corpus): todas las métricas.
.venv/Scripts/python evaluation/run_tutor_eval.py --mode real --course-id 2
```

### Qué se evalúa
- Comportamiento: **responder** (en dominio), **rechazar** (fuera de alcance),
  **pedir más contexto** (ambiguo).
- **No-alucinación** (no inventa plugins/DAWs), **uso de fuentes** del curso,
  **no afirmar análisis de audio**, y **latencia**.

## Qué NO hace el sistema

- **No analiza, no escucha ni califica audio.** El tutor lo aclara explícitamente y
  los prompts/reglas se lo prohíben (`tesis-rag/domain_packs/2.json`,
  `services/agent/verification.py`).
- **No devuelve notas al gradebook de Moodle** (write-back = trabajo futuro).
- El piloto es **mono-curso** (mezcla/masterización, `course_id=2`).

## Cómo se justifica Moodle

- **Web Services** para lo "core" del LMS: identidad de usuario, estructura del
  curso (`core_course_get_contents`) y **lectura** de notas/progreso
  (`gradereport_user_get_grade_items`, `core_completion_get_activities_completion_status`)
  — ver `tesis-rag/services/moodle_ws_client.py`.
- **Plugin `local_tesisai`** como dueño de las **tablas propias del tutor**
  (`mdl_local_tesisai_*`: lecciones, bloques, prompts, sesiones, trazas).
- **Acceso directo a BD acotado**: solo validar tokens (`mdl_external_tokens`) y
  roles de docente, una excepción justificada del contrato SOA.
- **Write-back de notas al gradebook**: declarado como **trabajo futuro**.
