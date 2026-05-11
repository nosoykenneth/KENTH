---
axis_id: "Eje 2"
axis_number: 2
axis_title: "Eje 2 - Integridad de la señal"
doc_layer: "limpio"
doc_type: "operacion_practica"
source_origin: "course"
status: "ready_for_indexing"
language: "es"
allowed_for_indexing: true
---

# EJE 2 — INTEGRIDAD DE LA SEÑAL
## Extracción Forense KENTH Academy

---

## 1. COBERTURA DEL EJE

**Fuentes que lo alimentan directamente:**

| Fuente | Contenido relevante para Eje 2 |
|---|---|
| Clases 11–12 (Mezcla) | Filtros: tipos, pendientes, criterios de uso por instrumento, consecuencias de fase, filtro invertido como técnica, fase lineal, filtrado de subsónicas |
| Clases 8–10 (Mezcla) | Corrección de polaridad top/bottom, alineación manual de batería, alineación con plugins, orden de prioridades |
| Clases 6–7 (Mezcla) | Gain staging por elemento: señales percusivas vs no percusivas, criterio VU, faders vs trim, subgrupos |
| Clase 24 (Training) | Split de bajo con crossover LR, prueba nula para verificar integridad del crossover |
| Clase 22 (Training) | Corrección de polaridad en grabación real, criterio compuerta en grupo de tambor, alineación con referencia |
| PDF: Apunte Filtros 2022 | Tipología de filtros, frecuencia de corte, pendientes, Butterworth, resonantes, fase lineal |
| PDF: Apunte Estructura de Ganancia | Niveles de señal, gain staging en cadena, procesadores, efectos, faders vs estructura |
| PDF: Apunte Filtros (sección fase) | Desplazamiento de fase en filtros no lineales, filtros de fase lineal, pre-ringing |
| Temario fuente (Módulos XII, parte de VIII y X) | Filtros, práctica de mezcla por filtrado, alineación de baterías |

**Partes dislocadas:**

La subsección de **corrección de interpretación** (Melodyne, triggers/replacement, cuantización) aparece en el temario fuente como módulo de Training (no como parte del curso principal de Mezcla) y prácticamente sin desarrollo técnico sistemático en las transcripciones de las clases de Mezcla. El contenido existe en el listing del temario fuente, pero no tiene cuerpo desarrollado en las fuentes disponibles. Es la subsección con mayor vacío de cobertura del eje.

El **gain staging por elemento** en el temario fuente aparece agrupado con los medidores (Módulo VII) y en la práctica de sesión (Módulo VIII). En KENTH ese contenido se separa: el concepto ya fue introducido en Eje 0-B; la aplicación por elemento y por cadena de procesadores es Eje 2.

---

## 2. MATRIZ NEUTRA DEL EJE

### BLOQUE A — FILTRADO POR DECISIÓN

