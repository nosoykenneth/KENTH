# Guiones corregidos — Eje 7 · KENTH Academy · v2
*Revisión: auditoría final + corrección integral*

---

# E7-L01 — Qué sí es mastering y qué ya llegaste tarde a arreglar

## Rol de esta lección dentro del proceso completo

Esta lección abre el eje y fija la frontera de trabajo. Antes de tocar una cadena de mastering, el alumno tiene que entender qué problemas pertenecen al master y cuáles debieron resolverse en mezcla. Sin esa frontera, todo lo que viene después se usa mal.

## Objetivo del video

Fijar el alcance real del mastering y presentar sus tres etapas en el orden lógico: técnica, comercial y artística.

## Resultado que debería conseguir el alumno al terminar

El alumno puede mirar una mezcla terminada, distinguir si el problema que detecta es global o específico, y decidir si corresponde seguir en mastering o volver a mezcla.

## Situación práctica de partida

Llega una mezcla estéreo al proyecto de mastering. El alumno escucha que en ciertos compases hay demasiado grave, pero no sabe si el problema es del tema completo o de un instrumento concreto. Antes de ecualizar por impulso, tiene que decidir si el mastering puede intervenir sin romper algo que sí estaba bien.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: DAW con la mezcla estéreo importada. Ningún procesador insertado todavía. Reproducción activa.]*

El primer gesto en mastering no es insertar un plugin. Es decidir si el problema que se escucha pertenece al mastering o si ya llegaste tarde y habría que volver a la mezcla. Esa diferencia define todo lo que viene después.

### 2. Desarrollo paso a paso

**Distinguir problema global de problema específico**

*[EN PANTALLA: la mezcla reproduce. El docente escucha sin tocar nada.]*

Lo primero es escuchar el tema completo y hacerse una pregunta concreta: ¿lo que molesta afecta al programa entero o a un elemento puntual?

Si toda la canción tiene un exceso de graves, eso sí entra en mastering. Si lo que está mal es la guitarra en ciertos compases, la reverb de una voz o el ataque de un bombo concreto, eso es mezcla. En mastering no hay acceso al elemento aislado. Cualquier procesamiento le cae encima a todo el programa al mismo tiempo.

*[EN PANTALLA: tabla simple en pantalla — dos columnas: "Problema global: puede resolverse en mastering" / "Problema específico: pertenece a mezcla".]*

La clasificación práctica:
- **Problema global:** densidad general, balance tonal general, imagen general, nivel general, picos generales.
- **Problema específico:** un instrumento, una frase, una reverb puntual, una automatización, una mala decisión de paneo de un elemento.

Si el problema es específico, se anota y se devuelve. Si es global, se continúa.

**Las tres etapas del mastering y su lógica de orden**

*[EN PANTALLA: diagrama de flujo con las tres etapas: Técnica → Comercial → Artística.]*

El mastering sigue un orden lógico — no un dogma, sino una consecuencia de qué depende de qué:

**Etapa técnica:** se resuelven problemas formales de la señal antes de empujar nivel o color. Si hay un problema técnico y se satura o limita primero, se amplifica el problema.

**Etapa comercial:** se lleva el programa al nivel de distribución que necesita sin destruirlo. Esta etapa solo puede hacerse bien sobre una señal ya técnicamente sana.

**Etapa artística:** no siempre hace falta. Solo entra si el material pide un pequeño ajuste de carácter y si ese ajuste no está corrigiendo una mezcla mal hecha. Si la señal ya llegó bien, insistir en "hacer mastering" con procesamiento por inercia empieza a degradar algo que ya funcionaba.

**Nota de terminología:** las tres etapas se llaman en este curso Técnica, Comercial y Artística. Hay otras terminologías en circulación (Técnica / Estética / Comercial, por ejemplo) que corresponden a la misma lógica subyacente con nombres diferentes. La secuencia y la función son lo relevante; los nombres son referencias operativas.

**La regla de trabajo**

El mastering traduce un sistema ya terminado. No reconstruye una mezcla.

### 3. Teoría aplicada en el punto correcto

El mastering es la preparación del programa fonográfico para su distribución. Su rasgo operativo es que cualquier procesamiento afecta simultáneamente a todos los elementos de la mezcla. Por eso la distinción clave no es técnica sino de alcance: problema global versus problema específico.

El flujo técnica → comercial → artística tiene un orden con consecuencias: resolver primero los problemas formales garantiza que la limitación y el carácter operen sobre una señal sana. Invertir ese orden amplifica problemas existentes.

### 4. Criterio de decisión

Antes de decidir herramientas, se decide terreno de intervención. Si el problema es global, mastering tiene sentido. Si es específico, no. En otra canción, lo que parece un exceso de grave global puede venir de un synth puntual: ahí la decisión cambia y corresponde corregir la mezcla.

### 5. Errores frecuentes y falsas reglas

"Mastering es el lugar donde se termina de arreglar todo." No. El mastering traduce lo que ya estaba bien, no completa lo que estaba mal.

"Toda mezcla necesita una etapa artística visible." No. Si la mezcla llega bien, puede no hacer falta ningún procesamiento de carácter.

"Si el track llegó a mastering, cualquier problema ya debe resolverse ahí." No. A veces la decisión correcta es devolver a mezcla.

### 6. Cierre

Ahora que se sabe qué pertenece al mastering, tiene sentido preparar la señal. La siguiente lección arranca ahí: ajustar la entrada, revisar DC offset y distinguirlo de la asimetría de forma de onda.

---

# E7-L02 — Trimming, DC offset y asimetría

## Rol de esta lección dentro del proceso completo

Esta lección prepara físicamente la señal antes de la cadena. Es la puerta de entrada al mastering real: nivel correcto, forma de onda saneada y headroom útil preservado.

## Objetivo del video

Preparar la señal antes de cualquier cadena de mastering mediante trimming, diagnóstico de DC offset y corrección de asimetría cuando corresponda.

## Resultado que debería conseguir el alumno al terminar

El alumno puede abrir una mezcla, medir su nivel de entrada, corregir desplazamiento por continua y distinguirlo de una asimetría que requiere otro tipo de intervención.

## Situación práctica de partida

La mezcla llega muy arriba de nivel. Los picos rozan el techo y el LUFS integrado está demasiado alto para alimentar con criterio una cadena de mastering. Además, la forma de onda muestra comportamiento extraño y el alumno no sabe si está viendo DC offset o asimetría.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: mezcla importada. El medidor de pico muestra valores muy cerca de 0 dBFS. El LUFS integrado está alto.]*

