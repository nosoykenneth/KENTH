---
axis_id: "Eje 5"
axis_number: 5
axis_title: "Eje 5 - Dimensión espacial"
doc_layer: "canonico"
doc_type: "teoria_principal"
source_origin: "course"
status: "ready_for_indexing"
language: "es"
allowed_for_indexing: true
---

# EJE 5 — DIMENSIÓN ESPACIAL
### KENTH Academy · Mezcla y Masterización · Contenido Final de Curso

---

## SECCIÓN 1 — FUNCIÓN PRÁCTICA DEL EJE

El Eje 5 construye la imagen tridimensional de la mezcla: dónde está cada elemento en el campo estéreo, a qué distancia percibida se escucha, y qué sensación de entorno rodea a cada fuente.

El Eje 3 definió el carácter tonal. El Eje 4 controló la energía y el movimiento. El Eje 5 trabaja la posición de cada elemento en el espacio. Una mezcla sin dimensión espacial construida es plana: los elementos están presentes pero no ocupan lugares distintos, no tienen distancias relativas, no crean profundidad.

El eje tiene tres dominios:

**Posicionamiento y anchura:** dónde se coloca cada elemento en el campo estéreo, con qué criterio, qué implica la ley de panorama para el comportamiento del bus, y qué herramientas —doubling, falso estéreo, procesamiento Mid/Side— permiten construir anchura con criterio técnico y artístico.

**Reverberación:** la herramienta principal para crear entorno y profundidad. Tipos de reverb, sus diferencias de carácter, y cómo procesar la reverb —antes, durante y después del procesador— para que contribuya a la imagen en lugar de embarrarla.

**Profundidad y delay:** cómo funciona la percepción de distancia, qué factores la determinan, y cómo el delay opera como herramienta espacial y musical.

**Límites del eje:**
- El goniómetro y el correlatómetro (Eje 1) son los instrumentos de diagnóstico de la imagen que el Eje 5 construye.
- El comb filtering no deseado del doubling se corrige en Eje 2. En el Eje 5, el comb filtering del doubling se gestiona como costo técnico de una herramienta creativa.
- El procesamiento Mid/Side en mezcla opera sobre la imagen en construcción. El MS sobre el programa completo entregado pertenece al Eje 7.

---

## SECCIÓN 2 — QUÉ DEBE PODER HACER EL ALUMNO AL TERMINAR ESTE EJE

Al completar el Eje 5, el alumno es capaz de:

- Identificar la configuración de Pan Law de su DAW y entender qué implica para el nivel del bus y para el compresor del bus.
- Elegir la configuración de Pan Law antes de comenzar la mezcla y mantenerla durante el proceso.
- Posicionar los elementos de la mezcla con criterio de jerarquía espacial, manteniendo los elementos de mayor peso al centro.
- Aplicar doubling real y entender sus consecuencias de monocompatibilidad.
- Usar falso estéreo (sample delay) con conciencia del rango perceptual del efecto Haas.
- Verificar la monocompatibilidad de las decisiones de posicionamiento.
- Configurar la matriz Mid/Side en la DAW y aplicar procesamiento quirúrgico diferenciado sobre la señal central y la lateral.
- Describir la secuencia temporal de la reverberación: sonido directo, early reflections, predelay y campo reverberante.
- Distinguir el carácter de los cuatro tipos principales de reverb (placa, resortes, algorítmica, convolución) y elegir según el objetivo.
- Configurar una reverb con predelay, RT60 y relación wet/dry según el instrumento y el resultado buscado.
- Aplicar EQ antes y después de la reverb para controlar la excitación y moldear la cola.
- Usar compresión con sidechain de la señal seca para que la reverb se abra entre frases.
- Construir profundidad percibida manipulando nivel relativo, contenido de alta frecuencia y relación directo/reverb.
- Sincronizar un delay al tempo del material y ajustar su feedback y nivel para que contribuya espacialmente.

---

## SECCIÓN 3 — SUBSECCIONES FINALES DEL EJE

El orden sigue la construcción del espacio de adentro hacia afuera: primero la posición horizontal (posicionamiento y anchura), luego el entorno (reverberación), luego la profundidad y el movimiento temporal (delay). Dentro del bloque de reverb, la fenomenología precede a los tipos y los tipos preceden al procesamiento.

**BLOQUE A — POSICIONAMIENTO Y ANCHURA**

- **5-A1** · Ley de panorama: la física del centro y las cuatro configuraciones
- **5-A2** · Posicionamiento en el campo estéreo: jerarquía y criterios
- **5-A3** · Doubling, falso estéreo y monocompatibilidad
- **5-A4** · Procesamiento Mid/Side en mezcla

**BLOQUE B — REVERBERACIÓN**

- **5-B1** · Fenomenología: cómo el cerebro construye el espacio
- **5-B2** · Tipos de reverb: placa, resortes, algorítmica y convolución
- **5-B3** · Parámetros y procesamiento de la reverb

**BLOQUE C — PROFUNDIDAD Y DELAY**

- **5-C1** · Profundidad percibida: los factores que alejan o acercan
- **5-C2** · Delay: herramienta espacial y musical

---

## SECCIÓN 4 — CURSO PRINCIPAL DEL EJE

---

### 5-A1 · LEY DE PANORAMA: LA FÍSICA DEL CENTRO Y LAS CUATRO CONFIGURACIONES

**Situación real**
El alumno nota que en su DAW, al poner una señal mono en el centro de la mezcla, el bus suena más lleno que cuando la misma señal está paneada a los extremos. También nota que al comparar su mezcla con la de un colega que usa otra DAW, los niveles del centro suenan diferentes aunque ambos tengan los panpots al centro. La causa es la ley de panorama.

**Explicación operativa**
Cuando una señal mono se posiciona al centro de un sistema estéreo, ambos monitores la reproducen simultáneamente a la misma amplitud. Eso duplica la potencia entregada al sistema respecto a tener la señal solo en un lado. El resultado físico es un incremento de 3 dB (suma acústica) o de hasta 6 dB (suma eléctrica de voltajes en fase).

Los fabricantes de DAWs y consolas compensan ese incremento de distintas formas, dando lugar a cuatro configuraciones estándar. Ninguna es "correcta" en términos absolutos: cada una tiene consecuencias diferentes para cómo suena el centro de la mezcla y para cómo trabaja el compresor del bus.

**Las cuatro configuraciones**

*+3 dB en los extremos:* la señal aumenta 3 dB al moverse del centro a los extremos. Las señales en los extremos son más fuertes que las del centro a igual posición de fader.

*–3 dB en el centro:* la señal baja 3 dB cuando se mueve de los extremos al centro. El estándar más habitual en entornos digitales.

*–4,5 dB en el centro:* punto intermedio entre la suma acústica (+3 dB) y la eléctrica (+6 dB). Es la configuración histórica de varias consolas analógicas (SSL, Neve, Focusrite). Produce un comportamiento de centro que se siente más parecido al analógico.

*–6 dB en el centro:* conserva la amplitud de voltaje constante independientemente de la posición del panpot. Una señal mono al centro tiene exactamente la mitad de amplitud de voltaje en cada canal que una señal en un extremo. Esta configuración es la más adecuada para comparar estéreo con mono con fidelidad de planos.

