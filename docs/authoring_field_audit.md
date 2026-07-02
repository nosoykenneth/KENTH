# Auditoría de campos de autoría del tutor (FASE 1)

> Rama: `feat/professor-video-timeline-cleanup` · Fecha: 2026-07-01
> Objetivo: inventariar **campo por campo** todo lo editable/visible en la autoría del
> tutor, determinar su **uso real** (prompt del tutor, RAG/indexación, UI del estudiante,
> evaluación, recursos, timeline, guardado útil) y decidir dónde debe vivir.
> Nada se borra de la BD en esta fase; solo se documenta y se decide visibilidad de UI.

## Método

Se leyó el código real (no se asumió uso por existencia):

- Frontend: `TutorPedagogyView.jsx` (Vista Profesor), `LessonVideoEditor.jsx` (Editor
  avanzado), `BlockTimeline.jsx`, `LessonResourcesPanel.jsx`, `sectionsService.js`,
  `types/lesson.ts`, `permissions.js`, gating en `CourseContentView.jsx`.
- Backend: `api/routes/authoring.py` (payloads + endpoints `/moments` y `/blocks`),
  `services/context_service.py` (qué se **inyecta** al prompt), `services/lesson_service.py`
  (`load_lesson`), `services/ai_prepare/{schema,persistence,service}.py` (borrador IA y
  `promote_draft`).

"Consumido por el tutor" = aparece en `render_context_block` (inyección) **o** se promueve
a un campo que sí se inyecta. "Consumido por RAG" = se indexa en Chroma (`ingest`).

## Terminología (obligatoria, no romper nombres internos)

| Capa | Etiqueta visible | Nombre técnico interno (NO cambia) |
|---|---|---|
| Admin / técnico (Editor avanzado) | **Bloques** | `block`, `blocks`, `block_id`, `lesson_blocks`, `start_time`, `end_time` |
| Vista Profesor | **Momentos de la clase** | mismos campos técnicos por debajo (`/moments` sobre `lesson_blocks`) |
| Estudiante / tutor | "momento", "parte de la lección", "parte del video" | nunca se muestra `block_id` |

Regla dura: el `block_id` (p. ej. `S0-L01-B1`) **nunca** se muestra al profesor/estudiante
ni debe aparecer como texto en la respuesta del tutor.

## Leyenda de decisiones

- `visible_profesor` — se muestra/edita en la Vista Profesor (lenguaje "Momentos").
- `visible_admin` — solo en el Editor avanzado (lenguaje "Bloques"/técnico).
- `oculto_avanzado` — se conserva en backend y se agrupa en admin bajo *"Configuración
  pedagógica avanzada"* (acordeón), fuera de la vista por defecto.
- `legacy_oculto` — ya no tiene uso real; se oculta de la UI, **no** se borra de la BD; se documenta.
- `eliminado_ui` — se retira del formulario (el campo del wire puede seguir existiendo por compat).
- `pendiente_backend` — el campo se edita pero **no se consume**; requiere decisión de backend
  (mapear/inyectar) o retirarlo de la UI.

---

## A. Campos de LECCIÓN (`LessonPayload` / `load_lesson` / `types/lesson.ts`)

