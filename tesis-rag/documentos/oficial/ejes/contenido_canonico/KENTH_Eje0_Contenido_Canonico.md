# EJE 0 — CAMPO DE DECISIÓN
### KENTH Academy · Mezcla y Masterización · Contenido Final de Curso

---

## SECCIÓN 1 — FUNCIÓN PRÁCTICA DEL EJE

El Eje 0 establece las condiciones mínimas para que cualquier decisión de mezcla sea confiable.

Antes de ecualizar, comprimir o colocar reverb, hay un problema anterior: ¿se puede confiar en lo que se escucha? Si el sistema de monitoreo colorea la señal, la sala refuerza frecuencias que no están en el audio, o la cadena digital tiene pérdidas invisibles, todas las decisiones posteriores se construyen sobre una base falsa.

El eje tiene dos capas funcionales:

**Capa A — Entorno físico:** monitores, sala, auriculares, nivel de escucha. Todo lo que afecta a cómo llega el sonido al oído antes de cualquier decisión.

**Capa B — Cadena digital:** sample rate, bits, decibeles, gain staging. Todo lo que define cómo viaja la señal dentro del sistema sin degradarse.

El Eje 0 no enseña a mezclar. Enseña a construir el campo desde el cual mezclar tiene sentido.

---

## SECCIÓN 2 — QUÉ DEBE PODER HACER EL ALUMNO AL TERMINAR ESTE EJE

Al completar el Eje 0, el alumno es capaz de:

- Evaluar la posición de sus monitores e identificar los problemas más probables derivados de esa posición.
- Reconocer qué tipo de problema acústico tiene su sala (resonancia modal, reflexiones tempranas, exceso de absorción) y qué tipo de tratamiento corresponde a cada caso.
- Decidir cuándo trabajar con monitores y cuándo usar auriculares, y cómo interpretar las diferencias entre ambos sistemas.
- Establecer y mantener un nivel de monitoreo de referencia consistente.
- Configurar una sesión con sample rate y profundidad de bits adecuados al proyecto.
- Entender qué significa cada tipo de dB y usarlos sin confundirlos.
- Distinguir el estándar AES del estándar EBU y configurar el nivel de calibración correcto para plugins de modelado analógico.
- Aplicar el principio de gain staging a la cadena de la sesión.
- Identificar cuándo la cadena digital tiene headroom insuficiente antes de comenzar a procesar.

---

## SECCIÓN 3 — SUBSECCIONES FINALES DEL EJE

Las subsecciones están ordenadas para enseñanza. La capa A precede a la B porque el entorno físico es la condición más inmediata: antes de abrir la DAW, ya existe un sistema de escucha con propiedades fijas.

**CAPA A — ENTORNO FÍSICO**

- **0-A1** · Posicionamiento de monitores
- **0-A2** · Sala: qué se puede y qué no se puede controlar
- **0-A3** · Auriculares como herramienta de trabajo
- **0-A4** · Nivel de monitoreo: consistencia y curvas isofónicas

**CAPA B — CADENA DIGITAL**

- **0-B1** · Sample rate y bits: configuración de la sesión
- **0-B2** · El decibel como unidad de trabajo
- **0-B3** · Gain staging: la lógica de nivel en la cadena

---

## SECCIÓN 4 — CURSO PRINCIPAL DEL EJE

---

### 0-A1 · POSICIONAMIENTO DE MONITORES

**Situación real**
El alumno abre una sesión, escucha que los graves suenan excesivos, y sube el analizador espectral. El analizador muestra un pico en 80 Hz. Decide cortar con el EQ. Al reproducir la mezcla en otro sistema, el bajo desaparece. El problema no era la señal: era la sala reforzando esa frecuencia.

**Explicación operativa**
Los monitores interactúan físicamente con el espacio. La posición determina qué frecuencias se acumulan y cuáles se cancelan en el punto de escucha.

Hay dos efectos principales:

1. **Acumulación por proximidad a paredes.** Las ondas graves se comportan de forma omnidireccional; al rebotar contra una superficie, se suman. El resultado es energía extra en graves que no existe en la señal.

2. **Cancelación por cuarto de longitud de onda.** Al alejarse de la pared, habrá siempre una distancia en la que la reflexión llega en fase opuesta a la señal directa y produce cancelación. No existe posición sin algún compromiso: la tarea es elegir el menos dañino.

