---

course_id: mezcla_masterizacion_kenth
module_id: M06
module_order: 6
module_title: Espacialidad, profundidad y ambiencia
module_slug: espacialidad-profundidad-ambiencia
doc_type: source_dossier
source_origin: author_compiled_from_transcripts
filename: M06_dossier_fuente.md
version: 0.1
status: draft_source_compilation
curation_source: extraccion_exhaustiva_notebooklm_desde_clases_definitivas
ready_for_indexing: false
-------------------------

# M06 — Dossier fuente exhaustivo

## Espacialidad, profundidad y ambiencia

> Este documento NO es guia canonica.
> NO es FAQ.
> NO es glosario final.
> Es una fuente intermedia exhaustiva, reorganizada por modulo, construida a partir de clases definitivas corregidas.
> Su objetivo es preservar detalle, matices, ejemplos, advertencias y trazabilidad antes de condensar doctrina para el RAG.

## 1. Alcance del dossier

* Este dossier reúne y reorganiza contenido del módulo **Espacialidad, profundidad y ambiencia** proveniente de:

  * clases núcleo del módulo;
  * clases de fundamentos acústicos;
  * clases de ruteo y flujo de señal;
  * clases de paneo y panorama estéreo;
  * clases de fase/alineación;
  * clases de ecualización;
  * clases de dinámica;
  * bloques de mezcla y training donde el profesor responde preguntas o resuelve casos prácticos que en realidad pertenecen a M06.

* El alcance incluye, cuando aparece en las fuentes:

  * ambiencia;
  * reverberación;
  * reflexiones tempranas;
  * eco;
  * profundidad por diferencia temporal entre sonido directo y reflexiones;
  * construcción de planos cercanos/lejanos;
  * percepción horizontal de la fuente;
  * relación entre paneo, imagen estéreo y espacialidad;
  * diferencias entre espacio real capturado y espacio artificial construido;
  * herramientas, plugins, ruteos y configuraciones operativas;
  * advertencias sobre destrucción del tamaño de sala, hundimiento de la mezcla, monocompatibilidad y falsificación espacial.

* El dossier **no** convierte todavía estas ideas en doctrina final cerrada.

  * Conserva recomendaciones fuertes del profesor.
  * Conserva también técnicas puntuales, creativas o contextuales que luego requerirán formulación prudente en la capa canónica.
  * Si una regla depende del objetivo estético, del tempo, del tipo de fuente o del contexto de mezcla, queda consignado como tal.

## 2. Núcleo conceptual del módulo

* **Ambiencia como concepto más amplio que reverb**

  * La ambiencia no se reduce a “poner reverb”.
  * Se define operativamente como la manera en que interactuamos auditivamente con el ambiente físico que nos rodea.
  * Incluye:

    * posición física de la fuente;
    * diferencia entre sonido directo y reflejado;
    * reflexiones tempranas;
    * rebotes;
    * contexto espacial completo.
  * La reverberación es solo una parte final de ese fenómeno más amplio.

* **Cómo se forma la reverberación**

  * El profesor descarta la idea simplista de que la reverb sea un sonido “estirado”.
  * Usa dos analogías:

    * **piedra en el agua**: la fuente emite, la onda se expande, rebota y genera nuevas ondas; cuando las reflexiones se multiplican y densifican, el sistema deja de percibir eventos separados y aparece la sensación de reverberación;
    * **cine y fotogramas**: así como el cerebro une imágenes fijas y percibe movimiento, también integra una masa muy densa de ecos y rebotes sucesivos hasta percibir una sola entidad espacial continua.

* **RT60**

  * Es el tiempo que tarda un sonido en caer **60 dB** desde su valor máximo tras un impulso.
  * Esa caída equivale a **un millón de veces menos energía**, momento en el que el sonido se considera extinguido.
  * El RT60 se presenta como referencia técnica clave para pensar duración, decaimiento y compatibilidad rítmica del campo reverberante.

