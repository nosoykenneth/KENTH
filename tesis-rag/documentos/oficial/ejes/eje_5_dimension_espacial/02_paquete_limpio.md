---
axis_id: "Eje 5"
axis_number: 5
axis_title: "Eje 5 - Dimensión espacial"
doc_layer: "limpio"
doc_type: "operacion_practica"
source_origin: "course"
status: "ready_for_indexing"
language: "es"
allowed_for_indexing: true
---

# EJE 5 — DIMENSIÓN ESPACIAL
## Extracción Forense KENTH Academy

---

## 1. COBERTURA DEL EJE

**Fuentes que lo alimentan directamente:**

| Fuente | Contenido relevante para Eje 5 |
|---|---|
| PDF: Ley de Panorama | Fundamento físico del Pan Law, cuatro configuraciones, implicaciones para el bus y para comparación mono/estéreo |
| Clases 7–9 (Mezcla) | Ley de panorama aplicada, elementos primarios/secundarios/terciarios, doubling, monocompatibilidad, convenciones de paneo, criterios de imagen estéreo |
| PDF: Apunte Reverb 2025 V2 | Fenomenología de la reverberación, tipos (plato, resortes, algorítmica, convolución), parámetros, procesamiento previo/posterior, aplicaciones por instrumento |
| Clases 20–21 (Mezcla) | Ambiencia, early reflections, RT60, formación perceptual de la reverb, reflexiones y cálculos de espacio |
| Clases 22–24 (Training) | Doubling, Mid/Side aplicado en mezcla, falseo estéreo, early reflections prácticas, room en batería |
| Clase 28 (Master) | MS manual en mezcla como herramienta quirúrgica de corrección espectral por zona |
| Temario fuente (Módulo XV) | Ambiencia, reverb, delay — lista canónica del eje |

**Partes dislocadas:**

El **Módulo XV** del temario fuente incluye la presentación del plugin **Ambience** (Rabinovich + Panitta) como referencia central de reverb algorítmica. En KENTH ese plugin tiene obligación de atribución pero **no puede ser la referencia estructural del eje**; el eje debe referenciarse con reverbs de documentación independiente.

El **procesamiento MS en mezcla** es nuevo en la arquitectura KENTH (no tenía slot propio en el temario fuente). La cobertura en las fuentes es buena (Clases 22, 28), pero su distinción respecto del MS en mastering (Eje 7) necesita declararse explícitamente al redactar.

El contenido de **delay** (tipos, parámetros, sincronización a tempo) tiene cobertura parcial en las fuentes; el apunte de reverb lo menciona pero no lo desarrolla como capítulo independiente. Las clases de Training lo mencionan como herramienta, pero sin el desarrollo teórico que tienen la reverb y el paneo.

---

## 2. MATRIZ NEUTRA DEL EJE

### BLOQUE A — POSICIONAMIENTO Y ANCHURA

