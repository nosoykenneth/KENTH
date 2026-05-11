# EJE 2 — INTEGRIDAD DE LA SEÑAL
### KENTH Academy · Mezcla y Masterización · Contenido Final de Curso

---

## SECCIÓN 1 — FUNCIÓN PRÁCTICA DEL EJE

El Eje 2 es la primera fase operativa del ciclo LDOV: Decidir y comenzar a Operar.

El Eje 1 diagnosticó qué hay en la señal. El Eje 2 actúa sobre esos diagnósticos: limpia lo que no debe estar, corrige lo que está mal relacionado, y calibra el nivel para que los procesadores posteriores operen correctamente.

La lógica del eje es de preparación, no de diseño. Aquí no se moldea el timbre, no se da carácter, no se construye imagen. Se garantiza que lo que llega al procesamiento posterior esté limpio, alineado y calibrado.

Cuatro dominios de operación:

**Filtrado:** eliminar energía que no aporta contenido útil. Puede ser energía por debajo del registro del instrumento, ruido, contenido que contamina a otro elemento en la mezcla, o contenido indeseable captado en la grabación.

**Corrección de polaridad y alineación:** resolver los problemas de relación entre señales que el Eje 1 diagnosticó. Una polaridad invertida corregida y señales alineadas temporalmente son condición para que cualquier procesamiento posterior tenga sentido.

**Gain staging por elemento:** asegurar que cada canal y cada procesador de la cadena recibe la señal en el nivel para el que fue diseñado. Sin gain staging correcto, la compresión, el EQ y la reverb del Eje 2 en adelante operan en condiciones desconocidas.

**Corrección de interpretación:** intervenir sobre errores de afinación o timing que afectan la coherencia del material antes de procesar su timbre o dinámica.

**Límite del eje:** el Eje 2 no modifica el carácter tonal de la señal. En el momento en que una decisión de filtrado busca darle brillo, calidez o color a un instrumento, ya es Eje 3. El Eje 2 filtra lo que no debe estar; el Eje 3 moldea lo que queda.

---

## SECCIÓN 2 — QUÉ DEBE PODER HACER EL ALUMNO AL TERMINAR ESTE EJE

Al completar el Eje 2, el alumno es capaz de:

- Aplicar un HPF o LPF con criterio de necesidad real: identificar qué se está eliminando, por qué, y verificar que el corte no afecta al contenido útil del instrumento.
- Elegir la pendiente del filtro según el objetivo de la intervención y las consecuencias de fase que implica.
- Reconocer cuándo el filtro debe ir antes del compresor en la cadena de inserts y por qué.
- Usar un filtro notch para eliminar una resonancia puntual con el mínimo Q necesario.
- Aplicar un filtro AllPass cuando el problema es de fase entre señales sin querer modificar el espectro.
- Corregir la polaridad invertida en un par de micrófonos con procedimiento verificado.
- Extender la verificación de polaridad desde el par inmediato hasta el conjunto de micrófonos.
- Alinear temporalmente señales de multitrack con criterio de prioridades.
- Verificar la integridad de un crossover de frecuencias con prueba nula.
- Calibrar el nivel de trabajo de señales percusivas y no percusivas antes de procesar.
- Distinguir el rol del fader de canal del rol del Trim o ganancia de clip en la cadena de procesamiento.
- Calibrar correctamente el nivel de envío a canales de efectos.
- Aplicar corrección de afinación con criterio de integridad, no de perfección absoluta.
- Aplicar corrección de timing con porcentaje de cuantización adecuado al material.
- Verificar y configurar un trigger de batería para evitar disparos incorrectos por bleed.

---

## SECCIÓN 3 — SUBSECCIONES FINALES DEL EJE

El orden sigue la lógica de preparación: primero se trabaja sobre los problemas de contenido frecuencial (filtrado), luego sobre los problemas relacionales (polaridad y alineación), luego sobre el nivel (gain staging), y finalmente sobre el material de la grabación (corrección de interpretación). Cada subsección construye condiciones para la siguiente.

**BLOQUE A — FILTRADO POR DECISIÓN**

- **2-A1** · HPF y LPF: cuándo filtrar, dónde cortar y con qué pendiente
- **2-A2** · Notch, AllPass y filtros de fase lineal: usos específicos
- **2-A3** · Posición del filtro en la cadena y consecuencias de fase

**BLOQUE B — CORRECCIÓN DE POLARIDAD Y ALINEACIÓN**

- **2-B1** · Corrección de polaridad: procedimiento y verificación en conjunto
- **2-B2** · Alineación temporal: manual, plugins y criterio de compromisos
- **2-B3** · Split de frecuencias: crossover correcto y prueba nula

**BLOQUE C — GAIN STAGING POR ELEMENTO**

- **2-C1** · Nivel de trabajo por tipo de señal: percusivas y no percusivas
- **2-C2** · Faders, Trim y envíos: roles diferenciados en la cadena

**BLOQUE D — CORRECCIÓN DE INTERPRETACIÓN**

- **2-D1** · Afinación, timing y triggers: criterios de intervención

---

## SECCIÓN 4 — CURSO PRINCIPAL DEL EJE

---

### 2-A1 · HPF Y LPF: CUÁNDO FILTRAR, DÓNDE CORTAR Y CON QUÉ PENDIENTE

**Situación real**
El alumno tiene un track de guitarra acústica. En el analizador hay energía por debajo de 80 Hz: no es la fundamental del instrumento, es vibración mecánica del estudio y ruido de bajo registro captado en la grabación. Al mismo tiempo, el bajo eléctrico ocupa ese mismo espacio y los dos instrumentos se pisarán. El alumno sabe que hay que filtrar, pero no sabe dónde exactamente ni con qué pendiente.

**Explicación operativa**
Filtrar no es lo mismo que ecualizar. Un filtro de paso de altos o de paso de bajos establece un límite: todo lo que está por debajo o por encima de ese límite se atenúa. No da carácter, no realza, no moldea: elimina. La decisión de filtrado responde a tres preguntas distintas que tienen distintos métodos de evaluación:

**Primera pregunta: ¿hay energía en esa zona que no debería estar?**
Ruido de bajo registro, rumble de sala, interferencias de red eléctrica, vibración mecánica. Esta energía no pertenece al instrumento. Se puede evaluar en solo: si al escuchar el canal aislado hay energía en frecuencias que el instrumento no emite, se elimina.

**Segunda pregunta: ¿hay energía del instrumento que está por debajo de su registro real?**
Una guitarra acústica no tiene fundamental por debajo de 80 Hz. Cualquier energía por debajo de ese punto es energía del entorno, no del instrumento. Esta también puede evaluarse en solo.

**Tercera pregunta: ¿el instrumento ocupa espacio que necesita otro elemento con mayor peso en esa zona?**
Esta pregunta no puede responderse en solo. Solo tiene sentido con la mezcla corriendo. Un cello puede tener fundamentales en la misma zona que el bajo eléctrico; si el bajo es el elemento que lleva esa región en la mezcla, el cello puede ceder algo de ese territorio para que ambos convivan. Pero si se evalúa en solo, ese corte puede sonar exagerado o incorrecto.