Antes de hablar de compresión, EQ o limitadores, hay que dejar la señal lista para entrar a la cadena. Si la entrada ya viene mal calibrada, todo lo demás empieza torcido.

### 2. Desarrollo paso a paso

**Trimming: calibrar el nivel de entrada**

*[EN PANTALLA: el docente aplica Trim o ajusta el clip gain del archivo importado. No usa el Master Fader para esto. Los picos bajan. El LUFS integrado baja.]*

Se carga la mezcla y antes de insertar procesadores de carácter se leen las estadísticas y los medidores: picos, LUFS integrados y comportamiento visual de la forma de onda.

Si la mezcla llega demasiado arriba, se hace trimming con clip gain o trim del archivo, no con el Master Fader. Los procesadores necesitan trabajar dentro de un rango razonable, especialmente si se van a usar modelados analógicos. La referencia operativa: dejar la mezcla en torno a **–20 a –23 LUFSi** de sonoridad integrada, que es el rango donde la cadena de mastering tiene más espacio para operar.

**DC offset: qué es y cómo corregirlo**

*[EN PANTALLA: vista de la forma de onda. La onda entera está desplazada por encima o por debajo del eje de cero.]*

Si toda la señal está desplazada fuera del cero, eso no es un detalle estético. Reduce headroom útil, favorece clipping asimétrico y hace reaccionar de forma distinta a los procesadores dinámicos.

*[EN PANTALLA: el docente aplica un HPF muy bajo — 2 a 5 Hz — sobre la señal. La forma de onda vuelve a centrar su eje.]*

Si el valor es despreciable, no se toca nada. Si es claramente significativo, se corrige con un HPF a frecuencia muy baja o con una herramienta específica de eliminación de DC.

**Asimetría: diferente del DC offset**

*[EN PANTALLA: vista de la forma de onda. El eje está centrado, pero los picos de un semiciclo son claramente más altos que los del otro.]*

La asimetría no es lo mismo que el DC offset. Aquí la señal sí está centrada, pero los picos de un semiciclo son más altos que los del otro. Eso no se corrige con HPF. Lo que está mal no es una componente continua: es la forma en que se suman las fases de los componentes frecuenciales.

*[EN PANTALLA: un filtro AllPass insertado en la señal. La asimetría se reduce visualmente.]*

Si la asimetría está limitando el headroom de forma real, se usa un AllPass, no un HPF.

**Verificación**

*[EN PANTALLA: el docente revisa la forma de onda y las estadísticas después de las correcciones. Escucha el programa.]*

Se vuelve a mirar la forma de onda y se escucha. Si se resolvió offset, el eje de reposo volvió al centro. Si se corrigió asimetría, los picos quedan más equilibrados. Si no cambió nada útil, no se insiste.

### 3. Teoría aplicada en el punto correcto

El trimming es condición previa para que la cadena opere en su rango óptimo. El DC offset es desplazamiento de la forma de onda fuera del cero y se corrige con HPF muy bajo o herramienta específica. La asimetría es una distribución desigual de picos con la señal centrada y su corrección se apoya en AllPass. Son fenómenos distintos con correcciones distintas.

### 4. Criterio de decisión

La prioridad no es "mejorar sonido" todavía, sino darle condiciones estables a la cadena. Si el offset es mínimo, no conviene corregir por deporte. Si la asimetría no limita de verdad el headroom ni genera problema operativo, tampoco hace falta intervenir. La evidencia manda, no la apariencia.

### 5. Errores frecuentes y falsas reglas

"Toda mezcla se baja 6 dB y listo." No. Se mide y se decide cuánto hace falta.

"Si la forma de onda está rara, siempre es DC offset." No. Puede ser asimetría — diagnóstico diferente, corrección diferente.

"Un HPF en 5 Hz no hace daño nunca." Tampoco. Si no hay problema, no se meten procesos porque sí.

Usar el Master Fader para resolver el nivel de entrada a la cadena. Eso no sustituye el trimming.

### 6. Cierre

Con la señal ya calibrada y saneada, tiene sentido leerla en serio como programa completo. La siguiente lección hace justamente eso: diagnóstico global de nivel, fase e imagen y espectro antes de intervenir.

---

# E7-L03 — Diagnóstico global del programa

## Rol de esta lección dentro del proceso completo

Esta lección convierte la preparación en lectura. El alumno aprende a mirar el master como sistema completo antes de procesarlo.

## Objetivo del video

Leer nivel, fase e imagen y espectro del programa completo antes de aplicar cualquier corrección o procesamiento de mastering.

## Resultado que debería conseguir el alumno al terminar

El alumno puede armar una inspección técnica mínima del master y salir de ella con una lista de problemas reales, no supuestos.

## Situación práctica de partida

La señal ya está calibrada para entrar a la cadena. El riesgo ahora no es técnico de entrada, sino de intervención sin diagnóstico: tocar EQ, compresión o limitación sin haber identificado qué problema real existe en el programa.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: DAW con la mezcla calibrada lista. Ningún procesador activo todavía. Medidores abiertos.]*

El error más caro en mastering no suele ser no saber usar un limitador. Suele ser empezar a mover cosas antes de haber leído bien la señal completa.

### 2. Desarrollo paso a paso

**Nivel: picos, LUFS e integrado**

*[EN PANTALLA: medidor LUFS (ej. Youlean Loudness Meter o equivalente) y medidor de pico activos. Se reproduce el programa completo.]*

Se leen los medidores de nivel. Se quiere saber dónde están los picos, qué LUFS integrados trae el programa y cuál es la relación general entre densidad y techo. No se decide loudness final todavía: solo se establece desde dónde se parte.

**Fase e imagen: goniómetro y correlatómetro**

*[EN PANTALLA: plugin con vista de goniómetro y correlatómetro activos (ej. SPAN Plus, iZotope Insight, o equivalente). El programa reproduce.]*

Se abren goniómetro y correlatómetro. En mastering ya no se corrige un micrófono o un track: se observa el comportamiento estéreo del programa entero. Si aparece una imagen sesgada, un exceso lateral extraño o una correlación problemática en graves, se anota. No se corrige todavía sin entender la causa.

**Espectro: tres familias de problemas**

*[EN PANTALLA: analizador espectral (SPAN o equivalente) en modo de promediado moderado, escala logarítmica. El programa reproduce.]*

Se buscan tres familias de problemas: subsónicas inútiles por debajo del fundamento, resonancias globales y desequilibrios generales de balance tonal.

*[EN PANTALLA: el docente señala cada tipo de anomalía en el analizador mientras reproduce.]*

