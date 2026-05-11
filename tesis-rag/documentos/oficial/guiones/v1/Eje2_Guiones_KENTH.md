# E2-L01 — HPF y LPF: cuándo filtrar de verdad

## Rol de esta lección dentro del proceso completo
Esta lección abre el Eje 2. El alumno ya aprendió a leer nivel, fase y espectro en el Eje 1. Ahora empieza a operar. El primer paso no es dar color ni corregir tono: es retirar energía que no debería seguir avanzando por la cadena. Si este paso se hace mal, el resto del procesamiento trabaja sobre basura, ruido o contenido mal priorizado.

## Objetivo del video
Enseñar a filtrar con criterio real, separando limpieza legítima de cortes arbitrarios.

## Resultado que debería conseguir el alumno al terminar
El alumno debe poder decidir si una señal necesita HPF o LPF, justificar por qué, elegir un punto de corte inicial razonable, ajustar la pendiente según el caso y verificar que el filtro limpia sin destruir contenido útil.

## Situación práctica de partida
Estamos en una sesión de mezcla y abrimos una guitarra acústica. En el analizador aparece energía por debajo de la zona útil del instrumento. Además, en la mezcla completa esa guitarra se pelea con el bajo y con parte del cuerpo del piano. El alumno ve el filtro, sabe que “normalmente se corta”, pero todavía no sabe qué está resolviendo ni bajo qué criterio.

## Estructura del guion

### 1. Apertura
En esta etapa no estamos ecualizando para embellecer nada. Estamos tomando una decisión mucho más básica: qué parte de esta señal merece seguir viva dentro de la mezcla y qué parte no. Si cortas por costumbre, te cargas información útil. Si no cortas nunca, arrastras energía que ensucia todo lo que viene después.

### 2. Desarrollo paso a paso
Primero pongo la guitarra en solo y abro el analizador. No para decidir por los ojos, sino para ubicar dónde está pasando algo sospechoso. Veo contenido en graves muy por debajo de la zona donde este instrumento debería tener información estable. Entonces hago la primera pregunta: ¿eso que veo pertenece al instrumento o pertenece al entorno de grabación, al ruido mecánico o a la suma con otras cosas?

Activo un HPF y no lo muevo de golpe hasta un número mágico. Lo subo desde abajo, lento, mientras escucho qué desaparece. Si lo que se va es solo ruido, vibración o densidad que no aporta identidad, voy bien. Si empieza a irse cuerpo real del instrumento, me pasé.

Hasta aquí sigo trabajando en solo porque estoy resolviendo dos cosas que sí pueden evaluarse aisladas: energía que no debería estar y energía que está por debajo del registro real del instrumento.

Ahora saco el solo y escucho la mezcla completa. Aquí entra otra pregunta distinta: aunque esa zona sí pertenezca al instrumento, ¿conviene que la conserve completa o conviene que ceda parte de ese territorio a otro elemento más importante en ese rango? Eso ya no se decide en solo. Se decide con la mezcla corriendo.

Si la guitarra comparte zona con el bajo, puede tener sentido subir un poco más el HPF aunque en solo suene apenas más delgada. No porque ese punto sea universal, sino porque en esta mezcla concreta ese espacio lo necesita más el bajo.

Con el LPF hago lo mismo pero del otro lado. Solo lo uso si arriba hay ruido, aspereza sobrante o si necesito retroceder un poco el instrumento en el plano sin entrar todavía en ecualización de carácter. Si el brillo superior es parte de la identidad del instrumento, no lo corto por limpieza automática.

Después pruebo pendientes. Una pendiente suave limpia de forma más gradual y suele sentirse menos agresiva. Una pendiente más pronunciada resuelve más rápido, pero también modifica más la relación de fase alrededor del corte. No asumo que 24 dB por octava es “mejor”; pruebo qué tanto necesito recortar y cuánto me conviene preservar alrededor de la zona útil.

La verificación final la hago en dos pasos. Primero vuelvo a escuchar el canal por sí solo para asegurarme de que no se quedó hueco. Luego escucho otra vez la mezcla completa para confirmar que el instrumento ahora ocupa mejor su lugar y no está empujando una región que no le corresponde.

### 3. Teoría aplicada en el punto correcto
Un filtro no es un ecualizador de color. Su función aquí es delimitar. La frecuencia de corte no marca el punto donde “empieza el corte” de forma abrupta; es el punto de referencia de la curva y la atenuación comienza antes o después según la pendiente. Por eso dos filtros con la misma frecuencia nominal pueden comportarse distinto.

En este eje trabajamos con tres criterios diferentes:

Primer criterio: protección. Quitar energía que no aporta contenido útil y sí carga la cadena.

Segundo criterio: registro. Eliminar contenido por debajo o por encima de la zona donde ese instrumento realmente vive.

Tercer criterio: espacio. Ceder territorio a otro elemento más importante en esa franja. Este tercero solo se evalúa en contexto.

