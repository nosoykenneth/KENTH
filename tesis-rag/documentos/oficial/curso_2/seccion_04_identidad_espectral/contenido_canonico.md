---
course_id: "2"
moodle_section_id: "5"
section_id: "5"
section_number: "4"
section_slug: "identidad_espectral"
section_title: "SECCIÓN 3: Identidad espectral"
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
legacy_axis: "Eje 3"  # solo trazabilidad de migración; NO usar como fuente
---

# EJE 3 — IDENTIDAD ESPECTRAL
### KENTH Academy · Mezcla y Masterización · Contenido Final de Curso

---

## SECCIÓN 1 — FUNCIÓN PRÁCTICA DEL EJE

El Eje 3 define el carácter tonal de cada elemento y construye la coherencia espectral de la mezcla como sistema.

El Eje 2 dejó las señales limpias, alineadas y calibradas. Esas señales tienen un espectro, pero no necesariamente un carácter definido ni una posición clara dentro del balance del conjunto. El Eje 3 es donde eso se trabaja.

El EQ es la herramienta central del eje. Pero usarlo bien requiere entender dos cosas antes de tocar un parámetro: qué tipo de problema se está resolviendo, y qué tipo de herramienta es la adecuada para ese problema.

El eje tiene cuatro dominios:

**Parámetros y tipología:** qué hace cada tipo de EQ, qué controla cada parámetro, y qué implica cada elección antes de mover nada.

**Criterio de decisión:** la diferencia entre EQ correctivo (eliminar lo que interfiere) y EQ estético (dar carácter a lo que suena). No son lo mismo ni se aplican igual.

**Modelado analógico:** por qué los EQs de circuito modelado suenan diferente a un EQ digital transparente, qué implica usarlos correctamente, y qué aporta cada familia clásica.

**EQ dinámico:** cuándo una campana estática no es la herramienta correcta y la ganancia debe actuar solo cuando el problema aparece.

**Límite del eje:** el Eje 3 trabaja el espectro por elemento y por grupo de instrumentos. El EQ del bus principal y el balance espectral global pertenecen al Eje 6. El Eje 3 no cierra la mezcla: define las identidades individuales que luego el Eje 6 integra como sistema.

---

## SECCIÓN 2 — QUÉ DEBE PODER HACER EL ALUMNO AL TERMINAR ESTE EJE

Al completar el Eje 3, el alumno es capaz de:

- Ajustar una campana de EQ con control deliberado de frecuencia central, ganancia y Q.
- Distinguir Q constante de Q proporcional y anticipar cómo se comportará la curva al cambiar la ganancia.
- Reconocer la diferencia entre un EQ simétrico y uno asimétrico, y qué implica para el boost y el cut.
- Usar un shelving con criterio, entendiendo dónde empieza realmente a actuar y qué zona del espectro afecta más allá de la frecuencia nominal.
- Elegir entre EQ gráfico, semiparamétrico y paramétrico según el objetivo de la intervención.
- Distinguir cuándo aplicar EQ correctivo y cuándo EQ estético, y adaptar el método de evaluación a cada caso.
- Usar la técnica de barrido para localizar resonancias o zonas problemáticas con precisión.
- Comparar el resultado de un EQ con bypass compensando el nivel percibido, sin confundir mejora tonal con aumento de volumen.
- Calibrar correctamente el nivel de entrada a un plugin de modelado analógico según su estándar.
- Identificar qué carácter tonal aporta cada familia de EQ analógico y elegir la herramienta según el objetivo.
- Usar la curva Pultec (boost + attenuate simultáneos en graves) con entendimiento de qué produce y por qué.
- Activar y configurar la función Split del canal SSL y entender qué resuelve.
- Configurar un EQ dinámico para resolver un problema frecuencial intermitente.
- Configurar un de-esser y verificar que la corrección no elimina la consonante por completo.

---

## SECCIÓN 3 — SUBSECCIONES FINALES DEL EJE

El orden dentro de cada bloque sigue la lógica de herramienta → criterio → aplicación. Los parámetros se presentan antes que los criterios de uso; los modelos analógicos van después de los criterios para que el alumno entienda qué espera del EQ antes de elegir qué herramienta usarlo; el EQ dinámico cierra el eje porque es la extensión del concepto de EQ hacia el dominio temporal.

**BLOQUE A — PARÁMETROS Y TIPOLOGÍA**

- **3-A1** · Peak/Bell y Shelving: parámetros esenciales de decisión
- **3-A2** · Gráfico, semiparamétrico y paramétrico: arquitecturas para cada objetivo

**BLOQUE B — CRITERIO DE DECISIÓN**

- **3-B1** · EQ correctivo vs EQ estético: la diferencia que organiza todo
- **3-B2** · EQ en contexto: evaluación, bypass y la trampa del nivel

**BLOQUE C — MODELADO ANALÓGICO**

- **3-C1** · THD, calibración y qué implica usar modelado analógico
- **3-C2** · Familias analógicas: API, Neve, SSL, Pultec

**BLOQUE D — EQ DINÁMICO**

- **3-D1** · EQ dinámico: cuándo una campana estática no alcanza
- **3-D2** · De-esser: sibilancia como problema intermitente

---

## SECCIÓN 4 — CURSO PRINCIPAL DEL EJE

---

### 3-A1 · PEAK/BELL Y SHELVING: PARÁMETROS ESENCIALES DE DECISIÓN

**Situación real**
El alumno inserta un EQ paramétrico en la voz. Quiere "dar presencia" y sube una campana en 3 kHz. El resultado suena diferente dependiendo del Q que usa. Con Q alto la voz suena metálica y estridente. Con Q bajo suena más abierta pero afecta una zona demasiado amplia. No sabe qué está controlando exactamente ni cómo elegir.

**Explicación operativa**
Una campana de EQ actúa en una zona del espectro definida por tres parámetros que trabajan juntos: la frecuencia donde actúa con mayor intensidad (frecuencia central), cuánta ganancia o atenuación aplica (ganancia), y cuán ancha o estrecha es la zona de influencia (Q o ancho de banda).

**Frecuencia central**
Es el punto de máxima ganancia o atenuación. Se calcula como la media geométrica de los extremos del ancho de banda, no como la media aritmética. En la práctica, el ajuste se hace al oído: la frecuencia nominal es una referencia, no una certeza matemática, especialmente en EQs de modelado analógico donde los valores impresos en el panel no siempre coinciden con exactitud con la acción del circuito.

**Q y ancho de banda**
Q = frecuencia central ÷ ancho de banda. Q alto significa campana estrecha: actúa en una zona pequeña del espectro con mayor selectividad. Q bajo significa campana ancha: afecta una zona extensa con mayor suavidad. Un Q de 0,7 produce una campana muy musical, casi un shelving. Un Q de 5 o más es quirúrgico: útil para correcciones muy localizadas.

Q y pendiente no son lo mismo. El Q afecta la forma de la parte superior de la campana. La pendiente de las laderas depende del diseño del filtro, y en muchos EQs no es un parámetro independiente.

