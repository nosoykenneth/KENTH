# H5P + Learning Signals — evaluación formativa que alimenta al tutor

> Documento vivo para la redacción (Capítulos IV–V). Diagramas: `diagramas.md`
> §8 (flujo) y §10 (estados).

## 1. Qué se construyó

Las 7 lecciones de la Sección 0 tienen su video convertido en **H5P
InteractiveVideo** (mod_hvp) con **29 interacciones calificables** (multiple
choice, true/false, summary) inyectadas vía `H5PCore::filterParameters` sobre
los contenidos existentes (sin reimportar `.h5p`, preservando el `cmid`).

La fuente única de las interacciones es el **manifest pedagógico**
`tesis-rag/data/learning_signals/course_2_interactions.json`: cada interacción
declara su `concept`, su enunciado y su **remediación** (timestamp del video,
recurso real de la lección y micro-práctica). El mismo manifest generó las
interacciones H5P y ahora interpreta los resultados: cada respuesta es
atribuible a un concepto.

## 2. Cadena de datos

1. El estudiante responde el InteractiveVideo → Moodle guarda
   `mdl_hvp_xapi_results` (padre compound + hijos por interacción) y gradebook.
2. `services/learning_signals.py` lee esos resultados (vía `db_service`),
   los mapea a conceptos por enunciado (respaldo: orden) y produce **señales**:
   `status` (`empty|not_attempted|available|error`), `percentage`,
   `level` (`needs_reinforcement <60 | partial 60–79 | ready >=80`),
   `weak_concepts` **priorizados por menor acierto** y `recommended_review`
   (máx. 3, cada uno con minuto+recurso+micro-práctica).
3. Dos consumos, ambos runtime (Capa 3):
   - **Guidance determinística** (`build_guidance_message`): mensaje listo para
     UI sin tocar el modelo ni Chroma. Cubre 1/2/3+ conceptos débiles con
     prioridades y respeta el nivel de ayuda configurado por el docente.
   - **Inyección al chat** (`signals_block_for` → bloque "SEÑALES DE
     APRENDIZAJE" en el contexto del tutor): el agente RAG orienta con los
     mismos datos cuando el alumno conversa.

## 3. Endpoints

| Endpoint | Guard | Uso |
|---|---|---|
| `GET /api/ai/learning-signals/lesson/{id}/me` | token del alumno | sus señales (solo suyas) |
| `GET /api/ai/learning-signals/lesson/{id}/summary` | require_teacher | agregado del aula (promedio, distribución, conceptos más fallados) |
| `POST /api/ai/learning-signals/sync/lesson/{id}` | require_course_view | recálculo idempotente del snapshot propio |
| `POST /api/ai/learning-signals/lesson/{id}/guidance` | require_course_view | guía determinística lista para UI |

## 4. UX de la orientación (cierre jul 2026)

- **Chat abierto**: la guía se inserta en el historial (dedupe por
  `attempt_id`).
- **Chat cerrado**: badge "Conviene reforzar · el tutor tiene una guía" +
  flecha con contador + sonido sutil (una sola vez por intento).
- **Persistencia**: la guía se guarda por curso+lección
  (`localStorage`, módulo puro `guidanceStore.js`) con `notified_at`/`seen_at`:
  sobrevive recargas, no repite sonido, expira a los 7 días y **nunca cruza de
  una lección a otra**.
- **Recuperación**: el badge es botón ("Ver guía del tutor") → abre el chat y
  reinserta o enfoca el mensaje (nunca duplica). La flecha del tutor hace lo
  mismo al abrir.
- Nuevo intento (attempt_id distinto) → nueva notificación completa.

## 5. Principios no negociables

- Las señales son **estado del alumno**, no evidencia del curso: **NUNCA se
  indexan en Chroma** ni entran a la query vectorial.
- Tono **no punitivo** ("conviene reforzar", nunca "vas mal"); no se recitan
  cifras salvo que aporten; jamás se exponen internos (xAPI, Chroma, ids).
- `ready` no dispara alerta amarilla: reconoce el avance y sugiere reto o
  siguiente actividad (solo menciona repaso suave si hubo un fallo puntual).
- `not_attempted`: invitación a hacer la actividad, sin inventar desempeño.

## 6. Validación

- `tests/test_learning_signals.py` (manifest, mapeo, niveles, señales, resumen,
  render, guidance) + `tests/test_final_ux_guidance.py` (multi-concepto,
  prioridades, help_level, chat general) — suite completa verde.
- Contrato frontend: `npm run test:guidance`
  (`verify_guidance_recovery_contract.mjs`).
- Datos reales en producción: 49 filas xAPI, resultados en 6/7 videos
  (Lección 6 sin intentos al cierre).

## 7. Pendientes

- Panel del profesor (`H5PSignalsPanel`) muestra el agregado por lección; una
  vista longitudinal por estudiante queda como trabajo futuro.
- Las señales dependen de que el estudiante responda el H5P (sin intento no hay
  personalización — by design).