**Por qué importa para la compresión del bus**
La configuración de Pan Law determina el nivel con el que las señales llegan al bus de salida. Una mezcla armada con Pan Law de –2,5 dB enviará más energía al bus en el centro que la misma mezcla con Pan Law de –6 dB. Si hay compresión en el bus, el compresor reaccionará de forma diferente. Cambiar el Pan Law después de haber establecido la compresión del bus equivale a cambiar el gain staging de toda la mezcla.

**Acción**
1. Antes de comenzar la mezcla: verificar la configuración de Pan Law de la DAW.
2. Elegir la configuración con criterio (–4,5 dB para comportamiento analógico; –6 dB para máxima fidelidad en comparaciones mono/estéreo).
3. No cambiar la configuración durante el proceso de mezcla.
4. Si se compara con otra DAW o con una referencia que puede tener un Pan Law diferente: tener en cuenta que las diferencias de nivel en el centro no son diferencias de mezcla sino de configuración.

**Verificación**
Panear una señal de prueba del extremo izquierdo al centro y al extremo derecho mientras se observa el nivel en el bus. Con Pan Law de –3 dB: el nivel en los extremos debe ser 3 dB mayor que en el centro. Con Pan Law de –6 dB: el nivel debe ser constante en cualquier posición. Con Pan Law de –4,5 dB: el nivel en los extremos es 4,5 dB mayor que en el centro.

**Error frecuente**
Interpretar que "dos DAWs suenan diferente" por sus motores de suma cuando la diferencia proviene de la configuración de Pan Law. El motor de suma de una DAW correctamente implementada es matemáticamente transparente; lo que produce diferencias de carácter entre DAWs en el centro de la imagen es la compensación de Pan Law, no la suma.

---

### 5-A2 · POSICIONAMIENTO EN EL CAMPO ESTÉREO: JERARQUÍA Y CRITERIOS

**Situación real**
El alumno mezcla una canción con batería, bajo, guitarras, teclados y voz. Panea todo al centro porque "quiere que suene sólido". La mezcla suena mono y aplastada. Al intentar abrir la imagen paneando todo, el bajo y el bombo desaparecen al colapsar a mono. No tiene criterio para decidir qué va dónde.

**Explicación operativa**
El posicionamiento estéreo no es arbitrario ni estético solamente: tiene una lógica técnica y perceptual que determina la translación de la mezcla a distintos sistemas y la legibilidad de cada elemento.

**Jerarquía de posicionamiento**
Los elementos con mayor peso en la producción y mayor densidad de contenido de baja frecuencia deben posicionarse al centro o muy cerca de él. Los graves son omnidireccionales: por debajo de aproximadamente 200 Hz, el cerebro pierde la capacidad de localizar sonidos por diferencias de nivel entre oídos. Lo que se percibe como "bombo a la izquierda" cuando se panea el bombo es el contenido de medios y agudos del golpe, no el grave. El grave sigue siendo omnidireccional y se distribuye hacia ambos altavoces independientemente del paneo.

Consecuencias prácticas:
- Bombo y bajo al centro siempre, no solo por monocompatibilidad sino porque el paneo del bajo no produce localización real del grave.
- La voz principal al centro: es la fuente de mayor atención del oyente.
- Los elementos secundarios (guitarras de acompañamiento, teclados de fondo) pueden abrirse hacia los lados con más libertad.
- Los elementos de mayor transitoriedad o menor peso (efectos breves, ornamentos, contra-melodías) pueden posicionarse más extremos.

**Criterios para abrir la imagen**
La apertura estéreo de la mezcla no depende de panear todos los elementos a los extremos. Depende del contraste entre los elementos del centro y los de los lados. Una mezcla con el bombo, el bajo y la voz al centro y las guitarras completamente a los lados puede sonar muy ancha. La misma mezcla con todo al 30% de apertura puede sonar estrecha aunque nada esté en el centro.

Verificación de monocompatibilidad: reproducir la mezcla en mono usando Pan Law de –6 dB. Los elementos que están al centro deben preservar su nivel y carácter. Los elementos que están paneados a los lados con diferencias de fase entre canales (doubling, efectos estéreo) pueden perder nivel o carácter al colapsar, lo cual es esperable y gestionable. Si elementos críticos como la voz o el bombo pierden nivel o timbre al colapsar a mono, hay un problema de relación de fase en esos canales, no un problema de paneo.

**Acción**
1. Posicionar bombo, bajo y voz principal al centro antes de abrir la imagen.
2. Abrir los elementos secundarios de forma gradual, escuchando el resultado en mono periódicamente.
3. No usar el paneo para dar carácter o presencia a un elemento que no la tiene: el paneo posiciona, no compensa problemas tonales o dinámicos.
4. Verificar la imagen con el goniómetro y el correlatómetro (Eje 1) mientras se construye.

**Verificación**
Colapsar la mezcla a mono y escuchar si los elementos críticos conservan su presencia y definición. Verificar con el goniómetro que la imagen es un óvalo vertical equilibrado. Si el goniómetro muestra inclinación hacia un lado, hay desbalance de paneo; si muestra un óvalo horizontal, hay problemas de correlación.

**Error frecuente**
Panear el bombo fuera del centro esperando que produzca una imagen más amplia o una sensación espacial más interesante. El grave del bombo no puede localizarse, por lo que el paneo no aporta lo que se busca; en mono, el bombo pierde nivel por los problemas de fase que introduce el paneo en material de amplia banda.

---

### 5-A3 · DOUBLING, FALSO ESTÉREO Y MONOCOMPATIBILIDAD

**Situación real**
El alumno quiere que las guitarras de la canción suenen anchas y densas. Considera dos opciones: grabar la misma parte dos veces y panear ambas tomas a los extremos, o copiar la misma toma y retardar ligeramente la copia. Ambas producen anchura estéreo, pero tienen consecuencias técnicas muy diferentes.

**Explicación operativa**

**Doubling real**
Dos tomas distintas de la misma parte musical, grabadas en momentos diferentes. Diferencias naturales de afinación, timing y timbre entre las dos tomas son parte de lo que produce el carácter. Al panear las dos tomas a los extremos (full panning), se crea una imagen estéreo amplia.

La consecuencia inevitable: las diferencias entre las dos tomas producen comb filtering cuando la mezcla se colapsa a mono. No es un defecto: es la consecuencia física de sumar dos señales con diferencias de fase entre ellas. El grado del comb filtering depende de cuán similares son las tomas. En producciones donde el doubling de guitarras es central al carácter del género (rock, metal), ese costo técnico de monocompatibilidad es habitualmente menor que el beneficio artístico de la densidad y el carácter del doubling real.

**Falso estéreo (sample delay)**
Una única toma se usa en dos canales: uno va sin modificar y el otro se retarda una pequeña cantidad de milisegundos (1–30 ms aproximadamente). El retardo produce una diferencia temporal entre los dos canales que el cerebro interpreta como anchura estéreo.

La relación perceptual entre el tiempo de retardo y el efecto:
- 1–35 ms: el cerebro integra ambas señales como una sola fuente y la localiza en la dirección del sonido más temprano (ley de precedencia o efecto Haas). El resultado es apertura estéreo sin percepción de eco.
- Por encima de ~20–35 ms: el segundo sonido comienza a percibirse como eco o evento separado.