**Teoría mínima**
- Pared trasera: +6 dB en graves. Esquina (dos paredes): +12 dB. Rincón (tres paredes): +18 dB.
- Los agudos son más direccionales que los graves. El tweeter debe apuntar al punto de escucha en plano horizontal y vertical.
- En monitores de dos vías, la orientación vertical u horizontal afecta la respuesta en la zona de cruce entre woofer y tweeter. El fabricante especifica la orientación correcta; no es una preferencia estética.
- El desacople mecánico (pads, soportes) evita que las vibraciones del gabinete se transfieran a la mesa y vuelvan como coloración estructural.

**Acción**
1. Verificar que el tweeter quede a la altura de los oídos.
2. Verificar que los monitores apunten al punto de escucha, no al frente.
3. Aumentar la distancia a la pared trasera todo lo que el espacio permita.
4. Comprobar la orientación especificada por el fabricante.
5. Colocar aisladores o pads bajo los monitores si están sobre superficie rígida.
6. Reproducir una mezcla de referencia conocida antes y después de cada ajuste; documentar la diferencia.

**Verificación**
Reproducir ruido rosa. Si hay un abultamiento pronunciado en graves en el punto de escucha, hay acumulación por proximidad o resonancia modal. Ese problema no se resuelve moviendo el EQ del material: se resuelve en la posición o en el tratamiento acústico.

**Error frecuente**
Apoyar los monitores contra la pared para "aprovechar el realce de graves" y luego compensar con EQ en el material. El resultado es una mezcla con graves corregidos para esa sala que sonará delgada en cualquier otro sistema.

---

### 0-A2 · SALA: QUÉ SE PUEDE Y QUÉ NO SE PUEDE CONTROLAR

**Situación real**
El alumno nota que ciertas notas del bajo suenan más fuertes que otras aunque el instrumento esté tocado a nivel uniforme. O escucha que los medios suenan "sucios" sin poder identificar la causa. La sala está coloreando la escucha.

**Explicación operativa**
Toda sala rectangular tiene frecuencias en las que la energía se acumula por reflexiones paralelas entre paredes. A esas frecuencias se las llama resonancias modales o modos de sala. No son ruido: son frecuencias específicas que la sala refuerza o cancela en puntos determinados del espacio.

Existen tres tipos de tratamiento, y no son intercambiables:

- **Paneles absorbentes:** reducen el tiempo que la energía tarda en disiparse (tiempo de reverberación). Tratan primeras reflexiones y exceso de reverberación. No controlan resonancias modales.
- **Resonadores (Helmholtz, de membrana):** diseñados para absorber frecuencias específicas, especialmente en el rango de graves. Son la herramienta para problemas modales.
- **Difusores:** dispersan la energía en distintas direcciones en lugar de absorberla. Reducen la sensación de "sala" sin crear exceso de absorción.

**Teoría mínima**
Las frecuencias modales aproximadas de una sala se calculan con: f = n × (343 / 2L), donde L es la dimensión de la sala en metros y n es un entero. Para una sala de 4 metros de largo: primera moda ≈ 43 Hz. Para 3 metros de ancho: ≈ 57 Hz. Esas frecuencias son exactamente donde la escucha puede estar inflada o cancelada.

**Acción**
1. Reproducir una pista de barrido de frecuencias (sine sweep) o ruido rosa en los monitores.
2. Caminar por la sala y notar dónde el bajo desaparece o se acumula — eso ubica los nodos y antinodos modales.
3. Si no se puede tratar la sala: usar auriculares de referencia con buena extensión en graves para verificar las decisiones en esa zona.
4. No compensar con EQ del material lo que es un problema de la sala.

**Verificación**
Reproducir la misma sección de material en otra ubicación del espacio (automóvil, auriculares, otro sistema). Si el problema desaparece en otro sistema, era la sala, no el audio.

**Error frecuente**
Aplicar tratamiento con espuma acústica de alta densidad en todas las paredes esperando resolver resonancias de sala. La espuma absorbe medios y agudos eficientemente; las resonancias de graves requieren estructuras de mayor masa o resonadores. El resultado es una sala con graves incontrolados y medios/agudos excesivamente muertos: el peor escenario posible para tomar decisiones de mezcla.

---

### 0-A3 · AURICULARES COMO HERRAMIENTA DE TRABAJO

**Situación real**
El alumno mezcla en auriculares cerrados porque no tiene monitores disponibles o el entorno es ruidoso. La mezcla suena equilibrada. Al escucharla en monitores o en otro sistema, los graves son excesivos y la imagen estéreo colapsa.

**Explicación operativa**
Los auriculares y los monitores entregan la señal de manera estructuralmente diferente. En monitores, la señal del canal izquierdo llega también, con un leve retardo y atenuación, al oído derecho (y viceversa). Esa interacción interaural es parte del mecanismo con el que el cerebro procesa la localización espacial.

