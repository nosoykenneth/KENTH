# E1-L01 — Peak, VU y RMS sin confundir qué mide cada uno

## Rol de esta lección dentro del proceso completo

Esta lección abre el Eje 1 y define la lógica base de todo lo que viene después: antes de corregir, hay que saber qué está pasando realmente en la señal. Su función es ordenar la lectura de nivel para que el alumno deje de mirar un solo medidor esperando que responda todas las preguntas. Aquí no se toca el audio. Aquí se aprende a leerlo.

## Objetivo del video

Que el alumno entienda qué información entrega cada medidor de nivel, qué pregunta técnica responde cada uno y por qué usar el medidor equivocado lleva a decisiones equivocadas.

## Resultado que debería conseguir el alumno al terminar

El alumno debería poder mirar una señal y decidir si necesita leer pico, nivel sostenido o promedio energético, sin confundir clipping con densidad ni densidad con volumen percibido. También debería poder detectar cuándo está sacando conclusiones erróneas por mirar solo el medidor de la DAW.

## Situación práctica de partida

Estamos abriendo una sesión de mezcla. Hay una batería con transitorios altos, un pad sostenido y una voz ya comprimida desde la grabación. El medidor principal de la DAW muestra comportamientos muy distintos entre esos tres elementos, pero a simple vista no queda claro cuál está realmente más denso, cuál está más cerca del clipping y cuál solo tiene picos rápidos.

## Estructura del guion

### 1. Apertura

Antes de ecualizar nada, antes de filtrar nada y antes de pensar en compresión, hay una pregunta más básica: qué está haciendo realmente esta señal en nivel. Y para responderla, no alcanza con mirar una barra que sube y baja. Esa barra puede estar mostrando picos, pero no necesariamente el peso sostenido de la señal. Si no separas esas dos cosas desde el principio, mezclas a ciegas.

Hoy vamos a ordenar eso con tres lecturas: Peak, VU y RMS. No para memorizarlas como teoría de manual, sino para que cuando abras una sesión sepas qué estás mirando y qué no.

### 2. Desarrollo paso a paso

Arranco con la batería. Reproduzco solo el bus de drums y miro el medidor de la DAW. La barra salta fuerte y rápido. Los picos son altos, pero eso por sí solo no me dice cuánta densidad tiene la batería en el tiempo. Lo único que sé es hasta dónde llegó el transitorio más alto. Ese es el territorio del Peak.

Entonces inserto un medidor de pico con retención. Lo que quiero aquí es algo muy concreto: saber si tengo riesgo de clipping y cuál fue el valor máximo alcanzado. Si el bombo pegó en -5 dBFS una vez, eso importa para headroom. Pero no significa que la batería esté densa o comprimida. Solo significa que tuvo un pico alto.

Ahora voy al pad. Reproduzco el pad solo. En el medidor Peak no parece pasar gran cosa. No tiene golpes bruscos. Pero al oído ocupa bastante espacio y sostiene energía todo el tiempo. Ahí el medidor Peak se queda corto para la pregunta que me interesa. Lo que necesito leer ahora es nivel sostenido. Inserto un VU. Y acá la lectura empieza a tener sentido: la aguja se mueve más lento, integra la señal y me deja ver cuánto peso sostiene ese pad en el tiempo.

Ahora paso a la voz. La voz tiene frases, consonantes, aire y una dinámica intermedia entre la batería y el pad. Si quiero comparar su peso general con otro elemento sostenido, el VU me sirve. Si quiero una lectura matemática más estable del promedio energético, uso RMS. Inserto un medidor RMS y empiezo a comparar.

Lo importante acá no es cuál medidor es mejor. Lo importante es qué estoy preguntando. Si quiero saber si un transitorio está rompiendo el headroom, miro Peak. Si quiero saber cuál señal está más sostenida y más cerca de un nivel de trabajo continuo, miro VU o RMS. Si quiero comparar la densidad de dos elementos largos, RMS me da una base más cuantificable. Si quiero una lectura que se parezca a cómo el oído percibe nivel sostenido, VU sigue siendo muy útil.

Entonces hago una prueba directa. Dejo sonando un golpe de batería y luego el pad. El Peak del golpe puede ser más alto que el del pad, pero el VU del pad puede quedar bastante más arriba porque está sosteniendo energía durante más tiempo. Eso es exactamente lo que necesito que el alumno vea: pico alto no equivale a señal densa. Señal densa no equivale a señal con más transitorio.