| # | Tema | Subtema | Concepto técnico | Definición neutra | Fórmula / Relación | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|---|
| 2A-01 | Filtros | Tipología | HPF / Low Cut | Atenúa frecuencias por debajo de la frecuencia de corte. Equivalencia: "pasa altos" = "corta bajos". La atenuación comienza antes de la frecuencia de corte, a distancia dependiente de la pendiente elegida | FC = frecuencia a –3 dB en la banda de atenuación. Pendiente: 6 dB/oct (1er orden), 12 dB/oct (2do), 18, 24 dB/oct | Verificar siempre con analizador que el corte no toca la fundamental del instrumento. Decisión 1: protección térmica / energía inútil. Decisión 2: limpieza bajo el registro del instrumento. Decisión 3: espacio en contexto de mezcla | La frecuencia de corte no es donde comienza la atenuación; una pendiente suave puede estar atenuando varias octavas antes de la FC nominal | Filtrar en solo y asumir que lo que suena bien ahí va a sonar bien en la mezcla | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2A-02 | Filtros | Tipología | LPF / High Cut | Atenúa frecuencias por encima de la frecuencia de corte. El desarrollo tímbrico de una fuente depende en parte de su contenido de alta frecuencia; aplicar sin necesidad puede degradar la identidad del instrumento | Igual que HPF pero invertido | Usar para control de ruido en alta frecuencia, interacción entre tweeters o transductores, y decisiones de perspectiva espacial (un LPF suave retrocede el instrumento en el espacio) | Un LPF suave emula el comportamiento natural de la distancia: el aire atenúa los agudos antes que los graves | Aplicar LPF en todos los canales como práctica de limpieza sin evaluar si el instrumento necesita su contenido de alta frecuencia para funcionar en la mezcla | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2A-03 | Filtros | Tipología | Band Pass / Reject / Notch | Band Pass: deja pasar una banda entre dos FC y atenúa fuera de ella. Band Reject: inverso del Band Pass. Notch: versión muy estrecha del reject, alta Q, para eliminación quirúrgica de una frecuencia específica | FC del Band Pass = √(f1 × f2) | Notch: para eliminar resonancias específicas de instrumentos o artefactos del entorno. Band Reject: para limpiezas más anchas. Band Pass: en FX (teléfono, radio AM) o como herramienta de análisis | El Notch a Q muy alta puede generar artefactos de fase y pre-ringing; usarlo con la menor ganancia necesaria | Usar notch de alta Q como recurso primario para problemas espectrales que deberían resolverse primero con EQ de ganancia o corrección de fuente | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2A-04 | Filtros | Tipología | AllPass | No atenúa ninguna frecuencia en amplitud; modifica la fase de forma selectiva en función de la frecuencia. Su función en mezcla es corregir o ajustar relaciones de fase entre señales sin alterar el balance espectral | — | Usar cuando el problema es exclusivamente de fase entre dos señales y no se quiere modificar el contenido frecuencial | Un AllPass es invisible en un analizador de amplitud pero transforma la relación de fase; su efecto es audible al sumar con otras señales | Confundir el AllPass con un procesador espectral; no tiene efecto audible solo sino en relación con otras señales | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2A-05 | Filtros | Pendientes | Pendiente de atenuación | La pendiente define cuántos dB se atenúan por octava (o por década) más allá de la FC. Valores típicos: 6, 12, 18, 24 dB/oct. A mayor pendiente, corte más abrupto pero mayor rotación de fase en torno a la FC | 1 polo = 6 dB/oct = 20 dB/déc | Pendiente suave: preserva transitorios; menor rotación de fase. Pendiente pronunciada: control rápido; mayor rotación de fase. Elegir según el objetivo: limpieza amplia → suave; eliminación precisa → pronunciada | Pendiente pronunciada debajo del registro real de un instrumento: permite filtrar sin tocar el sonido útil. Pendiente suave en un instrumento sin contenido útil en esa zona: genera una larga cola de atenuación innecesaria | Elegir siempre la pendiente más pronunciada disponible asumiendo que "más corte = mejor resultado" | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2A-06 | Filtros | Consecuencias | Desplazamiento de fase en filtros no lineales | Todo filtro no lineal (todos los estándar de tipo Butterworth, Bessel, etc.) introduce rotación de fase en torno a su frecuencia de corte. Esa rotación es frecuencia-dependiente y puede causar problemas al sumar esa señal con otras | — | El HPF es el primer eslabón de la cadena: colocarlo antes de procesadores dinámicos evita que el compresor o la compuerta reaccionen a contenido que luego se va a eliminar | Si un compresor está antes del HPF, las subsónicas pueden disparar el compresor y generar una compresión no deseada que luego queda grabada en el resultado después del filtro | Poner el filtro después del compresor en la cadena de inserts | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2A-07 | Filtros | Consecuencias | Filtros resonantes | Un filtro resonante genera un pico de ganancia en torno a la FC al aumentar el Q. Puede producir aumentos de nivel imprevistos en la salida. A Q muy alto puede dañar transductores. También puede producir rizado (ripple) en la respuesta | — | El filtro resonante es útil como herramienta de FX (síntesis, barridos); en mezcla usar con extrema cautela y solo con propósito tonal deliberado | Un HPF a 24 dB/oct con resonancia puede elevar el nivel de salida por encima del nivel de entrada: verificar siempre la salida del filtro con medidor | Subir el Q de un HPF de limpieza esperando que "más corte" equivale a "más controlado" | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2A-08 | Filtros | Consecuencias | Filtros de fase lineal | Los filtros de fase lineal no producen rotación de fase ni retardo dependiente de frecuencia. Solo existen en el dominio digital. Compromiso: introducen latencia (delay de grupo constante) y pre-ringing antes de los transitorios | — | Usar en mastering o en situaciones donde la preservación de la relación de fase es crítica y el pre-ringing no es un problema para el tipo de material (material no percusivo) | Pre-ringing es perceptible especialmente en material percusivo; para batería o percusión, los filtros de fase lineal pueden sonar peor que los estándar | Aplicar fase lineal por defecto en mezcla sin evaluar si el material es percusivo | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2A-09 | Filtros | Criterios operativos | Tres criterios de decisión de filtrado | Los tres criterios de uso de un filtro en mezcla son independientes y requieren distintos métodos de evaluación: (1) protección / control de energía inútil, (2) limpieza por debajo del registro del instrumento, (3) creación de espacio cediendo territorio a otro instrumento en el contexto de la mezcla | — | Criterios 1 y 2 pueden evaluarse con el instrumento en solo. Criterio 3 no puede evaluarse en solo: requiere el contexto de la mezcla completa | Lo que parece un corte excesivo en solo puede ser exactamente lo correcto en contexto de mezcla; lo que suena bien en solo puede estar ocupando espacio que no le corresponde | Decidir el punto de corte del filtro escuchando el canal en solo para los tres criterios | HEURÍSTICA OPERATIVA REFORMULABLE | REFORMULAR MÁS |
| 2A-10 | Filtros | Técnica | Filtro invertido como herramienta de decisión | Invertir el comportamiento del filtro (escuchar lo que se está quitando en lugar de lo que queda) permite detectar con precisión el punto exacto donde la energía que se elimina ya no aporta utilidad al instrumento dentro de la mezcla | — | Solo válido para el Criterio 3: escuchar lo que se lleva el filtro mientras la mezcla corre, hasta encontrar el punto donde lo que se extrae es solo barullo o territorio de otro instrumento | Trabajar con el filtro invertido en el contexto de la mezcla, no en solo; en solo el resultado siempre suena mal aunque en mezcla sea correcto | Confiar en el resultado en solo del filtro invertido para decidir el punto de corte | HEURÍSTICA OPERATIVA REFORMULABLE | REFORMULAR MÁS |
| 2A-11 | Filtros | Resolución visual | Lo que se ve vs lo que ocurre realmente | La representación gráfica de la curva de filtro en muchos plugins no refleja con exactitud lo que ocurre en la señal, especialmente en altas frecuencias o con valores de FFT bajos. El ajuste de resolución del plugin cambia la representación, no el filtro | — | Siempre verificar el efecto real del filtro con analizador espectral en la señal de salida; no confiar solo en la representación de la curva del plugin | A baja resolución de FFT, un filtro puede parecer actuar donde no actúa o viceversa; la señal es la referencia, no la curva visual del plugin | Ajustar la frecuencia de corte basándose únicamente en la visualización gráfica de la curva del plugin | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE B — CORRECCIÓN DE POLARIDAD Y ALINEACIÓN