| # | Tema | Subtema | Concepto técnico | Definición neutra | Fórmula / Relación | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|---|
| 5A-01 | Ley de panorama | Fundamento | Problema de la suma de amplificadores | Cuando una señal mono se posiciona al centro en un sistema estéreo, ambos canales la reproducen simultáneamente. Eso duplica la potencia entregada a los monitores, lo que produciría un incremento de 3 dB si no se compensara | Suma acústica al centro: +3 dB. Suma eléctrica (voltajes iguales): +6 dB | La ley de panorama compensa este incremento. La configuración elegida afecta el comportamiento del bus de salida cuando hay compresión | Distintas configuraciones de Pan Law son la principal razón por la que "dos DAWs suenan diferente" con el mismo material. No es el motor del sumador: es el Pan Law | Creer que los DAWs "suenan diferente" por sus motores de suma cuando la diferencia proviene de la configuración de Pan Law | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5A-02 | Ley de panorama | Configuraciones | Cuatro configuraciones estándar | (1) +3 dB en los extremos — la señal sube al moverse del centro a los extremos. (2) –3 dB en el centro — la señal baja al pasar de extremo a centro. (3) –4,5 dB en el centro — punto intermedio entre suma acústica y eléctrica; SSL, Neve, Focusrite. (4) –6 dB en el centro — conserva la amplitud de voltaje constante entre extremos y centro | Pan Law –3 dB: 0 dBFS extremo → +3 dB al centro = 3 dBFS. Pan Law –6 dB: amplitud de voltaje constante en cualquier posición | Elegir el Pan Law antes de empezar la mezcla y no cambiarlo durante el proceso; cambiar el Pan Law después de haber armado la compresión del bus altera el comportamiento dinámico de toda la mezcla | Para comparar estéreo vs mono con fidelidad de planos, usar un Pan Law de –6 dB; esa configuración conserva la amplitud de voltaje constante al colapsar | Cambiar la configuración de Pan Law a mitad de la mezcla porque el nivel del centro "parece bajo" | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5A-03 | Ley de panorama | Aplicación práctica | Pan Law y compresión del bus | La configuración de Pan Law determina el nivel con el que las señales llegan al bus de salida y, por tanto, cómo el compresor del bus reacciona. Una configuración de –2,5 dB se sentirá más comprimida que una de –6 dB si hay compresión en el bus | — | La ley de panorama de la DAW afecta directamente cómo trabaja el compresor de bus; elegir la configuración con criterio antes de encadenar el bus processing | Si el compresor del bus "parece trabajar demasiado", verificar que el Pan Law no esté enviando más nivel del esperado desde el centro de la mezcla | Ajustar el threshold del compresor del bus sin considerar que un cambio de Pan Law alterará toda la decisión | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5A-04 | Posicionamiento | Criterios | Elementos primarios, secundarios y terciarios | Criterio de jerarquía para el posicionamiento estéreo: elementos primarios (voz, bombo, bajo, tambor) → al centro o cerca del centro; relación de fase debe ser la más controlada. Elementos secundarios → más abiertos; pueden operar con cierto desfasaje sin problema. Elementos terciarios (efectos breves, ornamentos) → pueden ir más abiertos aún; toleran mayor desfasaje e incluso inversión de polaridad entre L/R puntual | — | Los graves son omnidireccionales; el cerebro no los localiza con precisión → mantener bombo y bajo al centro por razones de translación y de manejo en mastering | Si al mover el panpot del bombo a la izquierda lo que se localiza a la izquierda es el click (~3 kHz), no el grave: el grave no puede localizarse y se reparte entre ambos canales de todos modos | Panear el bombo o el bajo fuera del centro esperando obtener una imagen espacial más amplia sin perder consistencia en mono | HEURÍSTICA OPERATIVA REFORMULABLE | REFORMULAR MÁS |
| 5A-05 | Posicionamiento | Monocompatibilidad | Coherencia al colapsar a mono | Al colapsar a mono, las diferencias de fase entre señales que antes estaban separadas en el campo estéreo se vuelven sumas o cancelaciones. Pasar a mono no "arregla" los problemas de fase; si la mezcla tenía problemas, el mono los empeora | — | Verificar la mezcla en mono con una configuración de Pan Law de –6 dB para que los planos sean fieles. Si en mono no cambia nada, la mezcla era básicamente mono | El doubling real (dos tomas distintas de lo mismo) en full panning tiene problemas de monocompatibilidad inevitables; el costo artístico de esas diferencias de fase puede ser menor que el beneficio estéreo | Cerrar el panning del doubling hacia el centro pensando que "mejora la monocompatibilidad": solo empeora el problema gradualmente hasta el máximo al llegar al centro | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5A-06 | Posicionamiento | Doubling | Doubling real vs falso estéreo | Doubling real: la misma parte musical se toca (o canta) dos veces y se captura en dos tomas separadas. Al abrirlas en full panning se produce la imagen estéreo. El doubling tiene diferencias naturales entre tomas que producen el carácter. Falso estéreo: una sola toma se divide o se retarda para simular el efecto del doubling. El sample delay (1–30 ms aprox.) entre dos copias de una señal también produce una apertura estéreo pero introduce comb filtering al colapsar a mono | — | El doubling real da más carácter y más riqueza que el falso estéreo. El falso estéreo es más "controlado" pero el comb filtering al colapsar puede ser problemático | El doubling de guitarras en quad tracking genera más reflexiones de fase y potencialmente más problemas de monocompatibilidad. El beneficio artístico (densidad, carácter) puede superar el costo técnico en función del género | Usar falso estéreo esperando que suene igual que un doubling real y sin considerar el comb filtering al colapsar | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5A-07 | Procesamiento MS | Fundamento | Codificación Mid/Side | El procesamiento Mid/Side (M/S) codifica la señal estéreo en dos señales: Mid (suma de L y R, lo que está al centro) y Side (diferencia de L y R, lo que está en los laterales). Permite procesar de forma independiente el contenido central y el lateral | M = (L + R) / 2 · S = (L – R) / 2 · Reconstrucción: L = M + S · R = M – S | En mezcla: usar M/S para procesar de forma quirúrgica un problema que afecta solo al contenido central (como una resonancia del snare que aparece en Mid pero no en Side) | Una resonancia del snare suele estar en Mid; aplicarle EQ en Side no solo no la resuelve sino que modifica el Side innecesariamente | Aplicar el mismo procesamiento espectral a ambos canales L y R cuando el problema está en solo una de las componentes Mid o Side | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5A-08 | Procesamiento MS | Aplicación | MS en mezcla vs MS en mastering | MS en mezcla: opera sobre la imagen de la mezcla en construcción; herramienta quirúrgica para correcciones de elementos que viven en el Mid o el Side de la suma. MS en mastering: opera sobre el programa completo entregado; herramienta de ajuste de imagen estéreo y balance espectral de la señal final | — | La diferencia no es de herramienta sino de contexto: en mezcla el M/S toca elementos específicos; en mastering toca la imagen global entregada | Armar la matriz M/S manualmente en la DAW permite aplicar procesamiento dinámico independiente al Mid y al Side sin necesidad de un plugin dedicado | Aplicar MS de mastering a elementos individuales de la mezcla creyendo que es el mismo proceso | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE B — FENOMENOLOGÍA DE LA REVERBERACIÓN