Cierro esta parte mostrando el error más común: mirar el medidor vertical de la DAW y creer que ya entendiste el nivel. En muchas DAWs ese medidor es Peak. Sirve, sí. Pero solo responde una parte del problema.

### 3. Teoría aplicada en el punto correcto

Peak es lectura instantánea o casi instantánea del máximo valor alcanzado por la señal. Su función principal es proteger la cadena frente al clipping y documentar el techo real al que está llegando el audio.

VU integra aproximadamente 300 ms. No reacciona como el Peak. Justamente por eso sirve para leer nivel sostenido y aproximarse mejor al peso percibido de una señal continua.

RMS calcula la raíz cuadrática media dentro de una ventana temporal. No es un medidor “más musical” que VU ni un reemplazo automático. Es otra forma de leer promedio energético. Su ventaja es que permite comparaciones más controladas, siempre que el tiempo de integración sea consistente.

En una señal muy percusiva, Peak y VU pueden separarse varios decibeles. Esa diferencia no es un problema. Es información.

### 4. Criterio de decisión

Aquí el criterio no es elegir un medidor favorito. El criterio es elegir la lectura que corresponde a la pregunta.

Si la pregunta es “estoy cerca de clipping”, la respuesta viene del Peak.

Si la pregunta es “esta señal está trabajando demasiado alta para un procesador que espera un nivel sostenido razonable”, ahí VU o RMS empiezan a ser más útiles.

Si la pregunta es “cuál de estos dos elementos está ocupando más peso continuo en la mezcla”, Peak no alcanza. Necesitas una lectura integrada.

En otra canción, con material más comprimido o más sostenido, quizá VU y RMS se parezcan más. En una batería muy dinámica, van a separarse mucho. Esa diferencia no invalida ninguno de los dos. Solo te dice qué tipo de señal tienes delante.

### 5. Errores frecuentes y falsas reglas

El primer error es creer que el medidor de la DAW ya responde todo. No. Normalmente te está mostrando picos.

El segundo error es pensar que una señal con picos altos necesariamente suena más fuerte o más llena. No necesariamente. Puede tener mucho transitorio y poca densidad.

El tercer error es usar VU como único medidor en material muy percusivo y luego sorprenderse cuando aparecen clips más adelante en la cadena.

El cuarto error es tratar RMS y VU como si fueran idénticos. Se parecen en la función general de leer nivel sostenido, pero no son la misma lectura ni reaccionan igual.

Y el quinto error es querer mezclar mirando números en vez de entender qué representan esos números.

### 6. Cierre

Con esto ya no estamos mirando barras por costumbre. Estamos leyendo nivel con intención. En la siguiente lección damos un paso más: ya no solo queremos saber qué tan alto llega una señal o cuánto sostiene. Queremos leer densidad global y destino de entrega. Ahí entran K-System y LUFS.

---

# E1-L02 — K-System y LUFS: leer densidad y destino

## Rol de esta lección dentro del proceso completo

Esta lección amplía la lectura de nivel hacia dos problemas que no resuelven ni Peak ni VU por sí solos: la densidad global del material y la referencia de destino. Su papel es enseñarle al alumno a distinguir pico instantáneo de sonoridad integrada, y a entender por qué una mezcla puede tener picos controlados pero seguir estando muy lejos de la referencia real con la que la está comparando.

## Objetivo del video

Que el alumno pueda leer sonoridad integrada con criterio, diferenciar K-System de LUFS y entender qué información le aporta cada uno cuando compara una mezcla con referencias o prepara material para la siguiente fase del flujo.

## Resultado que debería conseguir el alumno al terminar

El alumno debería poder comparar una mezcla con una referencia comercial sin reducir la diferencia a “esta suena más fuerte”. Debería poder cuantificar densidad, entender que LUFS integrado no es lo mismo que Peak y usar esa lectura para ubicar el material dentro de un contexto real de trabajo.

## Situación práctica de partida

Tenemos una mezcla en progreso y una referencia comercial del mismo tipo de producción. Al igualar picos, la referencia sigue sonando más densa, más presente y más estable. El alumno necesita entender qué está midiendo esa diferencia y cómo leerla sin saltar a comprimir por reflejo.

## Estructura del guion

### 1. Apertura

Comparar una mezcla con una referencia solo por pico máximo no sirve. Puedes tener dos temas con el mismo techo de pico y una diferencia brutal en densidad percibida. Si no sabes leer eso, corres el riesgo de empujar la mezcla en la dirección equivocada solo porque la referencia “suena más grande”.

