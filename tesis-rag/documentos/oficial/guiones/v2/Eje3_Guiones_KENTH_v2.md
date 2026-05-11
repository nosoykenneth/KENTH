# Guiones corregidos — Eje 3 · KENTH Academy · v2
*Revisión: auditoría final + corrección integral*

---

# E3-L01 — Bell y shelving: los parámetros que de verdad mandan

## Rol de esta lección dentro del proceso completo

Esta es la entrada real al trabajo tonal del curso. El Eje 2 dejó la señal limpia, alineada y calibrada. Aquí empieza el momento en que ya no solo se quitan problemas: se decide cómo debe sonar el instrumento. Esta lección no busca "ecualizar bonito". Busca que el alumno entienda qué está moviendo cuando toca frecuencia, ganancia, Q y shelving.

## Objetivo del video

Dominar frecuencia, ganancia, Q y el comportamiento real del shelving para dejar de mover parámetros por intuición ciega.

## Resultado que debería conseguir el alumno al terminar

Que pueda abrir un EQ, identificar qué parámetro define el problema o el objetivo tonal, y prever qué efecto tendrá una campana ancha, una campana estrecha o un shelving antes de escucharlo.

## Situación práctica de partida

Una voz principal con presencia insuficiente. Se sube una campana en 3 kHz y el resultado cambia drásticamente según el Q. Se prueba un high shelf y da brillo pero también dureza. El problema no es que el EQ "suene mal": es que todavía no se entiende qué controla cada parámetro.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: DAW con voz principal en reproducción. EQ paramétrico insertado pero sin bandas activas todavía.]*

Antes de hablar de gusto, plugins o color, hay una cosa más básica: si no se entiende qué hace una campana y qué hace un shelf, cada movimiento de EQ es una apuesta. Mezclar así es perder tiempo y acumular decisiones que no se saben justificar.

### 2. Desarrollo paso a paso

**Campana: frecuencia y Q**

*[EN PANTALLA: voz en reproducción dentro de la mezcla completa. EQ paramétrico con una campana activa. El docente mueve frecuencia mientras escucha.]*

Se pone la voz en contexto con la mezcla, no en solo desde el inicio. La voz está un poco atrás, pero no apagada en todo el espectro. No hace falta tocar cualquier cosa: hay que intervenir una zona concreta.

Se abre una campana en el EQ. Primero se mueve la frecuencia, no para decidir todavía, sino para ubicar la zona donde la voz se acerca o donde se vuelve agresiva.

*[EN PANTALLA: frecuencia fijada. El docente mueve el Q de estrecho a ancho mientras el audio reproduce.]*

Con la frecuencia ubicada, se ajusta el Q.

Con Q alto — campana estrecha — el cambio es muy puntual. La voz empieza a sonar como si sobresaliera una parte del timbre en lugar de mejorar la presencia general.

*[EN PANTALLA: Q reducido — campana más ancha.]*

Con Q bajo — campana ancha — la intervención se reparte en una zona mayor y el resultado se siente más natural, pero también afecta más material alrededor.

Primera decisión real: si el objetivo es resolver algo localizado, se necesita más selectividad. Si el objetivo es empujar el carácter general de una zona, conviene una acción más amplia.

**Shelving de agudos: apertura con consecuencias**

*[EN PANTALLA: se cambia la campana por un high shelving. El docente ajusta y escucha.]*

El shelf no trabaja sobre un punto concreto: levanta todo el rango superior a partir de una zona de transición. Eso da apertura, pero también mueve más material del que a veces conviene. En esta voz el shelf da aire, pero también acerca la sibilancia y endurece consonantes.

*[EN PANTALLA: comparación directa bypass campana / bypass shelf, con nivel compensado.]*

La campana permite trabajar presencia sin arrastrar tanto el extremo alto. El shelf es más rápido pero menos selectivo. No hay un parámetro "mejor": hay una herramienta más precisa para el problema concreto.

**Shelving de graves: peso vs. masa**

*[EN PANTALLA: low shelf activo en un bajo o en la voz. Comparación con campana en la misma zona.]*

Una campana y un low shelf tampoco hacen lo mismo en graves. La campana puede reforzar una zona concreta. El shelf cambia la sensación de masa de una porción grande del espectro. Usado sin criterio, no solo agrega peso: también puede ensuciar los medios-bajos aunque no era esa la intención.

### 3. Teoría aplicada en el punto correcto

La frecuencia central de una campana es el punto de máxima acción. El Q define qué tan ancha o estrecha es la zona afectada. Q alto: intervención selectiva. Q bajo: intervención más amplia y suave. Q y pendiente de filtro son parámetros distintos.

Con shelving hay una trampa frecuente: la frecuencia marcada en pantalla no significa siempre "desde aquí empieza todo". Dependiendo del diseño, esa frecuencia puede representar la mitad de la ganancia o el punto de referencia del estante. Dos shelves con el mismo número no siempre reaccionan igual.

*[EN PANTALLA: dos plugins de EQ con el mismo shelf en el mismo Hz — uno digital, uno modelado. La curva visible es distinta.]*

