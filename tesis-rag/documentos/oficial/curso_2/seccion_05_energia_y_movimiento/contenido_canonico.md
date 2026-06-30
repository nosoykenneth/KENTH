---
course_id: "2"
moodle_section_id: "20"
section_id: "20"
section_number: "5"
section_slug: "energia_y_movimiento"
section_title: "SECCIÓN 4: Energía y movimiento"
resource_type: "lesson_content"
content_type: "markdown"
layer: "canonical"
scope: "section"
source: "canonical_md"
source_origin: "course"
status: "ready_for_indexing"
visible_to_student: "true"
allowed_for_indexing: "true"
version: "v1"
legacy_axis: "Eje 4"  # solo trazabilidad de migración; NO usar como fuente
---

# EJE 4 — ENERGÍA Y MOVIMIENTO
### KENTH Academy · Mezcla y Masterización · Contenido Final de Curso

---

## SECCIÓN 1 — FUNCIÓN PRÁCTICA DEL EJE

El Eje 4 controla el comportamiento energético de las señales en el tiempo: cuánto impacto tienen, qué tan densa se siente su presencia, cómo respiran dinámicamente y cómo ceden espacio a otros elementos.

El Eje 3 definió el carácter tonal de cada instrumento. El Eje 4 trabaja con lo que no puede verse en un analizador espectral: la envolvente, el movimiento, la energía que la señal entrega al oído segundo a segundo. Una mezcla con identidad espectral bien construida pero sin control dinámico suena plana, sin dirección, sin vida.

El eje tiene seis dominios:

**Parámetros del compresor:** cómo funciona cada control y cómo interactúan entre sí. Sin entender los parámetros, la compresión es un proceso de prueba y error sin dirección.

**Circuitos analógicos y su carácter:** qué tipo de elemento realiza la reducción de ganancia en cada familia de compresores, y qué implica eso para el sonido resultante.

**Objetivos y técnicas:** qué se quiere lograr con la compresión (técnicamente y artísticamente) y cómo aplicarla en paralelo, en serie o con sidechain.

**Marco de abordaje sistemático:** cómo relacionar las características de una señal con los parámetros de compresión más adecuados para procesarla.

**Expansores, compuertas y ducking:** las herramientas que actúan debajo del umbral y las que ceden espacio por sidechain.

**Limitadores y clippers en mezcla:** protección de picos y herramientas de densidad a nivel de canal y grupo.

**Límites del eje:**
- El EQ dinámico y el de-esser pertenecen al Eje 3 y no se desarrollan aquí.
- La compresión del bus de salida y el rango dinámico global de la mezcla pertenecen al Eje 6.
- Los limitadores y clippers en masterización pertenecen al Eje 7.

---

## SECCIÓN 2 — QUÉ DEBE PODER HACER EL ALUMNO AL TERMINAR ESTE EJE

Al completar el Eje 4, el alumno es capaz de:

- Ajustar threshold, ratio y knee con criterio de necesidad, no por valor numérico.
- Distinguir entre hard knee y soft knee, y elegir según el tipo de señal y el objetivo.
- Configurar los tiempos de ataque y release sabiendo qué modifica cada uno en la envolvente del instrumento.
- Usar makeup gain correctamente: partir desde 0 y comparar en igualdad de nivel.
- Identificar si un compresor usa detector Peak o RMS, feed-forward o feedback, y qué implica cada combinación para el resultado.
- Configurar stereo link o dual mono según el material procesado.
- Identificar qué tipo de circuito realiza la reducción de ganancia en los principales compresores analógicos y elegir según el objetivo.
- Definir el objetivo técnico o artístico de la compresión antes de ajustar un parámetro.
- Aplicar compresión en paralelo y en serie con criterio de tarea por etapa.
- Usar el filtrado del sidechain para controlar qué disparará el compresor.
- Conectar un sidechain externo para ducking o compuerta disparada externamente.
- Aplicar el marco de abordaje sistemático de la compresión para orientar el primer ajuste de parámetros según las características de la señal.
- Configurar una compuerta con threshold, hold y filtro del detector para batería con bleed.
- Establecer ducking de música bajo voz con sidechain externo correcto.
- Distinguir limitador de clipper y aplicar cada uno según el objetivo en mezcla.

---

## SECCIÓN 3 — SUBSECCIONES FINALES DEL EJE

El orden sigue la lógica herramienta → criterio → aplicación → marco de abordaje → herramientas de umbral inferior → herramientas de techo. Los parámetros van primero para que el alumno sepa qué controla antes de entrar al criterio y al marco de abordaje. Los circuitos analógicos preceden a las técnicas porque el tipo de compresor condiciona qué técnica es apropiada.

**BLOQUE A — PARÁMETROS DEL COMPRESOR**

- **4-A1** · Curva de transferencia: threshold, ratio y knee
- **4-A2** · Envolventes: ataque, release y hold
- **4-A3** · Makeup gain, circuito detector y parámetros de estéreo

**BLOQUE B — CIRCUITOS ANALÓGICOS**

- **4-B1** · Clasificación por mecanismo de reducción: cinco familias

**BLOQUE C — OBJETIVOS Y TÉCNICAS**

- **4-C1** · Objetivo antes que parámetros: técnicos y artísticos
- **4-C2** · Compresión paralela, en serie y sidechain

**BLOQUE D — MARCO DE ABORDAJE SISTEMÁTICO**

- **4-D1** · Criterio del Triángulo: señal, objetivo y parámetros

**BLOQUE E — EXPANSORES, COMPUERTAS Y DUCKING**

- **4-E1** · Expansores y compuertas: herramientas de umbral inferior
- **4-E2** · Ducking: sidechain externo para ceder espacio

**BLOQUE F — LIMITADORES Y CLIPPERS EN MEZCLA**

- **4-F1** · Limitadores y clippers: protección y densidad en mezcla

---

## SECCIÓN 4 — CURSO PRINCIPAL DEL EJE

---

### 4-A1 · CURVA DE TRANSFERENCIA: THRESHOLD, RATIO Y KNEE

**Situación real**
El alumno inserta un compresor en una pista de voz. Sin saber bien qué hace, mueve el threshold hasta que el medidor de reducción de ganancia se mueve. Luego sube el ratio "para que comprima más". La voz empieza a sonar comprimida, pero no sabe si está bien o si está destruyendo algo útil. No tiene un punto de referencia para sus decisiones.

**Explicación operativa**
La curva de transferencia de un compresor define la relación entre lo que entra y lo que sale. Tres parámetros la determinan: el umbral (a partir de qué nivel actúa), la relación de compresión (cuánto actúa sobre lo que supera el umbral) y el tipo de transición entre zona sin compresión y zona con compresión (el knee).

**Threshold (umbral)**
El threshold define el nivel a partir del cual el compresor comienza a reducir la ganancia. Todo lo que quede por debajo del umbral pasa sin modificación; todo lo que lo supere entra en la zona de compresión. El valor numérico en el panel no equivale directamente a dBFS: depende del diseño interno del compresor. La referencia correcta no es el número: es el medidor de reducción de ganancia (GR). Si el GR no se mueve, el threshold está por encima del material. Si el GR se mueve constantemente, el threshold está tan bajo que el compresor procesa todo el tiempo.

**Ratio**
El ratio define cuánto sube la señal de salida por cada dB que la señal de entrada supera el umbral. Ratio 2:1: por cada 2 dB sobre el umbral, solo sube 1 dB en la salida. Ratio 4:1: por cada 4 dB sobre el umbral, solo sube 1 dB. Ratio ∞:1: ningún incremento de señal supera el umbral en la salida: limitación.

Orientación práctica por rango de ratio:
- ≤2:1: compresión suave; reducción dinámica mínima, más musical, útil para glue.
- 4:1: compresión media; el estándar para muchas situaciones de mezcla.
- ≥8:1: compresión dura; control agresivo de picos.
- ≥20:1: limitación.

**Knee**
El knee define la forma de la transición entre la zona sin compresión y la zona con compresión en torno al threshold. Hard knee: la transición es abrupta, exactamente en el umbral. El compresor no actúa debajo del umbral y actúa al ratio completo al superarlo. Soft knee: la transición es gradual; la compresión comienza antes del umbral y alcanza el ratio completo de forma progresiva.

