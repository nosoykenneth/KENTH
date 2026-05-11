---
axis_id: "Eje 3"
axis_number: 3
axis_title: "Eje 3 - Identidad espectral"
doc_layer: "limpio"
doc_type: "operacion_practica"
source_origin: "course"
status: "ready_for_indexing"
language: "es"
allowed_for_indexing: true
---

# EJE 3 — IDENTIDAD ESPECTRAL
## Extracción Forense KENTH Academy

---

## 1. COBERTURA DEL EJE

**Fuentes que lo alimentan directamente:**

| Fuente | Contenido relevante para Eje 3 |
|---|---|
| Clases 13–15 (Mezcla) | EQ Peak, Shelving, Q, Q constante vs proporcional, simétrico vs asimétrico, gráficos, semiparamétrico, paramétrico, modelos analógicos (API, Neve, SSL, Pultec), EQ dinámico vs multibanda, de-esser |
| PDF: Apunte Ecualizadores 2020 | Peak/Bell, Shelving, parámetros, Q, BW, tipos de EQ, gráficos, semiparamétrico, paramétrico |
| Clase 14 (Mezcla) | SSL E y G (canal completo, split, sidechain de EQ a dinámica), Pultec EQP-1A y MQ-5, distorsión armónica, THD |
| Clase 7 (Mezcla) | Introducción diferenciada entre EQ tonal y correctivo; Pultec como "ecualizador de realce" vs EQ correctivo |
| Clase 15 (Mezcla) | EQ dinámico (FabFilter Pro-Q 4), comparación con multibanda, de-esser |
| Temario fuente (Módulo XIII) | Lista canónica: Peak, Shelving, Gráficos, Semiparamétrico, Paramétrico, Q constante/proporcional, Simétrico/asimétrico, EQ dinámico, Modelado analógico |

**Partes dislocadas desde otros bloques del curso fuente:**

En el temario fuente, el **EQ dinámico** aparece listado dentro del Módulo XIII junto con los demás ecualizadores, y la compresión multibanda en Módulo XIV. En KENTH, el EQ dinámico permanece en Eje 3 (herramienta espectral), mientras la compresión multibanda va a Eje 4. Esa división es propia de KENTH y no replicar el orden del temario fuente.

La **técnica de barrido de frecuencia** (sweep) para detección de problemas aparece como parte del uso del semiparamétrico; en KENTH pertenece a la práctica de EQ correctivo dentro del Eje 3, no como técnica de análisis del Eje 1.

El contenido de **de-esser** en el curso fuente está en Módulo XIV (procesadores dinámicos). En KENTH, su lógica es la del EQ dinámico aplicado a una banda específica, por lo que pertenece al cierre del Eje 3 o al inicio del Eje 4 según el enfoque de la redacción.

---

## 2. MATRIZ NEUTRA DEL EJE

### BLOQUE A — PARÁMETROS Y TIPOLOGÍA DE EQ