Hoy vamos a ponerle instrumento a esa comparación: K-System y LUFS.

### 2. Desarrollo paso a paso

Cargo la referencia comercial en un canal aparte y dejo sonando un fragmento completo. Primero miro Peak. Bien. Ya sé hasta dónde llega. Pero cuando paso a mi mezcla, aunque los picos estén relativamente cerca, el impacto no es el mismo. Entonces la pregunta cambia: no quiero saber solo el pico. Quiero saber la sonoridad que el material sostiene a lo largo del tiempo.

Inserto un medidor LUFS en la referencia y reproduzco un tramo suficiente para obtener lectura integrada. No me interesa la lectura momentánea al principio, porque oscila demasiado con cada evento. Quiero la integrada, la que resume el programa completo o al menos una sección representativa.

Ahora hago lo mismo con mi mezcla. Supongamos que mi mezcla está varios LU por debajo de la referencia. Ahí ya no estoy adivinando. Ya no digo “creo que le falta fuerza”. Ahora puedo decir: la diferencia de densidad integrada es real y está cuantificada.

Después introduzco el K-System no como reemplazo del LUFS, sino como otra manera de ordenar la lectura dentro de un contexto de rango dinámico. Muestro que K-20, K-14 y K-12 no son tres adornos raros. Son tres escalas pensadas para distintos escenarios de rango dinámico.

Si estoy trabajando material con más rango, un entorno tipo K-20 tiene sentido porque deja más margen. Si estoy en producción más densa y más cercana a consumo popular, K-14 puede ser una referencia más práctica de trabajo. Si estoy en material orientado a broadcast o muy comprimido, K-12 está más cerca de ese comportamiento.

Lo importante es que el alumno vea algo clave: K-System organiza una relación entre referencia de escucha y rango dinámico esperado. LUFS, en cambio, es la lectura estándar de sonoridad integrada que luego va a dialogar directamente con destinos de distribución y normalización.

Hago una comparación final entre tres cosas: pico máximo, sonoridad integrada y percepción. Una mezcla puede no clippear y aun así estar muy por debajo de la referencia en LUFS. O puede estar muy densa en LUFS y aun así conservar picos moderados. Por eso no se reemplazan entre sí.

### 3. Teoría aplicada en el punto correcto

LUFS mide sonoridad ponderada en el tiempo con un estándar diseñado para aproximarse mejor a la percepción auditiva que un simple medidor de pico. Tiene lecturas momentary, short-term e integrated. Para decisiones de comparación global y destino, la más importante es integrated.

True Peak no es lo mismo que LUFS. True Peak controla los picos de reconstrucción entre muestras. LUFS mide densidad o sonoridad integrada. Uno no reemplaza al otro.

K-System es un sistema de referencia propuesto por Bob Katz que ordena el trabajo según el rango dinámico esperado. K-20, K-14 y K-12 no significan “mejor o peor”. Significan contextos distintos de operación.

### 4. Criterio de decisión

Si tu pregunta es “qué tan denso está este material respecto a otro”, LUFS integrado es la lectura más directa.

Si tu pregunta es “en qué contexto de rango dinámico quiero organizar mi escucha y mi referencia de trabajo”, K-System ofrece una estructura útil.

Si estás comparando una mezcla con una referencia y descubres una diferencia de 5 o 6 LU, no significa automáticamente que debas comprimir más en ese momento. Primero tienes que decidir en qué etapa del flujo corresponde resolver esa diferencia y si realmente esa referencia es comparable por arreglo, género y objetivo.

En otro contexto, como premezcla o trabajo todavía muy temprano, quizá ni siquiera convenga perseguir una cercanía en LUFS. Pero sí conviene leerla para entender dónde estás parado.

### 5. Errores frecuentes y falsas reglas

El primer error es usar LUFS momentary como si fuera lectura global. No lo es. Sirve para comportamiento instantáneo, no para resumen del programa.

El segundo error es perseguir un número de LUFS demasiado pronto y empezar a deformar la mezcla antes de que el balance esté resuelto.

El tercer error es creer que si dos temas tienen el mismo pico máximo deberían sentirse igual de fuertes. No tiene sentido.

El cuarto error es tratar K-System como si fuera una norma universal obligatoria. No. Es una metodología de referencia útil, no una religión.

Y el quinto error es comparar tu mezcla contra cualquier track comercial sin preguntarte si de verdad juega en la misma cancha estética y dinámica.