| # | Tema | Subtema | Concepto técnico | Definición neutra | Fórmula / Relación | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|---|
| 2B-01 | Polaridad | Corrección en mono | Corrección snare top/bottom | El micrófono inferior del tambor tiende a quedar con polaridad inversa respecto al superior porque la membrana se mueve en sentido contrario cuando el parche es golpeado. Corregir la polaridad devuelve el grave y el cuerpo del tambor al sumar ambas señales | — | Procedimiento: emparejar niveles → escuchar juntos → insertar inversión de polaridad en el bottom → elegir la opción que devuelve más graves y cuerpo | La opción técnicamente correcta es la que suma más; si la otra suena artísticamente mejor, puede usarse a sabiendas del compromiso | Invertir la polaridad del top en lugar del bottom, o no verificar cuál señal es la referencia antes de corregir | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2B-02 | Polaridad | Corrección multimicrófono | Verificación de polaridad relativa en conjunto de batería | Después de resolver top/bottom del tambor, verificar la relación de polaridad entre el grupo de tambor y el overhead. Nadie garantiza que ambos sistemas de captación compartan la misma referencia de polaridad | — | Sumar el grupo de tambor (top+bottom) con el overhead al mismo nivel → invertir polaridad del grupo → quedarse con la opción que da más cuerpo e integración | Cuando alineás o corregís polaridad en un elemento, afectás su relación con otros; siempre verificar el efecto en el conjunto, no solo en el par corregido | Corregir solo el par inmediato (top/bottom) sin verificar la relación resultante con los micrófonos de ambiente | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2B-03 | Alineación | Manual | Alineación manual por transientes | La alineación manual consiste en desplazar temporalmente las señales para que los transitorios de los distintos micrófonos que captan la misma fuente coincidan, reduciendo o eliminando el comb filtering | — | Tomar un elemento de referencia (en batería: el tambor); alinear los demás respecto a esa referencia. Cada alineación sobre un elemento puede desalinear su relación con otro | En batería, la prioridad de alineación es el tambor: su sonido define la producción más que otros elementos. Alinear el hi-hat no importa si el tambor queda mal | Intentar que todos los elementos estén perfectamente alineados simultáneamente entre sí; en un sistema de múltiples micrófonos eso es imposible: siempre hay compromisos | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2B-04 | Alineación | Plugins | Autoalineación con plugin (tipo Auto-Align) | Los plugins de autoalineación analizan las relaciones temporales entre múltiples canales que captan la misma fuente y calculan los desplazamientos necesarios para minimizar el comb filtering | — | Insertar el plugin en el primer slot de inserción de cada canal (antes de cualquier otro proceso). Escanear sobre una sección representativa y extensa, no sobre una selección corta | El plugin reduce el tiempo operativo significativamente; no reemplaza el criterio sobre qué elemento tomar como referencia ni la verificación del resultado | Escanear sobre una sección muy corta o poco representativa del material | HEURÍSTICA OPERATIVA REFORMULABLE | REFORMULAR MÁS |
| 2B-05 | Alineación | Alineación con compuerta | Reducción del comb filtering por diferencia de nivel | Si la diferencia de nivel entre dos señales coherentes supera ~9,5 dB, el comb filtering se vuelve mínimo. Una compuerta bien configurada que reduce el nivel de un micrófono secundario durante los ataques del principal puede reducir drásticamente el problema sin necesidad de alineación temporal | Diferencia > 9 dB → comb filtering prácticamente inexistente | Usar ducking o compuerta en señales secundarias puede ser más eficiente que alinear temporalmente cuando la diferencia de nivel es manejable | Si dedicar tiempo a alinear los overheads queda superado por un ducking bien planteado que genera >9 dB de diferencia de nivel, el esfuerzo de alineación puede no ser necesario | Gastar tiempo alineando señales con gran diferencia de nivel cuando el comb filtering es mínimo o ya está resuelto por nivel | HEURÍSTICA OPERATIVA REFORMULABLE | REFORMULAR MÁS |
| 2B-06 | Alineación | Crossover de bajo | Split correcto para procesamiento paralelo | Para dividir un instrumento en dos bandas de procesamiento independiente (p.ej., bajo: subgrave + definición), un par simple de HPF+LPF no reconstruye correctamente al sumar. La FC queda a –3 dB en cada rama; la suma genera exceso en la banda de cruce y problemas de fase | LPF + HPF estándar: FC a –3 dB → exceso al sumar · Crossover Linkwitz-Riley (LR): dos filtros en cadena por rama → FC a –6 dB → suma reconstruida correctamente | Verificar integridad del crossover con prueba nula: sumar ambas ramas con una de ellas con polaridad invertida; si el crossover es correcto la suma se cancela | Si la prueba nula no produce cancelación completa, el split tiene problemas de amplitud o fase. La fase lineal en ambas ramas mejora la reconstrucción | Asumir que sumar un LPF y un HPF en frecuencia idéntica produce una suma que reconstruye el original correctamente | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE C — GAIN STAGING POR ELEMENTO