| # | Tema | Subtema | Concepto técnico | Definición neutra | Relación / Fórmula | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|---|
| 5B-01 | Reverb | Fundamento físico | La reverberación como fenómeno perceptual | La reverberación no es el "estiramiento" del sonido original: es la superposición temporal de cientos de reflexiones decaídas que el cerebro no puede separar individualmente y percibe como campo difuso. Es una construcción perceptual | RT60: tiempo en que la reverb cae 60 dB desde su nivel inicial, a partir del decaimiento medido linealmente | El RT60 depende fundamentalmente del volumen del recinto, los materiales, la absorción y la frecuencia de incidencia | La reverberación se construye cuando las reflexiones llegan más rápido de lo que el cerebro puede procesarlas por separado (~50 ms para sonidos percusivos; hasta 100 ms para sostenidos) | Asumir que el RT60 de la reverb en el plugin refleja el tiempo real que el oyente percibe; la percepción depende también del nivel relativo y el tipo de señal | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5B-02 | Reverb | Secuencia temporal | Sonido directo | La energía que viaja directamente desde la fuente al oyente sin rebotar. Componente principal para la localización de la fuente y el reconocimiento tímbrico original | — | El nivel relativo del sonido directo respecto de la reverb determina si la fuente se percibe cerca o lejos | Sin sonido directo, el oyente pierde la referencia de dónde está la fuente; la reverb sola sin señal seca no localiza | Añadir más reverb creyendo que "más espacio" equivale a "más presencia" cuando en realidad diluye el sonido directo y aleja la fuente | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5B-03 | Reverb | Secuencia temporal | Early Reflections (primeras reflexiones) | Reflexiones de bajo orden (hasta segundo o tercer rebote) que llegan dentro de ~50–80 ms del sonido directo. El cerebro no las percibe como eventos separados sino como ensanchamiento de la fuente. Determinan la percepción del tamaño del recinto, su forma y materiales | Límite perceptual: ~30–50 ms para percusivos; ~50–80 ms para sonidos de ataque suave; hasta 100 ms para señales sostenidas | Las early reflections también introducen comb filtering por interacción con el sonido directo; este filtrado modifica el timbre del instrumento en el espacio | Las early reflections dan información sobre el espacio antes de que el campo reverberante se forme; una reverb sin early reflections puede sonar "de otro mundo" | Confundir el predelay con el tiempo hasta la primera reflexión; el predelay es el tiempo hasta que se forma la masa densa reverberante, no hasta la primera reflexión | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5B-04 | Reverb | Secuencia temporal | Predelay | Tiempo entre el arribo del sonido directo / early reflections y el comienzo del campo reverberante (la "cola" perceptual). Predelay largo → la fuente parece más cercana y el espacio más grande. Predelay corto → la fuente parece más integrada al ambiente, más lejana | — | Usar predelay para separar la voz de su reverb y preservar la inteligibilidad. Reducir el predelay para que un instrumento se "pegue" más al ambiente | El predelay de 40–80 ms en reverb de voces permite que la voz se escuche clara antes de que entre la cola: inteligibilidad sin sacrificar el espacio | No usar predelay y perder la separación entre la señal seca y la reverb, lo que hace que el instrumento suene "dentro del espacio" en lugar de "en el espacio" | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5B-05 | Reverb | Factores acústicos | Densidad y difusión | Densidad: número de reflexiones por unidad de tiempo. Recintos con geometría irregular presentan mayor densidad. Difusión: distribución espacial de las reflexiones. Mayor difusión → campo reverberante más homogéneo y menos colorado | — | Mayor densidad y difusión → reverb más suave y menos "metalizada". Menor densidad → reverb con reflexiones discretas, más audibles como eventos | Para instrumentos que requieren suavidad (voces, cuerdas), preferir alta difusión. Para efectos dramáticos, reducir la difusión para obtener reflexiones más identificables | Subir la difusión de la reverb sin considerar que puede suavizar también la definición del instrumento | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5B-06 | Reverb | Factores acústicos | Timbre de la reverb | El timbre de la reverb depende de la absorción selectiva por frecuencia de los materiales del recinto (vidrio: brillante; madera: cálido; alfombra: oscuro). Los flutter echoes (reflexiones rápidas entre superficies paralelas) producen coloración metálica. El comb filtering por primeras reflexiones también colorea | — | El timbre de la reverb puede modificarse con EQ antes o después del procesador, controlando qué frecuencias excitan la reverb y cómo se percibe la cola resultante | Una reverb con cola brillante puede añadir "sibilancia a la sibilancia"; filtrar antes de la reverb evita que la reverb amplifique problemas ya existentes en el instrumento | Excitar la reverb con la señal completa sin considerar que las frecuencias problemáticas del instrumento también serán procesadas y amplificadas por la cola | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE C — TIPOS DE REVERB

