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
source_type: "glossary"
scope: "section"
source: "canonical_md"
content_type: "markdown"
visible_to_student: true
allowed_for_indexing: false
status: "approved_for_ingestion"
retention_status: "pending_lesson_mapping"
source_origin: "course"
corpus_version: "seccion_0_v1"
ingestion_batch_id: "seccion0_20260704"
original_relative_path: "leccion_0_5_gain_staging/04_glosario.md"
---

# 0.5 — Glosario de la lección

**Gain staging.** *Simple:* dar el nivel correcto en cada paso. *Técnico:* gestión del nivel de la señal a lo largo de todas las etapas de la cadena. *Ejemplo:* bajar pistas calientes al importarlas. *Error común:* verlo como un detalle menor.

**0 dBFS.** *Simple:* el máximo digital. *Técnico:* nivel de plena escala digital; por encima hay recorte. *Ejemplo:* un pico que toca 0 y clippea. *Error común:* mezclar rozando ese techo.

**Clipping (recorte).** *Simple:* distorsión por pasarse del máximo. *Técnico:* deformación de la onda al superar 0 dBFS. *Ejemplo:* aspereza al sumar pistas muy fuertes. *Error común:* confundirlo con saturación deseada.

**Headroom.** *Simple:* el margen hasta el techo. *Técnico:* distancia entre el nivel de la señal y 0 dBFS. *Ejemplo:* dejar picos varios dB por debajo de 0. *Error común:* no dejar margen en el master.

**dBFS.** *Simple:* la escala de nivel digital. *Técnico:* decibelios referidos a plena escala digital. *Ejemplo:* un medio en torno a −18 dBFS. *Error común:* confundirlo con dB SPL (volumen acústico).

**Nivel de pico.** *Simple:* lo más alto que llega la señal. *Técnico:* valor máximo instantáneo de la señal. *Ejemplo:* el pico de un golpe de caja. *Error común:* mirar solo el pico e ignorar el nivel medio.

**Nivel medio (RMS/loudness).** *Simple:* cuán fuerte suena en promedio. *Técnico:* medida de energía promedio, más ligada a la sonoridad percibida. *Ejemplo:* el cuerpo sostenido de un bajo. *Error común:* juzgar el nivel solo por los picos.

**Ganancia de entrada.** *Simple:* cuánta señal le mandas a un plugin. *Técnico:* nivel con que la señal llega a la entrada de un procesador. *Ejemplo:* ajustar un trim antes de una emulación. *Error común:* golpear el plugin demasiado fuerte.

**Ganancia de salida.** *Simple:* cuánto sale del plugin. *Técnico:* nivel con que el procesador entrega la señal a la etapa siguiente. *Ejemplo:* compensar el nivel tras comprimir. *Error común:* acumular ganancia y saturar el bus.

**Trim/Utility de ganancia.** *Simple:* un control simple de volumen previo. *Técnico:* plugin o control que ajusta el nivel sin colorear la señal. *Ejemplo:* bajar 6 dB antes de un plugin. *Error común:* usar el fader del canal para esto y descolocar el balance.

**Suma (summing).** *Simple:* juntar varias señales. *Técnico:* combinación de varias señales en un bus, cuyos niveles se acumulan. *Ejemplo:* ocho pistas de batería en un bus. *Error común:* no prever que la suma sube el nivel.

**Punto flotante.** *Simple:* cómo el DAW maneja niveles internamente. *Técnico:* representación numérica que tolera picos internos altos sin recorte hasta la salida. *Ejemplo:* un bus interno que "supera 0" pero se corrige antes del master. *Error común:* usarlo de excusa para no cuidar el gain staging.