**Q constante vs Q proporcional**
En un EQ con Q constante, la forma de la campana no cambia al modificar la ganancia: si se define Q 2 a +3 dB, también tendrá Q 2 a +9 dB. En un EQ con Q proporcional —frecuente en analógicos clásicos— a mayor ganancia, la parte superior de la campana se estrecha. El resultado es más musical a ganancias pequeñas (acción ancha y suave) y más selectivo a ganancias grandes (acción más concentrada). Es uno de los rasgos que hacen que los analógicos clásicos suenen diferente a un EQ digital transparente al mismo valor nominal.

**Simétrico vs asimétrico**
Un EQ simétrico produce la misma curva en boost y en cut a igual ganancia absoluta: +6 dB y –6 dB son imagen especular. Muchos EQs analógicos son asimétricos: la curva de cut es más estrecha y selectiva que la de boost. Esa asimetría tiene sentido musical: para corregir conviene precisión; para agregar color, conviene suavidad.

**Shelving**
A diferencia de la campana, el shelving no tiene un pico central: actúa sobre toda la banda por encima o por debajo de la frecuencia de corte. Un shelving de graves a 100 Hz sube o baja todo el contenido por debajo de ese punto. El detalle crítico: la frecuencia nominal no es donde empieza la acción, sino aproximadamente donde ya se ha alcanzado la mitad de la ganancia asignada (convención digital) o el punto de –3 dB del estante (convención analógica). La zona entre la frecuencia nominal y las frecuencias más alejadas también recibe una porción de la ganancia del shelving, que puede ser significativa. Un shelving de graves con +10 dB ajustado en 100 Hz estará dando varios dB también en la zona de 200–300 Hz.

El shelving resonante añade un pico antes del estante, lo que permite combinar peso general con énfasis selectivo en una zona. En graves puede ser útil y musical. En agudos, ese pico puede volverse artificial con rapidez.

**Acción**
1. Antes de mover el EQ: identificar qué problema se quiere resolver o qué carácter se quiere dar.
2. Elegir la frecuencia aproximada donde está el problema o donde se quiere la acción.
3. Ajustar el Q según la selectividad necesaria: estrecho para correcciones localizadas, ancho para color.
4. Aplicar la ganancia mínima necesaria. El EQ no es más efectivo por usar más ganancia.
5. Verificar con bypass compensando el nivel percibido.

**Verificación**
Al desactivar el EQ: el cambio debe ser claramente perceptible como diferencia tonal, no solo como diferencia de volumen. Si al bypass el instrumento suena mejor, el EQ estaba empeorando algo. Si al bypass suena igual de bien pero sin el problema que se quería resolver, el ajuste fue correcto.

**Error frecuente**
Subir una campana ancha en una zona "agradable" del espectro y aprobar el resultado sin compensar el nivel. Si ese mismo boost se compara con el bypass a nivel compensado, puede desaparecer completamente la diferencia percibida. El EQ no mejoró nada: solo subió el volumen.

---

### 3-A2 · GRÁFICO, SEMIPARAMÉTRICO Y PARAMÉTRICO: ARQUITECTURAS PARA CADA OBJETIVO

**Situación real**
El alumno tiene acceso a un gráfico de octava, a un semiparamétrico de dos bandas y a un paramétrico completo. Quiere saber cuándo usar cada uno. No es una pregunta de preferencia: es una pregunta de adecuación.

**Explicación operativa**
Los tres tipos de arquitectura resuelven cosas distintas. Usarlos incorrectamente no produce daño catastrófico, pero produce trabajo ineficiente: intentar una corrección quirúrgica con un gráfico de octava, o usar un paramétrico completo para algo que el gráfico resuelve en dos movimientos.

**EQ gráfico**
Las frecuencias y los anchos de banda los fija el fabricante. El usuario solo controla la ganancia de cada banda. Los gráficos de octava tienen diez bandas. Los de media octava y un tercio de octava tienen más bandas, más resolución y más interacción entre bandas adyacentes.

El gráfico de octava es el más musical: sus bandas amplias producen curvas suaves y evitan intervenciones excesivamente precisas que pueden resultar artificiales. Su limitación es que no permite aislar una frecuencia específica sin afectar las vecinas. Útil para ajustes de carácter global de un instrumento o de una sala.

**EQ semiparamétrico**
Dos controles: selección continua de frecuencia central dentro de un rango, y ganancia. Sin control de Q. El Q está fijado por el fabricante en un valor que funciona bien para la mayoría de las situaciones musicales. Es el EQ de barrido por excelencia: subir la ganancia y recorrer el espectro permite localizar rápidamente resonancias o zonas problemáticas. Una vez localizado el punto exacto, reducir la ganancia para cortar.

La técnica de barrido funciona porque el oído detecta mejor el exceso que la ausencia: a +10 dB en una zona problemática, esa zona se hace inmediatamente audible. A –10 dB en esa misma zona, la mejoría puede ser sutil. El semiparamétrico aprovecha esa asimetría perceptiva.

**EQ paramétrico**
Tres controles: frecuencia, ganancia y Q. El más versátil. Permite tanto correcciones de alta precisión (Q alto para aislar una resonancia puntual) como intervenciones musicales amplias (Q bajo para dar carácter a una zona). Es la herramienta adecuada cuando el problema o el objetivo está claramente identificado y se necesita control total sobre la intervención.

**Acción**
- Para ajustes de carácter global sin necesidad de precisión: gráfico de octava.
- Para localizar un problema espectral desconocido: semiparamétrico en modo barrido.
- Para corrección precisa de una resonancia o modelado tonal deliberado: paramétrico.

**Verificación**
Después de cualquier ajuste con gráfico: reproducir el instrumento en contexto y verificar que las bandas movidas no interactúan entre sí de forma no deseada. Con semiparamétrico o paramétrico: confirmar con el analizador que la curva actúa donde se pretende y no en una zona adyacente inesperada.

**Error frecuente**
Usar siempre el EQ más preciso disponible asumiendo que mayor control equivale a mejor resultado. Un gráfico de octava bien aplicado puede imprimir carácter en un instrumento con dos movimientos de fader. Un paramétrico mal usado puede producir un espectro artificialmente perforado con múltiples bandas de Q alto que no resuelven un problema real.

---

### 3-B1 · EQ CORRECTIVO VS EQ ESTÉTICO: LA DIFERENCIA QUE ORGANIZA TODO

**Situación real**
El alumno tiene un track de bajo que en el analizador muestra una resonancia prominente en 120 Hz que cambia el carácter de ciertas notas. También quiere que el bajo suene más redondo y cálido. Son dos problemas distintos que requieren dos tipos de intervención distintos.

**Explicación operativa**
La distinción entre EQ correctivo y EQ estético no es una categoría académica: es una guía práctica que define qué tipo de EQ usar, a qué Q, con qué ganancia, y cómo verificar si funcionó.

**EQ correctivo**
Resuelve un problema concreto: una resonancia, un exceso de energía en una zona específica, un enmascaramiento que impide que el instrumento se escuche en la mezcla, un contenido de alta frecuencia no deseado que distrae. Las características habituales:

- Sustractivo en la mayoría de los casos. El problema ya está en la señal: se trata de reducirlo, no de compensarlo con añadidos.
- Q relativamente alto para actuar de forma selectiva sobre la zona problemática sin afectar las frecuencias adyacentes útiles.
- La intervención puede evaluarse en solo si el problema es una resonancia del instrumento. Si el problema es enmascaramiento con otro elemento, la evaluación requiere el contexto de la mezcla.

**EQ estético**
Da carácter tonal deliberado al instrumento: peso, brillo, presencia, calidez, apertura. Las características habituales:

- Con frecuencia aditivo, aunque no necesariamente: recortar medios de una voz para que suene más abierta también es EQ estético.
- Q más bajo para intervenciones amplias y musicales.
- Requiere siempre verificación en el contexto de la mezcla. Lo que da carácter en solo puede resultar excesivo o incorrecto en el conjunto. Una voz que suena brillante y presente en solo puede resultar agresiva cuando está junto a guitarras con mucha presencia en la misma zona.

La frontera entre ambos tipos de EQ puede ser borrosa en casos intermedios, pero el criterio operativo es claro: si la intervención resuelve un problema, es correctiva; si modifica el timbre para que el instrumento funcione mejor en la mezcla, es estética.

**Enmascaramiento espectral**
Cuando dos instrumentos ocupan la misma zona del espectro con energía similar, se enmascaran mutuamente: cada uno reduce la audibilidad del otro en esa frecuencia. No es un problema de nivel absoluto: es un problema de densidad espectral en una zona específica. El EQ correctivo en estos casos opera cediendo espacio: una zona ligeramente recortada en el instrumento de menor importancia en ese rango abre la percepción del que tiene prioridad. Esa operación solo tiene sentido en el contexto de la mezcla, nunca en solo.

**Acción**
1. Antes de aplicar cualquier EQ: decidir si se está corrigiendo un problema o dando carácter.
2. Para EQ correctivo: buscar la zona problemática con barrido, cortar con Q adecuado al tamaño del problema, verificar con bypass.
3. Para EQ estético: evaluar en el contexto de la mezcla, no en solo. Aplicar con Q bajo y ganancia moderada. Verificar que el cambio persiste en el contexto y no es solo un artefacto de nivel.

**Verificación**
Un EQ correctivo bien hecho puede ser invisible: después del bypass, el problema que se quería resolver está presente y molesta; con el EQ activo, el problema no se escucha. Si el bypass suena tan bien como el EQ activo, el problema no existía o no era relevante en el contexto.

Un EQ estético bien hecho cambia el carácter del instrumento de forma audible y musical en el contexto de la mezcla, no solo en solo.

**Error frecuente**
Aplicar EQ estético aditivo extenso en solo del instrumento y luego sumarlo a la mezcla esperando que el resultado sea bueno. El EQ que suena bien en solo puede crear exactamente el enmascaramiento que se quería evitar cuando el instrumento se suma con los demás. La mezcla no es la suma de instrumentos bien ecualidados en solo: es un sistema en el que el EQ de cada elemento depende del EQ de los demás.

---

### 3-B2 · EQ EN CONTEXTO: EVALUACIÓN, BYPASS Y LA TRAMPA DEL NIVEL

**Situación real**
El alumno aplica EQ en un track de guitarra. Con el EQ activo suena mejor. Hace bypass. Con bypass también suena bien, tal vez incluso un poco mejor. No sabe qué pasó.

**Explicación operativa**
El oído tiene una tendencia bien documentada: percibe el nivel más alto como sonido de mejor calidad cuando la diferencia es pequeña. Si se aplica un EQ con ganancia positiva neta —aunque sea moderada— y se compara con el bypass a nivel equivalente, la señal procesada suena "mejor" simplemente porque es más fuerte. Esa ilusión no es una mejora real del carácter tonal: es un artefacto de nivel.

Esta trampa afecta especialmente al EQ aditivo. Incluso insertar un plugin de modelado analógico sin mover ningún parámetro puede hacer que la señal suene "más cálida" o "más presente" simplemente porque la distorsión armónica del modelado añade energía a ciertas frecuencias y el nivel percibido aumenta levemente.

**Evaluación correcta del EQ**
La comparación válida es: EQ activo vs bypass a nivel percibido equivalente. Si el EQ tiene ganancia neta positiva, hay que bajar el nivel de salida del plugin (o del fader) en la misma cantidad antes de comparar. Solo así la comparación evalúa el cambio tonal, no el cambio de nivel.

**El test del bypass prolongado**
Después de trabajar con un EQ durante un tiempo, el oído se adapta al sonido procesado. Hacer bypass en ese momento puede sonar peor simplemente por contraste. Una prueba más fiable: hacer bypass, esperar unos segundos de escucha sin el EQ, y luego evaluar si el EQ activo realmente añade algo necesario o si solo era contraste.

**EQ en contexto vs en solo**
El EQ estético requiere verificación en el contexto de la mezcla. Esto no es solo un principio general: tiene consecuencias operativas concretas.

Si se construye el EQ de cada instrumento en solo y luego se suman, el resultado puede ser una mezcla con todos los instrumentos bien definidos individualmente pero con zonas de enmascaramiento grave. Cada instrumento que fue equalizado para "sonar bien" en solo puede estar ocupando exactamente el espacio de otro.

El criterio práctico: aplicar el EQ estético con la mezcla corriendo. Ajustar escuchando el instrumento en relación con los demás. Hacer bypass y comparar en el contexto completo, no en solo.

**Acción**
1. Al comparar con bypass: compensar el nivel percibido antes de juzgar.
2. Para EQ aditivo: reducir el output del plugin en la misma cantidad de ganancia que se añadió neta antes de hacer bypass.
3. Para EQ estético: evaluar siempre con la mezcla corriendo, no en solo.
4. Si al bypass el instrumento suena mejor en la mezcla, el EQ estaba introduciendo un problema, no resolviendo uno.

**Verificación**
Después de completar el EQ de un instrumento: activar y desactivar con la mezcla completa sonando. Si el bypass con nivel compensado no muestra una diferencia tonal clara, el EQ no estaba haciendo nada tonal: solo estaba cambiando el volumen. En ese caso, simplemente subir el fader es más transparente.

**Error frecuente**
Aprobar el resultado de un EQ en solo del instrumento y asumir que eso garantiza un buen resultado en la mezcla. El EQ estético que "suena bien en solo" puede estar construyendo exactamente el problema de enmascaramiento que después habrá que resolver con más EQ en otros canales, entrando en un ciclo de correcciones que podría haberse evitado trabajando en contexto desde el inicio.

---

### 3-C1 · THD, CALIBRACIÓN Y QUÉ IMPLICA USAR MODELADO ANALÓGICO

**Situación real**
El alumno inserta un plugin de modelado de un EQ Neve 1073. Lo activa pero no mueve ningún parámetro. La señal ya suena diferente. Luego cambia el nivel de entrada al plugin y el carácter cambia de nuevo. No entiende qué está controlando.