El analizador no reemplaza la escucha, pero ayuda a no inventarse problemas. Si hay una acumulación por debajo del fundamento, se ve. Si hay una zona que empuja demasiado en todo el tema, se ve. Si hay sibilancia residual en el programa completo, también se ve.

**La diferencia de escala**

Esta lectura ya no es por instrumento. Si se detecta algo y se sospecha que viene de un solo elemento, se marca como límite del mastering. Si afecta al sistema completo, se sigue adelante.

**Lista de diagnóstico**

*[EN PANTALLA: el docente toma notas o escribe en un documento de texto simple mientras escucha y lee. Cuatro categorías: qué requiere corrección técnica / qué podría requerir ajuste de imagen / qué no conviene tocar / qué no pertenece a esta etapa.]*

Al final de la inspección queda una lista concreta. Eso es lo que guía el procesamiento, no la intuición del momento.

### 3. Teoría aplicada en el punto correcto

El diagnóstico en mastering reutiliza la lógica del Eje 1 (nivel, fase y espectro), pero ahora a escala global sobre el programa completo. El análisis debe cubrir: LUFS integrados, pico, correlación, goniómetro y espectro para identificar subsónicas, balance general y posibles residuos de sibilancia o imagen problemática.

### 4. Criterio de decisión

En mastering una corrección equivocada castiga a todo el programa. Si el diagnóstico muestra que no hay problema real en una zona, no se toca esa zona. En otra canción, un desbalance lateral podría ser parte del arreglo y no un defecto. Lo que manda es si rompe traducción, estabilidad o coherencia, no si se aleja de una imagen "bonita".

### 5. Errores frecuentes y falsas reglas

"El mastering empieza con un EQ." No. Empieza con lectura.

"Si el analizador muestra algo feo, hay que corregirlo." No necesariamente. La pregunta es si ese "feo" es un problema real del programa o una característica de su arreglo.

"Si la correlación baja, hay que cerrar estéreo." Tampoco. Primero hay que entender si el comportamiento es musical, tolerable o problemático para traducción.

### 6. Cierre

Con el diagnóstico hecho, ya se puede separar lectura de intervención. La siguiente lección entra en la primera intervención real: corrección espectral general, pero solo cuando el diagnóstico la justifica.

---

# E7-L04 — Corrección espectral general en mastering

## Rol de esta lección dentro del proceso completo

Esta lección convierte el diagnóstico en primeras correcciones globales. Se resuelven problemas del programa completo sin invadir terreno que corresponde a mezcla.

## Objetivo del video

Aplicar HPF subsónico, controlar resonancias globales y corregir balance L/R solo cuando el análisis demuestra que hace falta.

## Resultado que debería conseguir el alumno al terminar

El alumno puede intervenir el espectro global del master con criterio, sabiendo cuándo corregir, cuándo no tocar y cuándo devolver a mezcla.

## Situación práctica de partida

El análisis mostró posibles subsónicas, una resonancia que atraviesa la canción y cierto desbalance lateral en graves. El alumno tiene que decidir qué sí es corrección general y qué ya sería intentar mezclar desde el master.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: lista de diagnóstico de la lección anterior visible. Analizador espectral activo. Programa en reproducción.]*

Ahora sí se empieza a corregir, pero con una condición: lo que se haga aquí tiene que resolver un problema del programa completo, no disimular una mezcla mal resuelta por elemento.

### 2. Desarrollo paso a paso

**HPF subsónico: solo si hay evidencia**

*[EN PANTALLA: analizador espectral con zoom en la zona subsónica — debajo de 30 Hz. El programa reproduce.]*

Se empieza por la zona subsónica. No se carga un HPF por reflejo. Primero se escucha y se observa el analizador: ¿hay energía real que no aporta contenido musical y solo está cargando el sistema? Si la curva cae de forma natural hacia abajo, no se toca. Si hay una acumulación o cola que se sostiene por debajo del fundamento, ahí sí se plantea un HPF suave.

*[EN PANTALLA: HPF aplicado con pendiente suave — no agresiva. Antes y después comparados en el analizador.]*

El HPF en mastering no se aplica por hábito. Se aplica por evidencia.

**Resonancias globales: estáticas vs. intermitentes**

*[EN PANTALLA: analizador con una resonancia visible — una frecuencia que sobresale en el espectro promediado. EQ paramétrico insertado.]*

Si una frecuencia empuja la mezcla completa de forma consistente, se usa EQ paramétrico con Q razonable.

*[EN PANTALLA: la misma resonancia en el analizador — ahora solo aparece en ciertos momentos. EQ dinámico insertado.]*

Si la molestia aparece solo a ratos, un EQ dinámico puede ser mejor, porque una campana fija dejaría un hueco permanente donde el problema no existe. En mastering, los cortes innecesarios quitan naturalidad al programa completo.

**Corrección localizada en Mid o Side**

*[EN PANTALLA: procesamiento M/S activo. El docente aísla el Mid y muestra que la resonancia vive principalmente ahí.]*

Si la resonancia o el problema espectral vive sobre todo en Mid o sobre todo en Side, el M/S permite corregir donde vive el problema sin castigar todo el campo estéreo.

**Balance L/R**

*[EN PANTALLA: goniómetro mostrando la imagen inclinada hacia un lado en la zona grave.]*

Si la mezcla se apoya más en un lado en la zona grave, puede recentrarse esa base con herramientas de mono maker o gestión de imagen por bandas. Pero aquí se hace una pausa: si el problema viene claramente de un paneo mal decidido en mezcla, no se maquilla en mastering salvo que no haya otra opción operativa.

**Verificación en cada paso**

*[EN PANTALLA: comparación antes/después a igualdad de nivel. El docente escucha el programa entero, no solo la zona corregida.]*

En cada corrección se compara antes y después a igualdad de nivel y se escucha el programa entero. Si la corrección resuelve el síntoma pero empobrece el carácter general, se retrocede.

### 3. Teoría aplicada en el punto correcto

Tres correcciones generales principales en esta etapa: HPF subsónico solo cuando el análisis muestra energía problemática por debajo del fundamento; resonancias globales corregibles con EQ paramétrico o dinámico según su estabilidad; y reequilibrio L/R en graves mediante mono maker o recentrado cuando el problema compromete traducción.

Si el origen es un elemento puntual, lo correcto sigue siendo mezcla.

### 4. Criterio de decisión

HPF, EQ estático, EQ dinámico o control de imagen se eligen según evidencia. Si el problema es continuo, el EQ estático puede servir. Si aparece por momentos, conviene dinámica. Si está localizado en el centro o en los laterales, M/S tiene sentido. En otra canción, la misma frecuencia puede ser parte del carácter. No se corrige por número, se corrige por función.