En EQs modelados de circuitos analógicos clásicos, boost y cut no siempre son simétricos, y el Q puede estrecharse a medida que aumenta la ganancia. Eso explica por qué el mismo valor numérico no se comporta igual en todos los EQs.

### 4. Criterio de decisión

Se elige campana para presencia cuando el problema es de foco tonal localizado. Si la voz estuviera apagada en todo el rango superior, podría convenir un shelf. Si el instrumento necesitara un empuje en una zona expresiva específica, campana. Si necesitara cambiar la sensación completa de brillo o peso, shelf.

La decisión depende de qué zona se quiere afectar, qué tan localizada es la intervención y cuánto contenido útil hay alrededor de esa zona.

### 5. Errores frecuentes y falsas reglas

La presencia de una voz no siempre se resuelve en 3 kHz. La zona varía según el instrumento, la grabación y la mezcla.

Un high shelf no "abre" sin consecuencias. Siempre mueve más de lo que parece en el punto de ajuste.

Q estrecho no significa trabajo más profesional. Significa más selectividad. Según el problema, puede ser excesiva.

Un número igual en dos EQs distintos no garantiza el mismo resultado. La implementación importa.

### 6. Cierre

Ya se entiende qué controlan campana y shelving. Lo siguiente es igual de importante: incluso sabiendo eso, todavía falta decidir qué arquitectura de EQ conviene para cada tarea. Eso es la siguiente lección.

---

# E3-L02 — Gráfico, semi y paramétrico: cuál usar y por qué

## Rol de esta lección dentro del proceso completo

Después de entender los parámetros, toca entender las arquitecturas. El alumno ya sabe qué quiere mover; ahora necesita saber con qué herramienta conviene hacerlo.

## Objetivo del video

Elegir entre EQ gráfico, semiparamétrico y paramétrico según la tarea, en vez de usar siempre el plugin más completo por costumbre.

## Resultado que debería conseguir el alumno al terminar

Que pueda mirar un problema tonal y decidir si necesita una arquitectura rápida y musical, una de barrido práctico o una de control total.

## Situación práctica de partida

Hay una guitarra eléctrica, un piano y una voz. Cada uno pide una intervención distinta. El alumno tiene varios EQs pero usa siempre el mismo paramétrico de ocho bandas porque "sirve para todo". Sirve, sí. Pero no siempre conviene.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: tres plugins de EQ distintos cargados en la pantalla pero sin insertar en ningún canal todavía: uno gráfico, uno semiparamétrico, uno paramétrico de varias bandas.]*

Una mala costumbre frecuente es pensar que el mejor EQ es el que tiene más opciones. En mezcla eso no siempre ayuda. A veces da precisión inútil. A veces vuelve lento el proceso.

### 2. Desarrollo paso a paso

**Semiparamétrico para localizar**

*[EN PANTALLA: semiparamétrico insertado en la guitarra eléctrica. Una banda activa con ganancia subida. El docente mueve la frecuencia mientras la guitarra reproduce.]*

En esta guitarra hay algo molesto pero no está claro todavía en qué zona. El semiparamétrico es la herramienta adecuada aquí.

Se sube ganancia, se barre la frecuencia y se escucha dónde el problema se vuelve evidente. En cuanto se localiza, se deja de barrer y esa búsqueda se convierte en decisión: se baja la ganancia en esa frecuencia para cortar.

El valor del semiparamétrico no es que tenga menos control. Es que obliga a pensar por zona antes de obsesionarse con precisión milimétrica.

**Gráfico para carácter general**

*[EN PANTALLA: EQ gráfico insertado en el piano. Bandas en bloques amplios del espectro. El docente mueve bandas mientras el piano reproduce en la mezcla.]*

En el piano no se busca una resonancia puntual. Se está acomodando el carácter general: un ajuste ancho, rápido, musical. El gráfico obliga a pensar en bloques más grandes del espectro. En este caso eso ordena en vez de complicar. No se necesita cirugía. Se necesita dirección.

**Paramétrico para intervención precisa**

*[EN PANTALLA: EQ paramétrico insertado en la voz. Tres bandas activas: una de presencia, una de notch puntual, una de aire.]*

La voz sí requiere control fino: una zona de presencia con Q definido, una resonancia puntual, y tal vez algo de apertura arriba. Ahí el paramétrico tiene sentido porque ya se sabe qué se quiere tocar y con qué selectividad.

**El criterio de elección**

El criterio no es cuál EQ es más famoso ni más moderno. Las preguntas son: ¿todavía se está encontrando el problema? ¿ya se sabe exactamente dónde está? ¿se quiere una corrección precisa o una construcción tonal amplia?

Más control también aumenta la posibilidad de hacer daño innecesario. Si se entra con ocho bandas y Q estrecho en todo, se termina perforando el instrumento en vez de definirlo.

### 3. Teoría aplicada en el punto correcto

El gráfico trabaja con frecuencias fijas y prioriza rapidez y forma general. El semiparamétrico deja mover frecuencia y ganancia pero no Q; por eso funciona muy bien como herramienta de barrido y decisiones rápidas. El paramétrico añade control de Q y por eso sirve tanto para corrección quirúrgica como para construcción tonal más fina.