Hard knee es más adecuado para control de picos percusivos donde se necesita precisión. Soft knee es más natural para voces, cuerdas y buses donde la compresión no debe percibirse como un evento. Algunos compresores analógicos tienen curvas de transferencia que no son estrictamente ni una ni otra: son curvas híbridas que forman parte de su carácter propio.

**Teoría mínima**
La compresión puede ser descendente (downward) o ascendente (upward). La descendente —la más habitual— reduce la ganancia de lo que supera el umbral, reduciendo el rango dinámico por arriba. La ascendente aumenta la ganancia de lo que queda por debajo del umbral, comprimiendo el rango dinámico por abajo. La compresión ascendente puede combinarse con la descendente para lograr una dinámica más uniformizada, pero eleva también el piso de ruido de la señal.

En algunos compresores (incluido el SSL), cambiar el ratio también cambia el knee, lo que modifica el carácter completo de la respuesta más allá de la "cantidad" de compresión. No son siempre parámetros independientes.

**Acción**
1. Cargar el compresor con makeup gain en 0 y ratio y threshold en valores neutros.
2. Reproducir la sección más representativa del instrumento.
3. Bajar el threshold hasta que el GR muestre movimiento en los momentos que se quieren comprimir.
4. Ajustar el ratio según la intensidad de la reducción deseada.
5. Ajustar el knee según el tipo de señal y el objetivo (hard para percusivos, soft para sostenidos).
6. Verificar con bypass a nivel compensado antes de aprobar.

**Verificación**
Con el GR activo: la reducción debe moverse en los momentos donde el problema o el objetivo lo requiere, y no moverse (o moverse poco) en el resto. Si el GR se mueve constantemente, el threshold está demasiado bajo. Si no se mueve en los picos que se quería controlar, está demasiado alto.

**Error frecuente**
Subir el ratio para "comprimir más" sin considerar que algunos compresores cambian el knee al cambiar el ratio, modificando toda la curva de transferencia. Lo que parecía un ajuste de cantidad se convierte en un cambio de carácter. Verificar siempre el resultado auditivo completo después de cada cambio de ratio.

---

### 4-A2 · ENVOLVENTES: ATAQUE, RELEASE Y HOLD

**Situación real**
El alumno tiene un compresor en el bombo. El bombo se está comprimiendo bien en nivel, pero ha perdido el golpe inicial: no se siente el impacto del beater. En otro caso, el compresor tiene bombeo evidente entre notas: se escucha cómo "respira" el nivel de la señal de forma antinatural. Ambos son problemas de envolventes.

**Explicación operativa**
Los tiempos de envolvente del compresor determinan cómo el compresor entra y sale de la compresión en el tiempo. Son los parámetros que definen si la compresión es audible o invisible, y si moldea la envolvente del instrumento o la destruye.

**Tiempo de ataque**
El tiempo de ataque es el tiempo que tarda el compresor en alcanzar la reducción de ganancia objetivo desde que la señal supera el umbral. La reducción comienza desde el primer ciclo de la señal: el ataque no es cuánto espera el compresor para actuar, sino cuánto tarda en llegar a la reducción completa.

Un ataque lento deja pasar el transitorio inicial sin comprimirlo: el impacto del golpe llega intacto al oído, y luego el compresor atrapa el cuerpo de la señal. Un ataque rápido comprime desde el transitorio: reduce el impacto pero controla mejor los picos más agudos.

La comparación de tiempos de ataque entre distintos compresores solo es válida si usan el mismo criterio de medición. Los compresores analógicos clásicos usan el criterio del 63% (tiempo para alcanzar el 63% de la reducción). Muchos compresores digitales usan el criterio del 10/90% (tiempo entre 10% y 90% de la reducción). "10 ms" en un compresor no equivale a "10 ms" en otro que use un criterio diferente.

**Tiempo de release**
El release es el tiempo que tarda el compresor en liberar la reducción de ganancia una vez que la señal vuelve por debajo del umbral. Un release demasiado rápido produce bombeo: el nivel sube bruscamente después de cada compresión y ese movimiento se escucha. Un release demasiado lento mantiene el compresor activo más tiempo del necesario, aplastando el material que viene después del pico.

El release óptimo depende del tipo de señal y del objetivo. Para señales percusivas con transitorios rápidos y separados, un release relativamente rápido evita que la compresión de un golpe afecte al siguiente. Para señales sostenidas o buses, un release más lento produce compresión continua y musical. La función de auto-release presente en muchos compresores adapta el tiempo de liberación al contenido del programa, lo que puede ser muy eficiente para material mixto.

La relación entre el release y el tempo del material importa: un release que coincide con el pulso musical puede hacer que la compresión respire al ritmo de la canción, produciendo un efecto de movimiento que puede ser muy efectivo.

**Hold**
El hold define el tiempo mínimo durante el cual la compresión se mantiene activa después del ataque, incluso si la señal ya bajó del umbral. Evita que el compresor o la compuerta se cierren abruptamente en las pausas breves entre transitorios, produciendo saltos de nivel molestos. Especialmente útil en compuertas para evitar que se cierren entre sílabas o antes de que el cuerpo de un sonido percusivo haya terminado.

**Look-ahead**
El detector del compresor lee la señal con una pequeña anticipación, lo que le permite comenzar la reducción de ganancia antes de que el pico llegue a la salida. Resultado: el compresor puede reaccionar a transitorios muy rápidos sin distorsión de entrada. El precio es latencia: el procesador introduce un retardo en la señal de salida que debe compensarse con el plugin delay compensation del DAW.

**Acción**
1. Para preservar el impacto de un transitorio percusivo: empezar con ataque lento y ajustarlo hasta que el GR no atrape el transitorio inicial.
2. Para controlar picos agresivos sin merma del cuerpo: reducir gradualmente el ataque hasta encontrar el punto donde el control de picos se mantiene pero el golpe no desaparece.
3. Para resolver bombeo: aumentar el release. Si el bombeo persiste, también puede reducirse el ratio o subirse el threshold.
4. Verificar la relación del release con el tempo del material reproduciendo en contexto de mezcla.

**Verificación**
Comparar la señal procesada con el bypass en igualdad de nivel. Si el instrumento perdió su identidad de golpe o de arranque, el ataque es demasiado rápido. Si hay movimiento rítmico audible en el nivel que no corresponde a la dinámica del instrumento, el release está desfasado del material.

**Error frecuente**
Asumir que el tiempo de ataque es el tiempo que espera el compresor antes de actuar. No lo es: la reducción comienza desde el primer ciclo que supera el umbral. El ataque solo define cuánto tarda en llegar a la reducción completa. Con esta comprensión incorrecta, muchos alumnos intentan "dejar pasar el transitorio" con ataque lento pero obtienen resultados inesperados porque no entienden que el compresor ya está actuando parcialmente desde el primer momento.

---

### 4-A3 · MAKEUP GAIN, CIRCUITO DETECTOR Y PARÁMETROS DE ESTÉREO

**Situación real**
El alumno carga un compresor con un preset de fábrica. La señal suena "mejor" inmediatamente. Al hacer bypass, la señal suena más plana. Aprueba el preset. Días después, en otra sesión, la misma señal suena diferente. No sabe que el preset venía con makeup activo por defecto y lo que aprobó era simplemente una señal más fuerte.

**Explicación operativa**

**Makeup gain**
La compresión reduce el nivel de la señal. El makeup gain compensa esa reducción para que la salida del compresor esté a un nivel comparable al de la entrada. La trampa: si el compresor se carga con makeup activo por defecto y se compara con bypass sin compensar el nivel percibido, la señal comprimida siempre "suena mejor" porque suena más fuerte.

La regla de trabajo: cargar siempre el compresor con makeup en 0. Evaluar el efecto de la compresión. Compensar el nivel solo después de verificar que la compresión hace lo que se pretende. Comparar siempre con bypass a nivel equivalente antes de aprobar.

**Feed-forward vs feedback**
El detector de un compresor puede leer la señal antes de la reducción de ganancia (feed-forward) o después (feedback). Feed-forward: el compresor mide lo que entra. Su comportamiento es más predecible y puede ser más agresivo. Feedback: el compresor mide lo que sale, creando un sistema de retroalimentación. El resultado tiende a ser más musical y estable, porque la reducción se suaviza por el propio ciclo de retroalimentación.