| Campo | Dónde se muestra | Dónde se guarda | Quién edita | Prompt tutor | RAG | Alumno | Eval | Dup | Suele vacío | Decisión | Justificación |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `lesson_id` | Header (admin) | `lesson.lesson_id` (cmid) | sistema | sí (context) | sí (scope) | no | no | — | no | `visible_admin` (solo lectura) | Identidad anclada al cmid; **se filtra al LLM** → ver FASE 6. |
| `course_id` | — | `lesson.course_id` | sistema | sí | sí (scope) | no | no | — | no | sistema | Canónico Moodle. No es campo de formulario. |
| `moodle_section_id` | — (interno) | `lesson.moodle_section_id` | sistema (vínculo) | sí | sí (scope) | no | no | — | no | sistema | Scope de retrieval por sección. No editable a mano. |
| `axis_id` | — (siempre `""`) | `lesson.axis_id` | nadie | no | no | no | no | — | **siempre** | `legacy_oculto` | Migración ejes→secciones; el front ya envía `axis_id:''`. Esquema DB diferido. |
| `title` / `lesson_title` | Editor avanzado → Lección | `lesson.title` | admin | sí (context) | no | indirecto | no | — | no | `visible_admin` | Estructural; la IA no lo toca. |
| `order` | Editor avanzado → Lección | `lesson.order` | admin | no | no | no | no | — | no | `visible_admin` | Orden estructural = admin (reorder es `require_course_admin`). |
| `learning_goal` | Vista Profesor P3 · Editor avanzado · borrador IA | `lesson.learning_goal` | profesor + admin | **sí** (context) | no | no | sí | mismo campo en 3 UIs | a veces | `visible_profesor` + `visible_admin` | Objetivo inyectado; lo produce/edita la IA y el profesor. |
| `expected_action` | Editor avanzado → Lección | `lesson.expected_action` | admin | **sí** (context L411) | no | no | sí | — | **frecuente** | `oculto_avanzado` | Se inyecta pero es pre-IA; casi siempre vacío. Acordeón avanzado. |
| `learning_goals` (criterios de logro) | Editor avanzado → Lección | `lesson.learning_goals` | admin | **sí** (context L400) | no | no | **sí** | — | frecuente | `oculto_avanzado` | Criterios sí se inyectan; no los produce la IA. Agrupar en avanzado. |
| `prerequisites` | Editor avanzado → Lección | `lesson.prerequisites` | admin | **sí** (context L405) | no | no | no | — | frecuente | `oculto_avanzado` | Se inyecta (remite a lecciones previas). Avanzado. |
| `delegated_to_tutor` | Editor avanzado ("Delegado al Tutor") | `lesson.delegated_to_tutor` | admin (+ profesor vía IA) | **sí** (context L414) | no | no | no | mapea `tutor_focus` del borrador | a veces | `visible_admin` (+ `visible_profesor` vía "qué reforzar") | La IA promueve `tutor_focus`→`delegated_to_tutor`. |
| `attribution_constraints` | Editor avanzado ("Restricciones y Atribuciones") | `lesson.attribution_constraints` | admin (+ profesor vía IA) | **sí** (context L426, imperativo) | no | no | no | mapea `tutor_must_not_do` | a veces | `visible_admin` (+ `visible_profesor` vía "qué NO hacer") | Reglas obligatorias inyectadas. |
| `notes` | Editor avanzado ("Notas internas") | `lesson.notes` | admin | **no** (explícito) | no | no | no | — | frecuente | `visible_admin` | Interno del profe; nunca se inyecta. |
| `resources` | (gestionado por panel de recursos) | `lesson.resources[]` | sistema | indirecto | sí (vía docs) | sí | no | — | no | sistema | IDs de recursos; se gestiona en el panel, no como campo suelto. |
| `proactive_message` | Editor avanzado → Prompts · card de prueba | `lesson_prompts` | admin | **sí** (context L419) | no | sí (saludo) | no | — | a veces | `visible_admin` | Mensaje de apertura. La IA no lo genera hoy. |
| `suggested_prompts` | Editor avanzado → Prompts · card de prueba | `lesson_prompts` | admin | **sí** (context L421) | no | sí (chips) | no | — | a veces | `visible_admin` | Prompts sugeridos. |

### Lección → `metadata.pedagogy.*` (personalización del profesor, inyección aditiva)