Ese detalle importa porque muchos errores nacen de mezclar los tres criterios como si fueran uno solo.

### 4. Criterio de decisión
Aquí sí filtré porque había evidencia de sobra: contenido debajo del registro útil, acumulación que no aportaba identidad y conflicto real con un elemento más importante en esa zona. En otra canción podría no mover nada si esa guitarra fuera la base armónica principal y necesitara más cuerpo. O podría usar una pendiente más suave si la señal tuviera menos problema de acumulación y más necesidad de conservar naturalidad.

La decisión no la manda el instrumento por nombre. La manda la combinación entre lo que el instrumento es, lo que la grabación trajo y el lugar que debe ocupar en esta mezcla.

### 5. Errores frecuentes y falsas reglas
“Todas las pistas llevan HPF”. No. Algunas sí, otras no, y otras lo necesitan en otro punto muy distinto.

“Filtrar siempre mejora claridad”. No. A veces solo adelgaza la mezcla y te obliga a compensar después con otras herramientas.

“El punto de corte se decide en solo”. Solo parcialmente. El criterio de espacio no existe en solo.

“LPF sirve solo para quitar hiss”. No. También puede modificar perspectiva, pero si lo usas sin criterio, apagas identidad.

“Pendiente más fuerte es más profesional”. No. Es más agresiva. Eso no significa mejor.

### 6. Cierre
Con esto ya no estamos adivinando cortes: estamos separando limpieza real de recorte arbitrario. En la siguiente lección toca otra frontera importante: cuando el problema no se resuelve con un HPF o un LPF general, sino con herramientas más específicas como Notch, AllPass y fase lineal.

---

# E2-L02 — Notch, AllPass y fase lineal: cada problema con su herramienta

## Rol de esta lección dentro del proceso completo
Después de decidir cuándo un filtrado amplio tiene sentido, esta lección enseña a no sobrerreaccionar. No todos los problemas requieren cortar bandas enteras. Algunos exigen precisión quirúrgica. Otros ni siquiera son problemas de amplitud, sino de fase. Esta lección evita que el alumno use la herramienta equivocada para el diagnóstico correcto.

## Objetivo del video
Enseñar a distinguir cuándo conviene un Notch, cuándo un AllPass y cuándo un filtro de fase lineal aporta más de lo que complica.

## Resultado que debería conseguir el alumno al terminar
El alumno debe poder identificar si está frente a una resonancia puntual, a una relación de fase problemática entre señales o a una situación donde la fase lineal vale la pena, y elegir la herramienta adecuada sin convertirla en receta universal.

## Situación práctica de partida
Tenemos tres problemas distintos en la sesión. Uno: una guitarra eléctrica con una resonancia específica que salta en ciertas notas. Dos: dos micrófonos sobre una misma fuente que no terminan de sumar bien aunque ya están cerca en tiempo. Tres: una rama de procesamiento donde conservar la relación de fase es especialmente importante.

## Estructura del guion

### 1. Apertura
Uno de los errores más caros en mezcla es diagnosticar bien y operar mal. Oyes una resonancia y metes un HPF. Oyes una mala suma entre dos micros y haces un corte espectral. Oyes que algo cambia al sumar ramas y no sabes si el problema es amplitud o fase. Esta lección es para que cada problema vaya con su herramienta.

### 2. Desarrollo paso a paso
Empiezo con la resonancia. Pongo la guitarra en contexto y luego en solo para confirmar que ese punto está realmente sobresaliendo. No es una zona amplia del tono: es una frecuencia o una banda muy estrecha que se dispara más que el resto. Ahí no necesito redibujar el instrumento entero. Necesito recortar justo donde molesta. Por eso uso un Notch.

Lo coloco en la frecuencia problemática y no asumo que por ser quirúrgico debo usar el Q más extremo posible. Al contrario: subo el Q hasta localizar el problema, pero después lo reduzco al mínimo necesario para que la resonancia deje de mandar sin que el instrumento suene artificial.

Cambio de caso. Ahora tengo dos señales que por separado parecen correctas, pero al sumarlas aparece pérdida de cuerpo o una sensación rara en ciertas zonas. Si la amplitud está bien y el problema es la relación de fase entre ambas, un corte espectral no corrige la raíz. Aquí pruebo un AllPass.

Lo importante es entender que el AllPass no cambia el balance tonal por sí solo. En solo casi no me dice nada. Su efecto se revela en suma. Por eso lo ajusto escuchando ambas señales juntas. Muevo la frecuencia del AllPass y escucho en qué punto la suma recupera consistencia.

Tercer caso. Estoy en una situación donde alterar la fase relativa de ciertas regiones me puede costar más que la latencia del proceso. Entonces pruebo un filtro de fase lineal. Pero no lo activo por prestigio técnico. Lo activo si de verdad necesito preservar relación de fase y el material tolera su costo.