No hay una correlación fija entre arquitectura feed-forward/feedback y el tipo de circuito de reducción. Los fabricantes combinan según diseño. Un FET puede ser feedback; un VCA puede ser feed-forward. El comportamiento resultante depende de la implementación específica, no de una categoría general.

**Detector Peak vs RMS**
El detector del compresor puede responder a los picos instantáneos de la señal (Peak) o al promedio energético (RMS). El detector Peak sigue las variaciones instantáneas con mayor velocidad y puede ser más agresivo. El detector RMS responde al peso promedio de la señal, más parecido a la percepción auditiva de intensidad sostenida, y produce una compresión generalmente más musical y menos obvia.

Para señales percusivas con transitorios fuertes: un detector Peak permite controlarlos con precisión. Para señales sostenidas y buses: un detector RMS produce compresión más transparente.

**Stereo link vs Dual mono**
En compresores estéreo, el stereo link conecta los sidechains de los canales izquierdo y derecho: si un evento fuerte ocurre en un canal, ambos canales responden simultáneamente con la misma reducción de ganancia. Esto mantiene la imagen estéreo estable. En dual mono, cada canal reacciona de forma independiente: si solo el canal izquierdo supera el umbral, solo ese canal se comprime. La imagen estéreo puede desbalancearse.

Para la mayoría de las situaciones de mezcla con material estéreo: stereo link. Dual mono solo cuando el objetivo específico lo requiere (procesamiento selectivo creativo, o cuando se quiere que cada canal responda a su propia dinámica de forma independiente).

**Distorsión y aliasing**
Los compresores analógicos y sus modelados introducen distorsión armónica (THD) e intermodulación (IMD). Los compresores digitales con circuitos no lineales simulados pueden introducir aliasing cuando la operación no lineal produce componentes de frecuencia por encima del límite de Nyquist. El aliasing es inarmónico y no puede filtrarse a posteriori. Activar oversampling cuando esté disponible en compresores de modelado con circuitos no lineales.

**Acción**
1. Al cargar cualquier compresor: ajustar makeup gain a 0 antes de evaluar el resultado.
2. Verificar en qué posición llega el preset: si hay makeup activo, anotarlo y compensarlo para la comparación.
3. Elegir el modo stereo link para material estéreo a menos que haya un motivo específico para dual mono.
4. Activar oversampling cuando esté disponible en compresores de modelado analógico.

**Verificación**
Al comparar con bypass: el nivel percibido debe ser equivalente. Si el compresor suena mejor que el bypass sin comparación de nivel, repetir la comparación con nivel compensado antes de tomar la decisión.

**Error frecuente**
Cargar un compresor con su preset de fábrica, que puede incluir makeup activo, y aprobar el resultado sin compensar el nivel. La "mejora" percibida es simplemente un aumento de volumen. Si la misma compresión se aplica con makeup en 0, puede sonar indiferente o incluso peor que el bypass.

---

### 4-B1 · CLASIFICACIÓN POR MECANISMO DE REDUCCIÓN: CINCO FAMILIAS

**Situación real**
El alumno tiene acceso a modelados de varios compresores: un LA-2A, un 1176, un compresor de bus SSL, un Vari-mu. No sabe cuál usar para qué. Todos reducen el nivel cuando la señal supera el umbral, pero suenan radicalmente diferentes.

**Explicación operativa**
Un compresor se clasifica por el elemento que realiza la reducción de ganancia. No por los materiales del chasis ni por los componentes del circuito general: un compresor con válvulas en la etapa de amplificación pero un elemento óptico haciendo la reducción es un compresor óptico. El mecanismo de reducción define el carácter de la respuesta y, en gran parte, el sonido resultante.

**Compresores ópticos (Opto)**
La reducción de ganancia la realiza un sistema óptico: una fuente de luz cuya intensidad varía con el nivel de señal, y un receptor fotosensible que controla la ganancia en respuesta a esa luz. Las envolventes dependen del comportamiento físico del sistema óptico: la velocidad de encendido y apagado del elemento de luz determina el ataque y el release, y son dependientes del programa (responden diferente a distintos tipos de señal). El resultado es una respuesta muy musical, suave y natural.

Su limitación: no son adecuados para el control preciso de transitorios percusivos rápidos, donde la velocidad del sistema óptico es insuficiente para atrapar picos muy cortos.

Aplicaciones: voces, vientos, cuerdas, señales sostenidas. Buses donde se busca suavidad y musicalidad.

**Compresores VCA (Voltage Controlled Amplifier)**
La reducción la realiza un amplificador controlado por voltaje. Las envolventes están definidas por el circuito electrónico y pueden configurarse con mayor precisión y rapidez que en los ópticos. Son los compresores más versátiles en términos de control. El carácter varía enormemente entre modelos del mismo tipo: un VCA de la familia API y un VCA SSL tienen caracteres opuestos aunque ambos sean VCA.

Aplicaciones: control de batería, canales individuales, buses. La variedad de aplicaciones es la más amplia de todas las familias.

**Compresores FET (Field Effect Transistor)**
La reducción la realiza un transistor de efecto de campo. Los envolventes son extremadamente rápidas. La arquitectura feedback del detector —frecuente en esta familia— suaviza el comportamiento a pesar de la velocidad, produciendo una compresión dependiente del programa que puede ser muy musical. Los FET agregan un color y carácter marcados a la señal.

Aplicaciones: batería (rooms, close mics), bajo con carácter, voces donde se busca presencia y color. Compresión paralela donde la agresividad de la señal comprimida se mezclará con el original.

**Compresores Vari-mu / Delta Mu (valvulares)**
La reducción la realizan directamente las válvulas del circuito, que modifican su factor de amplificación según el nivel de señal. La respuesta es lenta y dependiente del programa. El carácter es cálido, suave y musical. Incluso sin comprimir de forma audible, la señal que pasa por un valvular puede recibir coloración por saturación armónica de las válvulas.

El pegamento que generan en buses es difícil de igualar con otros tipos de circuito. Aplicaciones: buses de mezcla, masterización, voces y bajo cuando se busca calidez y cohesión.

**Compresores de puente de diodos**
La reducción la realiza un puente de diodos; el sidechain usa una versión rectificada de la señal de audio. Las envolventes son rápidas y la no-linealidad es alta, produciendo un carácter musical muy específico y difícil de replicar con otras topologías. El modelo más representativo es el Neve 33609 / 5254.

Aplicaciones: cuando se busca el carácter específico de esta familia, que es claramente distinto a las otras cuatro.

**Acción**
Antes de elegir el compresor: definir el objetivo (técnico o artístico) y el tipo de señal. Luego elegir la familia cuyo mecanismo de reducción sea más adecuado para ese objetivo y ese tipo de señal. La tabla de la Sección 5 (Dossier) sirve como referencia rápida.

**Verificación**
Después de aplicar: comparar con bypass a nivel compensado y verificar que el carácter que aporta el circuito es el que se buscaba. Si el compresor aporta un carácter indeseado, cambiar de familia antes de intentar compensar con parámetros.

**Error frecuente**
Elegir el compresor por su nombre o por el que aparece por defecto en el template de la sesión, sin considerar el tipo de circuito y su carácter. Un óptico en una batería donde se necesita control preciso de transitorios puede frustrar el objetivo aunque los parámetros estén correctamente ajustados.

---

### 4-C1 · OBJETIVO ANTES QUE PARÁMETROS: TÉCNICOS Y ARTÍSTICOS

**Situación real**
El alumno tiene un bombo que en la mezcla parece correcto en nivel pero no tiene impacto. Inserta un compresor y empieza a mover parámetros sin saber qué quiere lograr. Después de varios minutos el bombo suena diferente pero tampoco tiene impacto. El tiempo pasó ajustando sin dirección.

**Explicación operativa**
Antes de ajustar cualquier parámetro del compresor, hay que definir qué se quiere que el compresor haga. Hay dos categorías de objetivos: técnicos (resolver un problema de dinámica) y artísticos (dar carácter o construir una sensación).

**Objetivos técnicos**

*Limitación de picos:* contener transitorios que superan umbrales críticos de la cadena. Los picos se controlan con ataque rápido, ratio alto y threshold alto (solo actúa sobre los picos más extremos). El objetivo no es cambiar el nivel promedio: es acotar los picos más agudos.