### 6. Cierre

Ya tenemos una lectura más seria de nivel y densidad. Pero todavía seguimos en el dominio del nivel. La siguiente lección cambia de eje interno: dejamos de preguntar cuánto nivel hay y empezamos a preguntar cómo se relacionan las señales entre sí. Entramos en polaridad.

---

# E1-L03 — Polaridad: cómo detectar el problema antes de tocar nada

## Rol de esta lección dentro del proceso completo

Esta lección inaugura el bloque relacional del Eje 1. Su papel es enseñarle al alumno a identificar un problema que muchas veces se corrige por reflejo, sin diagnóstico, o peor, se nombra mal. Aquí se separa inversión de polaridad de otros fenómenos y se establece una metodología de lectura antes de tocar el botón ∅.

## Objetivo del video

Que el alumno pueda detectar inversión de polaridad por escucha y por lectura comparativa, entendiendo cuándo tiene sentido revisar polaridad y cuándo el problema real está en otro lado.

## Resultado que debería conseguir el alumno al terminar

El alumno debería poder revisar dos señales relacionadas, escuchar su suma, observar su comportamiento y decidir con criterio si hay inversión de polaridad. Debería también dejar de usar “fase” como palabra comodín para todo.

## Situación práctica de partida

Tenemos dos micrófonos capturando la misma fuente, por ejemplo dos tomas relacionadas de una caja o un top y un bottom. Al sumarlos, el cuerpo desaparece o se adelgaza de forma anormal. El alumno necesita saber si está frente a una inversión de polaridad o frente a otro problema relacional.

## Estructura del guion

### 1. Apertura

Hay decisiones que parecen pequeñas pero cambian por completo lo que viene después. Una de ellas es esta: sumar dos señales y no saber si se están ayudando o se están destruyendo. Mucha gente lo llama “problema de fase” sin mirar nada más. Pero antes de hablar de fase, primero hay que revisar algo más básico: polaridad.

### 2. Desarrollo paso a paso

Pongo en solo dos señales relacionadas de la misma fuente. Primero las escucho juntas. No toco nada todavía. Solo escucho si al sumarse aparece una pérdida extraña de cuerpo, de low end o de pegada.

Después muteo una y luego la otra. Quiero construir una referencia mental clara de cómo suena cada una por separado y cómo suenan en conjunto. Si la suma suena claramente más débil que una de las señales sola en una zona donde debería reforzarse, ya tengo un indicio.

Ahora sí activo la inversión de polaridad en una de las dos. No porque “siempre haya que probar”. Lo hago porque ya escuché un síntoma compatible con problema de polaridad. Comparo A/B rápidamente.

Si al invertir polaridad la suma recupera cuerpo, estabilidad y centro, ese es un indicio fuerte de que una de las señales estaba invertida respecto a la otra. Si no cambia casi nada, o mejora una zona pero empeora otra de forma rara, entonces probablemente no era un problema binario de polaridad y hay que seguir leyendo.

Acá hago algo importante para el alumno: explico que la inversión de polaridad no es una corrección estética. No es “a ver cuál me gusta más”. Es una verificación técnica de coherencia entre señales relacionadas.

Luego enseño una rutina corta: escuchar cada señal sola, escuchar la suma, invertir polaridad en una sola, volver a escuchar la suma, decidir según el resultado total y no según una banda aislada.

También muestro un caso donde invertir polaridad no arregla nada. Eso es clave. Porque si solo enseñas el caso donde sí funciona, el alumno termina creyendo que siempre hay una respuesta binaria y rápida.

### 3. Teoría aplicada en el punto correcto

Invertir polaridad significa invertir el signo de toda la señal: lo positivo pasa a negativo y lo negativo a positivo. Es una operación binaria. No desplaza unas frecuencias más que otras. No introduce un retardo. No es lo mismo que un desfasaje temporal.

Por eso el botón ∅ normalmente no es un “botón de fase”. Es un inversor de polaridad. El problema aparece cuando esa señal se suma con otra relacionada. Escuchada sola, la inversión de polaridad puede no cambiar casi nada perceptible.

### 4. Criterio de decisión

Revisas polaridad cuando tienes señales que representan la misma fuente o una fuente estrechamente relacionada y la suma se comporta peor de lo esperable.

No revisas polaridad por costumbre en cualquier canal aislado.

Si al invertir polaridad la suma mejora de forma global, consistente y clara, la corrección tiene sentido.

