---

course_id: mezcla_masterizacion_kenth
module_id: M03
module_order: 3
module_title: Polaridad, fase y monocompatibilidad
module_slug: polaridad-fase-monocompatibilidad
doc_type: source_dossier
source_origin: author_compiled_from_transcripts
filename: M03_dossier_fuente.md
version: 0.1
status: draft_source_compilation
curation_source: extraccion_exhaustiva_notebooklm_desde_clases_definitivas
ready_for_indexing: false
-------------------------

# M03 — Dossier fuente exhaustivo

## Polaridad, fase y monocompatibilidad

> Este documento NO es guia canonica.
> NO es FAQ.
> NO es glosario final.
> Es una fuente intermedia exhaustiva, reorganizada por modulo, construida a partir de clases definitivas corregidas.
> Su objetivo es preservar detalle, matices, ejemplos, advertencias y trazabilidad antes de condensar doctrina para el RAG.

## 1. Alcance del dossier

* Este dossier reúne y reorganiza el contenido de M03 aunque haya aparecido:

  * en la clase central del módulo;
  * en demostraciones técnicas;
  * en respuestas a preguntas de estudiantes;
  * en clases posteriores de EQ, dinámica, tracking, mezcla y mastering;
  * en casos fronterizos donde la fase no se trata solo como relación entre dos señales, sino también como:

    * relación entre L/R;
    * relación entre close mics, overheads y room mics;
    * relación entre capas o doblajes;
    * relación interna entre armónicos de una misma forma de onda;
    * consecuencia de filtros, crossovers, compresión paralela o procesos multibanda.

* El alcance incluye, cuando aparecen en el material:

  * diferencia entre polaridad y fase;
  * expresión angular de la fase;
  * suma mono, suma coherente y suma no coherente;
  * cancelación parcial y cancelación total como caso ideal;
  * monocompatibilidad;
  * lectura prudente de correlación;
  * goniómetro, correlator, osciloscopio y medición por bandas;
  * comb filtering / filtro peine;
  * reglas numéricas y operativas;
  * jerarquía entre elementos primarios, secundarios y terciarios;
  * criterios de corrección y de no-corrección;
  * tensión entre decisión estética y problema técnico real.

* Quedan dentro del dossier varios contenidos dislocados porque pertenecen claramente a este módulo:

  * rotación de fase por ecualización;
  * fase lineal, latencia y pre-ringing;
  * compresión paralela y coloración por fase;
  * construcción de crossovers que reconstruyan sin error;
  * offset temporal para reparar graves no monocompatibles;
  * corrección de asimetría mediante all-pass;
  * problemas de fase derivados de monitoreo o posición de monitores.

---

## 2. Núcleo conceptual del módulo

* **Polaridad y fase no son lo mismo.**

  * La **polaridad** es binaria y absoluta.

    * Implica invertir positivo por negativo.
    * El ejemplo conceptual es invertir rojo por negro.
    * Está correcta o está invertida; no tiene estados intermedios.
  * La **fase** es relación temporal entre señales.

    * Implica desplazamiento, retraso o rotación de una señal respecto de otra.
    * Puede expresarse como desfase angular aunque físicamente ocurra en el tiempo.
  * El error terminológico clásico es llamar “fase” al botón que en realidad invierte polaridad.

    * El botón con el símbolo de círculo atravesado por diagonal, en consolas y plugins, está históricamente mal nombrado por la industria cuando se etiqueta como “phase”.
    * Su función real es **inversión de polaridad**.

* **Dos ondas a 180° y una inversión de polaridad pueden parecer equivalentes visualmente, pero conceptualmente no lo son.**

  * En un caso una señal fue desplazada.
  * En el otro fue invertida.
  * El material insiste en mantener separadas ambas nociones.

* **La fase se expresa en grados aunque el fenómeno ocurra en milisegundos.**

  * Se la explica por analogía con un círculo completo de 360°.
  * Equivalencias señaladas:

    * 0° = inicio del ciclo.
    * 90° = cuarto de ciclo.
    * 180° = medio ciclo.
    * 270° = tres cuartos de ciclo.
  * Por eso, decir que una onda “arranca en negativo” se corrige como formulación técnica imprecisa.

    * La formulación correcta es que arranca desplazada en 180°.

* **La suma perfecta y la cancelación perfecta son extremos ideales de relación de fase.**

  * A 0° la suma es máxima.
  * A 180° la cancelación es total en el caso ideal de señales equivalentes al sumarse.
  * Entre ambos extremos aparecen distintos grados de suma parcial, pérdida de solidez o cancelación parcial.