Si la fuente es muy percusiva, escucho con mucha atención si aparece pre-ringing. Si aparece, esa supuesta mejora técnica en realidad empeoró la percepción del ataque. En ese caso vuelvo a filtro estándar.

### 3. Teoría aplicada en el punto correcto
El Notch es una herramienta de banda muy estrecha. Sirve cuando el problema está localizado y no quiero alterar demasiado alrededor. El peligro es excederse con el Q y generar artefactos peores que la resonancia original.

El AllPass no atenúa ni realza amplitud. Modifica fase. Por eso es inútil como herramienta de tono y útil cuando la suma entre señales es el problema.

Los filtros de fase lineal evitan rotación de fase dependiente de frecuencia, pero a cambio introducen latencia y pre-ringing. No son “mejores”. Son un compromiso distinto.

### 4. Criterio de decisión
Usé Notch cuando el problema estaba en una zona puntual. Usé AllPass cuando el problema vivía en la relación entre señales. Consideré fase lineal solo cuando preservar fase pesaba más que el costo temporal del proceso.

En otra mezcla, una resonancia intermitente quizá no se resolvería mejor con Notch estático sino con EQ dinámico en Eje 3. Y una mala suma entre señales quizá se resolvería antes por alineación temporal que por AllPass. La herramienta correcta depende del tipo de problema, no de la fama del plugin.

### 5. Errores frecuentes y falsas reglas
“Si molesta una frecuencia, siempre se hace Notch”. No. Solo si el problema es realmente estrecho y localizado.

“AllPass arregla fase en cualquier caso”. No. Si el problema principal es tiempo, primero se revisa alineación temporal.

“Fase lineal es la opción pro”. No. A veces es la opción menos musical.

“En solo ya se oye si el AllPass funcionó”. No. Su sentido aparece en suma.

### 6. Cierre
Ya vimos que no todo se resuelve con filtros amplios. Pero incluso cuando eliges bien el tipo de filtro, todavía queda una variable crítica: dónde cae dentro de la cadena. Eso define qué procesadores trabajan sobre qué contenido. Esa es la siguiente lección.

---

# E2-L03 — El filtro dentro de la cadena: por qué el orden sí importa

## Rol de esta lección dentro del proceso completo
Esta lección une dos cosas que muchos alumnos aprenden separadas: filtrado y dinámica. No basta con saber filtrar; hay que entender qué pasa si el compresor o cualquier detector recibe contenido que luego será eliminado. Esta clase organiza la lógica interna del eje antes de pasar a polaridad y alineación.

## Objetivo del video
Explicar por qué el orden del filtro dentro de la cadena cambia el comportamiento del resto de procesadores, y cuándo conviene ubicarlo antes de la dinámica.

## Resultado que debería conseguir el alumno al terminar
El alumno debe poder justificar por qué un HPF de limpieza suele ir antes del compresor y entender cómo el orden afecta la respuesta dinámica y la relación de fase en sumas múltiples.

## Situación práctica de partida
Tenemos un bombo con energía muy baja que no aporta musicalmente, pero sí mueve mucho al compresor. El alumno comprime primero y filtra después. El resultado suena raro: el compresor trabaja de más, aunque luego esa energía desaparezca.

## Estructura del guion

### 1. Apertura
Un orden de inserts no es decoración. Cambia qué señal ve cada procesador. Si primero comprimes basura y luego la quitas, la compresión ya pasó. El daño o el movimiento ya quedó impreso.

### 2. Desarrollo paso a paso
Cargo el track del bombo y dejo el compresor antes del HPF. Reproduzco y miro la reducción de ganancia. El compresor se mueve más de lo que debería. Escucho el resultado y noto que el groove respira por una zona que casi ni se oye como contenido musical.

Ahora invierto el orden: pongo primero el HPF y después el compresor. Reproduzco exactamente el mismo pasaje. El compresor ahora recibe una versión más limpia de la señal. La reducción de ganancia cambia. Ya no está reaccionando a información que después voy a tirar.

Este punto es importante: no moví el threshold todavía. Solo cambié qué información llega al detector. Eso solo ya modifica el comportamiento del compresor.

Después reviso la suma con otros micrófonos. Si filtro un canal y el otro no, o si uso pendientes distintas, la rotación de fase alrededor de la frecuencia de corte puede cambiar cómo suman. Entonces no basta con decir “el filtro va primero”. También tengo que verificar cómo quedó la relación entre señales después de filtrarlo.

Propongo un orden de trabajo de este eje: primero Trim o ganancia de clip para poner el nivel correcto de entrada, después filtros de limpieza, luego correcciones de polaridad y alineación, y recién después procesadores dinámicos. No porque sea un dogma absoluto, sino porque en la mayoría de casos de integridad evita que la cadena trabaje sobre información que no debería seguir adelante.