Si mejora una cosa y destruye otra, o si casi no cambia, probablemente el problema no sea polaridad sino relación temporal o comportamiento frecuencial más complejo.

En otra sesión, con otro par de micrófonos o con otra geometría de grabación, puede que ambas polaridades produzcan compromisos distintos. Ahí no estás ante un “sí o no” limpio, sino ante un problema de alineación o fase que se trabajará después.

### 5. Errores frecuentes y falsas reglas

El primer error es llamar “fase” a cualquier cosa que pasa cuando dos señales no suman bien.

El segundo error es apretar ∅ al azar hasta que algo “guste más”. No se trata de gusto instantáneo, sino de coherencia técnica de la suma.

El tercer error es revisar polaridad en un canal solo como si ahí fuera a revelarse algo concluyente.

El cuarto error es pensar que si invertir polaridad no arregla el problema, entonces no hay ningún problema. Puede haber desfasaje temporal.

Y el quinto error es corregir polaridad sin escuchar la suma completa en contexto relacional.

### 6. Cierre

Con polaridad ya tenemos resuelto el problema binario más básico de relación entre señales. Pero no todo lo que suena hueco o flaco es polaridad. En la siguiente lección entramos en el terreno más fino: fase, desfasaje y comb filtering.

---

# E1-L04 — Fase y comb filtering: leer relaciones, no adivinar

## Rol de esta lección dentro del proceso completo

Esta lección lleva al alumno del problema binario de polaridad al territorio continuo y más complejo de la relación temporal y frecuencial entre señales. Su función es diagnosticar, no corregir. Deja preparado el terreno para que el Eje 2 intervenga con alineación temporal u otras acciones.

## Objetivo del video

Que el alumno aprenda a diferenciar inversión de polaridad, desfasaje y comb filtering, y que pueda reconocer por escucha y lectura cuándo una suma está generando cancelaciones parciales.

## Resultado que debería conseguir el alumno al terminar

El alumno debería poder escuchar dos señales relacionadas y detectar si el problema es una cancelación binaria simple o un patrón de filtrado en peine producto de diferencias temporales. También debería poder identificar que una suma problemática no siempre se corrige con el botón ∅.

## Situación práctica de partida

Tenemos dos micrófonos de una misma fuente o dos versiones de una misma señal con un pequeño retardo relativo. Al sumarlas, algunas zonas del espectro se refuerzan y otras se cancelan. El resultado no es una desaparición total, sino una coloración rara, hueca o filtrada.

## Estructura del guion

### 1. Apertura

Si en la lección anterior el problema era binario —normal o invertido— aquí entramos en un problema gradual. Las señales ya no están simplemente de un lado o del otro. Ahora están llegando en momentos diferentes. Y cuando eso pasa, la suma deja una firma muy particular: el comb filtering.

### 2. Desarrollo paso a paso

Cargo dos señales relacionadas. Primero hago la escucha simple: en solo conjunto. Quiero que el alumno oiga ese timbre raro, como hueco o peinado, que aparece cuando una señal se suma con una versión ligeramente desplazada de sí misma.

Ahora repito el gesto de la lección anterior: invierto polaridad. ¿Se arregla del todo? No. Quizá cambia el patrón, quizá mueve el problema, quizá hasta empeora otra zona. Ese momento es clave porque separa el diagnóstico anterior de este nuevo fenómeno.

Entonces muestro el analizador espectral. No para convertir la clase en una clase de física abstracta, sino para que el alumno vea la firma del problema: una serie de valles periódicos en el espectro. No un solo hueco. Una repetición de cancelaciones parciales. Esa repetición es la pista del comb filtering.

Después explico el gesto operativo mínimo: si dos señales similares llegan separadas en el tiempo por una diferencia pequeña, algunas frecuencias se suman y otras se cancelan según su longitud de onda relativa a ese desfase. No hace falta corregir todavía. Solo hace falta reconocerlo.

Hago una prueba adicional con retardo artificial muy corto sobre una copia de la señal original. Voy desplazando unos samples y el alumno escucha cómo aparece el peine. Así entiende que no estamos hablando de una idea abstracta: estamos hablando de tiempo relativo entre señales.

Luego conecto con un caso real: overheads, micrófonos cercanos, duplicados mal alineados, capas que parecen iguales pero no llegan juntas. En todos esos casos, el oído puede confundir el problema con falta de cuerpo, falta de foco o incluso “mala EQ”. Y no es EQ. Es relación temporal.

### 3. Teoría aplicada en el punto correcto