### 5. Errores frecuentes y falsas reglas

"Todo master lleva HPF subsónico." No.

"Si molesta una frecuencia, notch y listo." No en mastering, donde una corrección estrecha puede dejar el programa sin naturalidad.

"Si hay desbalance L/R, se arregla con imagen estéreo." Depende. Puede ser un problema de mezcla, no de master.

### 6. Cierre

Con la base espectral y lateral del programa corregida, tiene sentido trabajar dinámica de mastering con más control. La siguiente lección entra ahí: compresión en serie, paralela y ascendente.

---

# E7-L05 — Compresión en mastering: en serie, paralela y ascendente

## Rol de esta lección dentro del proceso completo

Esta lección introduce la gestión dinámica específica del mastering, donde la tarea no es comprimir un instrumento sino modelar la respuesta del programa completo.

## Objetivo del video

Comprimir en mastering por tareas diferenciadas y no por costumbre, usando serie, paralela o compresión ascendente según lo que el programa necesite.

## Resultado que debería conseguir el alumno al terminar

El alumno puede decidir si conviene una compresión escalonada, una capa paralela sutil o una intervención ascendente, y entender qué costo tiene cada opción.

## Situación práctica de partida

El master ya no tiene problemas técnicos evidentes, pero todavía necesita mayor consistencia dinámica o una sensación de densidad más estable antes de entrar a limitación. El alumno tiene que decidir cómo llegar ahí sin aplastar la mezcla.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: master en reproducción. El programa reproduce de forma razonablemente estable. No hay compresores en la cadena todavía.]*

En mastering no se comprime para "que suene más pro". Se comprime para una tarea concreta. Si no se sabe cuál es la tarea, cualquier compresor pedirá más y más reducción hasta arruinar la mezcla.

### 2. Desarrollo paso a paso

**¿Hace falta compresión antes del limitador?**

*[EN PANTALLA: el docente escucha el master sin compresión. Si la mezcla ya viene muy estable, puede no hacer falta añadir una etapa dinámica previa.]*

Lo primero es escuchar si realmente hace falta compresión previa al limitador. Si la mezcla ya viene muy estable y solo necesita techo comercial, quizá no se necesita sumar compresión. Si sí hace falta, la primera decisión no es ratio ni ataque: es qué tipo de compresión.

**Compresión en serie: dividir tareas**

*[EN PANTALLA: dos compresores en serie en la cadena del master. El primero con configuración más musical y suave. El segundo con menos ratio pero más precisión.]*

Si el programa necesita consistencia general y también mejor control de picos antes de la limitación, se prefiere compresión en serie. Un primer compresor más musical une el programa y lo estabiliza sin perseguir cada transitorio. Un segundo más preciso termina de ordenar los picos que quedan. Varios pasos pequeños suelen costar menos que una sola compresión grande.

**Compresión paralela: densidad sin aplastar**

*[EN PANTALLA: rama paralela con un compresor muy agresivo. El docente mezcla esa rama con el original.]*

Si lo que se busca es levantar detalle o densidad percibida sin aplanar tanto la señal principal, se prueba compresión paralela. Se mantiene la señal original y se mezcla una versión mucho más comprimida debajo. Si se hace con envolventes rápidas y agresivo, el costo puede ser aliasing o aspereza. La dosis y los tiempos importan más que en el contexto de mezcla de un solo canal.

**Compresión ascendente: levantar pasajes suaves**

Si lo que se busca es levantar pasajes suaves sin castigar los fuertes, la compresión ascendente puede ser el camino. Reduce la diferencia dinámica desde abajo, no desde arriba: no aplasta los momentos fuertes para acercarlos a los suaves, sino que eleva los suaves para acercarlos a los fuertes.

**Comparar siempre a nivel compensado**

*[EN PANTALLA: comparación antes/después de cada etapa con nivel igualado.]*

Cada vez que se prueba una de estas rutas, se compara a igualdad de nivel. Si la mejora desaparece al compensar loudness, no era una mejora: era volumen.

### 3. Teoría aplicada en el punto correcto

En mastering funcionan mejor varios pasos pequeños que saltos grandes. La compresión en serie con una primera etapa más musical y otra más precisa para picos es el enfoque más común. La compresión paralela puede subir densidad con costos distintos según los tiempos elegidos — envolventes rápidas pueden introducir aliasing o coloración. La compresión ascendente tiende a ser más transparente para levantar pasajes bajos sin afectar los picos.

### 4. Criterio de decisión

Serie cuando se necesita repartir tareas. Paralela cuando se quiere densidad sin cargar todo el peso sobre la ruta principal. Ascendente cuando el problema es la relación entre pasajes bajos y altos con menor aplastamiento. En otra canción, ninguna de las tres podría ser necesaria.

### 5. Errores frecuentes y falsas reglas

"Todo master profesional lleva dos compresores." No.

"La paralela siempre da densidad gratis." Tampoco; tiene costo.

"Si el limitador va a hacer loudness, la compresión previa no importa." Error. Una mala dinámica antes del limitador hace que el limitador trabaje peor y con más daño.

### 6. Cierre

Con la dinámica ya encaminada, queda una pregunta delicada: si además se quiere un poco de carácter, ¿cómo se suma sin usar saturación como maquillaje? La siguiente lección va a eso.

---

# E7-L06 — Saturación: carácter sin pasarte

## Rol de esta lección dentro del proceso completo

Esta lección añade la capa artística más sutil del eje. El alumno aprende a usar saturación como ajuste fino, no como recurso para esconder fallas previas.

## Objetivo del video

Usar saturación en mastering como herramienta de densidad y riqueza armónica controlada, evitando que se vuelva distorsión audible o autoengaño por nivel.

## Resultado que debería conseguir el alumno al terminar

El alumno puede probar saturación en mastering, compararla honestamente y decidir si aporta algo real o si solo está subiendo volumen y colorando de más.

## Situación práctica de partida

La señal ya está técnica y dinámicamente más estable, pero todavía se percibe algo seca o demasiado plana. El alumno considera una saturación sutil para sumar riqueza armónica, pero no quiere convertir el master en una distorsión disfrazada.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: master en reproducción. Plugin de saturación insertado con cantidad mínima activa.]*

La saturación en mastering no está para tapar una mezcla floja. Está, como mucho, para sumar un poco de densidad y armónicos si eso realmente mejora la traducción y el carácter del programa.

### 2. Desarrollo paso a paso

**Dosis deliberadamente baja**

*[EN PANTALLA: saturación con cantidad baja. El docente escucha.]*

