---
course_id: "2"
moodle_section_id: "2"
section_id: "2"
section_number: "1"
section_slug: "el_sistema_de_decision"
section_title: "SECCIÓN 0: El sistema de decisión"
lesson_id: "SEC2-R58"
lesson_number: "0.4"
lesson_title: "Anatomía universal del mixer: ruteo"
source_type: "canonical"
scope: "lesson"
source: "canonical_md"
content_type: "markdown"
visible_to_student: true
allowed_for_indexing: true
status: "approved_for_ingestion"
source_origin: "course"
corpus_version: "seccion_0_v1"
ingestion_batch_id: "seccion0_20260704"
original_relative_path: "leccion_0_4_anatomia_universal_mixer_ruteo/01_contenido_canonico.md"
---

# 0.4 — Anatomía universal del mixer: ruteo

## Objetivo de aprendizaje
Comprender el camino que recorre la señal dentro de cualquier mezclador —canal, bus, envío, retorno y master— para poder organizar una sesión y aplicar procesos en el punto correcto, sin importar el DAW.

## Idea central
Todos los mixers, sean de hardware o de software, comparten la misma anatomía básica. Si entiendes por dónde viaja la señal, puedes trabajar en cualquier DAW: cambian los nombres y los botones, no la lógica. El ruteo es el mapa; dominarlo es dejar de estar perdido dentro de la sesión.

## Explicación principal
La señal empieza en un **canal** (o pista de mezcla): ahí llega el audio de un instrumento o voz. Cada canal tiene, en orden, sus **inserts** (procesos en serie como EQ o compresión, que afectan a toda la señal que pasa), sus **envíos** (sends, que mandan una copia de la señal a otro destino), un **paneo** (posición en el estéreo) y un **fader** (nivel de salida del canal). La señal del canal se dirige a un destino de salida.

Ese destino suele ser un **bus** (o grupo): un canal que recibe la suma de varias pistas para tratarlas juntas. Por ejemplo, enrutar todas las pistas de batería a un bus "Batería" permite comprimir o ecualizar el conjunto con un solo proceso y controlar su nivel con un solo fader. Los buses pueden a su vez enrutarse a otros buses, formando una jerarquía.

Los **envíos** y **retornos** sirven para efectos compartidos, típicamente reverberación y delay. Un envío manda una porción de la señal del canal a un **canal de retorno** (o FX/aux) donde vive el efecto. Así, varias pistas comparten la misma reverb y se mezcla el resultado con un fader de retorno. La gran distinción es serie vs. paralelo: un insert procesa toda la señal en serie; un envío crea una rama en paralelo con una copia de la señal.

Dentro de los envíos hay dos modos: **pre-fader** (la señal enviada no depende del fader del canal) y **post-fader** (la señal enviada sigue al fader del canal). Post-fader es lo habitual para reverbs, porque si bajas la pista, baja también su reverb de forma natural. Pre-fader se usa para casos especiales como mezclas de monitoreo o efectos independientes del nivel del canal.

Al final, todo confluye en el **master** (o bus principal, main/stereo out): el canal por el que sale toda la mezcla hacia tus altavoces y hacia el archivo final. Lo que pongas en los inserts del master afecta a la mezcla completa, por lo que se maneja con especial cuidado.

Organizar bien este ruteo tiene beneficios directos: procesas grupos con eficiencia, controlas secciones enteras con un fader, compartes efectos sin duplicarlos y mantienes la sesión ordenada y entendible. Un ruteo caótico, en cambio, hace que cada decisión cueste más y que los problemas sean difíciles de rastrear.

## Conceptos clave
El **canal** es la puerta de entrada de cada fuente. Los **inserts** procesan en serie. Los **envíos/retornos** crean ramas en paralelo para efectos compartidos. El **bus** agrupa varias pistas. El **master** es la salida final. La distinción **serie vs. paralelo** y **pre/post-fader** define dónde y cómo actúa cada proceso.

## Procedimiento recomendado
Antes de mezclar, define tu ruteo: agrupa por familias (batería, voces, instrumentos) en buses. Crea uno o dos retornos para efectos compartidos (una reverb, un delay). Decide qué procesos van en insert (los que afectan a toda la señal de una pista) y cuáles en envío (los que se comparten). Comprueba que todo llega al master. Nombra y colorea las pistas y buses para orientarte.

## Criterios de decisión
Usa un insert cuando el proceso debe afectar íntegramente a una pista (EQ correctivo, compresión de esa voz). Usa un envío cuando varias pistas comparten un efecto o quieres mezclar señal seca y procesada (reverb, delay, compresión paralela). Agrupa en un bus cuando quieras tratar o controlar varias pistas como una unidad. Reserva el master para decisiones globales y mínimas.

## Errores comunes
Poner una reverb como insert en cada pista en vez de compartirla por envío. Confundir envío con salida y perder la señal. Enrutar todo directo al master sin buses, complicando el control. Usar pre-fader sin querer y que la reverb no siga al fader. Duplicar procesos que podrían vivir en un bus. No nombrar nada y perderse.

## Ejemplo aplicado
Una batería de ocho pistas suena descontrolada. Sin ruteo, el alumno intenta comprimir cada pista por separado, con resultados dispares. Con ruteo: enruta las ocho pistas a un bus "Batería", aplica una compresión suave de bus para pegarlas y controla toda la batería con un fader. Además, crea un retorno de reverb y manda por envío una porción de la caja y los toms, compartiendo el mismo espacio. Menos procesos, más control.

## Qué debe evitar el estudiante
Evita duplicar efectos que deberían compartirse por envío. Evita mezclar sin buses cuando hay muchas pistas. Evita tocar el master con procesos pesados antes de tener la mezcla equilibrada. Evita dejar la sesión sin nombres ni colores.

## Resumen final
La anatomía del mixer es universal: canal → inserts/envíos → bus → retornos → master. Los inserts procesan en serie; los envíos crean ramas en paralelo para efectos compartidos; los buses agrupan; el master es la salida final. Entender este mapa te deja trabajar en cualquier DAW y convierte una sesión caótica en una ordenada y controlable.

## Relación con otras lecciones de la sección
Esta lección da el vocabulario de señal que la 0.5 necesita: el gain staging se aplica a lo largo de este camino (canal, bus, master). Se apoya en el método de la 0.1 (cada decisión de ruteo también se diagnostica y verifica) y prepara el checklist de la 0.7, donde organizar el ruteo es un paso de arranque.