### 3. Teoría aplicada en el punto correcto
Los filtros estándar rotan fase alrededor de su frecuencia de corte. Los compresores reaccionan a la señal que reciben, no a la señal ideal que tú imaginabas dejar al final. Por eso el orden entre ambos cambia el resultado.

Si el contenido subsónico dispara el detector y luego se elimina, el compresor ya redujo ganancia por una causa que ya no existe en la salida. Eso es ineficiencia de cadena y, muchas veces, degradación audible.

### 4. Criterio de decisión
Aquí puse el filtro antes porque era filtrado de integridad: limpieza de contenido inútil. En otro contexto, un filtro colocado después de un compresor puede formar parte de una intención tonal o de un diseño más creativo, pero eso ya no es la lógica principal de este eje.

La pregunta correcta no es “qué plugin va primero”. La pregunta es “qué contenido quiero que vea el siguiente procesador”.

### 5. Errores frecuentes y falsas reglas
“El orden da igual si el resultado final parece parecido”. No. A veces lo que cambia no es el tono evidente sino la manera en que respira la dinámica.

“Siempre filtro antes de todo”. Casi siempre antes de dinámica cuando es limpieza, sí; pero no conviertas eso en mantra sin entender la razón.

“Si el compresor responde raro, el problema es el compresor”. Muchas veces no. A veces el problema es qué le estás enviando.

### 6. Cierre
Con esto el alumno ya tiene clara la lógica del filtrado dentro de la cadena. Ahora toca pasar de contenido frecuencial a relación entre señales: primero polaridad, luego alineación.

---

# E2-L04 — Corrección de polaridad: procedimiento corto y verificable

## Rol de esta lección dentro del proceso completo
Esta lección abre el bloque relacional del eje. Ya no estamos limpiando contenido sobrante: estamos resolviendo cómo dos o más señales sobre la misma fuente se suman entre sí. Polaridad correcta antes de alinear evita corregir tiempo sobre una relación binaria que ya venía mal desde el inicio.

## Objetivo del video
Enseñar un procedimiento corto, repetible y verificable para corregir polaridad en pares de micrófonos sin improvisación.

## Resultado que debería conseguir el alumno al terminar
El alumno debe poder revisar un par de micrófonos, igualar niveles, invertir polaridad de forma controlada, escuchar en contexto y escoger la versión que suma mejor, extendiendo luego esa verificación al conjunto.

## Situación práctica de partida
Estamos en una batería con micrófono superior e inferior del tambor. Al sumarlos, el tambor pierde cuerpo y no termina de asentarse con los overheads. El alumno sospecha de fase, pero todavía no separa bien polaridad de alineación.

## Estructura del guion

### 1. Apertura
Antes de mover clips y buscar milisegundos, hay una corrección más básica que puede devolverte el cuerpo de la suma en segundos: revisar polaridad.

### 2. Desarrollo paso a paso
Tomo el par top y bottom del tambor. Primero emparejo niveles lo mejor posible para no dejar que una diferencia grande de volumen engañe la comparación. Después escucho ambos juntos tal como están.

Luego invierto polaridad en uno de los dos canales. No lo hago al azar para “ver qué pasa” y quedarme con la opción más fuerte sin contexto. Lo hago sabiendo que el micrófono inferior suele quedar invertido respecto del superior por la física del movimiento del parche, pero igual verifico.

Escucho de nuevo el par. ¿Qué busco? Más cuerpo, más graves útiles, mejor integración del ataque con el cuerpo y menos sensación de hueco. Si la versión invertida devuelve solidez, me quedo con esa.

Pero no cierro ahí. Ahora comparo el par ya corregido contra overheads y contra el resto de la batería. Porque una polaridad que mejora el par aislado puede cambiar la relación con el conjunto. La regla práctica es corta: primero corrijo el par inmediato, luego verifico en el sistema completo.

No necesito volver esto una ceremonia eterna. El procedimiento debe ser rápido: emparejar, escuchar, invertir, comparar, decidir y verificar en contexto.

### 3. Teoría aplicada en el punto correcto
La inversión de polaridad no es lo mismo que un desplazamiento temporal. Polaridad es una inversión binaria del signo de la señal. Se corrige instantáneamente con el botón correspondiente. Si la suma cambia de forma dramática al invertir, el problema estaba ahí.

Eso no significa que la alineación temporal ya esté resuelta. Significa solo que la base binaria de la suma dejó de estar al revés.

### 4. Criterio de decisión
Aquí invertí polaridad porque la suma del par pedía cuerpo y coherencia, y la comparación inmediata mostraba una mejora clara. En otra grabación el micrófono inferior podría no necesitar inversión, o el problema principal podría ser tiempo y no polaridad. Por eso el botón no se pulsa por costumbre: se verifica.

### 5. Errores frecuentes y falsas reglas
“El micrófono bottom siempre va invertido”. No. Frecuentemente conviene, pero se verifica siempre.