*Nivelación de picos:* controlar la inconsistencia dinámica de una interpretación. Una voz que varía 10 dB entre la nota más fuerte y la más suave necesita nivelación para que el EQ y los efectos posteriores reciban una señal más predecible. Ataque y release moderados, ratio medio, threshold que actúe sobre los momentos más fuertes.

*Incremento del nivel RMS:* aumentar la densidad percibida de la señal. Ratio medio, threshold relativamente bajo para que el compresor actúe sobre buena parte del material, makeup compensado. El resultado es un instrumento que "llena más" sin necesariamente tener picos más altos.

*Nivelación de señal completa:* uniformizar todo el rango dinámico de forma transparente. Ataque lento, ratio bajo, threshold bajo, soft knee. El objetivo es que la interpretación suene más consistente sin que la compresión se note.

**Objetivos artísticos**

*Impacto:* reforzar el punch de transitorios percusivos. Ataque lento para que el transitorio pase sin compresión; luego el compresor atrapa el cuerpo de la señal. El contraste entre el pico libre y el cuerpo comprimido hace que el golpe suene más pronunciado, no menos. Esto es contraintuitivo: para más impacto, el ataque del compresor debe ser más lento.

*Color:* la distorsión armónica y el comportamiento no lineal del circuito modifican el timbre de la señal. Un FET o un óptico agregan color incluso con ratio bajo. Elegir el circuito por su carácter, no solo por su control dinámico.

*Pegamento (glue):* integrar elementos dispares en un conjunto cohesionado. Ratio bajo, soft knee, threshold moderado. La función del compresor es que los instrumentos "se muevan juntos" dinámicamente. El pegamento es más perceptible en compresión de buses y grupos.

**Acción**
1. Antes de abrir cualquier compresor: definir verbalmente el objetivo.
2. Según el objetivo técnico: elegir los parámetros adecuados para ese objetivo específico.
3. Según el objetivo artístico: elegir también el tipo de circuito cuyo carácter es coherente con el objetivo.
4. Verificar que el resultado corresponde al objetivo definido, no a otro objetivo distinto.

**Verificación**
Si el objetivo era impacto y el resultado es un bombo más nivelado pero sin golpe, el ataque fue demasiado rápido: estaba limitando picos en lugar de construir impacto. La verificación es siempre contra el objetivo declarado, no contra una sensación general de "suena mejor o peor".

**Error frecuente**
Aplicar la misma configuración de compresor a todos los instrumentos o a todos los objetivos. Los parámetros adecuados para limitación de picos (ataque rápido, ratio alto, threshold alto) son exactamente opuestos a los adecuados para construir impacto (ataque lento, ratio moderado). Confundir los objetivos produce resultados que deshacen el trabajo de mezcla.

---

### 4-C2 · COMPRESIÓN PARALELA, EN SERIE Y SIDECHAIN

**Situación real**
El alumno quiere más densidad en la batería sin perder el impacto de los golpes. Ha intentado comprimir directamente con ratio alto pero el resultado suena aplastado. También tiene una voz que bombea cuando comprime suficiente para nivelarla. Son dos problemas que la compresión en serie y en paralelo resuelven de formas distintas.

**Explicación operativa**

**Compresión en paralelo**
Mezclar la señal original sin comprimir con una copia de la misma señal procesada de forma agresiva. El original preserva los transitorios y la dinámica natural. La copia comprimida añade cuerpo, densidad y sustento. La mezcla de ambas produce un resultado que tiene el impacto del original y la densidad de la copia comprimida.

La clave: la señal comprimida en paralelo puede comprimirse de forma más agresiva de lo que se usaría en una compresión directa, porque la mezcla con el original suavizará el resultado. Si la copia comprimida se escucha sola y suena aplastada, eso es correcto: al mezclarse con el original, el resultado global preservará los transitorios.

El control de mezcla (wet/dry o parámetro "mix" del plugin) ajusta la proporción entre señal original y señal comprimida.

**Compresión en serie**
Aplicar dos compresores en cadena, cada uno con una tarea diferente. El primer compresor gestiona los picos más extremos con parámetros rápidos y agresivos. Con los picos controlados, el segundo compresor puede trabajar sobre el promedio con mayor musicalidad: ya no necesita gestionar los transitorios extremos, solo el nivel promedio.

El principio: un compresor que trabaja sobre material ya controlado puede ser más sutil y musical que uno que tiene que gestionar él solo todo el rango dinámico. La división de tareas produce un resultado más refinado que una sola etapa de compresión con todos los objetivos.

Orden habitual: primero el más rápido o agresivo (VCA, FET) para los picos; segundo el más musical (óptico, valvular) para el carácter y el cuerpo.

**Filtrado en el sidechain**
El detector del compresor puede recibir un filtro HPF que elimine las frecuencias bajas antes de que lleguen al circuito de detección. Si un compresor de bus recibe material completo con bombo, el bombo domina el detector porque tiene mucha energía: el compresor reacciona principalmente al bombo aunque todo el material esté superando el umbral. Un HPF en el sidechain reduce la influencia del bombo en el detector, haciendo que el compresor reaccione más al balance general de la mezcla y menos al bombo específicamente.

Este principio aplica también a compresores de canal: si el detector está reaccionando a una frecuencia indeseada (subsónicas, bleed de otro instrumento), el filtro del sidechain permite discriminar qué disparará el compresor.

**Sidechain externo**
El detector del compresor puede conectarse a una señal completamente externa: la señal de ese canal se comprime, pero el disparo viene de otra fuente. Esto permite que un elemento domine dinámicamente a otro sin interacción directa entre sus señales de audio. El caso más habitual es el ducking de música bajo voz: la señal de voz va al sidechain del compresor de la música, y cuando la voz sube, la música reduce nivel automáticamente. También permite compuertas disparadas externamente: el bombo dispara la compuerta de un sintetizador, produciendo el efecto de que el sintetizador "respira" al ritmo del bombo.

**Acción**
- Para más cuerpo sin perder impacto: compresión en paralelo. Comprimir agresivo en la copia y mezclar con el original al gusto.
- Para mezcla con rangos dinámicos complejos: compresión en serie con tareas diferenciadas.
- Si el compresor reacciona principalmente al bombo cuando se quiere que reaccione al material general: activar el HPF del sidechain.
- Para ducking: conectar la señal de disparo al sidechain externo del compresor del elemento que debe ceder.

**Verificación**
En compresión paralela: escuchar la mezcla completa y verificar que el impacto de los transitorios se preserva mientras el cuerpo suena más denso. Si el impacto desapareció, reducir el porcentaje de señal comprimida en la mezcla.

En sidechain externo para ducking: reproducir la señal de disparo y verificar que el GR del compresor se mueve exactamente cuando se quiere que el elemento ceda espacio. Si el GR se mueve cuando no debería, verificar el nivel de la señal de disparo o la sensibilidad del threshold.

**Error frecuente**
Usar la señal de voz con sus efectos (reverb, delay) como señal de disparo del ducking. La reverb de la voz también disparará la reducción de nivel, haciendo que la música baje incluso cuando la voz ya ha dejado de sonar pero su reverb aún está activa. La solución es usar un auxiliar paralelo de la voz sin efectos como señal de disparo.

---

### 4-D1 · CRITERIO DEL TRIÁNGULO: SEÑAL, OBJETIVO Y PARÁMETROS

> *Esta subsección se basa en el Criterio del Triángulo, marco desarrollado por Pablo Rabinovich y Pablo Panitta, presentado en AES/CAPER 2023.*

**Situación real**
El alumno tiene frente a sí un bombo, una voz y un pad de sintetizador. Los tres necesitan compresión, pero cada uno con un propósito diferente. No sabe por dónde empezar con ninguno de los tres. Necesita un marco de partida que oriente las decisiones antes de que el oído tome el control.

**Explicación operativa**
El Criterio del Triángulo es un marco de abordaje sistemático de la compresión que relaciona las características de la señal (nivel y duración) con los parámetros de compresión más adecuados para procesarla. Su función no es dar recetas cerradas: es orientar el primer ajuste y reducir el tiempo de prueba y error.

El marco organiza las señales en tres zonas según sus características:

**Zona alta del triángulo: señales de nivel alto y corta duración**
Señales con transitorios fuertes y breves. Los golpes de batería, los ataques de percusión, los transitorios de pizca en guitarra.