* **La percepción humana no equivale a la cancelación matemática.**

  * Cuando un oído recibe presión y el otro descompresión, no se produce cancelación a cero en el cerebro como en un nodo acústico captado por un micrófono.
  * Los oídos están separados físicamente.
  * El cerebro no anula la señal, pero sí la percibe como anómala, artificial, incómoda o “fuera de los parlantes”.
  * Esta distinción entre cancelación física y percepción binaural es central para no confundir:

    * fase en circuito o suma mono;
    * fase en el aire;
    * fase como experiencia psicoacústica.

* **La monocompatibilidad sigue siendo una exigencia práctica.**

  * Se corrige la idea de que ya no importa porque “todo es estéreo”.
  * El problema reaparece por:

    * radios AM;
    * muchas FM zonales;
    * televisores estándar;
    * oyentes fuera del sweet spot;
    * contextos reales donde la escucha se aproxima a mono o a una suma acústica no controlada.
  * Si la mezcla se desarma al pasar a mono, fallará fuera del entorno ideal de estudio.

* **No todos los problemas de fase deben tratarse como idénticos.**

  * Hay relaciones de fase entre:

    * L y R de una mezcla;
    * micros superiores e inferiores de un mismo tambor;
    * close mic y overhead;
    * overhead y sangrados;
    * pistas duplicadas o dobladas;
    * bandas de un crossover;
    * armónicos internos de una forma de onda.
  * Cada caso obliga a un diagnóstico distinto.

---

## 3. Distinciones clave del módulo

* **Polaridad vs. fase**

  * Polaridad:

    * inversión absoluta;
    * binaria;
    * no admite grados;
    * se chequea invirtiendo y escuchando cuál opción suma mejor.
  * Fase:

    * desplazamiento temporal/rotación;
    * sí admite grados;
    * puede variar continuamente;
    * puede repararse con tiempo, offset, posición, alineación o cambios de relación temporal.

* **Cancelación total ideal vs. cancelación parcial real**

  * La cancelación total aparece como caso ideal a 180° cuando dos señales equivalentes se oponen al sumarse.
  * En la práctica aparecen más frecuentemente:

    * cancelaciones parciales;
    * pérdida de graves;
    * ahuecamiento;
    * filtrado peine;
    * imagen falsa o incómoda;
    * degradación tímbrica.

* **Suma coherente vs. suma no coherente**

  * Una suma coherente exige señales con niveles parecidos y relaciones temporales suficientemente cercanas como para interferir de manera relevante.
  * Si las señales difieren mucho en nivel, la interferencia se vuelve despreciable.
  * El material formaliza esto con la tabla de sumas no coherentes y con la regla del 3 a 1.

* **Monocompatibilidad técnica vs. anchura estéreo**

  * El material responde de forma explícita que no se puede maximizar simultáneamente:

    * anchura estéreo extrema;
    * monocompatibilidad perfecta.
  * A mayor amplitud estéreo, menor monocompatibilidad.
  * Esto no significa que todo elemento ancho sea un error.
  * Significa que hay una relación costo/beneficio que debe leerse según el rol musical del elemento.

* **Error técnico real vs. costo estético aceptado**

  * **Primarios**:

    * voz principal;
    * bombo;
    * caja/tambor;
    * bajo.
    * Exigen monocompatibilidad estricta, centro sólido y buena suma.
  * **Secundarios**:

    * pads;
    * arpegiadores;
    * coros envolventes;
    * reverbs o capas que abrazan.
    * Pueden vivir mucho más abiertos.
    * Pueden rondar 90° y perder algo al cerrar a mono sin que eso sea automáticamente un error.
  * **Terciarios**:

    * FX muy cortos;
    * disparos;
    * elementos de duración brevísima.
    * Pueden incluso ir casi en contrafase extrema porque el oído no alcanza a marearse del mismo modo y el efecto sorpresa puede ser buscado.

* **Doubling real vs. falso estéreo**

  * No son equivalentes.
  * Duplicar una pista y retrasar un canal no reemplaza grabarla dos veces.
  * El falso estéreo genera comb filtering estático.
  * El doubling real produce variaciones humanas microscópicas de tiempo y pitch, de modo que el filtro peine se mueve y se vuelve estéticamente tolerable u orgánico.

* **Asimetría vs. DC Offset**

  * No son el mismo problema.
  * **DC Offset**:

    * desplazamiento de toda la onda por corriente continua cercana a 0 Hz;
    * se corrige con high-pass bajo.
  * **Asimetría**:

    * la onda está centrada pero sus picos se cargan más hacia arriba o hacia abajo;
    * se atribuye a la relación de fase entre armónicos;
    * se corrige con all-pass / rotor de fase, no con high-pass.

* **Proteger fase con fase lineal vs. aceptar rotación de fase**

  * Los filtros IIR/analógicos rotan fase.
  * Los de fase lineal evitan esa rotación relativa, pero introducen latencia y pre-ringing.
  * El material no presenta una salida “gratis”.
  * La formulación insistente es: **no hay filtros gratis**.