“Si suena más fuerte, ya quedó bien”. No necesariamente. Puede haber más nivel y peor integración.

“Polaridad y fase son lo mismo”. No. Polaridad es una decisión binaria; la alineación temporal viene después.

### 6. Cierre
La polaridad correcta deja la base lista. La siguiente lección entra donde esta ya no alcanza: cuando la suma sigue necesitando ajuste, no por inversión binaria, sino por diferencia temporal entre señales.

---

# E2-L05 — Alineación temporal: manual, plugin y compromiso real

## Rol de esta lección dentro del proceso completo
Con la polaridad ya revisada, esta lección aborda el siguiente nivel del problema relacional: señales que no están invertidas, pero sí llegan en tiempos distintos. Aquí el alumno aprende que alinear no es “hacer coincidir dibujitos”, sino ordenar prioridades y aceptar compromisos reales.

## Objetivo del video
Enseñar a alinear temporalmente señales múltiples de forma manual o con plugin, definiendo referencias y entendiendo qué se gana y qué se sacrifica.

## Resultado que debería conseguir el alumno al terminar
El alumno debe poder elegir una referencia de alineación, ajustar señales de forma manual o automática sobre un fragmento representativo, verificar la suma en contexto y entender que cada corrección puede mejorar una relación y empeorar otra.

## Situación práctica de partida
Estamos mezclando batería multicanal. El tambor no termina de asentarse con overheads y rooms. El alumno ve los transitorios desfasados y quiere arrastrarlo todo hasta que quede perfectamente alineado, como si la batería existiera en un solo plano temporal.

## Estructura del guion

### 1. Apertura
Alinear no es convertir una batería real en una captura imposible. Es decidir qué relación temporal quieres priorizar y cuál estás dispuesto a dejar menos perfecta.

### 2. Desarrollo paso a paso
Empiezo definiendo referencia. No alineo todo contra todo. Necesito un centro de decisión. En batería, tomo como referencia principal el tambor superior, porque suele definir mucho del groove y de la percepción de golpe. Después miro bombo, overheads y el resto.

Primero hago una alineación manual simple. Amplío la vista, localizo el transitorio relevante y acerco la señal secundaria a la principal. No busco una coincidencia visual obsesiva desde el primer sample posible. Busco una mejora audible en la suma.

Reproduzco y comparo. Si el cuerpo aparece, si la definición mejora y si la suma se siente más coherente, voy bien. Si la alineación del tambor mejora pero overheads empiezan a sentirse raros, ahí aparece el punto crucial: toda alineación es una prioridad, no una perfección global.

Después muestro la opción con plugin de autoalineación. Lo inserto temprano en la cadena, escojo una sección representativa y dejo que escanee suficiente material. Pero no apruebo el resultado solo porque el plugin “encontró” un ajuste. Escucho igual que en manual. El plugin acelera el trabajo; no reemplaza el criterio.

También introduzco un atajo importante: si una señal secundaria está más de unos cuantos dB por debajo de la principal, el comb filtering que aporta puede ser mínimo. A veces bajar esa señal o replantear su rol resuelve más que seguir corrigiendo tiempo milimétricamente.

### 3. Teoría aplicada en el punto correcto
La desalineación temporal produce cancelaciones y refuerzos distintos según frecuencia. Por eso no siempre se percibe como un simple eco o retardo, sino como pérdida de cuerpo, ataque raro o coloración. 

En configuraciones complejas no existe una alineación perfecta para todas las relaciones al mismo tiempo. La distancia física entre micrófonos también construye perspectiva. Si anulas toda diferencia temporal, puedes ganar pegada local pero perder imagen o profundidad natural.

### 4. Criterio de decisión
Aquí prioricé tambor como referencia y acepté el resto como compromiso. En otra producción podría ser el bombo el centro, o incluso los overheads si la mezcla dependiera más de perspectiva general que de close mics agresivos.

La decisión depende de qué elemento define el groove, la producción y la percepción dominante del kit en esa canción.

### 5. Errores frecuentes y falsas reglas
“Alinear siempre mejora”. No. A veces quita profundidad o vuelve artificial la captura.

“Si visualmente coincide, ya quedó”. No. La verificación es auditiva.

“El plugin sabe más que tú”. No. El plugin propone. Tú decides.

“Hay que alinear todo al mismo punto”. No. Eso ignora que cada relación cumple una función distinta.

### 6. Cierre
Ya sabemos corregir relaciones entre señales completas. La siguiente lección toma ese principio y lo lleva a una estructura más específica: dividir una señal por bandas y comprobar si ambas ramas siguen reconstruyendo el original sin destruir la suma.

---

# E2-L06 — Split de frecuencias y prueba nula

## Rol de esta lección dentro del proceso completo
Esta lección funciona como puente entre alineación y gain staging. Enseña al alumno a verificar la integridad de una señal cuando la divide en dos ramas para procesarlas por separado. No basta con separar graves y agudos: hay que comprobar que la suma sigue siendo confiable.