Orientación de parámetros:
- Ratio alto: la señal supera el umbral con mucha energía; hay que contenerla con firmeza.
- Hard knee: la transición abrupta en el umbral es adecuada porque los picos son cortos y precisos.
- Threshold alto: el compresor actúa solo en los momentos de mayor energía.
- Envolventes rápidas: la señal es breve; el compresor debe reaccionar y liberar rápidamente.

**Zona media del triángulo: señales de nivel medio y duración intermedia**
Señales con dinámica moderada y presencia continua. Melodías, riffs, líneas instrumentales con transitorios y sostenimiento.

Orientación de parámetros:
- Ratio medio: control sin aplastamiento.
- Knee medio o soft: transición más gradual para no percibir el compresor como un evento.
- Threshold medio: actúa sobre los momentos más fuertes de la señal sin comprimir todo el tiempo.
- Envolventes moderadas: suficientemente rápidas para controlar la dinámica, suficientemente lentas para no destruir la musicalidad.

**Zona baja del triángulo: señales de nivel bajo y mayor duración**
Señales sostenidas, de nivel más constante, con dinámica gradual. Pads, cuerdas largas, señales de fondo, ambientes.

Orientación de parámetros:
- Ratio bajo: compresión suave para una dinámica que ya es relativamente uniforme.
- Soft knee amplio: la transición gradual es coherente con el carácter de la señal.
- Threshold bajo: el compresor actúa sobre casi toda la señal de forma continua y sutil.
- Envolventes lentas: la señal es lenta; el compresor puede responder con calma.

**Aplicación práctica**
El triángulo es un punto de partida, no una receta. Una señal compleja puede tener características de distintas zonas simultáneamente. Un bombo, por ejemplo, puede requerir orientación de zona alta para sus transitorios y zona media para su cuerpo sostenido después del ataque. El marco orienta el primer ajuste; el oído ajusta desde ahí.

**Acción**
1. Evaluar las características de la señal: ¿tiene transitorios cortos y fuertes? ¿Es una señal sostenida de nivel medio? ¿Es un fondo de nivel bajo?
2. Ubicar la señal en la zona del triángulo que mejor corresponde a sus características.
3. Usar los parámetros orientativos de esa zona como punto de partida.
4. Reproducir el instrumento y ajustar a partir del comportamiento del GR y del oído.

**Verificación**
Si los parámetros iniciales del triángulo producen un resultado muy alejado del objetivo, hay dos posibilidades: la señal tiene características mixtas que la ubican en más de una zona, o el objetivo artístico requiere deliberadamente parámetros de una zona diferente a la que corresponde la señal. Ambas son situaciones normales. El marco da la orientación; la escucha da la respuesta.

**Error frecuente**
Usar el marco como una plantilla de parámetros numéricos fijos y no ajustar por oído. El Criterio del Triángulo organiza la lógica de la decisión, no los valores exactos. "Ratio alto para zona alta" no es "ratio = 10:1 siempre para un bombo": es la orientación de que el ratio debe estar en el rango alto para ese tipo de señal, con el ajuste preciso determinado por el material específico.

---

### 4-E1 · EXPANSORES Y COMPUERTAS: HERRAMIENTAS DE UMBRAL INFERIOR

**Situación real**
El alumno tiene una batería grabada con mucho bleed: el micrófono del tambor capta también los platillos y el hi-hat. Entre los golpes del tambor, el micrófono sigue capturando el bleed de los platillos, lo que hace que el tambor "nunca se calle" y el conjunto suene sucio. Necesita una herramienta que reduzca o elimine el bleed entre golpes sin afectar el sonido del tambor cuando se golpea.

**Explicación operativa**
La compresión actúa sobre lo que supera el umbral, reduciendo la dinámica por arriba. Los expansores y compuertas actúan debajo del umbral: reducen (o eliminan) lo que cae por debajo de un nivel mínimo.

**Expansor descendente**
Un expansor descendente actúa por debajo del umbral, reduciendo más el nivel de lo que ya está bajo. La señal que supera el umbral pasa sin modificación. La señal que cae por debajo del umbral se reduce según el ratio del expansor.

El ratio de un expansor conviene interpretarse al revés de cómo se lee en un compresor: ratio 1:2 significa que por cada 1 dB que la señal caiga bajo el umbral, la salida baja 2 dB. La señal débil se hace más débil. Escalas orientativas:

- 1:2 → expansión suave; reducción gradual.
- 1:4 → expansión media.
- 1:8 → expansión dura.
- 1:20 → casi compuerta; la señal bajo el umbral cae muy rápidamente.

El expansor es una alternativa más musical a la compuerta: en lugar de cerrar abruptamente, reduce de forma gradual. En materiales donde el corte abrupto de la compuerta sería audible, el expansor produce un resultado más natural.

**Compuerta**
Un expansor llevado a su expresión máxima: ratio aproximado 1:100 o infinito. La señal que cae por debajo del umbral se elimina completamente de la salida. Parámetros adicionales:

- **Threshold:** nivel por debajo del cual la compuerta se cierra.
- **Attack:** velocidad de apertura de la compuerta cuando la señal supera el umbral.
- **Release:** velocidad de cierre cuando la señal cae por debajo del umbral.
- **Hold:** tiempo mínimo durante el cual la compuerta permanece abierta después de haber detectado señal. Evita que se cierre entre sílabas o antes de que el cuerpo de un sonido haya terminado.
- **Range:** ganancia máxima de reducción cuando la compuerta está cerrada. Si el range es –∞, la compuerta corta completamente. Si se reduce el range a –20 dB, la compuerta no corta completamente sino que baja el nivel 20 dB, produciendo un resultado más musical.

**Filtro del detector en compuertas**
El detector de la compuerta puede recibir un filtro que lo haga reaccionar solo a una zona de frecuencias específica. En batería, si el tambor tiene su fundamental en torno a 180 Hz, colocar un filtro de paso de banda centrado en esa frecuencia en el detector hace que la compuerta se abra principalmente cuando detecta la fundamental del tambor, ignorando el bleed de platillos (que tiene predominantemente contenido de alta frecuencia).

El límite de las compuertas: si dos sonidos ocurren exactamente al mismo tiempo y a niveles similares (por ejemplo, un platillo que acompaña exactamente el golpe del tambor), la compuerta no puede distinguirlos por nivel. Hay que aceptar ese límite o gestionar el bleed por otros medios.

**Acción**
1. Insertar la compuerta en el canal del instrumento con bleed.
2. Abrir el detector a la señal de la fundamental del instrumento objetivo con el filtro del detector.
3. Ajustar el threshold: la compuerta debe abrirse con los golpes del instrumento y cerrarse entre ellos.
4. Ajustar el hold para que la compuerta no se cierre antes de que el cuerpo del sonido haya terminado.
5. Ajustar el release para que el cierre sea gradual y no produzca un corte abrupto audible.
6. Verificar que el bleed entre golpes se reduce sin que los golpes del instrumento sean afectados.

**Verificación**
Reproducir el material y escuchar específicamente los momentos entre golpes. Si el bleed desapareció o se redujo significativamente sin que el sonido del tambor pierda su cuerpo, la compuerta está bien configurada. Si el tambor se corta antes de terminar su decay, el threshold está demasiado alto o el hold demasiado corto.

**Error frecuente**
Configurar el threshold demasiado alto, haciendo que la compuerta se cierre durante el decay del instrumento y produzca un corte audible en el cuerpo del sonido. El resultado es un tambor con golpe limpio pero sin caída natural, que suena artificial y mecánico.

---

### 4-E2 · DUCKING: SIDECHAIN EXTERNO PARA CEDER ESPACIO

**Situación real**
El alumno mezcla una canción con letra. Cuando la voz canta, el piano y las guitarras compiten con ella en la misma zona de medios. La voz pierde presencia durante los coros aunque esté en el nivel correcto. Necesita que los demás elementos cedan espacio automáticamente cuando la voz está activa.

**Explicación operativa**
El ducking conecta la señal de disparo de una fuente (la voz) al sidechain del compresor de otra fuente (el piano, las guitarras o un bus de acompañamiento). Cuando la señal de disparo supera el umbral del compresor, el compresor reduce el nivel del elemento que debe ceder. Cuando la señal de disparo baja, el compresor libera la reducción y el elemento recupera su nivel.