| # | Tema | Subtema | Concepto técnico | Definición neutra | Fórmula / Relación | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|---|
| 2C-01 | Gain staging | Concepto aplicado | Estructura de ganancia por elemento | Aplicar el principio de gain staging a cada track individual: la señal debe entrar y salir de cada procesador dentro de su rango óptimo de trabajo. La salida de cada etapa debe ser consistente con la entrada de la siguiente | — | En cadena de inserts: verificar que la salida de cada procesador equivale (aproximadamente) a su entrada antes de continuar. Los faders de canal pertenecen al balance de mezcla, no al gain staging de la cadena | El gain staging deficiente en un canal no es solo un problema de ese canal: al llegar a subgrupos y master bus, la suma de niveles incorrectos dificulta el control global | Subir el fader del canal para compensar ganancia insuficiente en la cadena de inserts | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2C-02 | Gain staging | Señales percusivas | Criterio de nivel para señales percusivas | Las señales percusivas tienen un factor de cresta alto: la diferencia entre el pico y el promedio es grande. El VU subestima el nivel porque no captura transitorios. El medidor de pico es el más relevante para estas señales | Señales percusivas: monitorear con Peak; objetivo: picos no sobrepasen –6 a –12 dBFS (según headroom deseado) | Verificar que los picos de señales percusivas no saturen la entrada de procesadores dinámicos. Para señales percusivas, la regla de nivel visual ("la señal ocupa ~1/3 de la altura del clip") es una referencia práctica rápida | Un bombo va a mostrar más nivel en un VU que un tambor aunque piquen igual, por diferencias en el contenido de baja frecuencia que integra distinto; no comparar nivel con VU entre instrumentos percusivos de distinta naturaleza | Usar el VU como referencia de nivel para señales percusivas de alta cresta | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2C-03 | Gain staging | Señales no percusivas | Criterio de nivel para señales no percusivas | Las señales no percusivas (voz, bajo, sintetizador, guitarra sostenida) tienen dinámica más uniforme. El VU y el RMS son medidores adecuados para establecer su nivel de trabajo. Objetivo: aguja del VU con tendencia vertical / RMS ~–20 dBFS (sin compensación AES-17) | Objetivo RMS: ~–20 dBFS para señal no percusiva en punto de trabajo | Medir sobre una sección representativa del instrumento (la más densa o estable), no sobre todo el track ni sobre zonas poco representativas | La zona más fuerte del instrumento no debe saturar el procesador siguiente; ajustar la ganancia tomando como referencia los pasajes más fuertes | Medir el nivel de una voz tomando un fragmento de silencio o una zona inusualmente suave como referencia de ajuste | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2C-04 | Gain staging | Faders vs estructura | Rol diferenciado del fader | El fader de canal controla la relación de nivel en la suma (balance de mezcla). La estructura de ganancia gestiona los niveles dentro de la cadena de procesamiento de cada canal. Subir el fader para compensar ganancia baja en la cadena produce señales pobremente calibradas en los procesadores intermedios | — | Usar Trim o ajuste de ganancia de clip para corregir el nivel que llega a los procesadores; usar el fader solo para el balance final entre elementos en la mezcla | El Trim (o ganancia de clip) en el primer slot de inserción es la herramienta correcta para ajustar el nivel de trabajo de cada canal antes de los procesadores | Compensar con el fader lo que debería corregirse en el gain del clip o del primer procesador | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2C-05 | Gain staging | Envíos y efectos | Gain staging en cadena de efectos | El nivel del envío (send) a un canal de efectos no debe usarse para controlar la cantidad de efecto en la mezcla; debe calibrar el nivel de entrada al efecto. La salida del efecto se controla con el fader del canal del efecto | Objetivo nivel de entrada a efecto: ~–20 dBFS RMS | Si varios canales envían al mismo canal de efecto, verificar que la suma de los envíos no sature la entrada. En cadena en serie: el nivel de entrada al efecto afecta el carácter del procesamiento analógico o de modelado | Usar el send muy bajo para que el efecto "apenas se sienta" y el fader del canal de efecto muy alto para compensar es el error simétrico al de usar el fader para compensar ganancia | Usar el nivel del send para controlar cuánto efecto entra en la mezcla, ignorando el nivel de entrada al procesador del efecto | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE D — CORRECCIÓN DE INTERPRETACIÓN

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|
| 2D-01 | Corrección de afinación | Criterio de intervención | Integridad vs expresión | La corrección de afinación debe preservar la identidad expresiva de la interpretación. No toda desviación de la afinación temperada es un error; algunas son parte del carácter de la voz o el instrumento | Intervenir cuando la desviación produce incoherencia tonal en el contexto de la mezcla, no cuando simplemente difiere del temperamento igual | Una corrección excesiva puede eliminar el carácter del instrumento: el objetivo es integridad, no perfección absoluta | Aplicar corrección automática máxima a todas las pistas como práctica estándar sin evaluar si la interpretación tiene valor expresivo en sus desviaciones | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2D-02 | Corrección de afinación | Herramientas | Corrección tipo Melodyne | Las herramientas de corrección de afinación basadas en análisis de pitch permiten corrección automática (snap a la nota más cercana) y corrección manual (ajuste nota por nota). La corrección manual preserva mejor las características expresivas | — | Preferir corrección manual en voces con carácter expresivo propio. Corrección automática aceptable para instrumentos o voces con poco margen de expresión por desviación | La corrección automática con velocidad alta destruye el vibrato natural y el portamento; usarla solo cuando el material lo admite | Aplicar corrección automática a una voz principal con vibrato expresivo o inflexiones melismáticas propias del estilo | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2D-03 | Corrección de timing | Cuantización suave | Corrección rítmica preservando groove | La cuantización fija todos los eventos al grid temporal; la cuantización suave aplica una corrección parcial, acercando los eventos al grid sin llegar exactamente, preservando el groove y el feel humano | — | Elegir el porcentaje de cuantización según cuánto groove se quiere preservar. Para correcciones puntuales de timing problemático, intervenir nota por nota | El groove de una interpretación humana tiene variaciones intencionales que la cuantización total elimina; evaluar si la corrección mejora la mezcla o destruye el carácter | Aplicar cuantización al 100% a todos los elementos de una grabación en vivo asumiendo que la precisión temporal es siempre preferible | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 2D-04 | Triggers / Replacement | Batería y percusión | Trigger y replacement de piezas | El trigger detecta los ataques de una pieza de batería y dispara un sample o sonido de reemplazo/refuerzo. El replacement puede sustituir o blendear con la señal original. Se usa cuando la grabación tiene problemas de consistencia o cuando se busca un carácter de sonido específico | — | El blend entre original y sample permite preservar el realismo del sonido grabado mientras se refuerza la consistencia dinámica | El trigger puede dispararse incorrectamente por bleed de otras piezas; verificar los disparos antes de blendear para evitar artefactos | Aplicar replacement total sin verificar que los disparos corresponden a los golpes reales y no a bleed | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