| Campo | Vista | Guardado | Prompt tutor | Decisión | Justificación |
|---|---|---|---|---|---|
| `tutor_tone` | Vista Profesor P3 (Tono) | `metadata.pedagogy.tutor_tone` | **sí** (L440) | `visible_profesor` | La IA propone `recommended_tone`. |
| `help_level` | Vista Profesor P3 (Nivel de ayuda) | `metadata.pedagogy.help_level` | **sí** (L443) | `visible_profesor` | `recommended_help_level`. |
| `lesson_rules` | Vista Profesor P3 (Reglas importantes) | `metadata.pedagogy.lesson_rules` | **sí** (L447) | `visible_profesor` | Reglas de la lección. |
| `common_mistakes` | Vista Profesor P3 (Errores comunes) | `metadata.pedagogy.common_mistakes` | **sí** (L449) | `visible_profesor` | Errores a vigilar (nivel lección). |

### Lección → `metadata.ai_prepare.*` (aislamiento del borrador)

`draft`, `review`, `accepted_draft`, `ai_prepare_status`, `requires_review`,
`requires_reindex`, `ai_prepared_at/by`, `teacher_reviewed_at/by` → **sistema/interno**.
No son campos de formulario; no se muestran crudos. Decisión: sistema (ocultos).

---

## B. Campos de BLOQUE / MOMENTO (`Bloque` / `BlockPayload` / `MomentPayload` / `lesson_blocks`)

| Campo | Editor avanzado ("Bloques") | Vista Profesor ("Momentos") | Guardado | Prompt tutor | Decisión | Justificación |
|---|---|---|---|---|---|---|
| `block_id` | sí (etiqueta `S0-L01-B1`) | **nunca** | `lesson_blocks.block_id` | sí (context L362 → **fuga**) | `visible_admin`; quitar del texto que ve el LLM (FASE 6) | El profesor no ve IDs; el tutor no debe responder con ellos. |
| `block_order` | timeline (posición) | no | `lesson_blocks.block_order` | no | sistema | Estructura técnica; `/moments` lo preserva. |
| `start_time` / `end_time` | sí (Inicio/Fin s + drag) | **solo lectura humanizado** `0:00–1:10` | `lesson_blocks` | sí (resolución por timestamp) | `visible_admin` (crudo) / profesor solo lectura | El profesor no edita tiempos (barrera `extra="forbid"` en `/moments`). |
| `block_title` | "Título del bloque" | "Título" (del momento) | `lesson_blocks.block_title` | sí (context L362) | `visible_admin` + `visible_profesor` | Editable pedagógicamente. |
| `summary` | "Resumen (qué pasa en pantalla)" | "Resumen" | `lesson_blocks.summary` | sí (context L366) | `visible_admin` + `visible_profesor` | Editable. |
| `interaction_mode` | "Modo pedagógico" (select) + color timeline | **no** (no está en campos permitidos) | `lesson_blocks.interaction_mode` | sí (context L368 + `ctx.interaction_mode`) | `visible_admin` | Taxonomía técnica; `/moments` lo preserva si el profesor no lo envía. |
| `tutor_focus` | "Foco del tutor" | "Intención del tutor / qué reforzar" | `lesson_blocks.tutor_focus` | sí (context L370) | `visible_admin` + `visible_profesor` | Editable. |
| `concepts` | "Conceptos" | "Conceptos clave" | `lesson_blocks.concepts` | sí (context L372) | `visible_admin` + `visible_profesor` | Editable. |
| `preguntas_probables` | "Preguntas probables" | "Preguntas probables" | `lesson_blocks.preguntas_probables` | sí (context L374) | `visible_admin` + `visible_profesor` | Editable. |
| `common_mistakes` (por momento) | — | — (lo pide FASE 2 pero **no existe** a nivel bloque) | — | — | `pendiente_backend` | El borrador IA tiene `AiMoment.common_mistakes`, pero `lesson_blocks` no lo persiste. Ver hallazgo #4. |

---

## C. Campos del BORRADOR IA (`AiPrepareDraft`) y su promoción

`promote_draft` (persistence.py) mapea al ACEPTAR:

| Campo del borrador | ¿Se promueve? | Destino vivo (inyectado) |
|---|---|---|
| `learning_goal` | ✅ | `lesson.learning_goal` |
| `tutor_focus` | ✅ | `lesson.delegated_to_tutor` |
| `tutor_must_not_do` | ✅ | `lesson.attribution_constraints` |
| `recommended_tone` | ✅ | `metadata.pedagogy.tutor_tone` |
| `recommended_help_level` | ✅ | `metadata.pedagogy.help_level` |
| `lesson_rules` | ✅ | `metadata.pedagogy.lesson_rules` |
| `common_mistakes` | ✅ | `metadata.pedagogy.common_mistakes` |
| `moments[]` | ✅ | `lesson_blocks` (título/resumen/intención/conceptos/preguntas, preservando tiempos) |
| **`lesson_summary`** | ❌ | **ninguno** → ver hallazgo #1 |
| **`probable_questions`** (nivel lección) | ❌ | **ninguno** → ver hallazgo #2 |
| **`key_concepts`** (nivel lección) | ❌ | **ninguno** → ver hallazgo #3 |
| `terms_to_review` | ❌ (informativo) | — (guía de corrección de transcripción) |
| `transcript_quality_notes` | ❌ (informativo) | — |
| `confidence` | ❌ (informativo) | — (chip de confianza) |

---

## Hallazgos (campos "sospechosos / que no sirven" — lo que pidió el usuario)

**#1 — `lesson_summary` (Resumen de la clase): se edita pero NO se consume.**
La Vista Profesor P3 muestra y deja editar "Resumen de la clase", pero `promote_draft`
no lo mapea a ningún campo vivo ni `render_context_block` lo inyecta. Tras "Aceptar",
el resumen solo queda en `metadata.ai_prepare.accepted_draft` (blob muerto).
→ **Decisión propuesta**: inyectarlo como "Resumen de la lección" en `render_context_block`
(útil y barato) **o** marcarlo informativo. Recomendado: inyectar. (`pendiente_backend`)

**#2 — `probable_questions` a nivel lección: se edita pero NO se consume.**
P3 muestra "Preguntas probables (una por línea)" a nivel lección; no se promueve ni se
inyecta. Duplica el concepto per-momento (`preguntas_probables` de bloque, que sí se inyecta).
→ **Decisión propuesta**: retirar el campo de nivel lección de la UI del profesor y conservar
solo las **preguntas por momento** (evita duplicado y campo muerto). (`eliminado_ui` + `pendiente_backend`)

**#3 — `key_concepts` a nivel lección: en el form pero ni se muestra ni se promueve.**
`draftToForm` lo carga pero P3 no lo renderiza y no se promueve. Muerto.
→ **Decisión propuesta**: dropear del form. (`eliminado_ui`)

**#4 — `common_mistakes` por momento no tiene dónde guardarse.**
FASE 2 pide "errores comunes" por momento, pero `lesson_blocks` no tiene esa columna
(solo existe a nivel lección en `pedagogy.common_mistakes`). El `AiMoment.common_mistakes`
del borrador se descarta al fundir en bloques.
→ **Decisión propuesta**: NO tocar esquema en esta rama; en el modal de momento del profesor
**omitir "errores comunes" por momento** y mantener errores a nivel lección. (`pendiente_backend`)

**#5 — Fuga de IDs técnicos al LLM (FASE 6). [RESUELTO]**
`render_context_block` inyectaba `Bloque: {block_id} - {título}` y `Lección: {lesson_id} - …`
como texto que el modelo lee → riesgo de que el tutor repita códigos tipo `S0-L01-B4`.
→ **Hecho**: se quitó el `block_id` y el `lesson_id` del texto (se usan títulos + minutos
humanizados `m:ss`). La **sección SÍ se conserva** como grounding (`moodle_section_id=`),
porque un contrato existente (`test_moodle_section_contract`) y la restricción dura del encargo
("no romper moodle_section_id/section_id") lo exigen; el tutor no la verbaliza gracias a una
**instrucción anti-fuga** añadida al contexto. Cubierto por `tests/test_professor_language.py`. (FASE 6)