* **Relación entre sonido directo y campo reverberante**

  * El sonido directo cae con la **distancia** a la fuente.
  * La reverberación no cae del mismo modo con la distancia física del oyente dentro del recinto, sino con el **tiempo** de decaimiento.
  * En un recinto cargado de reflexiones, la energía reverberante tiende a repartirse de manera relativamente homogénea en el espacio.
  * Esta distinción es central para entender por qué el control de profundidad no depende solo de volumen absoluto, sino de la relación entre:

    * señal seca;
    * tiempo de llegada de reflexiones;
    * densidad de ambiente;
    * duración del decaimiento.

* **Profundidad como diferencia temporal entre directo y reflexión**

  * La profundidad no se enseña como “más reverb = más atrás” de forma aislada.
  * El principio central es la diferencia de tiempo entre:

    * el sonido directo;
    * la primera reflexión o el inicio del campo de ambiente.
  * Una fuente cercana:

    * se percibe primero con claridad en su sonido directo;
    * deja más espacio antes de que aparezca la reverberación.
  * Una fuente alejada:

    * presenta menos separación entre directo y reflejado;
    * suele ir acompañada de mayor proporción de ambiente.

* **Localización horizontal**

  * El cerebro localiza una fuente en el plano horizontal combinando cuatro factores:

    1. diferencia de tiempo de arribo entre ambos oídos;
    2. diferencia de amplitud;
    3. diferencia de fase;
    4. diferencia tímbrica producida por la sombra acústica de la cabeza.
  * Esto conecta espacialidad, paneo, fase y timbre en una sola lógica de percepción.

* **Sombra acústica**

  * Cuando la onda encuentra un obstáculo como la cabeza:

    * las frecuencias con longitud de onda mayor que el obstáculo lo rodean;
    * las frecuencias con longitud de onda menor chocan, se reflejan y/o se absorben parcialmente.
  * De ahí que el oído opuesto a la fuente pierda con mucha más severidad nivel en agudos que en graves.
  * Se aportan referencias físicas:

    * cabeza humana promedio: aproximadamente **17 cm** entre oídos;
    * una fuente a 90° puede generar alrededor de **0,5 milésimas de segundo** de diferencia interaural de arribo;
    * rango orientativo de longitudes de onda:

      * graves: del orden de **17 metros**;
      * agudos: del orden de **17 milímetros**.

* **Sala virtual y completamiento psicoacústico**

  * El docente plantea que una sala virtual puede construirse omitiendo cálculos complejos de trayectorias angulares y aun así funcionar perceptualmente.
  * El cerebro completa la información faltante.
  * La analogía usada es la de una palabra a la que le faltan letras pero que igualmente se lee.
  * Esto justifica por qué simulaciones relativamente simples en estéreo pueden generar una sensación espacial creíble.

## 3. Distinciones clave del módulo

* **Ambiencia vs. reverb**

  * La reverb no agota el concepto de ambiente.
  * La ambiencia abarca:

    * posición;
    * cercanía a paredes;
    * reflexiones tempranas;
    * rebotes;
    * contexto espacial.
  * La cola reverberante es solo una fase del fenómeno.

* **Reflexiones tempranas vs. eco**

  * Si una reflexión llega dentro de aproximadamente **50 ms** respecto del sonido directo, el sistema auditivo tiende a sumarla al sonido original.
  * El efecto suele ser:

    * ensanchamiento;
    * cuerpo;
    * refuerzo espacial.
  * Cuando supera aproximadamente **50 ms**, empieza a desprenderse como eco reconocible.
  * En señales muy percusivas, la separación puede sentirse ya desde **30 ms**.
  * El umbral se presenta como referencia sensible al contexto, no como valor absoluto universal.

* **Ambiente natural capturado vs. ambiente artificial construido**

  * Si existen **room mics** grabados, pueden cumplir naturalmente la función de espacio.
  * Sin embargo, el profesor distingue entre:

    * room natural usado como portador de carácter, agresividad o violencia;
    * ambiente artificial construido deliberadamente para profundidad y tridimensionalidad.
  * En el caso mostrado, los rooms de batería se revienten con compresión extrema para color, mientras la profundidad espacial “real” se arma aparte con un auxiliar dedicado.

* **Post-fader como regla general vs. Pre-fader como excepción espacial**

  * Regla general:

    * delays y reverbs en **post-fader**, para que al bajar el canal seco baje también la excitación del efecto.
  * Excepción espacial:

    * si se busca que una fuente parezca **alejarse**, se usa **pre-fader**;
    * al bajar el fader del canal, cae el sonido directo pero el ambiente conserva su nivel, forzando sensación de distancia.