Que uno sea más flexible no lo vuelve automáticamente superior en todos los casos.

### 4. Criterio de decisión

Semiparamétrico cuando todavía se está descubriendo el problema. Gráfico cuando se quieren cambios amplios y rápidos sin microcirugía. Paramétrico cuando el problema u objetivo ya está claro y se necesita precisión real.

La herramienta correcta depende del tipo de tarea, no del prestigio del plugin.

### 5. Errores frecuentes y falsas reglas

No siempre hay que usar el paramétrico porque "tiene más control". El control innecesario produce intervenciones innecesarias.

El gráfico no es un EQ menor. En ciertos contextos es más musical que un paramétrico de alta precisión.

Barrer frecuencias no es ecualizar: es localizar antes de decidir. Son dos operaciones distintas.

Si un semiparamétrico no permite tocar Q, eso no significa que sea peor. Significa que fue pensado para otra forma de trabajar.

### 6. Cierre

Ya se sabe qué controlar y con qué arquitectura hacerlo. Ahora viene la decisión que organiza el eje entero: cuándo se está corrigiendo un problema y cuándo se está construyendo carácter.

---

# E3-L03 — EQ correctivo vs EQ estético

## Rol de esta lección dentro del proceso completo

Esta lección ordena la intención. Sin esta diferencia, el alumno mezcla dos trabajos distintos con la misma lógica y termina tomando malas decisiones aunque conozca bien los controles.

## Objetivo del video

Separar claramente quitar problemas de construir carácter, y enseñar el procedimiento de barrido para localizar antes de cortar.

## Resultado que debería conseguir el alumno al terminar

Que pueda mirar una intervención de EQ y clasificarla por intención antes de mover una banda, y que tenga un procedimiento repetible para encontrar el punto exacto de una resonancia o problema.

## Situación práctica de partida

Un bajo con una resonancia en torno a 120 Hz y, además, un objetivo de que suene más grande y redondo en la mezcla. Si se tratan esas dos cosas con la misma lógica, el proceso se pierde.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: bajo en reproducción. Se escucha una nota que sobresale. EQ insertado pero sin bandas activas.]*

Hay una razón por la que mucha gente se enreda con el EQ: intenta corregir y diseñar tono al mismo tiempo, sin separar las dos tareas. Eso vuelve confuso todo el proceso.

### 2. Desarrollo paso a paso

**Tarea uno: EQ correctivo**

*[EN PANTALLA: bajo en solo. Se activa una campana con Q alto y ganancia elevada. El docente barre la frecuencia lentamente.]*

Se escucha una nota que sobresale en una zona concreta. Eso no es "carácter": es un comportamiento problemático del instrumento o de la grabación.

El procedimiento para localizarlo: se activa una banda con Q alto y se sube la ganancia. No para dejarla así — para exagerar el problema y encontrarlo con el oído. Se barre la frecuencia despacio hasta que el problema se hace evidente. Cuando la zona problemática está clara, se invierte el movimiento: ganancia hacia abajo, en esa frecuencia. Se reduce solo lo mínimo necesario.

*[EN PANTALLA: la resonancia localizada y cortada. Comparación antes/después con bypass.]*

No se está buscando que el bajo suene más bonito. Se está buscando que deje de imponerse donde no debe. Ésa es la intención correctiva.

**Tarea dos: EQ estético**

*[EN PANTALLA: bajo en mezcla completa, sin solo. El docente escucha y luego abre una banda amplia en graves.]*

Con la resonancia controlada, se escucha el bajo otra vez dentro de la mezcla. Ahora sí aparece otra pregunta: ¿el bajo ya tiene el peso y la forma que necesita para el arreglo? Si la respuesta es no, ya no se está corrigiendo un problema puntual: se está definiendo carácter. Eso es EQ estético.

La intervención es distinta en su mentalidad. No se busca una banda estrecha para sacar algo feo. Se busca una acción más musical, más amplia, que construya el rol del instrumento en la mezcla.

*[EN PANTALLA: campana ancha en la zona del cuerpo del bajo, en mezcla completa. Comparación antes/después.]*

Y aquí aparece un punto clave: el EQ correctivo muchas veces puede evaluarse parcialmente en solo, si el problema pertenece al canal. Pero el EQ estético no tiene sentido real fuera del contexto. Porque la pregunta no es "qué le falta al bajo en solo", sino "qué necesita esta mezcla para que el bajo cumpla su función".

### 3. Teoría aplicada en el punto correcto

El EQ correctivo tiende a ser más selectivo, normalmente sustractivo, orientado a eliminar interferencias, resonancias o enmascaramientos. El EQ estético modifica el timbre de manera deliberada: peso, presencia, brillo, apertura, densidad.

El procedimiento de barrido — boost con Q alto para localizar, luego cut en esa frecuencia — funciona porque el oído detecta mejor el exceso que la falta. Exagerar el problema para encontrarlo con el oído es más preciso que mover frecuencias a ciegas.

No son categorías decorativas. Cambian la forma de escuchar, de verificar y de decidir cuándo la intervención terminó.