**Teoría mínima**
La frecuencia de corte (FC) de un filtro es el punto donde la señal ha sido atenuada 3 dB. La atenuación comienza antes de ese punto, a una distancia que depende de la pendiente elegida:

- 6 dB/oct (1 polo): corte gradual, comienza a atenuar desde varias octavas antes de la FC. Mínima rotación de fase.
- 12, 18, 24 dB/oct: corte más abrupto, más concentrado en la FC. Mayor rotación de fase alrededor de la FC.

La elección de pendiente no es independiente de la pendiente de fase: un HPF de 24 dB/oct bien colocado limpia con precisión, pero rota más la fase en torno a la FC que uno de 6 dB/oct. En el contexto de señales que se sumarán con otras, esa rotación importa.

El LPF atúa los agudos. Su uso defensivo más habitual es controlar ruido de alta frecuencia, pero tiene también un efecto perceptivo: un LPF suave sobre un instrumento lo retrocede levemente en el espacio percibido, porque el aire atenúa los agudos de forma similar con la distancia. Aplicar LPF a todos los canales sin criterio puede degradar la identidad tímbrica de instrumentos que necesitan su contenido de alta frecuencia para funcionar.

**Acción**
1. Para la primera y segunda pregunta: activar el analizador, escuchar el canal en solo, identificar la zona de energía no deseada, colocar el HPF o LPF justo antes del comienzo del contenido útil del instrumento.
2. Para la tercera pregunta: con la mezcla corriendo, ajustar el punto de corte escuchando el impacto en el contexto. El canal en solo no informa sobre este criterio.
3. Una vez colocado el filtro, reproducir el pasaje más dinámico del instrumento y verificar con el analizador que el corte no toca la fundamental ni los primeros armónicos del instrumento.

**Verificación**
Después de filtrar: escuchar el canal en solo y confirmar que el instrumento no suena recortado, adelgazado o desprovisto de cuerpo. Luego escuchar en el contexto de la mezcla. Si en contexto el instrumento suena más integrado y menos invasivo, el filtro está bien colocado. Si en contexto el instrumento suena hueco o delgado, el corte fue demasiado agresivo o está en la zona equivocada.

**Error frecuente**
Colocar un HPF en todos los canales en el mismo punto de frecuencia como práctica automática de limpieza, sin verificar la fundamental real de cada instrumento. Un bajo eléctrico tiene fundamental entre 40 y 80 Hz dependiendo de la nota; un HPF a 100 Hz sobre ese canal está recortando el instrumento, no limpiando el canal.

---

### 2-A2 · NOTCH, ALLPASS Y FILTROS DE FASE LINEAL: USOS ESPECÍFICOS

**Situación real**
El alumno detecta una resonancia en 220 Hz en un track de guitarra eléctrica: es un pico estrecho que hace que una nota específica suene más que las demás. También tiene un split de bajo procesado en paralelo donde las dos ramas suenan bien por separado pero al sumarlas algo no cuadra. Y tiene una sesión de orquesta donde la alineación de fase entre instrumentos es crítica.

Cada uno de esos problemas tiene una herramienta específica.

**Explicación operativa**

**Notch (Band Reject de Q alto)**
Para resonancias puntuales: una nota que llena demasiado, un zumbido de red eléctrica (50 o 60 Hz y sus armónicos), una frecuencia modal del recinto captada en la grabación. El Notch actúa en una banda muy estrecha sin afectar las frecuencias vecinas. La regla es usar el Q mínimo necesario para resolver el problema: un Q excesivo introduce pre-ringing y artefactos de fase audibles, especialmente en material percusivo.

**AllPass**
Un filtro que no toca la amplitud: lo que entra igual de fuerte sale. Lo que modifica es la relación de fase entre las distintas frecuencias de la señal. Su efecto solo es audible cuando esa señal se suma con otra. Usos: ajustar la relación de fase entre dos micrófonos sobre la misma fuente cuando la alineación temporal no resuelve completamente el problema; o compensar la rotación de fase introducida por otro filtro en la cadena. Si se inserta un AllPass en un canal en solo y se escucha, no pasa nada audible. Si se suma con otra señal, la relación de fase cambia y el resultado es diferente.

**Filtros de fase lineal**
Los filtros estándar (Butterworth y derivados) rotan la fase alrededor de la frecuencia de corte. Esa rotación es una consecuencia de cómo están construidos. Los filtros de fase lineal son un diseño exclusivamente digital que evita esa rotación: el retardo que introduce es igual para todas las frecuencias (retardo de grupo constante). El precio es doble: latencia en la cadena, y pre-ringing —una especie de eco que aparece antes del transitorio. En material no percusivo (cuerdas, coros, pads) ese pre-ringing puede ser inaudible. En material percusivo (batería, percusión), el pre-ringing se hace claramente audible y puede sonar peor que el filtro estándar que pretendía evitarse.

**Acción**
- **Notch:** localizar la resonancia con el analizador, colocar el notch en esa frecuencia exacta, subir el Q hasta que el pico desaparezca, luego reducir el Q hasta el mínimo que resuelve el problema sin sonar artificial.
- **AllPass:** insertar en el canal con problema de fase relativa, ajustar la frecuencia del AllPass y escuchar el resultado en la suma con las otras señales, no en solo.
- **Fase lineal:** activar en contextos donde la preservación estricta de la relación de fase importa (mezcla orquestal, procesamiento de grupos donde la suma posterior es crítica) y donde el material no sea predominantemente percusivo.

**Verificación**
- Notch: con el analizador, verificar que el pico desapareció y que las frecuencias vecinas no fueron afectadas de forma audible.
- AllPass: escuchar siempre en suma con las señales relacionadas, comparar con y sin el AllPass.
- Fase lineal: escuchar el material percusivo presente con y sin el filtro; si hay pre-ringing audible, reemplazar por filtro estándar.

**Error frecuente**
Usar un Notch de Q muy alto para resolver un problema espectral que en realidad se resolvería mejor con un EQ correctivo de Q moderado. Un Q excesivo introduce artefactos que pueden ser más molestos que la resonancia original. Si el problema es una zona que suena un poco llena, el Notch no es la herramienta: el EQ paramétrico del Eje 3 es más apropiado.

---

### 2-A3 · POSICIÓN DEL FILTRO EN LA CADENA Y CONSECUENCIAS DE FASE

**Situación real**
El alumno tiene un track de bombo con un HPF colocado después del compresor. El compresor está respondiendo de forma extraña: bombea aunque el umbral parece correcto y el material no lo justifica. El problema no está en el compresor: está en el orden de los procesadores.

