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
source_type: "canonical"
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
original_relative_path: "leccion_0_5_gain_staging/01_contenido_canonico.md"
---

# 0.5 — Gain Staging: el cimiento de toda la cadena

## Objetivo de aprendizaje
Aprender a gestionar el nivel de la señal en cada etapa de la cadena de mezcla, dejando margen suficiente (headroom), para que cada procesador reciba una señal sana y la mezcla no sature ni pierda calidad.

## Idea central
El gain staging es asegurar que en cada punto del camino la señal tenga un nivel adecuado: ni tan alto que sature, ni tan bajo que se pierda. Es un trabajo poco glamuroso, pero es el cimiento sobre el que se apoyan la EQ, la compresión y todo lo demás. Con un buen gain staging, los plugins se comportan como esperas; con uno malo, todo suena peor y no sabes por qué.

## Explicación principal
En el dominio digital, el techo absoluto es 0 dBFS. Pasar de ahí produce recorte (clipping) digital, una distorsión desagradable. Por eso trabajamos por debajo de ese techo, dejando **headroom**: un margen de seguridad. Una práctica común y sensata es apuntar a niveles medios en torno a −18 dBFS a −12 dBFS en las pistas, dejando picos bien por debajo de 0. Estos valores no son mágicos ni obligatorios: son una zona cómoda heredada de la relación entre el mundo analógico y el digital, donde muchos procesadores fueron pensados para operar. Lo importante no es clavar un número, sino no acercarse peligrosamente a 0 en cada etapa.

El gain staging ocurre en varias etapas encadenadas: la señal entra a la pista, pasa por cada insert (que puede subir o bajar el nivel), llega al fader del canal, se suma en los buses y finalmente al master. Un error frecuente es que la suma de muchas pistas fuertes en un bus haga que el bus sature aunque cada pista suene bien por separado. Otro es que un plugin con mucha ganancia de salida golpee demasiado fuerte al siguiente. Por eso se cuida el nivel de entrada y salida de cada procesador.

Hay una razón técnica importante: muchos plugins, sobre todo las emulaciones analógicas, están calibrados para "sonar bien" a un nivel de entrada concreto. Si les mandas una señal demasiado caliente, distorsionan o comprimen de más; si es muy débil, apenas reaccionan. Ajustar el nivel de entrada para que el plugin trabaje en su zona óptima es parte del gain staging, no un detalle menor.

También conviene distinguir el nivel de la señal (lo que miden los medidores del DAW) del volumen de escucha (lo fuerte que suena en tus altavoces). Son cosas distintas: puedes tener una pista a −18 dBFS y escucharla fuerte o bajo según el volumen del monitor. El gain staging se refiere al nivel de la señal, no al volumen de escucha, que se gestionó en la lección de percepción.

Un buen flujo es: importa el material sin normalizar a tope, ajusta el nivel de cada pista para que sus picos queden con margen, verifica que los buses no saturan, y deja el master con headroom suficiente para que la etapa de masterización tenga dónde trabajar. Si en algún punto ves que te acercas a 0 o que un plugin distorsiona sin querer, baja el nivel de entrada antes de tocar otra cosa.

## Conceptos clave
**0 dBFS** es el techo digital; pasarlo produce clipping. El **headroom** es el margen que dejas hasta ese techo. El **nivel medio** (RMS/loudness) y el **pico** son medidas distintas que hay que vigilar. La **ganancia de entrada/salida** de cada plugin importa para que trabaje en su zona. El **gain staging** se aplica en todas las etapas: pista, insert, bus, master.

## Procedimiento recomendado
Importa las pistas y baja su nivel si vienen muy calientes, apuntando a picos con margen (por ejemplo, medios alrededor de −18 a −12 dBFS como guía). Antes de cada plugin, revisa que la entrada no esté saturando; ajusta con un control de ganancia previa si hace falta. Comprueba los buses: si un bus se acerca a 0, baja las pistas que lo alimentan o el propio bus. Deja el master con headroom (sin llegar a 0). Verifica con los medidores del DAW y con el oído.

## Criterios de decisión
Si algo satura, baja el nivel antes de añadir más procesos. Prefiere ajustar la ganancia de entrada del plugin a subir todo y luego bajar el master. Si una emulación distorsiona sin que lo busques, probablemente le llega demasiada señal: bájala. No persigas un número exacto; persigue margen y una señal que no sature en ninguna etapa. Deja siempre headroom en el master para la fase posterior.

## Errores comunes
Importar pistas al máximo y mezclar pegado a 0. Subir la ganancia de salida de cada plugin acumulando nivel hasta saturar el bus. Confundir el nivel de la señal con el volumen de escucha. Golpear las emulaciones con señal demasiado caliente. No dejar headroom en el master. Creer que "más fuerte" en cada etapa es "mejor".

## Ejemplo aplicado
Un alumno importa stems muy calientes; cada pista pica cerca de 0. Al sumarlas en el master, la mezcla clippea y suena áspera. En vez de poner un limitador para tapar el problema, baja el nivel de todas las pistas para que los picos queden con margen; el clipping desaparece, los compresores empiezan a comportarse de forma predecible y la mezcla suena más limpia. No cambió el balance, cambió el gain staging.

## Qué debe evitar el estudiante
Evita mezclar con las pistas y el master pegados a 0. Evita subir la salida de cada plugin sin control. Evita compensar un mal gain staging con un limitador al final. Evita confundir el medidor de nivel con el volumen de tus altavoces. Evita obsesionarte con clavar −18 exacto: es una guía, no una ley.

## Resumen final
El gain staging es dar a la señal el nivel correcto en cada etapa, dejando headroom hasta 0 dBFS. No es perseguir un número mágico, sino evitar la saturación y hacer que cada procesador trabaje en su zona. Es el cimiento silencioso que hace que EQ, compresión y emulaciones se comporten como deben. Con buen gain staging, todo lo demás es más fácil.

## Relación con otras lecciones de la sección
Esta lección aplica el vocabulario de ruteo de la 0.4 (pista, bus, master) a la gestión de nivel. Se apoya en la 0.2 al distinguir nivel de señal de volumen de escucha. Y es clave para la 0.6, porque las emulaciones analógicas dependen especialmente de recibir el nivel adecuado. En el checklist de la 0.7, verificar el gain staging es un paso de arranque.