En auriculares, cada canal llega exclusivamente a su oído. No hay cruce. La imagen estéreo que se percibe en auriculares no coincide con la que se percibe en monitores, aunque el material sea idéntico.

**Teoría mínima**
- Auriculares cerrados: mayor aislación acústica, útiles en grabación. Generan coloración en graves por las resonancias internas del casco. No son la opción recomendada para tomar decisiones de mezcla.
- Auriculares abiertos: menor coloración de grave, menor interacción mecánica con el oído. Mejor translación a monitores. Son el estándar de referencia para mezcla en auriculares.
- La relación de impedancia entre el auricular y la salida del amplificador afecta directamente la respuesta en frecuencia y el control del transductor. Si la impedancia de salida del amplificador es comparable a la del auricular (en lugar de ser significativamente menor), el transductor pierde amortiguamiento: el grave se vuelve impreciso y lento.

**Acción**
1. Para mezcla: usar auriculares abiertos siempre que sea posible.
2. Verificar la especificación de impedancia de los auriculares y de la salida de la interfaz o amplificador. Una relación adecuada implica que la impedancia de salida del amplificador es notablemente menor que la del auricular.
3. No asumir que lo que suena correcto en auriculares cerrados sonará correcto en monitores. Verificar siempre en ambos sistemas antes de dar por terminada una decisión crítica.
4. Usar el crossfeed con criterio: puede mejorar la translación en algunos casos, pero no resuelve estructuralmente el problema de la imagen estéreo en auriculares.

**Verificación**
Reproducir una mezcla de referencia conocida en los auriculares. Si la imagen estéreo se percibe completamente dentro de la cabeza sin naturalidad espacial, los auriculares no son confiables para decisiones de imagen. Complementar con monitores.

**Error frecuente**
Mezclar íntegramente en auriculares cerrados y confiar en que la imagen estéreo percibida será reproducible en monitores. Las posiciones de panoramización que suenan definidas en auriculares pueden colapsar al centro o sonar artificiales en reproducción con altavoces.

---

### 0-A4 · NIVEL DE MONITOREO: CONSISTENCIA Y CURVAS ISOFÓNICAS

**Situación real**
El alumno trabaja a volumen alto y la mezcla le suena con buenos graves y presencia. Al día siguiente la escucha a volumen bajo y nota que los graves desaparecieron. No cambió nada en el material.

**Explicación operativa**
La sensibilidad del oído a distintas frecuencias no es lineal ni constante: varía con el nivel de presión sonora. A bajo volumen, el oído es menos sensible a graves y a agudos extremos. A alto volumen, la curva se aplana y la percepción de graves y agudos se hace más evidente.

Si el nivel de monitoreo cambia entre sesiones o dentro de una misma sesión sin registro, el balance espectral percibido cambia aunque la señal sea idéntica. Las decisiones de mezcla se vuelven inconsistentes.

**Teoría mínima**
Las curvas ISO 226 (actualizadas a partir del trabajo original de Fletcher y Munson) describen este fenómeno. No es necesario memorizarlas: lo que importa operativamente es que a bajo volumen el oído necesita más energía en graves y agudos para percibirlos al mismo nivel que los medios. Una mezcla evaluada solo a alto volumen puede llegar a sonar delgada a niveles de reproducción domésticos.

**Acción**
1. Establecer un nivel de monitoreo de referencia y no abandonarlo durante las decisiones críticas de la sesión.
2. Realizar verificaciones periódicas a bajo volumen para detectar si el balance de graves y agudos se sostiene.
3. Usar una referencia conocida para calibrar la percepción al comenzar cada sesión.

**Verificación**
Reproducir el mismo pasaje a tres niveles distintos: bajo, medio (referencia), alto. Si el balance espectral cambia significativamente, el oído está respondiendo a las curvas isofónicas. La versión a nivel medio es la de referencia para tomar decisiones.

**Error frecuente**
Mezclar a alto volumen durante toda la sesión porque "se escucha mejor el detalle" y no verificar nunca a nivel bajo. El resultado es una mezcla con exceso de graves y agudos que suena agotadora en reproducción normal.

---

### 0-B1 · SAMPLE RATE Y BITS: CONFIGURACIÓN DE LA SESIÓN

**Situación real**
El alumno abre una sesión nueva y le aparece el diálogo de configuración: 44.1 kHz / 48 kHz / 96 kHz / 192 kHz. Y 16 bits / 24 bits / 32 bit float. Necesita saber qué elegir y por qué, sin perder tiempo en teoría que no cambia la decisión.