**Explicación operativa**
La posición del filtro en la cadena de inserts no es indiferente. El HPF elimina energía subsónica y de baja frecuencia. Si el HPF está después del compresor, el compresor está reaccionando a esa energía en el momento en que recibe la señal —antes de que el HPF la elimine. Las frecuencias muy bajas tienen mucha energía incluso cuando no son audibles: un rumble a 20 Hz que no se escucha puede mover el compresor tanto como el transitorio del bombo.

El resultado es compresión disparada por contenido que luego se elimina. Cuando el compresor comprime por la subsónica y luego el HPF la quita, la mezcla queda con la ganancia reducida por una causa que ya no existe en la señal.

La regla de posición: el HPF es el primer eslabón de la cadena. Va antes de cualquier procesador dinámico.

Las consecuencias de fase del HPF también importan cuando esa señal se suma con otras. Todo filtro estándar rota la fase en torno a su FC. En un bombo con micrófono delantero y trasero, el HPF en uno de los canales pero no en el otro (o con distinta FC o pendiente) cambia la relación de fase entre las dos señales. Si ya se corrió la polaridad y la alineación antes de insertar los filtros, los filtros pueden rehacerla.

El orden recomendado para la cadena de inserts del eje de integridad:
1. Trim o ganancia de clip (nivel de entrada a la cadena).
2. HPF / filtros de limpieza.
3. Corrección de polaridad y alineación (si no se aplica antes de los inserts).
4. EQ correctivo (si aplica Eje 3 en esa etapa).
5. Compresores y dinámicos.

**Acción**
1. Revisar la posición del HPF en cada canal que tenga compresores o compuertas: si el dinámico está antes del filtro, reordenar.
2. Si hay varios canales que se suman y todos tienen HPF, verificar que los puntos de corte y las pendientes no introduzcan diferencias de fase problemáticas en la zona de corte.
3. Verificar el resultado del reordenamiento escuchando el comportamiento del compresor: si el bombeo desaparece o se reduce al mover el HPF antes, el diagnóstico era correcto.

**Verificación**
Reproducir el pasaje con el compresor en bypass y con el HPF activo. Luego activar el compresor. Si ahora el compresor reacciona de forma coherente con el material sin activarse en exceso entre notas, el orden es correcto.

**Error frecuente**
Asumir que el orden de los inserts no importa mientras todos los procesadores estén activos. En un entorno de coma flotante el nivel total no clipea, pero el comportamiento de los procesadores dinámicos sí cambia según qué señal reciben. El orden no es estético: es funcional.

---

### 2-B1 · CORRECCIÓN DE POLARIDAD: PROCEDIMIENTO Y VERIFICACIÓN EN CONJUNTO

**Situación real**
El alumno tiene la batería grabada con micrófono superior e inferior del tambor, overheads y micrófono de bombo. Cada uno suena bien en solo. Al activarlos todos juntos, el tambor pierde cuerpo y los graves desaparecen. El diagnóstico de Eje 1 señala un problema de polaridad. Ahora es el momento de corregirlo.

**Explicación operativa**
La corrección de polaridad no es una operación única: es un procedimiento que se aplica por etapas, verificando en cada paso el impacto en el conjunto, no solo en el par inmediato.

El punto de partida más frecuente es el par de micrófonos superior e inferior del tambor. El micrófono inferior tiende a quedar con polaridad inversa respecto al superior porque las dos membranas del parche se mueven en direcciones opuestas cuando reciben el mismo golpe: la superior baja, la inferior sube (o viceversa según la dinámica del parche). Al sumarlos sin corregir, se cancelan parcialmente.

El procedimiento en dos fases:

**Fase 1: par top/bottom**
Emparejar los niveles de ambos micrófonos. Escucharlos juntos en mono. Notar el nivel y el cuerpo. Activar la inversión de polaridad en el micrófono inferior. Comparar. La opción correcta es la que devuelve más graves, más cuerpo y más integración. Quedarse con esa.

**Fase 2: el par corregido en relación con el resto**
Una vez corregido el par top/bottom, el resultado es una señal nueva. Esa señal nueva tiene una relación de polaridad con los overheads y con el micrófono de bombo que no ha sido verificada. Sumar el grupo de tambor (ya corregido) con los overheads al mismo nivel. Colapsar a mono. Notar el resultado. Invertir la polaridad del grupo de tambor respecto a los overheads. Quedarse con la versión que suena más integrada y con más graves.

Cada corrección modifica la relación con los demás elementos: no hay una secuencia automática. La lógica es siempre: corregir → verificar en conjunto → corregir si hace falta → verificar de nuevo.

**Teoría mínima**
La inversión de polaridad no afecta a una señal escuchada sola: el cerebro no percibe si una onda está en polaridad normal o invertida en ausencia de referencia. El problema surge en la suma. Si dos señales coherentes (la misma fuente captada con dos micrófonos) tienen polaridad opuesta, se cancelan. La cancelación es total si los niveles son idénticos; parcial si difieren. En el contexto de una batería completa, las cancelaciones parciales son las más frecuentes: producen un timbre endeble y opaco sin cancelación audible obvia.

**Acción**
1. Aislar el par top/bottom del tambor.
2. Emparejar niveles y colapsar a mono.
3. Activar la inversión de polaridad en el micrófono inferior y comparar con la versión sin invertir.
4. Elegir la opción con más graves y más cuerpo.
5. Incorporar los overheads. Sumar con el grupo de tambor corregido. Colapsar a mono.
6. Probar la inversión del grupo de tambor respecto a los overheads. Elegir.
7. Repetir el proceso para cada par adicional que se agregue (bombo, room mics).

**Verificación**
Con todos los micrófonos activos: colapsar a mono. La suma en mono debe sonar sólida, con graves presentes y sin sensación de vaciado. Si en mono el conjunto suena más lleno y definido que alguno de los canales por separado, la polaridad está bien. Si en mono el conjunto suena más delgado que el tambor solo, hay todavía un problema de polaridad no resuelto.

**Error frecuente**
Corregir solo el par top/bottom y dar por terminado el proceso sin verificar la relación resultante con los overheads. El par puede estar bien corregido internamente pero en relación inversa con los overheads, lo que produce exactamente el mismo efecto de pérdida de graves que se pretendía corregir.

---

### 2-B2 · ALINEACIÓN TEMPORAL: MANUAL, PLUGINS Y CRITERIO DE COMPROMISOS

**Situación real**
Los micrófonos de batería están a distintas distancias físicas de cada pieza. Esa diferencia de distancia es una diferencia temporal: el sonido llega a cada micrófono en momentos distintos. Al sumar las señales, esa diferencia produce comb filtering. La polaridad está corregida. El siguiente paso es alinear.

**Explicación operativa**
La alineación temporal consiste en desplazar las señales en el tiempo para que los transitorios de los distintos micrófonos que captan la misma fuente lleguen aproximadamente al mismo momento. La reducción del comb filtering es el resultado: al coincidir en el tiempo, las señales se suman con menos cancelaciones.