* **Cerrar a mono vs. corregir temporalmente**

  * Si el problema es de tiempo entre canales, no se corrige forzando amplitud al centro.
  * “Los problemas de tiempo se arreglan con tiempo”.
  * El mono maker no resuelve un desfase temporal; puede consolidar la cancelación.

---

## 4. Suma de señales, diagnóstico y lógica de interpretación

* **Suma mono de señales idénticas**

  * Se muestra explícitamente que dos señales idénticas sumadas en mono duplican voltaje.
  * Ejemplo:

    * dos senoidales de 100 Hz con pico en -6 dB suman 0 dB;
    * dos señales idénticas de -40 dB suman -34 dB.
  * El punto que se fija es que aquí se trabaja sobre suma de voltajes:

    * duplicar voltaje = +6 dB.

* **Relación entre ángulo, correlación y suma**

  * Equivalencias preservadas del material:

    * 0° / correlator +1 = suma de +6 dB.
    * 90° / correlator 0 = suma de +3 dB.
    * 120° = prácticamente sin suma.
    * 180° / correlator -1 = cancelación ideal a cero.
  * El material usa estas equivalencias como base de interpretación tanto técnica como visual.

* **Punto dulce de correlación**

  * Se propone como zona de equilibrio un promedio cercano al rango de 45°.
  * La lógica es:

    * buena suma mono;
    * imagen estéreo interesante;
    * menor riesgo de caer por fluctuación natural hacia zonas destructivas.
  * El propio material matiza que esta prudencia depende del tipo de elemento.

    * Para secundarios un promedio más abierto puede ser aceptable.

* **Lectura prudente del correlator**

  * No debe interpretarse en modo histérico por picos instantáneos.
  * Importa la tendencia general.
  * Debe usarse balística lenta o lectura promediada.
  * Si lo que queda en zona de cancelación es el promedio estructural, ahí sí hay problema real.

* **El correlator no es un promedio espectral neutro**

  * La lectura está arrastrada por la frecuencia dominante en amplitud.
  * Ejemplo conservado:

    * bajo a 100 Hz perfectamente en fase;
    * platillo a 5000 Hz cancelado;
    * el correlator puede mostrar “todo bien” porque manda el grave.
  * Inversamente:

    * en música con pads y arpegiadores dominantes en medios-agudos, la aguja puede ir a negativo aunque bombo y grave estén bien.
  * La conclusión preservada es:

    * el correlator no miente;
    * pero informa sobre la frecuencia dominante, no sobre todas por igual.

* **Diagnóstico por bandas**

  * Para escapar del arrastre de la frecuencia dominante se proponen dos rutas:

    * correlómetro multibanda;
    * correlator tradicional precedido por filtro pasabanda abrupto.
  * El filtro sugerido en la explicación es un pasabanda fuerte, por ejemplo de 48 dB/octava, haciendo barrido de frecuencia.
  * Así se aíslan regiones conflictivas ocultas por graves dominantes.

* **Lectura por rol musical**

  * El diagnóstico de una mezcla no se reduce a mirar si el correlator está siempre en +1.
  * Se juzga qué elemento se compromete al pasar a mono.
  * Si colapsan o se debilitan los elementos primarios, es problema técnico.
  * Si se afinan, diluyen o abren menos pads, coros o efectos secundarios, puede ser costo artístico aceptado.

* **Monocompatibilidad como chequeo concreto**

  * El material insiste en revisar en mono y no asumir que el estéreo basta.
  * También sugiere usar herramientas que hagan el chequeo con compensación más fiel.
  * Se recomienda Panipulator para comprobar paso a mono con ley de panorama de -6 dB por defecto, considerada más confiable para esta prueba.

* **Diagnóstico de inversión L/R del sistema**

  * Prueba propuesta:

    * emitir una señal compleja centrada en mono;
    * escuchar desde el sweet spot.
  * Si la señal aparece “fuera de los parlantes”, muy ancha o incómoda en vez de presentarse firme al frente, se sospecha:

    * inversión de polaridad L/R del sistema;
    * o una asimetría severa de sala.

* **Goniómetro**

  * Debe insertarse en una salida estéreo.
  * Lecturas preservadas:

    * línea vertical = mono / 0° / máxima suma.
    * óvalo que se ensancha = incremento de amplitud estéreo o mayor desfase.
    * círculo = cercanía a 90°.
    * línea horizontal = diferencia máxima / 180° / cancelación total al colapsar a mono.

* **Osciloscopio**

  * Se usa para comparar visualmente formas entre L y R.
  * Si ambas coinciden, el dibujo se superpone.
  * Si hay desfase, el corrimiento temporal se vuelve visible.

---

## 5. Ejemplos técnicos que no deben perderse

