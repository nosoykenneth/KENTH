# Guiones corregidos — Eje 1 · KENTH Academy · v2
*Revisión: auditoría final + corrección integral*

---

# E1-L01 — Peak, VU y RMS sin confundir qué mide cada uno

## Rol de esta lección dentro del proceso completo

Esta lección abre el Eje 1 y define la lógica base de todo lo que viene después: antes de corregir hay que saber qué está pasando realmente en la señal. Su función es ordenar la lectura de nivel para que el alumno deje de mirar un solo medidor esperando que responda todas las preguntas. Aquí no se toca el audio. Aquí se aprende a leerlo.

## Objetivo del video

Que el alumno entienda qué información entrega cada medidor de nivel, qué pregunta técnica responde cada uno y por qué usar el medidor equivocado lleva a decisiones equivocadas.

## Resultado que debería conseguir el alumno al terminar

Poder mirar una señal y decidir si necesita leer pico, nivel sostenido o promedio energético, sin confundir clipping con densidad ni densidad con volumen percibido. También detectar cuándo se están sacando conclusiones erróneas por mirar solo el medidor de la DAW.

## Situación práctica de partida

Se abre una sesión de mezcla. Hay una batería con transitorios altos, un pad sostenido y una voz ya comprimida desde la grabación. El medidor principal de la DAW muestra comportamientos muy distintos entre esos tres elementos, pero a simple vista no queda claro cuál está realmente más denso, cuál está más cerca del clipping y cuál solo tiene picos rápidos.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: DAW abierta con tres tracks visibles: batería, pad y voz. El medidor de nivel del master bus activo. Reproducción corriendo.]*

Antes de ecualizar nada, antes de filtrar nada y antes de pensar en compresión, hay una pregunta más básica: qué está haciendo realmente esta señal en nivel. Para responderla no alcanza con mirar una barra que sube y baja. Esa barra puede estar mostrando picos, pero no necesariamente el peso sostenido de la señal. Si no se separan esas dos cosas desde el principio, se mezcla a ciegas.

Este eje opera sobre la cadena calibrada del Eje 0. Los valores de referencia AES/EBU que el alumno estableció allí son el punto de partida para que estas lecturas tengan significado. Sin esa base, los números son arbitrarios.

Aquí se ordenan tres lecturas: Peak, VU y RMS. No para memorizarlas como teoría de manual, sino para que al abrir una sesión se sepa qué se está mirando y qué no.

### 2. Desarrollo paso a paso

**Peak: la lectura de picos**

*[EN PANTALLA: bus de batería en solo. Se inserta un medidor de pico con retención (ej. el medidor de canal del DAW con hold activado, o un plugin tipo Youlean o el meter nativo del canal). Reproducción activa.]*

Se reproduce solo el bus de batería y se observa el medidor. La barra salta fuerte y rápido. Los picos son altos. Pero eso por sí solo no indica cuánta densidad tiene la batería en el tiempo. Lo único que revela es hasta dónde llegó el transitorio más alto. Ese es el territorio del Peak.

El medidor de pico con retención permite saber si hay riesgo de clipping y cuál fue el valor máximo alcanzado. Si el bombo pegó en −5 dBFS, eso importa para el headroom. Pero no significa que la batería esté densa o comprimida. Solo significa que tuvo un pico alto.

**VU: la lectura de nivel sostenido**

*[EN PANTALLA: bus del pad en solo. Se inserta un plugin de VU meter (ej. VU Meter de Klanghelm u otro equivalente). Reproducción activa.]*

Se reproduce el pad solo. En el medidor Peak no parece pasar gran cosa: no tiene golpes bruscos. Pero al oído ocupa bastante espacio y sostiene energía todo el tiempo. El medidor Peak se queda corto para esa pregunta.

Se inserta un VU. La aguja se mueve más lento, integra la señal durante aproximadamente 300 ms y muestra cuánto peso sostiene ese pad en el tiempo. Esa lectura es más útil aquí.

**RMS: promedio energético con ventana definida**

*[EN PANTALLA: canal de voz con un medidor RMS activo (plugin con lectura RMS visible, ej. Waves PAZ Meters en modo RMS, o el panel de análisis del DAW). Se selecciona una sección representativa de la voz.]*

La voz tiene frases, consonantes, aire y una dinámica intermedia. Para comparar su peso general con otro elemento sostenido, el VU sirve. Para una lectura matemática más estable del promedio energético, se usa RMS.

Se inserta un medidor RMS y se reproduce una sección representativa — no una sílaba aislada ni el track entero con silencios. La lectura describe cuánto peso energético sostiene la voz en un tramo representativo.

**La comparación clave**

*[EN PANTALLA: el docente pone en paralelo el medidor Peak del bus de batería y el VU del pad. Los dos se reproducen mientras se observan los medidores simultáneamente.]*

Se deja sonando un golpe de batería y luego el pad. El Peak del golpe puede ser más alto que el del pad, pero el VU del pad puede quedar considerablemente más arriba porque está sosteniendo energía durante más tiempo.