| # | Tema | Subtema | Concepto técnico | Definición neutra | Fórmula / Relación | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|---|
| 3A-01 | EQ Peak / Bell | Parámetros | Frecuencia central (fc) | Punto de máxima ganancia o atenuación de una campana. Se calcula como la media geométrica de las frecuencias de corte inferior y superior del filtro | fc = √(f1 × f2) | La fc no es la media aritmética de los extremos del ancho de banda; es la media geométrica. Dos ecualizadores con la misma fc marcada pueden no actuar exactamente en esa frecuencia si tienen distinto diseño | En la práctica la fc se ajusta con el oído, no con la calculadora; conocer la fórmula sirve para interpretar correctamente lo que muestra la interfaz | Calcular la fc como (f1+f2)/2 y asumir que todos los EQs actúan exactamente en la frecuencia marcada | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3A-02 | EQ Peak / Bell | Parámetros | Ancho de banda (BW) y Q | El ancho de banda es la separación entre las dos frecuencias donde la curva cae 3 dB respecto a la ganancia máxima. Q es la frecuencia central dividida entre el ancho de banda: Q alto → campana estrecha y selectiva; Q bajo → campana ancha y suave | Q = fc / BW = fc / (f2 – f1) | Q y pendiente no son lo mismo. Q afecta principalmente la forma de la parte superior de la curva. La pendiente de las laderas de la campana depende del diseño del filtro | Un EQ con pendiente fija a 12 dB/oct puede parecer que el Q "es" la pendiente; no es así: solo opera dentro de una pendiente fija. Si el EQ permite cambiar la pendiente independientemente del Q, son dos variables distintas | Confundir Q con pendiente de filtro, o creer que subir el Q siempre endurece la pendiente | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3A-03 | EQ Peak / Bell | Tipos de Q | Q constante vs Q proporcional a la ganancia | Q constante: la forma de la curva no cambia al modificar la ganancia. Q proporcional: a mayor ganancia aplicada, el Q aumenta (la parte superior de la campana se estrecha). Muy común en ecualizadores analógicos | — | El Q proporcional hace que el ecualizador sea más suave a ganancias pequeñas y más selectivo a ganancias grandes; es perceptualmente más musical en muchos contextos. El Q constante es más predecible y quirúrgico | El API 550 y la mayoría de los analógicos clásicos trabajan con Q proporcional; el comportamiento es más suave que lo que marca la perilla | Esperar un comportamiento simétrico entre +3 dB y +9 dB en un ecualizador analógico con Q proporcional | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3A-04 | EQ Peak / Bell | Tipos de respuesta | Simétrico vs asimétrico | Un EQ simétrico tiene la misma forma de curva para boost y cut a igual ganancia absoluta: cortar −6 dB y subir +6 dB produce curvas especulares. Un EQ asimétrico tiene formas distintas para boost y cut. Muchos analógicos son asimétricos | — | En EQ asimétrico, la curva de corte suele ser más estrecha y selectiva que la de boost; esto tiene sentido musical: para corregir conviene precisión, para dar color conviene suavidad | Un EQ asimétrico con boost amplio y cut estrecho permite agregar carácter con una mano mientras corrige con la otra, sin que ambas operaciones tengan el mismo impacto en las frecuencias adyacentes | Esperar que boost y cut en un analógico produzcan curvas perfectamente simétricas | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3A-05 | EQ Shelving | Parámetros | Frecuencia de corte del shelving | En un shelving, la frecuencia de corte puede interpretarse de dos maneras: (a) el punto donde la curva alcanza la mitad de la ganancia asignada (convención digital frecuente), o (b) el punto 3 dB por debajo del valor máximo del estante (convención analógica frecuente). Las dos no coinciden | Convención digital: fc = punto donde se alcanza ganancia/2 · Convención analógica: fc = punto a –3 dB del estante | Verificar cómo define la fc el plugin antes de asumir que la acción comienza exactamente en esa frecuencia. Un shelving a 100 Hz con +10 dB puede estar en +5 dB en 100 Hz | En un shelving de graves con +10 dB ajustado en 100 Hz, la zona de 200–300 Hz también recibe ganancia significativa; ignorar esto puede engordar el espectro en una zona no deseada | Asumir que la ganancia del shelving está completamente a la izquierda de la frecuencia marcada, sin afectar nada por encima | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3A-06 | EQ Shelving | Resonancia | Shelving resonante | Algunos ecualizadores shelving permiten añadir resonancia en torno a la frecuencia de corte, generando un pico antes del estante. El punto de resonancia puede usarse para enfatizar selectivamente una zona dentro de la banda afectada por el shelving | — | Útil en graves para combinar peso general y énfasis selectivo en una zona específica (p.ej., bombo). En agudos, la resonancia tiende a volverse artificial rápidamente; usarla con moderación | El pico de resonancia crea un descenso inmediatamente después; esa "sombra" genera percepción de contraste que hace sonar más enfatizado el pico | Aplicar resonancia en shelving de agudos con la misma agresividad que en graves | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3A-07 | EQ Gráfico | Clasificación | Ecualizador gráfico (bandas fijas) | El fabricante determina las frecuencias centrales y el ancho de banda de cada banda; el usuario solo controla la ganancia. Se divide en bandas de octava, media octava o 1/3 de octava. A mayor número de bandas, mayor resolución espectral | Gráfico de octava ISO: 31,5 – 63 – 125 – 250 – 500 Hz – 1k – 2k – 4k – 8k – 16 kHz | Más bandas = más resolución pero mayor interacción entre bandas adyacentes. El gráfico de octava es el más musical y de curvas más suaves | El gráfico de octava no permite mover una sola frecuencia sin afectar las adyacentes; mover una fader afecta un tramo completo del espectro | Creer que un gráfico de octava ofrece el mismo control selectivo que un paramétrico | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3A-08 | EQ Semiparamétrico | Características | Semiparamétrico (barrido) | Dos controles: selección de frecuencia central (continua dentro de un rango) y ganancia/atenuación. No tiene control de Q. Se usa como "ecualizador de barrido" para localizar problemas espectrales | — | La técnica de barrido: subir la ganancia y recorrer el espectro escuchando qué zona molesta; una vez localizada, reducir la ganancia para cortar en ese punto | El semiparamétrico es suficiente para la mayoría de las intervenciones de color en una consola; el Q fijo del fabricante está elegido para ser musical en el contexto | Intentar hacer correcciones quirúrgicas con un semiparamétrico cuando se necesitaría un Q más estrecho | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3A-09 | EQ Paramétrico | Características | Paramétrico completo | Tres controles: frecuencia, ganancia y Q (ancho de banda). El más versátil: sirve tanto para corrección quirúrgica como para color musical. Permite ajustes muy precisos en cualquier zona del espectro | — | Para EQ correctivo de alta precisión, preferir el paramétrico. Para color musical amplio, también funciona bien con Q bajo. Es el EQ más adecuado cuando se sabe exactamente qué problema se quiere abordar | El paramétrico es la herramienta de elección cuando hay que resolver un problema específico; los analógicos clásicos son la elección cuando se quiere imprimir carácter sin necesitar precisión quirúrgica | Usar siempre el EQ más sofisticado disponible asumiendo que más control equivale a mejor resultado | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE B — CRITERIO DE DECISIÓN: CORRECTIVO VS ESTÉTICO

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|
| 3B-01 | Criterio | Correctivo | EQ correctivo | Intervención que elimina o atenúa un elemento no deseado o problemático en la señal: resonancias, problemas de registro, enmascaramiento excesivo. Tiende a ser sustractivo, selectivo (Q relativamente alto) y localizado | Intervenir cuando un elemento específico del espectro interfiere con la claridad del instrumento o con la mezcla. Verificar con bypass antes y después | Una corrección bien ejecutada puede ser invisible al oído (no se nota la ausencia de lo que se eliminó) | Hacer EQ correctivo en solo del instrumento sin verificar que el problema se percibe también en el contexto de la mezcla | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3B-02 | Criterio | Estético | EQ estético / tonal | Intervención que modifica el carácter tonal del instrumento o la mezcla de forma deliberada: agregar peso, brillo, calidez, presencia, apertura. Tiende a ser aditivo, más amplio (Q bajo), y puede realizarse con EQ analógico de carácter | Intervenir cuando el instrumento necesita una identidad tonal más clara en el contexto de la mezcla, no solo para eliminar un problema | El EQ aditivo con Q bajo afecta una zona amplia del espectro; en analógicos clásicos, insertar el ecualizador (aunque sea a ganancia 0) ya puede añadir coloración por distorsión armónica | Aplicar EQ aditivo esperando el mismo resultado que con corrección sustractiva, o no verificar el nivel de salida tras aplicar ganancia | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3B-03 | Criterio | Escucha | EQ en contexto vs en solo | El EQ correctivo puede decidirse en solo; el EQ estético requiere el contexto de la mezcla para validarse. Una zona que suena "mal" en solo puede ser exactamente correcta dentro de la mezcla porque otro instrumento la cubre o porque define el carácter del conjunto | Verificar cualquier decisión de EQ en el contexto de la mezcla, especialmente cuando el resultado suena exagerado en solo | Si al apagar y encender el EQ el cambio no se percibe en la mezcla, o se percibe solo como cambio de nivel, el ajuste puede no ser necesario o puede resolverse con fader | Hacer EQ exhaustivo de cada instrumento en solo y asumir que la suma de todos esos EQ producirá una buena mezcla | HEURÍSTICA OPERATIVA REFORMULABLE | REFORMULAR MÁS |
| 3B-04 | Criterio | Técnica de barrido | Barrido para localización de problemas | Técnica para detectar resonancias o zonas problemáticas: aplicar ganancia elevada en una campana de Q alto y recorrer el espectro mientras el instrumento suena, hasta identificar la frecuencia que molesta o se destaca negativamente; luego cortar en esa zona | — | Usar ganancia positiva para detectar, luego revertir a negativa para cortar. El oído detecta mejor el exceso que la falta | El barrido con boost exagerado también puede identificar zonas que conviene realzar musicalmente | Bajar el fader del instrumento mientras se hace el barrido, perdiendo el contexto de nivel real en el que va a operar el EQ | HEURÍSTICA OPERATIVA REFORMULABLE | REFORMULAR MÁS |
| 3B-05 | Criterio | Ilusión de nivel | EQ aditivo y falsa mejora por nivel | Insertar un ecualizador con ganancia positiva (o incluso sin moverlo, solo por coloración del circuito) puede hacer que la señal suene "mejor" simplemente porque sonó más fuerte. La percepción auditiva favorece el nivel más alto cuando la diferencia es pequeña | — | Siempre comparar con bypass compensando el nivel percibido. Si el bypass compensado suena igual, el EQ no estaba mejorando nada: solo subiendo el volumen | Un ecualizador aditivo a +2–3 dB puede dar ilusión de "mejora" que desaparecería si se compensara el nivel | Aprobar el resultado de un EQ sin compensar el nivel al comparar con bypass | HEURÍSTICA OPERATIVA REFORMULABLE | REFORMULAR MÁS |