| # | Tipo | Mecanismo | Carácter | Aplicaciones típicas | Advertencia | Categoría | Acción |
|---|---|---|---|---|---|---|---|
| 5C-01 | Reverb de placa (Plate) | Placa de acero bajo tensión excitada por transductor. Pickups captan las vibraciones de la placa. La posición del amortiguador ajusta el tiempo de decay (1–5 s) | Suave, denso, musical. Brillante en el extremo superior. Respuesta muy uniforme sin reflexiones identificables | Batería (snare especialmente), voces con brillo suave. Referencia: EMT 140 | El timbre del hardware original depende de la linealidad del driver y los preamps; los modelados de calidad lo replican incluyendo la coloración | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5C-02 | Reverb de resortes (Spring) | Transductores mecánicos conectados a resortes de acero. Las ondas viajan a velocidades distintas según la frecuencia (dispersión) → timbre metálico y dispersivo | Carácter metálico marcado. Cola no uniforme, con "saltos". Muy no lineal con señales fuertes (clangs). No lineal = musical | Guitarras (clásico de amplificadores), efectos dramáticos. Imposible de imitar fielmente con salas reales | La respuesta no lineal con señales fuertes puede producir artefactos; calibrar el nivel de entrada | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5C-03 | Reverb algorítmica | Modelos matemáticos y redes de retardos que simulan el comportamiento acústico. No reproduce un espacio específico sino que construye uno artificialmente mediante difusión, modulación y retroalimentación | Gran flexibilidad de parámetros. Muy variable según el algoritmo (hall, room, plate, chamber, shimmer). Alta musicalidad en los mejores modelos | Cualquier aplicación; especialmente cuando se necesita más control sobre la estructura de la reverb que el que ofrece una IR | No toda reverb algorítmica suena igual aunque se llame "hall"; el algoritmo específico define el carácter | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5C-04 | Reverb por convolución (IR) | Usa una Respuesta al Impulso (IR) del espacio o hardware: una grabación de cómo ese espacio responde a un impulso de amplio espectro. La convolución matemática combina el audio con la IR | Exactitud: reproduce fielmente el comportamiento acústico del espacio o hardware capturado. Menor flexibilidad que la algorítmica porque la estructura de la reverb está "fija" en la IR | Recintos acústicos reales, emulaciones de hardware clásico, cualquier uso donde la precisión del espacio sea prioritaria | La IR captura el comportamiento en un instante; variaciones del espacio real (temperatura, humedad, personas) no se replican | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE D — PARÁMETROS Y PROCESAMIENTO DE REVERB

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|
| 5D-01 | Parámetros | RT60 | Tiempo de reverberación | Tiempo en que la reverb decae 60 dB. La curva de decaimiento es exponencial; la medición en dB es lineal. El RT60 puede no ser el mismo en todas las frecuencias: los graves suelen tener mayor RT60 que los agudos en recintos reales | RT60 estimado con Sabine: T = 0,161 × V / A (V = volumen del recinto, A = absorción total) | Un RT60 muy largo en graves puede generar acumulación de energía baja que enturbia la mezcla; EQ posterior en la reverb puede controlar eso | Para calcular el cálculo de reflexiones práctico de una sala: 100 Hz = 10 ms de período = 3,43 m de distancia | Usar un RT60 largo porque "suena grande" sin considerar que en mezcla puede destruir la definición de todos los elementos que comparten esa reverb | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5D-02 | Procesamiento | Pre-EQ | Filtrado y EQ previos a la reverb | Colocar HPF y/o EQ antes de la reverb para controlar qué frecuencias excitan el procesador. El pre-EQ modifica la excitación del efecto sin tocar la señal audible directa | — | HPF antes de la reverb: evitar que las frecuencias graves innecesarias generen turbidez en la cola. Reducir medios resonantes: evitar que la cola enfatice zonas problemáticas del instrumento | Filtrar los agudos duros antes de la reverb (guitarras eléctricas, metales, tambores) puede hacer que la cola suene más natural sin modificar el brillo del instrumento seco | Excitar la reverb con la señal sin procesar y luego intentar corregir el resultado con EQ posterior; es más efectivo controlar la excitación desde el inicio | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5D-03 | Procesamiento | Post-EQ | EQ posterior a la reverb | EQ aplicado después de la reverb que moldea la cola reverberante ya generada, sin modificar cómo se genera | — | Roll-off de agudos en la cola: simula distancia o carácter vintage. Boost de medios-altos: presencia en reverbs vocales modernas. Corte de graves: controla acumulación de densidad en salas amplias | Una reverb más "oscura" (con roll-off de agudos) ubica perceptualmente el instrumento más atrás en el campo de profundidad | Cortar agudos en la reverb y simultáneamente en el instrumento directo; el post-EQ afecta solo la cola, no el instrumento seco | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5D-04 | Procesamiento | Compresión de reverb | Control de dinámica de la cola | Aplicar compresión después de la reverb para controlar las variaciones dinámicas de la cola. Puede usarse para pegamento (cola más nivelada), pumping (sidechain desde la señal seca), o aumento de densidad (reverbs muy espaciales que se necesitan más presentes) | — | Sidechain desde la señal seca: la reverb se "abre" entre frases sin tapar la fuente. Esto es especialmente útil en voces donde la inteligibilidad es crítica | La reverb gated (compuerta después de la reverb) produce el sonido icónico de los años 80; la compresión con pumping crea espacialidad rítmica muy útil en batería | Comprimir la reverb directamente sin considerar que afecta también las early reflections si el ataque es demasiado rápido | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5D-05 | Procesamiento | Delay + reverb | Combinaciones creativas | El delay puede colocarse antes de la reverb (refuerza la separación entre señal directa y cola, mejora inteligibilidad), después de la reverb (genera colas más complejas), o combinarse como alternativa a un predelay extenso. La combinación delay + reverb es clásica en voces modernas | — | Delay antes de la reverb en voces: mayor claridad que el solo predelay porque el delay puede tener su propio carácter tímbrico. Slapback hacia la reverb: muy usado en voces y cajas en mezclas vintage | Un delay de ~80 ms antes de la reverb puede hacer que la voz "flote" sobre el espacio sin perderse en él | Usar solo reverb cuando la combinación delay + reverb resolvería mejor el problema de inteligibilidad + espacio | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5D-06 | Procesamiento | Saturación de reverb | Saturación antes y después | Saturación suave aplicada a la reverb: (a) antes de la reverb, para imitar el comportamiento del hardware analógico; (b) después, para aportar densidad a la cola y controlar transitorios. La saturación puede también preceder a la excitación del procesador para evitar que picos fuertes produzcan artefactos en la cola | — | Una saturación suave antes de la reverb puede "suavizar" el ataque de la señal que excita el procesador, produciendo una cola más uniforme y menos dura | Saturar antes de la reverb para instrumentos percusivos reduce la probabilidad de que los picos de transiente generen "colas duras" en el inicio de la reverb | Aplicar saturación después de la reverb esperando el mismo efecto que antes; la saturación posterior colorea la cola ya generada, no la excitación | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE E — PROFUNDIDAD, DELAY Y PSICOACÚSTICA ESPACIAL

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|
| 5E-01 | Profundidad | Factores perceptuales | Construcción de la profundidad | La profundidad percibida depende de: (1) nivel relativo del sonido directo respecto a la reverb, (2) tiempo de llegada de las early reflections, (3) contenido de alta frecuencia (los agudos se atenúan con la distancia en el aire), (4) relación señal directa / campo reverberante | Ley de distancia: al duplicar la distancia, el sonido directo cae 6 dB | Para alejar un instrumento: reducir el nivel directo, aumentar la proporción de reverb, filtrar los agudos. Para acercarlo: aumentar el nivel directo, reducir la reverb, preservar los agudos | Un instrumento con LPF sutil en el canal directo ya suena "más atrás" aunque su nivel no cambie: los agudos son la primera señal de distancia que el cerebro procesa | Usar solo el nivel del fader para gestionar la profundidad sin considerar que el LPF y la reverb tienen mayor impacto perceptual en la sensación de distancia | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5E-02 | Profundidad | Efecto de precedencia | Ley de precedencia (Haas) | La ley de Haas establece que cuando dos sonidos idénticos llegan con una diferencia temporal de 1–35 ms, el cerebro los integra como uno solo y localiza la fuente en la dirección del primero que llega. Esto puede usarse para posicionar instrumentos sin cambiar su paneo | — | Aplicar un delay corto (1–20 ms) a la copia de una señal paneada al lado opuesto hace que el cerebro localice el sonido hacia la señal más temprana, creando sensación de ancho sin desfasaje problemático | El efecto Haas genera apertura estéreo sin las consecuencias de monocompatibilidad del doubling; pero a partir de ~20 ms puede percibirse como eco | Confundir el efecto Haas (integración perceptual por precedencia) con el doubling real, que depende de diferencias de interpretación entre tomas | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5E-03 | Delay | Parámetros básicos | Delay como herramienta espacial | El delay es un retardo de la señal que puede usarse como herramienta espacial (posicionamiento, profundidad, ensanchamiento), expresiva (tiempo musicalizado al tempo) o ambiental (slapback, early reflections simuladas). Parámetros: tiempo de delay, número de repeticiones (feedback), nivel de la señal retardada, y en algunos modelos EQ del delay | — | Sincronizar el delay al tempo de la canción para que las repeticiones queden en el pulso y contribuyan a la musicalidad en lugar de "tapar" el contenido | Un delay de cuarto de nota con feedback moderado en una guitarra puede crear un efecto de cola musical que aporta espacialidad sin la dificultad de ajustar una reverb compleja | Usar el delay sin sincronizar al tempo y obtener repeticiones que compiten rítmicamente con el instrumento principal | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 5E-04 | Psicoacústica | Localización | Mecanismo de localización auditiva | El cerebro determina la posición de una fuente usando: (1) diferencias de nivel entre ambos oídos (ILD), (2) diferencias de tiempo entre ambos oídos (ITD), (3) sombra acústica de la cabeza (HRTF en el plano frontal y vertical). Las frecuencias graves son difíciles de localizar porque su longitud de onda es grande respecto al diámetro de la cabeza | — | El panning actúa sobre la ILD: cambia el nivel entre L y R. Las diferencias de tiempo (sample delay) actúan sobre la ITD | Por debajo de ~200 Hz el cerebro pierde capacidad de localización basada en diferencias de nivel; lo que se percibe como "bombo a la izquierda" es en realidad el contenido de medios y agudos del bombo | Panear frecuencias muy graves esperando obtener localización cuando el cerebro no puede procesar la diferencia de nivel a esas frecuencias | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