### 4. Criterio de decisión

Si la pregunta es "qué sobra o qué molesta", se está en terreno correctivo. Si la pregunta es "qué quiero que este instrumento proyecte en la mezcla", se está en terreno estético.

Eso cambia la herramienta, el Q, la cantidad de ganancia y el lugar donde se verifica el resultado.

### 5. Errores frecuentes y falsas reglas

Toda sustracción no es automáticamente correctiva. Un corte ancho para dar espacio a otro instrumento puede ser una decisión estética.

Todo boost no es automáticamente estético. Un boost de barrido para localizar un problema es una herramienta de diagnóstico.

Una mezcla buena no sale de corregir cada canal hasta dejarlo limpio y luego sumar. El resultado en mezcla puede pedir que cada instrumento suene menos perfecto en solo.

Si un instrumento suena increíble en solo eso no significa que esté cumpliendo mejor su rol en la canción.

### 6. Cierre

Ya se separó la intención. El siguiente riesgo es otro: incluso cuando se decide bien, se puede aprobar un cambio simplemente porque quedó más fuerte. Ese autoengaño arruina decisiones que deberían ser buenas.

---

# E3-L04 — Ecualizar en contexto: bypass, nivel y autoengaño

## Rol de esta lección dentro del proceso completo

Esta lección protege la toma de decisiones. El alumno ya entiende parámetros, arquitecturas e intención. Ahora tiene que aprender a no engañarse comparando mal.

## Objetivo del video

Evitar aprobar cambios solo porque quedaron más fuertes.

## Resultado que debería conseguir el alumno al terminar

Que compare EQ activo y bypass con criterio de nivel y contexto, y que deje de confundir aumento de volumen con mejora tonal.

## Situación práctica de partida

Una guitarra rítmica. Se aplica un boost de presencia, se hace bypass y parece que con EQ suena "mejor". Cuando se compensa el nivel, esa supuesta mejora casi desaparece.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: guitarra rítmica en reproducción. EQ paramétrico insertado con un boost activo. El docente señala la diferencia de nivel en el medidor.]*

Una de las trampas más antiguas de mezcla sigue funcionando perfecto: se hace algo sonar más fuerte y el oído dice que suena mejor. Si no se controla eso, el EQ deja de ser criterio y se vuelve sesgo.

### 2. Desarrollo paso a paso

**El error sin control**

*[EN PANTALLA: guitarra con un boost activo. El docente activa y desactiva el EQ (bypass). Sin compensar nivel.]*

Se aplica un pequeño boost en la zona de presencia. Al hacer bypass parece mejor: más clara, más viva, más adelante.

Ese es el problema: lo que se está escuchando no es la mejora tonal. Es el aumento de nivel.

**La comparación correcta: bypass compensado**

*[EN PANTALLA: el docente baja la ganancia de salida del EQ para que el nivel con EQ activo y con bypass sean equivalentes. Luego hace la comparación.]*

Se compensa el nivel. Se baja la salida del EQ hasta que activo y bypass suenen al mismo volumen percibido. Ahora se vuelve a comparar.

La diferencia ya no es tan obvia. En algunos puntos incluso se prefiere la guitarra sin EQ.

Eso indica algo importante: antes no se estaba evaluando tono. Se estaba evaluando volumen.

**La comparación en mezcla completa**

*[EN PANTALLA: la mezcla completa activa con la guitarra dentro. El docente activa y desactiva el EQ de la guitarra con nivel compensado.]*

Hay un segundo autoengaño: aprobar una decisión en solo y enamorarse del canal aislado. Con la mezcla corriendo, lo que parecía una gran mejora puede volverse exceso de presencia, invasión del espacio de otro elemento, o simple cansancio en esa zona.

El EQ correctivo puede verificarse parcialmente en solo. El EQ estético siempre requiere verificación en contexto. Y en cualquier caso, la comparación con bypass sin nivel compensado no dice nada sobre el tono.

### 3. Teoría aplicada en el punto correcto

El oído prefiere casi siempre lo más fuerte cuando la diferencia es pequeña. Cualquier boost o cualquier proceso que agregue energía percibida puede venderse como mejora aunque no lo sea.

La comparación válida es EQ activo versus bypass con nivel percibido equivalente. En EQ estético, la verificación correcta ocurre en contexto, porque el problema real es relacional: cómo convive ese instrumento con los demás.

### 4. Criterio de decisión

Si el cambio desaparece al igualar el volumen percibido, no había una mejora tonal clara. Si el cambio solo funciona en solo pero no en mezcla, tampoco sirve.

La decisión correcta no es "¿suena más espectacular?" sino "¿cumple mejor su trabajo en la canción sin depender de una ilusión de nivel?"

### 5. Errores frecuentes y falsas reglas

Si con bypass baja la emoción no significa que el EQ esté bien. Puede significar que el EQ está aportando solo volumen.

Trabajar en solo no es error. Aprobar en solo sin verificar en mezcla sí lo es, especialmente para EQ estético.

Si el bypass no está compensado en nivel, no se está comparando EQ: se está comparando EQ más volumen.