Lo primero que hay que establecer es qué señal es la referencia. En un kit de batería, la referencia habitual es el tambor: es el instrumento con más peso en la producción, el que define el groove y el que más se escucha. Los demás micrófonos se alinean respecto a él, no entre sí.

El problema que inevitablemente aparece: cuando se alinea un micrófono respecto al tambor, puede desalinearse levemente respecto a otro. En un sistema de múltiples fuentes no es posible alinear todos los pares simultáneamente sin crear compromisos. La solución es establecer prioridades y aceptar los compromisos que corresponden a cada decisión.

**Alineación manual**
Seleccionar el canal a alinear. Activar solo ese canal junto al de referencia. Acercar la forma de onda al punto de referencia desplazando el clip hasta que los transitorios coincidan. Verificar en mono comparando antes y después.

**Alineación con plugins de autoalineación**
Los plugins de autoalineación (tipo Auto-Align) analizan las relaciones temporales entre canales y calculan los desplazamientos necesarios. Reducen significativamente el tiempo operativo. Dos condiciones para que funcionen bien: el plugin debe estar en el primer slot de inserción de cada canal, antes de cualquier procesador; y el análisis debe hacerse sobre una sección representativa y extensa del material, no sobre una selección corta o sobre una zona atípica del instrumento.

**Reducción de comb filtering por diferencia de nivel**
Cuando la diferencia de nivel entre dos señales coherentes supera aproximadamente 9,5 dB, el comb filtering se vuelve mínimo: la señal más débil no tiene suficiente energía para producir cancelaciones significativas al sumarse con la más fuerte. En algunos casos, reducir el nivel de un micrófono secundario (o aplicar una compuerta que lo baje durante los ataques del principal) puede ser más eficiente que alinear temporalmente. Esta estrategia se menciona aquí como criterio; las herramientas de compuerta y ducking se desarrollan en el Eje 4.

**Acción**
1. Confirmar que la polaridad está corregida antes de alinear. Alinear sobre una polaridad incorrecta empeora el resultado.
2. Definir la señal de referencia (en batería: el tambor) antes de empezar.
3. Alinear cada canal respecto a la referencia, uno a la vez.
4. Después de cada alineación, verificar en mono el resultado de la suma.
5. Si se usa un plugin: insertarlo en primer slot, escanear sobre la sección más representativa del material.
6. Verificar el resultado global con todos los canales activos en mono.

**Verificación**
Antes de alinear: reproducir en mono y notar el timbre del tambor (si es metálico, robótico o tiene coloración clara, hay comb filtering activo). Después de alinear: el timbre debe sonar más natural y directo. El comb filtering no siempre desaparece completamente (depende de las posiciones físicas de los micrófonos), pero debe reducirse claramente.

**Error frecuente**
Intentar que todos los pares posibles queden perfectamente alineados entre sí al mismo tiempo. En un sistema de múltiples micrófonos, la alineación perfecta de todos los pares simultáneos es matemáticamente imposible si las fuentes están en posiciones diferentes. El criterio es priorizar la relación más importante (tambor + overhead, por ejemplo) y aceptar el compromiso en las relaciones secundarias.

---

### 2-B3 · SPLIT DE FRECUENCIAS: CROSSOVER CORRECTO Y PRUEBA NULA

**Situación real**
El alumno quiere procesar el bajo eléctrico en dos capas: el subgrave con un compresor que le dé sustain y densidad, y la zona de definición (medios-bajos) con otro compresor más rápido que subraye el ataque. Para eso divide el bajo en dos bandas con un HPF y un LPF en ramas paralelas. Al sumarlas de nuevo, algo no cuadra: hay exceso de nivel en la zona de cruce y un cambio de timbre que no estaba en la señal original.

**Explicación operativa**
Un par HPF + LPF estándar con la misma frecuencia de corte no reconstruye correctamente la señal original al sumarse. Cada filtro atenúa –3 dB en la FC. Al sumar ambas ramas, la zona de cruce recibe el aporte de los dos filtros en ese punto: en lugar de cancelarse limpiamente o de sumar perfectamente, se produce un exceso o una coloración. Además, los filtros de fase estándar en cada rama rotan la fase de forma distinta, y esa diferencia afecta la reconstrucción.

La solución es el diseño Linkwitz-Riley (LR): en lugar de usar un único filtro por rama, se usan dos filtros en cascada de la misma pendiente en cada rama. El resultado es que ambas ramas tienen exactamente –6 dB en la FC y su suma reconstruye correctamente la señal original, con relación de fase coherente entre ramas.

**La prueba nula**
La verificación de la integridad del crossover se hace con la prueba nula:
1. Sumar ambas ramas del crossover.
2. Invertir la polaridad de una de las dos ramas.
3. Si el crossover está bien implementado, la suma se cancela: el resultado es silencio o señal de nivel mínimo.
4. Si no se cancela, hay un problema en el crossover: puede ser una diferencia de amplitud entre ramas en la zona de cruce, un problema de fase, o un diseño de filtro incorrecto.

Si la prueba nula no cancela, no tiene sentido seguir procesando las dos ramas por separado: el split está roto y cualquier procesamiento diferenciado quedará corrompido al sumar.

**Teoría mínima**
El crossover Linkwitz-Riley lleva el nombre de sus diseñadores, Siegfried Linkwitz y Russ Riley. Es el diseño estándar para divisores de frecuencia que requieren reconstrucción correcta de la suma. Las pendientes más comunes son LR-2 (12 dB/oct, dos filtros de 6 en cascada), LR-4 (24 dB/oct) y LR-8 (48 dB/oct).

**Acción**
1. Para dividir un instrumento en bandas de procesamiento paralelo: usar un par de filtros Linkwitz-Riley en lugar de un HPF + LPF sueltos.
2. Configurar la misma frecuencia de corte en ambas ramas.
3. Antes de procesar cada rama: hacer la prueba nula. Activar la suma de ambas ramas con una de ellas con polaridad invertida. Si el resultado es prácticamente silencio, el crossover está bien.
4. Solo si la prueba nula pasa: continuar con el procesamiento diferenciado de cada rama.

**Verificación**
Después de procesar cada rama y antes de hacer la suma final: escuchar la suma sin invertir ninguna rama y compararla con el bypass total de la señal original. El timbre y el nivel deben ser comparables. Si hay coloración evidente o exceso en la zona de cruce, el crossover tiene un problema.

**Error frecuente**
Usar un HPF y un LPF con la misma FC en ramas paralelas asumiendo que la suma reconstruirá el original. No lo hace. El resultado es un cambio de timbre en la zona de cruce que puede confundirse con un problema de EQ o de procesamiento de las ramas, cuando el problema está en el diseño del split.

---

### 2-C1 · NIVEL DE TRABAJO POR TIPO DE SEÑAL: PERCUSIVAS Y NO PERCUSIVAS