* **Doubling real vs. falso estéreo por duplicación digital**

  * El **doubling real** implica grabar la interpretación dos veces.
  * La microdiferencia real de timing y pitch produce modulación orgánica y apertura natural.
  * El **falso estéreo** por duplicar digitalmente una pista y retrasarla con un delay fijo genera un filtro peine estático y destruye la suma mono.
  * Se presenta como error técnico claro.

* **Construcción espacial sutil vs. efecto evidente**

  * El ambiente no tiene por qué “oírse” todo el tiempo como efecto obvio.
  * Puede operar en un plano subliminal.
  * La prueba de su eficacia no es que llame la atención, sino que, al mutearlo, la escena pierda realismo, tamaño o tridimensionalidad.

* **Coherencia espacial vs. mito de la reverb única**

  * Se corrige la idea de que todos los instrumentos deban compartir una sola reverb para parecer en “el mismo cuarto”.
  * El docente sostiene que hoy se pueden combinar reverbs diferentes, incluso cortas con largas, y aun así conservar comunión espacial.
  * No se fija una única receta; se abre el criterio a contrastes estéticos y planos diferenciados.

## 4. Espacio, profundidad y lógica de construcción espacial

* **Construcción de profundidad mediante predelay manual**

  * En vez de depender del predelay interno de una reverb, el profesor coloca un plugin de delay simple antes de la reverb en el auxiliar.
  * Este retraso previo modela la distancia aparente entre el sonido directo y el primer rebote.
  * Cuando se trabaja así:

    * el **predelay interno de la reverb debe quedar en cero**;
    * el control de plano se realiza externamente por pista o por envío.

* **Lógica de planos**

  * Menor delay previo + mayor mezcla de ambiente:

    * fuente más atrás.
  * Mayor delay previo + menor mezcla de ambiente:

    * fuente más adelante.
  * Aplicación mostrada:

    * **conga/tumbadora**: más atrás, sin delay extra importante y con mayor cantidad de ambiente;
    * **guitarra base**: más cercana que la conga, con más delay y menos mezcla de ambiente;
    * **voz principal**: al frente, con la mayor cantidad de delay posible dentro del criterio espacial y con ambiente controlado para no hundirla.

* **Ambiencia antes que cola reverberante**

  * La enseñanza insiste en “armar la habitación” primero.
  * Antes de pensar en colas largas, se trabaja con:

    * reflexiones tempranas;
    * diferencias de tiempo;
    * diferencias de nivel;
    * asimetrías laterales.
  * La reverb larga aparece después como un posible componente, no como punto de partida.

* **Simulación de habitación con delays cortos**

  * Se puede construir una habitación virtual usando solamente delays.
  * Ejemplo operativo:

    * un lado a **11 ms**;
    * otro lado a **46 ms**;
    * **feedback** pequeño de aproximadamente **10%**.
  * Esto genera la percepción de que la fuente está más cerca de una pared que de la otra.

* **Ley de distancia aplicada a la sala virtual**

  * No basta con retrasar una reflexión más que otra.
  * También debe caer de nivel la reflexión más lejana.
  * Referencia física:

    * cada duplicación de distancia implica una caída de **6 dB** en campo abierto;
    * fórmula general consignada: **20 · log10(D1/D2)**.
  * Se aclara que esta referencia es estrictamente teórica para campo abierto y se usa como base para emular relaciones de amplitud en habitaciones virtuales.

* **Plano horizontal y espacialidad estéreo**

  * La percepción izquierda-derecha no es solo “paneo”.
  * Está gobernada por:

    * tiempo;
    * nivel;
    * fase;
    * filtrado natural por sombra acústica.
  * Esto vuelve inseparables la espacialidad y la forma en que una mezcla estéreo será decodificada por un oyente real.

* **Monitores vs. auriculares**

  * En monitores:

    * una señal paneada full izquierda no entra exclusivamente al oído izquierdo;
    * viaja por la sala y alcanza ambos oídos, con retrasos, sombras y cruce interaural.
  * En auriculares:

    * la interacción cruzada se pierde en gran medida;
    * el campo estéreo se simplifica artificialmente.
  * Consecuencia:

    * la construcción de profundidad, paneo y ambiente juzgada solo con auriculares suele quedar desproporcionada.