---

### BLOQUE C — MODELADO ANALÓGICO

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|
| 3C-01 | Modelado analógico | THD y distorsión | Distorsión armónica como carácter | El modelado analógico no solo emula la curva de ecualización del hardware original; también modela la distorsión armónica (THD) y el comportamiento no lineal de los componentes originales. Segundo armónico: percepción cálida, musical. Tercer armónico: percepción más brillante y agresiva | — | El nivel de entrada al plugin de modelado afecta la cantidad de distorsión generada; calibrar según estándar AES o EBU para operar en el punto de trabajo correcto del modelo | Insertar un modelado analógico sin calibrar el nivel de entrada equivale a usar el hardware original con la señal demasiado fuerte o demasiado débil | Usar el mismo nivel de entrada para todos los plugins de modelado sin verificar el estándar de calibración de cada uno | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3C-02 | Modelado analógico | Perillas nominales | Divergencia entre valor marcado y respuesta real | En equipos analógicos y sus modelados, el valor impreso en el panel (frecuencia, ganancia) no siempre coincide exactamente con lo que el circuito hace. Es parte intrínseca del comportamiento analógico | — | No ecualizar leyendo números como si fueran una verdad matemática cerrada; usar el oído como árbitro. Las frecuencias nominales son una referencia, no una certeza | Dos plugins que modelan el mismo equipo de distintos desarrolladores pueden sonar diferente: el modelado incluye decisiones de interpretación del comportamiento del hardware | Calibrar frecuencias del EQ analógico esperando el mismo resultado que con un paramétrico digital transparente | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3C-03 | Modelado analógico | API 550A | API 550A: características | Ecualizador de tres bandas con frecuencias fijas por pasos, HPF incorporado, Q proporcional. Carácter: presencia pronunciada en medios, graves con mucho impacto. Frecuencias graves: 100, 200 Hz; medios: 500, 1k, 2k, 3k Hz; agudos: 5, 8, 10, 12, 16 kHz | — | Usar cuando se busca un sonido de medios presentes y graves con impacto; ideal para batería, guitarras, voces con carácter frontal | El API 550A tiene solo tres bandas pero las frecuencias cubren muy bien los puntos críticos de los instrumentos más comunes en mezcla | Esperar el mismo resultado del 550A y el 550B: son distintos en arquitectura y comportamiento tonal | MÉTODO O CONTENIDO ATRIBUIBLE | USAR CON ATRIBUCIÓN |
| 3C-04 | Modelado analógico | API 550B | API 550B: características | Ecualizador de cuatro bandas con más frecuencias disponibles que el 550A, mayor selectividad. Misma familia tonal pero con más opciones de ajuste | — | Usar cuando se necesita más flexibilidad de frecuencia dentro del carácter API; la cuarta banda permite intervenciones adicionales sin cambiar la firma tonal | El 550B tiene una banda más pero sigue siendo API: seguirá sonando marcadamente en medios y graves comparado con otras familias | Intercambiar 550A y 550B esperando resultados idénticos por tener el mismo nombre de familia | MÉTODO O CONTENIDO ATRIBUIBLE | USAR CON ATRIBUCIÓN |
| 3C-05 | Modelado analógico | API 560 | API 560: ecualizador gráfico de 10 bandas | Gráfico de una octava con diez bandas y carácter API muy presente. Muy efectivo en batería, guitarras y voces cuando se busca carácter marcado sin precisión paramétrica | — | Usar para imprimir carácter amplio de firma; no para correcciones quirúrgicas. La resolución de octava no permite precisión pero sí imprime el timbre API de forma consistente | Un gráfico de firma fuerte como el 560 puede hacer más en timbre con pocos movimientos que muchas intervenciones de paramétrico transparente | Usar el 560 como sustituto de un paramétrico cuando se necesita resolución espectral fina | MÉTODO O CONTENIDO ATRIBUIBLE | USAR CON ATRIBUCIÓN |
| 3C-06 | Modelado analógico | Neve 1073 | Neve 1073: características | Tres bandas + HPF. Graves solo en shelving; frecuencias: 35, 60, 110, 220 Hz (shelving). Medios: semiparamétrico. Agudos: shelving. Carácter: agudos sedosos, graves con empuje denso pero menos impacto directo que API | — | Usar cuando se busca musicalidad sin agresividad: batería con cuerpo suave, voces con brillo sin navaja, instrumentos de cuerdas, mezclas con rango dinámico amplio | Las frecuencias de 60, 110 y 220 Hz en la sección de graves del 1073 son características muy reconocibles del sonido Neve | Esperar de un Neve el mismo tipo de impacto en medios que de un API: son familias opuestas en ese aspecto | MÉTODO O CONTENIDO ATRIBUIBLE | USAR CON ATRIBUCIÓN |
| 3C-07 | Modelado analógico | Neve 1084 / 1081 | Neve 1084 y 1081: variantes extendidas | El 1084 añade LPF, más opciones de frecuencia en agudos (10, 12, 16 kHz), botón High Q que convierte el medio en Q proporcional. El 1081 es la versión de cuatro bandas full paramétrico. Mismo carácter Neve con más flexibilidad | — | Usar el 1084 cuando se necesita la firma Neve con mayor control; el botón High Q transforma la dinámica de trabajo de la banda de medios | La posibilidad de bypass por banda en algunos modelos Neve es una ventaja operativa: permite comparar el efecto de cada banda aisladamente | Asumir que 1073, 1084 y 1081 suenan idéntico por ser de la misma marca y familia tonal | MÉTODO O CONTENIDO ATRIBUIBLE | USAR CON ATRIBUCIÓN |
| 3C-08 | Modelado analógico | SSL E y G | SSL E y G: canal completo con split | El canal SSL incluye EQ + dinámica en un solo strip. El botón Split define el orden: (off) entrada → dinámica → filtros/EQ; (on) entrada → filtros → dinámica → EQ. El Channel Out invierte el EQ y la dinámica. La opción dynamic sidechain envía el EQ al circuito de control de la dinámica sin que el EQ se escuche en la señal de salida | — | Activar split en el canal SSL para que el compresor no reaccione a componentes que el filtro va a eliminar. Usar dynamic sidechain cuando se quiere que el detector de dinámica sea selectivo en frecuencia | Los diferentes tipos de potes en SSL (Brown, Black, Orange) producen variaciones de curva dentro de la misma familia tonal | Dejar el Split en off sin considerar que el compresor puede estar reaccionando a subsónicas o ultrasónicas que luego el EQ eliminará | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3C-09 | Modelado analógico | Pultec EQP-1A | Pultec EQP-1A: ecualizador pasivo de programa | Ecualizador pasivo (sin amplificación activa en la sección de EQ) con etapa valvular posterior. Diseñado originalmente para señal completa de programa. Graves por pasos: 20, 30, 60, 100 Hz en shelving. Boost y attenuate son shelving independientes de pendiente asimétrica | — | El Pultec funciona "a oído": los valores impresos en el panel no son exactos y varían entre unidades. El nivel de entrada afecta la coloración (distorsión armónica valvular) | Aplicar boost y attenuate simultáneamente en graves genera la curva Pultec: énfasis en la zona elegida con limpieza en la octava superior, lo que hace que los graves suenen más definidos y menos embarrados | Usar los valores del panel del Pultec como si fueran referencias exactas de frecuencia o ganancia | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3C-10 | Modelado analógico | Curva Pultec | Mecanismo de la curva Pultec | Al activar boost y attenuate simultáneamente en la sección de graves, las curvas de boost y attenuate no son simétricas: la de boost empieza antes (más a la izquierda) y la de attenuate empieza después. El resultado es un énfasis en la zona grave elegida con una limpieza en la octava siguiente | Relación aproximada: boost en 100 Hz → limpieza ~1 kHz; boost en 60 Hz → limpieza ~600 Hz; boost en 30 Hz → limpieza ~300 Hz | Usar cuando se quiere peso en graves sin embarrar la zona de medios bajos (200–300 Hz), que es donde la mezcla puede volverse turbia | Esta curva no es una resonancia en el sentido técnico de los filtros; es el producto de la asimetría entre dos circuitos independientes de boost y cut | Confundir la curva Pultec con el comportamiento de un shelving resonante | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3C-11 | Modelado analógico | Pultec agudos | Pultec EQP-1A sección agudos: peligro del modo sharp | En agudos: el boost es en campana y la atenuación es en shelving. El control de ancho de banda (broad/sharp) puede llevar el pico de la campana a niveles muy superiores a lo indicado; en modo sharp con atenuación simultánea puede generarse una forma equivalente a un pasabajos resonante con picos superiores a 20 dB | — | Nunca usar extremos de boost + attenuate en modo sharp sin verificar el nivel real del pico con analizador: el riesgo es real para los transductores | Antes de usar combinaciones extremas, verificar la curva resultante con un analizador. Si el pico supera los 15–18 dB, evaluar si la aplicación tiene sentido musical real o si es un accidente de diseño | Confiar en los valores visuales del panel en modo sharp del Pultec para estimar el nivel real del pico resultante | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3C-12 | Modelado analógico | Pultec MQ-5 | Pultec MQ-5: EQ de medios con curva "smile" | El MQ-5 tiene tres bandas de medios: campana aditiva + campana sustractiva + campana aditiva. La estructura produce una curva pico-dip-pico que permite realzar una zona de medios mientras se limpia otra adyacente | — | Usar la banda aditiva para barrido de localización, luego enfocar la banda sustractiva en la zona identificada; la tercera banda queda libre para refuerzo adicional | La curva en V del MQ-5 crea contraste espectral dentro de los medios: resaltar una zona limpiando la adyacente hace que la zona realzada suene más presente | Esperar que el MQ-5 funcione como un paramétrico: sus bandas están fijas y la interacción entre ellas es parte del diseño, no una limitación | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE D — EQ DINÁMICO

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|
| 3D-01 | EQ dinámico | Definición | EQ dinámico como herramienta espectral adaptiva | Un EQ dinámico es una campana o shelf que aplica ganancia o atenuación solo cuando la señal supera (o baja de) un umbral en la zona de frecuencia definida. El rango de ganancia reemplaza al ratio del compresor. No divide la señal en bandas con crossovers como el multibanda | Umbral (threshold) + rango (range) = cuánto actúa y hasta cuándo. Algunos implementan también attack y release | Usar cuando el problema es específico y ocurre de forma intermitente: la sibilancia es el ejemplo clásico, pero también sirve para resonancias que solo aparecen en ciertos momentos | El EQ dinámico opera en el espectro de forma adaptiva; es una herramienta espectral aunque tenga comportamiento temporal. Su lugar pedagógico es Eje 3, no Eje 4 | Tratarlo como un compresor por bandas o confundirlo con la compresión multibanda | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3D-02 | EQ dinámico | EQ dinámico vs multibanda | Diferencia estructural | El multibanda divide la señal con crossovers y aplica compresores completos (con ratio) a cada banda. El EQ dinámico aplica una campana dinámica (con range) sin crossovers. El multibanda trabaja bien por zonas amplias del espectro; el EQ dinámico trabaja mejor en problemas frecuenciales puntuales | — | Para resolver una sibilancia o una resonancia intermitente: EQ dinámico. Para controlar una banda entera del espectro de forma dinámica: multibanda | Pasar por crossovers ya implica rotación de fase aunque la banda no comprima; el EQ dinámico, al no usar crossovers, tiene menos impacto en la fase | Usar el multibanda para resolver un problema puntual que el EQ dinámico resolvería con mayor precisión y menor efecto colateral | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 3D-03 | EQ dinámico | De-esser | De-esser como EQ dinámico de banda | Un de-esser es un EQ dinámico (o un compresor de sidechain frecuencial) especializado en la banda de la sibilancia. La sibilancia no se corrige con EQ estático porque es un fenómeno intermitente; todo fenómeno intermitente requiere tratamiento dinámico, no estático | — | Modo Wide: cuando la sibilancia supera el umbral, se reduce la ganancia de la señal completa. Modo Split: cuando supera el umbral, solo se reduce la banda de sibilancia | El exceso de corrección convierte la S en una Z: verificar siempre con el material corriendo que la corrección no elimina la consonante por completo | Aplicar EQ estático sustractivo en la zona de sibilancia esperando que resuelva una consonante que ocurre intermitentemente | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