**Situación real**
El alumno tiene una sesión nueva. Los tracks de batería tienen clips que visualmente llenan casi toda la pista. Los tracks de sintetizador y voz se ven pequeños. El fader del bombo está a –5 dB para que no llene el bus. El compresor del bombo tiene el threshold a 0 dBFS y no hace nada. El compresor de la voz tiene el threshold a –12 dBFS y está comprimiendo constantemente aunque la dinámica de la voz parece normal. El problema es de gain staging: los niveles que llegan a los procesadores no son los que se asumen.

**Explicación operativa**
El gain staging por elemento asegura que cada procesador de la cadena recibe la señal en el nivel para el que fue diseñado. El primer paso es establecer el nivel de trabajo de cada canal antes de empezar a procesar.

Los criterios de nivel son distintos según el tipo de señal:

**Señales percusivas (batería, percusión, transitorios fuertes)**
Tienen factor de cresta alto: la diferencia entre el pico y el promedio puede ser de 10 dB o más. El VU subestima el nivel porque no captura los transitorios cortos. La referencia correcta es el medidor Peak. El objetivo es que los picos de los instrumentos percusivos no excedan –6 a –12 dBFS en el canal, dejando headroom suficiente para el procesamiento posterior. La referencia visual rápida: el clip ocupa aproximadamente un tercio de la altura del carril de la pista.

Un bombo integra más energía en el VU que un tambor aunque piquen igual, porque el contenido de baja frecuencia del bombo integra de forma diferente en el tiempo. No comparar nivel entre instrumentos percusivos de distinta naturaleza usando el VU como referencia.

**Señales no percusivas (voz, bajo, guitarras sostenidas, sintetizadores)**
Tienen dinámica más uniforme. El VU y el RMS son los medidores adecuados. El objetivo de trabajo es aproximadamente –20 dBFS RMS para el pasaje más denso y representativo del instrumento. La sección de referencia para medir no debe ser un fragmento de silencio ni una zona inusualmente suave: debe ser el pasaje más fuerte y representativo del material.

**La herramienta: Trim o ganancia de clip**
El nivel que llega a los procesadores se controla con la ganancia de clip o con un plugin de Trim en el primer slot de inserción, no con el fader de canal. El fader de canal pertenece al balance de mezcla: define la relación entre elementos en la suma. Si el fader se usa para compensar un nivel de trabajo bajo en la cadena, los procesadores están recibiendo señal insuficiente aunque el nivel del fader parezca correcto.

**Acción**
1. Para cada canal percusivo: leer el nivel con el medidor Peak. Ajustar la ganancia de clip o el Trim para que los picos del pasaje más representativo estén entre –6 y –12 dBFS.
2. Para cada canal no percusivo: leer el nivel con el VU o RMS. Ajustar para que el pasaje más representativo promedíe en torno a –20 dBFS RMS.
3. Realizar el ajuste con ganancia de clip o Trim (primer slot), no con el fader de canal.
4. Medir siempre sobre la sección más densa y representativa del instrumento.

**Verificación**
Con todos los canales ajustados al nivel de trabajo correcto y los faders en 0 dB: el bus principal debe mostrar un nivel razonable sin saturar. Si el bus ya está sobrecargado con los faders a 0, el problema está en el gain staging de los canales individuales. Si hay que subir el fader de un canal a +6 dB para que el instrumento se escuche en la mezcla, el gain staging de ese canal está mal.

**Error frecuente**
Ajustar el nivel de trabajo de un canal percusivo usando el VU como referencia. Una batería puede mostrar –10 dBVU mientras sus picos llegan a –2 dBFS. Si los procesadores están ajustados para recibir señal a –10 dBVU, cada transitorio está sobrecargando la entrada del compresor a razón de 8 dB. El compresor está recibiendo saturación antes de empezar a comprimir.

---

### 2-C2 · FADERS, TRIM Y ENVÍOS: ROLES DIFERENCIADOS EN LA CADENA

**Situación real**
El alumno sube el send de la voz al canal de reverb hasta que "se siente la reverb en la mezcla". El canal de reverb tiene el fader muy alto. La reverb suena bien en el estudio pero al día siguiente, con otros monitores, suena excesiva. El problema no es de nivel de reverb en la mezcla: es de nivel de entrada al procesador de reverb, que estaba recibiendo demasiada señal y operando fuera de su punto de trabajo.

**Explicación operativa**
En la cadena de audio hay tres tipos de control de nivel con funciones distintas que no son intercambiables:

**Trim / ganancia de clip**
Controla el nivel de señal que llega a la cadena de procesadores de un canal. Opera antes de los inserts. Su función es garantizar que los procesadores reciben señal dentro de su rango óptimo. No afecta el balance de la mezcla.

**Fader de canal**
Controla la relación de nivel entre ese canal y los demás en la suma. Opera después de los inserts (en la mayoría de las configuraciones). Su función es el balance de mezcla. No es la herramienta para ajustar el nivel de trabajo dentro de la cadena.

**Send (nivel de envío a efectos)**
Controla el nivel de señal que llega al canal de efecto (reverb, delay, chorus). Su función es calibrar la entrada al procesador del efecto. No es la herramienta para controlar cuánta reverb se escucha en la mezcla: eso lo controla el fader del canal de efecto.

La confusión más frecuente con los envíos: usar el send muy bajo para que la reverb "apenas se sienta", y subir el fader del canal de efecto para compensar. El procesador de reverb está recibiendo señal de entrada muy baja y su salida está siendo amplificada por el fader. Resultado: el modelado del procesador no opera en su rango correcto, y el nivel de reverb en la mezcla es difícil de controlar con precisión.

El flujo correcto:
- El send calibra la entrada al efecto al nivel de trabajo que el procesador espera (aproximadamente –20 dBFS RMS para la mayoría de los procesadores de efectos).
- El fader del canal de efecto controla cuánto de esa señal procesada entra en la mezcla.

**Acción**
1. Al configurar un envío a reverb o delay: ajustar el send para que el nivel de entrada al procesador esté en su rango de trabajo (verificar con el VU del plugin de efecto si lo tiene).
2. Controlar la cantidad de efecto en la mezcla con el fader del canal de efecto, no con el send.
3. Cuando varios canales envían al mismo canal de efecto: verificar que la suma de los envíos no satura la entrada del procesador.
4. Si el fader de un canal está significativamente alejado de 0 dB para que el instrumento suene bien en la mezcla: revisar el Trim de ese canal antes de mover el fader.

**Verificación**
El fader de canal debe operar como control de balance, no como compensación de gain staging. Si la mayoría de los faders están entre –5 y +5 dB respecto a 0, el gain staging es correcto. Si varios faders están a –15 dB o a +10 dB para que los instrumentos suenen bien, el nivel de trabajo de esos canales no está bien calibrado.

**Error frecuente**
Bajar el fader de un canal cuyo procesador (compresor, saturador) está recibiendo demasiada señal. El fader baja el nivel en la mezcla pero el procesador sigue recibiendo la misma señal de entrada. La corrección correcta es bajar el Trim o la ganancia de clip antes de los inserts.

---