* **Centro de la escena y ley de panorama**

  * Cuando una señal va de los extremos al centro, termina alimentando ambos monitores y aumenta su potencia acústica.
  * Por eso los DAW aplican una **Pan Law**, por ejemplo **-3 dB** en el centro en Pro Tools.
  * Cambiar la ley de panorama a mitad de mezcla desordena:

    * la perspectiva espacial;
    * los balances;
    * la interacción con el mix bus.
  * Se trata de un complemento matemático importante para la escena estéreo.

* **Falsa amplitud por inversión de polaridad L/R**

  * Invertir la polaridad de un canal en una señal estéreo puede no mostrar cancelación eléctrica obvia en el master, pero sí destruir la referencia espacial frontal.
  * La imagen se vuelve artificialmente ancha y deja de proyectarse “de frente”.
  * El docente lo describe como una ruptura de la perspectiva, capaz de generar extrañeza, mareo o náusea.

* **Depth real capturado vs. destrucción por alineación**

  * Los **room mics** no deben alinearse temporalmente con los micrófonos cercanos.
  * Su función es precisamente llegar más tarde.
  * Ese retraso aporta:

    * distancia;
    * tamaño;
    * aire;
    * perspectiva lejana.
  * Alinearlos elimina la profundidad natural capturada.

## 5. Ejemplos técnicos que no deben perderse

* **Predelay manual con BL Sample Delay + Sound City**

  * El profesor arma auxiliares con una reverb `Sound City` de Waves y delante inserta `BL Sample Delay`.
  * Reparte distintos planos ajustando:

    * tiempo de retraso previo;
    * cantidad de mezcla de ambiente.
  * La demostración funciona como modelo directo de construcción de cercanía/lejanía.

* **Habitación virtual con delays simples**

  * Demostración con delays asimétricos:

    * 11 ms de un lado;
    * 46 ms del otro;
    * feedback pequeño;
    * atenuación diferencial de nivel según distancia.
  * El objetivo no es producir un eco rítmico, sino materializar acústicamente la posición de una fuente respecto de paredes laterales.

* **Ambiente general de batería con RVerb**

  * Desde el grupo de batería se crea un envío post-fader a un auxiliar estéreo con `RVerb`.
  * La lógica no es usar “reverb por cola”, sino ambiente:

    * se sube el nivel de **early reflections**;
    * se baja la cola principal;
    * se exagera primero el tamaño para encontrar la dimensión;
    * luego se reduce hasta el punto útil.
  * Esto permite envolver sin lavar.

* **Rooms naturales usados para agresividad y ambiente artificial usado para profundidad**

  * En batería, los room mics grabados no se usan necesariamente para “sala natural bonita”.
  * Se pueden comprimir salvajemente, por ejemplo con `CLA-76` en **all buttons**, para sumar violencia y carácter.
  * La sensación de profundidad y tamaño de la batería se puede construir aparte con otro auxiliar.

* **Ducking de reverb/delay disparado por la señal seca**

  * El compresor se inserta **después** del efecto espacial, en el auxiliar.
  * El detector sidechain se alimenta desde la **señal directa original**, no desde la propia reverb.
  * Efecto buscado:

    * la transiente o el ataque canta limpio;
    * la reverb/delay queda planchada en ese instante;
    * el release permite que el espacio “suba” y rellene solo en los huecos.
  * Se aplica tanto a voz como a tambor.

* **Reverb reverse / gated en paralelo para tambor**

  * Se construye un auxiliar con reverb en modo reverse.
  * Se vuelve más explosivo el tambor.
  * Antes de fijar la sensación, se inserta un compresor opto en el auxiliar, disparado por la señal directa del tambor.
  * Se trata de una construcción espacial-dinámica, no solo tímbrica.

* **Agrupación de ambientes por familias y tamaños**

  * En lugar de una sola reverb, se pueden armar auxiliares distintos:

    * ambiente grande para batería y bajo;
    * ambiente más pequeño para guitarras;
    * ambiente más controlado para voz.
  * El material no lo impone como ley universal; lo presenta como criterio dependiente del objetivo estético.