## 3. CONTENIDO ATRIBUIBLE DEL EJE

| Bloque | Atribución requerida | Obligación específica |
|---|---|---|
| **Plugin Ambience** (reverb algorítmica) | Autoría: Pablo Panitta y Pablo Rabinovich. Herramienta desarrollada por los autores fuente, presentada en el Módulo XV del temario fuente | **OBLIGACIÓN ARQUITECTURAL**: si KENTH menciona Ambience como herramienta de referencia, requiere atribución doble (Panitta / Rabinovich). **RESTRICCIÓN ESTRUCTURAL**: Ambience no puede ser la referencia central del Eje 5 ni el único ejemplo de reverb algorítmica. El eje debe referenciarse con reverbs de documentación independiente |
| PDF: Ley de Panorama | Autoría: Pablo Rabinovich. La doctrina técnica del Pan Law es de dominio general; la formulación del apunte no debe copiarse | Reformular; la doctrina técnica es reutilizable |
| PDF: Apunte Reverb 2025 V2 | Autoría: Pablo Rabinovich. La fenomenología y los tipos de reverb son dominio técnico general; la formulación específica del apunte y las listas de modelos recomendados son del autor fuente | Reformular; los criterios técnicos son reutilizables; las recomendaciones específicas de plugins requieren verificación independiente |
| Criterio de elementos primarios/secundarios/terciarios para el posicionamiento | Formulación del autor fuente con ese naming específico. La lógica subyacente (jerarquía de paneo) es de dominio general del campo | REFORMULAR sin reproducir el naming específico si se usa como doctrina general; USAR CON ATRIBUCIÓN si se usa el sistema con ese nombre |

