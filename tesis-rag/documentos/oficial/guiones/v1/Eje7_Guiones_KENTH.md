# E7-L01 — Qué sí es mastering y qué ya llegaste tarde a arreglar

## Rol de esta lección dentro del proceso completo
Esta lección abre el eje y fija la frontera de trabajo. Antes de tocar una cadena de mastering, el alumno tiene que entender qué problemas pertenecen al master y cuáles debieron resolverse en mezcla. Sin esa frontera, todo lo que viene después se usa mal.

## Objetivo del video
Fijar el alcance real del mastering y presentar sus tres etapas en el orden correcto: técnica, comercial y artística.

## Resultado que debería conseguir el alumno al terminar
El alumno puede mirar una mezcla terminada, distinguir si el problema que detecta es global o específico, y decidir si corresponde seguir en mastering o volver a mezcla.

## Situación práctica de partida
Llega una mezcla estéreo al proyecto de mastering. El alumno escucha que en ciertos compases hay demasiado grave, pero no sabe si el problema es del tema completo o de un instrumento concreto. Antes de ecualizar por impulso, tiene que decidir si el mastering puede intervenir sin romper algo que sí estaba bien.

## Estructura del guion

### 1. Apertura
Hoy no vamos a empezar con plugins. Vamos a empezar con una decisión más básica: si este problema pertenece al mastering o si ya llegaste tarde y tendrías que volver a la mezcla. Esa diferencia define todo el eje.

### 2. Desarrollo paso a paso
Abro la mezcla estéreo y lo primero que hago no es procesar. Escucho el tema completo y me hago una pregunta muy concreta: ¿lo que me molesta afecta al programa entero o a un elemento puntual?

Si escucho que toda la canción tiene un exceso de graves, eso sí entra en mastering. Si lo que está mal es la guitarra en ciertos compases, la reverb de una voz o el ataque de un bombo concreto, eso ya es mezcla. En mastering no tengo acceso al elemento aislado. Todo lo que haga aquí le cae encima a toda la canción.

Entonces hago una primera clasificación. Problema global: densidad general, balance tonal general, imagen general, nivel general, picos generales. Problema específico: un instrumento, una frase, una reverb, una automatización puntual, una mala decisión de paneo de un elemento. Si es específico, lo marco y lo devuelvo. Si es global, sigo.

A partir de ahí presento las tres etapas del mastering como flujo real de trabajo. Primera etapa: técnica. Aquí resuelvo problemas formales de la señal antes de empujar nivel o color. Segunda etapa: comercial. Aquí llevo el programa al nivel de distribución que necesita sin destruirlo. Tercera etapa: artística. Esta no siempre hace falta. Solo entra si el material pide un pequeño ajuste de carácter y si ese ajuste no está corrigiendo una mezcla mal hecha.

Lo importante no es memorizar los nombres. Lo importante es el orden. Si la señal tiene un problema técnico y yo primero la saturo o la limito, lo amplifico. Si la señal ya llegó bien y yo insisto en “hacer mastering” con procesamiento porque sí, empiezo a degradar algo que ya funcionaba.

Entonces cierro la primera inspección con una regla de trabajo: el mastering traduce un sistema ya terminado. No reconstruye una mezcla.

### 3. Teoría aplicada en el punto correcto
El mastering es la preparación del programa fonográfico para su distribución. Su rasgo operativo es que cualquier procesamiento afecta simultáneamente a todos los elementos de la mezcla. Por eso la distinción clave no es técnica sino de alcance: problema global versus problema específico. El flujo también tiene orden necesario: técnica antes que comercial, y artística solo si hace falta. Esa lógica está en la base canónica del Eje 7 y define el arranque del proceso. fileciteturn2file0 fileciteturn3file4

### 4. Criterio de decisión
Aquí sigo este camino porque todavía no estoy decidiendo herramientas, sino terreno de intervención. Si el problema es global, mastering tiene sentido. Si es específico, no. En otra canción podría parecer que un exceso de grave es global, pero al revisar quizá descubres que solo aparece cuando entra un synth puntual. Ahí la decisión cambia: no necesitas un master distinto, necesitas corregir la mezcla.

### 5. Errores frecuentes y falsas reglas
El error más común es creer que mastering es “el lugar donde se termina de arreglar todo”. No. También es falso pensar que toda mezcla necesita una etapa artística visible. Otra falsa regla es asumir que, si el track llegó a mastering, entonces cualquier problema ya debe resolverse ahí. No necesariamente. A veces la decisión correcta es no seguir y pedir revisión de mezcla.

### 6. Cierre
Ahora que ya sabemos qué sí pertenece al mastering, recién tiene sentido preparar la señal. La siguiente lección arranca ahí: ajustar entrada, revisar DC offset y distinguirlo de la asimetría de forma de onda.

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
Antes de hablar de compresión, EQ o limitadores, hay que dejar la señal lista para entrar a la cadena. Si la entrada ya viene mal calibrada, todo lo demás empieza torcido.