**Explicación operativa**
El **sample rate** determina cuántas muestras por segundo se toman de la señal. Su efecto práctico más relevante no es la calidad del audio grabado (con SR correcto, la reproducción es exacta hasta el límite de Nyquist), sino el comportamiento de los plugins durante el procesamiento. Los plugins que realizan operaciones no lineales (saturadores, compresores con modelado) pueden generar distorsión inarmónica si operan cerca del límite frecuencial de la sesión. A mayor SR, ese límite se aleja.

Los **bits** determinan la resolución con la que se almacena cada muestra de amplitud. Más bits = más escalones de amplitud = más rango dinámico = menos ruido de cuantización.

La **aritmética de coma flotante** del motor interno de la DAW permite que el procesamiento interno supere 0 dBFS sin generar clipping. El clipping real ocurre al convertir la señal a formato fijo (exportación a 24 o 16 bits, o salida D/A).

**Teoría mínima**
- Sample rate: f_Nyquist = SR ÷ 2. A 44.1 kHz, el límite es 22.05 kHz. A 96 kHz, el límite es 48 kHz.
- Bits: cada bit añade aproximadamente 6 dB de rango dinámico. 16 bits ≈ 96 dB. 24 bits ≈ 144 dB.
- 32 bit float: aritmética interna de la DAW. No hay clipping interno. El clipping se produce en la salida.

**Acción**
1. Sesión de producción y mezcla: 48 kHz o 44.1 kHz (según el destino del proyecto), 24 bits.
2. Si los plugins que se usarán no tienen oversampling propio, considerar 88.2 kHz o 96 kHz para reducir aliasing durante el procesamiento.
3. El motor interno de la DAW opera en 32 o 64 bit float según la aplicación; no se configura: es un atributo del motor.
4. Al exportar: usar el formato y profundidad de bits del destino (CD: 16 bits / 44.1 kHz; streaming: 24 bits / 44.1 kHz o 48 kHz; para mastering: 24 bits al SR del proyecto).
5. Activar oversampling en saturadores y compresores con modelado analógico cuando la CPU lo permita.

**Verificación**
Revisar que la sesión no mezcle archivos grabados a diferentes sample rates. Si la DAW muestra advertencias de conversión de SR, hay fuentes con configuraciones distintas: resolver antes de procesar.

**Error frecuente**
Subir el SR del proyecto creyendo que eso mejora la calidad de archivos ya grabados a SR menor, o que da "más detalle" a la señal. El SR no mejora lo que ya está grabado; solo afecta el comportamiento del procesamiento a partir de ese punto.

---

### 0-B2 · EL DECIBEL COMO UNIDAD DE TRABAJO

**Situación real**
El alumno lee en diferentes fuentes: –18 dBFS, +4 dBu, 0 VU, –20 dBFS. Todos parecen referirse al mismo nivel de trabajo, pero los números son distintos. No entiende la relación entre ellos y no sabe cómo configurar los plugins correctamente.

**Explicación operativa**
El decibel es siempre una relación entre dos valores. Cuando hay una letra adicional (u, FS, V, SPL), indica que esa relación está fijada contra un valor de referencia específico. Cambiar la referencia cambia el número, aunque el nivel físico sea el mismo.

En la cadena de producción musical conviven tres dominios con sus propias referencias:
- **Analógico (voltaje):** dBu (ref: 0,775 V) y dBV (ref: 1 V).
- **Digital:** dBFS (ref: el máximo nivel codificable).
- **Acústico:** dBSPL (ref: 20 μPa, el umbral de audición humana).

El punto donde esos dominios se conectan (el conversor A/D y D/A) no es universal: depende del hardware y del estándar elegido.

**Teoría mínima**
Dos estándares principales definen la relación entre el nivel analógico y el digital:

- **AES RP155:** +4 dBu = –20 dBFS = 0 VU. Máximo headroom analógico: +24 dBu = 0 dBFS.
- **EBU R68:** 0 dBu = –18 dBFS. Máximo headroom: +18 dBu = 0 dBFS.

Un plugin VU calibrado a AES mostrará 0 VU cuando la señal esté a –20 dBFS. El mismo plugin calibrado a EBU mostrará 0 VU a –18 dBFS. Usar el estándar incorrecto desplaza el punto de trabajo del procesador.

Relaciones de uso frecuente:
- Duplicar la potencia: +3 dB.
- Duplicar el voltaje: +6 dB.
- El nivel se percibe como "el doble de fuerte" con un incremento de aproximadamente +10 dB.