La fase describe una relación entre señales o entre componentes frecuenciales. Cuando dos señales similares llegan en tiempos distintos, la diferencia de tiempo equivale a diferencias de fase distintas según la frecuencia. Por eso no se cancela todo por igual. Se cancelan unas bandas y otras no.

Ese patrón periódico de refuerzos y cancelaciones parciales se llama comb filtering porque el espectro se ve como un peine.

La polaridad invertida es un caso binario y uniforme. El desfasaje no. El desfasaje depende de frecuencia y tiempo relativo.

### 4. Criterio de decisión

Si la suma empeora de forma global y una inversión de polaridad la arregla claramente, estabas más cerca de un problema de polaridad.

Si la suma suena filtrada, rara, con huecos repetidos, y la inversión de polaridad no resuelve el problema de forma limpia, probablemente estás frente a un desfase temporal y comb filtering.

Si el analizador muestra valles periódicos y la escucha confirma esa coloración, ya tienes un diagnóstico operativo suficiente para pasar al Eje 2.

En otra fuente menos correlacionada, quizá el problema no se manifieste de forma tan evidente. Y en señales muy diferentes entre sí, no tiene sentido esperar el mismo patrón. Este diagnóstico vale sobre todo para señales relacionadas.

### 5. Errores frecuentes y falsas reglas

El primer error es seguir llamando “problema de fase” a todo sin separar qué tipo de relación está fallando.

El segundo error es intentar arreglar comb filtering con EQ. Puedes disimular algo, pero no corregiste la causa.

El tercer error es pensar que si dos señales no cancelan por completo entonces no hay un problema relacional serio.

El cuarto error es duplicar una señal, retrasarla unos samples para “abrirla” y no revisar lo que eso hace al colapsar a mono.

Y el quinto error es querer corregir ya mismo antes de haber descrito bien el síntoma.

### 6. Cierre

Hasta aquí ya sabemos leer nivel y relaciones entre señales. Nos falta una tercera lectura: cómo está distribuida la energía por frecuencia. En la siguiente lección entramos al analizador espectral, pero no como adorno visual. Vamos a configurarlo para que realmente sirva.

---

# E1-L05 — Analizador espectral: cómo configurarlo para que sí sirva

## Rol de esta lección dentro del proceso completo

Esta lección abre el bloque espectral del Eje 1. Su función es convertir el analizador en un instrumento de diagnóstico real, no en una pantalla bonita que confirma prejuicios. Aquí el alumno aprende a configurar escala, resolución y comportamiento temporal del analizador según la pregunta que está intentando responder.

## Objetivo del video

Que el alumno aprenda a configurar un analizador espectral con criterio, entendiendo qué cambia al modificar escala, FFT, ventana y promediado, y para qué tipo de diagnóstico sirve cada ajuste.

## Resultado que debería conseguir el alumno al terminar

El alumno debería poder montar un analizador útil para detectar subsónicas, resonancias, balance tonal global o firmas de comb filtering, sin sacar conclusiones torcidas por una mala configuración del instrumento.

## Situación práctica de partida

Estamos en plena sesión y el alumno abre un analizador. Ve una montaña de información moviéndose todo el tiempo, pero no sabe si está leyendo graves reales, resonancias puntuales, ruido o simple comportamiento normal de la señal. El problema no es que falte el analizador. El problema es que no está configurado para la pregunta correcta.

## Estructura del guion

### 1. Apertura

Abrir un analizador no equivale a entender el espectro. Si la configuración no corresponde a la pregunta que estás haciendo, el instrumento no te aclara nada. Solo te distrae con movimiento.

Hoy no vamos a usar el analizador para “ver la música”. Vamos a configurarlo para diagnosticar problemas concretos.

### 2. Desarrollo paso a paso

Empiezo con una mezcla completa. Inserto un analizador básico y dejo la configuración por defecto. Luego pregunto: qué estoy viendo exactamente. La respuesta honesta es: todavía no mucho. Hay demasiada información y no está enfocada.

Entonces voy parámetro por parámetro.

Primero la escala de frecuencia. Muestro por qué una escala logarítmica suele ser más útil para música que una lineal: organiza mejor la percepción del rango audible y deja ver con más sentido las relaciones entre graves, medios y agudos. Si busco lectura musical global, la logarítmica ayuda más.

