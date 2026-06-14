# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

**TIC KENTH** is an AI tutor for an online course platform (thesis project, ESPE). A student watches lessons and asks a RAG-grounded tutor questions; a teacher authors lesson structure, resources and transcripts that feed the tutor. The pilot course domain is audio **mezcla y masterización** (mixing/mastering), and almost everything user-facing is in **Spanish** — match that language in prompts, domain data, and UI strings.

The system is **SOA behind an API Gateway**. Three+ codebases cooperate by REST contract; they do not import each other. See `docs/arquitectura.md` for the authoritative architecture (it is also thesis Ch. IV source material).

## Repository layout (codebases live in different directories)

This is the most important thing to internalize: the project spans several roots, not all under the primary working dir.

| Path | What |
|---|---|
| `tesis-rag/` | **FastAPI + LangGraph RAG backend** (the AI service). Python 3.11, venv in `tesis-rag/.venv`. |
| `frontend-tesis/` | **React 19 SPA** (Vite, Tailwind v4, react-router 7). The only client. |
| `C:\Moodle\server\moodle\local\tesisai` | **Moodle plugin** `local_tesisai`: owns the operational DB schema (`db/install.xml`) and Web Service definitions (`db/services.php`, `externallib.php`). |
| `C:\Moodle\server\moodle\proyecto_curso\api_persistente` | Native PHP endpoints for auth/login, onboarding, and payments (PayPal/Payphone). |
| `docs/`, `*.md` at root | Design notes (`arquitectura.md`, `funcionIA.md`, `notebooklm.md`, `pasadas.md`, etc.). Many root `.md`/`.txt` files are scratch/thesis notes, not code.

Moodle (Apache + MariaDB) is **external** to the project — in dev it's XAMPP at `C:\Moodle\server`; the backend reads its `config.php` for DB credentials.

## Common commands

### Backend (`tesis-rag/`)
```bash
# run the API (dev, reload) — http://localhost:8000
python main.py                      # or: uvicorn main:app --reload --port 8000

# tests (pytest; tests live in tesis-rag/tests/, plus loose test_*.py at root)
python -m pytest tests/                              # the maintained suite
python -m pytest tests/test_domain_pack_phase0.py    # single file
python -m pytest tests/test_source_policy.py::test_name -q   # single test

# reindex the vector store from the approved corpus (DESTRUCTIVE rebuild — see gotchas)
python scripts/reindex_rag_clean.py

# one-off verification/diagnostic scripts (run from tesis-rag/ root so imports resolve)
python scripts/verify_phase1.py     # scripts/ and scratch/ are full of these
```
There is no `pytest.ini`/`pyproject.toml`; run pytest from the `tesis-rag/` dir. `scratch/` is throwaway experiments — don't treat it as the suite.

### Frontend (`frontend-tesis/`)
```bash
npm run dev      # Vite dev server :5173, proxies /api/ai -> :8000, /api/lms -> :80
npm run build    # production bundle (consumed by the nginx gateway in prod)
npm run lint     # eslint
npm run test:moodle-section   # contract test: scripts/verify_moodle_section_contract.mjs
```

### Full stack (deploy mode)
```bash
docker compose up -d   # gateway(nginx) + frontend(static) + fastapi + ollama + loki/promtail/grafana
```
Copy `.env.example` → `.env` first. First Ollama boot pulls models (5–15 min).

## Architecture essentials

### Two run modes, one codebase
- **Dev**: native XAMPP Moodle (:80), native Ollama (:11434), `uvicorn` (:8000), Vite (:5173). No physical gateway — Vite's proxy plays that role.
- **Deploy**: `docker compose` brings up the nginx gateway (`8090:80` in dev, `80:80` on the server) + all services; Moodle stays external (`host.docker.internal` / configurable upstream in `nginx/nginx.conf`).

Parity is guaranteed because the frontend **only ever calls two prefixes**, mapped identically by Vite (dev) and nginx (prod):
- `/api/ai/*` → FastAPI (RAG service)
- `/api/lms/*` → Moodle (Apache/PHP)
- (`/moodle_api/*`, `/rag_api/*` are legacy aliases kept because PHP responses hardcode them.)

### Request flow (student asks the tutor)
SPA → gateway `/api/ai/chat` (rate-limited per token) → FastAPI `POST /chat` → auth (token validated against Moodle DB) → LangGraph `super_agente` → retrieval (Chroma, pre-filtered by course) + Ollama → answer + traces persisted to Moodle tables. Every request emits a JSON log → Promtail → Loki → Grafana.