## 3. CONTENIDO ATRIBUIBLE DEL EJE

| Bloque | Atribución requerida | Etiqueta recomendada |
|---|---|---|
| PDF: Apunte Filtros 2022 | Autoría: Pablo Rabinovich. La doctrina técnica (tipos de filtro, frecuencia de corte, pendientes) es de dominio general; la formulación del apunte no debe copiarse | Reformular; citar si se usa directamente |
| PDF: Apunte Estructura de Ganancia | Autoría: Pablo Rabinovich. La doctrina técnica de gain staging es de dominio general del campo; la formulación del apunte no debe copiarse | Reformular; citar si se usa directamente |
| Criterio de tres decisiones para el uso de filtros en mezcla (protección / registro / espacio) | Formulación estructurada presente en el curso fuente. La lógica es general pero la formulación como "tres criterios" en ese orden específico puede considerarse la organización propia del autor fuente | REFORMULAR MÁS al redactar; no reproducir el orden ni la formulación específica |
| Técnica del "filtro invertido" como método de decisión para el Criterio 3 | Observación práctica del autor fuente; metodología operativa identificable con su enseñanza | USAR CON ATRIBUCIÓN si se presenta como técnica específica; reformular si se integra como práctica general |
| Crossover Linkwitz-Riley + prueba nula para verificación | Linkwitz-Riley: diseño de filtro de dominio técnico general (autoría Siegfried Linkwitz / Russ Riley). La aplicación específica mostrada en clase (Training 24) es práctica del autor fuente | Atribuir LR a sus autores; reformular la aplicación práctica |