El comb filtering al colapsar a mono es predecible con el falso estéreo: la primera cancelación ocurre en f = 1/(2×Δt), y las siguientes en los múltiplos impares. Con 5 ms de retardo, la primera cancelación está en 100 Hz. Ese patrón puede ser un problema técnico o puede usarse como herramienta creativa, dependiendo del contexto.

**Monocompatibilidad del doubling**
Cuando se intenta "mejorar" la monocompatibilidad del doubling cerrando el panning de las dos tomas hacia el centro, el resultado es el opuesto al buscado: las dos tomas se suman cada vez más directamente, y el comb filtering se hace más severo precisamente cuando llegan al centro con el paneo completamente cerrado. La monocompatibilidad del doubling no mejora cerrando el paneo: empeora.

Si la monocompatibilidad del doubling es un problema real en la mezcla, las opciones son: reducir el nivel de una de las dos tomas para que la cancelación sea parcial (menor nivel = menor comb filtering), o aceptar el costo como parte del carácter del material.

**Acción**
- Para doubling real: panear las dos tomas a los extremos, verificar en mono, aceptar o gestionar el costo de monocompatibilidad.
- Para falso estéreo: usar un sample delay entre 5 y 20 ms en la copia del canal opuesto. Verificar el resultado en mono con el analizador para identificar la primera cancelación y evaluar si afecta una zona crítica del instrumento.
- No cerrar el paneo del doubling para "arreglar" la monocompatibilidad: empeora el problema.

**Verificación**
Reproducir el instrumento en doubling o falso estéreo en mono. Si la cancelación afecta una zona frecuencial crítica del instrumento (por ejemplo, la presencia de una guitarra a 3 kHz), evaluar si el beneficio estéreo justifica el costo. Si el instrumento pierde su identidad en mono, el doubling puede no ser la herramienta adecuada para ese instrumento en ese contexto.

**Error frecuente**
Usar falso estéreo (sample delay) esperando el mismo resultado que un doubling real. El falso estéreo produce apertura estéreo pero sin las diferencias de timbre, afinación y timing que dan carácter al doubling real. El resultado puede sonar más "controlado" pero también más artificial. Para géneros donde el carácter del doubling real es central, el falso estéreo es un sustituto funcional pero no equivalente.

---

### 5-A4 · PROCESAMIENTO MID/SIDE EN MEZCLA

**Situación real**
El alumno tiene una resonancia en el snare que aparece claramente en la suma mono de la mezcla pero no en los extremos estéreo. Sabe que esa resonancia está principalmente en el contenido central de la imagen. Si aplica EQ en los canales L y R por igual, procesará tanto el contenido del centro como el de los lados, aunque el problema esté solo en el Mid. Necesita operar sobre el Mid sin tocar el Side.

**Explicación operativa**
El procesamiento Mid/Side codifica la señal estéreo convencional (L y R) en dos señales distintas:

- **Mid:** la suma de L y R. Contiene todo lo que está al centro de la imagen: la voz, el bombo, el bajo, cualquier elemento paneado al centro.
- **Side:** la diferencia de L y R. Contiene todo lo que está en los laterales: los elementos paneados, las diferencias de fase entre canales, el "espacio" de la imagen estéreo.

La decodificación es el proceso inverso: M + S reconstruye el canal L; M – S reconstruye el canal R.

En la mezcla, el procesamiento M/S permite intervenir quirúrgicamente sobre el contenido central o lateral de forma independiente. Si hay una resonancia que aparece en Mid (porque el snare está paneado al centro), procesarla solo en Mid evita modificar el contenido del Side. Si hay exceso de brillo en los laterales (por ejemplo, los overheads o los efectos estéreo), reducirlo solo en el Side sin afectar el brillo del contenido central.

**MS en mezcla vs MS en mastering**
El procesamiento M/S en mezcla opera sobre la imagen en construcción: sus decisiones afectan elementos específicos que viven en el Mid o el Side de la suma en ese momento. El procesamiento M/S en mastering opera sobre el programa completo ya entregado: sus decisiones afectan toda la información que quedó codificada en la imagen estéreo final.

La herramienta es la misma. El contexto es diferente, y con él el criterio de intervención. El M/S de mastering se desarrolla en el Eje 7.

**Configuración de la matriz M/S en la DAW**
La matriz M/S puede armarse manualmente con dos canales auxiliares y un par de ganancias diferenciadas (+6 dB y –6 dB o +3 dB y –3 dB según el diseño), o con un plugin dedicado que realiza la codificación y decodificación. La mayoría de los EQs modernos incluyen la opción de procesar en M/S directamente.

**Acción**
1. Si hay un problema espectral que parece estar principalmente en el contenido central de la imagen (lo que se escucha al colapsar a mono): usar M/S y aplicar el procesamiento solo en Mid.
2. Si hay un problema en los laterales (brillo excesivo de los efectos estéreo, imagen demasiado amplia en una zona de frecuencias): procesar solo en Side.
3. Comparar el resultado con bypass verificando que la corrección afecta exactamente la zona que se pretende sin modificar la otra.

**Verificación**
Después de procesar en Mid: colapsar a mono y verificar que el problema corregido ya no está. Reproducir en estéreo y verificar que el Side no fue afectado. Si el procesamiento en Mid modifica también la imagen lateral (lo que puede ocurrir si hay contenido correlado entre Mid y Side), revisar el criterio de intervención.

**Error frecuente**
Aplicar el mismo procesamiento espectral a ambos canales L y R cuando el problema está solo en el Mid. El resultado es que el Side también se modifica aunque no tenga el problema, y la imagen estéreo puede cambiar de forma indeseada. El M/S evita ese efecto secundario cuando el problema es localizable en una de las dos componentes.

---

### 5-B1 · FENOMENOLOGÍA: CÓMO EL CEREBRO CONSTRUYE EL ESPACIO

**Situación real**
El alumno inserta una reverb en la voz y sube el wet al máximo. La voz "desaparece en el espacio" y pierde presencia. Baja el wet y la reverb casi no se escucha. No entiende por qué la reverb no produce el resultado que busca y no sabe qué parámetros ajustar.

**Explicación operativa**
La reverberación no es el "estiramiento" del sonido original: es la suma perceptual de cientos de reflexiones que el cerebro no puede separar individualmente. Cuando las reflexiones llegan lo suficientemente rápido y densas, el cerebro las integra en un campo difuso y las percibe como entorno, no como ecos. La reverberación es una construcción perceptual que el procesador imita.

Para usar la reverb con criterio, hay que entender la secuencia temporal de cómo el cerebro construye el espacio a partir de la señal acústica.

**Sonido directo**
La energía que viaja directamente desde la fuente al oyente. Es la primera información en llegar. Define dónde está la fuente, de qué dirección viene, y cuál es su timbre de referencia. Sin sonido directo, el oyente pierde la referencia de posición y timbre: la reverb sola no localiza.

**Early reflections (primeras reflexiones)**
Las reflexiones de bajo orden (primer y segundo rebote en las superficies del recinto) que llegan en los primeros 50–80 ms después del sonido directo (el umbral exacto varía según el tipo de señal). El cerebro no las percibe como eventos separados sino como ensanchamiento de la fuente. Son las reflexiones que informan sobre el tamaño y la forma del recinto antes de que se forme el campo reverberante denso.