* **Apertura espacial por bandas en muestras estáticas**

  * Para abrir un sample cerrado:

    * se envía a un bus ciego;
    * se sacan tres envíos pre-fader: Low, Mid, High.
  * Tratamientos mostrados:

    * **Low**: compresión sidechain referida al bajo;
    * **Mid**: pasabanda con trémolo y reverb;
    * **High**: delay ping-pong y reverb.
  * Se presenta como técnica creativa específica de diseño espacial.

* **Apertura del ambiente y no del directo en hi-hat**

  * Para ensanchar un hi-hat estático, el docente no modula el canal directo.
  * Lo envía a una reverb, luego procesa ese campo reverberante con:

    * compresión;
    * flanger;
    * sidechain con el bombo;
    * filtrado.
  * Resultado:

    * el hi-hat directo permanece enfocado;
    * su campo espacial se abre, modula y respira en el estéreo sin perder foco rítmico central.

* **Doubling real como solución espacial verdadera**

  * Ante la tentación de duplicar digitalmente y retrasar, el profesor insiste en volver a grabar la toma completa.
  * La modulación natural producto de imperfecciones mínimas evita el filtro peine estático y protege la suma mono.

## 6. Preguntas de estudiantes que sí aportan contenido

* **Reflexión cercana = antes y más fuerte**

  * Al construir la sala virtual, un alumno señala que la pared más cercana no solo debería reflejar antes, sino también con más amplitud.
  * El profesor confirma y aprovecha para fijar la ley de distancia.
  * La pregunta consolida que la espacialidad no se simula solo con tiempo, sino también con nivel.

* **¿Cuándo deja de ser profundidad y pasa a ser eco?**

  * Un alumno pregunta por el límite temporal perceptual.
  * El profesor responde con la referencia de:

    * alrededor de **50 ms** como frontera general;
    * en material muy percusivo, separación posible desde **30 ms**.
  * Esto fija un criterio técnico central para predelay y reflexiones tempranas.

* **¿Hace falta ambiente artificial si ya tengo room mics?**

  * La pregunta obliga a distinguir:

    * room natural como captura del espacio real;
    * room procesado como herramienta de carácter;
    * ambiente artificial como construcción específica de tridimensionalidad.
  * El profesor responde que no siempre haría falta, pero que en la sesión mostrada sí separa ambas funciones.

* **Duda sobre post-fader y pre-fader en reverbs**

  * El estudiante recuerda el dogma de que los efectos temporales “siempre” van post-fader.
  * La respuesta corrige el absolutismo:

    * post-fader como regla práctica;
    * pre-fader como recurso espacial de alejamiento.

## 7. Advertencias, matices y correcciones del profesor

* **No llamar “ambiente” a cualquier cola larga**

  * El profesor corrige el hábito de equiparar ambiente con reverb larga.
  * La tridimensionalidad no se resuelve tirando una cola encima del canal.

* **El ambiente no siempre debe oírse**

  * Un ambiente bien calibrado puede pasar desapercibido mientras está activo.
  * Si al mutearlo la mezcla pierde realismo o tamaño, está cumpliendo su función.

* **Exceso de reverb = hundimiento**

  * Error reiterado en trabajos de alumnos:

    * demasiado ambiente;
    * pérdida de frente;
    * pérdida de definición;
    * mezcla hundida.
  * La espacialidad mal dosificada aleja y diluye transientes.

* **Duración de la reverb subordinada al tempo**

  * La cola reverberante de un golpe no debería arrastrarse hasta tapar el siguiente golpe importante.
  * Si se ignora el tempo y la figuración, el groove se embarra y los elementos se empujan hacia atrás.
  * El RT60 debe pensarse con cálculo musical, no “a ojo”.

* **Cuidado con filtrar los room mics**

  * Cortes high-pass agresivos en los room mics no solo limpian graves: también **achican la sala**.
  * Si se quiere conservar sensación de gran recinto, el tratamiento de graves en la ambiencia debe ser muy cuidadoso.
  * El material sugiere pendientes suaves o reconsiderar el nivel global antes que destruir la base espacial.