El resultado es que los elementos de acompañamiento reducen nivel automáticamente cuando la voz está activa, sin necesidad de automatizar cada canal manualmente.

**Configuración del ducking**
El sidechain externo recibe la señal de voz (u otro elemento de disparo). El compresor del bus de acompañamiento reacciona a esa señal: cuando la voz sube, el bus de acompañamiento baja.

Detalle crítico: la señal de disparo debe ser la voz sin efectos (sin reverb, sin delay). Si la reverb de la voz también llega al sidechain, el compresor continuará bajando el acompañamiento incluso cuando la voz ya ha terminado pero su cola de reverberación sigue activa. El resultado es que el acompañamiento permanece bajo durante las colas de efecto de la voz, lo que produce un ducking exagerado y antinatural.

La solución es usar un auxiliar paralelo de la voz procesada (dry, sin efectos) como señal de disparo. El sidechain recibe la voz seca; el resultado en la mezcla incluye los efectos normalmente.

**Sidechain externo en contexto musical**
El ducking tiene aplicaciones más allá del control voz/música. Un bombo disparando la compuerta de un sintetizador de pad produce el efecto de que el pad respira rítmicamente con el bombo. Una guitarra rítmica disparando la compuerta de un pad crea un movimiento rítmico en el pad que sigue el patrón de la guitarra. Son aplicaciones creativas del mismo principio técnico.

**Acción**
1. Crear un bus auxiliar de la señal de disparo (voz) sin efectos.
2. Conectar ese auxiliar al sidechain externo del compresor del elemento que debe ceder.
3. Ajustar el threshold para que el ducking se active en el nivel de voz activa.
4. Ajustar el release para que la recuperación sea musical y no produzca un salto de nivel audible al final de cada frase.
5. Verificar con el material completo que el ducking es perceptible como más espacio para la voz pero no como una variación de nivel obvia en el acompañamiento.

**Verificación**
El ducking bien ejecutado no debería escucharse como tal: el oyente debe percibir que la voz tiene presencia y espacio, no que los demás instrumentos están bajando de nivel. Si el ducking es claramente audible como movimiento de nivel del acompañamiento, el range del compresor es demasiado amplio o el release demasiado lento.

**Error frecuente**
Conectar al sidechain la señal de voz con reverb. La cola de reverberación de la voz continúa disparando el compresor después de que la voz ha terminado. El acompañamiento permanece bajo durante las colas de reverb, lo que distorsiona la percepción del espacio y puede hacer que el acompañamiento suene ausente entre frases vocales.

---

### 4-F1 · LIMITADORES Y CLIPPERS: PROTECCIÓN Y DENSIDAD EN MEZCLA

**Situación real**
El alumno tiene un bus de batería donde picos extremos de los overheads saturan el bus ocasionalmente. Un compresor normal que controle esos picos aplasta también el cuerpo de la batería. Necesita algo que intervenga solo en los picos más extremos sin afectar el resto de la dinámica.

**Explicación operativa**
El limitador y el clipper son dos herramientas distintas que operan en el techo de la señal, y no son intercambiables.

**Limitador**
Un compresor con ratio ≥20:1 y envolventes rápidas. La señal no puede superar el threshold definido en la salida. El limitador actúa sobre la ganancia: cuando la señal llega al umbral, reduce la ganancia para que no lo supere.

En mezcla por canal: permite contener transitorios extremos que un compresor normal no alcanza a controlar sin comprimir también el cuerpo del instrumento. Si el threshold se establece por encima del nivel promedio del instrumento y solo actúa en los picos más extremos, el resto de la señal no es afectado.

En buses: con precaución. Un limitador de ataque muy rápido en un bus de batería puede destruir los transitorios de todos los instrumentos que pasan por ese bus. Si el objetivo es solo proteger de picos ocasionales, el ataque puede ser levemente más lento para que los transitorios más cortos no se vean afectados.

**Clipper**
El clipper recorta la forma de onda directamente cuando supera el umbral, en lugar de actuar sobre la ganancia. El resultado es saturación armónica: la forma de onda clippeada genera armónicos adicionales. El clipper actúa sobre la forma de onda; el limitador actúa sobre la ganancia.

Las consecuencias son diferentes: el clipper puede aumentar la densidad percibida de la señal aunque el nivel RMS no suba significativamente, porque la distorsión armónica hace que la señal "llene más" perceptivamente. Un pequeño uso del clipper en elementos percusivos puede aumentar el punch percibido sin los efectos de bombeo que puede producir un limitador rápido.

La cantidad de clipping y el carácter de la distorsión resultante dependen del diseño del plugin. Algunos clippers son suaves y musicales a bajas cantidades de recorte; otros son más agresivos. El clipper no es adecuado para señales sostenidas donde la distorsión armónica sería claramente audible y antinatural.

**Límite del eje:** los limitadores y clippers en masterización —con sus objetivos específicos de ceiling de entrega y loudness integrado— pertenecen al Eje 7. El Eje 4 solo cubre su uso en mezcla a nivel de canal y grupo.

**Acción**
- Para proteger un bus de batería de picos extremos sin afectar el cuerpo: usar un limitador con threshold por encima del nivel promedio y ataque suficientemente rápido para los picos.
- Para aumentar la densidad percibida de un elemento percusivo sin compresión: pequeño uso del clipper verificando que la distorsión resultante es musical.
- Para cualquier uso: verificar con el analizador o el medidor Peak que el nivel de salida no excede el techo esperado.

**Verificación**
Con el limitador: reproducir el pasaje más dinámico y verificar que los picos se controlan pero que el cuerpo del instrumento pasa sin reducción. Si el GR se mueve constantemente, el threshold está demasiado bajo y el limitador está funcionando como compresor.

Con el clipper: escuchar el instrumento con y sin el clipper. Si la distorsión armónica es musical y añade densidad sin sonar sucia, el uso es correcto. Si hay distorsión audible en las notas sostenidas o en el cuerpo del sonido, la cantidad de clipping es excesiva.

**Error frecuente**
Usar el limitador como herramienta de gain staging para corregir un canal que está llegando con demasiado nivel a la cadena. Un limitador bien configurado no debe estar reduciendo ganancia constantemente: eso es trabajo del Trim o del gain de clip (Eje 2). El limitador es para los picos ocasionales que superan lo que el gain staging normal puede gestionar.

---

## SECCIÓN 5 — DOSSIER CANÓNICO DE APOYO

---

### PARÁMETROS DEL COMPRESOR

**Curva de transferencia**

| Parámetro | Definición | Criterio de uso |
|---|---|---|
| Threshold | Nivel a partir del cual actúa el compresor | Referencia: medidor de GR, no el valor numérico |
| Ratio | Relación entrada/salida sobre el umbral | ≤2:1 suave; 4:1 medio; ≥8:1 duro; ≥20:1 limitación |
| Hard knee | Transición abrupta en el umbral | Señales percusivas; control preciso de picos |
| Soft knee | Transición gradual antes del umbral | Voces, cuerdas, buses; compresión menos obvia |
| Compresión downward | Reduce ganancia sobre el umbral | La más habitual en mezcla |
| Compresión upward | Aumenta ganancia bajo el umbral | Comprime por abajo; eleva también el piso de ruido |

**Envolventes**

| Parámetro | Definición | Criterio |
|---|---|---|
| Ataque | Tiempo para alcanzar la reducción objetivo desde que se supera el umbral | Lento para preservar transitorio; rápido para controlar picos |
| Release | Tiempo para liberar la reducción cuando la señal baja del umbral | Rápido para transitorios separados; lento para señales sostenidas |
| Hold | Tiempo mínimo de compresión activa tras el ataque | Evita cierres abruptos en pausas breves |
| Look-ahead | El detector lee con anticipación | Permite reacción anticipada; añade latencia que debe compensarse |

**Criterios de medición del tiempo de ataque**
- 63%: tiempo para alcanzar el 63% de la reducción (criterio analógico clásico).
- 10/90%: tiempo entre 10% y 90% de la reducción (criterio digital frecuente).

Los tiempos de ataque solo son comparables entre compresores que usan el mismo criterio.

**Circuito detector y arquitectura**

