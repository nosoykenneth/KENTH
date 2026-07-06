# FASE 3 — Auditoría: tono y nivel de ayuda por lección

## Dónde vive la configuración
- **UI**: Vista Profesor (`TutorPedagogyView.jsx`) — selects "Tono" (`TONE_OPTIONS`) y
  "Nivel de ayuda" (`HELP_OPTIONS`). Opciones REALES:
  - tono: `directo | paciente | exigente | socratico | practico | "" (automático)`
  - ayuda: `orientar | explicar | corregir | preguntar | ejemplo_guiado | "" (automático)`
- **Persistencia**: `PUT /authoring/lessons/{id}/pedagogy` (apply_profile) →
  `mdl_local_tesisai_lessons.metadata_json → $.pedagogy.tutor_tone / $.pedagogy.help_level`.
  Es **metadata inyectada**, NO entra a Chroma (inject-vs-index respetado). ✔
- **Consumo en chat**: `context_service.render_context_block` lee
  `active_lesson.metadata.pedagogy` y lo inyecta en el bloque CONTEXTO ACTIVO. ✔ (por lesson_id)
- **Consumo en guidance**: ANTES el guidance determinístico NO lo usaba. ✖→✔ corregido:
  `learning_signals.guidance_for` lee `help_level` de la lección (`_lesson_help_level`).

## Hallazgo central (pre-fix)
La inyección existía pero era DÉBIL: solo la palabra cruda
("Tono del tutor solicitado por el profesor: practico"). Con llama3.1:8b el efecto
era marginal → el profesor percibía que "no afecta".

## Fix aplicado
- `services/pedagogy_profile.py`: `TONE_DIRECTIVES` / `HELP_DIRECTIVES` — cada valor
  de la UI se traduce a una directiva OPERATIVA de comportamiento (determinista).
- `services/context_service.py`: inyecta "COMO APLICAR EL TONO: …" y
  "COMO APLICAR EL NIVEL DE AYUDA: …" + regla: el comportamiento nunca elimina
  minuto/recurso cuando hay learning_signals.
- `services/learning_signals.py`: el cierre del mensaje de guía respeta help_level
  (`_HELP_LEVEL_CLOSERS`), sin perder timestamp/recurso/micro-práctica.
- Valores desconocidos/vacíos → no se inyecta directiva (default limpio).

## Tabla de estado por lección (curso 2, pre-fix == post-fix en datos)
| lesson_id | tono_configurado | nivel_ayuda | source_config | usado_en_chat | usado_en_guidance | verdict |
|---|---|---|---|---|---|---|
| SEC2-R55 | practico | orientar | metadata_json $.pedagogy | SÍ (+directiva operativa) | SÍ (cierre por help_level) | OK post-fix |
| SEC2-R56 | practico | orientar | metadata_json $.pedagogy | SÍ (+directiva operativa) | SÍ | OK post-fix |
| SEC2-R57 | practico | orientar | metadata_json $.pedagogy | SÍ (+directiva operativa) | SÍ | OK post-fix |
| SEC2-R58 | practico | orientar | metadata_json $.pedagogy | SÍ (+directiva operativa) | SÍ | OK post-fix |
| SEC2-R59 | practico | orientar | metadata_json $.pedagogy | SÍ (+directiva operativa) | SÍ | OK post-fix |
| SEC2-R60 | practico | orientar | metadata_json $.pedagogy | SÍ (+directiva operativa) | SÍ | OK post-fix |
| SEC2-R61 | practico | orientar | metadata_json $.pedagogy | SÍ (+directiva operativa) | SÍ | OK post-fix |

Antes del fix el verdict era "PARCIAL: se inyecta la palabra pero sin semántica
operativa; guidance determinístico la ignoraba".

## Garantías (tests: tests/test_final_ux_guidance.py)
- Directivas cubren TODAS las opciones reales de la UI; desconocidas no inyectan.
- practico/orientar, socratico/preguntar, exigente/corregir verificados en el render.
- El nivel de ayuda NUNCA elimina minuto/recurso en la guía (test explícito).
- Sin pedagogía configurada → cero inyección (no contamina otras lecciones).
- Las preferencias NO se indexan en Chroma (inject-only, sin cambios de ingest).

## Nota sobre el encargo
El encargo mencionaba opciones hipotéticas (Técnico/Motivador/Neutral, Pistas/
Paso a paso/Respuesta directa). NO existen en la UI ni en datos: se implementaron
directivas para las opciones REALES (directo/paciente/exigente/socratico/practico
y orientar/explicar/corregir/preguntar/ejemplo_guiado) para no inventar
funcionalidad. La semántica pedida quedó cubierta por equivalencia:
practico≈Práctico, socratico≈Socrático, orientar≈Orientar, preguntar≈Pistas,
ejemplo_guiado≈Paso a paso guiado, explicar≈Respuesta directa + comprobación.