**Explicación operativa**
Un EQ de modelado analógico no es solo la curva de ecualización del hardware original. Es también la distorsión armónica (THD) que el circuito original produce al trabajar, el comportamiento no lineal de sus componentes, y el comportamiento específico del transformador de entrada y salida.

Esos elementos no son defectos que el modelado trata de evitar: son la razón principal por la que los equipos analógicos suenan diferentes a un EQ digital transparente, y son exactamente lo que el modelado intenta replicar.

**Distorsión armónica**
Cuando una señal pasa por un circuito no lineal, genera frecuencias adicionales que son múltiplos enteros de la frecuencia original (armónicos). El segundo armónico (el doble de la frecuencia fundamental) produce una sensación de calidez y musicalidad. El tercer armónico y los siguientes impares producen una sensación más brillante y agresiva. Los circuitos analógicos generan combinaciones distintas de estos armónicos según su diseño.

La cantidad de distorsión armónica generada depende del nivel de la señal que recibe el circuito. A mayor nivel de entrada, más distorsión. Esto significa que el nivel de entrada al plugin de modelado no es un parámetro indiferente: cambia el carácter del procesamiento.

**Calibración del nivel de entrada**
Cada plugin de modelado analógico tiene un punto de trabajo para el que fue diseñado, definido según el estándar de calibración que emula (AES o EBU, ya vistos en Eje 0-B y Eje 1). Si el nivel de entrada al plugin es significativamente diferente al del punto de calibración, el modelado no opera como fue concebido. Puede sonar con menos carácter (si la señal llega demasiado baja) o con demasiada distorsión (si llega demasiado alta).

Antes de usar cualquier plugin de modelado analógico: verificar qué estándar de calibración implementa y calibrar el nivel de la sesión en consecuencia. Esto ya fue establecido en el gain staging del Eje 2; el Eje 3 lo retoma como requisito previo para que el modelado funcione correctamente.

**Los valores del panel no son exactos**
En los equipos analógicos originales, los valores impresos en el panel (frecuencias, ganancias) no son precisos en el sentido matemático de un EQ digital. Son referencias del fabricante que se interpretan con el oído, no con una calculadora. Los modelados heredan esa característica: dos plugins que modelan el mismo equipo de distintos desarrolladores pueden sonar diferente porque el modelado incluye decisiones de interpretación del comportamiento del hardware.

**Acción**
1. Al insertar un plugin de modelado analógico: verificar el estándar de calibración del plugin (AES: 0 VU = –20 dBFS; EBU: 0 VU = –18 dBFS).
2. Calibrar el nivel de entrada al plugin según ese estándar, usando el gain staging del canal (Trim, no fader).
3. Evaluar el carácter del plugin con un pasaje representativo del instrumento antes de ajustar cualquier parámetro.
4. Recordar que los valores nominales del panel son referencias de partida para el oído, no certezas numéricas.

**Verificación**
Con el plugin activo pero sin parámetros ajustados: comparar con bypass a nivel percibido equivalente. Si ya hay una diferencia de carácter apreciable (calidez, densidad, suavidad de agudos), el modelado está funcionando y el nivel de entrada es adecuado. Si no hay diferencia apreciable, el nivel puede estar demasiado bajo para que el modelado genere distorsión armónica significativa.

**Error frecuente**
Usar el mismo nivel de entrada para todos los plugins de modelado analógico sin verificar el estándar de calibración de cada uno. Un plugin calibrado a AES espera señal a –20 dBFS. Uno calibrado a EBU espera –18 dBFS. Dos dB de diferencia en el punto de trabajo cambia el carácter del modelado y puede producir resultados inconsistentes entre distintos plugins en la misma sesión.

---

### 3-C2 · FAMILIAS ANALÓGICAS: API, NEVE, SSL, PULTEC

**Situación real**
El alumno tiene acceso a modelados de distintas familias analógicas y no sabe cuál usar para qué. No quiere memorizarlos todos: quiere un criterio para elegir según el objetivo.

**Explicación operativa**
Cada familia de EQ analógico tiene un carácter que resulta de sus decisiones de diseño: el tipo de circuito (transistor, válvula, transformadores), las frecuencias disponibles, el comportamiento del Q proporcional, y la cantidad y tipo de distorsión armónica que genera. Conocer esas diferencias permite elegir la herramienta según lo que se necesita, no por familiaridad o hábito.

**API 550A y 550B**
La familia API (Audio Precision Instruments) tiene un carácter marcado en medios y un impacto pronunciado en graves. El 550A tiene tres bandas con frecuencias fijas por pasos, más un HPF. El 550B tiene cuatro bandas con más opciones de frecuencia. Ambos trabajan con Q proporcional.

Su carácter los hace adecuados para instrumentos que necesitan frontalidad: batería (especialmente caja y overheads), guitarras eléctricas, voces con presencia directa. La familia API no es sutil: si se quiere que algo "esté delante" en la mezcla, un EQ de esta familia puede construir esa percepción.

**Neve 1073, 1084 y 1081**
La familia Neve (AMS Neve) tiene un carácter opuesto a API en los extremos espectrales: agudos densos y suaves, graves con cuerpo pero sin impacto agresivo. El 1073 es el modelo de tres bandas con HPF; el 1084 y el 1081 amplían la flexibilidad con más frecuencias disponibles y opciones adicionales de Q.

El carácter Neve hace que los instrumentos suenen con calidez y cuerpo sin agresividad. Es adecuado para voces que necesitan brillo sin sibilancia, cuerdas, coros, producciones de rango dinámico amplio. Donde la familia API empuja hacia adelante, la familia Neve envuelve sin herir.

**SSL E y G — canal completo con Split**
El canal SSL (Solid State Logic) incluye EQ y dinámica en un único strip. Es un EQ versátil con carácter propio más neutro que API o Neve. Su particularidad más operativamente importante para la mezcla no es solo su curva sino la función **Split**.

El Split define el orden de procesamiento dentro del canal:
- **Split desactivado:** la señal entra → dinámica → filtros/EQ.
- **Split activado:** la señal entra → filtros → dinámica → EQ.

Con Split activo, el compresor del canal recibe la señal ya filtrada: no reacciona a las subsónicas ni a contenido que los filtros van a eliminar. Es el mismo principio que la posición del HPF antes del compresor vista en el Eje 2, implementado dentro del canal.

La función **dynamic sidechain** del SSL envía la señal del EQ al detector del compresor sin que el EQ se escuche en la señal de salida. Esto permite que el compresor reaccione selectivamente en frecuencia sin colorear la señal con el EQ de sidechain.

**Pultec EQP-1A**
El EQP-1A (Pulse Techniques) es un ecualizador pasivo con etapa valvular posterior. La sección de graves opera con frecuencias fijas por pasos (20, 30, 60, 100 Hz) y tiene dos controles independientes: boost y attenuate. Son dos circuitos distintos, no el mismo con signo opuesto.