Un plugin analógico insertado sin tocar bandas no mejora la mezcla por existir. Puede agregar carácter real, puede agregar solo densidad percibida por nivel, o puede hacer ambas cosas. Siempre se verifica a nivel compensado.

### 6. Cierre

Ya se pueden tomar decisiones de EQ sin engañarse tan fácil. Ahora sí tiene sentido entrar al territorio del modelado analógico y entender qué cambia de verdad cuando se usan esas herramientas.

---

# E3-L05 — Modelado analógico: calibración y THD útil

## Rol de esta lección dentro del proceso completo

Aquí el eje pasa de la geometría del EQ al comportamiento del circuito modelado. Es el puente entre entender curvas y entender color.

## Objetivo del video

Entender qué cambia al usar EQs modelados y cómo alimentarlos correctamente para que su carácter sea útil y controlado.

## Resultado que debería conseguir el alumno al terminar

Que pueda insertar un EQ modelado, calibrar su entrada y distinguir entre curva tonal y carácter armónico del circuito.

## Situación práctica de partida

Se inserta un modelado de EQ analógico sin tocar ninguna banda y la señal ya cambia. Luego se cambia el nivel de entrada y cambia otra vez. Se necesita entender por qué.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: canal de voz en el DAW. Plugin de EQ modelado analógico insertado. Ninguna banda activa.]*

Un EQ modelado no solo mueve frecuencias. También modela cómo se comporta un circuito cuando le entra señal. Si no se entiende eso, se puede usarlo bien por accidente o arruinarlo sin darse cuenta.

### 2. Desarrollo paso a paso

**El nivel de entrada cambia el carácter**

*[EN PANTALLA: Trim del canal antes del EQ. El docente ajusta el nivel de entrada al plugin. Se escucha el resultado con distintos niveles de entrada. El EQ sigue sin bandas activas.]*

Lo primero que se verifica antes de ajustar bandas es el nivel de entrada. En un EQ modelado, la entrada no es un detalle administrativo: es parte del sonido.

Con menos nivel, el plugin se comporta de forma más discreta. Con más nivel, el carácter se vuelve más evidente — armónicos, densidad, respuesta no lineal — y en algún punto empieza a empujar demasiado.

El primer paso práctico es verificar el punto de calibración del plugin y ajustar con Trim para que la señal llegue donde el modelado fue pensado para trabajar.

**Insertar sin bandas: comprobar el carácter base**

*[EN PANTALLA: EQ modelado activo sin bandas. Bypass on/off con nivel compensado. Se escucha la diferencia.]*

Se activa el plugin sin tocar ninguna banda y se compara contra bypass con nivel compensado. Si hay diferencia audible, el plugin está modelando comportamiento de circuito: transformadores, tolerancias, distorsión armónica. Eso puede ser útil o puede ser neutral según el material.

La diferencia no debería venderse como mejora por el solo hecho de existir. Se verifica a nivel igual.

**EQ con bandas: curva más carácter**

*[EN PANTALLA: el docente ahora activa una banda del EQ modelado y ajusta. Se escucha la combinación de curva + carácter del circuito.]*

Una vez calibrada la entrada, sí se mueven bandas. La diferencia respecto a un EQ digital transparente es que aquí no solo cambia la curva: también cambia el carácter con el que esa curva se imprime. Las dos cosas actúan juntas.

### 3. Teoría aplicada en el punto correcto

El modelado analógico no emula únicamente la ecualización del equipo: emula también la distorsión armónica total (THD) y el comportamiento no lineal del circuito original.

Según el circuito y el nivel de entrada, aparecen armónicos que el oído puede leer como calidez, densidad, agresividad o suavidad. Por eso el nivel de entrada importa: muy bajo, el carácter puede no aparecer; muy alto, el modelado deja de ser útil y empieza a exagerar.

Los valores impresos en los paneles analógicos — y en muchos de sus modelados — no deben interpretarse con la rigidez matemática de un EQ digital transparente. Son referencias, no certezas.

### 4. Criterio de decisión

El modelado analógico tiene sentido cuando no solo se quiere mover una zona del espectro, sino también imprimir comportamiento de circuito. Pero solo vale si el material y el contexto justifican ese color.

Para limpieza extrema y precisión quirúrgica, un EQ digital transparente es más adecuado. Para carácter, densidad o una respuesta menos clínica, el modelado puede ganar valor.

### 5. Errores frecuentes y falsas reglas

Un EQ modelado no es mejor por defecto. Depende de qué necesita el material.

Más nivel de entrada no significa más profesional. Significa más carácter del circuito. Si ese carácter no es el que se busca, es un problema.

Si no se calibra la entrada, no se puede evaluar el plugin con honestidad. Se está combinando calibración y criterio en una sola decisión confusa.

Insertar un modelado en todos los canales no da automáticamente una mezcla con carácter. Puede dar una mezcla cargada y desordenada.

### 6. Cierre

Ya se entiende qué cambia cuando se usa modelado. Ahora toca algo más útil todavía: no pensar en estas familias como reliquias famosas, sino como decisiones tonales concretas orientadas a objetivos específicos.