* **Ingeniería inversa con mezcla comercial mediante inversión de polaridad de un canal**

  * Procedimiento:

    * tomar mezcla estéreo;
    * invertir polaridad de L o de R;
    * sumar a mono.
  * Resultado:

    * se cancelan elementos perfectamente centrados;
    * sobreviven los laterales.
  * Ejemplos preservados:

    * en *The Eagles* desaparecen voz, bajo, bombo y tambor, quedando expuestos efectos estéreo, reverbs y guitarras laterales;
    * en *Metallica* sobreviven las guitarras por el doubling abierto, y se expone una reverb plate compartida entre batería y voz.
  * Uso:

    * herramienta “brutal” de ingeniería inversa;
    * sirve para estudiar cómo otro ingeniero distribuyó centro, lados y monocompatibilidad.

* **Top/Bottom de tambor**

  * El golpe hace que la presión y el movimiento de los parches generen polaridad relativa opuesta entre mic superior e inferior.
  * Procedimiento:

    * emparejar niveles;
    * invertir polaridad de uno, generalmente el bottom;
    * elegir la versión con más cuerpo y graves.
  * Se lo presenta como caso diario y obligatorio de chequeo en grabación acústica.

* **Grupo de tambor vs. overhead**

  * Luego de sumar top y bottom, se compara el grupo resultante con el tambor que sangra en overheads.
  * Se invierte polaridad del grupo completo respecto del overhead y se escoge la opción más sólida.
  * La prioridad declarada es preservar el tambor como referencia.

* **Falso estéreo por duplicación con delay**

  * Ejemplo:

    * duplicar una pista mono;
    * panear L/R;
    * retrasar uno de los lados.
  * Resultado:

    * sensación de pseudoanchura;
    * comb filtering estático;
    * ahuecamiento brutal al cerrar a mono.
  * El material insiste en que esto no es doubling.

* **Doubling real**

  * El músico graba dos veces.
  * Como nadie toca exactamente igual:

    * cambian microtimings;
    * cambia afinación microscópica;
    * el filtro peine se mueve/modula.
  * El resultado se percibe como:

    * pared de sonido;
    * grosor;
    * naturalidad relativa;
    * costo de monocompatibilidad asumido.
  * Se lo vincula explícitamente a rock y metal, por ejemplo quad tracking.

* **Filtro peine por retraso temporal**

  * Demostración:

    * duplicar una voz;
    * retrasar copia entre 1 y 10 ms;
    * observar analizador.
  * Se conserva el ejemplo concreto:

    * con 5 ms de retraso, la primera cancelación cae en 100 Hz;
    * luego alternan cancelaciones y sumas en múltiplos, dibujando “los dientes del peine”.
  * Descripción sonora preservada:

    * metálico;
    * robótico;
    * como flanger;
    * como caja de zapatos.

* **Técnica del piolín / equidistancia con overheads**

  * Si se mueve overhead para que tambor quede equidistante y alineado temporalmente:

    * puede arreglarse la transiente del tambor;
    * pero desbalancearse radicalmente el nivel relativo de los platillos.
  * Se conserva el ejemplo de diferencia extrema de cercanía:

    * un overhead puede quedar a 10 cm de un platillo y a 40 cm del otro;
    * eso altera violentamente el balance del set.
  * La conclusión es que no hay solución perfecta al alinear múltiples fuentes del kit.

* **Ducking en overheads para neutralizar interferencia con tambor**

  * Caso:

    * tambor muy procesado en close mic;
    * tambor crudo entrando por overhead;
    * choque de fase difícil de resolver solo moviendo tiempos.
  * Solución:

    * compresor en overheads;
    * sidechain desde el canal de tambor;
    * atenuar más de 9 dB durante la fracción de segundo del golpe.
  * Lógica:

    * se fuerza dinámicamente una diferencia de nivel suficiente para salir de suma coherente;
    * se vuelve perceptivamente irrelevante la interferencia temporal.

* **Inversión L/R en una mezcla estéreo**

  * Si se invierte la polaridad de un canal completo en la reproducción:

    * no hay cancelación eléctrica inmediata porque cada canal viaja por circuito separado;
    * pero acústicamente aparecen dos catástrofes:

      * pérdida de graves;
      * destrucción de la localización frontal.
  * Se describe la percepción como:

    * imagen falsa;
    * ancha de manera antinatural;
    * fuera de los parlantes;
    * capaz de provocar mareo o náuseas.

* **Analización de pad/arpegiador súper estéreo**

  * El material conserva la pregunta de si puede ser muy ancho y perfectamente monocompatible.
  * La respuesta es negativa en términos físicos.
  * Se conserva como ejemplo de tensión entre objetivo estético y restricción técnica.

* **Capas de vientos o voces que se vuelven nasales o a campana**

  * Caso surgido en clase posterior:

    * capas que suenan bien por separado;
    * al sumarse generan nasalidad o color de campana.
  * Diagnóstico del docente:

    * interferencias constructivas y destructivas;
    * problema de fase.
  * Primera propuesta:

    * desplazar temporalmente las capas un semiperíodo para invertir la relación entre suma y resta.