Las early reflections también interactúan con el sonido directo, produciendo comb filtering que modifica el timbre del instrumento en el espacio. Esta coloración es parte de lo que hace que un espacio suene "real".

**Predelay**
El tiempo entre el final de las early reflections y el inicio del campo reverberante denso. No es el tiempo hasta la primera reflexión (que es inmediata): es el tiempo hasta que la masa densa de reflexiones indiferenciables se forma. Un predelay largo hace que la fuente suene más cercana y el espacio más grande, porque hay un silencio relativo entre el instrumento y la "nube" de reverb. Un predelay corto integra la señal directa con el campo reverberante rápidamente, haciendo que el instrumento suene más dentro del espacio.

**Campo reverberante**
La masa densa de reflexiones que el cerebro no puede separar individualmente. Es el "tail" perceptual. Su tiempo de decaimiento —el RT60— define cuánto dura el espacio percibido. El RT60 depende del volumen del recinto, los materiales, la absorción y la frecuencia: en recintos reales, los graves suelen tener mayor RT60 que los agudos porque se absorben menos.

**Acción**
Antes de ajustar cualquier parámetro de una reverb: identificar qué parte de la secuencia temporal necesita trabajo. ¿El instrumento está muy dentro del espacio y necesita más separación con el sonido directo? → ajustar el predelay. ¿El espacio se percibe demasiado pequeño? → las early reflections necesitan más tiempo o la sala más volumen. ¿La cola es demasiado larga? → reducir el RT60.

**Verificación**
Con la reverb activa y el wet apropiado: reproducir el material e identificar si la fuente tiene una posición clara en el espacio (sonido directo audible) antes de que entre la reverb (predelay correcto) y si la cola decae de forma natural al final de las notas (RT60 adecuado para el material).

**Error frecuente**
Confundir el predelay con el tiempo hasta la primera reflexión. El predelay en el plugin es el tiempo hasta que se forma la masa densa reverberante, no hasta la primera reflexión discreta. La primera reflexión en un espacio real puede estar a 5–10 ms; el predelay de un plugin puede ser 40–80 ms. Son dos eventos diferentes en la secuencia temporal de la reverberación.

---

### 5-B2 · TIPOS DE REVERB: PLACA, RESORTES, ALGORÍTMICA Y CONVOLUCIÓN

**Situación real**
El alumno tiene acceso a varios tipos de reverb y no sabe cuál usar para la batería, cuál para la voz y cuál para "un espacio realista de sala". Todos producen reverberación, pero con caracteres radicalmente diferentes.

**Explicación operativa**
Los cuatro tipos principales de reverb difieren en su mecanismo de generación, lo que produce caracteres acústicos específicos que no son intercambiables.

**Reverb de placa (Plate)**
Originalmente hardware: una placa de acero bajo tensión excitada por un transductor, con pickups que captan las vibraciones. El amortiguador ajusta el tiempo de decay. El carácter resultante es suave, denso y uniforme: sin reflexiones discretas identificables, con un comienzo muy rápido del campo reverberante. El extremo superior tiene un brillo específico de la placa.

Uso en mezcla: batería (especialmente caja), voces que necesitan brillo suave y presencia sin reflexiones espaciales obvias. La EMT 140 es la referencia histórica. Sus modelados digitales y los plugins de convolución con IRs de placas reales son las herramientas actuales equivalentes.

**Reverb de resortes (Spring)**
Mecanismo mecánico: transductores conectados a resortes de acero por los que las ondas viajan a velocidades distintas según la frecuencia (dispersión). El resultado es un carácter metálico y dispersivo con una cola no uniforme. A señales fuertes, los resortes responden de forma no lineal con artefactos de "clang" que son parte de su carácter. Es la reverb de los amplificadores de guitarra clásicos.

Uso en mezcla: guitarras (especialmente en géneros donde ese carácter es parte del sonido), efectos creativos donde se quiere un timbre inusual y no natural. No es adecuada para reproducir espacios reales: su dispersión la hace inconfundiblemente mecánica.

**Reverb algorítmica**
Modelos matemáticos que simulan el comportamiento acústico mediante redes de retardos, difusores y retroalimentación. No reproduce un espacio específico sino que construye uno artificialmente con máxima flexibilidad de parámetros: tamaño del recinto, forma, materiales, densidad de early reflections, difusión, modulación. Las mejores algorítmicas actuales —como Valhalla Room, Valhalla VintageVerb, FabFilter Pro-R 2— ofrecen múltiples algoritmos dentro del mismo plugin (room, hall, plate, chamber, shimmer).

Uso en mezcla: cualquier aplicación donde se necesite control preciso sobre la estructura del espacio y el carácter. Es la herramienta más versátil porque sus parámetros pueden ajustarse libremente.

**Reverb por convolución (IR)**
Usa una Respuesta al Impulso (IR): una grabación de cómo un espacio real o un hardware específico responde a un impulso de amplio espectro. La convolución matemática combina el audio con la IR, reproduciendo fielmente el comportamiento acústico del espacio capturado.

Su ventaja es la exactitud: un IR de una sala de conciertos específica reproduce el comportamiento de esa sala. Su limitación es la menor flexibilidad: la estructura de la reverb está fija en la IR y solo puede modificarse mediante EQ y otras herramientas después del procesamiento.

Uso en mezcla: cuando la precisión de un espacio real o de un hardware específico es prioritaria (orquesta, acústica de instrumento específico, emulación de hardware clásico con IRs de calidad).

**Acción**
- Batería (caja) o voz con brillo suave: reverb de plata.
- Guitarras con carácter retro o efectos creativos: spring.
- Cualquier espacio artificial con control preciso de parámetros: algorítmica.
- Reproducción de un espacio real específico: convolución con IR de calidad.

**Verificación**
Después de elegir el tipo y configurar los parámetros básicos: comparar el resultado con la referencia del género. Si el espacio suena incoherente con el estilo del material (por ejemplo, una sala de conciertos orquestal en un tema de rock moderno), reconsiderar el tipo de reverb antes de ajustar parámetros.

**Error frecuente**
Elegir la reverb por el nombre del preset ("Large Hall", "Warm Room") sin verificar que el carácter del tipo de reverb es coherente con el instrumento y el objetivo. Un "Large Hall" de spring reverb y un "Large Hall" de algorítmica suenan completamente diferentes aunque el nombre del preset sea idéntico.

---

### 5-B3 · PARÁMETROS Y PROCESAMIENTO DE LA REVERB

**Situación real**
El alumno tiene una reverb en una voz que suena turbia: los graves de la cola se acumulan y la voz pierde claridad. También nota que la cola de la reverb amplifica la sibilancia de la voz. Intenta compensarlo bajando el wet pero la reverb se vuelve inaudible antes de que los problemas desaparezcan. Los problemas no están en la cantidad de reverb: están en qué frecuencias está excitando la reverb.

**Explicación operativa**
La reverb no actúa sobre el resultado final del instrumento de forma aislada: procesa la señal que recibe y devuelve una cola basada en esa señal. Si la señal que excita la reverb tiene graves innecesarios, la cola los amplificará. Si tiene sibilancias, la cola también las tendrá. Controlar qué entra en la reverb es tan importante como controlar sus parámetros internos.

