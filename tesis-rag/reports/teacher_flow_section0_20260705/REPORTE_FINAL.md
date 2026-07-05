# REPORTE FINAL — Flujo docente RAG para la Sección 0

**Rama:** `feat/teacher-driven-rag-section0` (desde `main` @ `07bdf30`).
**Fecha:** 2026-07-05. **Curso:** 2 (Mezcla y Masterización). **Sección:** 0 — El
sistema de decisión (`moodle_section_id=2`, `section_number=1`).

## Resumen ejecutivo

Se implementó el **flujo docente teacher-driven** que permite alimentar el RAG del
tutor **desde la interfaz** (sin Markdown/YAML/Chroma): transcripción aprobada →
"Preparar tutor con IA" → aceptar → `teacher_approved_context` materializado e
**indexado incremental**. Validado end-to-end **localmente sobre las 2 lecciones que
existen en la BD local (0.1, 0.2)**. Las 5 lecciones restantes (0.3–0.7) **no existen
en la BD local** (viven sólo en el servidor); su población se ejecuta con el mismo
driver en el runbook del servidor.

## Mapeo de lecciones (Fase 1)

| corpus | título esperado | lesson_id | cmid | en BD local | acción |
|---|---|---|---|---|---|
| 0.1 | Mezclar es decidir: el ciclo de trabajo | SEC2-R55 | 55 | ✅ | importada+aprobada+indexada+teacher_context |
| 0.2 | Tu oído miente: percepción y nivel de escucha | SEC2-R56 | 56 | ✅ | importada+aprobada+indexada (teacher_context pendiente de ai_prepare) |
| 0.3 | Monitores y auriculares: trabajar con lo que tienes | SEC2-R57 | 57 | ❌ server-only | runbook servidor |
| 0.4 | Anatomía universal del mixer: ruteo | SEC2-R58 | 58 | ❌ server-only | runbook servidor |
| 0.5 | Gain Staging: el cimiento de toda la cadena | SEC2-R59 | 59 | ❌ server-only | runbook servidor |
| 0.6 | Nativos vs emulaciones analógicas: la matriz de decisión | SEC2-R60 | 60 | ❌ server-only | runbook servidor |
| 0.7 | Checklist de sesión lista para mezclar | SEC2-R61 | 61 | ❌ server-only | runbook servidor |

- Regla `lesson_id = SEC2-R{cmid}`, `cmid = 54 + número`. Verificado 1‑a‑1.
- **Sin cruces de título.** Cada `.txt` autodeclara su número de lección en la 1ª
  línea; el driver lo verifica. 0.5 = Gain Staging, 0.6 = Nativos (no cruzados).
- Los títulos en BD son UTF-8 correcto (el "mojibake" era artefacto de consola).

## Transcripciones importadas (Fase 2/3)

- Formato origen: `[MM:SS.mmm --> MM:SS.mmm]  texto` (VTT-like), UTF-8, 7 archivos.
- Tratadas como **verdaderas/aprobadas** (equiv. Whisper corregido). Sin metadatos
  visibles de origen. Timestamps preservados (segmentación operativa).
- Local aplicado: R55 (95 segmentos, ~510 s), R56 (87 segmentos, ~459 s), estado
  `transcript_status=approved`.

## Cambios de código

| Área | Archivo | Qué |
|---|---|---|
| Fase 3 | `config.py` | flag `INDEX_TRANSCRIPT_ONLY_AFTER_APPROVAL` (default true) + estados + helper |
| Fase 3 | `services/transcription_service.py` | Whisper crudo → `generated_pending_review`, NO indexa con flag on |
| Fase 5 | `services/teacher_context.py` (nuevo) | `build_teacher_approved_context_document` + `publish_lesson_teacher_context` |
| Fase 5 | `ingest.py` | `index_teacher_approved_context` + `delete_teacher_approved_context`; transcript `lesson_title` humano |
| Fase 6 | `api/routes/authoring.py` | accept publica + `POST /publish` (require_teacher) |
| Fase 6 | `ingest.reindex_course_documents` | reindexa también teacher_context por lección |
| Fase 12 | `frontend .../TutorPedagogyView.jsx`, `sectionsService.js` | botón "Publicar cambios del tutor" + estados humanos |
| Driver | `scripts/teacher_flow_section0.py` | import→approve→index→teacher_context→dedupe→audit (idempotente, dry-run) |
| Val. | `scripts/chat_validate_section0.py` | chat por lección por invocación directa del agente |
| Tests | `tests/test_teacher_flow.py` | 13 pruebas del contrato del flujo |

## Chroma antes/después (local, Sección 0)

| | antes | después |
|---|---|---|
| chunks Sección 0 | 15 (transcripción vieja, formato path-form) | **19** |
| R55 | 8 | 11 (9 transcript + 2 teacher_context) |
| R56 | 7 | 8 (8 transcript) |
| stale (axis / path-form source) | 15 (formato viejo) | **0** |

Backup previo: `bd_vectorial_backup_teacherflow_20260705_142050`.

## Validaciones

- **Chroma (Fase 10):** ver `CHROMA_POST_AUDIT.md`. Todos `visible=true`,
  `allowed=true`, `scope=lesson`, `section_number=1`; 0 stale; 0 axis.
- **Chat (Fase 11):** ver `CHAT_VALIDATION.md`. R55/R56 grounded, `scope=lesson`,
  sin fuga de IDs ni de otra lección; fuera de dominio rechazado. Hallazgo menor:
  muletilla "según la evidencia" del modelo local `llama3.2:3b` (no del prompt).