Eso es exactamente lo que el alumno necesita ver: pico alto no equivale a señal densa. Señal densa no equivale a señal con más transitorio. Son dos dimensiones distintas del nivel.

*[EN PANTALLA: el medidor vertical principal del DAW mostrando solo barras de pico. El docente señala el medidor.]*

El medidor vertical de la DAW normalmente es Peak. Sirve, sí. Pero solo responde una parte del problema.

### 3. Teoría aplicada en el punto correcto

Peak es lectura instantánea o casi instantánea del máximo valor alcanzado. Su función principal es proteger la cadena frente al clipping y documentar el techo real al que está llegando el audio.

VU integra aproximadamente 300 ms. No reacciona como el Peak. Justamente por eso sirve para leer nivel sostenido y aproximarse mejor al peso percibido de una señal continua.

RMS calcula la raíz cuadrática media dentro de una ventana temporal. No es un medidor "más musical" que VU ni un reemplazo automático. Es otra forma de leer promedio energético. Su ventaja es que permite comparaciones más controladas siempre que el tiempo de integración sea consistente entre los medidores que se están comparando.

En una señal muy percusiva, Peak y VU pueden separarse varios decibeles. Esa diferencia no es un problema: es información.

### 4. Criterio de decisión

El criterio no es elegir un medidor favorito. Es elegir la lectura que corresponde a la pregunta.

Si la pregunta es "estoy cerca de clipping", la respuesta viene del Peak.

Si la pregunta es "esta señal está trabajando demasiado alta para un procesador que espera un nivel sostenido razonable", VU o RMS son más útiles.

Si la pregunta es "cuál de estos dos elementos está ocupando más peso continuo en la mezcla", Peak no alcanza. Se necesita una lectura integrada.

### 5. Errores frecuentes y falsas reglas

El medidor de la DAW no responde todo. Normalmente muestra picos.

Una señal con picos altos no necesariamente suena más fuerte o más llena. Puede tener mucho transitorio y poca densidad.

Usar VU como único medidor en material muy percusivo y luego sorprenderse cuando aparecen clips más adelante en la cadena es uno de los errores más frecuentes.

RMS y VU no son idénticos. Se parecen en la función general de leer nivel sostenido, pero no son la misma lectura ni reaccionan igual.

Mezclar mirando números en vez de entender qué representan esos números.

### 6. Cierre

Con esto ya no se miran barras por costumbre. Se lee nivel con intención. En la siguiente lección se da un paso más: ya no solo se quiere saber qué tan alto llega una señal o cuánto sostiene. Se quiere leer densidad global y destino de entrega. Ahí entran K-System y LUFS.

---

# E1-L02 — K-System y LUFS: leer densidad y destino

## Rol de esta lección dentro del proceso completo

Esta lección amplía la lectura de nivel hacia dos problemas que no resuelven ni Peak ni VU por sí solos: la densidad global del material y la referencia de destino. Su papel es enseñar a distinguir pico instantáneo de sonoridad integrada, y a entender por qué una mezcla puede tener picos controlados pero seguir estando muy lejos de la referencia real con la que se está comparando.

## Objetivo del video

Leer sonoridad integrada con criterio, diferenciar K-System de LUFS y entender qué información aporta cada uno cuando se compara una mezcla con referencias o se prepara material para la siguiente fase del flujo.

## Resultado que debería conseguir el alumno al terminar

Poder comparar una mezcla con una referencia comercial sin reducir la diferencia a "esta suena más fuerte". Cuantificar densidad, entender que LUFS integrado no es lo mismo que Peak y usar esa lectura para ubicar el material dentro de un contexto real de trabajo.

## Situación práctica de partida

Una mezcla en progreso y una referencia comercial del mismo tipo de producción. Al igualar picos, la referencia sigue sonando más densa, más presente y más estable. El alumno necesita entender qué está midiendo esa diferencia y cómo leerla sin saltar a comprimir por reflejo.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: dos canales en el DAW: la mezcla en progreso y la referencia comercial importada. Ambas tienen picos similares en el medidor Peak.]*

Comparar una mezcla con una referencia solo por pico máximo no sirve. Pueden existir dos temas con el mismo techo de pico y una diferencia brutal en densidad percibida. Si no se sabe leer eso, se corre el riesgo de empujar la mezcla en la dirección equivocada solo porque la referencia "suena más grande".

### 2. Desarrollo paso a paso

**LUFS: sonoridad integrada**

*[EN PANTALLA: plugin de medidor LUFS (ej. Youlean Loudness Meter, LUFS Meter de Klanghelm, iZotope Insight, o equivalente). El docente lo inserta en la referencia comercial y deja correr un fragmento. La lectura que importa: LUFS Integrated, no el momentary.]*

Se carga la referencia comercial en un canal aparte y se deja sonando un fragmento completo. Se mira el medidor LUFS. La lectura momentánea oscila demasiado con cada evento. Lo que se necesita es la lectura **integrada**: la que resume el programa completo o al menos una sección representativa.