---

## 4. BLOQUEOS DEL EJE

| Bloque bloqueado | Tipo de riesgo | Por qué no debe pasar |
|---|---|---|
| Plugin Ambience como referencia central del eje | MÉTODO ATRIBUIBLE — RESTRICCIÓN ESTRUCTURAL | Centrar el eje en una herramienta del autor fuente crea dependencia estructural identificable |
| Anécdotas de referencia: The Eagles, Metallica, Enigma, Pink Floyd, Draco Rosa como ejemplos de análisis de imagen estéreo | EXPRESIÓN NO REUTILIZABLE | Ejemplos de análisis específicos del docente situados en sus clases; identificables con su curso |
| Formulaciones orales: "una locomotora que te pasa por arriba" (Metallica), "la canción de los noventa que se ganó un Grammy" | EXPRESIÓN NO REUTILIZABLE | Frases y referencias situadas en el contexto de clase del autor fuente |
| Secuencia pedagógica del temario fuente: Módulo XV en ese orden (ambiencia → reverb → delay con Ambience como pivote) | ESTRUCTURA NO REUTILIZABLE | Orden de exposición reconocible del curso fuente |
| Referencia a la presentación de Ambience en clase como evento pedagógico del autor fuente | EXPRESIÓN NO REUTILIZABLE | Situado en la biografía del autor fuente |
| La "guía de usos de reverb por instrumento" tal como está formulada en el apunte | EXPRESIÓN NO REUTILIZABLE / ESTRUCTURA NO REUTILIZABLE | La formulación específica y la estructura de la guía pertenecen al apunte del autor fuente; la reformulación completa es posible pero no copiando la organización ni las frases |

---

## 5. VACÍOS Y TENSIONES DEL EJE