- **Tests backend:** `pytest tests/` → **213 passed, 4 skipped** (incluye
  `test_teacher_flow.py` 13/13).
- **Frontend:** `lint` 0 errores; `test:moodle-section` OK; `test:chat-sources` OK;
  `build` OK.

## Riesgos pendientes / notas

1. **0.3–0.7 no existen en la BD local** (sólo servidor). Su población completa
   (transcripción + ai_prepare + teacher_context) se ejecuta en el runbook servidor.
2. **ai_prepare requiere `qwen2.5:14b-instruct`** (ausente en local). Por eso R56
   local no tiene aún `teacher_approved_context`. En el servidor sí está disponible.
3. **Muletilla "según la evidencia"** (modelo pequeño local): follow-up de bajo
   riesgo en `verification.py`, fuera de este alcance para no tocar el gate phase0.
4. **Bloques de R55 previos** eran de una grabación anterior; `ai_prepare` en el
   servidor los realinea a la transcripción importada.

## Rollback

- Índice: restaurar `bd_vectorial_backup_teacherflow_20260705_142050` sobre
  `bd_vectorial` (o `--supersede-canonical` no se usó, así que el corpus MD sigue).
- Código: `git revert` del merge / volver a `main@07bdf30`.
- BD: la transcripción es delete-then-add por lección; re-importar la anterior si
  hiciera falta (no se borran otras lecciones ni otras secciones).

## Runbook del servidor (poblar las 7 lecciones + deploy)

Ver `docs/tic/FLUJO_DOCENTE_RAG.md` y la sección "Deploy" del PR. Resumen:

```bash
# 1) Alinear código
ssh kenneth@100.97.90.86
cd /srv/kenneth/tic-kenth
git fetch origin && git checkout main && git reset --hard origin/main
docker compose -f docker-compose.deploy.yml --env-file .env build fastapi frontend
docker compose -f docker-compose.deploy.yml --env-file .env up -d fastapi frontend

# 2) Copiar las 7 transcripciones al contenedor (o bind-mount) y correr el driver
#    DENTRO del contenedor fastapi (tiene Ollama + BD + Chroma del server):
docker compose -f docker-compose.deploy.yml exec fastapi \
  python scripts/teacher_flow_section0.py            # DRY-RUN primero
docker compose -f docker-compose.deploy.yml exec fastapi \
  python scripts/teacher_flow_section0.py --apply --report reports/teacher_flow_section0_server

# 3) Preparar tutor con IA por lección (ai_prepare) — 0.1..0.7 — y publicar:
#    vía UI (profesor) o el endpoint /ai-prepare + /ai-prepare/accept por lección.

# 4) Validar
docker compose -f docker-compose.deploy.yml exec fastapi \
  python scripts/chat_validate_section0.py --report reports/teacher_flow_section0_server
bash scripts/smoke_produccion.sh

# 5) Verificar título de R59 == "Gain Staging" y R60 == "Nativos" (anti-cruce) ANTES
#    de indexar; el driver avisa si el .txt no autodeclara el número esperado.
```

## Definition of Done — estado (COMPLETADO en servidor)

Ver detalle en `SERVER_RESULTS.md` y evidencia en `server/*.json`.

| Criterio | Local | Servidor (prod) |
|---|---|---|
| 7 lecciones mapeadas correctamente | ✅ | ✅ (R55–R61) |
| Transcripciones cargadas y aprobadas | ✅ 0.1, 0.2 | ✅ 0.1–0.7 |
| Transcripciones viejas reemplazadas | ✅ | ✅ (delete-then-add) |
| Títulos cruzados corregidos antes de indexar | n/a | ✅ R59 "Nativos"→"Gain Staging", R57 |
| Perfil IA generado/aceptado por lección | parcial (R55/R56 smoke) | ✅ 0.1–0.7 (`ai_prepare ok` ×7, qwen3:14b) |
| `teacher_approved_context` por lección | ✅ R55 | ✅ 7/7 (43 chunks) |
| Indexado incremental (sin rebuild global) | ✅ | ✅ |
| Chroma sin stale/axis | ✅ | ✅ (0 stale, 0 axis) |
| Chat responde bien por lección | ✅ R55/R56 | ✅ 7/7 (0 issues serios, R59→Gain Staging) |
| Fuera de dominio rechazado | ✅ | ✅ |
| Profesor sin Markdown/YAML/Chroma | ✅ (flujo + UI) | ✅ (mismo código) |
| Tests / build / lint | ✅ | n/a |
| Smoke de producción | n/a | ✅ 9 PASS / 0 FAIL |
| Servidor en `main` limpio | — | ✅ `1dbe5cd`, árbol rastreado limpio, health ok |

**Flujo docente RAG LISTO para Sección 0.** Las 7 lecciones tienen transcripción
aprobada + perfil IA aceptado + `teacher_approved_context` indexado; el tutor
responde grounded por lección sin cruces (R59 = Gain Staging, R60 = Nativos); 0
chunks stale/axis; smoke 9/9; servidor en `main` limpio y sano.

**Decisión Fase 7 (dueño):** se **mantiene** el corpus `canonical_md` (208 chunks)
junto al flujo docente — flujo docente = fuente primaria, corpus canónico
complementa. Reversible a índice puro-flujo con `--supersede-canonical`.