* **No alinear temporalmente los room mics**

  * La llegada tardía de los room mics es parte del fenómeno espacial que se desea conservar.
  * Alinear por automatismo destruye distancia y tamaño.

* **El envío al ambiente conviene salir del canal limpio**

  * Cuando existe una voz limpia y otra/o otras paralelas muy comprimidas, el error típico es mandar la suma a la reverb.
  * El profesor corrige:

    * alimentar la reverb desde el canal limpio;
    * conservar dinámica viva;
    * evitar que el campo reverberante reciba una señal rígida y planchada.

* **No comprimir la reverb “desde sí misma”**

  * El error no es usar compresión después del efecto, sino dispararla con la propia reverb.
  * La corrección es:

    * compresor después del efecto;
    * sidechain desde la pista seca.
  * Así el ambiente cede ante la fuente y no al revés.

* **El mito de la reverb única**

  * No usar una sola reverb para todo no implica romper la coherencia espacial.
  * Pueden convivir reverbs distintas si el criterio de planos y contraste está bien resuelto.

* **Auriculares como referencia espacial engañosa**

  * Mezclar espacialidad solo en auriculares rompe la lectura cruzada real del campo estéreo.
  * Esto afecta paneo, balances de profundidad y tamaño percibido.

* **La espacialidad puede justificar compromisos de fase**

  * En materiales de tipo ambient o inmersivos, el profesor muestra ejemplos donde la correlación cae a zonas rojas.
  * No lo trata automáticamente como error.
  * En esos casos, la profundidad emocional y la inmersión pueden imponerse sobre la monocompatibilidad estricta.
  * Este criterio queda como contenido sensible que requiere formulación prudente posterior.

* **La sala “entra más de lo que parece”**

  * El profesor subraya que grabar en distintos puntos físicos del cuarto cambia radicalmente el resultado.
  * Esto amplía la ambiencia más allá de la mezcla y la sitúa también en tracking y producción.

* **La reverb del auricular del músico no es un lujo accesorio**

  * Rechaza la lógica de grabar completamente seco “porque luego la reverb se añade en mezcla”.
  * Sostiene que el campo reverberante que oye el músico cambia:

    * su interpretación;
    * su groove;
    * su intensidad expresiva.

## 8. Herramientas, referencias técnicas, configuraciones y detalles operativos

* **Plugins y herramientas mencionados**

  * `BL Sample Delay (Blue Lab)`

    * usado antes de la reverb para construir profundidad por retraso manual.
  * `Sound City (Waves)`

    * reverb usada para construir ambiente;
    * señalada como efectiva aunque demandante en recursos.
  * `RVerb (Waves)`

    * usada para ambiente general, privilegiando reflexiones tempranas por sobre cola.
  * `Lexicon 480 / Relab LX480 Essentials / Complete`

    * señalado como modelo de alta gama;
    * la versión Essentials se presenta como suficiente para la mayoría de trabajos.
  * `FabFilter Pro-R`
  * `Valhalla`

    * mencionados como alternativas válidas para construir ambientes artificiales.
  * `CLA-76`

    * usado en room mics para agresividad y carácter, no necesariamente para profundidad realista.
  * `RComp` y compresores tipo Opto

    * usados en ducking de reverb/delay o en auxiliares de efectos.
  * `Roland Dimension`

    * usado para ensanchamiento sutil y apertura en elementos estáticos, operando sobre el Side.
  * `Provocative`

    * efecto tipo chorus/delay por bandas para abrir y engrosar señales procesadas.
  * `Correlometer` y goniómetro

    * usados para vigilar consecuencias de ensanchamientos espaciales sobre monocompatibilidad.

* **Configuraciones operativas**

  * Regla general:

    * envíos a delays/reverbs en **post-fader**.
  * Excepción creativa:

    * **pre-fader** para alejamiento.
  * Si el predelay se construye manualmente con un plugin de delay externo:

    * predelay interno de la reverb en **cero**.
  * En `RVerb` para ambiente:

    * subir **early reflections**;
    * bajar la cola principal.
  * Si el bus de reverb atiende a un único track:

    * envío a **0 dB** y mezcla por el retorno del auxiliar.
  * Si atiende a múltiples tracks:

    * retorno más estable y dosificación desde cada envío individual.
  * En sala virtual por delays:

    * tiempos asimétricos;
    * pequeño feedback;
    * nivel diferenciado según distancia.
  * En ducking de ambiente:

    * compresor después del efecto;
    * sidechain desde la pista seca;
    * release ajustado para que el espacio emerja en los huecos.