### 2. Desarrollo paso a paso
Cargo la mezcla y no inserto todavía procesadores de carácter. Primero miro estadísticas y medidores. Quiero saber tres cosas: picos, LUFS integrados y comportamiento visual de la forma de onda.

Si la mezcla llega demasiado arriba, hago trimming con clip gain o trim del archivo, no con el fader del master. Necesito que los procesadores trabajen dentro de un rango razonable, especialmente si voy a usar modelados analógicos. El objetivo práctico de entrada es dejar la mezcla en un rango de trabajo aproximadamente entre –20 y –23 LUFSi si esa cadena lo necesita.

Después reviso DC offset. Si toda la señal está desplazada fuera del cero, eso no es un detalle estético. Reduce headroom útil, favorece clipping asimétrico y hace reaccionar distinto a los procesadores dinámicos. Si el valor es despreciable, no toco nada. Si es claramente significativo, lo corrijo con un HPF muy bajo o con una herramienta específica de offset.

Ahora separo eso de la asimetría. Aquí la señal sí está centrada, pero los picos de un semiciclo son más altos que los del otro. Eso no se corrige como DC offset. Lo que está mal aquí no es una componente continua: es la forma en que se están sumando las fases de los componentes frecuenciales. Entonces, si realmente necesito corregirla porque me está comiendo headroom de un lado, uso un AllPass, no un HPF.

Hago una comprobación simple al final: vuelvo a mirar la forma de onda, reviso estadísticas y escucho. Si resolví offset, el eje de reposo vuelve al centro. Si corregí asimetría, los picos quedan más equilibrados. Si no cambió nada útil, no insisto.

### 3. Teoría aplicada en el punto correcto
El trimming es condición previa para que la cadena opere en su rango óptimo; en Eje 7 se recomienda un punto de entrada aproximado de –20 a –23 LUFSi cuando se trabaja con procesadores calibrados a ese entorno. El DC offset es desplazamiento de la forma de onda fuera del cero y se corrige con HPF muy bajo o herramienta específica. La asimetría, en cambio, es una distribución desigual de picos con la señal centrada y su corrección se apoya en AllPass. Son fenómenos distintos y con correcciones distintas. fileciteturn2file0 fileciteturn2file1

### 4. Criterio de decisión
Aquí elegimos este camino porque la prioridad no es “mejorar sonido” todavía, sino darle condiciones estables a la cadena. Si el offset es mínimo, no conviene corregir por deporte. Si la asimetría no limita de verdad el headroom ni genera problema operativo, tampoco hace falta intervenir. En otra canción, la forma de onda puede verse rara pero no justificar corrección. La evidencia manda, no la apariencia.

### 5. Errores frecuentes y falsas reglas
Falso: “toda mezcla se baja 6 dB y listo”. No. Se mide y se decide cuánto hace falta. Falso: “si la forma de onda está rara, siempre es DC offset”. No. Falso: “un HPF en 5 Hz no hace daño nunca”. Tampoco. Si no hay problema, no metas procesos porque sí. Y otro error clásico: usar el master fader para resolver el nivel de entrada a la cadena. Eso no sustituye el trimming.

### 6. Cierre
Con la señal ya calibrada y saneada, recién tiene sentido leerla en serio como programa completo. En la siguiente lección hacemos justamente eso: diagnóstico global de nivel, fase e imagen y espectro antes de intervenir.

---

# E7-L03 — Diagnóstico global del programa

## Rol de esta lección dentro del proceso completo
Esta lección convierte la preparación en lectura. Aquí el alumno aprende a mirar el master como sistema completo antes de procesarlo.

## Objetivo del video
Leer nivel, fase e imagen y espectro del programa completo antes de aplicar cualquier corrección o procesamiento de mastering.

## Resultado que debería conseguir el alumno al terminar
El alumno puede armar una inspección técnica mínima del master y salir de ella con una lista de problemas reales, no supuestos.

## Situación práctica de partida
La señal ya está calibrada para entrar a la cadena. Ahora el riesgo no es técnico de entrada, sino de intervención sin diagnóstico: tocar EQ, compresión o limitación sin haber identificado qué problema real existe en el programa.

## Estructura del guion

### 1. Apertura
El error más caro en mastering no suele ser no saber usar un limitador. Suele ser empezar a mover cosas antes de haber leído bien la señal completa.

### 2. Desarrollo paso a paso
Empiezo con medidores de nivel. Quiero saber dónde están los picos, qué LUFS integrados trae el programa y cuál es la relación general entre densidad y techo. No estoy decidiendo loudness final todavía; solo estoy entendiendo desde dónde parto.

Después miro fase e imagen. Abro goniómetro y correlatómetro porque en mastering ya no estoy corrigiendo un micrófono o un track, sino el comportamiento estéreo del programa entero. Si veo una imagen sesgada, un exceso lateral extraño o una correlación problemática en graves, lo anoto. No lo corrijo todavía sin entender la causa.

Luego paso al espectro. Busco tres familias de problemas: subsónicas inútiles, resonancias globales y desequilibrios generales de balance tonal. Aquí el analizador no reemplaza a la escucha, pero sí me ayuda a no inventarme problemas. Si hay una subida anómala debajo del fundamento, lo veo. Si hay una zona que empuja demasiado todo el tema, lo veo. Si la sibilancia residual está apareciendo en el programa completo, también lo veo.