---

## 4. BLOQUEOS DEL EJE

| Bloque bloqueado | Tipo de riesgo | Por qué no debe pasar |
|---|---|---|
| Anécdota del docente con ejecutivo de Sony/compañía discográfica sobre "la voz y el tambor" | EXPRESIÓN NO REUTILIZABLE | Historia personal del autor fuente; identificable y no transferible |
| Formulaciones orales: "recién empieza la mezcla", "se alinean de a una, de a poquito", "se pincha todo", "al rojo vivo" | EXPRESIÓN NO REUTILIZABLE | Vocabulario oral muy marcado del docente fuente |
| Secuencia pedagógica del curso fuente: primero análisis espectral → filtros teóricos → práctica de mezcla solo con filtros (Clases 10→11→12) | ESTRUCTURA NO REUTILIZABLE | Orden específico del curso fuente; reconocible como arquitectura de ese curso |
| Descripción comparativa de consolas (SSL vs API vs Trident "paleta de colores") en el contexto de gain staging | EXPRESIÓN NO REUTILIZABLE | Analogía personal del docente; contexto situado en su práctica particular |
| Referencia a anécdota del artista de los 90 y el Clarín (ya presente en otras clases) | EXPRESIÓN NO REUTILIZABLE | Historia personal repetida del autor fuente |
| Ejemplo de ruido rosa filtrado como sustituto de Tonal Balance Control (método casero) | EXPRESIÓN NO REUTILIZABLE | Técnica presentada con "solución de pobre" y referencia a iZotope; tono oral identificable con el docente fuente |
| Orden exacto de la práctica de filtrado por instrumento: bombo → bajo → guitarras acústicas base → guitarras de arreglo → voz | ESTRUCTURA NO REUTILIZABLE | Secuencia pedagógica reconocible del curso fuente |

---

## 5. VACÍOS Y TENSIONES DEL EJE

| Tipo | Descripción | Implicación para redacción |
|---|---|---|
| **Vacío mayor** | La subsección de corrección de interpretación (Melodyne, timing, triggers/replacement) tiene cobertura mínima en las fuentes. Aparece en el temario fuente como lista de temas del Training (no del curso principal) pero sin clases específicas desarrolladas disponibles. Los Bloques 2D de la matriz son casi enteramente doctrina general del campo sin respaldo sólido en las fuentes específicas | Esta subsección requiere construcción desde fuentes externas o reducción a criterios generales. No puede ser densamente desarrollada solo desde las fuentes disponibles |
| **Vacío menor** | Los tipos de filtro Notch y AllPass tienen escasa cobertura práctica en las transcripciones; se mencionan en el PDF de filtros pero sin casos de uso detallados en mezcla | Al redactar: desarrollar con fuentes externas o reducir al criterio funcional esencial |
| **Tensión de límite** | La frontera entre filtrado de limpieza (Eje 2) y EQ correctivo (Eje 3) puede ser difusa. El Criterio 3 de filtrado (ceder espacio en contexto de mezcla) puede confundirse con ecualización correctiva cuando el corte está dentro del registro del instrumento | Al redactar: dejar explícito que el filtrado del Eje 2 no modifica el carácter tonal; cuando el ajuste busca modificar el timbre o resaltar frecuencias, ya es Eje 3 |
| **Tensión de límite** | El gain staging por elemento en Eje 2 se apoya en el VU y el RMS, que fueron introducidos como instrumentos de lectura en Eje 1. El alumno necesita conocer Eje 1 para aplicar correctamente el gain staging de Eje 2 | Declarar el cruce explícitamente: la lectura de nivel aprendida en Eje 1 es la herramienta operativa del gain staging de Eje 2 |
| **Tensión de límite** | Los filtros resonantes como herramienta de FX (barridos de síntesis) aparecen mencionados en el apunte; en KENTH ese uso expresivo probablemente pertenece más a Eje 3 o Eje 5 que a Eje 2. El Eje 2 debería contener solo el uso defensivo del resonante (notch de limpieza) | Al redactar: Eje 2 incluye filtros resonantes solo para limpieza; el uso creativo del resonante pertenece a otros ejes |
| **Tensión de cruce con Eje 4** | La compuerta y el ducking aparecen como herramienta de reducción de comb filtering (Bloque 2B-05). Su desarrollo técnico completo (parámetros, configuración) pertenece a Eje 4 | En Eje 2: solo el criterio de uso de la compuerta como herramienta de integridad (reducir señal secundaria); el funcionamiento interno de la compuerta se desarrolla en Eje 4 |
| **Cruce activo con Eje 1** | Las correcciones de Eje 2 nacen del diagnóstico de Eje 1; el alumno no puede aplicar corrección de polaridad, alineación ni filtrado sin haber leído primero la señal | Eje 2 debe abrirse con referencia explícita al diagnóstico del Eje 1 como condición de posibilidad |