*[EN PANTALLA: el mismo plugin ahora en la mezcla del alumno. Reproducción del mismo fragmento. Se comparan los valores integrados entre la referencia y la mezcla.]*

Se hace lo mismo con la mezcla. Si la mezcla está varios LU por debajo de la referencia, eso ya no es una impresión. Es una diferencia cuantificada. No se dice "creo que le falta fuerza". Se puede decir: la diferencia de densidad integrada es real y mide N LU.

Eso no significa comprimir inmediatamente. Significa saber exactamente qué diferencia hay y decidir en qué etapa del flujo corresponde resolverla.

**K-System: organizar la lectura según el rango dinámico**

*[EN PANTALLA: medidor con escala K (plugin o medidor del DAW con modo K activo). El docente muestra K-20, K-14 y K-12 como selectores de escala.]*

El K-System fue desarrollado por Bob Katz como sistema de medición de sonoridad calibrada. Las tres escalas —K-20, K-14 y K-12— no son adornos. Son tres contextos distintos de operación según el rango dinámico esperado del material.

K-20 deja más margen y tiene sentido en material con amplio rango dinámico: orquesta, postproducción, material de alta fidelidad. K-14 es una referencia práctica para producción pop/rock de alta calidad. K-12 se acerca al comportamiento de material muy comprimido orientado a broadcast.

Lo que el alumno necesita ver: K-System organiza la relación entre referencia de escucha y rango dinámico esperado del tipo de producción. LUFS, en cambio, es la lectura estándar de sonoridad integrada que va a dialogar directamente con destinos de distribución y normalización.

**La comparación final: tres cosas distintas**

*[EN PANTALLA: tres lecturas en pantalla para la misma mezcla: Peak, LUFS integrado, y medidor K. El docente señala cada uno y describe qué pregunta responde.]*

Una mezcla puede no clippear y estar muy por debajo de la referencia en LUFS. O puede estar muy densa en LUFS y aun así conservar picos moderados. Por eso no se reemplazan entre sí.

### 3. Teoría aplicada en el punto correcto

LUFS mide sonoridad ponderada en el tiempo según el estándar EBU R128 / ITU-R BS.1770, diseñado para aproximarse mejor a la percepción auditiva que un medidor de pico. Tiene tres lecturas: Momentary (ventana de 400 ms), Short-Term (aproximadamente 1–3 s) e Integrated (programa completo). Para decisiones de comparación global y destino, la más relevante es la integrada.

True Peak no es lo mismo que LUFS. True Peak controla los picos de reconstrucción entre muestras (en dBTP). LUFS mide sonoridad integrada. Uno no reemplaza al otro.

El K-System fue diseñado por Bob Katz. Sus tres escalas —K-20, K-14 y K-12— están calibradas a 85 dBSPL en ponderación C en el punto de escucha. Son contextos de trabajo, no niveles de entrega definitivos.

### 4. Criterio de decisión

Si la pregunta es "qué tan denso está este material respecto a otro", LUFS integrado es la lectura más directa.

Si la pregunta es "en qué contexto de rango dinámico quiero organizar mi escucha y mi referencia de trabajo", K-System ofrece una estructura útil.

Si se descubre una diferencia de 5 o 6 LU respecto a una referencia, eso no significa automáticamente comprimir más en ese momento. Primero hay que decidir en qué etapa del flujo corresponde resolver esa diferencia y si esa referencia es realmente comparable en arreglo, género y objetivo.

### 5. Errores frecuentes y falsas reglas

Usar LUFS momentary como lectura global. No lo es. Sirve para comportamiento instantáneo, no para resumen del programa.

Perseguir un número de LUFS demasiado pronto y empezar a deformar la mezcla antes de que el balance esté resuelto.

Creer que si dos temas tienen el mismo pico máximo deberían sentirse igual de fuertes.

Tratar K-System como norma universal obligatoria. Es una metodología de referencia útil con contextos específicos de uso.

Comparar una mezcla contra cualquier track comercial sin verificar si realmente juega en la misma cancha estética y dinámica.

### 6. Cierre

Ya hay una lectura más seria de nivel y densidad. Pero todavía se está en el dominio del nivel. La siguiente lección cambia de pregunta: ya no se pregunta cuánto nivel hay, sino cómo se relacionan las señales entre sí. Entramos en polaridad.

---

# E1-L03 — Polaridad: cómo detectar el problema antes de tocar nada

## Rol de esta lección dentro del proceso completo

Esta lección inaugura el bloque relacional del Eje 1. Su papel es identificar un problema que muchas veces se corrige por reflejo sin diagnóstico, o que se nombra mal. Aquí se separa la inversión de polaridad de otros fenómenos y se establece una metodología de lectura antes de tocar el botón ∅.

## Objetivo del video

Detectar inversión de polaridad por escucha y por lectura comparativa, entendiendo cuándo tiene sentido revisar polaridad y cuándo el problema real está en otro lado.