Lo importante es que esta lectura ya no es por instrumento. Si detecto algo y sospecho que viene de un solo elemento, lo marco como límite del mastering. Si detecto que afecta al sistema, sigo adelante.

Al final de la inspección dejo una lista concreta: qué requiere corrección técnica, qué podría requerir ajuste de imagen, qué quizá no conviene tocar y qué definitivamente no pertenece a esta etapa.

### 3. Teoría aplicada en el punto correcto
El diagnóstico en mastering reutiliza la lógica del Eje 1: nivel, fase y espectro, pero ahora a escala global. La teoría mínima obligatoria del eje indica analizar la señal completa antes de insertar cualquier procesador y revisar LUFS integrados, pico, correlación, goniómetro y espectro para identificar subsónicas, balance general y posibles residuos de sibilancia o imagen. fileciteturn2file1 fileciteturn3file9

### 4. Criterio de decisión
Este camino se elige porque en mastering una corrección equivocada castiga a todo el programa. Si el diagnóstico muestra que no hay problema real en una zona, no toco esa zona. En otra canción, un desbalance lateral podría ser parte del arreglo y no un defecto. Lo que manda es si rompe traducción, estabilidad o coherencia, no si se aleja de una imagen “bonita”.

### 5. Errores frecuentes y falsas reglas
Falso: “el mastering empieza con un EQ”. No. Empieza con lectura. Falso: “si el analizador muestra algo feo, hay que corregirlo”. No necesariamente. Falso: “si la correlación baja, hay que cerrar estéreo”. Tampoco. Primero hay que entender si el comportamiento es musical, tolerable o problemático para traducción.

### 6. Cierre
Con el diagnóstico hecho, ya podemos separar lectura de intervención. La siguiente lección entra en la primera intervención real del eje: corrección espectral general, pero solo cuando el diagnóstico la justifica.

---

# E7-L04 — Corrección espectral general en mastering

## Rol de esta lección dentro del proceso completo
Esta lección convierte el diagnóstico en primeras correcciones globales. Aquí se resuelven problemas del programa completo sin invadir terreno que corresponde a mezcla.

## Objetivo del video
Aplicar HPF subsónico, controlar resonancias globales y corregir balance L/R solo cuando el análisis demuestra que hace falta.

## Resultado que debería conseguir el alumno al terminar
El alumno puede intervenir el espectro global del master con criterio, sabiendo cuándo corregir, cuándo no tocar y cuándo devolver a mezcla.

## Situación práctica de partida
El análisis mostró posibles subsónicas, una resonancia que atraviesa la canción y cierto desbalance lateral en graves. El alumno tiene que decidir qué sí es corrección general y qué ya sería intentar mezclar desde el master.

## Estructura del guion

### 1. Apertura
Ahora sí entramos a corregir, pero con una condición: lo que hagamos aquí tiene que resolver un problema del programa completo, no disimular una mezcla mal resuelta por elemento.

### 2. Desarrollo paso a paso
Empiezo por la zona subsónica. No cargo un HPF por reflejo. Primero escucho, miro el analizador y pregunto: ¿hay energía real que no aporta contenido musical y solo está cargando el sistema? Si la curva cae de forma natural hacia abajo, no toco. Si hay una acumulación o una cola que se sostiene por debajo del fundamento, ahí sí planteo un HPF suave y bien elegido.

Después reviso resonancias. Si una frecuencia empuja la mezcla completa de forma consistente, uso EQ paramétrico con Q razonable. Si esa molestia aparece solo a ratos, un EQ dinámico puede ser mejor porque no quiero dejar un hueco permanente donde el problema no existe. Y si descubro que la molestia vive sobre todo en Mid o sobre todo en Side, uso M/S para no castigar todo el campo estéreo por igual.

Luego miro balance L/R, sobre todo abajo. Si la mezcla se apoya más en un lado en la zona grave, puedo recentrar esa base con herramientas tipo mono maker o con una gestión de imagen por bandas. Pero aquí hago una pausa clave: si el problema viene claramente de un paneo mal decidido en mezcla, no lo maquillo en mastering salvo que no haya otra opción operativa.

En cada corrección comparo antes y después a igualdad de nivel y vuelvo a escuchar el programa entero. Si la corrección resuelve el síntoma pero empobrece el carácter general, retrocedo.

### 3. Teoría aplicada en el punto correcto
La base canónica del eje define tres correcciones generales principales: HPF subsónico solo cuando el análisis muestra energía problemática por debajo del fundamento; resonancias globales corregibles con EQ paramétrico o dinámico según su estabilidad; y reequilibrio L/R, especialmente en graves, mediante herramientas de recentrado o mono maker cuando el problema compromete traducción. También aclara que, si el origen es un elemento puntual, lo correcto sigue siendo mezcla. fileciteturn2file1 fileciteturn3file7