| Dimensión | Opción | Carácter |
|---|---|---|
| Detector | Peak | Rápido; responde a variaciones instantáneas |
| Detector | RMS | Responde al promedio energético; más musical |
| Arquitectura | Feed-forward | Lee la entrada; más predecible y agresivo |
| Arquitectura | Feedback | Lee la salida; más estable y musical |
| Modo estéreo | Stereo link | Ambos canales reaccionan juntos; preserva imagen |
| Modo estéreo | Dual mono | Cada canal reacciona independientemente |

**Regla del makeup gain**
Cargar todo compresor con makeup en 0. Evaluar la compresión. Compensar el nivel solo después. Comparar con bypass en igualdad de nivel antes de aprobar.

---

### CIRCUITOS ANALÓGICOS

| Tipo | Mecanismo de reducción | Carácter | Aplicaciones orientativas |
|---|---|---|---|
| Óptico | Elemento óptico (lámpara + fotorresistencia) | Lento; dependiente del programa; muy musical | Voces, vientos, cuerdas, buses suaves |
| VCA | Amplificador controlado por voltaje | Versátil; carácter muy variable entre modelos | Batería, canales, buses (según modelo) |
| FET | Transistor de efecto de campo | Muy rápido; feedback aporta musicalidad; agrega color | Batería (rooms, close), bajo, paralela |
| Vari-mu | Válvulas en circuito de ganancia | Lento; cálido; pegamento excelente | Buses, masterización, voces/bajo suaves |
| Puente de diodos | Puente de diodos; sidechain rectificado | Rápido; no-lineal; carácter muy propio | Cuando se busca ese carácter específico |

---

### OBJETIVOS Y TÉCNICAS

**Objetivos técnicos y orientación de parámetros**

| Objetivo | Ataque | Release | Ratio | Threshold |
|---|---|---|---|---|
| Limitación de picos | Rápido | Rápido | Alto | Alto |
| Nivelación de picos | Moderado | Moderado | Medio | Moderado |
| Incremento de RMS | Lento-moderado | Moderado | Medio | Bajo-moderado |
| Nivelación total | Lento | Lento | Bajo | Bajo |

**Compresión paralela**
- La señal comprimida en la rama de efecto puede ser muy agresiva.
- La mezcla con el original suaviza el resultado global.
- El control wet/dry (o mix) ajusta la proporción.

**Compresión en serie**
- Primer compresor: gestiona picos extremos (VCA, FET).
- Segundo compresor: trabaja el cuerpo y el carácter (óptico, valvular).
- Cada compresor hace una tarea definida.

---

### CRITERIO DEL TRIÁNGULO

*Basado en el Criterio del Triángulo de Pablo Rabinovich y Pablo Panitta (AES/CAPER 2023).*

| Zona | Características de la señal | Ratio | Knee | Threshold | Envolventes |
|---|---|---|---|---|---|
| Alta | Nivel alto / corta duración / transitorios fuertes | Alto | Hard | Alto | Rápidas |
| Media | Nivel medio / duración intermedia | Medio | Medio | Moderado | Moderadas |
| Baja | Nivel bajo / mayor duración / señales sostenidas | Bajo | Soft | Bajo | Lentas |

El triángulo es un punto de partida, no una receta. El oído ajusta desde ahí.

---

### EXPANSORES, COMPUERTAS Y DUCKING

**Expansor descendente: escalas orientativas**

| Ratio | Comportamiento |
|---|---|
| 1:2 | Expansión suave |
| 1:4 | Expansión media |
| 1:8 | Expansión dura |
| 1:20 | Casi compuerta |

**Parámetros de compuerta**
Threshold, attack, release, hold, range. El hold evita que la compuerta se cierre antes de que el cuerpo del sonido haya terminado.

**Filtro del detector en compuerta**
Centrar un filtro de paso de banda en la fundamental del instrumento objetivo para discriminar el disparo e ignorar el bleed de otros elementos.

**Ducking — señal de disparo**
Usar siempre la señal de disparo sin efectos (dry). Si la señal de disparo incluye reverb o delay, esos efectos también dispararán la reducción.

---

## SECCIÓN 6 — REGLAS PARA RAG

### Qué indexar

- Parámetros del compresor: threshold, ratio, knee, ataque, release, hold, makeup gain — con definiciones funcionales y criterios.
- Q constante de cuándo actúa la reducción: desde el primer ciclo.
- Criterios de medición del tiempo de ataque: 63% vs 10/90%.
- Detector Peak vs RMS con criterio de uso.
- Feed-forward vs feedback: diferencia y consecuencia.
- Stereo link vs dual mono con criterio.
- Tabla de circuitos analógicos con mecanismo, carácter y aplicaciones.
- Tabla de objetivos técnicos de compresión con orientación de parámetros.
- Objetivos artísticos: impacto, color, glue.
- Compresión paralela: principio y uso del mix.
- Compresión en serie: principio de división de tareas.
- HPF en sidechain: criterio de uso en buses.
- Sidechain externo: ducking y disparo externo de compuerta.
- Criterio del Triángulo: tabla de zonas y parámetros — **con atribución obligatoria a Rabinovich y Panitta, AES/CAPER 2023**.
- Expansor descendente: escalas de ratio y comportamiento.
- Compuerta: parámetros, hold, filtro del detector.
- Límite del bleed simultáneo: la compuerta no puede separar sonidos simultáneos por nivel.
- Ducking: señal de disparo sin efectos.
- Limitador vs clipper: diferencia estructural y de uso.
- Limitadores en mezcla: uso en canal y grupo (no en mastering).

### Qué no indexar

- EQ dinámico y de-esser: pertenecen a Eje 3.
- Compresión del bus de salida y rango dinámico global: pertenecen a Eje 6.
- Limitadores y clippers en masterización: pertenecen a Eje 7.
- Expresiones orales del autor fuente (bloqueadas).
- Formulaciones de los PDFs del autor fuente copiadas directamente.

### Etiquetado por eje
`eje:4` para todo el contenido de esta unidad.

### Etiquetado por bloque interno
`bloque:4A` — parámetros.
`bloque:4B` — circuitos.
`bloque:4C` — objetivos y técnicas.
`bloque:4D` — criterio del triángulo (con flag de atribución).
`bloque:4E` — expansores, compuertas, ducking.
`bloque:4F` — limitadores y clippers en mezcla.

### Etiquetado por fase LDOV
- Diagnóstico de dinámica y lectura del GR: `LDOV:Leer`.
- Definición del objetivo y elección del compresor/circuito: `LDOV:Decidir`.
- Ajuste de parámetros y configuración de la compresión: `LDOV:Operar`.
- Verificación con bypass compensado, GR en movimiento correcto, escucha en contexto: `LDOV:Verificar`.

### Teoría mínima vs ampliación opcional

**Teoría mínima obligatoria (prioridad alta):**
- Curva de transferencia: threshold, ratio, knee.
- Ataque como velocidad de llegada (no de espera).
- Makeup desde 0 + comparación compensada.
- Tabla de circuitos analógicos con carácter.
- Objetivos técnicos con orientación de parámetros.
- Criterio del Triángulo con tabla de zonas — con atribución.
- Compresión paralela: principio y uso.
- Compuerta: threshold, hold, filtro de detector.
- Ducking: señal dry como disparo.
- Limitador vs clipper: diferencia fundamental.

**Teoría de precisión útil (prioridad media):**
- Criterios de medición del ataque (63% vs 10/90%).
- Feed-forward vs feedback.
- Detector Peak vs RMS.
- Compresión en serie: tarea por etapa.
- HPF en sidechain: criterio en buses.
- Compresión upward: función y limitación.
- Expansor descendente: escalas de ratio.

**Teoría profunda opcional (IA/FAQ/anexo):**
- THD e IMD en compresores analógicos: tipos de distorsión y su carácter.
- Aliasing en procesadores dinámicos: mecanismo y prevención.
- Curvas de transferencia vintage: no-linealidades específicas de modelos clásicos.
- Configuración de parámetros por instrumento específico: bombo, tambor, voz, bajo, etc.

---

## SECCIÓN 7 — REGLAS PARA GUIONES

### Partes que deben ser demostración

