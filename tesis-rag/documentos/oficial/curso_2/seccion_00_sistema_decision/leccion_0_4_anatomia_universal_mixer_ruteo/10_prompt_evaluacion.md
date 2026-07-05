---
course_id: "2"
moodle_section_id: "2"
section_id: "2"
section_number: "1"
section_slug: "el_sistema_de_decision"
section_title: "SECCIÓN 0: El sistema de decisión"
lesson_id: ""
lesson_number: "0.4"
lesson_title: "Anatomía universal del mixer: ruteo"
source_type: "evaluation_prompt"
scope: "lesson"
source: "canonical_md"
content_type: "markdown"
visible_to_student: false
allowed_for_indexing: false
status: "excluded_evaluation"
source_origin: "course"
corpus_version: "seccion_0_v1"
ingestion_batch_id: "seccion0_20260704"
original_relative_path: "leccion_0_4_anatomia_universal_mixer_ruteo/10_prompt_evaluacion.md"
---

# 0.4 — Prompt de evaluación (no indexable)

Uso interno. Contiene respuestas esperadas; no indexar.

## Preguntas conceptuales
1. Describe el recorrido de la señal en un mixer. *Esperado:* canal → inserts/envíos → bus → retorno → master. *Fuente:* canónico.
2. Diferencia entre insert y envío. *Esperado:* serie (toda la señal) vs. paralelo (copia). *Fuente:* canónico.
3. ¿Para qué sirven los buses? *Esperado:* agrupar y controlar varias pistas juntas. *Fuente:* canónico.
4. ¿Qué diferencia hay entre pre-fader y post-fader? *Esperado:* pre no depende del fader; post lo sigue. *Fuente:* glosario.
5. ¿Por qué usar un retorno para la reverb? *Esperado:* compartir un efecto entre varias pistas de forma eficiente. *Fuente:* canónico.

## Preguntas literales esperadas (como si existiera transcripción)
6. "En esta lección se nombra el punto final por donde sale toda la mezcla, ¿cuál es?" *Esperado:* el master (bus principal). *Fuente:* momentos.
7. "En esta parte se recomienda un modo de envío para reverbs, ¿cuál?" *Esperado:* post-fader. *Fuente:* momentos/glosario.
8. "En este ejercicio, ¿qué tipo de efecto se coloca en el canal de retorno?" *Esperado:* una reverb (efecto compartido). *Fuente:* actividad.

## Preguntas fuera de dominio
9. "¿Qué ratio de compresión uso en el bus de batería?" *Esperado:* señalar que el ajuste es de la sección de dinámica; aquí solo el ruteo. *Fuente:* límites.
10. "¿Cómo ecualizo una voz para que brille?" *Esperado:* fuera del alcance de 0.4; remitir a EQ.

## Preguntas ambiguas
11. "¿Dónde pongo la reverb?" *Esperado:* pedir si es para una pista o compartida; recomendar retorno vía envío si es compartida. *Fuente:* FAQ 3.
12. "¿Necesito buses?" *Esperado:* depende del número de pistas y del control deseado; con muchas, sí. *Fuente:* FAQ 16.

## Criterios de calificación
Acierta si: explica el flujo universal, distingue serie/paralelo y pre/post, recomienda retorno para efectos compartidos, y traduce a DAWs sin inventar menús. Falla si: confunde insert y envío, enruta todo al master por defecto, o inventa nombres de funciones.