## Objetivo del video
Enseñar a construir o revisar un split por crossover y validarlo con prueba nula antes de seguir procesando.

## Resultado que debería conseguir el alumno al terminar
El alumno debe poder entender qué busca un crossover correcto, usar la prueba nula como verificación y detenerse si la suma no reconstruye adecuadamente el original.

## Situación práctica de partida
Tenemos un bajo que queremos dividir en una rama grave y una rama media-aguda para procesarlas distinto. El alumno crea el split, procesa por separado y asume que si ambas ramas suenan bien aisladas, el diseño ya es correcto. Pero al recombinar, la suma pierde integridad.

## Estructura del guion

### 1. Apertura
Separar una señal no es gratis. Si el punto de cruce o la relación de fase entre ramas está mal, todo lo que hagas después trabaja sobre una base rota.

### 2. Desarrollo paso a paso
Tomo la señal original y la duplico en dos ramas. Una quedará para la zona grave y la otra para la zona alta o media-alta. Configuro el crossover con un diseño pensado para que ambas ramas puedan recombinarse con coherencia.

Antes de entusiasmarme con el procesamiento separado, hago una prueba básica: sumo ambas ramas tal como están y comparo contra la señal original. Si ya aquí noto rarezas de tono o nivel, todavía no empiezo a diseñar sonido. Primero corrijo el split.

Luego hago la prueba nula. Sumo ambas ramas y en una de ellas invierto polaridad. Si el crossover está bien construido y ambas ramas realmente reconstruyen la señal original, la cancelación debería ser casi total o dejar un residuo mínimo.

Si no cancela, no sigo adelante. Algo en amplitud, en fase o en el diseño del cruce no está bien. Resolver eso ahora es más barato que descubrirlo cuando ya haya distorsión, compresión y ecualización distintas en cada rama.

### 3. Teoría aplicada en el punto correcto
Un crossover no solo reparte frecuencias. También determina cómo se comportan ambas ramas en la zona de cruce. Si la suma entre ellas no está diseñada para reconstruir bien, el resultado final cambia aunque cada rama aislada parezca correcta.

La prueba nula no es una ceremonia académica. Es una verificación directa de integridad: o la estructura está sana o no lo está.

### 4. Criterio de decisión
Aquí uso prueba nula porque estoy ante una arquitectura de división paralela donde la reconstrucción importa. En otro contexto creativo, quizá no necesite reconstrucción exacta porque el split es deliberadamente transformador. Pero en este eje la prioridad es integridad, no efecto especial.

### 5. Errores frecuentes y falsas reglas
“Si las dos ramas suenan bien por separado, el split está bien”. Falso.

“La prueba nula es opcional”. No si quieres verificar integridad real.

“Después lo compenso con EQ”. Mala idea. Eso tapa un problema estructural con otra herramienta.

### 6. Cierre
Con esto cerramos el bloque relacional y dejamos lista una señal limpia y bien construida. Ahora toca calibrar niveles para que los procesadores posteriores reciban cada tipo de señal en su punto de trabajo.

---

# E2-L07 — Gain staging por tipo de señal

## Rol de esta lección dentro del proceso completo
Esta lección abre el bloque de nivel operativo del eje. El alumno ya filtró, corrigió polaridad y alineó. Ahora necesita asegurar que lo que entra a cada procesador llega con el nivel adecuado. Sin esto, el resto del curso opera en terreno inestable.

## Objetivo del video
Enseñar a calibrar el nivel de trabajo según el tipo de señal, distinguiendo señales percusivas y no percusivas.

## Resultado que debería conseguir el alumno al terminar
El alumno debe poder elegir el medidor de referencia adecuado para el tipo de señal, ajustar el nivel de entrada con Trim o ganancia de clip y dejar cada canal listo para procesarse sin depender de valores ciegos.

## Situación práctica de partida
Tenemos una voz, un bajo y una batería entrando a distintos procesadores. El alumno mira solo el medidor general de la DAW y asume que mientras no clippee, todo está bien. Pero algunos plugins reaccionan demasiado y otros casi no reaccionan.

## Estructura del guion

### 1. Apertura
Que una pista no esté clippeando no significa que esté bien calibrada. Una cadena puede tener headroom y aun así estar trabajando fuera de su punto útil.

### 2. Desarrollo paso a paso
Empiezo con una señal percusiva. En batería o percusión la referencia principal no suele ser el VU. Aquí me interesa más el comportamiento de los picos. Ajusto Trim o clip gain para que los picos caigan en una zona razonable que deje margen y evite que el siguiente procesador reciba demasiado nivel.

Luego paso a una señal no percusiva, por ejemplo una voz o un bajo sostenido. Aquí el Peak por sí solo no describe bien el nivel de trabajo. Ahora sí uso VU o RMS sobre un pasaje representativo. No tomo una sílaba aislada ni el track entero con silencios. Elijo una sección que represente cómo esa fuente vive realmente en la canción.