* **Roland Dimension en bajo en paralelo**

  * Ante miedo preventivo por posible fase en graves, el docente no aplica filtro por paranoia.
  * Abre goniómetro y correlómetro multibanda y decide según medición real.
  * Se conserva la conclusión operativa:

    * si la medición muestra que no destruye mono ni imagen, no hace falta introducir corrección preventiva.

* **Posición de monitores y crossover**

  * Si un monitor pensado para trabajar vertical se coloca horizontal:

    * cambia la relación geométrica entre woofer y tweeter;
    * en la frecuencia de cruce ambos emiten a la vez;
    * pequeños movimientos laterales de la cabeza alteran tiempos de llegada;
    * aparecen problemas de fase y cambios tímbricos incontrolables.
  * Se conserva como ejemplo de fase en el aire derivada de diseño físico y escucha.

---

## 6. Preguntas de estudiantes que sí aportan contenido

* **¿Si un oído recibe presión y el otro descompresión, se cancela el sonido?**

  * La pregunta habilita la distinción entre:

    * cancelación matemática en un punto físico o en una suma mono;
    * percepción humana binaural.
  * Respuesta preservada:

    * no se anula a cero;
    * se percibe raro, antinatural y molesto.

* **¿Conviene mutear graves para revisar correlación real de medios y agudos?**

  * La pregunta origina la explicación sobre:

    * frecuencia dominante;
    * correlómetro multibanda;
    * barrido con pasabanda abrupto.

* **¿Se puede tener un pad o arpegiador súper ancho y perfectamente mono-compatible?**

  * Respuesta:

    * no plenamente;
    * hay intercambio inevitable entre anchura y solidez mono.
  * También ayuda a introducir la jerarquía entre elementos primarios y secundarios.

* **Si el problema grave está por debajo de 120 Hz, ¿por qué no usar mono maker?**

  * La pregunta fuerza la corrección de un dogma operativo muy extendido.
  * Respuesta:

    * no corrige porque el problema es temporal;
    * puede destruir el grave;
    * la reparación verdadera es offset temporal.

* **¿Puede reemplazarse el doubling real duplicando una toma y retrasándola?**

  * La respuesta diferencia con claridad:

    * doubling real;
    * falso estéreo;
    * comb filtering estático vs. modulado.

* **¿Qué pasa con la fase en compresión paralela?**

  * La respuesta amplía el módulo hacia dinámica:

    * los compresores analógicos o modelados no son perfectamente planos;
    * pueden introducir rotación de fase y pequeña alteración tímbrica;
    * no suele tratarse como problema destructivo sino como parte del color.

* **¿Por qué varias capas de voces o vientos suenan nasales cuando se superponen?**

  * La respuesta instala explícitamente que una superposición puede generar interferencias constructivas y destructivas aunque cada capa aislada suene bien.

* **¿Hace falta filtrar preventivamente graves cuando se agrega modulación paralela a un bajo?**

  * La respuesta instala una idea metodológica:

    * no trabajar por paranoia;
    * medir y decidir con evidencia.

---

## 7. Advertencias, matices y correcciones del profesor

* **Corrección terminológica**

  * No llamar “fase” a la inversión de polaridad.
  * El botón industrialmente mal etiquetado debe entenderse técnicamente como inversión de polaridad.

* **No confundir lectura del correlator con verdad total**

  * El correlator depende de la frecuencia dominante.
  * Puede dar “todo bien” cuando una zona alta está destruida.
  * Puede dar “todo mal” cuando lo que está abierto son elementos secundarios.
  * Debe leerse:

    * con balística lenta;
    * por bandas cuando haga falta;
    * según función musical de lo que está sonando.

* **No todos los elementos deben estar perfectamente en fase**

  * Buscar +1 en todo puede ser error de criterio.
  * Primarios exigen rigor mayor.
  * Secundarios pueden abrirse.
  * Terciarios pueden exagerarse si el efecto lo justifica.

* **No convertir una recomendación artística en ley universal**

  * El rango de 45° como punto dulce se conserva como guía útil, no como ley indiscriminada.
  * El propio material admite excepciones artísticas claras.

* **Ojo con la técnica del piolín**

  * La alineación temporal perfecta de una fuente puede destruir el balance de amplitud del kit.
  * En batería no existe alineación perfecta para todo simultáneamente.
  * Cada corrección temporal reabre otro conflicto.

* **Prioridad del tambor**

  * Cuando haya que sacrificar algo en la batería acústica, el material fija una prioridad operativa:

    * dejar perfecto el tambor respecto de overheads.
  * Esto aparece como dogma operativo del docente, sensible al contexto pero sostenido con fuerza.