| Tipo | Descripción | Implicación para redacción |
|---|---|---|
| **Vacío mayor** | El **delay** como herramienta tiene cobertura parcial. El apunte de reverb lo menciona en relación a la reverb, pero no tiene un capítulo propio que cubra tipos (tape delay, analog, digital, multitap), parámetros completos ni sincronización a tempo de forma sistemática. Las transcripciones lo mencionan como herramienta pero sin desarrollo teórico propio | Al redactar: construir el contenido de delay desde fuentes externas o reducirlo a criterios operativos básicos bien fundamentados |
| **Vacío** | La **modulación estéreo** (chorus, ensemble, vibratos estéreos) como herramienta de construcción de imagen está listada en la arquitectura pero casi no tiene desarrollo en las fuentes. Solo se menciona el Roland Dimension en contexto de training | Construir desde fuentes externas o reducir a una entrada breve en la matriz |
| **Vacío relativo** | La **psicoacústica espacial aplicada** (localización, envolvimiento, efecto de precedencia) tiene cobertura conceptual pero poca aplicación práctica en las fuentes del proyecto más allá del análisis del paneo | Al redactar: la doctrina está disponible; los casos de uso prácticos deberán construirse editorialmente |
| **Tensión crítica de atribución** | El plugin **Ambience** es la herramienta de reverb algorítmica presentada en el temario fuente como pivot del módulo XV. Si KENTH lo usa, atribución obligatoria. Si no lo usa (por la restricción estructural), necesita substituirlo con al menos dos o tres reverbs algorítmicas de documentación independiente | **Decisión editorial obligatoria**: definir antes de redactar qué reverbs algorítmicas de referencia usará KENTH como ejemplos principales; la lista del apunte de reverb (Valhalla, FabFilter Pro-R 2, etc.) puede servir como punto de partida |
| **Tensión de límite** | El MS en mezcla (Eje 5) y el MS en mastering (Eje 7) usan exactamente la misma herramienta y la misma mecánica de codificación/decodificación. La diferencia es el contexto de uso (imagen en construcción vs programa final). En las fuentes, las clases de mastering desarrollan el MS de forma más extensa que las de mezcla | Al redactar Eje 5: declarar explícitamente el límite; introducir la mecánica M/S y su uso en corrección quirúrgica de mezcla; remitir al Eje 7 para el MS sobre el programa completo |
| **Tensión de cruce con Eje 1** | El goniómetro y el correlatómetro (herramientas de lectura de Eje 1) son las herramientas de diagnóstico del campo espacial y de imagen estéreo. El Eje 5 opera sobre esa lectura | Declarar el cruce: el posicionamiento y la imagen del Eje 5 se monitorizan con los instrumentos de Eje 1 |
| **Tensión de cruce con Eje 2** | El comb filtering producido por el doubling o el falso estéreo puede diagnosticarse en Eje 1 y corregirse (alineación temporal) en Eje 2. En Eje 5, el doubling y el falso estéreo se usan creativamente. La frontera puede difuminarse | Al redactar: en Eje 5, el comb filtering del doubling se aborda como costo técnico de la herramienta creativa; la corrección del comb filtering no deseado pertenece a Eje 2 |
| **Tensión de profundidad variable** | El apunte de reverb 2025 tiene un nivel de detalle técnico muy alto (física del resorte, del plate, convolución) que supera el nivel de profundidad de las demás fuentes del eje. Al redactar habrá que compensar ese desbalance y no replicar la profundidad del apunte como si fuera el nivel estándar del eje | Al redactar: usar el nivel de profundidad apropiado para el propósito pedagógico de KENTH; no convertir el eje en un manual exhaustivo de acústica y reverb |

---

## 6. PAQUETE LIMPIO DEL EJE

### EJE 5 — DIMENSIÓN ESPACIAL · Paquete limpio para proyecto generativo

---

**FUNCIÓN DEL EJE:** Construir la imagen tridimensional de la mezcla: anchura, profundidad y altura percibida. Sin dimensión espacial la mezcla es plana. El espacio se construye sobre señales que ya tienen carácter tonal y energía gestionada.

**ADVERTENCIA ANTES DE REDACTAR:** Definir qué reverbs algorítmicas de referencia usará KENTH (dado que Ambience no puede ser referencia central).

---

#### BLOQUE A — POSICIONAMIENTO Y ANCHURA

**Doctrina reutilizable:**
- Ley de Panorama: al posicionar una señal mono al centro se alimentan ambos monitores simultáneamente → incremento de potencia acústica de 3 dB. Los fabricantes compensan de distintas formas. Cuatro configuraciones: +3 dB en extremos, –3 dB en centro, –4,5 dB en centro (SSL/Neve), –6 dB en centro (conserva amplitud de voltaje constante)
- El Pan Law elegido debe fijarse al inicio y no modificarse durante la mezcla. Cambiarlo con compresión en el bus ya establecida altera el comportamiento dinámico de toda la mezcla
- La configuración de Pan Law es la principal causa de que "dos DAWs suenen diferente" con el mismo material; no es el motor de suma
- Para comparar estéreo vs mono con fidelidad de planos, usar Pan Law de –6 dB
- Graves: omnidireccionales; el cerebro no los localiza con precisión por debajo de ~200 Hz. Mantener bombo y bajo al centro por razones de translación y mastering
- Elementos en el campo estéreo por jerarquía perceptual: los más críticos (lo que el oyente "escucha primero") deben tener la relación de fase más controlada. Los elementos secundarios y terciarios toleran mayor desfasaje
- Doubling real: dos tomas distintas de lo mismo. Abiertas en full panning producen imagen estéreo con comb filtering al colapsar a mono. El costo técnico puede ser menor que el beneficio artístico según el género
- Falso estéreo (sample delay): produce apertura con comb filtering predecible. ~1–20 ms → efecto Haas (integración perceptual); >20 ms → eco perceptible
- Procesamiento M/S en mezcla: codifica L/R en Mid (suma) y Side (diferencia). Permite procesamiento quirúrgico sobre el contenido central o lateral de forma independiente. Diferente del MS en mastering (que opera sobre el programa completo entregado)

**Heurísticas reformulables:**
- Si en mono no cambia nada, la mezcla era básicamente mono desde el origen
- Una resonancia de snare que aparece en Mid no tiene por qué tratarse también en Side; el M/S evita el procesamiento innecesario del lado incorrecto
- Monocompatibilidad del doubling: cerrar el panning hacia el centro no mejora el problema; lo empeora gradualmente hasta el máximo al llegar a mono