Después ajusto la resolución FFT. Si la dejo muy baja, el analizador responde rápido pero con poco detalle fino. Si la subo mucho, puedo ver resonancias más precisas, pero pierdo inmediatez temporal y la lectura se vuelve más pesada. Entonces enseño el criterio: para balance global, no necesito una FFT exageradamente alta. Para cazar una resonancia estrecha o ver con más detalle un patrón de peine, sí conviene mayor resolución.

Luego voy a la ventana y al promediado. Si no hay promediado, la pantalla puede moverse tanto que el alumno termina leyendo accidentes y no tendencias. Agrego un promedio razonable y la imagen empieza a estabilizarse. Ahora sí se puede evaluar mejor el balance general.

Hago una demostración concreta de cuatro preguntas distintas.

Primera: hay energía subsónica. Bajo el zoom y configuro una lectura que me permita ver claramente si debajo del fundamento del material hay contenido inútil.

Segunda: sospecho una resonancia. Subo resolución FFT y reduzco la dependencia del promedio para ver mejor picos estrechos.

Tercera: quiero comparar balance tonal global con una referencia. Uso escala logarítmica y promediado suficiente para leer tendencia, no microaccidentes.

Cuarta: sospecho comb filtering. Busco una resolución que deje visibles valles repetidos.

Lo importante es que el alumno vea que el analizador no tiene una sola configuración “correcta”. Tiene configuraciones útiles según el diagnóstico.

### 3. Teoría aplicada en el punto correcto

La FFT determina cómo se descompone la señal en componentes frecuenciales para ser visualizada. Más resolución permite distinguir detalles más finos en frecuencia, pero compromete respuesta temporal.

La ventana influye en cómo se comporta el análisis en el tiempo y en la precisión de la representación. El promediado suaviza el comportamiento para que puedas leer tendencia y no solo fluctuación instantánea.

La escala logarítmica organiza la frecuencia de un modo más cercano a cómo entendemos el rango musical. La lineal puede tener sentido en otros análisis, pero para mezcla suele ser menos práctica como vista general.

### 4. Criterio de decisión

Si buscas balance tonal global, prioriza una lectura estable y legible.

Si buscas una resonancia puntual, prioriza resolución.

Si buscas actividad en subgraves o exceso de energía inútil, enfoca el rango bajo y evita sacar conclusiones con una escala que lo esconda.

Si comparas con una referencia, no copies la curva visual como receta. Usa la referencia para detectar desbalances grandes, no para forzar una coincidencia milimétrica.

En otra mezcla, con otro arreglo o con otra estética, la curva general puede cambiar mucho y seguir siendo correcta. El analizador ayuda a leer. No decide por ti.

### 5. Errores frecuentes y falsas reglas

El primer error es usar siempre la configuración por defecto.

El segundo error es creer que más resolución FFT siempre es mejor. No necesariamente. A veces solo vuelves la lectura más torpe.

El tercer error es usar el analizador como juez final de EQ o balance.

El cuarto error es querer que la mezcla copie exactamente la silueta de una referencia comercial.

Y el quinto error es olvidar que el analizador complementa la escucha; no la reemplaza.

### 6. Cierre

Ya sabemos leer nivel, relaciones y espectro. Nos queda cerrar el eje con una lectura que conecta directamente con el espacio estéreo: goniómetro y correlatómetro. Ahí vamos a ver apertura, correlación y riesgo de mono antes de que el Eje 5 empiece a construir imagen.

---

# E1-L06 — Imagen estéreo: goniómetro y correlatómetro

## Rol de esta lección dentro del proceso completo

Esta lección cierra el Eje 1 integrando la lectura espacial de la mezcla. Su función es enseñarle al alumno a leer apertura, distribución entre canales y riesgo de monocompatibilidad sin modificar todavía la imagen. También deja tendido el puente natural hacia el Eje 5, donde esa imagen ya no solo se leerá: se construirá.

## Objetivo del video

Que el alumno pueda usar goniómetro y correlatómetro para diagnosticar la imagen estéreo de una señal o mezcla, distinguir apertura útil de incoherencia problemática y detectar riesgo de colapso al pasar a mono.

## Resultado que debería conseguir el alumno al terminar

El alumno debería poder mirar y escuchar una mezcla, interpretar si la imagen está centrada, abierta, demasiado lateral o en riesgo de cancelación, y registrar ese diagnóstico antes de pasar a la fase de corrección o construcción espacial.

## Situación práctica de partida

Tenemos una mezcla que en estéreo parece amplia y atractiva, pero al colapsarla a mono algunos elementos caen de nivel o cambian demasiado. El alumno necesita una forma de leer esa situación antes de decidir si el problema es tolerable, creativo o técnicamente peligroso.