## Resultado que debería conseguir el alumno al terminar

Poder revisar dos señales relacionadas, escuchar su suma, observar su comportamiento y decidir con criterio si hay inversión de polaridad. Dejar de usar "fase" como palabra comodín para todo.

## Situación práctica de partida

Dos micrófonos capturando la misma fuente — por ejemplo el top y el bottom de un tambor. Al sumarlos, el cuerpo desaparece o se adelgaza de forma anormal. El alumno necesita saber si está frente a una inversión de polaridad o frente a otro problema relacional.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: dos canales del DAW — top y bottom de un tambor — activos y en reproducción. El bus que los suma muestra menos cuerpo del esperado.]*

Hay decisiones que parecen pequeñas pero cambian completamente lo que viene después. Una de ellas es esta: sumar dos señales y no saber si se están ayudando o destruyendo entre sí.

Antes de revisar nada, hay que nombrar bien el problema. El botón marcado ∅ en el canal no es un botón de fase: es un inversor de polaridad. Invierte el signo de toda la señal de forma uniforme en todas las frecuencias. Eso es distinto de un desplazamiento temporal, que produce cancelaciones selectivas según frecuencia. Esa distinción va a importar en la lección siguiente.

### 2. Desarrollo paso a paso

**Escuchar antes de tocar**

*[EN PANTALLA: los dos canales del tambor en suma. Se reproduce el pasaje. El docente no toca nada. Luego mutea uno y otro alternativamente.]*

Se ponen en solo los dos canales relacionados. Primero se escuchan juntos sin tocar nada. Solo se escucha si al sumarse aparece una pérdida extraña de cuerpo, de low end o de pegada.

Después se mutea uno y luego el otro, para construir una referencia mental clara de cómo suena cada señal por separado y cómo suenan en conjunto. Si la suma suena claramente más débil que una de las señales sola en una zona donde debería reforzarse, hay un indicio.

**Invertir y comparar**

*[EN PANTALLA: el docente activa el botón ∅ (inversor de polaridad) en el canal bottom. Comparación directa A/B mientras la reproducción continúa.]*

Se activa la inversión de polaridad en uno de los dos canales. No porque "siempre haya que probar": se hace porque ya se escuchó un síntoma compatible con problema de polaridad.

Si al invertir la suma recupera cuerpo, estabilidad y centro de forma clara, hay un indicio fuerte de que una de las señales estaba invertida respecto a la otra.

*[EN PANTALLA: el docente alterna la inversión on/off varias veces. La diferencia debe ser audible.]*

Si no cambia casi nada, o mejora una zona pero empeora otra de forma rara, entonces probablemente no es un problema binario de polaridad. Hay que seguir leyendo en otra dirección.

**El caso donde invertir no arregla**

*[EN PANTALLA: par de señales donde el problema no desaparece con la inversión de polaridad.]*

Este caso es igual de importante que el anterior. Si se enseña solo el caso donde sí funciona, el alumno termina creyendo que siempre hay una respuesta binaria y rápida para cualquier problema de suma.

**La rutina corta**

La secuencia es: escuchar cada señal sola → escuchar la suma → invertir polaridad en una sola → volver a escuchar la suma → decidir según el resultado total, no según una banda aislada.

### 3. Teoría aplicada en el punto correcto

Invertir polaridad significa invertir el signo de toda la señal: lo positivo pasa a negativo y lo negativo a positivo. Es una operación binaria. No desplaza unas frecuencias más que otras. No introduce un retardo.

Por eso el botón ∅ normalmente no es un "botón de fase". Es un inversor de polaridad. El problema aparece cuando esa señal se suma con otra relacionada. Escuchada sola, la inversión de polaridad puede no cambiar casi nada perceptible, porque el oído es poco sensible a la inversión de una señal sin referencia.

### 4. Criterio de decisión

Se revisa polaridad cuando hay señales que representan la misma fuente o una fuente estrechamente relacionada y la suma se comporta peor de lo esperable.

No se revisa polaridad por costumbre en cualquier canal aislado.

Si al invertir la suma mejora de forma global, consistente y clara, la corrección tiene sentido. Si mejora algo y destruye otra cosa, o si casi no cambia, probablemente el problema no sea polaridad sino relación temporal o comportamiento frecuencial más complejo.

### 5. Errores frecuentes y falsas reglas

Llamar "problema de fase" a cualquier situación en que dos señales no sumen bien. El lenguaje importa porque define qué herramienta usar.

Apretar ∅ al azar hasta que algo "guste más". No se trata de gusto instantáneo: se trata de coherencia técnica de la suma.

Revisar polaridad en un canal solo como si ahí fuera a revelarse algo concluyente. La polaridad solo tiene sentido evaluarla en suma.

Pensar que si invertir polaridad no arregla el problema, entonces no hay ningún problema. Puede haber desfasaje temporal — que es la lección siguiente.