* **No alinear room mics automáticamente**

  * La sala debe llegar tarde.
  * Su función es dar distancia, tamaño y aire.
  * Si se alinea temporalmente, se destruye esa percepción.

* **No cambiar ley de panorama a mitad de mezcla**

  * La ley se define al principio y no se toca.
  * Alterarla después cambia niveles que llegan a procesos dinámicos y puede desarmar el equilibrio ya construido.

* **Ojo con ecualizar después de alinear**

  * Todo EQ IIR o analógico rota fase.
  * Si se alineó una batería y luego se ecualizan individualmente sus piezas, se vuelve a mover la relación temporal.
  * El material corrige además el mito de que un shelving “salva” la fase.
  * También rota.

* **No hay filtros gratis**

  * Evitar rotación de fase con fase lineal trae:

    * latencia;
    * pre-ringing;
    * energía previa al transiente.
  * La decisión no es entre bien y mal, sino entre tipos de daño o compromiso.

* **No usar mono maker como cura mágica**

  * Si los graves L/R están desfasados, colapsarlos al centro no los arregla.
  * Suma la onda atrasada con la adelantada.
  * Puede destruir el grave.
  * La frase doctrinal preservada es:

    * **los problemas de tiempo se arreglan con tiempo**.

* **No usar high-pass para corregir asimetría**

  * Si no hay DC Offset sino asimetría por fase interna de armónicos, el high-pass no resuelve el problema correcto.
  * El recurso pertinente es all-pass / rotor de fase.

* **No trabajar por paranoia**

  * Ante un efecto potencialmente problemático en graves, el criterio explícito es medir primero.
  * No aplicar filtros destructivos preventivos si la medición no muestra problema real.

* **No suponer que duplicar y retrasar equivale a grabar dos veces**

  * El material lo rechaza de manera frontal.
  * La duplicación con delay deja un peine estático.
  * El doblaje real genera variación humana y por eso se comporta distinto.

* **No borrar la dimensión psicoacústica**

  * Aunque no haya cancelación matemática a cero en escucha binaural, un error de polaridad/fase puede ser perceptualmente grave:

    * localización extraña;
    * pérdida de frente;
    * sensación antinatural;
    * incomodidad física.

---

## 8. Herramientas, referencias técnicas, configuraciones y detalles operativos

* **Herramientas de medición**

  * **Correlator / Correlatómetro**

    * mide relación de fase entre +1 y -1;
    * debe ir en salidas estéreo.
  * **Goniómetro**

    * lectura geométrica de mono, apertura y cancelación;
    * debe ir en salida estéreo.
  * **Osciloscopio**

    * permite ver superposición o corrimiento entre canales.
  * **Correlometer de Voxengo**

    * lectura multibanda para no depender solo de la frecuencia dominante.

* **Herramientas/plugins de corrección o trabajo**

  * **Auto-Align 2 (Sound Radix)**

    * autoalineación de fase entre múltiples canales;
    * debe insertarse en primer slot;
    * conviene analizar una muestra larga o el set completo, no un fragmento corto.
  * **Ozone 5**

    * usado como referencia para offset temporal entre canales;
    * también asociado al uso de rotor de fase / all-pass para asimetría.
  * **Faker**

    * plugin referido como solución específica para corregir monocompatibilidad de graves mediante compensación temporal.
  * **Panipulator**

    * recomendado para comprobar paso de estéreo a mono;
    * por defecto usa ley de panorama de -6 dB, considerada útil para chequeo más fiel.
  * **S1 MS Matrix** u otro codificador/decodificador M/S

    * usado en armado manual de matriz Mid/Side.

* **Procedimientos prácticos preservados**

  * **Chequeo de polaridad top/bottom**

    * emparejar nivel;
    * invertir uno;
    * elegir más cuerpo/grave.
  * **Chequeo de polaridad entre grupo de tambor y overhead**

    * emparejar niveles;
    * invertir grupo;
    * elegir opción más sólida.
  * **Ingeniería inversa de mezcla**

    * invertir L o R;
    * colapsar a mono;
    * escuchar centro cancelado y laterales expuestos.
  * **Diagnóstico por pasabanda**

    * insertar pasabanda abrupto, por ejemplo 48 dB/octava, antes del correlator;
    * barrer espectro y localizar bandas conflictivas.
  * **Alineación visual manual de batería**

    * usar el tambor como eje temporal prioritario, no el bombo.
  * **Armado manual de matriz M/S**

    * duplicar mezcla;
    * codificar a Mid/Side;
    * enviar a buses separados;
    * crear auxiliares mono;
    * procesar por separado;
    * recombinar en bus estéreo;
    * decodificar;
    * compensar pérdida matemática de 6 dB del ruteo.
  * **Corrección de monocompatibilidad grave con offset**

    * aislar problema en M/S o banda problemática;
    * retrasar un canal algunos milisegundos;
    * realinear ciclos hasta recuperar suma.
  * **Corrección de asimetría con all-pass**

    * usar all-pass/rotor de fase;
    * escuchar si el audio se rompe o no;
    * buscar mejorar simetría de picos y margen limitable.
  * **Corrección de comb filtering por absorción**

    * si la reflexión genera peine y acercar mic arruina timbre, no ecualizar;
    * colocar material absorbente denso en la trayectoria reflejada;
    * bajar más de 9 dB la reflexión para volver despreciable la interferencia.
  * **Ducking en overheads**

    * sidechain desde tambor;
    * caída mayor a 9 dB durante el golpe;
    * solución dinámica al conflicto de fase.