### 2-D1 · AFINACIÓN, TIMING Y TRIGGERS: CRITERIOS DE INTERVENCIÓN

**Situación real**
El alumno tiene una grabación de voz con algunas notas que desafinan levemente. Una pista de bajo tiene notas sueltas con timing inconsistente respecto al bombo. Y una batería grabada en vivo tiene golpes donde la dinámica varía mucho entre uno y otro, dificultando la compresión coherente.

**Explicación operativa**
La corrección de interpretación opera sobre el material de la grabación antes de procesarlo con EQ, compresión o efectos. El criterio de intervención es siempre el mismo: corregir lo que afecta la integridad de la señal en el contexto de la mezcla, no perseguir la perfección técnica por principio.

**Corrección de afinación**
No toda desviación de la nota temperada es un error. Las desviaciones intencionales son parte del carácter de la voz o del instrumento: el vibrato, el portamento, las inflexiones melismáticas, la forma en que una nota se "busca" antes de aterrizar. Intervenir sobre esas desviaciones es destruir la interpretación, no mejorarla.

La intervención está justificada cuando la desviación produce incoherencia tonal en el contexto de la mezcla: una nota que disuena con la armonía, una frase que chirría contra los demás instrumentos, un intervalo que en el registro de la grabación produciría una disonancia no intencional.

Las herramientas de corrección de afinación permiten corrección automática (ajuste al semitono más cercano con velocidad de respuesta configurable) y corrección manual (nota por nota). La corrección automática a velocidad máxima elimina el carácter expresivo de la voz: el vibrato desaparece, el portamento se corta, cada nota aterriza directa sin transición. Puede ser apropiada para instrumentos sin expresión por desviación, pero destruye una voz con carácter propio.

**Corrección de timing**
La cuantización total ajusta todos los eventos exactamente al grid temporal. Elimina el groove humano. Una caja tocada por un baterista real no está en el grid: está ligeramente antes o después dependiendo de cómo el músico interpreta el tiempo. Esas variaciones son parte del feel de la grabación.

La cuantización suave aplica una corrección parcial: acerca los eventos al grid sin llegar exactamente, preservando parte de la variabilidad humana. El porcentaje de cuantización controla cuánto se acerca al grid. Para correcciones puntuales de notas con timing claramente problemático, la intervención nota por nota es más precisa que la cuantización global.

**Triggers y replacement de batería**
El trigger detecta los ataques de una pieza de batería y dispara un sample de reemplazo o refuerzo. Se usa cuando la grabación tiene inconsistencia dinámica que dificulta la compresión coherente, o cuando el carácter del sonido grabado no corresponde a lo que necesita la producción.

El blend entre señal original y sample permite combinar el realismo de la grabación con la consistencia del sample. La verificación crítica es que los disparos del trigger corresponden a golpes reales y no a bleed de otras piezas: un trigger disparado por el hi-hat que se cuela en el micrófono del tambor produce un sample del tambor en un momento donde no hubo golpe, arruinando el groove.

**Acción**
- **Afinación:** escuchar el material en el contexto de la mezcla. Identificar las notas que producen incoherencia tonal. Corregir solo esas notas, con el mínimo ajuste necesario. Preferir corrección manual en voces con carácter expresivo.
- **Timing:** identificar los eventos con timing problemático en el contexto del groove. Aplicar cuantización suave como operación global solo si el problema es generalizado. Para casos puntuales, corregir nota por nota.
- **Triggers:** configurar el trigger y revisar cada disparo contra el material de audio antes de hacer el blend. Desactivar los disparos que no corresponden a golpes reales.

**Verificación**
Después de cualquier corrección de interpretación: escuchar el material en el contexto de la mezcla completa. Si la corrección mejoró la coherencia tonal o rítmica sin quitarle carácter al instrumento, está bien. Si el instrumento suena mecánico, estéril o artificialmente perfecto, la corrección fue excesiva.

**Error frecuente**
Aplicar corrección de afinación automática a máxima velocidad a toda la voz principal como primera operación de la mezcla. El resultado es una voz técnicamente en tono pero sin identidad expresiva. Las desviaciones que hacían reconocible la interpretación han desaparecido.

---

## SECCIÓN 5 — DOSSIER CANÓNICO DE APOYO

---

### FILTRADO POR DECISIÓN

**Tipos de filtro y función**

| Filtro | Función | Uso en Eje 2 |
|---|---|---|
| HPF / Low Cut | Atenúa por debajo de la FC | Eliminar energía inútil de bajo registro |
| LPF / High Cut | Atenúa por encima de la FC | Control de ruido en alta frecuencia; perspectiva espacial |
| Band Pass | Deja pasar una banda entre dos FC | FX; análisis |
| Band Reject | Inverso del Band Pass | Limpiezas de banda ancha |
| Notch | Band Reject de Q alto | Resonancias puntuales |
| AllPass | Modifica fase sin tocar amplitud | Ajuste de relaciones de fase sin alterar espectro |

**Pendientes de filtro**

| Pendiente | Orden | Característica |
|---|---|---|
| 6 dB/oct | 1 polo | Suave; mínima rotación de fase |
| 12 dB/oct | 2 polos | Moderada |
| 18 dB/oct | 3 polos | Pronunciada |
| 24 dB/oct | 4 polos | Abrupta; mayor rotación de fase en la FC |

La frecuencia de corte es el punto de –3 dB. La atenuación comienza antes: a 6 dB/oct puede estar atenuando varias octavas por encima de la FC nominal. El analizador espectral en la señal de salida es la única referencia confiable sobre lo que el filtro hace realmente.

**Filtros de fase lineal**
Solo existen en el dominio digital. No producen rotación de fase. Introducen latencia (delay de grupo constante) y pre-ringing. El pre-ringing es audible en material percusivo: el sonido del filtro aparece antes del transitorio, como un eco previo. En material no percusivo el pre-ringing puede ser inaudible. Aplicar con criterio según el tipo de material.

**Tres criterios de filtrado**
El filtrado del Eje 2 responde a tres necesidades distintas:
1. Protección: eliminar energía sin contenido útil que carga la cadena (subsónicas, ruido de red, interferencias).
2. Registro: eliminar energía por debajo del registro real del instrumento.
3. Espacio: ceder territorio a otro elemento de mayor presencia en esa zona de frecuencias.

Los criterios 1 y 2 pueden evaluarse en solo. El criterio 3 solo puede evaluarse con la mezcla corriendo.

---

### CORRECCIÓN DE POLARIDAD Y ALINEACIÓN

**Procedimiento de verificación de polaridad en conjunto**
1. Par top/bottom del tambor: emparejar niveles → escuchar en mono → invertir el bottom → elegir la opción con más graves.
2. El grupo corregido vs overhead: sumar en mono → invertir el grupo → elegir la opción con más integración.
3. El conjunto vs micrófonos de sala o adicionales: repetir el proceso.

Cada paso puede modificar la relación con el siguiente. No hay una secuencia automática: verificar siempre en el conjunto después de cada corrección.