### 4. Criterio de decisión
Aquí elegimos HPF, EQ estático, EQ dinámico o control de imagen según evidencia. Si el problema es continuo, el corte o el EQ estático pueden servir. Si aparece por momentos, conviene dinámica. Si está localizado en el centro o en los laterales, M/S tiene sentido. En otra canción, la misma frecuencia puede ser parte del carácter y no un defecto. No se corrige por número, se corrige por función.

### 5. Errores frecuentes y falsas reglas
Falso: “todo master lleva HPF subsónico”. No. Falso: “si molesta una frecuencia, notch y listo”. No en mastering, donde una corrección estrecha puede dejar el programa sin naturalidad. Falso: “si hay desbalance L/R, se arregla con imagen estéreo”. Depende. Puede ser un problema de mezcla, no de master.

### 6. Cierre
Una vez corregida la base espectral y lateral del programa, recién tiene sentido trabajar dinámica de mastering con más control. La siguiente lección entra ahí: compresión en serie, paralela y ascendente.

---

# E7-L05 — Compresión en mastering: en serie, paralela y ascendente

## Rol de esta lección dentro del proceso completo
Esta lección introduce la gestión dinámica específica del mastering, donde la tarea no es comprimir un instrumento sino modelar la respuesta del programa completo.

## Objetivo del video
Comprimir en mastering por tareas diferenciadas y no por costumbre, usando serie, paralelo o compresión ascendente según lo que el programa necesite.

## Resultado que debería conseguir el alumno al terminar
El alumno puede decidir si conviene una compresión escalonada, una capa paralela sutil o una intervención ascendente, y entender qué costo tiene cada opción.

## Situación práctica de partida
El master ya no tiene problemas técnicos evidentes, pero todavía necesita mayor consistencia dinámica o una sensación de densidad más estable antes de entrar a limitación. El alumno tiene que decidir cómo llegar ahí sin aplastar la mezcla.

## Estructura del guion

### 1. Apertura
En mastering no se comprime para “que suene más pro”. Se comprime para una tarea concreta. Si no sabes cuál es la tarea, cualquier compresor te va a pedir más y más reducción hasta que arruines la mezcla.

### 2. Desarrollo paso a paso
Empiezo por escuchar si realmente hace falta compresión previa al limitador. Si la mezcla ya viene muy estable y solo necesita techo comercial, quizá no necesito sumar compresión. Si sí la necesita, la primera decisión no es ratio ni ataque: es si quiero una compresión escalonada, una capa paralela o un enfoque ascendente.

Si el programa necesita consistencia general y, además, mejor control de picos antes de limitación, prefiero compresión en serie. Pongo primero un compresor más musical, que una el programa y lo estabilice sin perseguir cada transitorio. Después, si todavía quedan picos que me complican la etapa comercial, añado un compresor más preciso para terminar de ordenarlos. La lógica es simple: varios pasos pequeños suelen costar menos que una sola compresión grande.

Si lo que busco es levantar detalle o densidad percibida sin aplanar tanto la señal principal, pruebo compresión paralela. Mantengo la señal original y mezclo una versión mucho más comprimida debajo. Escucho con atención porque, si lo hago agresivo y con envolventes rápidas, el costo puede ser aliasing, aspereza o una sensación de suciedad en el movimiento.

Si lo que quiero es levantar pasajes suaves sin castigar los fuertes, la compresión ascendente puede ser mejor camino. No siempre está disponible en todos los equipos, pero conceptualmente sirve para otra tarea: reducir diferencia desde abajo, no desde arriba.

Cada vez que pruebo una de estas rutas, comparo a igualdad de nivel. Si la supuesta mejora desaparece cuando compenso loudness, no era una mejora: era volumen.

### 3. Teoría aplicada en el punto correcto
El paquete limpio del eje plantea que en mastering funcionan mejor varios pasos pequeños que saltos grandes; propone compresión en serie con una primera etapa más musical y otra más precisa para picos, y además ubica la compresión paralela y la ascendente como alternativas para elevar densidad o pasajes bajos con costos distintos. La paralela puede introducir aliasing o coloración con envolventes rápidas; la ascendente tiende a ser más transparente en ese uso. fileciteturn3file9 fileciteturn3file10

### 4. Criterio de decisión
Elijo serie cuando necesito repartir tareas. Elijo paralelo cuando quiero densidad sin cargar todo el peso sobre la ruta principal. Elijo ascendente cuando el problema es la relación entre pasajes bajos y altos y quiero una intervención menos aplastante. En otra canción, ninguna de las tres podría ser necesaria. El criterio no es “qué técnica me gusta”, sino “qué problema dinámico existe antes del limitador”.

### 5. Errores frecuentes y falsas reglas
Falso: “todo master profesional lleva dos compresores”. No. Falso: “la paralela siempre da densidad gratis”. Tampoco; tiene costo. Falso: “si el limitador va a hacer loudness, la compresión previa no importa”. Error. Una mala dinámica antes del limitador hace que el limitador trabaje peor.

### 6. Cierre
Con la dinámica ya encaminada, queda una pregunta delicada: si además quiero un poco de carácter, ¿cómo lo sumo sin usar saturación como maquillaje? La siguiente lección va a eso.