Se activa la saturación con una dosis deliberadamente baja. No se busca escuchar distorsión como efecto. Se busca que el programa se sienta un poco más unido, más presente o con una riqueza armónica sutil, especialmente en pasajes que sin ella quedan demasiado austeros.

**Compensar nivel: la comparación honesta**

*[EN PANTALLA: el docente baja el nivel de salida del saturador para compensar. Hace bypass varias veces con nivel igualado.]*

Se compensa el nivel antes de comparar. Si la saturación levanta aunque sea un poco el volumen, la comparación queda sesgada. Con nivel igualado, se hace bypass varias veces. Si la mejora desaparece al compensar, era puro volumen. Si lo que queda es una sensación real de densidad, presencia o calor sin pérdida de limpieza, se continúa.

**Escuchar el costo**

*[EN PANTALLA: el docente sube gradualmente la saturación más allá del punto útil. Los agudos se vuelven más ásperos. El docente vuelve al punto de utilidad.]*

Si los agudos se vuelven ásperos, si el centro se espesa demasiado o si la mezcla pierde apertura, ya se excedió el punto útil. En mastering, el umbral de utilidad de la saturación es pequeño. La saturación no debería anunciarse sola.

**Lo que la saturación no reemplaza**

La saturación no reemplaza compresión, EQ ni limitación. Si se está usando saturación porque no se sabe cómo controlar picos, porque faltó compresión o porque la mezcla vino vacía, se le está cargando una tarea que no le corresponde.

### 3. Teoría aplicada en el punto correcto

La saturación en mastering añade riqueza armónica y densidad percibida mediante la generación de armónicos adicionales. El criterio operativo: si se escucha como distorsión, hay demasiada. La comparación debe hacerse siempre a igualdad de nivel. En mastering, lo correcto es que el cambio sea pequeño pero útil.

### 4. Criterio de decisión

Se usa saturación solo si, una vez resueltos problemas técnicos y dinámica, todavía falta una pequeña sensación de cohesión armónica o presencia. Si el material ya llegó con carácter suficiente, no se necesita. En una producción acústica o muy transparente, la mejor decisión puede ser no tocarla.

### 5. Errores frecuentes y falsas reglas

"Todo master mejora con un poco de saturación." No.

"Si no se oye claramente, no está haciendo nada." Tampoco. En mastering, a veces lo correcto es que el cambio sea pequeño.

"Saturación es compresión con otro nombre." No. Puede afectar densidad percibida, pero no sustituye tareas dinámicas específicas.

### 6. Cierre

Con carácter y dinámica ya encaminados, toca revisar cómo está distribuido el programa en el campo estéreo completo. La siguiente lección entra a Mid/Side e imagen del programa final.

---

# E7-L07 — Mid/Side e imagen del programa completo

## Rol de esta lección dentro del proceso completo

Esta lección trabaja la imagen estéreo del master ya consolidado. No construye espacio como en mezcla: corrige o ajusta el resultado final a escala global.

## Objetivo del video

Usar M/S e imagen estéreo en mastering sin invadir decisiones de mezcla ni desestabilizar los graves del programa.

## Resultado que debería conseguir el alumno al terminar

El alumno puede intervenir Mid y Side del master con criterio, distinguirlo del M/S de mezcla y decidir cuándo recentrar graves o abrir zonas superiores del espectro.

## Situación práctica de partida

El alumno escucha que el master está algo estrecho arriba o que los graves no se sienten firmes en el centro. También detecta que cierta molestia vive más en Mid que en Side. Necesita actuar sin desarmar el balance del programa.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: plugin M/S de mastering activo. Goniómetro visible. El programa reproduce.]*

Mid/Side en mastering no sirve para mezclar desde atrás. Sirve para corregir o ajustar el programa final cuando el centro y los laterales necesitan un trato distinto.

### 2. Desarrollo paso a paso

**Recordar el alcance del M/S en mastering**

*[EN PANTALLA: el docente señala el procesamiento M/S — Mid y Side claramente separados en el plugin.]*

Intervenir en Mid no significa mover una voz aislada: significa mover todo lo que comparte el centro del programa. Intervenir en Side significa mover todo lo lateral. El alcance es siempre global.

**Recentrar graves para más peso y estabilidad**

*[EN PANTALLA: el docente activa un procesamiento que mantiene los graves en mono o más cerca del centro. El goniómetro muestra más estabilidad en la zona baja.]*

Si los graves se sienten inestables, se prueba recentrarlos o mantenerlos en mono por debajo de una zona determinada. Eso suele dar más peso y estabilidad. No se hace porque sí: se hace si el programa lo necesita y si el diagnóstico confirmó ese comportamiento.

**Abrir levemente arriba si está justificado**

Si hay algo en medios o agudos que conviene abrir levemente para dar más aire, se hace con conservación. En mastering, abrir un poco arriba puede dar apertura, pero sin control puede debilitar el centro, arruinar compatibilidad o volver artificial la imagen.

**Corregir donde vive el problema**

*[EN PANTALLA: EQ M/S con corrección aplicada solo al Mid, sin tocar el Side.]*

Si se detectó una resonancia o dureza localizada más en Mid o más en Side durante el diagnóstico, se usa esa separación para corregir donde vive el problema, no en todo el programa.

*[EN PANTALLA: el docente alterna entre la escucha M/S y la escucha normal (reconstruida) y también colapsa a mono para verificar.]*

En cada paso se vuelve al mono y a la escucha normal para asegurar que no se está comprando apertura a cambio de perder solidez.

### 3. Teoría aplicada en el punto correcto

El M/S de mastering y el M/S de mezcla usan la misma mecánica de codificación/decodificación (introducida en el Eje 5), pero el contexto es radicalmente distinto: aquí el procesamiento opera sobre el programa completo entregado, no sobre una imagen en construcción. En mezcla todavía se puede volver a la pista. En mastering, no.

Se recomienda mantener graves más centrados para peso y estabilidad, y usar M/S cuando un problema está alojado en Mid o Side sin necesidad de castigar toda la imagen.

### 4. Criterio de decisión

Se elige M/S cuando el centro y los laterales no están pidiendo lo mismo. Si el programa está estable y natural, no hace falta tocar imagen. Si el problema está claramente en un elemento puntual, eso era mezcla. En otra canción, una imagen muy abierta puede ser parte del lenguaje estético y no requerir recentrado.

### 5. Errores frecuentes y falsas reglas

"En mastering siempre se abren los sides." No.

"Los graves siempre van en mono." Como regla universal, no. Depende del material y del problema.

"Si una resonancia está al centro, se arregla con EQ normal." Podría, pero M/S permite resolver sin afectar todo el campo estéreo si la evidencia lo justifica.

### 6. Cierre