**Alineación temporal: criterio de prioridades en batería**

| Prioridad | Elemento de referencia | Justificación |
|---|---|---|
| 1ª | Tambor (top) | Define el groove y la producción |
| 2ª | Bombo | Base rítmica primaria |
| 3ª | Overheads | Perspectiva del kit; se alinean al tambor |
| 4ª | Resto | Hi-hat, room, otros micrófonos adicionales |

Cada alineación sobre un elemento puede crear un compromiso con otro. Definir las prioridades antes de empezar y aceptar los compromisos que resultan.

**Crossover Linkwitz-Riley**
Diseño de Siegfried Linkwitz y Russ Riley. Usa dos filtros de la misma pendiente en cascada por cada rama. FC resultante: –6 dB (en lugar de –3 dB de un filtro solo). Suma de ambas ramas: reconstrucción correcta del original con relación de fase coherente.

**Prueba nula para verificación de crossover**
Sumar ambas ramas → invertir polaridad de una → si el resultado es silencio o señal mínima, el crossover es correcto. Si la suma no cancela, hay problema de amplitud o fase en el crossover. No continuar con procesamiento diferenciado hasta resolver.

---

### GAIN STAGING POR ELEMENTO

**Referencias de nivel por tipo de señal**

| Tipo de señal | Medidor de referencia | Objetivo |
|---|---|---|
| Percusiva (batería, percusión) | Peak | Picos entre –6 y –12 dBFS |
| No percusiva (voz, bajo, sintetizador) | VU / RMS | ~–20 dBFS RMS en pasaje representativo |

**Roles diferenciados en la cadena**

| Herramienta | Función | No usar para |
|---|---|---|
| Trim / ganancia de clip | Calibrar nivel de entrada a la cadena de procesadores | Balance de mezcla |
| Fader de canal | Balance entre elementos en la suma | Compensar gain staging incorrecto |
| Send (envío a efecto) | Calibrar nivel de entrada al procesador del efecto | Controlar cuánto efecto hay en la mezcla |
| Fader del canal de efecto | Controlar la salida del efecto en la mezcla | Compensar nivel de entrada al efecto |

**Orden de inserción recomendado para el eje de integridad**
1. Trim / ganancia de clip
2. HPF / filtros de limpieza
3. Procesadores de polaridad y alineación
4. Procesadores dinámicos (compresores, compuertas)

La corrección del orden puede cambiar drásticamente el comportamiento del compresor: un HPF antes del compresor evita que las subsónicas disparen la compresión.

---

## SECCIÓN 6 — REGLAS PARA RAG

### Qué indexar

- Tipología de filtros: HPF, LPF, Notch, Band Reject, AllPass, fase lineal — con función y criterio de uso.
- Tabla de pendientes de filtro y rotación de fase asociada.
- Los tres criterios de filtrado (con reformulación propia, no como secuencia del autor fuente).
- Posición del HPF en la cadena: antes de procesadores dinámicos.
- Filtros de fase lineal: ventajas, compromiso de pre-ringing y criterio de uso por tipo de material.
- Procedimiento de corrección de polaridad: par top/bottom → verificación en conjunto.
- Alineación temporal: criterio de prioridades, método manual y con plugin.
- Crossover Linkwitz-Riley: diseño, propósito, prueba nula.
- Reducción de comb filtering por diferencia de nivel: criterio de umbral ~9,5 dB.
- Tabla de nivel de trabajo por tipo de señal.
- Roles diferenciados: Trim, fader, send — con tabla de uso correcto.
- Criterios de corrección de afinación: integridad vs expresión.
- Cuantización suave vs total: criterio de preservación de groove.
- Triggers: verificación de disparos antes del blend.

### Qué no indexar

- Uso creativo de filtros resonantes (barridos de síntesis, FX): pertenece a Eje 3 o Eje 5.
- Desarrollo técnico de compuertas y ducking como herramientas dinámicas: pertenece a Eje 4.
- EQ correctivo que modifica carácter tonal: pertenece a Eje 3.
- Ejemplos y anécdotas del autor fuente.
- Formulaciones orales marcadas del docente fuente.
- Secuencia pedagógica específica del curso fuente.

### Etiquetado por eje
`eje:2` para todo el contenido de esta unidad.

### Etiquetado por bloque interno
`bloque:2A` — filtrado.
`bloque:2B` — polaridad y alineación.
`bloque:2C` — gain staging.
`bloque:2D` — corrección de interpretación.

### Etiquetado por fase LDOV
- Diagnóstico que activa el eje: `LDOV:Leer` (viene de Eje 1).
- Decisión de filtrado, polaridad y gain staging: `LDOV:Decidir`.
- Ejecución del filtrado, corrección, alineación, calibración: `LDOV:Operar`.
- Verificación en solo, en mono y en mezcla: `LDOV:Verificar`.

### Teoría mínima vs ampliación opcional

**Teoría mínima obligatoria (prioridad alta):**
- HPF antes del compresor en la cadena.
- Tres criterios de filtrado — formulación propia.
- Procedimiento de polaridad top/bottom + verificación en conjunto.
- Criterio de referencia para alineación temporal.
- Prueba nula para crossover.
- Tabla de nivel de trabajo percusivo vs no percusivo.
- Roles diferenciados Trim / fader / send.

**Teoría de precisión útil (prioridad media):**
- Filtros de fase lineal y pre-ringing.
- Notch: criterio de Q mínimo necesario.
- AllPass: cuándo y cómo usarlo.
- Crossover LR: diseño de dos filtros en cascada.
- Cuantización suave vs total: porcentaje y criterio.

**Teoría profunda opcional (IA/FAQ/anexo):**
- Matemática de los tipos de filtro (Butterworth, Bessel, Chebyshev).
- Especificaciones técnicas del diseño Linkwitz-Riley.
- Algoritmos de herramientas de corrección de afinación (análisis de pitch, algoritmos de corrección).
- Comparación de plugins de autoalineación temporal.

---

## SECCIÓN 7 — REGLAS PARA GUIONES

### Partes que deben ser demostración

- **HPF y sus tres criterios:** sesión real con track de guitarra y analizador activo. Mostrar primero la energía en el analizador antes del corte; mover el punto de corte mientras la mezcla corre para el criterio 3.
- **Escuchar lo que se elimina:** activar la función de filtro invertido (o equivalente en el plugin) con la mezcla corriendo. El alumno debe escuchar la diferencia entre evaluar en solo y evaluar en contexto.
- **HPF antes vs después del compresor:** comparar el comportamiento del compresor en ambas posiciones con el mismo material. La diferencia en el comportamiento dinámico debe ser audible y visible en el gain reduction.
- **Corrección de polaridad paso a paso:** sesión de batería real. Mostrar antes y después de cada paso. El antes/después en mono debe ser claramente audible.
- **Prueba nula:** mostrar la suma antes de invertir, la inversión, y el resultado casi silencioso. Luego mostrar qué pasa con un crossover incorrecto.
- **Gain staging: antes y después:** sesión con tracks sin calibrar vs sesión calibrada. Mostrar el comportamiento de un compresor en ambos casos.