**Acción**
1. Al instalar un plugin de modelado analógico, verificar qué estándar de calibración usa (AES o EBU).
2. Configurar el nivel de trabajo de la sesión de acuerdo con ese estándar para que el plugin opere en el punto para el que fue diseñado.
3. Al ver "0 dB" en cualquier medidor, verificar siempre qué referencia está usando ese medidor antes de tomar una decisión.

**Verificación**
Si los plugins de modelado suenan como si estuvieran sobredriveados sin haber superado 0 VU, el problema es probablemente un estándar de calibración incorrecto: el plugin está recibiendo más nivel del que espera.

**Error frecuente**
Asumir que "0 dB" significa lo mismo en todos los contextos. No lo significa. 0 dBFS es el techo digital (cualquier cosa por encima distorsiona en la exportación). 0 dBu es un nivel analógico de referencia modesto. 0 VU puede ser –18 dBFS o –20 dBFS según el estándar. Mezclar estas referencias produce decisiones de nivel sin base confiable.

---

### 0-B3 · GAIN STAGING: LA LÓGICA DE NIVEL EN LA CADENA

**Situación real**
El alumno carga una sesión con 30 tracks, todos con faders a 0 dB. El bus principal está saturado. Empieza a bajar el fader master. La mezcla "se domestica" pero al escucharla más de cerca, los procesadores de cada track están recibiendo señal excesiva y generando distorsión interna. El problema no está en el master: está en cada etapa de la cadena.

**Explicación operativa**
El gain staging es la práctica de gestionar el nivel de señal en cada etapa de la cadena de procesamiento. El objetivo es que cada dispositivo o procesador reciba señal en el rango en el que opera correctamente: con suficiente nivel para estar por encima del piso de ruido, pero sin saturar la entrada.

En una DAW con motor de 32 bit float, no hay clipping interno. Pero eso no significa que el gain staging sea irrelevante:
- Los plugins de modelado analógico se diseñaron para operar en rangos de nivel específicos. Si se les entrega demasiado nivel, el comportamiento del modelado es diferente al esperado (no necesariamente "incorrecto", pero sí diferente al diseño).
- El headroom insuficiente antes del bus final hace que la compresión de pegamento opere con umbrales forzados en lugar de intencionales.
- Un gain staging deficiente en los tracks de origen acumula desequilibrios que se revelan en etapas posteriores.

**Teoría mínima**
El nivel de referencia de trabajo en la sesión (lo que habitualmente se llama el "nivel cómodo" de los tracks antes del procesamiento) se ubica entre –18 y –20 dBFS RMS para señales de contenido sostenido, con headroom de pico suficiente para los transitorios. No es una regla rígida: es un punto de partida.

La lógica de cadena: si el nivel de salida de un plugin es mayor que el nivel de entrada, se acumula ganancia a lo largo de la cadena. Si cada track llega al bus con más nivel del necesario, el fader del bus necesita compensar en lugar de controlar.

**Acción**
1. Antes de empezar a procesar, ajustar el nivel de los clips o el gain de entrada de los tracks para que los instrumentos más densos promedien entre –18 y –20 dBFS RMS.
2. Al agregar cada procesador, verificar que el nivel de salida del procesador sea comparable al de entrada; ajustar el output gain del plugin si es necesario.
3. No compensar todo con el fader del master: el problema de gain staging está en los tracks y en los buses, no en el fader final.

**Verificación**
Con todos los faders en 0 dB y sin procesadores, el bus principal no debe estar saturado. Si ya hay señal excesiva antes de procesar, el problema es de nivel de clip o de nivel de fader de cada track.

**Error frecuente**
Dejar todos los faders a 0 dB y "solucionar" el exceso de nivel bajando el master al final. Eso no resuelve el problema: los procesadores de cada track ya están recibiendo señal incorrecta y operando fuera de su rango de diseño.

---

## SECCIÓN 5 — DOSSIER CANÓNICO DE APOYO

El dossier es material de consulta técnica. No está diseñado para ser leído de corrido: sirve para verificar un concepto, resolver una duda técnica o profundizar un punto específico.

---

### ACÚSTICA Y MONITOREO

**Reflexiones en graves y posición de monitores**
Las ondas de frecuencias bajas tienen longitudes de onda largas y se comportan de forma omnidireccional en espacios pequeños. Al acercarse una fuente a una superficie paralela, la reflexión suma energía al sonido directo. La acumulación es aproximadamente: pared simple +6 dB, unión de dos paredes +12 dB, esquina de tres paredes +18 dB, en la frecuencia donde la reflexión llega en fase con la directa.

Al alejarse de la pared, existe una distancia en la que la reflexión llega desfasada 180° (λ/4) y produce cancelación. El efecto es un peine de frecuencias afectadas (comb filtering) que varía con la posición. No existe posición sin compromiso.