Con imagen y centro bajo control, ya queda la etapa que más fácilmente se sobreusa: la limitación. La siguiente lección entra al limitador, al método delta y al control de True Peak.

---

# E7-L08 — Limitador, método delta y True Peak

## Rol de esta lección dentro del proceso completo

Esta lección aborda la etapa comercial del mastering. El programa se lleva a nivel de distribución controlando daño y techo real de salida.

## Objetivo del video

Llevar el programa al nivel comercial necesario con limitación controlada, usando método delta para escuchar el daño y verificando True Peak antes y después de codificación.

## Resultado que debería conseguir el alumno al terminar

El alumno puede configurar un limitador de mastering con criterio, entender la relación entre threshold y out ceiling, evaluar artefactos con método delta y verificar True Peak del archivo final.

## Situación práctica de partida

La mezcla ya está corregida, equilibrada y con la dinámica previa resuelta. Falta elevar el nivel de salida para distribución sin destruir transitorios, graves ni naturalidad del programa.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: limitador de mastering insertado al final de la cadena. Out ceiling y threshold visibles. El programa reproduce.]*

Aquí es donde más gente arruina el master. No por usar un limitador, sino por usarlo sin escuchar qué está sacrificando a cambio del nivel.

### 2. Desarrollo paso a paso

**Fijar el ceiling antes de mover el threshold**

*[EN PANTALLA: el docente fija el Out Ceiling del limitador primero — por ejemplo –1 dBTP. El threshold todavía está alto, sin actuar.]*

Se inserta el limitador al final de la cadena. Lo primero es fijar el Out Ceiling: hasta dónde puede salir la señal. Después se empieza a bajar el threshold para aumentar el nivel.

En la práctica, el threshold controla cuánto material llega al techo de salida: threshold más bajo = más señal comprimida contra el ceiling. El ceiling define el límite absoluto de salida.

**Escuchar mientras se sube nivel**

*[EN PANTALLA: el docente baja el threshold del limitador gradualmente. El GR empieza a aparecer. El docente escucha especialmente graves y transitorios.]*

Mientras sube el nivel, no se mira solo el medidor de LUFS. Se escucha especialmente graves, transitorios y sensación de respiración del tema. Si el grave se vuelve borroso o si el ataque pierde forma, el limitador ya está pagando el loudness con daño audible.

**Método delta: escuchar qué está destruyendo el limitador**

*[EN PANTALLA: el docente muestra cómo montar el método delta: (1) copia del bus del master pre-limitador; (2) inversión de polaridad en esa copia; (3) suma de la copia invertida con la salida del limitador. Lo que suena es la diferencia — el "delta".]*

El método delta consiste en restar lo que sale del limitador de lo que entra a él. El resultado es lo que el limitador está eliminando.

Implementación práctica: (1) duplicar el señal antes del limitador, (2) invertir la polaridad de esa copia, (3) sumarla con la salida del limitador. Lo que se oye en esa suma es exactamente lo que el limitador ha modificado.

*[EN PANTALLA: el docente escucha el delta. Si se oye solo picos aislados y material esperable, el limitador trabaja bien. Si se oye cuerpo, groove, graves útiles o información musical sostenida, se excedió el rango útil.]*

Si en el delta se escucha solo picos aislados o material esperable, se va bien. Si se empieza a oír cuerpo, groove, graves útiles o información musical sostenida, se está limitando demasiado.

**Verificar True Peak**

*[EN PANTALLA: medidor de True Peak activo (la mayoría de plugins de LUFS incluyen True Peak). El docente revisa el valor después de exportar o simular exportación.]*

No basta con ver el Sample Peak del proyecto. Se verifica el True Peak real, sobre todo si después hay codificación a AAC o MP3. El True Peak puede subir después de esa conversión.

*[EN PANTALLA: versión codificada del master abierta en el DAW o analizada con un medidor. True Peak de la versión codificada visible.]*

Se verifica también el archivo codificado cuando aplica, porque el True Peak puede superar el del WAV de entrega.

### 3. Teoría aplicada en el punto correcto

El limitador de mastering tiene threshold como control de cuánto entra a la zona de limitación y Out Ceiling como techo de salida. El método delta es una técnica estándar del campo para evaluar el daño introducido por la limitación. El True Peak mide los picos entre muestras que pueden superar el ceiling de muestra — especialmente relevante al codificar a formatos con pérdida.

### 4. Criterio de decisión

Se decide cuánto limitar según el destino, el género y lo que el programa tolera sin romperse. Si una producción acústica pierde vida rápido, no se persigue el mismo nivel que una producción electrónica densa. Si el delta empieza a devolver demasiada música y no solo exceso, ya se cruzó la línea.

### 5. Errores frecuentes y falsas reglas

"Más LUFS es mejor master." No.

"Si no clippea el ceiling, está bien." Tampoco. Se puede destruir la señal sin pasar el techo.

"El método delta es opcional." No si se quiere entender qué se está pagando por el loudness.

"Con ver el WAV basta para True Peak." No cuando habrá codificación posterior.

### 6. Cierre

Ya hay un master casi listo, pero todavía falta decidir el objetivo de loudness con criterio real y no con números memorizados. La siguiente lección entra a normalización de plataformas y criterio por género.

---

# E7-L09 — Targets de plataformas y criterio por género

## Rol de esta lección dentro del proceso completo

Esta lección contextualiza la etapa comercial. El alumno entiende que el loudness no se decide en abstracto, sino en función de plataforma, normalización y lenguaje del material.

## Objetivo del video

Decidir loudness de entrega entendiendo que las plataformas normalizan volumen y que el objetivo final depende del tipo de música y de cómo soporta esa densidad.

## Resultado que debería conseguir el alumno al terminar

El alumno puede interpretar targets de plataformas sin tomarlos como mandamientos rígidos y elegir un objetivo de loudness coherente con el género y el comportamiento del master.

## Situación práctica de partida

El alumno ya llevó el programa a un nivel posible, pero ahora se enfrenta a la típica duda: "¿lo dejo a –14 porque eso dice Spotify?", "¿aprieto más porque el género lo aguanta?", "¿qué pasa si entrego más fuerte o más suave?".

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: medidor LUFS activo. El master reproduce con un nivel integrado visible.]*

Los targets de plataformas no son recetas de mastering. Son referencias de normalización. Si no se entiende esa diferencia, se empieza a masterizar para el medidor en vez de masterizar para la música.

### 2. Desarrollo paso a paso

**Qué hace la normalización**

La plataforma, en términos generales, no masteriza el audio. Ajusta la reproducción para acercar material más fuerte o más suave a un rango de escucha consistente. Eso significa que perseguir ciegamente un número puede ser absurdo si para llegar ahí se destruye el programa.