La **curva Pultec** resulta de activar boost y attenuate simultáneamente en la misma frecuencia de graves. Las pendientes de los dos circuitos son asimétricas: el boost empieza antes (cubre una zona más baja) y el attenuate empieza después (actúa más arriba). El resultado es un énfasis en la zona elegida de graves con una limpieza en la octava siguiente. Esa limpieza es lo que hace que los graves del Pultec suenen definidos en lugar de embarrados: la energía turbia de los medios-bajos se reduce mientras el grave fundamental se refuerza.

Relación aproximada: boost en 100 Hz genera limpieza en torno a 1 kHz; boost en 60 Hz genera limpieza en torno a 600 Hz; boost en 30 Hz genera limpieza en torno a 300 Hz.

La sección de agudos del EQP-1A tiene una advertencia de seguridad real: en modo sharp con boost y attenuate simultáneos, pueden generarse picos de 20–25 dB que no están indicados visualmente en el panel. Antes de usar configuraciones extremas en agudos: verificar el nivel real del pico con el analizador. El riesgo para los transductores es real.

**Pultec MQ-5**
El MQ-5 opera en la zona de medios con una estructura de tres bandas: campana aditiva, campana sustractiva, campana aditiva. La interacción entre ellas produce una curva de contraste en la zona media del espectro. Útil para situaciones donde se quiere resaltar una parte de los medios limpiando la zona adyacente.

**Acción**
- Instrumento que necesita frontalidad y presencia directa → familia API.
- Instrumento que necesita cuerpo y brillo sin agresividad → familia Neve.
- Canal completo con integración EQ + dinámica y control de orden de procesamiento → SSL con Split correctamente configurado.
- Graves de programa que necesitan peso sin turbiedad → Pultec EQP-1A con curva boost + attenuate.
- Corrección y color en zona de medios con contraste espectral → Pultec MQ-5.

**Verificación**
Después de aplicar modelado analógico: comparar el carácter del resultado con el objetivo definido antes de insertar el plugin. Si se buscaba calidez y el resultado es agresividad, la familia elegida puede no ser la adecuada para ese instrumento en ese contexto. Cambiar de familia antes de tratar de compensar con parámetros.

**Error frecuente**
Elegir el plugin de modelado por familiaridad o por nombre reconocido sin considerar el carácter que aporta. Un EQ Neve en una batería donde se necesita impacto directo puede requerir el doble de trabajo para llegar al resultado que un EQ de familia API alcanza en dos movimientos.

---

### 3-D1 · EQ DINÁMICO: CUÁNDO UNA CAMPANA ESTÁTICA NO ALCANZA

**Situación real**
El alumno tiene una guitarra eléctrica con una resonancia en 400 Hz que suena exagerada durante las notas sostenidas pero es aceptable durante el picking rápido. Si aplica una campana estática de –4 dB en 400 Hz, la resonancia se controla en las notas sostenidas pero la guitarra suena adelgazada durante el picking. El problema es intermitente; la solución estática no puede discriminar cuándo intervenir.

**Explicación operativa**
Un EQ dinámico es una campana o shelf que aplica ganancia o atenuación solo cuando la señal en esa frecuencia supera (o baja de) un umbral definido. Fuera de ese umbral, la campana no actúa: la señal pasa sin modificación en esa banda. Cuando el umbral se supera, la campana aplica su ganancia hasta un límite máximo definido por el parámetro de rango.

Es una herramienta espectral —pertenece al Eje 3— aunque tenga comportamiento temporal. La distinción con la compresión multibanda es estructural: el multibanda divide la señal con crossovers y aplica compresores con ratio a cada banda. El EQ dinámico aplica campanas con rango sin crossovers. El multibanda trabaja bien sobre zonas amplias del espectro con problemas generalizados; el EQ dinámico trabaja mejor sobre problemas frecuenciales puntuales e intermitentes.

**Parámetros del EQ dinámico**
- **Frecuencia:** igual que en cualquier campana de EQ.
- **Umbral (threshold):** nivel de la señal en esa frecuencia a partir del cual la campana empieza a actuar.
- **Rango (range):** ganancia máxima que puede aplicar la campana cuando se supera el umbral.
- **Attack y release:** algunos implementan estos parámetros para controlar la velocidad de respuesta. Si no están disponibles, el plugin los gestiona automáticamente.

**Cuándo usar EQ dinámico**
El criterio es simple: cuando el problema es intermitente. Si hay una resonancia que aparece en ciertas notas o en ciertos momentos del instrumento pero no en otros, el EQ estático es una solución de compromiso que puede mejorar los momentos problemáticos pero degradar los que estaban bien. El EQ dinámico actúa solo cuando el problema aparece.

Otros casos de uso: un exceso de graves en una voz que solo aparece en ciertas consonantes vocales; una zona de medios en un bajo eléctrico que se acumula en ciertas posiciones del instrumento; un brillo excesivo en una guitarra acústica que solo ocurre en las notas agudas.

**Acción**
1. Identificar la frecuencia del problema con la técnica de barrido (como en el EQ estático).
2. Insertar el EQ dinámico y posicionar la campana en esa frecuencia.
3. Ajustar el umbral: escuchar mientras el instrumento suena y bajar el umbral hasta que el EQ empiece a actuar en los momentos problemáticos sin actuar en los que están bien.
4. Ajustar el rango: la cantidad de atenuación que se aplica cuando el umbral se supera.
5. Verificar que durante los momentos no problemáticos el EQ no actúa.

**Verificación**
Reproducir el instrumento completo e ir viendo el gain reduction del EQ dinámico. El GR debe moverse solo durante los momentos donde el problema es audible. Si el GR se mueve constantemente, el umbral está demasiado bajo y el EQ está actuando como estático. Si nunca se mueve, el umbral está demasiado alto y el EQ no resuelve nada.

**Error frecuente**
Aplicar un EQ estático con corte amplio para resolver un problema intermitente. El resultado es un instrumento permanentemente recortado en esa zona, con un timbre más delgado o apagado incluso en los momentos donde la señal estaba bien. El EQ dinámico permite mantener el carácter del instrumento excepto cuando el problema aparece.

---

### 3-D2 · DE-ESSER: SIBILANCIA COMO PROBLEMA INTERMITENTE

**Situación real**
El alumno tiene una voz con sibilancias excesivas. Intenta resolverlo con un corte estático en 7–8 kHz. Las sibilancias mejoran, pero ahora la voz suena opaca y sin aire incluso entre las sibilantes. El EQ estático no puede discriminar cuándo hay sibilancia y cuándo no.

**Explicación operativa**
La sibilancia es por definición un fenómeno intermitente: ocurre en las consonantes sibilantes (S, Z, Ch) y no durante el resto de la voz. Un EQ estático no puede hacer esa distinción. La herramienta adecuada para un problema intermitente es una herramienta dinámica.

El de-esser es un EQ dinámico especializado en la banda de sibilancias. Su mecánica es la misma que el EQ dinámico: cuando la señal en la banda de sibilancia supera el umbral, se aplica atenuación. Cuando no supera el umbral (durante el resto de la voz), la señal pasa sin modificación en esa zona.

**Dos modos de operación**