## Estructura del guion

### 1. Apertura

Una mezcla puede parecer grande en estéreo y aun así estar mal construida en términos de coherencia entre canales. Si no lees eso antes, puedes enamorarte de una apertura que luego se desarma en mono.

Hoy cerramos el Eje 1 con dos herramientas que no corrigen nada, pero te dicen muchísimo sobre la imagen: goniómetro y correlatómetro.

### 2. Desarrollo paso a paso

Empiezo con una mezcla relativamente centrada. Inserto un goniómetro. Lo primero que quiero que el alumno entienda es que no se trata de “dibujitos bonitos”. La forma refleja cómo se distribuye la energía entre los dos canales.

Si la imagen aparece como una figura principalmente vertical y concentrada, hay bastante contenido correlacionado y centrado. Si se abre en diagonal o en horizontal, la mezcla se está yendo más a los lados o a relaciones menos correlacionadas.

Después abro más una pareja de elementos o activo un efecto estéreo evidente. El goniómetro se ensancha. Bien. Pero esa apertura visual no me dice todavía si es segura. Entonces miro el correlatómetro.

En el correlatómetro, valores cercanos a +1 indican alta correlación entre canales. Al acercarse a 0 hay menos coherencia entre ellos. Si se va hacia negativo, aparece riesgo fuerte de cancelación al colapsar a mono.

Hago la prueba completa: escucho en estéreo, miro ambas herramientas y luego colapso a mono. El alumno ve y escucha qué pasa cuando una imagen que parecía impresionante en estéreo pierde demasiada información al sumarse.

También muestro un caso importante: una mezcla no necesita vivir pegada a +1 todo el tiempo para estar bien. Una apertura saludable puede hacer que la correlación baje sin entrar en zona problemática. El objetivo no es mezclar “todo súper correlacionado”. El objetivo es entender el costo de cada decisión espacial.

Conecto esto con el resto del curso: en Eje 1 solo diagnosticamos. Si una imagen está demasiado riesgosa, lo registramos. La corrección técnica de ciertas relaciones puede pasar por Eje 2. La construcción deliberada de la imagen, ya con intención artística y espacial, llegará en Eje 5.

### 3. Teoría aplicada en el punto correcto

El goniómetro representa visualmente la relación instantánea entre canal izquierdo y derecho. Una traza más vertical sugiere mayor componente común entre ambos canales. Una traza más ancha u horizontal sugiere más diferencia lateral.

El correlatómetro resume la coherencia entre canales en un valor. Cerca de +1 hay alta correlación. Cerca de 0 hay poca correlación. En negativo, el riesgo de cancelación al sumar a mono aumenta mucho.

Ninguna de las dos herramientas decide por sí sola si algo está bien o mal. Son instrumentos de lectura que siempre deben cruzarse con escucha.

### 4. Criterio de decisión

Si la mezcla pierde demasiado al colapsar a mono y el correlatómetro cae con frecuencia a zona negativa, tienes un síntoma serio de incompatibilidad.

Si la mezcla está abierta, el goniómetro lo confirma y el correlatómetro baja moderadamente sin comprometer la suma en mono, probablemente esa apertura sea funcional.

Si una fuente crítica del centro —voz principal, bombo, bajo— cambia demasiado en mono, el problema ya no es solo “la mezcla está abierta”. Hay una decisión espacial o relacional que requiere revisión.

En otros contextos, algunos efectos laterales o decorativos pueden tolerar más costo en mono porque no sostienen el núcleo de la canción. El criterio depende del rol del elemento.

### 5. Errores frecuentes y falsas reglas

El primer error es creer que una mezcla buena debe quedarse siempre cerca de +1. Eso mataría mucha apertura útil.

El segundo error es creer que una imagen ancha siempre es mejor.

El tercero es mirar el goniómetro como si fuera un adorno y no una lectura relacional.

El cuarto es aprobar una imagen estéreo sin colapsar a mono al menos como verificación.

Y el quinto es tratar cualquier caída en correlación como si fuera automáticamente un desastre técnico.

### 6. Cierre

Con esto el Eje 1 queda completo. Ya sabes leer nivel, densidad, relaciones entre señales, espectro e imagen estéreo. Y eso deja una consecuencia clara: ahora sí puedes entrar al Eje 2 con diagnósticos concretos en la mano. Lo que sigue ya no es adivinar. Es corregir lo que esta lectura acaba de revelar.