**Predelay**
El tiempo entre la señal directa y el inicio del campo reverberante. Rango habitual para la mayoría de las aplicaciones: 10–80 ms. En voces, un predelay de 30–60 ms preserva la inteligibilidad porque el oyente escucha la voz directa antes de que entre la cola. Un predelay de 0 ms integra inmediatamente la voz en el espacio: sonido más inmersivo pero menos claro.

**RT60**
El tiempo en que la reverb decae 60 dB. Escalas orientativas:
- Habitación pequeña: 0,3–0,6 s.
- Sala de ensayo: 0,6–1,0 s.
- Sala de conciertos media: 1,5–2,5 s.
- Catedral: 3–10 s.

Un RT60 largo en mezcla no equivale a "más espacio": equivale a más tiempo de ruido de fondo entre frases. Para la mayoría de las aplicaciones en mezcla contemporánea, RT60 moderados (0,8–2,0 s según el material) producen espacio sin destruir la definición.

**EQ antes de la reverb (pre-EQ)**
Controla qué frecuencias excitan el procesador. HPF antes de la reverb: elimina las frecuencias bajas innecesarias que generarían turbidez en la cola. Corte en la zona de medios problemáticos: evita que la reverb amplifique resonancias ya existentes en el instrumento. El pre-EQ modifica la excitación sin tocar la señal directa: el instrumento suena igual; la cola cambia.

**EQ después de la reverb (post-EQ)**
Moldea la cola ya generada. Un roll-off de agudos en la cola aleja perceptualmente el instrumento porque simula la atenuación natural de los agudos con la distancia. Un corte de graves en la cola reduce la turbidez sin modificar el instrumento. El post-EQ afecta solo la cola: el instrumento seco no cambia.

**Compresión con sidechain de la señal directa**
Un compresor aplicado después de la reverb con sidechain de la señal directa: cuando la señal directa está presente, el compresor baja la reverb (el instrumento "tapa" su propia reverb). Cuando la señal directa deja de sonar, el compresor libera y la reverb sube. El resultado es que la reverb "se abre" entre frases sin tapar el instrumento cuando está sonando. Muy útil en voces donde la inteligibilidad es crítica.

**Delay antes de la reverb**
Un delay corto (30–80 ms) antes de la reverb puede dar más claridad que el predelay solo, porque el delay tiene su propio carácter tímbrico y la separación entre la voz y la reverb se percibe con más definición. La combinación delay + reverb es una técnica habitual en voces modernas.

**Wet/Dry**
La relación entre la señal procesada (wet) y la señal directa (dry) en el canal de efectos. En cadena paralela (send): el canal del instrumento siempre tiene 100% dry; el wet se controla con el fader del canal de reverb. No mezclar ambas señales en el mismo canal a menos que sea intencional.

**Acción**
1. Colocar un HPF antes de la reverb como punto de partida en cualquier instrumento (excepto cuando se quiere reverb en graves deliberadamente).
2. Ajustar el predelay: empezar en 30–40 ms para voces y ajustar según la claridad deseada.
3. Ajustar el RT60: empezar moderado y solo aumentar si el espacio lo requiere.
4. Aplicar post-EQ en la cola para controlar turbidez (corte de graves) o percepción de distancia (roll-off de agudos).
5. Si la sibilancia aparece en la cola: filtrar los agudos en el pre-EQ o usar un de-esser antes de la reverb.

**Verificación**
Reproducir la voz o el instrumento con y sin la reverb a nivel equivalente. La reverb bien configurada debe añadir espacio y profundidad sin cambiar la posición percibida de la fuente en primer plano ni añadir colores frecuenciales que no estaban en el instrumento directo.

**Error frecuente**
Excitar la reverb con la señal completa sin procesar y luego intentar corregir los problemas de la cola con post-EQ. Si la señal que excita la reverb tiene turbidez de graves o sibilancias, la cola reflejará esos problemas. Es más efectivo controlar la excitación desde el inicio con pre-EQ que remediar la cola después.

---

### 5-C1 · PROFUNDIDAD PERCIBIDA: LOS FACTORES QUE ALEJAN O ACERCAN

**Situación real**
La mezcla del alumno tiene todos los instrumentos sonando a la misma distancia percibida. Todo parece "pegado" al oído. No hay planos de profundidad: la batería, la guitarra de fondo y la voz principal se perciben en el mismo lugar. Necesita crear la sensación de que algunos elementos están más cerca y otros más lejos.

**Explicación operativa**
La profundidad percibida en una mezcla no depende de un único factor: es el resultado de al menos cuatro señales que el cerebro integra simultáneamente para construir la sensación de distancia de una fuente.

**Factor 1: Nivel relativo del sonido directo**
A mayor distancia, el sonido pierde energía (–6 dB al duplicar la distancia en campo libre). Reducir el nivel de la señal directa de un instrumento lo aleja perceptualmente. Pero el nivel solo no es suficiente: si solo se baja el fader, el instrumento suena más tranquilo pero no necesariamente más lejano.

**Factor 2: Contenido de alta frecuencia**
El aire absorbe los agudos antes que los graves. Un instrumento a 10 metros suena más oscuro que el mismo instrumento a 1 metro aunque esté al mismo nivel. Un LPF sutil aplicado al canal directo de un instrumento produce una sensación de mayor distancia que el mismo recorte de nivel sin el filtro. El contenido de alta frecuencia es la primera señal de distancia que el cerebro procesa.

**Factor 3: Relación directo/reverb**
A mayor distancia, la proporción de campo reverberante aumenta respecto al sonido directo. Para alejar un instrumento: aumentar el wet de su reverb y/o reducir el nivel directo. Para acercarlo: aumentar el nivel directo y/o reducir el wet.

**Factor 4: Tiempo de las early reflections**
Las early reflections de un espacio más grande tarden más en llegar. Un predelay más largo en la reverb del instrumento contribuye a la sensación de que el instrumento está en un espacio mayor, lo que implica mayor distancia percibida.

**Construcción práctica de un plano de profundidad**
Para alejar un instrumento: reducir el nivel directo + HPF o LPF sutil en el canal directo + aumentar la proporción de reverb (más wet o reverb con predelay más largo).

Para acercar un instrumento: aumentar el nivel directo + preservar o realzar los agudos + reducir la reverb o usar predelay corto.

La diferencia de profundidad percibida entre el primer plano (voz) y el fondo (guitarras de acompañamiento) puede construirse principalmente con la diferencia de brillo (agudos) y de proporción de reverb, sin necesidad de diferencias de nivel grandes.

**Acción**
1. Identificar qué elementos deben estar en primer plano (voz, bombo, bajo) y cuáles en planos más lejanos.
2. Para los elementos de fondo: aplicar LPF sutil en el canal directo (–2 a –4 dB en el rango de 8–12 kHz puede ser suficiente) + aumentar la proporción de reverb.
3. Para el primer plano: preservar los agudos, reducir la reverb al mínimo o usar solo predelay sin cola larga.
4. Comparar los planos reproduciendo el material completo y verificando si la diferencia de distancia es perceptible.