Corregir polaridad sin escuchar la suma completa en contexto relacional.

### 6. Cierre

Con polaridad ya está resuelto el problema binario más básico de relación entre señales. Pero no todo lo que suena hueco o flaco es polaridad. En la siguiente lección se entra en el terreno más fino: fase, desfasaje y comb filtering.

---

# E1-L04 — Fase y comb filtering: leer relaciones, no adivinar

## Rol de esta lección dentro del proceso completo

Esta lección lleva al alumno del problema binario de polaridad al territorio continuo y más complejo de la relación temporal y frecuencial entre señales. Su función es diagnosticar, no corregir. Deja preparado el terreno para que el Eje 2 intervenga con alineación temporal u otras acciones.

## Objetivo del video

Diferenciar inversión de polaridad, desfasaje y comb filtering, y reconocer por escucha y lectura cuándo una suma está generando cancelaciones parciales.

## Resultado que debería conseguir el alumno al terminar

Escuchar dos señales relacionadas y detectar si el problema es una cancelación binaria simple o un patrón de filtrado en peine producto de diferencias temporales. Identificar que una suma problemática no siempre se corrige con el botón ∅.

## Situación práctica de partida

Dos micrófonos de una misma fuente con un pequeño retardo relativo entre sí. Al sumarlas, algunas zonas del espectro se refuerzan y otras se cancelan. El resultado no es una desaparición total, sino una coloración rara, hueca o filtrada.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: dos señales relacionadas en el DAW. En la lección anterior se resolvió el problema binario de polaridad. Ahora las señales suenan pero todavía hay una coloración extraña al sumarlas.]*

Si en la lección anterior el problema era binario — normal o invertido — aquí se entra en un problema gradual. Las señales ya no están simplemente de un lado o del otro. Están llegando en momentos diferentes. Y cuando eso pasa, la suma deja una firma muy particular: el comb filtering.

### 2. Desarrollo paso a paso

**Escuchar el patrón**

*[EN PANTALLA: dos señales relacionadas en suma. Reproducción activa. El docente describe el timbre raro que se escucha.]*

Se cargan dos señales relacionadas y se escucha en solo conjunto. El alumno debe oír ese timbre particular: como hueco, peinado o con cierta coloración que no pertenece a ninguna de las dos señales por separado.

**Descartar polaridad como solución**

*[EN PANTALLA: el docente activa el botón ∅ en una de las señales. Se escucha. El problema cambia pero no desaparece limpiamente.]*

Se repite el gesto de la lección anterior: se invierte la polaridad. ¿Se arregla del todo? No. Quizá cambia el patrón, quizá mueve el problema a otra zona, quizá hasta empeora algo. Ese momento separa el diagnóstico anterior de este nuevo fenómeno.

**Visualizar la firma del comb filtering**

*[EN PANTALLA: se inserta un analizador espectral (SPAN o equivalente) en el bus de suma. Reproducción activa. Se observa el espectro: no hay un solo hueco sino una serie de valles periódicos a intervalos regulares.]*

Se observa el analizador espectral. La firma del comb filtering no es un solo hueco en el espectro: es una serie de valles periódicos, repetidos a intervalos regulares. Esa repetición es la clave del diagnóstico.

**Demo de retardo artificial**

*[EN PANTALLA: el docente duplica una señal de audio en un segundo canal. Selecciona el clip duplicado y lo desplaza manualmente en el timeline del DAW unos pocos milisegundos o samples. El analizador espectral muestra cómo aparecen los valles periódicos a medida que el desplazamiento aumenta.]*

Se hace una prueba directa: se duplica una señal y se desplaza la copia unos pocos milisegundos en el timeline. Al reproducir, el analizador muestra cómo aparecen los valles periódicos del peine. Cuanto mayor es el desplazamiento temporal, más juntos quedan los valles.

Esto no es física abstracta. Es tiempo relativo entre señales, y es lo que ocurre cuando dos micrófonos sobre la misma fuente están en posiciones distintas en el espacio.

**Casos reales donde ocurre esto**

*[EN PANTALLA: el docente señala distintos tracks en la sesión — overheads, close mics, capas de grabación.]*

Overheads y micrófonos cercanos en batería, capas de guitarra registradas en distintas posiciones, duplicados de pistas mal alineados: en todos esos casos el oído puede confundir el problema con falta de cuerpo, falta de foco o "mala EQ". No es EQ. Es relación temporal entre señales.

En el Eje 1 solo se diagnostica. Si la lectura confirma comb filtering, se registra el hallazgo. La corrección — alineación temporal u otras acciones — ocurre en el Eje 2.

### 3. Teoría aplicada en el punto correcto

La fase describe la relación entre señales en términos de posición en el ciclo de la onda. Cuando dos señales similares llegan en tiempos distintos, la diferencia de tiempo equivale a diferencias de fase distintas según la frecuencia. Por eso no se cancela todo por igual: se cancelan unas bandas y otras no.