* **Valores y referencias numéricas**

  * **6 dB** por duplicación de distancia en campo abierto.
  * Fórmula: **20 · log10(D1/D2)**.
  * **50 ms** como frontera orientativa entre reflexión temprana y eco.
  * **30 ms** posible desprendimiento perceptual en material muy percusivo.
  * **11 ms / 46 ms / 10% de feedback** como ejemplo didáctico para habitación asimétrica.
  * **0,5 milésimas de segundo** como diferencia de arribo aproximada a 90° en un humano promedio.
  * **17 cm** de separación interaural de referencia.
  * **17 m / 17 mm** como extremos ilustrativos de longitudes de onda para graves y agudos.
  * **60 dB** de caída para RT60.

* **Técnicas de diagnóstico**

  * Mutear el bus de ambiente:

    * si la mezcla pierde realismo, el ambiente estaba bien calibrado aunque no fuera evidente.
  * Escuchar hundimiento de la mezcla:

    * síntoma de exceso de colas o abuso general de ambiente.
  * Verificar monocompatibilidad de ensanchamientos:

    * usar correlómetro y goniómetro;
    * si la señal se hunde o pasa a rojo promedio al plegar a mono, el recurso espacial es destructivo.
  * Detectar desproporción entre auriculares y monitores:

    * comprender que la diferencia no es un simple cambio tonal, sino una modificación del sistema de decodificación interaural.

## 9. Contenido dislocado que sí pertenece a M06

* **Clase 1 — sala virtual y completamiento psicoacústico**

  * Fundamento teórico de por qué la simulación espacial simple puede funcionar perceptualmente aun cuando no reproduzca toda la complejidad geométrica real.

* **Clase 3 — localización horizontal, sombra acústica y auriculares**

  * Base psicoacústica del plano horizontal.
  * Explica por qué el estéreo juzgado solo con auriculares falsea la experiencia real de espacialidad.

* **Clase 6 — pre/post fader y fuente limpia hacia reverb**

  * Dos aportes centrales de profundidad:

    * pre-fader para alejamiento;
    * alimentación del ambiente desde la señal limpia, no desde la suma comprimida.

* **Clase 8 — Pan Law e inversión de polaridad L/R**

  * Complementa el módulo al explicar:

    * el comportamiento del centro de la escena estéreo;
    * la falsa amplitud y pérdida de frontalidad cuando se rompe la referencia de polaridad entre canales.

* **Clase 9 — prioridad artística de la espacialidad sobre la monocompatibilidad**

  * En ciertos materiales inmersivos, la profundidad emocional puede justificar correlaciones problemáticas.
  * No se presenta como permiso universal, sino como criterio artístico condicionado al lenguaje musical.

* **Clase 10 — no alinear room mics**

  * Regla espacial fuerte:

    * no destruir el retraso natural que constituye la sensación de sala.

* **Clase 12 — high-pass en room mics achica la sala**

  * Cruce directo entre ecualización y espacialidad.
  * Lo primero que se altera no es solo el balance tonal, sino el tamaño percibido del recinto.

* **Clase 13 — ambiencia en tracking y monitoreo del intérprete**

  * La ambiencia entra en la grabación y además afecta psicológicamente la performance del músico.
  * La reverb de monitoreo se presenta como parte de la producción expresiva.

* **Clase 22 / 23 / 24 — ducking de reverb y delay**

  * Cruce entre dinámica y espacialidad.
  * Técnica avanzada para preservar nitidez del directo y permitir que el espacio aparezca solo cuando conviene.

* **Clase 23 — apertura espacial por bandas y modulación indirecta del campo reverberante**

  * Casos creativos donde la espacialidad se diseña desde auxiliares y bandas, no necesariamente desde la fuente seca.

## 10. Mapa de cobertura

* **Fundamentos perceptuales**

  * localización horizontal;
  * tiempo, nivel, fase y timbre;
  * sombra acústica;
  * interacción interaural;
  * diferencia entre escucha en monitores y auriculares.