**Modo Wide (o Broadband):** cuando la sibilancia supera el umbral, se reduce el nivel de toda la señal, no solo de la banda de sibilancia. La reducción de nivel también afecta las frecuencias fuera de la banda problemática. Es más agresivo pero puede sonar más natural en algunos casos porque el comportamiento del compresor es más familiar para el oído.

**Modo Split (o Bandwise):** cuando la sibilancia supera el umbral, solo se reduce la banda de la sibilancia. El resto de la señal no se ve afectada. Es más preciso y preserva mejor el carácter de la voz fuera de la zona sibilante.

**El exceso de corrección**
El error más frecuente en el uso del de-esser es eliminar completamente la consonante: la S se convierte en Z (lispy) o desaparece. La sibilancia es parte de la inteligibilidad de la voz. El objetivo del de-esser no es eliminarla: es reducirla al nivel donde deja de distraer sin hacer que la voz pierda claridad consonántica.

La verificación del de-esser debe hacerse siempre con el material corriendo en tiempo real, escuchando las consonantes antes y después de la corrección. El analizador y el GR son referencias secundarias: el criterio final es si la consonante suena natural o si ha perdido su carácter.

**Acción**
1. Identificar la zona de frecuencia de la sibilancia (habitualmente entre 5 y 10 kHz según la voz y el micrófono).
2. Ajustar el umbral del de-esser: empezar alto y bajar hasta que el GR empiece a moverse en las sibilantes problemáticas.
3. Ajustar el range o ratio: la cantidad de reducción aplicada.
4. Elegir el modo (Wide o Split) según cuál preserve mejor el carácter de la voz en los momentos no sibilantes.
5. Reproducir la voz completa y verificar que las consonantes corregidas siguen siendo inteligibles y naturales.

**Verificación**
Reproducir una frase con sibilantes. Activar y desactivar el de-esser en tiempo real. Con el de-esser activo: las sibilantes deben estar presentes pero sin destacar ni distraer. Si con el de-esser activo las consonantes suenan como Z o desaparecen, la corrección es excesiva: subir el umbral o reducir el range.

**Error frecuente**
Usar un EQ estático sustractivo amplio en la zona de sibilancia. Resuelve el problema cuando hay sibilancia pero introduce opacidad en los momentos donde la voz no es sibilante. El resultado es una voz consistentemente más opaca en la zona de presencia e inteligibilidad, que luego puede compensarse con más EQ aditivo —generando un ciclo de correcciones que podría haberse evitado con el de-esser desde el inicio.

---

## SECCIÓN 5 — DOSSIER CANÓNICO DE APOYO

---

### PARÁMETROS DE EQ

**Campana (Peak/Bell)**

| Parámetro | Definición | Criterio de uso |
|---|---|---|
| Frecuencia central (fc) | Punto de máxima ganancia o atenuación. fc = √(f1 × f2) | Ajustar al oído; el valor nominal es una referencia, no una certeza |
| Q | fc ÷ BW. Q alto = campana estrecha. Q bajo = campana ancha | Estrecho para corrección localizada; ancho para color musical |
| Ganancia | Cantidad de boost o cut aplicada | Usar la mínima necesaria; más ganancia no equivale a mejor resultado |
| Q constante | La forma de la campana no varía con la ganancia | Más predecible; habitual en EQ digital transparente |
| Q proporcional | A mayor ganancia, la parte superior de la campana se estrecha | Más musical a ganancias pequeñas; más selectivo a ganancias grandes. Habitual en analógicos |
| Simétrico | Boost y cut son imagen especular | Predecible; habitual en EQ digital |
| Asimétrico | Boost y cut tienen formas distintas | Cut más estrecho que boost; habitual en analógicos; más musical |

**Shelving**

La FC del shelving puede interpretarse de dos formas según el fabricante: punto de ganancia ÷ 2 (convención digital) o punto de –3 dB del estante (convención analógica). Las dos no coinciden. La ganancia del shelving no está completamente por debajo o por encima de la frecuencia nominal: afecta también las frecuencias vecinas. Un shelving de graves con +10 dB en 100 Hz aplica varios dB también en la zona de 200–300 Hz.

El shelving resonante introduce un pico antes del estante. Útil en graves para combinar peso general con énfasis selectivo. En agudos, el pico puede volverse artificialmente prominente.

**Tipos de arquitectura**

| Tipo | Control del usuario | Resolución | Uso |
|---|---|---|---|
| Gráfico | Solo ganancia (fc y Q fijos) | Por bandas de octava / media octava / tercio | Carácter global; ajustes amplios y musicales |
| Semiparamétrico | fc + ganancia (sin Q) | Continuo en un rango | Barrido para localizar problemas |
| Paramétrico | fc + ganancia + Q | Máxima | Corrección precisa y color deliberado |

---

### CRITERIOS DE DECISIÓN

**EQ correctivo vs EQ estético**

| Dimensión | Correctivo | Estético |
|---|---|---|
| Objetivo | Eliminar un problema | Dar carácter tonal |
| Tendencia | Sustractivo | Aditivo o sustractivo con propósito de timbre |
| Q habitual | Relativamente alto | Más bajo |
| Evaluación en solo | Válida si el problema es del instrumento | Insuficiente; requiere contexto |
| Verificación | Bypass con nivel compensado | Bypass con nivel compensado en contexto de mezcla |

**Trampa del nivel en EQ aditivo**
El oído tiende a percibir el nivel más alto como mejor calidad cuando la diferencia es pequeña. Antes de aprobar cualquier EQ aditivo: reducir el output del plugin en la cantidad de ganancia neta aplicada y comparar con bypass. Si la diferencia tonal desaparece, el EQ solo estaba subiendo el volumen.

**Enmascaramiento espectral**
Cuando dos instrumentos tienen energía similar en la misma zona frecuencial, se enmascaran mutuamente. La solución correctiva es ceder espacio en el instrumento de menor prioridad en esa zona. Esta operación solo tiene sentido con la mezcla completa sonando.

---

### MODELADO ANALÓGICO

**Distorsión armónica**
- Segundo armónico: cálido, musical, perceptualmente más consonante.
- Tercer armónico y superiores impares: más brillante y agresivo.
- La cantidad de THD depende del nivel de entrada al circuito.

**Calibración**
Verificar el estándar de calibración del plugin (AES: 0 VU = –20 dBFS; EBU: 0 VU = –18 dBFS) antes de usarlo. El gain staging del canal debe llevar la señal al punto de trabajo correcto del modelo.

**Perfiles de familias analógicas**