Ajusto el nivel hasta que la señal quede cerca de un punto de trabajo razonable para los procesadores que vendrán después. No busco un número mágico universal, pero sí una referencia consistente para que el comportamiento del compresor, del EQ modelado o del saturador no dependa del azar de cómo vino grabado el archivo.

Comparo también entre distintas fuentes. Un bombo y un tambor pueden tener picos parecidos y aun así cargar distinto un VU. Por eso no comparo cualquier instrumento con cualquier instrumento usando el mismo medidor sin pensar qué estoy midiendo realmente.

### 3. Teoría aplicada en el punto correcto
Las señales percusivas tienen alta cresta: gran distancia entre pico y nivel sostenido. Las no percusivas suelen describirse mejor con medidores integrados o promediados. Por eso el mismo sistema de lectura no sirve igual para todo.

El gain staging aquí no es balance musical. Es calibración de entrada a la cadena. Esa diferencia evita que el alumno use el fader para corregir lo que debía resolver con Trim.

### 4. Criterio de decisión
En este caso usé Peak para percusivas y VU o RMS para no percusivas porque la información relevante no es la misma. En otra sesión, si un sintetizador tiene transitorios muy agresivos, quizá combine ambas lecturas. Lo importante es entender qué pregunta responde cada medidor.

### 5. Errores frecuentes y falsas reglas
“Mientras no llegue a rojo, está bien”. No.

“Todo se calibra con VU”. No.

“Todo se calibra con Peak”. Tampoco.

“Gain staging es bajar faders”. No. Eso es balance de mezcla, no calibración de entrada.

### 6. Cierre
Ya tenemos claro con qué lectura decidir el nivel de trabajo. Falta una distinción igual de importante: qué control usa ese ajuste y cuál no. Eso es lo que organiza la siguiente lección.

---

# E2-L08 — Faders, trim y envíos: quién hace qué

## Rol de esta lección dentro del proceso completo
Esta lección ordena los controles de nivel de la sesión para que el alumno no solucione un problema correcto con el control incorrecto. Es una clase breve, pero crucial, porque muchos errores de flujo nacen aquí y contaminan todo lo demás.

## Objetivo del video
Distinguir con claridad el papel del Trim, del fader de canal, del send y del fader del retorno de efecto.

## Resultado que debería conseguir el alumno al terminar
El alumno debe poder elegir el control adecuado según quiera calibrar entrada a la cadena, balancear en la mezcla, alimentar un efecto o regular cuánto efecto vuelve a la suma.

## Situación práctica de partida
El alumno quiere que un compresor reciba menos nivel, pero en vez de usar Trim baja el fader. Luego quiere más reverb y sube el send sin revisar si en realidad lo que necesitaba era más retorno. Todo empieza a confundirse.

## Estructura del guion

### 1. Apertura
No todos los controles de nivel hacen lo mismo. Si los tratas como equivalentes, la sesión deja de tener lógica y empiezas a corregir consecuencias en vez de causas.

### 2. Desarrollo paso a paso
Empiezo con el Trim o la ganancia de clip. Este control define cuánto nivel entra realmente a la cadena de procesamiento. Si un compresor, saturador o EQ modelado está recibiendo demasiado o muy poco, aquí es donde lo corrijo.

Paso al fader del canal. Este no lo uso para calibrar la entrada del compresor. Lo uso para decidir cuánto pesa ese elemento dentro de la suma final. Es una decisión de balance musical.

Ahora miro un envío a un efecto. El send controla cuánto nivel entra al procesador del efecto. Si mando demasiado, puedo estar saturando la entrada del efecto o activando una respuesta distinta de la esperada. Pero eso no es lo mismo que cuánto efecto oigo en la mezcla.

Para controlar cuánto efecto escucho en la mezcla, uso el fader del retorno o del canal de efecto. Esa es la salida del efecto hacia la suma. Entonces separo dos decisiones: cuánto alimento el efecto y cuánto efecto dejo oír.

Hago una demostración simple. Envío una voz a una reverb. Primero ajusto el send hasta que la reverb trabaje de forma correcta. Luego con el fader del retorno decido cuánto ambiente aparece en la mezcla. Si intento resolver ambas cosas con un solo control, pierdo precisión.

### 3. Teoría aplicada en el punto correcto
Trim ajusta nivel de entrada a la cadena. Fader ajusta balance en la suma. Send ajusta nivel de entrada al efecto. Fader del efecto ajusta salida del efecto a la mezcla. 

Cuando se mezclan estas funciones, el problema deja de ser técnico y pasa a ser de flujo: ya no sabes qué parte de la cadena estás corrigiendo realmente.