* **Fundamentos acústicos**

  * formación de la reverberación;
  * reflexiones tempranas;
  * eco;
  * campo directo vs. campo reverberante;
  * RT60;
  * ley de distancia.

* **Construcción espacial**

  * sala virtual con delays;
  * predelay manual;
  * diferencias de plano;
  * ambiente por early reflections;
  * agrupación de ambientes por familia instrumental.

* **Criterios de mezcla**

  * ambiente sutil;
  * exceso de reverb como hundimiento;
  * RT60 subordinado al tempo;
  * coherencia espacial sin necesidad de reverb única;
  * uso diferenciado de room natural y ambiente artificial.

* **Ruteo y operación**

  * post-fader general;
  * pre-fader para alejamiento;
  * envío desde señal limpia;
  * ganancia unidad en buses de reverb;
  * predelay interno anulado cuando el predelay se construye externamente.

* **Corrección y diagnóstico**

  * ducking de reverb/delay por sidechain desde seco;
  * chequeo por muteo del ambiente;
  * validación de monocompatibilidad;
  * detección de hundimiento;
  * cuidado con filtros y alineación que destruyen la sala.

* **Casos creativos y límites**

  * reverse/gated reverb en paralelo;
  * modulación del campo reverberante;
  * apertura por bandas;
  * ensanchamientos que requieren verificación mono;
  * prioridad artística de la espacialidad en contextos inmersivos específicos.

## 11. Trazabilidad principal por clases

* **Clase 1**

  * sala virtual;
  * simplificación geométrica;
  * completamiento psicoacústico.

* **Clase 3**

  * localización horizontal;
  * tiempo, amplitud, fase y timbre;
  * sombra acústica;
  * diferencia entre monitores y auriculares.

* **Clase 6**

  * envíos post-fader como regla;
  * pre-fader para alejamiento;
  * envío a reverb desde canal limpio, no desde señal paralela planchada.

* **Clase 8**

  * Pan Law;
  * centro de la escena;
  * falsa amplitud y pérdida de frontalidad por inversión de polaridad L/R.

* **Clase 9**

  * espacialidad emocional;
  * correlación negativa o problemática en músicas inmersivas;
  * prioridad estética sobre corrección técnica absoluta en contextos puntuales.

* **Clase 10**

  * error de alinear room mics;
  * preservación de llegada tard llegada tardía y tamaño de sala.

* **Clase 12**

  * destrucción del tamaño de la sala por high-pass agresivo en room mics.

* **Clase 13**

  * influencia del espacio en tracking;
  * diferencia por posición física en la sala;
  * necesidad de reverb de monitoreo para la performance del artista.

* **Clase 20**

  * definición amplia de ambiencia;
  * formación de la reverberación;
  * analogía de piedra en el agua;
  * analogía de fotogramas;
  * RT60;
  * diferencia entre directo y campo reverberante;
  * reflexiones tempranas vs. eco;
  * simulación de habitación con delays;
  * ley de distancia;
  * mito de la reverb única.

* **Clase 21**

  * construcción de profundidad por predelay manual;
  * `BL Sample Delay`;
  * `Sound City`;
  * cero predelay interno en la reverb cuando el plano se diseña externamente;
  * criterios de conga, guitarra y voz en distintos planos;
  * ambiente sutil.

* **Clase 22**

  * `RVerb` usada como ambiente mediante early reflections;
  * exceso de reverb como hundimiento;
  * rooms naturales usados para agresividad;
  * ambiente artificial para profundidad;
  * ducking de reverb;
  * reverse/gated reverb en paralelo.

* **Clase 23**

  * chequeo por muteo del ambiente;
  * modulación indirecta del campo reverberante;
  * apertura por bandas;
  * chorus/delay y ensanchamientos a validar en mono;
  * doubling real vs. falso estéreo;
  * ducking aplicado a delay y reverb.

* **Clase 24**

  * duración de la reverb subordinada al tempo;
  * ruteo a ganancia unidad en buses de reverb;
  * agrupación de ambientes por familias;
  * refuerzo del ducking de campo reverberante como técnica de limpieza espacial.