---

# E7-L06 — Saturación: carácter sin pasarte

## Rol de esta lección dentro del proceso completo
Esta lección añade la capa artística más sutil del eje. Aquí el alumno aprende a usar saturación como ajuste fino, no como recurso para esconder fallas previas.

## Objetivo del video
Usar saturación en mastering como una herramienta de densidad y riqueza armónica controlada, evitando que se vuelva distorsión audible o autoengaño por nivel.

## Resultado que debería conseguir el alumno al terminar
El alumno puede probar saturación en mastering, compararla honestamente y decidir si aporta algo real o si solo está subiendo volumen y colorando de más.

## Situación práctica de partida
La señal ya está técnica y dinámicamente más estable, pero todavía se percibe algo seca o demasiado plana. El alumno considera una saturación sutil para sumar riqueza armónica, pero no quiere convertir el master en una distorsión disfrazada.

## Estructura del guion

### 1. Apertura
La saturación en mastering no está para tapar una mezcla floja. Está, como mucho, para sumar un poco de densidad y armónicos si eso realmente mejora la traducción y el carácter del programa.

### 2. Desarrollo paso a paso
Primero activo la saturación con una dosis deliberadamente baja. No busco escuchar distorsión como efecto. Busco que el programa se sienta un poco más unido, más presente o con una riqueza armónica sutil, especialmente en pasajes que sin ella quedan demasiado austeros.

Después compenso nivel. Esto no es negociable. Si la saturación levanta aunque sea un poco el volumen, la comparación queda sesgada. Entonces igualo loudness y hago bypass varias veces. Si la mejora desaparece al compensar, era puro volumen. Si lo que queda es una sensación real de densidad, presencia o calor y no una pérdida de limpieza, sigo.

También escucho el costo. Si los agudos se vuelven ásperos, si el centro se espesa demasiado o si la mezcla pierde apertura, ya me pasé. En mastering, lo normal es que el umbral de utilidad sea pequeño. La saturación no debería anunciarse sola.

Y hago una distinción importante: saturar no reemplaza compresión, EQ ni limitación. Si estoy usando saturación porque no sé cómo controlar picos, porque faltó compresión o porque la mezcla vino vacía, estoy cargando en ella una tarea que no le corresponde.

### 3. Teoría aplicada en el punto correcto
La doctrina reutilizable del eje describe la saturación en mastering como una forma de añadir riqueza armónica y densidad percibida. También marca un criterio operativo claro: si se escucha como distorsión, hay demasiada, y la comparación debe hacerse siempre a igualdad de nivel. Ese es el marco correcto para usarla como ajuste fino, no como maquillaje. fileciteturn3file9 fileciteturn3file10

### 4. Criterio de decisión
Aquí uso saturación solo si, una vez resueltos problemas técnicos y dinámica, todavía falta una pequeña sensación de cohesión armónica o presencia. Si el material ya llegó con carácter suficiente, no la necesito. En otra canción, especialmente una producción acústica o muy transparente, la mejor decisión puede ser no tocarla.

### 5. Errores frecuentes y falsas reglas
Falso: “todo master mejora con un poco de saturación”. No. Falso: “si no se oye claramente, no está haciendo nada”. Tampoco. En mastering, a veces lo correcto es que el cambio sea pequeño pero útil. Falso: “saturación es compresión con otro nombre”. No. Puede afectar densidad percibida, pero no sustituye tareas dinámicas específicas.

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
Mid/Side en mastering no sirve para mezclar desde atrás. Sirve para corregir o ajustar el programa final cuando el centro y los laterales necesitan un trato distinto.

### 2. Desarrollo paso a paso
Lo primero que hago es recordar qué significa intervenir aquí. Mid contiene todo lo que está en el centro del programa; Side, lo lateral. Si muevo Mid, no estoy moviendo una voz aislada: estoy moviendo todo lo que comparte el centro.

Empiezo por escuchar si el problema es de imagen o de balance. Si los graves se sienten inestables, pruebo recentrarlos o mantenerlos en mono por debajo de una zona determinada. Esto suele dar más peso y estabilidad. No lo hago porque sí: lo hago si el programa lo necesita.

Después reviso si hay algo en medios o agudos que convenga abrir levemente. Aquí soy conservador. En mastering, abrir un poco arriba puede dar aire, pero si lo hago sin control puedo debilitar centro, arruinar compatibilidad o volver artificial la imagen.

Si detecté una resonancia o una dureza localizada más en Mid o más en Side, uso esa separación a mi favor. Corrijo donde vive el problema, no en todo el programa. Y en cada paso vuelvo al mono y a la escucha normal para asegurar que no estoy comprando apertura a cambio de perder solidez.

### 3. Teoría aplicada en el punto correcto
El eje distingue con claridad el M/S de mastering del de mezcla: la mecánica es la misma, pero aquí el procesamiento opera sobre el programa completo. El paquete limpio recomienda mantener graves más centrados para peso y estabilidad, y usar M/S cuando un problema está alojado en Mid o Side sin necesidad de castigar toda la imagen. También marca el cruce explícito con Eje 5: aquí no se enseña la codificación, sino el criterio de uso global. fileciteturn3file9 fileciteturn3file6