---

# E3-L06 — API, Neve, SSL y Pultec como decisiones tonales, no como fetiches

## Rol de esta lección dentro del proceso completo

Esta lección aterriza el modelado a decisiones reales. No es historia del hardware. Es criterio de elección según objetivos tonales concretos.

## Objetivo del video

Asociar familias de modelado a objetivos tonales concretos, no a instrumentos específicos ni a nombres de marca.

## Resultado que debería conseguir el alumno al terminar

Que pueda escoger entre familias de modelado según lo que necesita que ocurra en la mezcla, partiendo del objetivo tonal y no del prestigio o la costumbre.

## Situación práctica de partida

Varios instrumentos con necesidades tonales distintas. El alumno ve muchos nombres míticos y no sabe cuál usar ni por qué.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: cuatro plugins de EQ modelado abiertos — API, Neve, SSL, Pultec. Sin insertar en ningún canal todavía.]*

Elegir un modelado por el nombre o porque "siempre se usa en este instrumento" ya es perder la oportunidad de decidir. Estas familias sirven cuando se sabe qué objetivo tonal se está buscando. La marca es la consecuencia de esa decisión, no el punto de partida.

### 2. Desarrollo paso a paso

Las cuatro familias principales tienen fabricantes identificables. API Technologies desarrolló los circuitos de la familia API. AMS Neve es el origen de la familia Neve. Solid State Logic es la marca detrás del SSL. Pulse Techniques creó el EQP-1A que es la base del diseño Pultec.

*[EN PANTALLA: en cada demo, el plugin correspondiente se inserta en el canal. El docente ajusta y escucha. No hay una secuencia fija instrumento-marca: se parte del objetivo tonal.]*

**Objetivo: frontalidad, decisión, empuje en medios**

Si lo que se busca es que un elemento salga hacia adelante, gane presencia en la zona media-alta y tenga más definición de ataque, la familia API suele acercarse a ese resultado. Sus circuitos tienden a aportar frontalidad y filo en la zona de presencia.

**Objetivo: cuerpo y brillo sin agresividad**

Si el objetivo es más densidad general con brillo que no se vuelva áspero, la familia Neve suele trabajar en esa dirección. Menos filo, más masa tonal amable, mayor densidad sin que el resultado se ponga duro.

**Objetivo: flujo completo de canal con dinámica integrada**

La familia SSL no entra solo por su carácter de EQ. Entra por la lógica de canal que integra filtros, dinámica y EQ dentro de un mismo flujo de procesamiento. En situaciones donde el control operativo del strip importa tanto como el color, el SSL tiene una ventaja de diseño.

**Objetivo: peso en graves con limpieza relativa alrededor**

La curva Pultec en graves es el resultado de usar boost y attenuate simultáneos en zonas próximas: el boost añade peso y el attenuate simultáneo reorganiza la zona alrededor, lo que evita que el resultado se ensucie en medios-bajos. Ese mecanismo es lo que da su utilidad específica en la zona grave.

*[EN PANTALLA: demo de la curva Pultec con boost y attenuate activos al mismo tiempo. Analizador mostrando el resultado de la curva.]*

Lo importante no es memorizar una tabla de emparejamientos. Es entender que cada familia tiene una forma distinta de llegar a un objetivo tonal, y que el mismo objetivo puede alcanzarse de formas distintas según el material.

### 3. Teoría aplicada en el punto correcto

API Technologies, AMS Neve, Solid State Logic y Pulse Techniques son cuatro familias que se distinguen no solo por sus frecuencias disponibles, sino por tipo de circuito, respuesta de Q, comportamiento armónico y filosofía de diseño.

En el caso de la curva Pultec en graves, el efecto útil viene de la interacción entre boost y attenuate simultáneos, no de una supuesta magia abstracta del equipo. Es un mecanismo técnico documentado.

### 4. Criterio de decisión

Si se necesita frontalidad y definición en medios, API puede ser el punto de partida. Si se necesita cuerpo y brillo más amable, Neve suele dar ese resultado. Si se necesita versatilidad de canal y flujo interno integrado, SSL tiene sentido. Si se necesita peso en graves con limpieza relativa alrededor, el diseño Pultec puede ser excelente.

La decisión final depende del material real, del arreglo y del lugar que ese instrumento debe ocupar en la mezcla, no de la convención de "siempre esta marca con este instrumento".

### 5. Errores frecuentes y falsas reglas

No existe una familia universalmente superior. Cada una tiene fortalezas en contextos específicos.

No uses la curva Pultec en graves porque "siempre queda lindo". Úsala cuando necesitas el mecanismo específico de boost más attenuate simultáneos. Si el material no lo necesita, puede ensuciar más de lo que organiza.

No conviertas SSL en respuesta para todo solo porque resuelve muchas cosas. La versatilidad no es universalidad.

Si un plugin es famoso no por eso coincide con el objetivo de la pista. La pregunta sigue siendo qué objetivo tonal se está buscando.

### 6. Cierre