---

## 6. PAQUETE LIMPIO DEL EJE

### EJE 2 — INTEGRIDAD DE LA SEÑAL · Paquete limpio para proyecto generativo

---

**FUNCIÓN DEL EJE:** Primera fase operativa del ciclo LDOV. Limpia, alinea y corrige antes de moldear. Una señal con problemas de fase, contenido inútil, nivel mal calibrado o interpretación defectuosa contaminará todo el procesamiento posterior.

---

#### BLOQUE A — FILTRADO POR DECISIÓN

**Doctrina reutilizable:**
- HPF/Low Cut: atenúa por debajo de una FC. La atenuación comienza antes de la FC: a pendiente más suave, antes empieza
- LPF/High Cut: atenúa por encima de FC. Usar con precaución; el desarrollo tímbrico del instrumento depende de su contenido de alta frecuencia. Un LPF suave retrocede el instrumento en el espacio percibido
- Band Pass / Band Reject / Notch: control de bandas específicas. Notch para resonancias puntuales; usar con el mínimo Q necesario para evitar pre-ringing
- AllPass: modifica fase sin tocar amplitud. Invisible en el analizador espectral; su efecto solo es audible en suma con otras señales
- Pendientes: 6 dB/oct (1 polo) → 12, 18, 24 dB/oct. Mayor pendiente → corte más abrupto + mayor rotación de fase en torno a la FC
- La frecuencia de corte es donde ocurre –3 dB; la atenuación comienza antes, a distancia dependiente de la pendiente
- El HPF es el primer eslabón de la cadena de inserts: si va después del compresor, el compresor reacciona a contenido que luego se elimina
- Filtros no lineales (estándar) rotan la fase en torno a la FC. Los filtros de fase lineal (solo digital) evitan la rotación de fase pero introducen latencia y pre-ringing; problemáticos con material percusivo
- Filtros resonantes: pico de ganancia en torno a FC al aumentar Q. En mezcla: solo para limpieza defensiva (notch); el uso creativo del resonante no pertenece a este eje
- La representación gráfica del plugin no siempre refleja exactamente lo que ocurre en la señal; verificar con analizador

**Tres criterios de filtrado (a reformular sin reproducir la secuencia del autor fuente):**
- Criterio de protección: controlar energía muy baja o muy alta que no aporta contenido útil y carga la cadena
- Criterio de registro: eliminar energía por debajo del registro real del instrumento
- Criterio de espacio: ceder territorio dentro del registro del instrumento a otro elemento de mayor preponderancia en ese rango — solo evaluable con la mezcla corriendo, no en solo

**Heurísticas reformulables:**
- Escuchar lo que se elimina (no lo que queda) mientras la mezcla corre: detecta con precisión el punto donde la energía cortada ya no aporta utilidad en el contexto
- Un corte que suena excesivo en solo puede ser exactamente correcto en mezcla
- Para señales que se alejan en el espacio percibido: un LPF suave simula la atenuación natural de los agudos con la distancia

**Atribuciones:**
- Filtros Butterworth / Bessel / Linkwitz-Riley: diseños de dominio técnico general; citar autores si se mencionan por nombre
- PDFs de Rabinovich: reformular la formulación; la doctrina técnica es de dominio general

**Advertencias:**
- LÍMITE Eje 2 / Eje 3: el filtrado que modifica carácter tonal (elección deliberada de timbre, realce de zona) ya es Eje 3. Eje 2 solo filtra lo que no debe estar
- CRUCE → EJE 4: compuertas y ducking para reducción de señales secundarias se mencionan en Eje 2 como criterio; el desarrollo técnico de esas herramientas pertenece a Eje 4

**Bloqueos:** secuencia pedagógica de la práctica de filtrado del curso fuente; ejemplos anclados en el contexto de clase; formulaciones orales del docente

---

#### BLOQUE B — CORRECCIÓN DE POLARIDAD Y ALINEACIÓN

**Doctrina reutilizable:**
- Corrección de polaridad en tambor: el micrófono inferior tiende a quedar invertido respecto al superior por la física del parche. Corregirlo devuelve el cuerpo y los graves al sumar
- Verificar siempre: (1) par top/bottom entre sí → (2) par corregido vs micrófonos de ambiente
- Procedimiento de verificación: emparejar niveles → escuchar en contexto → invertir → elegir la versión con más graves y más integración
- Cada alineación temporal sobre un elemento puede crear desalineación con otro: definir prioridades antes de alinear. Prioridad en batería: el tambor
- Alineación manual: desplazar temporalmente señales hasta que los transitorios de distintos micrófonos sobre la misma fuente se aproximen
- Plugins de autoalineación: insertar en primer slot de cada canal; escanear sobre sección representativa y extensa
- Crossover correcto (split paralelo): usar diseño Linkwitz-Riley (dos filtros en cadena por rama, cada uno con la misma pendiente → FC a –6 dB). Verificar con prueba nula: sumar ambas ramas con una invertida; si el crossover es correcto, la suma se cancela casi completamente
- Si la diferencia de nivel entre micrófonos supera ~9,5 dB, el comb filtering es mínimo; reducir nivel de señal secundaria puede ser más eficiente que alinear temporalmente