### 4. Criterio de decisión
Elijo M/S cuando el centro y los laterales no están pidiendo lo mismo. Si el programa está estable y natural, no hace falta tocar imagen. Si el problema está claramente en un elemento puntual, otra vez, eso ya era mezcla. En otra canción, una imagen muy abierta puede ser parte del lenguaje estético y no requerir recentrado adicional.

### 5. Errores frecuentes y falsas reglas
Falso: “en mastering siempre se abren los sides”. No. Falso: “los graves siempre van en mono”. Como regla universal, no. Depende del material y del problema. Falso: “si una resonancia está al centro, se arregla con EQ normal”. Podría, pero M/S te permite resolver sin afectar todo el campo si la evidencia lo justifica.

### 6. Cierre
Con imagen y centro bajo control, ya queda la etapa que más fácilmente se sobreusa: la limitación. La siguiente lección entra al limitador, al método delta y al control de True Peak.

---

# E7-L08 — Limitador, método delta y True Peak

## Rol de esta lección dentro del proceso completo
Esta lección aborda la etapa comercial del mastering. Aquí el programa se lleva a nivel de distribución controlando daño y techo real de salida.

## Objetivo del video
Llevar el programa al nivel comercial necesario con limitación controlada, usando método delta para escuchar el daño y verificando True Peak antes y después de codificación.

## Resultado que debería conseguir el alumno al terminar
El alumno puede configurar un limitador de mastering con criterio, entender la relación entre threshold y out ceiling, evaluar artefactos con método delta y verificar True Peak del archivo final.

## Situación práctica de partida
La mezcla ya está corregida, equilibrada y con la dinámica previa resuelta. Falta elevar nivel de salida para distribución sin destruir transitorios, graves ni naturalidad del programa.

## Estructura del guion

### 1. Apertura
Aquí es donde más gente arruina el master. No por usar un limitador, sino por usarlo sin escuchar qué está sacrificando a cambio del nivel.

### 2. Desarrollo paso a paso
Inserto el limitador al final de la cadena. Primero fijo el out ceiling: necesito definir hasta dónde puede salir la señal. Después empiezo a bajar threshold para aumentar nivel. En la práctica, threshold aquí funciona como control de cuánto material le estoy empujando al limitador; el ceiling define el techo.

Mientras subo nivel, no me quedo mirando solo LUFS. Escucho especialmente graves, transitorios y sensación de respiración del tema. Si el grave se vuelve borroso o si el ataque pierde forma, el limitador ya está pagando el loudness con daño audible.

Entonces entra el método delta. Hago la comparación entre lo que sale del limitador y lo que el limitador está eliminando. Esa resta me dice qué está destruyendo. Si en el delta escucho solo picos aislados o material esperable, voy bien. Si en el delta empiezo a oír cuerpo, groove, graves útiles o información musical sostenida, estoy limitando demasiado.

Luego verifico True Peak. No me basta con ver sample peak del proyecto. Quiero saber cuál es el techo real, sobre todo si después va a haber codificación a AAC o MP3. Por eso verifico también el archivo codificado cuando aplica, porque el True Peak puede subir después de esa conversión.

### 3. Teoría aplicada en el punto correcto
El eje define el limitador de mastering como una herramienta donde threshold controla cuánto entra y out ceiling fija el techo de salida. También establece el método delta como técnica estándar del campo para evaluar el daño introducido por la limitación y recalca la importancia del True Peak, incluido el del archivo codificado, no solo el WAV del proyecto. fileciteturn3file9 fileciteturn3file5

### 4. Criterio de decisión
Aquí elijo cuánto limitar según el destino, el género y lo que el programa tolera sin romperse. Si una producción acústica pierde vida rápido, no persigo el mismo nivel que una producción electrónica densa. Si el delta empieza a devolver demasiada música y no solo exceso, ya crucé la línea. En otra canción, el limitador puede tolerar más trabajo o bastante menos.

### 5. Errores frecuentes y falsas reglas
Falso: “más LUFS es mejor master”. No. Falso: “si no clippea el ceiling, está bien”. Tampoco; puedes destruir la señal sin pasar el techo. Falso: “el método delta es opcional”. No si quieres entender qué estás pagando por el loudness. Falso: “con ver el WAV basta para True Peak”. No cuando habrá codificación posterior.

### 6. Cierre
Ya tenemos el master casi listo, pero todavía falta decidir el objetivo de loudness con criterio real y no con números memorizados. La siguiente lección entra a normalización de plataformas y criterio por género.

---

# E7-L09 — Targets de plataformas y criterio por género

## Rol de esta lección dentro del proceso completo
Esta lección contextualiza la etapa comercial. Aquí el alumno entiende que el loudness no se decide en abstracto, sino en función de plataforma, normalización y lenguaje del material.

## Objetivo del video
Decidir loudness de entrega entendiendo que las plataformas normalizan volumen y que el objetivo final depende del tipo de música y de cómo soporta esa densidad.