| Familia | Fabricante | Carácter | Uso típico en mezcla |
|---|---|---|---|
| API 550A | API Technologies | Medios presentes, graves con impacto directo | Batería, guitarras, voces con frontalidad |
| API 550B | API Technologies | Mismo carácter, 4 bandas y más frecuencias | Cuando se necesita más flexibilidad dentro del carácter API |
| API 560 | API Technologies | Gráfico de octava con firma API | Carácter amplio sin precisión paramétrica |
| Neve 1073 | AMS Neve | Agudos suaves, graves con cuerpo denso | Voces, cuerdas, producciones de amplio rango dinámico |
| Neve 1084 | AMS Neve | Neve con más frecuencias de agudos, botón High Q | Firma Neve con mayor control de banda |
| SSL E/G canal | Solid State Logic | Versátil; función Split y dynamic sidechain | Canal completo con control de orden EQ/dinámica |
| Pultec EQP-1A | Pulse Techniques | Pasivo valvular; curva Pultec en graves | Graves de programa; peso sin turbiedad |
| Pultec MQ-5 | Pulse Techniques | Tres bandas de medios en curva pico-dip-pico | Contraste espectral en zona media |

**Curva Pultec**
Boost + attenuate simultáneos en graves del EQP-1A. Las pendientes son asimétricas: el boost abarca una zona más baja y el attenuate actúa en la octava siguiente. Resultado: énfasis en la frecuencia elegida con limpieza en la octava superior.

| Boost | Limpieza aproximada |
|---|---|
| 100 Hz | ~1 kHz |
| 60 Hz | ~600 Hz |
| 30 Hz | ~300 Hz |

No es un shelving resonante: es el producto de la asimetría entre dos circuitos independientes.

**Advertencia de seguridad — Pultec agudos en modo sharp**
Con boost y attenuate simultáneos en modo sharp, pueden generarse picos de 20–25 dB no indicados visualmente en el panel. Verificar siempre con analizador antes de usar configuraciones extremas. Riesgo real para tweeter.

---

### EQ DINÁMICO

**EQ dinámico vs compresión multibanda**

| Herramienta | División de señal | Tipo de control | Uso adecuado |
|---|---|---|---|
| EQ dinámico | Sin crossovers | Campana con rango dinámico | Problemas frecuenciales puntuales e intermitentes |
| Compresión multibanda | Crossovers por banda | Compresor con ratio por banda | Control dinámico de zonas amplias del espectro |

**De-esser: modos de operación**

| Modo | Comportamiento | Cuándo usarlo |
|---|---|---|
| Wide / Broadband | Reduce toda la señal cuando se supera el umbral | Cuando el comportamiento de compresor general suena más natural |
| Split / Bandwise | Reduce solo la banda sibilante cuando se supera el umbral | Cuando se quiere preservar el carácter de la voz fuera de la zona sibilante |

---

## SECCIÓN 6 — REGLAS PARA RAG

### Qué indexar

- Parámetros de campana de EQ: frecuencia central, Q, BW, ganancia — con definiciones funcionales.
- Q constante vs Q proporcional: diferencia y consecuencia práctica.
- Simétrico vs asimétrico: diferencia y consecuencia práctica.
- Shelving: convención de FC digital vs analógica; zona de influencia más allá de la FC nominal.
- Shelving resonante: función y limitación en agudos.
- Tabla de tipos de arquitectura (gráfico, semiparamétrico, paramétrico) con criterio de uso.
- Técnica de barrido para localización de problemas espectrales.
- Distinción EQ correctivo vs EQ estético: tabla de características.
- Trampa del nivel en EQ aditivo: criterio de comparación con bypass compensado.
- EQ en contexto vs en solo: criterio y consecuencias.
- THD en modelado analógico: segundo armónico vs tercero; impacto del nivel de entrada.
- Calibración de plugins de modelado: AES vs EBU.
- Tabla de perfiles de familias analógicas con carácter y uso típico.
- Curva Pultec: mecanismo y tabla de relación boost/limpieza.
- Advertencia de seguridad Pultec en modo sharp.
- SSL Split: función y criterio de uso.
- Función dynamic sidechain del canal SSL.
- EQ dinámico vs multibanda: tabla de diferencias estructurales.
- De-esser: modos Wide y Split con criterio de elección.

### Qué no indexar

- Balance espectral global del mix bus: pertenece a Eje 6.
- Compresión multibanda con desarrollo de parámetros completos: pertenece a Eje 4.
- Metáforas y formulaciones del autor fuente (bloqueadas).
- Artículo del autor fuente sobre SSL.
- Expresiones comparativas API vs Neve del autor fuente.

### Etiquetado por eje
`eje:3` para todo el contenido de esta unidad.

### Etiquetado por bloque interno
`bloque:3A` — parámetros y tipología.
`bloque:3B` — criterios de decisión.
`bloque:3C` — modelado analógico.
`bloque:3D` — EQ dinámico y de-esser.

### Etiquetado por fase LDOV
- Diagnóstico de problemas espectrales con analizador y barrido: `LDOV:Leer`.
- Decisión de tipo de EQ, tipo de intervención y herramienta: `LDOV:Decidir`.
- Aplicación del EQ (campana, shelving, modelado, dinámico): `LDOV:Operar`.
- Verificación con bypass compensado, verificación en contexto, analizador: `LDOV:Verificar`.

### Teoría mínima vs ampliación opcional

**Teoría mínima obligatoria (prioridad alta):**
- Parámetros de campana: fc, Q, ganancia.
- Q constante vs proporcional — diferencia práctica.
- EQ correctivo vs estético — criterio de evaluación.
- Trampa del nivel: comparar con bypass compensado.
- THD en modelado y calibración de nivel.
- Curva Pultec: mecanismo y uso.
- EQ dinámico vs estático — criterio de elección.
- De-esser: dos modos y verificación de corrección.

**Teoría de precisión útil (prioridad media):**
- Simétrico vs asimétrico en analógicos.
- Shelving resonante y sus limitaciones.
- Diferencia entre familias analógicas con criterio de uso.
- SSL Split y dynamic sidechain.
- Advertencia de seguridad del Pultec en agudos.

**Teoría profunda opcional (IA/FAQ/anexo):**
- Matemática de la fc como media geométrica.
- Tipos de distorsión armónica (espectro de armónicos por tipo de circuito).
- Enmascaramiento espectral: threshold of masking, upward masking (psicoacústica).
- Batimientos y tonos de combinación.
- Comparativa técnica entre modelados de distintos desarrolladores del mismo equipo.

---

## SECCIÓN 7 — REGLAS PARA GUIONES

### Partes que deben ser demostración

- **Q bajo vs Q alto sobre el mismo instrumento:** mostrar el efecto de una campana a Q 0,7 y Q 5 en la misma frecuencia con la misma ganancia. La diferencia debe ser audible y visible en el analizador.
- **Q proporcional en acción:** mostrar cómo cambia la forma de la campana en un EQ analógico al modificar la ganancia (con analizador).
- **Trampa del nivel:** demostración en vivo de un EQ aditivo "que mejora" y la misma comparación con bypass a nivel compensado. La diferencia entre ambas comparaciones debe ser audible.
- **Técnica de barrido:** aplicar en una sesión real con un instrumento que tenga una resonancia identificable. Mostrar el proceso desde el boost hasta el corte.
- **EQ en solo vs en contexto:** mostrar el mismo EQ estético que suena "bien" en solo y luego el impacto en la mezcla (potencialmente problemático). Luego mostrar el ajuste correcto hecho en contexto.
- **Curva Pultec:** mostrar en el analizador la curva que produce boost + attenuate simultáneos, compararla con un shelving simple y escuchar la diferencia en un bajo o bombo.
- **SSL Split activado vs desactivado:** mostrar cómo el compresor del canal reacciona diferente con Split on/off ante una señal con subsónicas.
- **De-esser Wide vs Split:** demostración auditiva de ambos modos sobre una voz con sibilancias, incluyendo la comparación de sobrecoIrrección.