* **Valores y referencias técnicas preservadas**

  * 0°, 90°, 180°, 270° como referencias del ciclo.
  * 0° = correlator +1 = +6 dB.
  * 90° = correlator 0 = +3 dB.
  * 120° = casi sin suma.
  * 180° = correlator -1 = cancelación ideal.
  * Punto dulce orientativo alrededor de 45°.
  * Comb filtering entre 1 ms y aprox. 50 ms.
  * Ejemplo clave:

    * 5 ms de retraso = primera cancelación en 100 Hz.
  * Regla 3 a 1:

    * 20·log10(3/1) ≈ 9,5 dB.
  * Tabla de sumas no coherentes:

    * 0–1 dB de diferencia = suma aprox. 3 dB.
    * 2–4 dB = suma aprox. 2 dB.
    * 5–8 dB = suma aprox. 1 dB.
    * más de 9 dB = interferencia menor a 1 dB, despreciable.
  * Rotación por EQ IIR:

    * 45° por polo en frecuencia de corte.
    * 12 dB/oct = 90°.
    * 24 dB/oct = 180°.

* **Configuraciones operativas**

  * Goniómetro y correlator en salidas estéreo, no en canales mono.
  * Balística lenta para juzgar tendencia y no picos aislados.
  * Room mics: no alinear automáticamente.
  * Ley de panorama: definir al comienzo y no cambiar luego.
  * Auto-Align: primer slot, muestra larga.

---

## 9. Contenido dislocado que sí pertenece a M03

* **Rotación de fase por ecualización**

  * Todo filtro no lineal en fase rota la relación temporal.
  * Esto incluye shelving.
  * Consecuencia directa:

    * alinear batería y luego ecualizar sus piezas puede reabrir el conflicto de fase.
  * Pertenece a M03 porque afecta de manera directa la coherencia temporal buscada en tracking y mezcla.

* **Fase lineal, latencia y pre-ringing**

  * Los crossovers y multibandas rotan fase.
  * El modo fase lineal intenta evitar esa rotación, pero introduce:

    * latencia;
    * pre-ringing;
    * energía previa al golpe.
  * Esto expande el módulo hacia la decisión entre preservar fase o preservar transiente.

* **Crossovers y reconstrucción correcta**

  * Para dividir un bajo en bandas no basta poner HP en un canal y LP en otro a misma frecuencia si la reconstrucción no está pensada.
  * Si ambos caen a -3 dB en el punto de corte, pueden reforzarse y no cancelar en prueba nula.
  * El material conserva como solución:

    * cruce tipo Linkwitz-Riley;
    * atenuación a -6 dB en la frecuencia de corte;
    * fase lineal para reconstrucción perfecta y plana.
  * Esto pertenece a M03 porque muestra fase y suma matemática en ruteo.

* **Compresión paralela y color de fase**

  * La señal procesada por compresores analógicos/modelados no suele ser perfectamente plana.
  * Al mezclarla con la señal limpia aparecen pequeñas rotaciones y alteraciones tímbricas.
  * No se presenta como desastre, sino como parte del color.
  * Aun así, pertenece a M03 porque la fase afecta la suma paralelo/seco.

* **Superposición de capas**

  * Varias voces o vientos que suenan bien solos pueden generar nasalidad al sumarse.
  * Se diagnostica como interferencia de fase.
  * Se propone desplazar temporalmente capas para cambiar la relación entre suma y cancelación.

* **Falso diagnóstico en mastering**

  * En problemas graves de mono no basta colapsar el low-end al centro.
  * La reparación pertinente es temporal y por banda.
  * Se incorpora porque representa una formulación madura del mismo principio del módulo aplicada al mastering.

* **Asimetría de onda compleja**

  * La fase ya no aparece solo como relación entre dos canales o dos micrófonos.
  * Aparece también como relación entre armónicos internos de una misma señal mono.
  * El uso de all-pass para reordenar esa fase interna amplía el módulo sin salir de su núcleo.

* **Monitoreo y orientación física de cajas**

  * La geometría del woofer/tweeter y del crossover afecta fase y timbre en el punto de escucha.
  * Acostar una caja diseñada para vertical puede producir errores severos de fase con pequeños movimientos laterales.
  * Este material pertenece a M03 porque la fase se manifiesta también en el aire y en la escucha, no solo en el DAW.

