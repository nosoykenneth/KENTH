---
course_id: "2"
moodle_section_id: "2"
section_id: "2"
section_number: "1"
section_slug: "el_sistema_de_decision"
section_title: "SECCIÓN 0: El sistema de decisión"
lesson_id: ""
lesson_number: "0.5"
lesson_title: "Gain Staging: el cimiento de toda la cadena"
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
original_relative_path: "leccion_0_5_gain_staging/10_prompt_evaluacion.md"
---

# 0.5 — Prompt de evaluación (no indexable)

Uso interno. Contiene respuestas esperadas; no indexar.

## Preguntas conceptuales
1. ¿Qué es el gain staging y por qué es el cimiento? *Esperado:* nivel adecuado en cada etapa; hace que todo lo demás funcione. *Fuente:* canónico.
2. ¿Qué es el headroom y por qué importa? *Esperado:* margen hasta 0 dBFS; evita clipping y deja espacio a masterización. *Fuente:* glosario.
3. ¿Por qué un bus puede saturar aunque las pistas estén bien? *Esperado:* la suma acumula nivel. *Fuente:* canónico.
4. ¿Por qué las emulaciones dependen del nivel de entrada? *Esperado:* están calibradas para una zona; demasiada señal distorsiona. *Fuente:* canónico.
5. Diferencia entre nivel de señal y volumen de escucha. *Esperado:* uno lo miden los medidores; el otro es el volumen del monitor. *Fuente:* canónico.

## Preguntas literales esperadas (como si existiera transcripción)
6. "En esta lección se menciona un valor de referencia para los niveles medios, ¿cuál?" *Esperado:* alrededor de −18 a −12 dBFS, como guía. *Fuente:* momentos.
7. "En esta parte se dice qué hacer si una emulación distorsiona sin querer, ¿qué?" *Esperado:* bajar el nivel de entrada. *Fuente:* momentos.
8. "En este ejercicio, ¿qué debe conservar el master?" *Esperado:* headroom (margen hasta 0). *Fuente:* actividad.

## Preguntas fuera de dominio
9. "¿A cuántos LUFS masterizo para streaming?" *Esperado:* señalar que es loudness de masterización, distinto del gain staging; remitir a esa sección.
10. "¿Qué micrófono da más nivel al grabar?" *Esperado:* fuera del alcance; es grabación.

## Preguntas ambiguas
11. "Mi mezcla distorsiona, ¿qué hago?" *Esperado:* pedir en qué etapa satura (pista, bus, master) y bajar el nivel ahí. *Fuente:* guía del tutor.
12. "¿Debo dejar todo a −18?" *Esperado:* aclarar que es guía, no ley; el objetivo es margen y no saturar. *Fuente:* FAQ 3.

## Criterios de calificación
Acierta si: explica headroom y etapas, trata −18 como guía, corrige saturación bajando nivel (no con limitador), distingue nivel de volumen de escucha y no confunde gain staging con loudness. Falla si: dogmatiza un número, tapa clipping con limitador o mezcla conceptos de masterización.