**Heurísticas reformulables:**
- Para un split de bajo: si la prueba nula no cancela, hay problema en el crossover (amplitud o fase); no continuar sin resolverlo
- Verificar polaridad siempre antes de alinear; la alineación sobre una polaridad incorrecta amplifía el problema

**Atribuciones:**
- Linkwitz-Riley: Siegfried Linkwitz / Russ Riley

**Advertencias:**
- CRUCE → EJE 1: la corrección de polaridad y alineación nacen del diagnóstico del Eje 1; sin diagnóstico previo, no hay corrección
- VACÍO: corrección de polaridad en señales estéreo (no solo en multimicrófono mono) tiene cobertura pero su aplicación práctica detallada está más desarrollada en Eje 1 que en Eje 2

**Bloqueos:** anécdotas del docente situadas en el contexto de esas clases; formulaciones orales marcadas

---

#### BLOQUE C — GAIN STAGING POR ELEMENTO

**Doctrina reutilizable:**
- La cadena de inserts opera en serie: la salida de cada procesador debe calibrarse antes de entrar al siguiente
- Señales percusivas: referencia de nivel por Peak (picos). Objetivo: picos entre –6 y –12 dBFS según headroom deseado. El VU es engañoso para percusión de alta cresta
- Señales no percusivas: referencia por VU o RMS. Objetivo: ~–20 dBFS RMS sin compensación AES-17
- Medir sobre secciones representativas del instrumento, no sobre todo el track ni sobre zonas atípicas
- El fader de canal controla el balance en la suma; la ganancia de clip o Trim en primer slot controla el nivel que llega a los procesadores. No son intercambiables
- Nivel de envío a efectos: calibra la entrada al efecto; el fader del canal del efecto controla la salida en la mezcla. Usar el send para controlar cuánto efecto entra es el error más frecuente
- En sumadores y subgrupos: gestionar el nivel de llegada con Trim o plugin de ganancia en el primer slot, no solo con los faders de los canales que envían

**Heurísticas reformulables:**
- Un bombo integra más nivel en el VU que un tambor aunque tengan picos similares: no comparar nivel entre instrumentos percusivos de distinta naturaleza usando VU como referencia
- La regla visual del "clip a un tercio de su altura" es un atajo rápido para señales no percusivas en mezcla

**Atribuciones:**
- PDF Estructura de Ganancia: Rabinovich. Reformular la formulación; doctrina del campo es de dominio general

**Advertencias:**
- CRUCE → EJE 0: el concepto de gain staging fue introducido en Eje 0-B. Eje 2 desarrolla la aplicación por elemento
- CRUCE → EJE 1: la calibración del VU para plugins de modelado (AES vs EBU) fue cubierta en Eje 1

**Bloqueos:** formulaciones orales del docente; ejemplos de nombres de plugins específicos como referencia central

---

#### BLOQUE D — CORRECCIÓN DE INTERPRETACIÓN

**Advertencia de cobertura:** esta subsección tiene escaso desarrollo en las fuentes disponibles. El contenido siguiente es doctrina técnica general del campo; no está respaldado por desarrollo específico en las fuentes del proyecto. Al redactar, construir desde fuentes externas o solicitar búsqueda adicional.

**Doctrina reutilizable:**
- Corrección de afinación: intervenir cuando la desviación produce incoherencia tonal en el contexto de la mezcla. El objetivo es integridad, no perfección de afinación temperada
- Herramientas tipo Melodyne: permiten corrección automática (snap a nota más cercana) y manual (nota por nota). La corrección manual preserva mejor las características expresivas
- Corrección de timing: la cuantización total elimina el groove; la cuantización suave (porcentaje parcial) acerca al grid preservando el feel. Para errores puntuales, corrección nota por nota
- Triggers/replacement: el trigger detecta ataques y dispara un sample de reemplazo o refuerzo. El blend original+sample preserva el realismo mientras aumenta la consistencia dinámica. Verificar que los disparos corresponden a golpes reales y no a bleed antes de blendear

**Advertencias:**
- VACÍO MAYOR: esta subsección requiere construcción desde fuentes externas o reducción a criterios generales. Las fuentes disponibles del proyecto no la desarrollan con suficiente profundidad
- LÍMITE: la corrección de interpretación no modifica el carácter tonal ni dinámico del material; solo corrige errores de afinación o timing que afectan la integridad de la señal en el contexto de la mezcla

---

*Paquete listo para ingesta en Proyecto Generativo. Siguiente eje cuando lo indiques.*