**#6 — Editor avanzado: campos pre-IA agrupables.**
`expected_action`, `learning_goals` (criterios), `prerequisites` siguen inyectándose pero la IA
ya no los produce y suelen estar vacíos. No borrarlos (rompería el fallback de contexto);
agruparlos en un acordeón *"Configuración pedagógica avanzada"* plegado por defecto. (`oculto_avanzado`)

**#7 — `axis_id` legacy en todos los payloads.**
El front ya envía `axis_id:''` en todas las escrituras; el backend lo fuerza a `""`. Esquema DB
diferido (Capa 4). Ocultar de cualquier UI y documentar. (`legacy_oculto`)

**#8 — Panel de recursos: expone estado técnico al profesor.**
`LessonResourcesPanel` muestra `index_status`, `chunk_count`, `index_error`, `media_type`.
FASE 4 pide ocultar lo técnico al profesor y mostrar un mensaje humano
("El tutor se actualizará después de procesar este recurso"). El admin/técnico sí puede verlo.
→ **Decisión propuesta**: parametrizar el panel con `technical={false}` para el profesor. (`visible_admin` para los badges técnicos)

**#9 — `/resources` (authoring) vs `uploadLessonResource` (ragService).**
El panel sube por `ragService.uploadLessonResource`; el endpoint `PUT /authoring/resources/{id}`
(`ResourcePayload`: `source_uri`, `duration_seconds`, `page_count`, `tags`, `axis_id`) no lo usa
la UI actual. Posible endpoint legacy/paralelo.
→ **Decisión propuesta**: no tocar en esta rama; marcar para revisión. (`legacy_oculto` a nivel UI; endpoint queda)

---

## Impacto en las fases siguientes

- **FASE 2/3 (Vista Profesor con video+timeline)**: el profesor edita momentos con
  `block_title/summary/tutor_focus/concepts/preguntas_probables` vía `PUT /moments`
  (ya existe `updateMoments` en `sectionsService.js`, hoy **no usado** por la Vista Profesor).
  Reutilizar `useResourceVideoBridge` + `BlockTimeline` con `readOnlyTimes` (sin drag, sin
  handles) y etiqueta "Momentos de la clase".
- **FASE 4 (recursos)**: reutilizar `LessonResourcesPanel` con modo no técnico.
- **FASE 5 (admin limpio)**: acordeón "Configuración pedagógica avanzada" para #6; ocultar #7.
- **FASE 6 (lenguaje)**: corregir #5 en `context_service` + regla de prompt.
- **FASE 7 (permisos)**: `/moments`=`require_teacher`, `/blocks`=`require_course_admin` (ya OK);
  la Vista Profesor debe guardar SOLO por `/moments`.

---

# Modelo pedagógico CANÓNICO (Tarea 2 — unificación Profesor/Admin/IA)

Un único **perfil pedagógico** que leen/escriben por igual la Vista Profesor, el
Editor Avanzado (admin) y el endpoint de IA; lo consume `context_service`. **No es
una tabla nueva**: es una normalización sobre el almacenamiento existente (sin
migración, sin perder datos). Implementado en `services/pedagogy_profile.py`
(`build_profile` / `apply_profile`) y expuesto por `PUT /authoring/lessons/{id}/pedagogy`.

## Campos del perfil ↔ almacenamiento real