**Resonancias modales**
Las dimensiones de una sala rectangular determinan frecuencias en las que las reflexiones entre superficies paralelas se refuerzan constructivamente. La primera frecuencia modal de un eje es f = 343 / (2 × L), donde L es la distancia entre las dos superficies paralelas en metros. Los modos afectan la reproducción de frecuencias graves y son la causa principal de inconsistencia en las decisiones de mezcla en esa zona.

Herramienta de diagnóstico: generador de barrido de frecuencias (sine sweep) + medición en el punto de escucha. Herramienta de corrección: resonadores sintonizados o difusores de baja frecuencia. Los paneles de espuma no corrigen resonancias modales.

**Auriculares: impedancia y amortiguamiento**
El factor de amortiguamiento (damping factor) del transductor depende de la relación entre la impedancia de salida del amplificador y la impedancia del transductor. Si la impedancia de salida del amplificador es comparable (o mayor) a la del auricular, el control del movimiento del transductor se reduce y el grave pierde precisión. La relación recomendada es que la impedancia de salida del amplificador sea al menos 8 veces menor que la del auricular.

**Curvas ISO 226**
Las curvas de igual sonoridad (ISO 226, actualizadas a partir de Fletcher-Munson 1933) describen los niveles de presión sonora necesarios a cada frecuencia para producir la misma percepción de intensidad. A bajo SPL, el oído requiere más energía en graves (por debajo de 500 Hz) y en agudos (por encima de 8 kHz) para percibirlos con la misma intensidad que los medios. A alto SPL, la diferencia se reduce. Consecuencia práctica: las decisiones de balance espectral tomadas a un nivel de monitoreo no son directamente válidas a otro nivel distinto.

---

### CADENA DIGITAL

**Sample rate y aliasing**
El teorema de Nyquist-Shannon establece que para reconstruir correctamente una frecuencia f es necesario al menos 2 muestras por ciclo, es decir, un sample rate mínimo de 2f. Cualquier frecuencia mayor que f_Nyquist = SR/2 que llegue al conversor produce aliasing: una frecuencia inarmónica falsa dentro de la banda útil. El aliasing no es filtrable a posteriori.

El oversampling en plugins procesa la señal internamente a una frecuencia mayor y luego la reduce, evitando que las operaciones no lineales (rectificación, saturación, compresión con modelado) generen aliasing en la banda de audio útil.

**Profundidad de bits**
Cada bit de profundidad añade aproximadamente 6,02 dB de rango dinámico (de forma más precisa: RD ≈ 6,02 × n + 1,76 dB, donde n = número de bits). La diferencia práctica entre 16 y 24 bits no es lineal: 24 bits ofrece 256 veces más escalones de amplitud que 16 bits. El ruido de cuantización en 24 bits está por debajo del umbral de audición en cualquier contexto de producción musical.

**Coma fija y coma flotante**
Los conversores A/D y D/A operan en coma fija: cada muestra ocupa una posición fija en la grilla de cuantización. El motor interno de la DAW opera en coma flotante (32 o 64 bit según la aplicación): el valor se representa con mantisa y exponente, lo que permite cubrir un rango dinámico mucho mayor sin límite de clipping interno. El clipping real ocurre en la conversión D/A o al exportar a formato fijo (24 o 16 bits).

**Estándares de calibración**
| Estándar | Relación |
|---|---|
| AES RP155 | +4 dBu = –20 dBFS = 0 VU |
| EBU R68 | 0 dBu = –18 dBFS |

La diferencia práctica: en AES, hay 20 dB de headroom entre el nivel de referencia y el techo digital. En EBU, hay 18 dB. Al usar plugins de modelado analógico, identificar qué estándar aplica el plugin determina en qué rango de dBFS debe trabajar la señal para que el modelado opere correctamente.

**Niveles de señal en producción**
| Tipo de señal | Nivel típico |
|---|---|
| Micrófono | desde –60 dBu |
| Instrumento (Hi-Z pasivo) | intermedio, variable |
| Línea profesional | +4 dBu (≈ 1,23 V rms) |
| Línea semiprofesional | –10 dBV (≈ 0,316 V rms) |

La diferencia entre +4 dBu y –10 dBV es de aproximadamente 11,8 dB. Conectar equipo semiprofesional a una entrada calibrada para +4 dBu deja la señal enterrada en el piso de ruido. Conectar equipo profesional a una entrada de –10 dBV puede saturar la entrada.

---

## SECCIÓN 6 — REGLAS PARA RAG

### Qué indexar