## 3. CONTENIDO ATRIBUIBLE DEL EJE

| Bloque | Atribución requerida | Etiqueta recomendada |
|---|---|---|
| PDF: Apunte Ecualizadores 2020 | Autoría: Pablo Rabinovich. La taxonomía y los parámetros de EQ son de dominio general del campo; la formulación del apunte no debe copiarse | Reformular; citar si se usa la formulación directamente |
| Modelos API 550A, 550B, 560 | Hardware de API Technologies (empresa). El análisis de su carácter tonal es del dominio general del campo, pero las descripciones específicas del docente fuente sobre el comportamiento de cada modelo son suyas | Reformular las descripciones; nombrar los modelos con atribución a API como fabricante |
| Modelos Neve 1073, 1084, 1081 | Hardware de AMS Neve. Mismo criterio que API | Reformular descripciones; atribuir a AMS Neve como fabricante |
| Modelos SSL E y G | Hardware de Solid State Logic. Idem | Reformular; atribuir a SSL |
| Modelos Pultec EQP-1A y MQ-5 | Hardware de Pulse Techniques / Pultec. Curva Pultec: fenómeno técnico de dominio general del campo (ampliamente documentado en fuentes independientes) | La curva Pultec puede explicarse sin atribución al docente fuente; sí nombrar el equipo original |
| Artículo del docente "El secreto de los potes en las legendarias mesas SSL" | Autoría: Pablo Rabinovich (artículo publicado en el blog del instituto). No usar su contenido sin atribución | BLOQUEAR como fuente directa; citar si se referencia externamente |
| Descripciones comparativas API vs Neve ("patada en el estómago" vs "empujón"; "navaja" vs "seda") | EXPRESIÓN NO REUTILIZABLE — ver Sección 4 | — |

