# SERVER_RESULTS — Flujo docente RAG en producción (bodyguard26)

Ejecución del runbook completo en el servidor (`kenneth@100.97.90.86`,
`/srv/kenneth/tic-kenth`, `docker-compose.deploy.yml`). Fecha 2026-07-05.
Código: `main` @ `1dbe5cd` (merge de PR #13). Evidencia cruda:
`server/teacher_flow_run.json`, `server/chat_validation.json`.

## Deploy

- `git reset --hard origin/main` → `1dbe5cd`; los 7 `.txt` de transcripción y los
  scripts quedaron en la imagen tras `build fastapi frontend` + `up -d`.
- **Gotcha aplicado:** tras recrear `fastapi`, el gateway nginx devolvía 502 (IP
  upstream vieja); `up -d --force-recreate gateway` lo resolvió.
- Health tras deploy: `status:ok` (fastapi/moodle_db/moodle_ws/chroma/ollama ok).
- Chroma respaldado antes de mutar: `runtime/chroma_backup_teacherflow_20260705_194545` (19M).

## Fase 1 — corrección de títulos (anti-cruce) ANTES de indexar

Los títulos cacheados en `mdl_local_tesisai_lessons.title` estaban desalineados
respecto al **nombre real del H5P** (fuente de verdad, lo que ve el alumno):

| lesson_id | title cacheado (antes) | H5P real / corregido |
|---|---|---|
| SEC2-R57 | "3 — Volumen y Gain" | **Lección 3 — Monitores y auriculares…** |
| SEC2-R59 | "Lección 5 — Nativos vs emulaciones…" | **Lección 5 — Gain Staging…** |

Se corrigieron los 7 títulos al nombre H5P (R59 y R57 eran los cruzados; el resto
ya coincidía). Esto satisface la regla explícita: *"Si SEC2-R59 dice 'Nativos' pero
visualmente aparece 'Gain Staging', corregir antes de indexar."*

## Fase 2/6/8 — población de las 7 lecciones (un comando)

`scripts/teacher_flow_section0.py --apply --ai-prepare` (modelo `qwen3:14b`):

| # | lesson_id | segmentos | transcript chunks | teacher_context chunks | ai_prepare |
|---|---|---|---|---|---|
| 0.1 | SEC2-R55 | 95 | 9 | 6 | ok |
| 0.2 | SEC2-R56 | 87 | 8 | 7 | ok |
| 0.3 | SEC2-R57 | 66 | 6 | 6 | ok |
| 0.4 | SEC2-R58 | 68 | 6 | 6 | ok |
| 0.5 | SEC2-R59 | 63 | 6 | 6 | ok |
| 0.6 | SEC2-R60 | 64 | 6 | 6 | ok |
| 0.7 | SEC2-R61 | 59 | 6 | 6 | ok |

Cada `ai_prepare` promovió el perfil completo (learning_goal, lesson_summary,
key_concepts, common_mistakes, probable_questions, tutor_focus, moments 4–8) y
publicó su `teacher_approved_context`. Total teacher_context: **43 chunks**.

## Chroma (Sección 0)

- pre: 233 → post: **299** chunks.
- Composición: `canonical_md`=208, `transcript`=47, `teacher_approved_context`=43,
  `resource_file`=1.
- **0 chunks stale** (path-form `transcription:*`), **0 `axis`/`axis_id`**.
- Decisión del dueño (Fase 7): **mantener ambos** — el flujo docente es la fuente
  PRIMARIA (transcripción real + contexto aprobado) y el corpus canónico
  complementa con profundidad técnica. No se superseder (reversible con
  `--supersede-canonical` si se decide índice puro-flujo).

## Fase 11 — validación de chat (7 lecciones, 21 preguntas + borde)

Modelo de chat: `llama3.1:8b`. **0 problemas serios** (sin fuga de IDs, sin
herencia de otra lección, sin respuestas vacías). Todas `scope=lesson` salvo 2
preguntas ambiguas que —correctamente— pidieron precisión (`ev=bajo`).

| lección | ¿De qué trata? (resumen respuesta) |
|---|---|
| 0.1 | mezclar = decisiones conscientes; ciclo de trabajo |
| 0.2 | tu oído miente; nivel de escucha |
| 0.3 | trabajar con el equipo que tienes; monitores/auriculares |
| 0.4 | anatomía universal del mixer; ruteo |
| **0.5** | **gain staging; evitar saturación** ✅ (no "Nativos" — cruce resuelto) |
| 0.6 | nativos vs emulaciones; matriz de decisión |
| 0.7 | checklist de 6 bloques para dejar la sesión lista |

- **R59 responde sobre Gain Staging** (no Nativos): el arreglo de título se validó
  end-to-end en el tutor.
- Fuera de dominio ("¿capital de Francia?") → `bloqueo` (`out_of_domain:semantic`).
- Muletilla "según la evidencia" en 10/21 respuestas: comportamiento intermitente
  del modelo (no del prompt/pack), pre-existente; follow-up de bajo riesgo.

## Smoke de producción

`scripts/smoke_produccion.sh` → **9 PASS / 0 FAIL** (seguridad sin token 401/403,
assets 200, 9 contenedores arriba). Pruebas autenticadas omitidas (sin MOODLE_TOKEN).

## Estado final

- Servidor en `main` @ `1dbe5cd`, árbol rastreado **limpio**, health `status:ok`.
- 7 lecciones de Sección 0 con transcripción aprobada + perfil IA + contexto
  aprobado indexado; tutor grounded por lección; sin cruces de título.
- Rollback: restaurar `runtime/chroma_backup_teacherflow_20260705_194545`.