- Toda la doctrina técnica de posicionamiento de monitores (efectos de pared, λ/4, desacople).
- Taxonomía de tratamiento acústico (absorbentes, resonadores, difusores) con criterio de uso.
- Problema estructural de auriculares (ausencia de interacción interaural) y limitaciones de crossfeed.
- Relación impedancia auricular/amplificador y su efecto en el damping del transductor.
- Curvas ISO 226: descripción funcional y consecuencia práctica en el nivel de monitoreo.
- Sample rate: f_Nyquist, aliasing, oversampling — con criterio operativo.
- Profundidad de bits: rango dinámico, coma fija vs flotante — con criterio operativo.
- Tipos de dB referenciado y sus referencias absolutas.
- Estándares AES RP155 y EBU R68 con tabla de equivalencias.
- Niveles de señal por tipo (mic, instrumento, línea pro, línea semipro).
- Principio de gain staging: función y objetivo.

### Qué no indexar

- Anécdotas, ejemplos personales o formulaciones orales del autor fuente.
- Contenido sobre medidores de nivel (VU, RMS, Peak, K-System): pertenece a Eje 1.
- Configuración y uso del analizador espectral: pertenece a Eje 1.
- Gain staging por elemento/procesador individual: pertenece a Eje 2.
- Routing básico de sesión en DAW: pertenece al cierre de Eje 0-B en el curso pero su profundización operativa corresponde a Eje 2.

### Etiquetado por eje
`eje:0` para todo el contenido de esta unidad.

### Etiquetado por capa interna
`capa:0A` — entorno físico (monitores, sala, auriculares, nivel).
`capa:0B` — cadena digital (SR, bits, dB, gain staging).

### Etiquetado por fase LDOV
- Contenido de posicionamiento y diagnóstico de sala: `LDOV:Leer`
- Contenido de selección de SR, bits y estándar de calibración: `LDOV:Decidir`
- Procedimientos de posicionamiento, configuración de sesión, calibración: `LDOV:Operar`
- Verificaciones con ruido rosa, referencias cruzadas de sistema a sistema: `LDOV:Verificar`

### Teoría mínima vs ampliación opcional
**Teoría mínima obligatoria (indexar con prioridad alta):**
- Efectos de pared en graves.
- f_Nyquist = SR/2.
- Bits = resolución de amplitud.
- Tabla de tipos de dB referenciado.
- Tabla AES/EBU.
- Definición funcional de gain staging.

**Teoría de precisión útil (indexar con prioridad media):**
- Coma fija vs flotante.
- Impedancia auricular/amplificador.
- Cálculo aproximado de frecuencias modales.
- Oversampling: cuándo activarlo.

**Teoría profunda opcional (para IA/FAQ/anexo):**
- Fórmula detallada de RD por bits.
- Curvas ISO 226 con valores numéricos por frecuencia.
- Tipos de resonadores con especificaciones de diseño.
- Diferencias técnicas entre tipos de crossfeed.

---

## SECCIÓN 7 — REGLAS PARA GUIONES

### Partes que deben ser demostración

- **Posicionamiento de monitores:** mostrar en cámara o con representación visual el triángulo equilátero de escucha, el eje de tiro del tweeter, la distancia a las paredes, y los aisladores bajo los monitores.
- **Problema de sala:** reproducir audio en el espacio y recorrerlo físicamente para que el alumno pueda ver la diferencia de percepción según la posición en la sala.
- **Auriculares vs monitores:** reproducir el mismo pasaje en ambos sistemas y señalar las diferencias de imagen estéreo y respuesta de graves.
- **Aliasing en plugins:** demostración auditiva y visual (espectrograma) de plugin no lineal sin oversampling vs con oversampling a diferentes SR.
- **Estándar de calibración en plugin:** mostrar en pantalla la diferencia entre un plugin configurado a AES y el mismo a EBU con el mismo nivel de señal de entrada.
- **Gain staging:** sesión real con tracks a nivel excesivo vs sesión con gain staging aplicado; comparar el headroom disponible en el bus antes de procesar.

### Partes que pueden ser explicación a cámara

- Curvas isofónicas: descripción del fenómeno y consecuencia práctica. No requiere demostración visual compleja.
- Tipos de tratamiento acústico: diferencias entre paneles, resonadores y difusores.
- Tipos de dB: tabla de referencias con breve explicación de cada unidad.
- Coma fija vs flotante: concepto.

### Partes que conviene enseñar con sesión real

- Configuración de una sesión nueva: elección de SR y bits según el destino del proyecto.
- Ajuste de nivel de clips antes de empezar a procesar (gain staging inicial de sesión).
- Identificación de qué estándar usa un plugin de modelado y cómo ajustar el nivel de trabajo.

