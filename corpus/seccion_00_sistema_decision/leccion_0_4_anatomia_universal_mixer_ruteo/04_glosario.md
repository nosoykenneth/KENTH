---
course_title: "Mezcla y Masterización"
section_number: 0
section_title: "El sistema de decisión"
lesson_number: "0.4"
lesson_title: "Anatomía universal del mixer: ruteo"
source_type: "glossary"
recommended_scope: "lesson"
visible_to_student: true
allowed_for_indexing: true
status: "approved_for_ingestion"
---

# 0.4 — Glosario de la lección

**Canal (pista de mezcla).** *Simple:* donde llega el audio de una fuente. *Técnico:* ruta que recibe una señal y la procesa antes de enviarla a un destino. *Ejemplo:* el canal de la voz principal. *Error común:* confundir pista de audio con canal de mezcla en algunos DAWs.

**Insert.** *Simple:* un efecto puesto en línea en la pista. *Técnico:* procesador en serie que afecta a toda la señal que pasa por el canal. *Ejemplo:* un EQ correctivo en la voz. *Error común:* usarlo para efectos que deberían compartirse.

**Envío (send).** *Simple:* mandar una copia de la señal a otro sitio. *Técnico:* derivación en paralelo que envía parte de la señal a un retorno o bus. *Ejemplo:* mandar la caja a una reverb. *Error común:* confundirlo con la salida del canal.

**Retorno (return/aux/FX).** *Simple:* el canal donde vive un efecto compartido. *Técnico:* canal que recibe envíos, aloja un efecto y devuelve la señal a la mezcla. *Ejemplo:* un retorno con una reverb de sala. *Error común:* poner en él procesos que deberían ir en insert.

**Bus (grupo).** *Simple:* un canal que junta varias pistas. *Técnico:* canal que suma varias señales para procesarlas y controlarlas juntas. *Ejemplo:* un bus de batería. *Error común:* no usarlo y enrutar todo al master.

**Master (bus principal).** *Simple:* la salida final de la mezcla. *Técnico:* bus por el que pasa toda la mezcla hacia la reproducción y el archivo final. *Ejemplo:* el stereo out del proyecto. *Error común:* sobrecargarlo de procesos pronto.

**Serie.** *Simple:* uno tras otro, todo pasa por ahí. *Técnico:* procesamiento donde la señal atraviesa el efecto por completo. *Ejemplo:* EQ en insert. *Error común:* usar serie cuando se busca mezclar seco y procesado.

**Paralelo.** *Simple:* una copia aparte que luego se suma. *Técnico:* rama que procesa una copia de la señal y la mezcla con la original. *Ejemplo:* reverb por envío. *Error común:* no aprovecharlo para compartir efectos.

**Pre-fader.** *Simple:* el envío no depende del fader del canal. *Técnico:* toma de señal antes del fader; su nivel es independiente del fader. *Ejemplo:* una mezcla de monitoreo. *Error común:* usarlo por error en reverbs.

**Post-fader.** *Simple:* el envío sigue al fader del canal. *Técnico:* toma de señal después del fader; sube y baja con él. *Ejemplo:* reverb que sigue el nivel de la pista. *Error común:* no darse cuenta de que la reverb no baja al bajar el canal (por estar en pre).

**Paneo.** *Simple:* la posición izquierda-derecha del sonido. *Técnico:* control de la distribución de una señal entre los canales estéreo. *Ejemplo:* guitarras a los lados. *Error común:* paneos extremos que se caen en mono.

**Fader.** *Simple:* el control de volumen del canal. *Técnico:* control de nivel de salida de un canal o bus. *Ejemplo:* subir la voz 1 dB. *Error común:* usarlo como única herramienta de balance ignorando el ruteo.

**Sub-bus.** *Simple:* un bus dentro de otro bus. *Técnico:* agrupación intermedia que se enruta a otro bus superior. *Ejemplo:* bus de toms dentro del bus de batería. *Error común:* crear jerarquías innecesariamente complejas.