**Dos escenarios**

*[EN PANTALLA: comparación conceptual — master muy por encima del target / master bastante por debajo del target.]*

Escenario uno: master muy por encima del target. La plataforma probablemente lo bajará en reproducción. Escenario dos: master bastante por debajo. La plataforma podría subirlo, pero ese material conservará más rango dinámico si fue bien construido.

La pregunta correcta no es "qué número tengo que poner", sino "qué densidad soporta esta música sin romperse y cómo se comportará en su destino."

**Criterio por género y arreglo**

*[EN PANTALLA: dos masters distintos — uno de producción electrónica densa, otro de jazz acústico. Los dos tienen LUFSi distintos y está justificado.]*

Una producción urbana o electrónica densa suele tolerar más nivel aparente. Un jazz acústico, una balada aireada o una obra con más rango dinámico piden otra relación entre impacto y respiración. No se igualan decisiones solo porque comparten plataforma.

**Consultar la documentación oficial actualizada**

*[EN PANTALLA: el docente muestra cómo acceder a la documentación de plataformas — Spotify for Artists, Apple Music for Artists, YouTube Studio.]*

Los valores de target de cada plataforma pueden cambiar. No se memorizan como verdad eterna. Se consultan en la documentación actual de cada plataforma: Spotify publica sus guidelines en Spotify for Artists; Apple en Apple Music for Artists; YouTube en YouTube Studio. Los valores que estaban vigentes cuando se grabó esta lección pueden haber cambiado; siempre verificar en la fuente.

### 3. Teoría aplicada en el punto correcto

La normalización de plataformas es ajuste de volumen de reproducción, no procesamiento de audio. El LUFS objetivo se adapta al género y al comportamiento del programa, no se impone como número universal. Los valores de plataformas se verifican en fuentes oficiales porque pueden cambiar.

### 4. Criterio de decisión

El loudness final se cruza con tres variables: cuánto aguanta el material, qué sensación estética necesita y cómo será normalizado en destino. Si el programa pierde transitorio, profundidad o naturalidad antes de llegar al número objetivo, se para antes. En otra canción del mismo proyecto, el objetivo podría cambiar aunque la plataforma sea la misma.

### 5. Errores frecuentes y falsas reglas

"Si es para streaming, siempre –14 LUFS." No. Ese valor es una referencia, no una ley.

"Si la plataforma lo baja, da igual destrozar la mezcla para subirla." Tampoco.

"Todos los géneros deben competir al mismo nivel." No. La traducción correcta depende de cómo está construido el programa.

### 6. Cierre

Con el loudness decidido, ya solo falta la última parte técnica de la entrega: bits, resampleo, dither y verificación del archivo exportado. La siguiente lección cierra ese tramo.

---

# E7-L10 — Dithering, resampleo y archivo final

## Rol de esta lección dentro del proceso completo

Esta lección cierra la entrega digital. El master sale al formato correcto sin errores de conversión ni ruido innecesario acumulado.

## Objetivo del video

Cerrar la entrega digital del master aplicando dither solo cuando corresponde, resampleo con criterio y verificación del archivo exportado.

## Resultado que debería conseguir el alumno al terminar

El alumno puede exportar un master final sabiendo cuándo aplicar dither, qué revisar después del bounce y por qué el archivo exportado también se verifica.

## Situación práctica de partida

El master ya está decidido en sonido y nivel. Ahora toca convertirlo al formato real de entrega. El riesgo no es artístico: es arruinar el archivo final por una conversión mal hecha o por aplicar procesos que no hacían falta.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: ventana de exportación del DAW. Las configuraciones de sample rate, bit depth y formato de archivo visibles.]*

Muchos masters no se rompen en la cadena. Se rompen al salir. Por eso esta parte no es administrativa: es parte técnica del proceso.

### 2. Desarrollo paso a paso

**Definir el destino real**

*[EN PANTALLA: el docente configura la ventana de exportación. Sample rate del destino. Bit depth del destino. Formato: WAV para entrega de alta calidad / MP3 o AAC para formato de distribución con pérdida.]*

Lo primero es definir el destino real: sample rate y profundidad de bits del archivo final. Esa decisión no se toma por costumbre sino por requerimiento de entrega. Si el destino pide 44.1 kHz / 16 bits (CD), las configuraciones son esas. Si pide 44.1 kHz / 24 bits (mastering para streaming con mayor resolución), esas otras.

**Dithering: solo si hay reducción de bits, solo una vez**

*[EN PANTALLA: el docente activa el dithering en el plugin o en la configuración de exportación. Solo visible si la exportación implica reducción de profundidad de bits.]*

Si hay reducción de profundidad de bits, el dithering se aplica. Una sola vez. En la conversión final. No en exports intermedios, no en pruebas, no "por si acaso".

Si se exporta a 24 bits desde un proyecto a 32 bits float, técnicamente no hay reducción relevante — el dither puede no ser necesario. Si se exporta a 16 bits, el dither es necesario.

*[EN PANTALLA: opción de noise shaping en el plugin de dither. El docente muestra las opciones.]*

Si hay opción de noise shaping, se usa entendiendo que no reduce ruido total: redistribuye su percepción hacia frecuencias donde el oído es menos sensible. El ruido total sigue siendo el mismo.

**Resampleo: con SRC de calidad**

*[EN PANTALLA: si hay cambio de sample rate, el docente activa el SRC de mayor calidad disponible — preferiblemente offline o de alta calidad en el DAW.]*

Si hay cambio de sample rate, se aplica el SRC de mayor calidad disponible. No se deja al azar ni se asume que cualquier conversión sonará igual. El resampleo de baja calidad puede introducir aliasing audible.

**Master Fader en 0 dB al exportar**

*[EN PANTALLA: el Master Fader visible en 0 dB antes de exportar.]*

Se exporta con el Master Fader en 0 dB. No se mueve el Master Fader para compensar nivel en el último momento. Si hay que ajustar nivel de salida, se hace dentro de la cadena del master, no aquí.

**Verificación del archivo exportado**

*[EN PANTALLA: el docente importa el archivo exportado en una nueva pista del DAW o en un reproductor. Revisa LUFS integrados, True Peak, forma de onda.]*

Se vuelve a abrir el archivo exportado. Se verifican LUFS integrados, True Peak, forma de onda y comportamiento general.

*[EN PANTALLA: si el destino incluye versión codificada con pérdida (MP3, AAC), el docente también abre esa versión y verifica el True Peak.]*