Hasta aquí se habló de EQ estático: una decisión tonal que actúa de forma constante. Ahora entra un caso distinto: cuando el problema no está presente todo el tiempo y una banda fija empieza a quedarse corta.

---

# E3-L07 — EQ dinámico: cuando el problema no está siempre

## Rol de esta lección dentro del proceso completo

Esta lección abre el cruce entre espectro y tiempo sin salir del Eje 3. Es la transición hacia herramientas espectrales adaptativas antes de entrar de lleno a dinámica en el Eje 4.

## Objetivo del video

Usar EQ dinámico cuando una campana fija se queda corta.

## Resultado que debería conseguir el alumno al terminar

Que pueda identificar un problema frecuencial intermitente y resolverlo sin adelgazar todo el canal permanentemente.

## Situación práctica de partida

Una guitarra con una resonancia en medios que solo aparece en notas sostenidas. Una campana fija corrige esas notas, pero empeora el resto del performance.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: guitarra en reproducción. El docente escucha varias frases. Algunas suenan normales; otras tienen una zona media que se dispara.]*

Hay problemas que no viven todo el tiempo en el canal. Si se aplica una campana fija, se castigan también los momentos que estaban bien.

### 2. Desarrollo paso a paso

**El problema con la campana estática**

*[EN PANTALLA: EQ paramétrico con una campana en la zona problemática. Reproducción de la guitarra — varios compases.]*

Se prueba la solución obvia: campana estática en la frecuencia problemática. Funciona en el momento malo. Pero cuando vuelve una frase normal, la guitarra queda más delgada de lo necesario. Se paga un costo tonal permanente por un problema que solo existe parte del tiempo.

**Reformular la pregunta**

El problema no es "necesito menos de esta frecuencia siempre". El problema es "necesito menos de esta frecuencia cuando se pasa de un umbral". Eso cambia la herramienta.

**EQ dinámico: banda con umbral**

*[EN PANTALLA: se cambia el EQ paramétrico por un EQ dinámico (ej. Fabfilter Pro-Q en modo dinámico, o Waves F6, o equivalente). Se configura la misma frecuencia con reducción de ganancia y umbral.]*

Se ubica la misma frecuencia en el EQ dinámico, se define un rango de reducción y se ajusta el umbral hasta que la banda reacciona solo cuando la resonancia realmente aparece.

*[EN PANTALLA: comparación entre campana fija y EQ dinámico en la misma guitarra. Analizador o GR del EQ dinámico visible para mostrar cuándo actúa y cuándo no.]*

En los momentos problemáticos, la zona baja. En los momentos sanos, la guitarra conserva su cuerpo. Esa es la diferencia práctica.

**El límite con la compresión multibanda**

El EQ dinámico es una herramienta espectral: actúa como una campana o shelf que solo entra cuando la energía en esa zona supera el umbral definido. Por eso su lugar pedagógico es aquí — en el eje de identidad espectral — y no en el eje de dinámica.

La compresión multibanda divide la señal por bandas amplias y procesa cada banda con un compresor independiente. Eso ya es una herramienta dinámica con división de espectro. La lógica de intervención es otra y pertenece al Eje 4.

### 3. Teoría aplicada en el punto correcto

El EQ dinámico combina localización espectral con comportamiento condicionado por umbral. Actúa como una campana o shelf que solo entra cuando la energía en esa zona supera el punto definido.

Por eso sirve cuando el problema es intermitente y no conviene confundirlo con compresión multibanda: el multibanda opera con lógica de compresor por banda y pertenece al territorio dinámico.

### 4. Criterio de decisión

EQ dinámico tiene sentido cuando el problema está en una zona concreta, no está presente todo el tiempo, y una campana estática obliga a pagar un costo tonal permanente para resolver algo que solo ocurre parte del tiempo.

Si la molestia es constante, la campana fija puede bastar. Si la zona problemática es demasiado amplia y el comportamiento es de banda completa con dinámica, la herramienta correcta empieza a acercarse más al multibanda — y eso es Eje 4.

### 5. Errores frecuentes y falsas reglas

EQ dinámico no es automáticamente más sofisticado ni mejor. Si el problema es constante, la campana fija es la solución más limpia.

No lo uses en cada canal solo porque permite ver movimiento. Donde el problema no es intermitente, el movimiento no aporta nada.

No es lo mismo que compresión multibanda aunque ambos se muevan en el tiempo. La lógica de intervención, la escala de la zona tratada y el proceso subyacente son distintos.

### 6. Cierre

Ya se resolvió un problema intermitente en una zona cualquiera del espectro. Ahora el caso más cotidiano y más maltratado: la sibilancia en voz.

---

# E3-L08 — De-esser: sibilancia sin matar la dicción

## Rol de esta lección dentro del proceso completo

Es el cierre práctico del eje. Toma la lógica del EQ dinámico y la aplica al caso más común de mezcla vocal: controlar sibilancia sin destruir la voz.

## Objetivo del video

Resolver sibilancia como problema intermitente, no como recorte bruto.

## Resultado que debería conseguir el alumno al terminar

Que pueda controlar sibilancias sin apagar el aire útil de la voz ni destruir la inteligibilidad de las consonantes.