**Verificación**
Reproducir la mezcla e identificar si los elementos tienen posiciones distintas en el plano de profundidad. Si todo suena a la misma distancia, el primer ajuste es comparar el brillo de los instrumentos entre sí: los del primer plano deben sonar más brillantes que los del fondo aunque tengan el mismo nivel nominal.

**Error frecuente**
Usar solo el nivel del fader para gestionar la profundidad sin considerar el LPF ni la reverb. Un instrumento más bajo de nivel que otro no necesariamente suena más lejano: puede sonar simplemente más silencioso. La distancia percibida requiere la combinación de los factores de nivel, timbre y campo reverberante.

---

### 5-C2 · DELAY: HERRAMIENTA ESPACIAL Y MUSICAL

**Situación real**
El alumno inserta un delay en una guitarra. El delay produce repeticiones que compiten rítmicamente con la guitarra y ensucia la mezcla. Lo baja hasta que casi no se escucha. No sabe cómo usarlo para que contribuya al espacio en lugar de competir con el instrumento.

**Explicación operativa**
El delay puede usarse de tres formas distintas en la mezcla, y cada una requiere una configuración diferente:

**Como herramienta espacial (corto, 1–35 ms)**
En el rango del efecto Haas, un delay muy corto aplicado a una copia paneada al canal opuesto crea apertura estéreo. El cerebro integra las dos señales como una sola fuente y localiza el sonido hacia la señal más temprana, produciendo la sensación de que el instrumento ocupa más espacio lateral sin comb filtering severo. Esta técnica es una alternativa al falso estéreo con sample delay: el resultado es similar pero con el delay sincronizable y con control de feedback.

**Como herramienta musical (sincronizado al tempo)**
En el rango de 80 ms a varios cientos de ms (dependiendo del tempo), el delay produce repeticiones que se perciben como eventos rítmicos. Si el tiempo del delay está sincronizado al tempo del material —cuarto de nota, octava de nota, punteado— las repeticiones caen en el pulso y contribuyen a la sensación rítmica en lugar de competir con el instrumento. Un delay de negra sincronizado produce una repetición por cada tiempo del compás; uno de corchea, dos repeticiones por tiempo.

Parámetro clave: el feedback controla cuántas repeticiones se producen antes de que la señal desaparezca. Feedback bajo (1–2 repeticiones) es sutil y espacial. Feedback alto (5+ repeticiones) produce una cola de ecos que llena el espacio entre frases.

**Como herramienta combinada con reverb**
Un delay de 40–80 ms antes de la reverb puede dar más claridad que el predelay solo, porque el delay tiene su propio carácter tímbrico y la separación entre la señal directa y la cola reverberante se percibe con más definición. La combinación es especialmente efectiva en voces donde la inteligibilidad es crítica pero se quiere espacio amplio.

**Tipos de delay por carácter**
- **Tape delay:** emula las irregularidades del cabezal magnético: oscilaciones de velocidad leves, compresión, coloración tonal de las repeticiones. Carácter muy musical y cálido.
- **Analog delay:** emula el delay analógico (BBD, bucket-brigade devices): las repeticiones se oscurecen gradualmente con cada ciclo de retroalimentación. Carácter cálido y sin las irregularidades del tape.
- **Digital delay:** repeticiones exactas e idénticas a la señal original. Muy preciso pero puede sonar frío en comparación con tape o analog. Efectivo cuando se quiere que las repeticiones se escuchen claramente.
- **Multitap delay:** varias cabezas de reproducción a tiempos distintos, produciendo patrones de repetición complejos.

**Sincronización al tempo**
La sincronización del delay al tempo del material puede hacerse manualmente (calculando el tiempo en ms a partir del BPM: ms = 60.000 ÷ BPM para un cuarto de nota) o activando la sincronización MIDI/tempo del plugin si está disponible. Para puntillo de negra: multiplicar el tiempo de negra por 1,5.

**Acción**
1. Para apertura estéreo con el efecto Haas: usar delay corto (5–20 ms) en una copia paneada al lado opuesto, sin feedback o con feedback mínimo.
2. Para delay musical sincronizado: activar sincronización de tempo, elegir la subdivisión (negra, corchea, puntillo de negra según el groove), ajustar feedback al número de repeticiones deseado.
3. Para delay antes de reverb en voces: usar 30–80 ms sin feedback o con feedback mínimo, antes del canal de reverb.
4. Controlar la cantidad de delay en la mezcla con el fader del canal del efecto (send en paralelo), no con el nivel del send.

**Verificación**
Reproducir el pasaje con delay sincronizado al tempo. Las repeticiones deben "encajar" rítmicamente con el material: no deben competir con el instrumento ni producir acentos en tiempos débiles. Si las repeticiones suenan fuera de lugar rítmicamente, verificar la sincronización de tempo o cambiar la subdivisión.

**Error frecuente**
No sincronizar el delay al tempo del material y obtener repeticiones que compiten rítmicamente con el instrumento. El delay no sincronizado puede sonar espacial a bajo nivel, pero a cualquier nivel audible como repeticiones produce una sensación de desorganización rítmica que confunde en lugar de contribuir al espacio.

---

## SECCIÓN 5 — DOSSIER CANÓNICO DE APOYO

---

### POSICIONAMIENTO Y ANCHURA

**Ley de panorama — cuatro configuraciones**

| Configuración | Comportamiento | Referencia histórica |
|---|---|---|
| +3 dB en extremos | Los extremos son 3 dB más fuertes que el centro | Poco habitual en mezcla moderna |
| –3 dB en centro | El centro es 3 dB más bajo que los extremos | Estándar digital más habitual |
| –4,5 dB en centro | Punto intermedio acústico/eléctrico | SSL, Neve, Focusrite analógico |
| –6 dB en centro | Amplitud de voltaje constante en cualquier posición | Más adecuado para comparación mono/estéreo |

Elegir la configuración antes de comenzar la mezcla. No modificarla si hay compresión en el bus establecida.

**Localización de graves**
Por debajo de ~200 Hz, el cerebro pierde capacidad de localizar por diferencias de nivel entre oídos. Lo que se percibe como "instrumento a la izquierda" en señales de baja frecuencia es el contenido de medios y agudos, no el grave. Mantener bombo y bajo al centro.

**Doubling y monocompatibilidad**

| Tipo | Imagen estéreo | Comb filtering en mono | Carácter |
|---|---|---|---|
| Doubling real | Por diferencias naturales de toma | Presente; variable según las tomas | Musical, orgánico |
| Falso estéreo (1–35 ms) | Por efecto Haas | Predecible (f = 1/2Δt) | Controlado, menos orgánico |
| Falso estéreo (>35 ms) | Eco perceptible | Igual | Efecto de eco, no doubling |

Cerrar el paneo del doubling para "mejorar" la monocompatibilidad empeora el problema.

**Codificación Mid/Side**

| Señal | Contenido | Operación |
|---|---|---|
| Mid | Lo que está al centro (suma L+R) | M = (L + R) / 2 |
| Side | Lo que está en los laterales (diferencia L–R) | S = (L – R) / 2 |
| Reconstrucción L | — | L = M + S |
| Reconstrucción R | — | R = M – S |

---

### REVERBERACIÓN