- **Curva de transferencia en tiempo real:** mostrar el GR de un compresor mientras el instrumento suena. Mover threshold y ratio y mostrar el impacto en el movimiento del GR.
- **Ataque y el transitorio percusivo:** mostrar en una batería el efecto de ataque lento (transitorio preservado) vs ataque rápido (transitorio comprimido). La diferencia debe ser claramente audible.
- **Release y bombeo:** producir deliberadamente bombeo con release muy corto en material rítmico para que el alumno identifique el síntoma antes de corregirlo.
- **Makeup y la trampa del nivel:** demostración en vivo de comparación sin compensar vs comparación compensada. Debe mostrarse que la diferencia desaparece cuando se iguala el nivel.
- **Compresión paralela:** mostrar la señal original, la copia comprimida de forma agresiva (en solo), y la mezcla de ambas. La diferencia entre comprimir directo y en paralelo debe ser perceptible.
- **Filtro del detector en compuerta de batería:** mostrar la compuerta sin filtro (el hi-hat dispara la apertura) y con filtro (solo el tambor la dispara).
- **Ducking:** demostración en vivo con voz sobre música. Mostrar el GR del compresor del bus de música moviéndose cuando la voz está activa.
- **Criterio del Triángulo aplicado:** demostrar la diferencia entre empezar con parámetros aleatorios y empezar con los parámetros orientativos del triángulo en un bombo y en una voz.

### Partes que pueden ser explicación a cámara

- Compresión downward vs upward: concepto con gráfico de curva de transferencia.
- Feed-forward vs feedback: concepto con diagrama de señal.
- Circuitos analógicos y su mecanismo de reducción: descripción con diagrama.
- Criterio del Triángulo: presentación del marco con la gráfica del triángulo. Aclarar la atribución en el momento de la presentación.

### Partes que conviene enseñar con sesión real

- Compresión de un kit de batería completo aplicando el Criterio del Triángulo como marco de partida.
- Compresión paralela de batería o de voz: configurar el bus de efectos y ajustar el mix.
- Configuración de compuerta con filtro del detector en una batería con bleed.
- Ducking de música bajo voz con sidechain externo dry.

### Partes que conviene mandar a la capa de apoyo

- THD, IMD y aliasing en compresores: descripción técnica extendida.
- Configuración de parámetros de compresión por instrumento específico (por vacío de cobertura en las fuentes).
- Curvas de transferencia vintage específicas por modelo.
- Comparativa técnica extendida entre modelos de la misma familia.
- Historia de los equipos y sus fabricantes.

---

## SECCIÓN 8 — CAPA DE APOYO POR IA

### Temas que conviene dejar listos para profundización vía IA

- Configuración de parámetros de compresión por instrumento específico: bombo, tambor, overheads, bajo, voz, guitarra eléctrica, guitarra acústica, cuerdas.
- Diferencias técnicas entre modelos específicos de la misma familia (distintas variantes de ópticos, VCAs, FETs).
- THD e IMD en compresores analógicos: qué tipos de distorsión generan y cómo afectan al carácter.
- Aliasing en procesadores dinámicos digitales: mecanismo, condiciones en las que ocurre, prevención.
- Curvas de transferencia no estándar de compresores vintage: descripción de comportamientos no lineales específicos.
- Comparativa entre release automático y manual: cuándo uno es preferible al otro.
- Técnicas avanzadas de sidechain: EQ en sidechain, multiband sidechain.
- Cómo configurar el Criterio del Triángulo para señales con características mixtas (por ejemplo, un bombo que necesita tanto control de pico como sustento).

### Ejemplos de preguntas que el alumno podría hacerle a la IA

- "¿Cómo configuro un compresor en un bombo para aumentar el impacto en lugar de reducirlo?"
- "¿Cuál es la diferencia práctica entre un detector Peak y un detector RMS en un bus de batería?"
- "¿Cómo aplico el Criterio del Triángulo a una voz con mucha variación dinámica entre versos y coros?"
- "Explícame la diferencia en práctica entre un compresor óptico y un FET en una voz principal."
- "¿Cuándo conviene usar compresión en serie en lugar de compresión paralela?"
- "¿Qué parámetros ajusto en la compuerta de un tambor para que no se corte el decay del golpe?"
- "¿Cómo configuro el ducking para que el acompañamiento ceda espacio a la voz sin que el ducking se escuche como tal?"
- "¿Cuándo es mejor usar un clipper que un limitador en un bus de mezcla?"

---

## SECCIÓN 9 — BLOQUES QUE REQUIEREN ATRIBUCIÓN EXPLÍCITA

### Criterio del Triángulo — OBLIGATORIO
El Criterio del Triángulo es un marco desarrollado por Pablo Rabinovich y Pablo Panitta, presentado en AES/CAPER 2023. Su uso en el curso requiere crédito nominativo explícito. No es suficiente un agradecimiento genérico.

**Formulación sugerida para el cuerpo del curso (primera presentación):**
> "Esta subsección se basa en el Criterio del Triángulo, marco de abordaje sistemático de la compresión desarrollado por Pablo Rabinovich y Pablo Panitta, presentado en AES/CAPER 2023."

**Formulación sugerida para el dossier y el RAG:**
> *Basado en el Criterio del Triángulo de Pablo Rabinovich y Pablo Panitta (AES/CAPER 2023).*

**Formulación sugerida para el guión:**
Al presentar el marco en cámara, incluir la frase de atribución antes de explicar el contenido. No al final: la atribución va en el momento de la presentación del marco, no como nota al pie.

### Equipos analógicos — fabricantes
Los modelos de hardware deben referenciarse con atribución a sus fabricantes cuando se introducen:

- LA-2A → Teletronix / Universal Audio (UA).
- 1176 → UREI / Universal Audio (UA).
- API 2500 → API Technologies.
- Fairchild 670 → Fairchild Recording Equipment.
- Manley Variable Mu → Manley Laboratories.
- SSL Bus Compressor → Solid State Logic.
- Neve 33609 / 5254 → AMS Neve.

La doctrina del campo sobre el carácter de cada modelo no requiere atribución al autor fuente; sí nombrar el fabricante original al introducir el equipo.

### PDFs del autor fuente
Los PDF de Procesadores Dinámicos 2022 y Tipos de Compresores son de autoría de Pablo Rabinovich. La doctrina técnica es de dominio general. No requiere atribución cuando se reformula. Si se cita cualquier formulación directa, la cita requiere atribución puntual.

---

## SECCIÓN 10 — CONTINUIDAD CON OTROS EJES

**De dónde viene este eje**
El Eje 4 viene del **Eje 3 — Identidad espectral**.

La señal que llega al Eje 4 tiene ya un carácter tonal definido. El compresor actuará sobre ese carácter: si la señal tiene zonas espectrales incorrectas, el compresor las integrará en su detección y su comportamiento. Una voz con exceso de bajas frecuencias hará que el compresor reaccione desproporcionadamente a esas frecuencias. Por eso el EQ del Eje 3 precede a la compresión del Eje 4.

Cruce con Eje 2: el filtrado del sidechain (HPF en el detector del compresor) es una aplicación funcional de los filtros del Eje 2 al servicio de la compresión del Eje 4. El alumno ya conoce los filtros; aquí se usa ese conocimiento en un nuevo contexto.

Cruce con Eje 3: el EQ dinámico y el de-esser pertenecen al Eje 3 y no se desarrollan en el Eje 4. Si el alumno llega al Eje 4 buscando esas herramientas, la referencia correcta es el Eje 3.

**A qué eje prepara**
El Eje 4 prepara directamente al **Eje 5 — Espacio y perspectiva**.

La compresión controla la energía y el movimiento de la señal en el tiempo. Una vez que la señal tiene su carácter tonal (Eje 3) y su comportamiento dinámico (Eje 4) definidos, el Eje 5 trabaja su posición en el espacio: dónde está en el campo estéreo, a qué distancia percibida, con qué sensación de entorno. La reverb y el delay del Eje 5 actúan sobre señales dinámicamente definidas; si la dinámica no está controlada, los efectos de espacio amplifican los problemas.

**Cruce con Eje 6**
La compresión de bus de salida —el compresor que procesa la mezcla completa— pertenece al Eje 6. El Eje 4 introduce el concepto de compresor de bus como extensión natural de lo aprendido, pero su desarrollo operativo en el contexto de la mezcla global está en el Eje 6.

---

*KENTH Academy — Eje 4 · Versión de producción v1.0*
*Generado desde arquitectura congelada v1.0-final y paquete limpio Eje 4.*
*Criterio del Triángulo: basado en el trabajo de Pablo Rabinovich y Pablo Panitta (AES/CAPER 2023).*