Ese patrón periódico de refuerzos y cancelaciones se llama comb filtering porque el espectro, visto en un analizador, se parece a un peine.

La polaridad invertida es una operación binaria y uniforme. El desfasaje temporal no: depende de la frecuencia y del retardo relativo entre señales.

### 4. Criterio de decisión

Si la suma empeora de forma global y una inversión de polaridad la arregla claramente: el problema era más cercano a una inversión de polaridad.

Si la suma suena filtrada, hueca, con valles repetidos en el analizador, y la inversión de polaridad no resuelve el problema de forma limpia: probablemente hay un desfasaje temporal y comb filtering.

Si el analizador muestra valles periódicos y la escucha confirma esa coloración: hay un diagnóstico operativo suficiente para pasar al Eje 2.

### 5. Errores frecuentes y falsas reglas

Seguir llamando "problema de fase" a todo sin separar qué tipo de relación está fallando. El lenguaje impreciso lleva a la herramienta equivocada.

Intentar arreglar comb filtering con EQ. Se puede disimular algo, pero no se corrigió la causa.

Pensar que si dos señales no cancelan por completo, entonces no hay un problema relacional serio. El comb filtering no requiere cancelación total para ser dañino.

Duplicar una señal, retrasarla unos samples para "abrirla" y no revisar lo que eso hace al colapsar a mono.

Querer corregir antes de haber descrito bien el síntoma.

### 6. Cierre

Hasta aquí se sabe leer nivel y relaciones entre señales. Falta una tercera lectura: cómo está distribuida la energía por frecuencia. En la siguiente lección se entra al analizador espectral, pero no como adorno visual. Se configura para que realmente sirva.

---

# E1-L05 — Analizador espectral: cómo configurarlo para que sí sirva

## Rol de esta lección dentro del proceso completo

Esta lección abre el bloque espectral del Eje 1. Su función es convertir el analizador en un instrumento de diagnóstico real, no en una pantalla que confirma prejuicios. El alumno aprende a configurar escala, resolución y comportamiento temporal del analizador según la pregunta que está intentando responder.

## Objetivo del video

Configurar un analizador espectral con criterio, entendiendo qué cambia al modificar escala, FFT, ventana y promediado, y para qué tipo de diagnóstico sirve cada ajuste.

## Resultado que debería conseguir el alumno al terminar

Montar un analizador útil para detectar subsónicas, resonancias, balance tonal global o firmas de comb filtering, sin sacar conclusiones torcidas por una mala configuración del instrumento.

## Situación práctica de partida

Se abre un analizador en mitad de la sesión. Aparece una montaña de información moviéndose todo el tiempo pero no queda claro si se está leyendo graves reales, resonancias puntuales, ruido o comportamiento normal de la señal. El problema no es que falte el analizador. Es que no está configurado para la pregunta correcta.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: SPAN (o analizador equivalente) insertado en el bus de salida de la mezcla. Configuración por defecto activa. Reproducción corriendo.]*

Abrir un analizador no equivale a entender el espectro. Si la configuración no corresponde a la pregunta que se está haciendo, el instrumento no aclara nada. Solo distrae con movimiento.

### 2. Desarrollo paso a paso

**Empezar desde la configuración por defecto**

*[EN PANTALLA: el analizador con configuración por defecto. El docente señala la pantalla.]*

Se inserta el analizador y se deja con la configuración estándar. La respuesta honesta a "qué se está viendo exactamente" es: todavía no mucho. Hay demasiada información y no está enfocada para ninguna pregunta concreta.

**Escala de frecuencia: logarítmica vs. lineal**

*[EN PANTALLA: el docente cambia la escala del analizador entre logarítmica y lineal. Se observa el cambio visual.]*

Una escala logarítmica organiza mejor la percepción del rango audible para música: distribuye el espectro de forma más cercana a cómo el oído percibe las relaciones entre frecuencias. Graves, medios y agudos se leen con más sentido. La lineal puede tener utilidad en análisis específicos, pero para diagnóstico general de mezcla, la logarítmica es más práctica.

**Resolución FFT**

*[EN PANTALLA: el docente cambia el tamaño de FFT de bajo a alto y muestra el cambio en la definición visual del espectro.]*

Con resolución FFT baja, el analizador responde rápido pero con poco detalle fino: útil para lectura de balance dinámico. Con resolución alta, se pueden ver resonancias más precisas, pero se pierde inmediatez temporal y la lectura se vuelve más pesada.

Criterio: para balance tonal general, no se necesita una FFT exageradamente alta. Para cazar una resonancia estrecha o ver el patrón de un comb filter, sí conviene mayor resolución.

**Ventana y promediado**

*[EN PANTALLA: el docente ajusta el parámetro de promediado o Average Time. Sin promediado: pantalla que se mueve caóticamente. Con promediado moderado: imagen más estable.]*

Sin promediado, la pantalla puede moverse tanto que se terminan leyendo accidentes y no tendencias. Con un promedio razonable, la imagen se estabiliza y se puede evaluar mejor el balance general.