**Secuencia temporal**
1. Sonido directo: localización y timbre de referencia.
2. Early reflections (0–80 ms): información del recinto; no se perciben como ecos.
3. Predelay: separación entre señal directa y cola densa.
4. Campo reverberante: masa difusa de reflexiones. RT60 = tiempo de decaimiento de 60 dB.

**Tipos de reverb**

| Tipo | Carácter | Aplicación principal |
|---|---|---|
| Placa | Suave, denso, uniforme, brillante | Batería (snare), voces |
| Resortes | Metálico, dispersivo, no lineal | Guitarras, efectos creativos |
| Algorítmica | Flexible, variable según algoritmo | Cualquier aplicación con control de parámetros |
| Convolución (IR) | Exacta al espacio capturado | Recintos reales, emulaciones de hardware |

**Procesamiento de la reverb**

| Etapa | Herramienta | Función |
|---|---|---|
| Antes | HPF | Elimina graves que generan turbidez en la cola |
| Antes | EQ correctivo | Evita que la reverb amplifique problemas del instrumento |
| Antes | Saturación suave | Suaviza el ataque de excitación |
| Después | EQ (roll-off agudos) | Aleja la fuente perceptualmente |
| Después | EQ (corte graves) | Reduce acumulación de densidad |
| Después | Compresor + sidechain dry | Abre la reverb entre frases; mejora inteligibilidad |

---

### PROFUNDIDAD Y DELAY

**Factores de profundidad percibida**

| Factor | Para alejar | Para acercar |
|---|---|---|
| Nivel directo | Reducir | Aumentar |
| Agudos | LPF sutil en el directo | Preservar o realzar agudos |
| Reverb (wet) | Aumentar | Reducir |
| Predelay | Predelay más largo | Predelay más corto |

**Delay — tipos y carácter**

| Tipo | Carácter de las repeticiones | Uso típico |
|---|---|---|
| Tape | Irregularidades, compresión, oscilaciones de velocidad | Carácter cálido, vintage |
| Analog | Repeticiones que se oscurecen progresivamente | Carácter cálido, controlado |
| Digital | Repeticiones exactas | Precisión; puede sonar frío |
| Multitap | Múltiples repeticiones a distintos tiempos | Patrones rítmicos complejos |

**Sincronización de delay al tempo**
- Negra: 60.000 ÷ BPM (ms)
- Corchea: 30.000 ÷ BPM (ms)
- Negra puntillo: (60.000 ÷ BPM) × 1,5

---

## SECCIÓN 6 — REGLAS PARA RAG

### Qué indexar

- Ley de panorama: cuatro configuraciones con tabla y criterio.
- Pan Law y compresión del bus: relación de dependencia.
- Localización de graves: límite de ~200 Hz para localización por nivel.
- Criterio de posicionamiento por jerarquía (peso, rango frecuencial, tipo de señal).
- Doubling real vs falso estéreo: tabla de diferencias con monocompatibilidad.
- Efecto Haas / ley de precedencia: rango temporal y aplicación.
- Codificación M/S: fórmulas y tabla de contenido Mid/Side.
- MS en mezcla vs MS en mastering: distinción de contexto.
- Secuencia temporal de la reverberación: sonido directo, early reflections, predelay, campo reverberante.
- RT60: definición y escalas de referencia por tipo de recinto.
- Tabla de tipos de reverb con carácter y aplicación.
- Tabla de procesamiento de reverb (pre y post) con función.
- Compresión de reverb con sidechain: función y uso.
- Delay + reverb en voces: criterio de combinación.
- Tabla de factores de profundidad percibida.
- Tipos de delay con carácter y uso.
- Sincronización de delay al tempo: fórmulas.

### Qué no indexar

- Análisis de referencia con artistas específicos del autor fuente.
- Plugin Ambience como referencia central (puede mencionarse con atribución en capa de apoyo).
- Formulaciones específicas del Apunte Reverb 2025 V2 ni del PDF Ley de Panorama.
- MS de mastering sobre programa completo: pertenece a Eje 7.

### Etiquetado por eje
`eje:5` para todo el contenido de esta unidad.

### Etiquetado por bloque interno
`bloque:5A` — posicionamiento y anchura.
`bloque:5B` — reverberación.
`bloque:5C` — profundidad y delay.

### Etiquetado por fase LDOV
- Lectura de imagen con goniómetro/correlatómetro (cruza con Eje 1): `LDOV:Leer`.
- Decisión de tipo de reverb, tipo de delay, criterio de posicionamiento: `LDOV:Decidir`.
- Configuración de parámetros, aplicación de procesamiento: `LDOV:Operar`.
- Verificación en mono, comparación con referencia, escucha de planos: `LDOV:Verificar`.

### Teoría mínima vs ampliación opcional

**Teoría mínima obligatoria (prioridad alta):**
- Pan Law: cuatro configuraciones y criterio de elección.
- Graves omnidireccionales: límite de localización a ~200 Hz.
- Doubling vs falso estéreo: diferencias y monocompatibilidad.
- Secuencia temporal de la reverb: sonido directo, early reflections, predelay, cola.
- RT60 como parámetro de control de duración del espacio.
- Pre-EQ en reverb: HPF como punto de partida.
- Factores de profundidad percibida: brillo, nivel, reverb.
- Delay sincronizado al tempo: por qué y cómo.

**Teoría de precisión útil (prioridad media):**
- Codificación M/S: fórmulas y aplicación en mezcla.
- Ley de precedencia (Haas): rango temporal y aplicación.
- Post-EQ en reverb y su impacto perceptual.
- Compresión con sidechain de reverb.
- Combinación delay + reverb en voces.
- Tipos de delay por carácter.

**Teoría profunda opcional (IA/FAQ/anexo):**
- Física de la placa y del resorte.
- Cálculo de RT60 con fórmula de Sabine.
- Mecanismo de localización auditiva: ILD, ITD, HRTF.
- Psicoacústica de la reverberación: fusión perceptual de reflexiones.
- Convolución matemática como proceso.
- Comparativa extendida de algoritmos de reverb por modelo.

---

## SECCIÓN 7 — REGLAS PARA GUIONES

### Partes que deben ser demostración

- **Pan Law en acción:** mostrar en la DAW cómo cambia el nivel en el bus al mover el panpot con distintas configuraciones de Pan Law. La diferencia debe verse en el medidor en tiempo real.
- **Monocompatibilidad del doubling:** reproducir en estéreo y luego en mono, antes y después de la corrección o del ajuste del paneo. La diferencia debe ser claramente audible.
- **Secuencia temporal de la reverb:** usar un plugin de reverb con visualización de early reflections o mostrar la forma de onda de la cola para ilustrar sonido directo, early reflections, predelay y campo reverberante.
- **Pre-EQ vs post-EQ en reverb:** mostrar auditivamente la diferencia entre excitar una reverb con señal completa vs con HPF previo; luego mostrar el roll-off de agudos en la cola.
- **Factores de profundidad:** mostrar en tiempo real el efecto de LPF sutil en la señal directa sobre la percepción de distancia.
- **Delay sincronizado vs no sincronizado:** reproducir el mismo delay con y sin sincronización de tempo. La diferencia de musicalidad debe ser inmediatamente audible.
- **Compresión con sidechain en reverb:** mostrar cómo la reverb "se abre" entre frases con el sidechain activo vs sin él.