| Campo canónico | Almacenamiento | Inyectado al tutor | Profesor | Admin |
|---|---|---|---|---|
| `learning_goal` | `lessons.learning_goal` | sí | ✔ | ✔ |
| `lesson_summary` | `metadata.pedagogy.lesson_summary` | sí | ✔ | ✔ |
| `tutor_tone` | `metadata.pedagogy.tutor_tone` | sí | ✔ | ✔ |
| `help_level` | `metadata.pedagogy.help_level` | sí | ✔ | ✔ |
| `lesson_rules[]` | `metadata.pedagogy.lesson_rules` (lista) | sí | ✔ | ✔ |
| `key_concepts[]` | `metadata.pedagogy.key_concepts` | **sí (nuevo)** | ✔ | ✔ |
| `common_mistakes[]` | `metadata.pedagogy.common_mistakes` | sí | ✔ | ✔ |
| `probable_questions[]` | `metadata.pedagogy.probable_questions` | **sí (nuevo)** | ✔ | ✔ |
| `tutor_focus[]` | `lessons.delegated_to_tutor` | sí | ✔ | ✔ |
| `tutor_must_not_do[]` | `lessons.attribution_constraints` | sí | ✔ | ✔ |
| `proactive_message` | `lesson_prompts (proactive)` | sí + **alumno** | ✔ | ✔ |
| `suggested_prompts[]` | `lesson_prompts (suggested)` | sí + **alumno (chips)** | ✔ | ✔ |
| `moments[]` | `lesson_blocks` (+ `block.metadata.common_mistakes`) | sí | ✔ (/moments) | ✔ (/blocks) |

Momento canónico: `{block_id, title, summary, pedagogical_intent, key_concepts,
common_mistakes, probable_questions}` → columnas de `lesson_blocks`
(`block_title/summary/tutor_focus/concepts/preguntas_probables`) + `common_mistakes`
en `block.metadata`. `pedagogical_intent` **unifica** con `tutor_focus` (un solo campo,
no duplicado). `block_id`/`start_time`/`end_time`/`interaction_mode`/`order` = estructura
técnica (admin), preservada por `/moments`.

## Mapeo de campos legacy (FASE 2 de la tarea)

| Campo legacy | Decisión | Mapeo | Profesor | Admin | Legacy |
|---|---|---|---|---|---|
| mensaje proactivo | **campo canónico propio** (student-facing) | `proactive_message` | ✔ | ✔ | no |
| preguntas sugeridas | **campo canónico propio** (chips del alumno) | `suggested_prompts` | ✔ | ✔ | no |
| delegado al tutor | canónico | = `tutor_focus` | ✔ ("qué reforzar") | ✔ | no |
| restricciones y atribuciones | canónico | = `tutor_must_not_do` | ✔ ("qué evitar") | ✔ | no |
| objetivo de aprendizaje | canónico | = `learning_goal` | ✔ | ✔ | no |
| prompts del tutor (lesson_prompts) | canónico | = proactive/suggested | ✔ | ✔ | no |
| acción esperada | **legacy** (se inyecta como respaldo; la IA no lo genera) | sin mapear | ✗ | ✔ colapsado | sí |
| criterios de logro | **legacy** (evaluación futura; se inyecta) | sin mapear | ✗ | ✔ colapsado | sí |
| prerrequisitos | **legacy** (navegación futura; se inyecta) | sin mapear | ✗ | ✔ colapsado | sí |
| orden | estructural | "Orden dentro de la sección" | ✗ | ✔ | no |
| axis_id | legacy (siempre `""`) | — | ✗ | ✗ | sí |

## Reglas de escritura/lectura

- **La IA** (`ai-prepare`/`accept`) rellena el mismo perfil: `promote_draft` traduce el
  borrador → perfil canónico y usa `apply_profile(mode="merge")` (vacío del borrador
  NO borra lo previo). Un solo endpoint para ambas vistas.
- **Los editores** guardan el perfil con `apply_profile(mode="replace")` vía
  `PUT /pedagogy` (permite limpiar). Los **momentos** por `/moments` (profesor, preserva
  tiempos) o `/blocks` (admin, estructura). La **estructura** (title/order/section/notes/
  legacy) por `upsert_lesson`.
- **`requires_reindex` = false** para el perfil (inyectado, no indexado). Solo
  transcripción y recursos reindexan.
- Compatibilidad: `lesson_rules` pasó de string a **lista**; `context_service` y el front
  toleran ambos. No se borra nada de la BD.