**Cuatro preguntas, cuatro configuraciones**

*[EN PANTALLA: el docente ajusta el analizador para cada uno de los cuatro casos y señala los cambios de configuración.]*

**Caso 1 — Energía subsónica:** se baja el zoom del eje de amplitud para ver claramente si debajo del fundamento del material hay contenido inútil por debajo de los 20–30 Hz.

**Caso 2 — Resonancia puntual:** se sube la resolución FFT y se reduce la dependencia del promedio para ver picos estrechos con más precisión.

**Caso 3 — Balance tonal global vs. referencia:** se usa escala logarítmica y promediado suficiente para leer tendencia, no microaccidentes. Se puede cargar la referencia en paralelo para comparar curvas.

**Caso 4 — Sospecha de comb filtering:** se ajusta la resolución para que los valles periódicos sean visibles como patrón repetido, no como accidentes aislados.

*[EN PANTALLA: en cada caso, el analizador muestra el patrón específico descrito.]*

El analizador no tiene una configuración "correcta". Tiene configuraciones útiles según el diagnóstico.

### 3. Teoría aplicada en el punto correcto

La FFT determina cómo se descompone la señal en componentes frecuenciales para ser visualizada. Más resolución permite distinguir detalles más finos en frecuencia, pero compromete la respuesta temporal: no se puede tener las dos cosas al máximo al mismo tiempo.

La ventana influye en cómo se comporta el análisis en el tiempo y en la precisión de la representación espectral. El promediado suaviza el comportamiento para que se pueda leer tendencia y no solo fluctuación instantánea.

La escala logarítmica organiza la frecuencia de un modo más cercano a cómo se percibe el rango musical.

### 4. Criterio de decisión

Para balance tonal global: escala logarítmica, promediado moderado, resolución FFT media.

Para resonancia puntual: alta resolución FFT, poco o nada de promediado.

Para energía subsónica: extender el rango de visualización hacia abajo, ajustar la escala de amplitud para que la zona baja sea legible.

Para comb filtering: resolución suficiente para ver los valles periódicos con claridad.

Si se compara con una referencia, no se copia la curva visual como receta. Se usa la referencia para detectar desbalances grandes, no para forzar coincidencia milimétrica.

### 5. Errores frecuentes y falsas reglas

Usar siempre la configuración por defecto.

Creer que más resolución FFT siempre es mejor. A veces solo vuelve la lectura más torpe para el tipo de diagnóstico que se está haciendo.

Usar el analizador como juez final de EQ o balance.

Querer que la mezcla copie exactamente la silueta de una referencia comercial.

Olvidar que el analizador complementa la escucha; no la reemplaza.

### 6. Cierre

Ya se sabe leer nivel, relaciones y espectro. Queda cerrar el eje con una lectura que conecta directamente con el espacio estéreo: goniómetro y correlatómetro. Ahí se va a ver apertura, correlación y riesgo de mono antes de que el Eje 5 empiece a construir imagen.

---

# E1-L06 — Imagen estéreo: goniómetro y correlatómetro

## Rol de esta lección dentro del proceso completo

Esta lección cierra el Eje 1 integrando la lectura espacial de la mezcla. Su función es enseñar a leer apertura, distribución entre canales y riesgo de monocompatibilidad sin modificar todavía la imagen. También deja tendido el puente natural hacia el Eje 2 (corrección de relaciones) y el Eje 5 (construcción deliberada de imagen).

## Objetivo del video

Usar goniómetro y correlatómetro para diagnosticar la imagen estéreo de una señal o mezcla, distinguir apertura útil de incoherencia problemática y detectar riesgo de colapso al pasar a mono.

## Resultado que debería conseguir el alumno al terminar

Mirar y escuchar una mezcla, interpretar si la imagen está centrada, abierta, demasiado lateral o en riesgo de cancelación, y registrar ese diagnóstico antes de pasar a la fase de corrección o construcción espacial.

## Situación práctica de partida

Una mezcla que en estéreo parece amplia y atractiva, pero al colapsarla a mono algunos elementos caen de nivel o cambian demasiado. El alumno necesita una forma de leer esa situación antes de decidir si el problema es tolerable, creativo o técnicamente peligroso.

## Estructura del guion

### 1. Apertura

*[EN PANTALLA: mezcla completa en reproducción. Plugin de análisis estéreo (ej. SPAN Plus, iZotope Insight, Waves PAZ Analyzer, o equivalente) con vista de goniómetro y correlatómetro activos.]*

Una mezcla puede parecer grande en estéreo y aun así estar mal construida en términos de coherencia entre canales. Si no se lee eso antes, se puede quedar enamorado de una apertura que luego se desarma en mono.

Este es el último instrumento del Eje 1. Como los demás, no corrige nada: diagnostica.

### 2. Desarrollo paso a paso

**Goniómetro: leer distribución entre canales**

*[EN PANTALLA: mezcla relativamente centrada en reproducción. Goniómetro visible. La figura se muestra principalmente vertical.]*