---

## 4. BLOQUEOS DEL EJE

| Bloque bloqueado | Tipo de riesgo | Por qué no debe pasar |
|---|---|---|
| Metáforas de carácter API vs Neve: "patada en el estómago" / "empujón"; "navaja en la oreja" / "seda pura" | EXPRESIÓN NO REUTILIZABLE | Analogías memorables y muy reconocibles del autor fuente; son su forma distintiva de describir los modelos |
| Frase "mezclas la misma canción en una API o en una Neve y obtenés mezclas totalmente distintas" | EXPRESIÓN NO REUTILIZABLE | Formulación oral marcada del docente fuente |
| Regla oral sobre frecuencias "inglesas vs norteamericanas" de consolas (12 kHz vs 10 kHz; 80/60 Hz vs 100 Hz) | EXPRESIÓN NO REUTILIZABLE | Observación cultural presentada como regla informal del docente; verificación independiente necesaria antes de reutilizar como doctrina |
| Descripción del Pultec como equipos que "se volvieron famosos por hacer lo contrario de lo que decía el manual" | EXPRESIÓN NO REUTILIZABLE | Formulación oral memorable y situada en el contexto de clase |
| Secuencia pedagógica del temario fuente para este módulo: tipos de EQ → Q → simétrico/asimétrico → gráficos → analógicos (API → Neve → SSL → Pultec) | ESTRUCTURA NO REUTILIZABLE | Orden de exposición reconocible del curso fuente |
| Referencia al artículo propio del docente publicado en el blog del instituto | EXPRESIÓN NO REUTILIZABLE | Autobiográfico; localiza la autoría en el docente fuente |
| Anécdota de Grammy mencionada en clase 14 como contexto de saturación y producción urbana | EXPRESIÓN NO REUTILIZABLE | Historia o referencia personal del autor fuente |