## Resultado que debería conseguir el alumno al terminar
El alumno puede interpretar targets de plataformas sin tomarlos como mandamientos rígidos y elegir un objetivo de loudness coherente con el género y el comportamiento del master.

## Situación práctica de partida
El alumno ya llevó el programa a un nivel posible, pero ahora se enfrenta a la típica duda: “¿lo dejo a –14 porque eso dice Spotify?”, “¿aprieto más porque el género lo aguanta?”, “¿qué pasa si entrego más fuerte o más suave?”.

## Estructura del guion

### 1. Apertura
Los targets de plataformas no son recetas de mastering. Son referencias de normalización. Si no entiendes esa diferencia, empiezas a masterizar para el medidor en vez de masterizar para la música.

### 2. Desarrollo paso a paso
Primero aclaro qué hace la normalización. La plataforma, en términos generales, no “masteriza” tu audio. Ajusta reproducción para acercar material más fuerte o más suave a un rango de escucha consistente. Eso significa que perseguir ciegamente un número puede ser absurdo si para llegar ahí destruyes el programa.

Después comparo dos escenarios. Uno: master muy por encima del target. La plataforma probablemente lo bajará. Dos: master bastante por debajo. La plataforma podría subirlo, pero ese material seguirá conservando más rango dinámico si fue bien construido. Entonces la pregunta correcta no es “qué número tengo que poner”, sino “qué densidad soporta esta música sin romperse y cómo se comportará en su destino?”.

Ahí entra criterio por género y por arreglo. Una producción urbana o electrónica densa suele tolerar más nivel aparente. Un jazz acústico, una balada aireada o una obra con más rango dinámico piden otra relación entre impacto y respiración. Por eso no igualo decisiones solo porque comparten plataforma.

También dejo una nota operativa importante: los valores oficiales pueden cambiar. Se consultan en la documentación actual de cada plataforma; no se memorizan como verdad eterna.

### 3. Teoría aplicada en el punto correcto
La base canónica del eje incluye normalización de plataformas como ajuste de volumen y no como procesamiento de audio, e insiste en adaptar el LUFS objetivo al género. El paquete limpio además deja claro que los valores de plataformas deben verificarse en fuentes oficiales porque pueden cambiar, así que no se presentan como definitivos. fileciteturn3file3 fileciteturn1file8

### 4. Criterio de decisión
Elijo loudness final cruzando tres variables: cuánto aguanta el material, qué sensación estética necesita y cómo será normalizado en destino. Si el programa pierde transitorio, profundidad o naturalidad antes de llegar al número que “alguien dijo”, paro antes. En otra canción del mismo proyecto, el objetivo podría cambiar aunque la plataforma sea la misma.

### 5. Errores frecuentes y falsas reglas
Falso: “si es para streaming, siempre –14 LUFS”. No. Falso: “si la plataforma lo baja, da igual destrozar la mezcla para subirla”. Tampoco. Falso: “todos los géneros deben competir al mismo nivel”. No. La traducción correcta depende de cómo está construido el programa.

### 6. Cierre
Con el loudness decidido, ya solo falta la última parte técnica de la entrega: bits, resampleo, dither y verificación del archivo exportado. La siguiente lección cierra ese tramo.

---

# E7-L10 — Dithering, resampleo y archivo final

## Rol de esta lección dentro del proceso completo
Esta lección cierra la entrega digital. Aquí se asegura que el master salga al formato correcto sin errores de conversión ni ruido innecesario acumulado.

## Objetivo del video
Cerrar la entrega digital del master aplicando dither solo cuando corresponde, resampleo con criterio y verificación del archivo exportado.

## Resultado que debería conseguir el alumno al terminar
El alumno puede exportar un master final sabiendo cuándo aplicar dither, qué revisar después del bounce y por qué el archivo exportado también se verifica.

## Situación práctica de partida
El master ya está decidido en sonido y nivel. Ahora toca convertirlo al formato real de entrega. El riesgo aquí no es artístico: es arruinar el archivo final por una conversión mal hecha o por aplicar procesos que no hacían falta.

## Estructura del guion

### 1. Apertura
Muchos masters no se rompen en la cadena. Se rompen al salir. Por eso esta parte no es administrativa: es parte técnica del proceso.

### 2. Desarrollo paso a paso
Lo primero es definir el destino real: sample rate y profundidad de bits del archivo final. Esa decisión no se toma por costumbre, se toma por requerimiento de entrega.

Si voy a reducir profundidad de bits, ahí sí entra dithering. Una sola vez. En la conversión final. No en exports intermedios, no en pruebas, no “por si acaso”. Si además tengo opción de noise shaping, lo uso entendiendo que no reduce ruido total: redistribuye su percepción.

Si hay cambio de sample rate, aplico el SRC de mayor calidad disponible. No lo dejo al azar ni asumo que cualquier conversión sonará igual.

Exporto con el master fader en 0 dB y después hago algo que muchos saltan: vuelvo a abrir el archivo exportado. Reviso LUFS integrados, True Peak, forma de onda y comportamiento general. Si el destino incluye una versión codificada con pérdida, verifico también esa versión, no solo el WAV.