### Partes que conviene mandar a la capa de apoyo

- Fórmulas de decibeles (potencia vs voltaje): el alumno debe conocer la diferencia; el desarrollo matemático completo va al dossier.
- Cálculo de frecuencias modales: el concepto va en el curso; la fórmula y el procedimiento de cálculo detallado van al dossier y a la IA.
- Tipos de resonadores y su diseño: solo se nombran en el curso; el desarrollo técnico completo es para la capa de apoyo.
- Diferencias técnicas entre tipos de auriculares (impedancias específicas por modelo, respuestas en frecuencia comparadas): dossier y IA.

---

## SECCIÓN 8 — CAPA DE APOYO POR IA

### Temas que conviene dejar listos para profundización vía IA

- Cálculo detallado de frecuencias modales a partir de las dimensiones de la sala del alumno.
- Evaluación de la relación impedancia auricular/amplificador con los datos del hardware específico del alumno.
- Comparación técnica entre distintos pares de auriculares de referencia para mezcla.
- Desarrollo matemático completo de las fórmulas de dB (potencia, voltaje).
- Diferencias entre los distintos tipos de crossfeed y cuándo tiene sentido activarlo.
- Cálculo del rango dinámico teórico para distintas profundidades de bits.
- Guía para estimar el SR óptimo de proyecto según los plugins que el alumno usa.
- Ampliación sobre las curvas ISO 226 con valores numéricos.
- Diferencias técnicas entre tipos de tratamiento acústico (materiales, coeficientes de absorción).

### Ejemplos de preguntas que el alumno podría hacerle a la IA

- "Mi sala mide 4 metros de largo, 3 metros de ancho y 2,5 metros de alto. ¿Cuáles son las frecuencias modales principales que debo considerar?"
- "Tengo unos auriculares de 250 Ω y mi interfaz tiene 30 Ω de impedancia de salida. ¿Cómo afecta esto al sonido?"
- "¿Cuándo conviene trabajar a 88.2 kHz en lugar de 44.1 kHz?"
- "Explícame la diferencia entre el AES RP155 y el EBU R68 en términos prácticos."
- "Tengo espuma acústica en todas las paredes y sigo teniendo problemas de bajo. ¿Qué pasa?"
- "¿Qué significa que la DAW trabaje en 32 bit float si igual puedo saturar al exportar?"
- "¿Cómo calibro un plugin VU para que funcione correctamente con mi nivel de trabajo?"
- "¿Qué auriculares abiertos son buena referencia para mezcla en un rango de precio accesible?"

---

## SECCIÓN 9 — BLOQUES QUE REQUIEREN ATRIBUCIÓN EXPLÍCITA

El contenido del Eje 0 es en su totalidad doctrina técnica de dominio general (física acústica, DSP, normas publicadas). No existe en este eje ningún bloque que requiera atribución al autor fuente.

Las referencias a estándares se citan como documentos normativos:

- AES RP155: "según norma AES RP155"
- EBU R68: "según norma EBU R68"
- Curvas de igual sonoridad: "curvas ISO 226 (Fletcher-Munson)"
- Teorema de Nyquist-Shannon: "teorema de Nyquist-Shannon"

Si en materiales de apoyo se cita directamente alguna formulación o documento del autor fuente, esa cita requiere atribución puntual. No afecta al cuerpo principal del curso.

---

## SECCIÓN 10 — CONTINUIDAD CON OTROS EJES

**De dónde viene este eje**
El Eje 0 es el punto de entrada del curso. No tiene un eje anterior. Es la condición de posibilidad de todo lo que sigue.

**A qué eje prepara**
El Eje 0 prepara directamente al **Eje 1 — Lectura de señales**.

El cruce funciona así:
- El Eje 0 establece que la cadena de escucha y la cadena digital son confiables.
- El Eje 1 enseña a usar los instrumentos de medición (analizador espectral, medidores de nivel, goniómetro, correlatómetro) sobre esa cadena calibrada.

Sin el Eje 0, las lecturas del Eje 1 carecen de base: el alumno no sabe si lo que mide es real o es un artefacto de su sistema.

**Nota de transición para el alumno**
Los instrumentos de medición (VU, RMS, Peak, K-System, analizador espectral) no se desarrollan en el Eje 0. Se introducen en el Eje 1. La razón: antes de aprender a leer, hay que tener un sistema de lectura confiable. El Eje 0 construye ese sistema. El Eje 1 lo pone a trabajar.

---

*KENTH Academy — Eje 0 · Versión de producción v1.0*
*Generado desde arquitectura congelada v1.0-final y paquete limpio Eje 0.*