---

## 5. VACÍOS Y TENSIONES DEL EJE

| Tipo | Descripción | Implicación para redacción |
|---|---|---|
| **Vacío** | El enmascaramiento espectral (masking) aparece en la arquitectura de KENTH como tema del Eje 3, pero en las fuentes no tiene desarrollo técnico propio independiente; aparece implícito en las decisiones de filtrado (Eje 2) y EQ contextual, pero sin una explicación formal del fenómeno perceptual | Al redactar: construir el concepto de masking desde psicoacústica general (fuentes externas: threshold of masking, upward masking) o reducir a criterio operativo sin el desarrollo teórico |
| **Vacío** | Los batimientos y tonos de combinación aparecen listados en la arquitectura como herramienta de EQ correctivo, pero no tienen desarrollo específico en las fuentes del proyecto más allá de su mención en contexto de suma de señales. | Construir desde fuentes externas o reducir a advertencia de diagnóstico cruzando con Eje 1 |
| **Vacío relativo** | El EQ dinámico tiene buena cobertura técnica en Clase 15 (comparación con multibanda, parameters, de-esser), pero carece de ejemplos prácticos de aplicación en mezcla para voces, guitarras u otros instrumentos | Al redactar: la doctrina técnica está disponible; los casos de uso concretos por instrumento deberán construirse editorialmente |
| **Tensión de límite** | La frontera entre EQ correctivo (Eje 3) y filtrado de limpieza (Eje 2) puede difuminarse cuando el EQ correctivo opera en la zona baja del espectro del instrumento. Un HPF a 200 Hz en una guitarra puede ser Eje 2 o Eje 3 según si elimina contenido inútil o compite con el bajo | Al redactar: declarar explícitamente el criterio de límite: si la intervención espectral busca liberar espacio para otro elemento o eliminar contenido inútil sin modificar el carácter, es Eje 2; si busca definir o modificar el timbre del instrumento, es Eje 3 |
| **Tensión de cruce con Eje 4** | El de-esser y el EQ dinámico tienen comportamiento dinámico y pueden cruzarse conceptualmente con compresores y compresión multibanda (Eje 4). La arquitectura de KENTH los mantiene en Eje 3 | Al redactar: declarar el cruce; explicar por qué el EQ dinámico vive en Eje 3 (herramienta espectral de comportamiento adaptivo) y el multibanda en Eje 4 (herramienta dinámica con división de bandas) |
| **Tensión de cruce con Eje 6** | El EQ del mix bus o el balance espectral global como decisión de EQ pertenecen a Eje 6 (integración global), no a Eje 3. El Eje 3 trabaja espectro por elemento | Al redactar: cuando se hable de EQ en Eje 3 siempre referir al procesamiento por canal o grupo de instrumento; el EQ del bus principal va a Eje 6 |
| **Tensión de profundidad** | El tratamiento de modelos analógicos es extenso en las fuentes (clases 13 y 14 son casi íntegramente sobre esto), mientras que otros subtemas del eje (masking, tonos de combinación, EQ en contexto como sistema) tienen cobertura mínima. Al redactar habrá que compensar ese desbalance | No replicar la proporción de las fuentes; equilibrar la profundidad según los objetivos pedagógicos de KENTH |