**Atribuciones:**
- PDF Ley de Panorama: Rabinovich (reformular formulación)
- Criterio de naming "primarios/secundarios/terciarios": Rabinovich si se usa el sistema con ese nombre específico

**Advertencias:**
- CRUCE → EJE 1: goniómetro y correlatómetro (Eje 1) monitorean la imagen del Eje 5
- CRUCE → EJE 2: el comb filtering del doubling no deseado se corrige en Eje 2; en Eje 5 se gestiona como costo técnico de la herramienta creativa
- LÍMITE Eje 5 / Eje 7: el MS en mezcla opera sobre la imagen en construcción; el MS en mastering opera sobre el programa completo entregado

---

#### BLOQUE B — REVERBERACIÓN

**Doctrina reutilizable:**

La reverberación es la superposición de cientos de reflexiones que el cerebro no puede separar individualmente. No es el "estiramiento" del sonido; es una construcción perceptual.

**Secuencia temporal (dominio general del campo):**
- Sonido directo: llega primero; localiza la fuente; define el timbre de referencia
- Early reflections: 0–80 ms según el tipo de sonido; no se perciben como eventos separados; determinan la percepción del tamaño del recinto
- Predelay: tiempo entre el sonido directo y la masa densa reverberante. Largo → fuente más cercana, espacio más grande. Corto → fuente más integrada al ambiente
- Campo reverberante: masa densa de reflexiones indiferenciables; el "tail" perceptual

**Factores del RT60:** volumen del recinto, materiales, absorción, frecuencia. Los graves suelen tener mayor RT60 que los agudos.

**Tipos:**
- Placa (plate): suave, densa, musical. Batería y voces
- Resortes (spring): metálica, dispersiva, no lineal con señales fuertes. Guitarras y efectos creativos
- Algorítmica: máxima flexibilidad de parámetros; construye espacios artificiales. Cualquier aplicación
- Convolución (IR): reproduce un espacio real o hardware específico con gran exactitud; menor flexibilidad estructural

**Procesamiento de la reverb:**
- Pre-EQ/filtrado: controla qué frecuencias excitan el procesador. HPF evita turbidez en la cola; recorte de medios problemáticos evita que la reverb amplifique esos problemas
- Post-EQ: moldea la cola ya generada. Roll-off de agudos → aleja la fuente perceptualmente y simula distancia o carácter vintage
- Compresión de reverb: sidechain desde la señal seca para que la reverb se abra entre frases; pumping rítmico; nivelación de la cola
- Delay + reverb: combinaciones que permiten mayor inteligibilidad que el predelay solo; slapback antes de la reverb para voces y cajas
- Saturación: antes de la reverb → suaviza el ataque de excitación; después → colorea la cola

**Atribuciones:**
- PDF Apunte Reverb 2025: Rabinovich (reformular formulación; la doctrina técnica de reverb es de dominio general)
- Plugin Ambience: USAR CON ATRIBUCIÓN DOBLE si se menciona (Panitta / Rabinovich); NO como referencia central del eje

**Advertencias:**
- RESTRICCIÓN ESTRUCTURAL: definir reverbs de referencia con documentación independiente del autor fuente antes de redactar
- VACÍO: delay como herramienta independiente tiene cobertura insuficiente en las fuentes; construir desde doctrina general o fuentes externas

---

#### BLOQUE C — PROFUNDIDAD Y PSICOACÚSTICA ESPACIAL

**Doctrina reutilizable:**
- La profundidad percibida depende de: nivel relativo directo/reverb, tiempo de las early reflections, contenido de alta frecuencia (los agudos se atenúan con la distancia en el aire), densidad del campo reverberante
- Para alejar un instrumento: reducir nivel directo + aumentar reverb + LPF sutil en la señal directa. El LPF tiene mayor impacto perceptual en la sensación de distancia que el nivel solo
- Efecto de precedencia (ley de Haas): con diferencias de tiempo de 1–35 ms entre dos señales idénticas, el cerebro las integra y localiza la fuente en la dirección del sonido más temprano. Aplicación: sample delay a una copia paneada al lado opuesto crea anchura estéreo sin el comb filtering del doubling clásico
- Localización de graves: por debajo de ~200 Hz, el cerebro pierde capacidad de localización por diferencias de nivel. Lo que se percibe como "bombo a la izquierda" es el contenido de medios y agudos del bombo, no el grave

**Heurísticas reformulables:**
- Sincronizar el delay al tempo; las repeticiones en el pulso musical contribuyen a la musicalidad
- Delay de 40–80 ms antes de la reverb en voces: mayor claridad que el predelay solo porque el delay tiene su propio carácter tímbrico

**Atribuciones:**
- Efecto de precedencia / ley de Haas: Helmut Haas (dominio público científico)

**Advertencias:**
- VACÍO: delay como herramienta con desarrollo sistemático propio (tipos, parámetros, sincronización a tempo) necesita construcción desde fuentes externas o doctrina general del campo
- VACÍO: modulación estéreo (chorus, ensemble) tiene cobertura mínima en las fuentes

---

*Paquete listo para ingesta en Proyecto Generativo. Siguiente eje cuando lo indiques.*