### 4. Criterio de decisión
Aquí usé cada control según su función estructural. En otra sesión puede haber variantes de routing, pero la lógica se mantiene: entrada a la cadena, balance de suma, entrada a efecto y retorno del efecto no son la misma decisión.

### 5. Errores frecuentes y falsas reglas
“Bajo el fader y ya recibe menos el compresor”. Solo si el compresor está después del fader o si el routing lo permite; no lo asumas.

“Subo el send para tener más reverb”. A veces lo único que logras es excitar distinto el efecto, no colocar mejor el retorno.

“Trim y fader son intercambiables”. No.

### 6. Cierre
Con esto cerramos el bloque de calibración. La señal ya está limpia, alineada y bien organizada en nivel. Solo queda el último paso del eje: cuándo intervenir la interpretación sin destruir la música.

---

# E2-L09 — Afinación, timing y triggers sin destruir la interpretación

## Rol de esta lección dentro del proceso completo
Esta lección cierra el Eje 2. No trabaja carácter ni estética de mezcla; trabaja integridad musical mínima antes de entrar a decisiones más profundas de tono, dinámica y espacio. También deja claro el límite: corregir no es esterilizar.

## Objetivo del video
Enseñar a intervenir afinación, timing y triggers solo hasta el punto en que la interpretación recupere coherencia sin perder expresividad.

## Resultado que debería conseguir el alumno al terminar
El alumno debe poder decidir cuándo corregir afinación, cuánto cuantizar, cuándo dejar variación humana intacta y cómo revisar un trigger para que dispare golpes reales y no bleed o fantasmas innecesarios.

## Situación práctica de partida
Tenemos una voz con algunas notas que se caen, una batería con golpes apenas corridos y un refuerzo de tambor por trigger que a veces dispara donde no debe. El alumno quiere “arreglarlo todo”, pero corre el riesgo de borrar lo que hacía creíble la interpretación.

## Estructura del guion

### 1. Apertura
Corregir no significa volver clínico todo lo que estaba vivo. En este punto del proceso solo intervenimos cuando la ejecución ya está rompiendo la coherencia de la mezcla.

### 2. Desarrollo paso a paso
Empiezo con afinación. Escucho la voz en contexto. No pregunto primero si la nota cae exacta sobre la rejilla temperada; pregunto si la desviación se vuelve problema musical dentro de esta canción. Si sí, corrijo. Si no, dejar una pequeña inestabilidad puede ser más honesto y más musical que fijarlo todo al centro.

Cuando corrijo, prefiero tocar lo mínimo necesario. Si una frase entera está bien y solo una nota molesta, no reescribo toda la línea. Intervengo donde el problema aparece.

Paso al timing. Aquí hago la misma lógica. Si el groove general funciona y solo hay algunos ataques que rompen demasiado la coherencia, corrijo puntualmente. Si cuantizo todo al cien por ciento, puede que gane orden visual pero pierda respiración musical. Entonces uso cuantización parcial cuando conviene y corrección manual cuando el error es muy localizado.

Ahora reviso triggers. Cargo el disparador y no doy por hecho que cada detección es válida. Escucho el tambor original, miro dónde está disparando y compruebo si responde a golpes reales o si está leyendo bleed de otra pieza. Ajusto sensibilidad, umbral o filtrado del detector hasta que el trigger represente la intención original y no una falsa activación.

Si hago reemplazo o refuerzo con sample, no borro de inmediato el original. Primero verifico si el blend suma consistencia sin volver artificial la batería.

### 3. Teoría aplicada en el punto correcto
La afinación en este eje se corrige por integridad, no por perfección matemática. El timing se ajusta por coherencia de groove, no por obsesión con el grid. El trigger se valida por detección confiable, no por la comodidad de ver que “algo está disparando”.

Eso coloca esta lección dentro del Eje 2 y no en un eje de diseño: aquí restauramos consistencia mínima para que el procesamiento posterior tenga sentido.

### 4. Criterio de decisión
Corregí cuando la desviación ya afectaba la lectura musical de la mezcla. No corregí todo porque la interpretación también necesita variación real para sentirse humana.

En otra canción más mecánica o más editada, el margen de corrección podría ser mayor. En una producción más orgánica, podría ser menor. El criterio cambia con el rol estético de la interpretación dentro del tema.

### 5. Errores frecuentes y falsas reglas
“Todo debe quedar perfectamente afinado”. No.

“Todo debe caer exacto al grid”. No.

“Si el trigger dispara mucho, está funcionando”. No. Puede estar detectando lo incorrecto.

“Reemplazar siempre queda mejor que reforzar”. No.

### 6. Cierre
Con esto el Eje 2 queda cerrado. La señal ya no solo fue leída: fue limpiada, alineada, calibrada y, cuando hacía falta, corregida en su interpretación mínima. Recién ahora tiene sentido pasar al siguiente nivel: construir identidad espectral sin mezclar tono con problemas que debieron resolverse antes.