## Situación práctica de partida

Una voz bien armada tonalmente, pero las eses saltan demasiado. Un corte fijo en la zona alta reduce la molestia, pero también apaga la voz entera.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: voz en reproducción dentro de la mezcla. Las eses saltan con claridad. EQ insertado pero sin actuar.]*

La sibilancia no es un problema de brillo constante. Es un problema que aparece por momentos. Si se trata como si estuviera presente todo el tiempo, se lleva puesta la dicción y el aire útil de la voz.

### 2. Desarrollo paso a paso

**Verificar primero: ¿qué banda es el problema real?**

*[EN PANTALLA: EQ paramétrico con barrido en la zona alta (6–10 kHz aprox). El docente localiza la frecuencia exacta donde la sibilancia se exagera.]*

No se parte cortando 7 u 8 kHz porque sí. Primero se confirma qué banda está activando el problema en esta voz concreta. El mismo procedimiento de barrido: boost con Q alto, barrer, localizar, verificar.

**El problema con el corte fijo**

*[EN PANTALLA: campana fija con corte en la frecuencia localizada. Reproducción completa de la voz.]*

Con un corte estático, la molestia baja, pero la voz pierde apertura también cuando no hay sibilancia. El costo no conviene cuando el problema es intermitente.

**De-esser: control dinámico sobre la zona sibilante**

*[EN PANTALLA: de-esser insertado (ej. Waves DeEsser, Sibilance, FabFilter Pro-DS, o equivalente). Frecuencia ajustada a la zona identificada.]*

El de-esser es una forma especializada de EQ dinámico o control dinámico sobre la zona sibilante. Se ajusta la frecuencia a la zona localizada, se define el umbral hasta que la reducción actúa solo cuando la ese realmente salta, y se controla la cantidad de reducción para no excederse.

**Modos wide y split: dos formas distintas de intervenir**

*[EN PANTALLA: selector de modo en el de-esser. El docente alterna entre wide y split y escucha el efecto en la voz.]*

Muchos de-essers ofrecen dos modos. En modo **wide** (también llamado broadband o wideband), cuando la sibilancia activa el umbral, el de-esser reduce el nivel de toda la señal — no solo de la banda sibilante. Eso suena más natural en algunos contextos porque la reducción no es espectral sino de volumen general.

En modo **split** (o bandpass), el de-esser reduce solo la banda sibilante y deja pasar el resto de la señal sin cambios. Más selectivo, menos efecto colateral sobre el resto de la voz.

La decisión no sale del nombre del modo: sale de lo que pasa con esta voz en esta mezcla. Si el modo wide suena más natural, se usa. Si el modo split da más control sin artefactos, se usa.

**Verificación: frase completa, no palabra aislada**

*[EN PANTALLA: reproducción de la voz completa durante varios compases, no solo en la palabra problemática.]*

Después de ajustar el de-esser, se escucha la voz completa. El objetivo no es ganar una batalla contra una consonante: es conservar una voz usable, clara y controlada a lo largo de toda la canción.

### 3. Teoría aplicada en el punto correcto

El de-esser funciona porque la sibilancia es intermitente. Cuando la energía en la banda sibilante supera el umbral, entra la reducción. Cuando no, la voz pasa normal.

Por eso un recorte fijo suele ser peor solución: actúa también cuando el problema no está presente. El criterio correcto no es "quitar todas las eses", sino bajar solo lo necesario para que no distraigan.

### 4. Criterio de decisión

El de-esser tiene sentido cuando la molestia está asociada a consonantes o eventos breves en una banda localizada del extremo alto. Si toda la voz está agresiva arriba, el problema puede no ser sibilancia sino balance tonal general — y la herramienta correcta es EQ estático.

Si la molestia varía mucho según palabra o interpretación, se ajusta el umbral con más cuidado y se verifica frase completa, no palabra aislada.

### 5. Errores frecuentes y falsas reglas

Una voz bien mezclada no es una voz sin eses. Las eses son parte de la dicción y de la presencia vocal. El objetivo es que no distraigan, no que desaparezcan.

No se corta brillo general para resolver una sibilancia puntual. Eso destruye la apertura de toda la voz para resolver un problema que existía solo en parte del tiempo.

No usar un preset de de-esser y asumir que quedó bien. La frecuencia y el umbral dependen de esta voz específica, no de una configuración genérica.

Si al final la voz suena más opaca pero ya no molesta, eso no significa que esté resuelto. Puede significar que la voz fue dañada en su inteligibilidad general.

### 6. Cierre

*[EN PANTALLA: voz completa en reproducción dentro de la mezcla. Clara, sin sibilancia invasiva, con dicción intacta.]*

Con esto se cierra el Eje 3. La señal ya no solo está limpia y alineada: ahora tiene identidad espectral. El siguiente paso es inevitable: cómo esa identidad reacciona en el tiempo cuando se entra al territorio de la dinámica.

---

*KENTH Academy — Eje 3 · Guiones v2 · Revisión final*
*Revisión basada en: auditoría forense, contenido canónico Eje 3, paquete limpio Eje 3, criterios pedagógicos KENTH.*