### The LangGraph agent (`tesis-rag/services/agent/`)
`agent_service.py` is a thin façade over `services/agent/graph.py`. The graph is a **supervisor router** (`nodo_supervisor`) that dispatches to one of: `agente_rag` (the main path), `agente_web` (DuckDuckGo, only when the user forces it), `guardia` (out-of-domain refusal), `saludo` (greetings, no LLM), `perdido` ("lost student" guidance mode). Logic is split across `routing.py`, `retrieval.py`, `verification.py`, `vision.py`, `prompts.py`. The RAG node does heavy **post-generation verification** (strips invented citations/locations, gates "future axis" previews, repairs generic "no evidence" answers from contextual metadata) — changes to answer behavior usually belong in `verification.py`/`retrieval.py`, not just the prompt.

### Domain Pack — domain lives in data, not code
All course-specific knowledge (persona, node prompts, axis taxonomy, concept lexicon, bl/allow-lists, controlled FAQ answers) is loaded from `tesis-rag/domain_packs/<course_id>.json` via `services/domain/domain_pack.py`; `_default.json` is the neutral fallback. The Python agent is meant to be a "blank canvas" that processes injected domain data. **Do not re-hardcode domain vocabulary into the agent** — extend the pack JSON. `course_id` == the numeric Moodle course id (pilot default `2`).

### Contextual tutor — three layers (don't conflate them)
- **Layer 1 (knowledge / RAG)**: the indexed corpus, retrieved per axis/section. `ingest.py` + ChromaDB (`bd_vectorial/`).
- **Layer 2 (activity context)**: what the student is doing *right now* (current lesson/section/active video block). Built by `services/context_service.py` into a pre-rendered text block that is **injected into the prompt but never added to the retrieval query** (avoids polluting search).
- **Layer 3 (session state)**: per-session runtime state.

Related distinction baked into the schema: **inject vs index**. A document/resource has independent flags `allowed_for_indexing` (text becomes RAG evidence) and `visible_to_student` (file may be shown/downloaded). A resource can be indexed-but-not-visible (tutor uses the text as knowledge but must not surface the file).

### Persistence is Moodle-first (`tesis-rag/services/db_service.py`)
The operational DB **is Moodle's MariaDB**; project tables are the `mdl_local_tesisai_*` tables defined in the plugin's `db/install.xml` (lessons, lesson_blocks, course_resources, resource links, prompts, tutor sessions/messages, message/interaction traces, session_context, axes, documents, transcript_segments). SQLite (`bd_chat/`) is a **dev-only fallback**. Per the SOA contract, direct reads of core Moodle tables are forbidden **except** `mdl_external_tokens` (auth) and `mdl_local_tesisai_*` (ours); everything else goes through Web Services.

### Auth contract (`tesis-rag/api/dependencies.py`)
- `get_current_user_id`: `Authorization: Bearer <moodle_token>` validated against `mdl_external_tokens`. When Moodle DB is active the token is **mandatory**; only in isolated dev (SQLite, no Moodle) is the `X-User-Id` header accepted.
- `require_teacher`: teacher/manager actions (authoring) require `X-Course-Id` and a Moodle teacher role in that course. It resolves the client-sent course id (which may be HMAC-**signed** — see `_sign_course_id`/`_decode_signed_course_id`) to the canonical numeric id for write scoping.

## Gotchas

- **`.pyc` files are tracked in git** (the `__pycache__` dirs under `tesis-rag/`). `git stash`/`pop` jams on them — use `git show`/`git worktree` to compare against HEAD instead of stashing. (Remembered project hazard.)
- **Reindex is destructive**: `reindex_rag_clean.py` / `rebuild_all_documents()` wipes and rebuilds ChromaDB. Several `bd_vectorial_backup_*` dirs exist because of this. After changing axis→section mapping or ingest logic, a reindex is required for it to take effect.
- **Corpus ingestion policy**: only files under approved paths with the right markers get indexed. `documentos/no_indexar/**` is explicitly excluded; `documentos/oficial/**` (ejes, global, guiones) is the canonical corpus. See `es_documento_aprobado_para_indexar()` and the `tests/test_ingest_public_policy.py` / `test_source_policy.py` guards before changing ingest filtering.
- **Lesson identity is anchored to the Moodle `cmid`**, not list position — reordering lessons must not swap their metadata.
- The `local_tesisai_axes` table and "axis" concept are partly being migrated toward Moodle sections; check current memory notes before building on axis-specific code.