### Partes que pueden ser explicación a cámara

- Codificación M/S: concepto con diagrama de suma/diferencia.
- Ley de precedencia (Haas): descripción del fenómeno con gráfico de tiempo.
- Tipos de delay: caracterización con descripción y ejemplo de uso.
- Tipos de reverb: taxonomía con descripción de carácter.

### Partes que conviene enseñar con sesión real

- Posicionamiento completo de una mezcla: desde el centro hacia los extremos, con verificación en mono a cada paso.
- Configuración de reverb completa en voz: pre-EQ + predelay + RT60 + post-EQ + sidechain.
- Construcción de profundidad comparando primer plano con fondo en una sesión real.

### Partes que conviene mandar a la capa de apoyo

- Física de la placa y del resorte (detalle mecánico).
- Cálculo de RT60 con fórmula de Sabine.
- Mecanismo de localización auditiva: ILD, ITD, HRTF.
- Comparativa extendida de reverbs algorítmicas por modelo y algoritmo.
- Modulación estéreo (chorus, ensemble) como herramienta de anchura (cobertura mínima en fuentes).

---

## SECCIÓN 8 — CAPA DE APOYO POR IA

### Temas que conviene dejar listos para profundización vía IA

- Cálculo de RT60 con la fórmula de Sabine a partir de las dimensiones de un recinto.
- Mecanismo de localización auditiva: diferencias interaurales de nivel (ILD), de tiempo (ITD) y función de transferencia relacionada con la cabeza (HRTF).
- Física del reverb de placa y del resorte: por qué su timbre es el que es.
- Comparativa de reverbs algorítmicas: Valhalla Room vs VintageVerb vs FabFilter Pro-R 2 vs otras.
- Técnicas avanzadas de diseño de delay: multitap, modulación del tiempo de delay, ping-pong.
- Modulación estéreo: chorus, ensemble, vibrato estéreo como herramientas de anchura.
- Psicoacústica del envolvimiento espacial y su diferencia con la anchura estéreo.
- Convolución matemática: cómo funciona el proceso de la reverb por convolución.

### Ejemplos de preguntas que el alumno podría hacerle a la IA

- "¿Por qué el bombo no se puede panear fuera del centro y mantener su consistencia en mono?"
- "¿Cómo calculo el tiempo de delay en ms para que esté sincronizado a 120 BPM en negras punteadas?"
- "Explícame la diferencia entre predelay y early reflections en términos de qué le dice cada uno al oído sobre el espacio."
- "¿Cuándo conviene usar una reverb de convolución en lugar de una algorítmica?"
- "¿Cómo configuro la compresión con sidechain en una reverb de voz para que se abra entre frases?"
- "Explícame el mecanismo físico que produce el timbre metálico de los resortes en una spring reverb."
- "¿Qué es el HRTF y cómo se relaciona con la localización de sonidos en auriculares?"
- "¿Cómo uso la ley de precedencia para crear anchura estéreo sin los problemas de monocompatibilidad del doubling?"

---

## SECCIÓN 9 — BLOQUES QUE REQUIEREN ATRIBUCIÓN EXPLÍCITA

### Plugin Ambience — OBLIGATORIA SI SE MENCIONA
El plugin Ambience es una reverb algorítmica desarrollada por Pablo Panitta y Pablo Rabinovich. Si se menciona en cualquier material del curso —guiones, dossier, FAQ, ejemplos—, requiere atribución doble a ambos autores.

**Formulación sugerida para cualquier mención:**
> "Ambience, reverb algorítmica desarrollada por Pablo Panitta y Pablo Rabinovich."

**Restricción estructural:** Ambience no puede ser la referencia central del Eje 5. Los ejemplos de reverb algorítmica en el cuerpo del curso y en el dossier usan referencias de documentación independiente (Valhalla Room, Valhalla VintageVerb, FabFilter Pro-R 2, Lexicon, entre otras).

### PDF Ley de Panorama
Autoría: Pablo Rabinovich. La doctrina técnica del Pan Law es de dominio general del campo. La formulación del apunte no debe reproducirse. El contenido presentado en este eje está reformulado con base en esa doctrina.

### Criterio de nomenclatura "primarios / secundarios / terciarios"
Si se usa el sistema de jerarquía de posicionamiento con ese naming específico (primarios / secundarios / terciarios), requiere atribución a Pablo Rabinovich. En este eje se usa una reformulación del mismo principio con terminología diferente (jerarquía por peso, rango frecuencial y tipo de señal), lo que no requiere atribución.

### PDF Apunte Reverb 2025 V2
Autoría: Pablo Rabinovich. La fenomenología de la reverberación y los tipos son doctrina técnica general del campo. El contenido presentado en este eje está reformulado. Si se cita cualquier formulación directa del apunte, la cita requiere atribución puntual.

### Ley de precedencia / Efecto Haas
Documentado por Helmut Haas en su tesis doctoral (1949). Dominio público científico. Se puede presentar como "ley de precedencia" o "efecto Haas" con atribución a Haas al introducir el término.

---

## SECCIÓN 10 — CONTINUIDAD CON OTROS EJES

**De dónde viene este eje**
El Eje 5 viene del **Eje 4 — Energía y movimiento**.

La señal que llega al Eje 5 tiene carácter tonal definido (Eje 3) y energía gestionada (Eje 4). La dimensión espacial se construye sobre esa base. Si la dinámica no está controlada, la reverb amplifica las variaciones dinámicas no deseadas: los picos dinámicos de un instrumento sin comprimir producen una cola reverberante también dinámica que puede sonar irregular o descontrolada.

Cruce activo con Eje 1: el goniómetro y el correlatómetro (herramientas de Eje 1) son los instrumentos de diagnóstico de la imagen que el Eje 5 construye. A medida que se construye el posicionamiento y la reverb, el goniómetro monitoriza la forma de la imagen y el correlatómetro verifica la monocompatibilidad.

Cruce con Eje 2: el comb filtering producido por el doubling o el falso estéreo puede diagnosticarse en Eje 1. Si ese comb filtering es un problema técnico no deseado (por ejemplo, en una grabación multimicrófono), se corrige en Eje 2. En el Eje 5, el comb filtering del doubling es un costo técnico de una herramienta creativa, gestionable pero no necesariamente problemático.

**A qué eje prepara**
El Eje 5 prepara directamente al **Eje 6 — Integración global**.

La lógica del cruce: una vez que cada elemento tiene su carácter tonal, su energía y su posición en el espacio, el Eje 6 trabaja la mezcla como sistema integrado: el balance espectral global, la compresión del bus de salida que "pega" todos los elementos, la automatización que da movimiento dinámico a la mezcla completa, y las decisiones finales antes de entregar para masterización.

**Cruce con Eje 7**
El procesamiento Mid/Side sobre el programa completo, el balance espacial de la señal entregada y la corrección de imagen estéreo en la masterización pertenecen al Eje 7. El M/S del Eje 5 opera sobre la imagen en construcción durante la mezcla; el M/S del Eje 7 opera sobre el resultado final ya consolidado.

---

*KENTH Academy — Eje 5 · Versión de producción v1.0*
*Generado desde arquitectura congelada v1.0-final y paquete limpio Eje 5.*