### Partes que pueden ser explicación a cámara

- Tipos de filtro y sus funciones: HPF, LPF, Notch, AllPass. Con gráfico de curva de respuesta.
- Filtros de fase lineal: concepto de pre-ringing con ejemplo visual de forma de onda.
- Roles diferenciados Trim / fader / send: con diagrama de señal de cadena.
- Criterios de corrección de interpretación: la distinción integridad / expresión puede ser a cámara con breve ejemplo.

### Partes que conviene enseñar con sesión real

- Corrección de polaridad en un kit de batería completo: todo el procedimiento en una sola sesión.
- Alineación temporal con plugin: insertar, escanear, verificar el antes y después en mono.
- Calibración de gain staging de una sesión desde cero: Trim por canal, verificación con medidores.
- Corrección de afinación en una voz: mostrar la diferencia entre corrección automática agresiva y corrección manual nota por nota.

### Partes que conviene mandar a la capa de apoyo

- Matemática de los tipos de filtro y sus diseños.
- Especificaciones técnicas del diseño Linkwitz-Riley.
- Comparativa extendida de plugins de autoalineación.
- Detalles de algoritmos de corrección de pitch.
- Cuantización avanzada: groove templates, corrección de timing por instrumento.

---

## SECCIÓN 8 — CAPA DE APOYO POR IA

### Temas que conviene dejar listos para profundización vía IA

- Cálculo de la frecuencia de primera cancelación del comb filtering y cómo ese dato informa la alineación necesaria.
- Comparación técnica entre distintos tipos de filtro (Butterworth, Bessel, Linkwitz-Riley) con sus propiedades de fase y amplitud.
- Algoritmos de herramientas de autoalineación temporal: cómo calculan el desplazamiento.
- Detalle del diseño Linkwitz-Riley: por qué dos filtros en cascada resuelven el problema de reconstrucción.
- Diferencia entre cuantización estándar, cuantización suave y groove templates.
- Herramientas de corrección de pitch: cómo funciona el análisis de pitch en Melodyne y similares.
- Triggers de batería: parámetros de configuración, sensibilidad, retardo, bleed rejection.
- Impacto del pre-ringing de los filtros de fase lineal: en qué materiales es audible y en cuáles no.

### Ejemplos de preguntas que el alumno podría hacerle a la IA

- "¿Por qué los filtros de fase lineal producen pre-ringing? ¿Cuándo ese pre-ringing es un problema real?"
- "Explícame con detalle cómo funciona el diseño de crossover Linkwitz-Riley y por qué reconstruye mejor que un par HPF/LPF simple."
- "¿Cómo determino con precisión a qué frecuencia colocar el HPF de un bajo eléctrico en una canción específica?"
- "¿Cuál es la diferencia operativa entre la corrección automática y la corrección manual en herramientas tipo Melodyne?"
- "Mi trigger está disparando en el bleed del hi-hat en el micrófono del tambor. ¿Qué parámetros ajusto para resolver eso?"
- "¿Cuándo conviene usar un AllPass en lugar de un rotor de fase para resolver problemas de relación de fase entre canales?"
- "Explícame qué significa cuantizar a un 60% de cuantización suave en términos prácticos."
- "Mi prueba nula no cancela completamente. ¿Qué puede estar fallando en el crossover?"

---

## SECCIÓN 9 — BLOQUES QUE REQUIEREN ATRIBUCIÓN EXPLÍCITA

### Técnica del filtro invertido como método de decisión
En las fuentes, esta técnica aparece como observación práctica y metodología operativa del autor fuente. Si se presenta en el curso como una técnica con nombre propio o como método identificable, requiere atribución. Si se integra como práctica general del campo sin presentarla como método específico, puede reformularse sin atribución.

Criterio adoptado en este eje: la técnica se presenta como práctica operativa general (escuchar lo que se elimina mientras la mezcla corre) sin presentarla como método con nombre propio. No requiere atribución en esa formulación.

### Crossover Linkwitz-Riley
El diseño lleva el nombre de sus autores, Siegfried Linkwitz y Russ Riley. Si se menciona por nombre en el curso:

**Formulación sugerida:**
> "El crossover Linkwitz-Riley, desarrollado por Siegfried Linkwitz y Russ Riley, resuelve el problema de reconstrucción del original al dividir una señal en dos bandas de procesamiento paralelo."

### Criterio de los tres tipos de filtrado
La lógica de los tres criterios (protección, registro, espacio) es una organización didáctica presente en el curso fuente. Se reformula aquí con terminología propia y sin reproducir el orden ni la formulación específica del autor fuente. No requiere atribución en la formulación adoptada.

### PDFs del autor fuente
Si en algún material de apoyo del curso se cita directamente cualquier formulación de los apuntes de filtros o de gain staging del autor fuente, esa cita requiere atribución puntual. La doctrina técnica contenida en esos documentos es de dominio general del campo y no requiere atribución cuando se reformula.

---

## SECCIÓN 10 — CONTINUIDAD CON OTROS EJES

**De dónde viene este eje**
El Eje 2 viene del **Eje 1 — Lectura de señales**.

El Eje 1 diagnosticó los problemas que el Eje 2 ahora resuelve. Las correcciones de polaridad nacen del diagnóstico de polaridad invertida. La alineación temporal nace del diagnóstico de comb filtering. El gain staging por elemento aplica el conocimiento de los medidores de nivel (VU, Peak, RMS) aprendidos en el Eje 1. Sin el diagnóstico del Eje 1, el Eje 2 opera sin información.

Además, el Eje 2 retoma el principio de gain staging conceptual introducido en el Eje 0-B y lo aplica track por track y procesador por procesador.

**A qué eje prepara**
El Eje 2 prepara directamente al **Eje 3 — Identidad espectral**.

La lógica del cruce: el Eje 3 usa el EQ para moldear el carácter tonal de los instrumentos. Si una señal tiene problemas de polaridad no corregidos, comb filtering activo, o nivel mal calibrado, el EQ del Eje 3 actuará sobre esos problemas sin poder separarlos del contenido real del instrumento. La señal limpia, alineada y calibrada del Eje 2 es la condición para que el EQ del Eje 3 trabaje sobre el instrumento, no sobre sus problemas.

**Nota de límite para el alumno**
El Eje 2 termina en la señal limpia, alineada y calibrada. El primer EQ que busca darle carácter tonal a un instrumento —hacer el bombo más profundo, aclarar la voz, dar presencia a la guitarra— ya es Eje 3. La línea está en la intención: si el filtro elimina lo que no debe estar, es Eje 2. Si el EQ construye lo que debe sonar, es Eje 3.

---

*KENTH Academy — Eje 2 · Versión de producción v1.0*
*Generado desde arquitectura congelada v1.0-final y paquete limpio Eje 2.*