### Partes que pueden ser explicación a cámara

- Q constante vs Q proporcional: concepto con gráfico de curva.
- Simétrico vs asimétrico: explicación con visualización de curvas de boost y cut.
- THD en modelado analógico: segundo vs tercer armónico — descripción del fenómeno con gráfico.
- Diferencia estructural EQ dinámico vs multibanda: descripción con diagrama de señal.

### Partes que conviene enseñar con sesión real

- Aplicación de EQ correctivo en un kit de batería: identificar y resolver resonancias con la técnica de barrido.
- EQ estético de una voz con modelado analógico: calibración, aplicación y verificación en contexto de mezcla.
- Configuración de EQ dinámico en guitarra con resonancia intermitente.
- Configuración de de-esser en voz: ajuste de umbral y range, verificación de consonantes.

### Partes que conviene mandar a la capa de apoyo

- Matemática de la frecuencia central como media geométrica.
- Tipos de distorsión armónica y espectro de armónicos por tipo de circuito.
- Enmascaramiento espectral: psicoacústica detallada (threshold of masking, upward masking).
- Batimientos y tonos de combinación.
- Comparativa técnica entre distintos modelados del mismo equipo de distintos desarrolladores.
- Historia de los equipos clásicos y sus fabricantes.

---

## SECCIÓN 8 — CAPA DE APOYO POR IA

### Temas que conviene dejar listos para profundización vía IA

- Cálculo de la frecuencia central como media geométrica y por qué no coincide con la media aritmética.
- Tipos de distorsión armónica: segundo armónico vs tercer armónico, qué circuitos generan cuál.
- Enmascaramiento espectral: cómo funciona el threshold of masking y el upward masking.
- Batimientos y tonos de combinación: cuándo aparecen y cómo detectarlos.
- Diferencias técnicas entre distintos modelados del mismo equipo de distintos desarrolladores.
- Historia y características técnicas de los equipos analógicos clásicos (API, Neve, SSL, Pultec).
- Funcionamiento interno de la compresión multibanda y por qué difiere estructuralmente del EQ dinámico.
- Variantes del canal SSL E vs G y sus diferencias prácticas.

### Ejemplos de preguntas que el alumno podría hacerle a la IA

- "¿Por qué la frecuencia central de una campana de EQ es la media geométrica y no la aritmética?"
- "Explícame la diferencia entre el segundo y el tercer armónico en distorsión analógica y cómo afectan al carácter del sonido."
- "¿Qué es el enmascaramiento espectral y cómo influye en las decisiones de EQ en una mezcla densa?"
- "¿Cuándo conviene usar la curva Pultec en graves y cuándo un shelving simple es suficiente?"
- "¿Qué diferencia práctica hay entre el SSL E y el SSL G en el canal?"
- "Tengo una guitarra con una resonancia que solo aparece en las notas de la tercera cuerda. ¿Cómo configuro el EQ dinámico para resolver solo ese caso?"
- "¿Por qué el de-esser en modo Split a veces suena más natural que en modo Wide?"
- "Explícame cómo funciona la función dynamic sidechain del canal SSL y cuándo tiene sentido usarla."

---

## SECCIÓN 9 — BLOQUES QUE REQUIEREN ATRIBUCIÓN EXPLÍCITA

### Equipos analógicos — fabricantes
Los nombres de los equipos deben ir acompañados de atribución al fabricante cuando se presentan por primera vez:

- API 550A, 550B, 560 → API Technologies
- Neve 1073, 1084, 1081 → AMS Neve
- SSL E/G canal → Solid State Logic
- Pultec EQP-1A, MQ-5 → Pulse Techniques

Formulación sugerida de primera mención:
> "El [modelo] de [fabricante] es un ecualizador [descripción funcional breve]."

El análisis de su carácter tonal es doctrina general del campo y no requiere atribución al autor fuente, siempre que las descripciones se reformulen sin reproducir las metáforas y expresiones identificables del docente fuente (bloqueadas en Sección 4).

### Curva Pultec
El mecanismo de la curva Pultec (boost + attenuate simultáneos produciendo énfasis + limpieza) es doctrina técnica de dominio general, ampliamente documentada en fuentes independientes del campo. No requiere atribución al autor fuente. El equipo se nombra con atribución a Pulse Techniques como fabricante.

### Apunte de Ecualizadores 2020
Autoría: Pablo Rabinovich. La taxonomía de EQ y los parámetros son de dominio general del campo. No requieren atribución cuando se reformulan. Si se cita cualquier formulación directa del apunte, la cita requiere atribución puntual.

---

## SECCIÓN 10 — CONTINUIDAD CON OTROS EJES

**De dónde viene este eje**
El Eje 3 viene del **Eje 2 — Integridad de la señal**.

El Eje 2 entregó señales limpias, alineadas y calibradas. El Eje 3 opera sobre esas señales para definir su carácter tonal y su posición espectral en la mezcla. Sin la limpieza del Eje 2, el EQ del Eje 3 actuaría también sobre los problemas que quedaron sin resolver (resonancias no corregidas, comb filtering, nivel mal calibrado), mezclando intervenciones que deberían estar separadas.

El límite entre ejes está en la intención: si la intervención elimina lo que no debe estar, es Eje 2. Si la intervención modifica el timbre para construir el carácter del instrumento, es Eje 3.

**A qué eje prepara**
El Eje 3 prepara directamente al **Eje 4 — Energía y movimiento**.

La lógica del cruce: la compresión actúa sobre una señal con carácter tonal ya definido. Comprimir antes de ecualizar significa comprimir el espectro del problema, no el espectro del instrumento deseado. El compresor reacciona a la señal que recibe; si esa señal tiene zonas espectrales incorrectas, el compresor las integra en su cálculo de nivel y en su umbral de disparo.

Hay un cruce específico que debe declararse: el EQ dinámico y el de-esser (Eje 3) tienen comportamiento temporal, pero su lugar pedagógico es Eje 3 porque son herramientas espectrales. La compresión multibanda, aunque divide el espectro, es una herramienta dinámica y pertenece al Eje 4. El alumno debe conocer esa frontera antes de entrar al Eje 4 para no confundir las herramientas.

**Cruce con Eje 6**
El balance espectral global de la mezcla como sistema —el EQ del mix bus, la corrección tonal del programa completo— no se trabaja en el Eje 3. Pertenece al Eje 6. El Eje 3 define las identidades espectrales individuales; el Eje 6 las equilibra como conjunto.

---

*KENTH Academy — Eje 3 · Versión de producción v1.0*
*Generado desde arquitectura congelada v1.0-final y paquete limpio Eje 3.*
