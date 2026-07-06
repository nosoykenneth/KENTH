# Tutor adaptativo — cómo el tutor personaliza sin dejar de ser verificable

> Documento vivo para la redacción (Capítulos IV–V). Diagrama del contexto:
> `diagramas.md` §9; estados: §10.

## 1. Las tres capas del tutor (no conflar)

| Capa | Qué es | Cómo llega al modelo |
|---|---|---|
| 1. Conocimiento | corpus aprobado del curso (transcripciones, recursos, teacher_context) | **RAG**: retrieval Chroma scope-aware, citado como fuentes |
| 2. Contexto de actividad | dónde está el alumno: lección, momento del video, bloque activo, perfil pedagógico de la lección | **inyección** (bloque CONTEXTO ACTIVO), nunca en la query vectorial |
| 3. Estado runtime | sesión + **learning signals** (desempeño H5P del alumno) | **inyección** (bloque SEÑALES), nunca indexado |

## 2. Adaptación por desempeño (learning signals)

Cuando el alumno pregunta dentro de una lección con actividad H5P respondida,
el tutor recibe sus conceptos débiles **priorizados** y las remediaciones del
manifest (minuto + recurso + micro-práctica) con la instrucción de mencionarlas
explícitamente. Reglas por nivel:

- `needs_reinforcement`: orientación guiada, pasos concretos, sin reto avanzado.
- `partial`: refuerzo puntual, conectar los conceptos fallados, práctica corta.
- `ready`: reconocer avance, proponer reto aplicado; sin alerta de refuerzo.

Con 3+ conceptos débiles el tutor cubre máximo 3 como "Prioridad 1/2/3" y
recomienda una ruta corta — no satura.

## 3. Adaptación por configuración docente (tono / nivel de ayuda)

El docente configura por lección (Vista Profesor → perfil canónico,
`metadata.pedagogy`):

- **Tono**: `directo | paciente | exigente | socratico | practico`
- **Nivel de ayuda**: `orientar | explicar | corregir | preguntar | ejemplo_guiado`

Cada valor se traduce a una **directiva operativa** determinística
(`services/pedagogy_profile.py: TONE_DIRECTIVES / HELP_DIRECTIVES`) que
`context_service` inyecta como norma de comportamiento ("COMO APLICAR EL
TONO…"). Regla dura inyectada junto a ellas: *el tono y el nivel de ayuda
regulan CÓMO responde, nunca la verdad del contenido; jamás omiten el minuto o
el recurso cuando hay señales*. La guidance determinística también respeta el
nivel de ayuda (cierre del mensaje).

## 4. Chat de lección vs chat general

| | Chat de lección | Chat general (fuera de lecciones) |
|---|---|---|
| Contexto activo | lección/bloque/momento | ninguno |
| Learning signals | inyectadas (si hay actividad) | **nunca** (no hay lesson_id) |
| Tono/nivel de ayuda | los de la lección | ninguno (neutral) |
| "¿Qué debo reforzar?" | orienta con las señales reales | respuesta determinística: pide abrir una lección específica (no inventa señales) |
| RAG | scope lección>sección>curso | RAG general del curso |

El deflector del chat general (`is_personal_progress_question` +
`GENERAL_PROGRESS_NO_LESSON_MESSAGE` en `chat.py`) es deliberadamente estrecho:
solo preguntas personales de progreso; el resto sigue el flujo normal del
agente.

## 5. Verificación post-generación (anti-alucinación)

Después de generar, `verification.py` repara/bloquea: citas o ubicaciones
inventadas, previews de contenido futuro no delegado, respuestas "sin
evidencia" reparables desde metadata contextual, violaciones de
`attribution_constraints`. La orientación H5P además es **determinística**
(no pasa por el modelo), así que el minuto/recurso recomendados nunca son
alucinados.

## 6. Trazabilidad

Cada interacción persiste su traza (`interaction_traces`): intención, ruta,
scope de retrieval, chunks y scores, fuentes, modelo, latencia, políticas
aplicadas y si hubo señales (`runtime_context.has_learning_signals`). Esto
sostiene el requisito de **precisión medible** (OE4) del anteproyecto.

## 7. Pendientes

- El tono/nivel están configurados hoy de forma homogénea
  (practico/orientar en las 7 lecciones); la diferenciación por lección es
  decisión pedagógica del docente, el mecanismo ya la soporta.
- `session_state` (señales de frustración/perdido) es heurístico simple.