---

## 6. PAQUETE LIMPIO DEL EJE

### EJE 3 — IDENTIDAD ESPECTRAL · Paquete limpio para proyecto generativo

---

**FUNCIÓN DEL EJE:** Moldear el carácter tonal de cada elemento y la coherencia espectral de la mezcla como sistema. Sin identidad espectral definida, los elementos compiten por el mismo espacio y la mezcla carece de balance propio.

---

#### BLOQUE A — PARÁMETROS Y TIPOLOGÍA

**Doctrina reutilizable:**
- EQ Peak/Bell: mayor acción en la frecuencia central (fc), que es la media geométrica de los extremos del BW. fc = √(f1 × f2)
- Q = fc / BW = fc / (f2–f1). Q alto → campana estrecha. Q bajo → campana ancha y suave
- Q y pendiente son parámetros distintos. Q afecta la forma de la parte superior de la curva; la pendiente de las laderas depende del diseño del filtro
- Q constante: la forma de la curva no varía con la ganancia. Q proporcional: a mayor ganancia, la parte superior de la campana se estrecha. Los analógicos clásicos suelen tener Q proporcional
- Simétrico: las curvas de boost y cut son espejo. Asimétrico: boost y cut tienen formas distintas (frecuente en analógicos; el cut suele ser más estrecho que el boost)
- EQ Shelving: la FC puede interpretarse como el punto de ganancia/2 (convención digital) o como –3 dB del estante (convención analógica). Las dos no coinciden; verificar antes de asumir dónde actúa
- Shelving resonante: introduce un pico antes del estante; efectivo en graves para combinar peso general con énfasis localizado; problemático en agudos si se exagera
- Gráfico: frecuencias fijas; el usuario solo controla ganancia. División por octava, media octava o 1/3 de octava. A mayor número de bandas, mayor interacción entre bandas adyacentes
- Semiparamétrico: control de frecuencia y ganancia; sin Q. Herramienta de barrido para localizar problemas
- Paramétrico: control de frecuencia, ganancia y Q. Más versátil para corrección precisa y color musical

**Advertencias:**
- LÍMITE Eje 2 / Eje 3: los filtros de limpieza (HPF, notch defensivo) son Eje 2. Un shelving o campana que modifica el carácter tonal ya es Eje 3
- CRUCE → EJE 6: el EQ del mix bus y el balance espectral global pertenecen a Eje 6, no a este eje

---

#### BLOQUE B — CRITERIO DE DECISIÓN

**Doctrina reutilizable:**
- EQ correctivo: elimina o atenúa elementos no deseados. Tendencia sustractiva, Q relativamente alto, localizado. Puede decidirse en solo
- EQ estético/tonal: modifica el carácter del instrumento de forma deliberada. Tendencia aditiva, Q más bajo, validación en contexto de mezcla
- Lo que suena "mal" en solo puede ser correcto en la mezcla; y a la inversa. El EQ estético requiere siempre verificación en contexto

