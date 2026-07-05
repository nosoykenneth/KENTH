---
course_id: "2"
moodle_section_id: "2"
section_id: "2"
section_number: "1"
section_slug: "el_sistema_de_decision"
section_title: "SECCIÓN 0: El sistema de decisión"
lesson_id: "SEC2-R59"
lesson_number: "0.5"
lesson_title: "Gain Staging: el cimiento de toda la cadena"
source_type: "activity"
scope: "lesson"
source: "canonical_md"
content_type: "markdown"
visible_to_student: true
allowed_for_indexing: true
status: "approved_for_ingestion"
source_origin: "course"
corpus_version: "seccion_0_v1"
ingestion_batch_id: "seccion0_20260704"
original_relative_path: "leccion_0_5_gain_staging/06_actividad_practica.md"
---

# 0.5 — Actividad práctica: gain staging de una sesión

## Objetivo
Ajustar el nivel de una sesión etapa por etapa para que ninguna sature y el master conserve headroom.

## Materiales necesarios
Un DAW, un proyecto con varias pistas (mejor si vienen calientes) y los medidores de nivel del DAW.

## Preparación
Abre el proyecto y observa los medidores de cada pista, de los buses y del master. Identifica dónde se acerca la señal a 0.

## Pasos
1. Revisa cada pista: si sus picos están muy cerca de 0, baja su nivel (con un trim/utility) hasta dejar margen.
2. Comprueba los buses: si alguno se acerca a 0 por la suma, baja las pistas que lo alimentan o el bus.
3. Inserta un plugin en una pista y ajusta su ganancia de entrada para que trabaje en su zona (que no distorsione sin querer).
4. Verifica el master: deja los picos por debajo de 0 con margen.
5. Comprueba con el oído que no hay aspereza de clipping y que el balance no cambió respecto al inicio.

## Qué debe entregar el estudiante
Una nota con los niveles antes y después en pistas problemáticas, buses y master, y una explicación de qué ajustó y por qué. Opcionalmente capturas de los medidores.

## Criterios de revisión
Se valora que ninguna etapa sature, que se use trim en vez de descolocar faders, que el master tenga headroom y que el balance se mantenga.

## Errores frecuentes
Bajar solo el master y dejar los buses saturando. Usar el fader para el gain staging y descolocar el balance. Obsesionarse con clavar −18. Poner un limitador para tapar clipping.

## Versión básica
Trabaja solo pista y master: baja las pistas calientes y deja headroom en el master.

## Versión avanzada
Añade el ajuste de entrada de una emulación analógica, documentando cómo cambia su comportamiento con más o menos señal de entrada, y revisa pico vs. nivel medio.

## Adaptación si solo tienes auriculares
Perfecto: el gain staging es cuestión de medidores y niveles, no de sistema. Mantén volumen moderado y confía en los medidores además del oído.

## Adaptación si usas FL Studio
Usa Fruity Balance o el control de "Input gain" de las pistas del Mixer como trim, vigila los medidores de cada pista del Mixer y del Master, y recuerda que el punto flotante interno tolera picos, pero cuida el Master.

## Adaptación si usas otro DAW
En Ableton usa Utility como trim; en Reaper, el control de volumen de item/trim o un JS gain; en Logic/Cubase, el Gain plugin. Vigila los medidores de pista, grupo y master en todos.