Se empieza con una mezcla relativamente centrada. Lo primero que el alumno necesita entender es que el goniómetro no muestra "dibujitos bonitos". La forma refleja cómo se distribuye la energía entre los dos canales.

Si la imagen aparece como una figura principalmente vertical y concentrada, hay bastante contenido correlacionado y centrado. Si se abre en diagonal, la mezcla tiene más diferencias entre canales izquierdo y derecho.

*[EN PANTALLA: se abre más la imagen estéreo con un efecto o al activar elementos laterales. El goniómetro se ensancha.]*

Se abre más la imagen y el goniómetro se ensancha. Pero esa apertura visual no indica todavía si es segura. Para eso se mira el correlatómetro.

**Correlatómetro: leer coherencia entre canales**

*[EN PANTALLA: el correlatómetro visible junto al goniómetro. La aguja o barra se mueve entre −1 y +1.]*

Valores cercanos a +1 indican alta correlación: los canales se mueven muy parecido. Al acercarse a 0 hay menos coherencia. Si se va hacia negativo, aparece riesgo fuerte de cancelación al colapsar a mono.

**Prueba de colapso a mono**

*[EN PANTALLA: el docente activa el modo mono del DAW (función Mono del master bus, o un plugin de utilidades de suma a mono, o el botón de mono del sistema de monitoreo). Reproducción activa.]*

Se escucha la mezcla en estéreo, se observan ambas herramientas y luego se colapsa a mono. El alumno ve y escucha qué pasa cuando una imagen que parecía impresionante en estéreo pierde información al sumarse.

*[EN PANTALLA: el docente alterna estéreo y mono mientras la mezcla reproduce.]*

Si la diferencia es drástica — elementos que desaparecen, cambios fuertes de nivel en el centro, frecuencias que se cancelan — hay información de diagnóstico concreta. No es necesariamente una emergencia, pero es un hallazgo que hay que registrar.

**El rango normal de trabajo**

Una mezcla no necesita vivir pegada a +1 todo el tiempo para estar bien. Una apertura saludable puede hacer que la correlación baje sin entrar en zona problemática. El objetivo no es mezclar "todo súper correlacionado". El objetivo es entender el costo de cada decisión espacial.

### 3. Teoría aplicada en el punto correcto

El goniómetro representa visualmente la relación instantánea entre canal izquierdo y derecho. Una traza más vertical sugiere mayor componente común entre ambos canales. Una traza más ancha u horizontal sugiere más diferencia lateral entre ellos.

El correlatómetro resume la coherencia entre canales en un valor. Cerca de +1: alta correlación. Cerca de 0: poca correlación. En negativo: riesgo de cancelación al sumar a mono.

Ninguna de las dos herramientas decide sola si algo está bien o mal. Son instrumentos de lectura que siempre se cruzan con escucha.

### 4. Criterio de decisión

Si la mezcla pierde demasiado al colapsar a mono y el correlatómetro cae con frecuencia a zona negativa: síntoma serio de incompatibilidad que requiere atención.

Si la mezcla está abierta, el goniómetro lo confirma y el correlatómetro baja moderadamente sin comprometer la suma en mono: esa apertura probablemente es funcional.

Si una fuente crítica del centro — voz principal, bombo, bajo — cambia demasiado en mono: hay una decisión espacial o relacional que requiere revisión.

### 5. Errores frecuentes y falsas reglas

Creer que una mezcla buena debe quedarse siempre cerca de +1. Eso mataría mucha apertura útil.

Creer que una imagen ancha siempre es mejor.

Mirar el goniómetro como si fuera un adorno y no una lectura relacional.

Aprobar una imagen estéreo sin colapsar a mono al menos como verificación.

Tratar cualquier caída en correlación como si fuera automáticamente un desastre técnico.

### 6. Cierre

*[EN PANTALLA: tabla visible en pantalla o sobre el contenido del DAW: dos columnas — DIAGNÓSTICO (Eje 1) → CORRECCIÓN (Eje 2).]*

Con esto el Eje 1 queda completo. Ya se sabe leer nivel, densidad, relaciones entre señales, espectro e imagen estéreo.

Cada uno de esos diagnósticos activa una acción específica en el Eje 2:

| Diagnóstico (Eje 1) | Corrección (Eje 2) |
|---|---|
| Inversión de polaridad | Botón ∅ en el micrófono correcto |
| Comb filtering entre micrófonos | Alineación temporal / ajuste de fase |
| Señal con nivel mal calibrado | Gain staging por elemento |
| Imagen con riesgo de cancelación | Corrección de relación entre canales |

Lo que sigue ya no es adivinar. Es corregir lo que esta lectura acaba de revelar.

---

*KENTH Academy — Eje 1 · Guiones v2 · Revisión final*
*Revisión basada en: auditoría forense, contenido canónico Eje 1, paquete limpio Eje 1, criterios pedagógicos KENTH.*