**Heurísticas reformulables:**
- Técnica de barrido: aplicar boost elevado con Q alto y recorrer el espectro hasta identificar la frecuencia problemática; cortar en esa frecuencia. El oído detecta mejor el exceso que la falta
- Comparar siempre con bypass compensando el nivel percibido: el EQ aditivo puede dar ilusión de mejora por simple aumento de volumen
- Si el cambio del EQ no se percibe en la mezcla o solo se percibe como cambio de nivel, la intervención puede no ser necesaria

**Advertencias:**
- VACÍO: masking espectral y tonos de combinación listados en la arquitectura tienen cobertura mínima en las fuentes; construir desde psicoacústica general

---

#### BLOQUE C — MODELADO ANALÓGICO

**Doctrina reutilizable:**
- El modelado analógico no emula solo la curva; emula también la THD, la distorsión armónica y el comportamiento no lineal del circuito original
- El nivel de entrada al plugin de modelado afecta la coloración. Calibrar según el estándar AES o EBU del modelo emulado
- Los valores impresos en los paneles analógicos (y muchos de sus modelados) no son exactos: son referencias, no certezas matemáticas. La herramienta principal es el oído
- Distintos desarrolladores que emulan el mismo equipo producen sonidos distintos: el modelado incluye decisiones de interpretación del hardware

**Perfiles funcionales para uso por familia (reformular descripciones sin reproducir las metáforas del autor fuente):**

| Familia | Carácter general | Uso típico en mezcla |
|---|---|---|
| API 550A/B | Medios presentes, graves con impacto pronunciado | Batería, guitarras, voces con carácter frontal |
| API 560 | Gráfico de firma amplia, medios marcados | Cuando se busca carácter API sin precisión paramétrica |
| Neve 1073 | Agudos suaves y densos, graves con cuerpo no agresivo | Voces, cuerdas, mezclas de amplio rango dinámico |
| Neve 1084/1081 | Neve con mayor flexibilidad; botón High Q modifica la dinámica del medio | Cuando se necesita firma Neve con más control de banda |
| SSL E/G (canal) | Versátil, funciona como strip completo; Split y dynamic sidechain son herramientas clave | Mezcla integrada; usar Split para que la dinámica no reaccione a frecuencias que el EQ eliminará |
| Pultec EQP-1A | Pasivo valvular; graves por pasos; curva Pultec (boost+attenuate simultáneos) | Graves de mezcla o master; presencia de programa completo |
| Pultec MQ-5 | Medios en curva pico-dip-pico | Corrección y color en la zona media del espectro |

**Curva Pultec (reutilizable sin atribución al docente fuente; es del dominio general del campo):**
- Boost y attenuate simultáneos en graves: las dos pendientes son asimétricas → énfasis en la zona de boost + limpieza en la octava superior
- Relación aproximada: boost en 100 Hz → limpieza cerca de 1 kHz; boost en 60 Hz → limpieza cerca de 600 Hz
- No es una resonancia: es el producto de la asimetría entre dos circuitos de boost y cut independientes

**Pultec agudos — advertencia de seguridad:**
- Modo sharp con boost elevado y atenuación simultánea puede generar picos de 20–25 dB. Riesgo real para tweeter. Verificar siempre con analizador antes de usar configuraciones extremas

**Atribuciones:**
- Equipos: API Technologies, AMS Neve, Solid State Logic, Pulse Techniques/Pultec (fabricantes históricos)
- PDFs de Rabinovich: reformular la formulación

**Bloqueos:** metáforas de carácter del autor fuente; artículo del blog; regla oral sobre consolas inglesas vs norteamericanas sin verificación; secuencia pedagógica del curso fuente

---

#### BLOQUE D — EQ DINÁMICO

**Doctrina reutilizable:**
- EQ dinámico: campana o shelf que actúa solo cuando la señal supera un umbral en esa frecuencia. No usa crossovers. Su lugar pedagógico es Eje 3 (herramienta espectral adaptiva), no Eje 4
- Diferencia con multibanda: el multibanda divide con crossovers y aplica compresores con ratio; el EQ dinámico aplica campanas con range. Multibanda: problemas de zonas amplias. EQ dinámico: problemas puntuales e intermitentes
- De-esser: EQ dinámico especializado en sibilancias. La sibilancia es intermitente; todo fenómeno intermitente requiere tratamiento dinámico. Modos Wide (señal completa) y Split (solo la banda)
- Exceso de corrección en de-esser: transforma la S en Z. Verificar siempre con el material corriendo

**Advertencias:**
- CRUCE → EJE 4: el EQ dinámico puede cruzar con compresión multibanda en contexto de compresión frecuencial, pero su enseñanza base y parámetros pertenecen a Eje 3. El cruce es declarado, no absorción
- VACÍO: casos de uso prácticos del EQ dinámico por instrumento no están cubiertos en las fuentes; construir editorialmente

---

*Paquete listo para ingesta en Proyecto Generativo. Siguiente eje cuando lo indiques.*