* **Uso de medición en tiempo real en decisiones de mezcla**

  * El caso del Dimension en el bajo refuerza una doctrina transversal:

    * no corregir por reflejo;
    * medir correlación y mono;
    * decidir con evidencia.
  * Aunque aparezca en otra clase, es plenamente del módulo.

---

## 10. Mapa de cobertura

* **Núcleo teórico**

  * diferencia entre polaridad y fase;
  * fase como desplazamiento angular/temporal;
  * monocompatibilidad;
  * percepción binaural vs. cancelación física;
  * suma mono y relaciones de ángulo.

* **Núcleo de diagnóstico**

  * correlator;
  * goniómetro;
  * osciloscopio;
  * correlómetro multibanda;
  * lectura con balística;
  * lectura por bandas;
  * lectura según rol musical;
  * prueba de sistema invertido L/R;
  * revisión en mono.

* **Núcleo de grabación y mezcla**

  * top/bottom;
  * grupo de tambor vs. overheads;
  * técnica del piolín y sus límites;
  * prioridad del tambor;
  * no alinear room mics;
  * ducking como solución dinámica;
  * regla 3 a 1;
  * sumas no coherentes;
  * absorción como corrección del peine por reflexión.

* **Núcleo de imagen estéreo y producción**

  * inversión L/R;
  * falso estéreo;
  * doubling real;
  * anchura vs. mono;
  * rol de elementos primarios, secundarios y terciarios;
  * análisis inverso de mezclas comerciales.

* **Núcleo fronterizo de procesamiento**

  * rotación de fase por EQ IIR;
  * shelf también rota;
  * fase lineal y pre-ringing;
  * crossovers correctos;
  * compresión paralela y coloración por fase;
  * offset temporal por bandas;
  * M/S como marco operativo;
  * asimetría de onda y all-pass.

* **Núcleo de mastering/corrección avanzada**

  * rechazo al mono maker como cura universal;
  * corrección con offset temporal;
  * uso de herramientas específicas como Ozone/Faker;
  * recuperación de headroom por reorganización de fase interna.

---

## 11. Trazabilidad principal por clases

* **Clase 1**

  * primera formulación de diferencia entre polaridad y fase.

* **Clase 3**

  * percepción binaural vs. cancelación física;
  * sombra acústica y anomalía espacial;
  * problemas de fase derivados de posición de monitores y crossover;
  * prueba perceptual de sistema invertido L/R.

* **Clase 8**

  * núcleo central del módulo:

    * polaridad vs. fase;
    * grados;
    * goniómetro;
    * correlator;
    * osciloscopio;
    * monocompatibilidad;
    * inversión L/R;
    * ingeniería inversa con mezcla comercial;
    * top/bottom;
    * grupo de tambor y overhead;
    * ley de panorama;
    * Panipulator.

* **Clase 9**

  * correlator dominado por frecuencia principal;
  * medición por bandas con pasabanda o multibanda;
  * jerarquía de elementos primarios/secundarios/terciarios;
  * falso estéreo vs. doubling;
  * comb filtering;
  * regla 3 a 1;
  * sumas no coherentes;
  * corrección por absorción;
  * offset temporal para reparar graves.

* **Clase 10**

  * límites de la técnica del piolín;
  * prioridad del tambor;
  * alineación visual;
  * Auto-Align;
  * no alinear room mics;
  * ducking de overheads como solución moderna.

* **Clase 11**

  * rotación de fase por EQ IIR;
  * 45° por polo;
  * desalineación posterior a la EQ;
  * shelf también rota;
  * fase lineal;
  * latencia;
  * pre-ringing.

* **Clase 13**

  * capas de voces/vientos;
  * nasalidad/campana por interferencia de fase;
  * desplazamiento temporal como primera respuesta correctiva.

* **Clase 15**

  * refuerzo del problema de crossovers y fase lineal en procesos multibanda.

* **Clase 19**

  * compresión paralela;
  * pequeña rotación de fase y alteración tímbrica como parte del color.

* **Clase 23**

  * doubling real vs. falso estéreo;
  * utilidad práctica de medición en tiempo real con efectos de modulación;
  * continuidad del tema de guitarras dobladas en contexto de mezcla.

* **Clase 24**

  * cruce correcto de bandas en split de bajo;
  * Linkwitz-Riley;
  * reconstrucción plana;
  * prueba nula y suma.

* **Clase 26**

  * mastering y monocompatibilidad grave;
  * crítica al mono maker;
  * offset temporal con Ozone/Faker;
  * armado manual de matriz M/S;
  * asimetría de onda;
  * all-pass / rotor de fase;
  * separación estricta entre asimetría y DC Offset.