Si el destino incluye una versión codificada con pérdida, se verifica también esa versión. El True Peak puede subir después de la codificación.

### 3. Teoría aplicada en el punto correcto

El dithering se aplica solo cuando hay reducción de profundidad de bits, y una sola vez al final. El noise shaping redistribuye el ruido, no lo elimina. El resampleo debe hacerse con SRC de calidad. La verificación del archivo exportado, incluido el control de True Peak del archivo codificado, es parte del proceso, no un extra opcional.

Estas operaciones son la aplicación final de la doctrina de bits y sample rate introducida en el Eje 0-B: aquí se aplica en el contexto de la entrega del master definitivo.

### 4. Criterio de decisión

Se aplica dither solo si hay reducción real de bits. Se aplica SRC solo si el destino exige otro sample rate. Y se verifica siempre el archivo exportado porque el resultado final no es el proyecto abierto en el DAW: es el archivo que va a circular. En flujos con múltiples deliverables con distintas resoluciones, cada uno se decide según destino.

### 5. Errores frecuentes y falsas reglas

"Siempre hay que poner dither al exportar." No.

"El noise shaping reduce el ruido." No; lo redistribuye.

"Si el proyecto suena bien, el archivo exportado también." No necesariamente.

"El resampleo es un trámite sin costo." Depende de la calidad del SRC.

### 6. Cierre

Ya está el archivo final. Pero si el trabajo no es un single sino un conjunto, todavía falta una etapa de criterio mayor: cómo hacer que varias canciones convivan como una sola obra. La siguiente y última lección entra en mastering de álbum.

---

# E7-L11 — Mastering de álbum

## Rol de esta lección dentro del proceso completo

Esta lección cierra el eje ampliando la escala de decisión. El alumno deja de pensar en una canción aislada y pasa a pensar en continuidad, contraste intencional y coherencia de conjunto.

## Objetivo del video

Igualar coherencia entre canciones sin borrar identidad, usando referencia cruzada y nivelación intencional en contexto de álbum.

## Resultado que debería conseguir el alumno al terminar

El alumno puede masterizar varias canciones como un conjunto, mantener identidad común sin homogeneizarlo todo y nivelar la experiencia de escucha con criterio musical.

## Situación práctica de partida

Ya existen varios masters o premasteres del mismo proyecto. Cada uno puede sonar bien por separado, pero al reproducirlos seguidos aparecen saltos de densidad, color o energía que hacen que el conjunto deje de sentirse como un mismo disco.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: varios masters del álbum cargados en el DAW. El docente los reproduce en secuencia — se perciben saltos de densidad y tono entre canciones.]*

Masterizar un álbum no es repetir once veces el mastering de un single. Es trabajar sobre un conjunto donde cada decisión individual se reevalúa contra el resto.

### 2. Desarrollo paso a paso

**Escuchar en contexto: transiciones reales**

*[EN PANTALLA: el docente reproduce el final de una canción y el inicio de la siguiente sin pausa. El salto de energía o tono es evidente.]*

Lo primero es dejar de escuchar canciones sueltas. Se arma una reproducción en contexto y se comparan transiciones reales. Lo que se busca no es si todas suenan igual, sino si todas conviven.

**Referencia cruzada activa**

*[EN PANTALLA: el docente trabaja en la canción actual y vuelve periódicamente a escuchar las demás canciones del álbum para comparar.]*

Se trabaja con referencia cruzada activa. Se ajusta una canción y se vuelve enseguida a las demás. No se masteriza cada una encerrado en su propia burbuja. En álbum, el contexto cambia la evaluación de cada decisión.

**Variables a comparar entre canciones**

*[EN PANTALLA: medidores LUFS y Peak activos para cada canción mientras el docente las compara.]*

Se revisan entre canciones: color, densidad, low end, apertura y nivel percibido. Si una canción tiene más grave por su arreglo, puede estar bien. El problema aparece cuando esa diferencia no se siente intencional sino accidental.

**Nivelación intencional, no uniformidad de LUFS**

*[EN PANTALLA: el docente muestra que las canciones del álbum tienen LUFSi distintos — y eso es correcto porque cada una tiene su densidad propia.]*

La nivelación en álbum no iguala todos los LUFS integrados. Una balada puede y a veces debe sentirse más abierta o menos densa que un tema más agresivo. Lo importante es que el recorrido del disco tenga lógica y que los cambios parezcan decisiones de producción, no errores de consistencia.

**Coherencia vs. uniformidad**

La meta final no es volumen uniforme ni timbre idéntico. Es que todo "suene al mismo disco" sin borrar la personalidad de cada canción.

### 3. Teoría aplicada en el punto correcto

El mastering de álbum difiere del de single a nivel de criterio, no de mecánica. La referencia cruzada constante, la coherencia de conjunto y la nivelación intencional son los tres principios que guían el trabajo.

Una canción perfecta sola puede quedar desproporcionada dentro del álbum. La unidad de trabajo en mastering de álbum no es la canción sino el disco.

### 4. Criterio de decisión

Se decide en relación con el conjunto. Si una canción necesita más densidad por carácter, puede dársele siempre que no rompa continuidad. Si una transición requiere contraste, ese contraste debe sentirse buscado. En otro álbum, la coherencia podría construirse desde mayor homogeneidad o desde contrastes más marcados. Lo que cambia es la estética del proyecto, no la necesidad de comparar en contexto.

### 5. Errores frecuentes y falsas reglas

"Para sonar coherente, todo debe tener el mismo volumen." No.

"Si cada canción sola suena perfecta, el álbum ya está." Tampoco.

"Coherencia de álbum significa borrar diferencias." No. Significa que las diferencias tengan sentido dentro de una misma identidad.

### 6. Cierre

*[EN PANTALLA: los masters del álbum reproducidos en secuencia. El conjunto suena con identidad propia. Los saltos anteriores ya no están.]*

Con esto se cierra el Eje 7. Ya no se está preparando una mezcla: se está entregando un programa listo para vivir fuera de la sesión, ya sea como single o como obra completa. El ciclo LDOV que comenzó en el Eje 0 con la calibración del sistema de escucha termina aquí, con el archivo que llegará al oyente.

---

*KENTH Academy — Eje 7 · Guiones v2 · Revisión final*
*Revisión basada en: auditoría forense, contenido canónico Eje 7, paquete limpio Eje 7, criterios pedagógicos KENTH.*
*Terminología adoptada: Técnica / Comercial / Artística (según formulación predominante en las clases; el Apunte Mastering 2022 usa Técnica / Estética / Comercial — misma lógica, diferente nomenclatura).*
*Método delta: técnica estándar del campo; no requiere atribución al autor fuente.*