### 3. Teoría aplicada en el punto correcto
La teoría mínima obligatoria del eje indica que el dither se aplica solo cuando hay reducción de profundidad de bits y una sola vez, al final. También incluye noise shaping como redistribución del ruido y no como eliminación, resampleo con SRC de calidad y verificación posterior del archivo exportado, incluido el control de True Peak del archivo codificado cuando corresponde. fileciteturn3file3 fileciteturn3file8

### 4. Criterio de decisión
Aquí aplico dither solo si realmente estoy bajando bits. Si no hay reducción, no lo necesito. Aplico SRC solo si el destino exige otro sample rate. Y verifico siempre el archivo exportado porque el resultado final no es el proyecto abierto en el DAW: es el archivo que va a circular. En otro flujo, podría haber múltiples deliverables con distintas resoluciones; cada uno se decide según destino.

### 5. Errores frecuentes y falsas reglas
Falso: “siempre hay que poner dither al exportar”. No. Falso: “el noise shaping reduce el ruido”. No; lo mueve. Falso: “si el proyecto suena bien, el archivo exportado también”. No necesariamente. Y falso también: “el resampleo es un trámite sin costo”. Depende de la calidad del SRC.

### 6. Cierre
Ya está el archivo final. Pero si el trabajo no es un single sino un conjunto, todavía falta una etapa de criterio mayor: cómo hacer que varias canciones convivan como una sola obra. La siguiente y última lección entra en mastering de álbum.

---

# E7-L11 — Mastering de álbum

## Rol de esta lección dentro del proceso completo
Esta lección cierra el eje ampliando la escala de decisión. Aquí el alumno deja de pensar en una canción aislada y pasa a pensar en continuidad, contraste intencional y coherencia de conjunto.

## Objetivo del video
Igualar coherencia entre canciones sin borrar identidad, usando referencia cruzada y nivelación intencional en contexto de álbum.

## Resultado que debería conseguir el alumno al terminar
El alumno puede masterizar varias canciones como un conjunto, mantener identidad común sin homogeneizarlo todo y nivelar la experiencia de escucha con criterio musical.

## Situación práctica de partida
Ya existen varios masters o premasteres del mismo proyecto. Cada uno puede sonar bien por separado, pero al reproducirlos seguidos aparecen saltos de densidad, color o energía que hacen que el conjunto deje de sentirse como un mismo disco.

## Estructura del guion

### 1. Apertura
Masterizar un álbum no es repetir once veces el mastering de un single. Es trabajar sobre un conjunto donde cada decisión individual se reevalúa contra el resto.

### 2. Desarrollo paso a paso
Empiezo dejando de escuchar canciones sueltas. Armo una reproducción en contexto y comparo transiciones reales. Lo primero que busco no es si todas suenan igual, sino si todas conviven.

Reviso color, densidad, low end, apertura y nivel percibido entre canciones. Si una canción pide más grave por su arreglo, eso puede estar bien. El problema aparece cuando esa diferencia no se siente intencional sino accidental.

Entonces trabajo con referencia cruzada activa. Ajusto una canción y vuelvo enseguida a las demás. No masterizo cada una encerrado en su propia burbuja. En álbum, el contexto cambia la evaluación de cada decisión.

Después abordo la nivelación. Aquí no igualo todos los LUFS integrados como si fueran piezas intercambiables. Una balada puede y a veces debe sentirse más abierta o menos densa que un tema más agresivo. Lo importante es que el recorrido del disco tenga lógica y que los cambios parezcan decisiones de producción, no errores de consistencia.

La meta final no es volumen uniforme ni timbre idéntico. Es que todo “suene al mismo disco” sin borrar la personalidad de cada canción.

### 3. Teoría aplicada en el punto correcto
La base canónica del eje distingue mastering de álbum frente a single a nivel de criterio y no de mecánica. El paquete limpio insiste en referencia cruzada constante, coherencia de conjunto y nivelación intencional, no en igualar todas las canciones al mismo LUFS. También aclara que una canción perfecta sola puede quedar desproporcionada dentro del álbum. fileciteturn3file11 fileciteturn3file8

### 4. Criterio de decisión
Aquí decido en relación con el conjunto. Si una canción necesita más densidad por carácter, puedo dársela siempre que no rompa continuidad. Si una transición requiere contraste, ese contraste debe sentirse buscado. En otro álbum, la coherencia podría construirse desde una mayor homogeneidad o desde contrastes más marcados. Lo que cambia es la estética del proyecto, no la necesidad de comparar en contexto.

### 5. Errores frecuentes y falsas reglas
Falso: “para sonar coherente, todo debe tener el mismo volumen”. No. Falso: “si cada canción sola suena perfecta, el álbum ya está”. Tampoco. Falso: “coherencia de álbum significa borrar diferencias”. No. Significa que las diferencias tengan sentido dentro de una misma identidad.

### 6. Cierre
Con esto se cierra el Eje 7. Ya no estamos preparando una mezcla: estamos entregando un programa listo para vivir fuera de la sesión, ya sea como single o como obra completa.
