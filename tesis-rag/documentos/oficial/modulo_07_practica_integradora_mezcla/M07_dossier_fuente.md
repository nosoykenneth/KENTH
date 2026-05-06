---

course_id: mezcla_masterizacion_kenth
module_id: M07
module_order: 7
module_title: Práctica integradora de mezcla
module_slug: practica-integradora-mezcla
doc_type: source_dossier
source_origin: author_compiled_from_transcripts
filename: M07_dossier_fuente.md
version: 0.1
status: draft_source_compilation
curation_source: extraccion_exhaustiva_notebooklm_desde_clases_definitivas
ready_for_indexing: false
-------------------------

# M07 — Dossier fuente exhaustivo

## Práctica integradora de mezcla

> Este documento NO es guia canonica.
> NO es FAQ.
> NO es glosario final.
> Es una fuente intermedia exhaustiva, reorganizada por modulo, construida a partir de clases definitivas corregidas.
> Su objetivo es preservar detalle, matices, ejemplos, advertencias y trazabilidad antes de condensar doctrina para el RAG.

## 1. Alcance del dossier

* Este dossier reúne el material perteneciente al **Módulo 7: Práctica integradora de mezcla**.
* El módulo no se limita a una sola clase ni a una técnica aislada. Integra contenidos de:

  * sesiones de *training* de mezcla;
  * decisiones de ruteo;
  * gain staging;
  * dinámica;
  * filtros y ecualización;
  * espacialidad;
  * edición;
  * procesamiento Mid/Side;
  * diagnóstico de problemas;
  * gestión profesional del proyecto;
  * preparación de sesiones para continuidad, archivo y eventual mastering.
* La práctica integradora de mezcla aparece principalmente en las clases 21 a 24, pero también recibe contenido dislocado desde clases previas y posteriores:

  * Clase 6: ruteo, buses, auxiliares, envíos pre/post, arquitectura de efectos.
  * Clase 7: PLR y relación entre pico y promedio.
  * Clase 10: regla 3:1 aplicada dinámicamente a overheads.
  * Clase 11: crítica a la “mezcla Tetris” y concepto real de pegamento.
  * Clase 12: filtrado contextual, balance tonal con ruido rosa, límite de la mezcla frente a problemas de arreglo o grabación.
  * Clase 13: frontera entre mezcla, arreglo y grabación.
  * Clase 21: bolero, jerarquía de planos, consola Neve, espacialidad, gestión de cliente, problemas de guitarra/voz.
  * Clase 22: baterías, triggering, gates, reverb excesiva, gestión de recursos.
  * Clase 23: bajo, hip hop, samples, falso estéreo, denoising, ducking avanzado.
  * Clase 24: grupos, importación de sesiones, envíos, reverbs, delays, Mix Bus, split de bajo, limpieza de sesión.
  * Clase 25: método de álbum, canción hilo conductor, continuidad entre mezclas.
  * Clase 28: matriz Mid/Side híbrida, Waves C4, Pultec en Side, reparación avanzada de tensión vocal.
* El dossier preserva:

  * procedimientos técnicos;
  * valores numéricos;
  * ejemplos de clase;
  * advertencias;
  * preguntas de estudiantes con valor doctrinal;
  * analogías del profesor;
  * límites de validez contextual;
  * casos donde el profesor corrige malentendidos típicos.
* El material debe tratarse como fuente intermedia para construir después:

  * `M07_guia_canonica.md`;
  * `M07_faq.json`;
  * `M07_glosario.json`.

## 2. Núcleo conceptual del módulo

* **La mezcla como integración, no como suma de plugins**

  * La práctica integradora no consiste en aplicar procesadores por costumbre.
  * La mezcla exige decidir:

    * qué problema existe;
    * en qué eje ocurre;
    * qué herramienta corresponde;
    * cuánto conviene intervenir;
    * qué se destruye si se interviene demasiado.
  * La mezcla no arregla todo. Si una canción exige docenas de ecualizadores *Notch*, microcirugías constantes y correcciones extremas, el problema puede estar antes de la mezcla:

    * mala partitura;
    * mal arreglo;
    * instrumento mal elegido;
    * micrófono mal colocado;
    * mala sala;
    * mala librería;
    * mala grabación.
  * Se conserva la formulación asociada a Jerónimo Labrada: **“Si la partitura es mala, la mezcla es mala”**.
  * La preproducción y el arreglo musical aparecen como una porción decisiva del resultado final.

* **El problema tridimensional de la mezcla: tiempo, nivel y frecuencia**

  * El docente organiza los problemas de mezcla en tres ejes:

    * tiempo;
    * nivel;
    * frecuencia.
  * Una falla frecuente es usar una herramienta del eje equivocado.
  * Ejemplo central:

    * Si un tom debería hacer “doom” pero hace “duuuum”, el reflejo automático sería ecualizar la resonancia.
    * El profesor advierte que esa frecuencia puede ser parte vital de la identidad del instrumento.
    * El problema no necesariamente es “qué frecuencia tiene”, sino **cuánto tiempo dura**.
    * La solución corresponde al eje tiempo/nivel:

      * compuerta;
      * expansor;
      * ajuste de *Hold*;
      * ajuste de *Release*.
  * Este criterio atraviesa el módulo: antes de procesar hay que diagnosticar el tipo real de problema.

* **Jerarquía de planos**

  * La mezcla debe establecer qué elemento está adelante, cuál sostiene y cuál debe quedar en segundo o tercer plano.
  * En el bolero melódico trabajado en clase:

    * la voz y la guitarra principal deben estar al frente;
    * la conga debe ir atrás, sosteniendo;
    * si la conga cobra demasiado protagonismo, el tema deja de sentirse melancólico y se vuelve rítmico/bailable.
  * El plano no se decide solo por gusto personal.
  * El plano responde al género, al concepto, a la letra y al clima emocional buscado.

* **La mezcla como dirección de una película**

  * Analogía conservada:

    * los músicos son los actores;
    * la letra es el argumento;
    * el productor es el director;
    * una película no la dirigen todos los actores al mismo tiempo.
  * La mezcla necesita una idea rectora.
  * En bandas autoproducidas, cada músico tiende a buscarse a sí mismo:

    * el bajista pide más bajo;
    * el vocalista pide más voz;
    * el guitarrista puede pedir más guitarra.
  * El ingeniero no debe mezclar bajo cinco criterios diferentes.
  * Frase central preservada: **“Es mejor ir detrás de una idea equivocada que detrás de cinco ideas correctas pero diferentes”**.
  * Debe existir una única voz cantante o figura de producción que tome decisiones.

* **El álbum como edificio**

  * Un álbum no debe mezclarse como canciones totalmente aisladas desde cero.
  * Analogía:

    * el álbum es un edificio;
    * la estructura, las columnas, los cimientos, las tuberías y el hueco del ascensor deben mantenerse;
    * lo que cambia es la decoración de cada piso.
  * En mezcla:

    * se elige una canción “hilo conductor”;
    * se mezcla primero hasta aprobación;
    * se exporta/importa la estructura de esa mezcla a las canciones siguientes;
    * se ajusta cada tema según su arreglo y necesidad;
    * se mantiene una referencia del primer bounce para no perder el norte tímbrico.
  * Esta metodología evita que un disco termine sonando como varios discos desconectados.

* **El pegamento no nace únicamente en el Mix Bus**

  * El docente critica la “mezcla Tetris”:

    * aislar matemáticamente cada instrumento con filtros de pendientes muy abruptas;
    * usar pendientes de 24 a 96 dB/octava para que los instrumentos no se toquen espectralmente;
    * luego intentar “pegar” todo con un compresor en el Mix Bus.
  * La contradicción señalada:

    * primero se impide la interacción natural entre pistas;
    * luego se pretende recuperar esa interacción con compresión global.
  * El pegamento real empieza antes:

    * en la interacción acústica;
    * en el uso prudente de filtros;
    * en pendientes suaves cuando el contexto lo permite;
    * en no desarmar la mezcla por exceso de separación.

* **La mezcla se juzga en contexto**

  * El profesor prohíbe decidir ecualización contextual en *Solo*.
  * Si se recorta una guitarra rítmica alrededor de 280–285 Hz escuchándola sola, puede parecer delgada o destruida.
  * En contexto, ese mismo recorte puede ser lo que permite que el bajo respire y que la mezcla no se embarre.
  * El tercer motivo técnico para filtrar o ecualizar es hacerle lugar espectral a otro instrumento.
  * Esa decisión pertenece a la mezcla real, no al laboratorio de pistas aisladas.

* **La práctica integradora como uso combinado de módulos anteriores**

  * El módulo reúne:

    * ganancia y flujo de señal;
    * filtros;
    * fase;
    * dinámica;
    * espacialidad;
    * edición;
    * automatización;
    * ruteo;
    * diagnóstico macro;
    * referencias;
    * gestión de CPU;
    * preservación del proyecto.
  * La integración se ve en técnicas que combinan varios ejes simultáneamente:

    * Mid/Side + compresión multibanda + release vocal;
    * filtros + tremolo + delays por bandas;
    * sidechain dinámico en Mid;
    * reverb comprimida por señal seca;
    * triggering + alineación de fase;
    * gates con detector filtrado;
    * ruido rosa filtrado como control macro-espectral.

## 3. Distinciones clave del módulo

* **Mezclar una canción vs. mezclar un álbum**

  * Canción aislada:

    * se puede construir la sesión desde cero;
    * las decisiones solo tienen que sostener esa pieza.
  * Álbum:

    * necesita continuidad estructural y tímbrica;
    * se recomienda partir de una canción hilo conductor;
    * se importa la estructura mediante *Import Session Data* o equivalente;
    * se ajusta cada tema sin perder el sonido global del disco.
  * La canción hilo conductor puede ser:

    * la más representativa;
    * la que tiene más elementos comunes con el resto;
    * el tema principal o hit;
    * la que mejor define el sonido del proyecto.

* **Estructura base vs. decoración específica**

  * Estructura base:

    * mixer;
    * ruteos;
    * subgrupos;
    * niveles operativos;
    * EQs base;
    * compresores de bus;
    * arquitectura de efectos;
    * consola virtual.
  * Decoración específica:

    * balances propios de cada canción;
    * color;
    * automatizaciones;
    * arreglos particulares;
    * decisiones de plano según letra y energía.

* **Tiempo, nivel y frecuencia**

  * Problema de frecuencia:

    * resonancia;
    * enmascaramiento;
    * aspereza;
    * exceso o falta de zona tonal.
  * Problema de nivel:

    * pico errático;
    * desbalance;
    * elemento demasiado adelante o atrás.
  * Problema de tiempo:

    * cola demasiado larga;
    * sustain excesivo;
    * reverb que invade;
    * release mal ajustado;
    * tom que dura demasiado.
  * La herramienta debe responder al eje correcto.

* **Neve vs. SSL**

  * Neve / Lindell:

    * elegida para formaciones acústicas pequeñas;
    * útil cuando se buscan curvas anchas;
    * menor cantidad de bandas;
    * color;
    * distorsión armónica;
    * preamplificación con THD;
    * pegamento cálido;
    * integración musical.
  * SSL:

    * más precisa;
    * más selectiva;
    * más paramétrica;
    * útil en mezclas densas;
    * pertinente para pop/rock de muchas pistas;
    * puede resultar excesiva o menos integradora para un bolero acústico de pocos instrumentos.
  * La elección de consola virtual se subordina a la densidad del arreglo y a la estética buscada.

* **Compresión individual vs. compresión de grupo**

  * Compresión individual:

    * primera etapa;
    * corrige picos erráticos;
    * controla tomas independientes;
    * puede usar compresores rápidos como 1176.
  * Compresión de grupo:

    * segunda etapa;
    * no debe usarse para cazar picos individuales;
    * sirve para amalgamar;
    * puede usar compresores lentos como LA-2A o Lindell/Neve 2254;
    * reducción sugerida: 1 a 2 dB para *Glue*.
  * Error corregido:

    * insertar un 1176 directamente en el grupo de guitarras o coros.
    * Si la toma izquierda tiene un pico, el compresor aplasta también la derecha aunque no tuviera problema.

* **Ducking estándar vs. ducking Mid Only**

  * Ducking estándar:

    * baja todo el bajo cuando entra el bombo;
    * puede generar bombeo notorio;
    * puede destruir chorus, estéreo o movimiento lateral del bajo.
  * Ducking avanzado Mid Only:

    * usa una herramienta multibanda o ecualizador dinámico como Pro-MB;
    * aísla solo la zona de conflicto;
    * recibe sidechain externo desde el bombo;
    * opera estrictamente en el canal Mid;
    * despeja el centro para el bombo;
    * conserva los laterales y la amplitud estéreo del bajo.

* **Limpieza pop vs. suciedad rock**

  * Pop moderno:

    * busca separación extrema;
    * tiende a aislar o borrar bleed;
    * gates más cerrados.
  * Rock/orgánico:

    * el bleed puede aportar tamaño, realidad y pegamento acústico;
    * no todo sangrado es basura;
    * un *Range* moderado en la compuerta, por ejemplo -10 dB en vez de -80 dB, deja un fondo constante que une los cuerpos de batería.
  * Esta distinción no debe convertirse en ley universal; depende de estética, género y producción.

* **Doubling real vs. falso estéreo**

  * Doubling real:

    * el músico graba dos veces;
    * las diferencias humanas microscópicas de tiempo y afinación hacen que la fase module;
    * genera amplitud estéreo orgánica;
    * conserva mejor la monocompatibilidad.
  * Falso estéreo:

    * duplicar digitalmente una pista mono;
    * panear copias;
    * aplicar Sample Delay estático;
    * genera filtro peine fijo;
    * al colapsar a mono puede cancelar y destruir la señal.
  * La corrección del profesor separa producción genuina de atajos digitales destructivos.

* **Bus vs. auxiliar**

  * Bus:

    * ruta interna;
    * cable invisible por donde viaja el audio;
    * no tiene por sí mismo plugins ni salida física.
  * Auxiliar:

    * canal o módulo de destino;
    * recibe el bus;
    * puede tener inserts, fader, salida y procesamiento.
  * Esta distinción es básica para entender ruteos complejos del módulo.

* **Master Fader vs. Mix Bus auxiliar**

  * En una arquitectura profesional:

    * el Mix Bus auxiliar puede recibir la mezcla entera antes del Master Fader;
    * permite imprimir stems;
    * permite envíos paralelos de la mezcla completa;
    * permite insertar procesos analógicos o de mezcla.
  * El Master Fader puede reservarse para:

    * medición;
    * analizadores;
    * LUFS;
    * herramientas que no deben imprimirse necesariamente en el bounce.
  * La pregunta del estudiante sobre enviar todo directo al Master Fader permite fijar esta distinción.

* **Un solo cuarto de reverb vs. profundidad por contraste**

  * Mito corregido:

    * “La reverb tiene que ser la misma para todos para que parezca el mismo cuarto”.
  * Corrección:

    * la tridimensionalidad se construye diferenciando tamaños, profundidades y planos;
    * no se logra haciendo una sopa única.
  * Ejemplo:

    * ambiente grande para batería y bajo, empujándolos lejos;
    * ambiente medio para guitarras;
    * ambiente corto y controlado para la voz en primer plano.

* **Post-fader por defecto vs. pre-fader para alejamiento**

  * Dogma corregido:

    * todos los envíos de reverb/delay deben ir siempre post-fader.
  * Técnica de alejamiento:

    * poner el envío en pre-fader;
    * automatizar bajando el fader del canal seco;
    * la señal directa baja;
    * la reverb se mantiene;
    * el sonido parece alejarse en profundidad.

* **HPF en master “por las dudas” vs. limpieza canal por canal**

  * Mito corregido:

    * insertar un High-Pass a 20 Hz en el Master por seguridad.
  * Problemas:

    * arrastra basura subsónica de pistas que debieron limpiarse antes;
    * ensucia subgrupos;
    * roba espacio intermedio;
    * un HPF en el master rota la fase global;
    * puede elevar picos espurios por overshot.
  * Criterio del profesor:

    * limpieza subsónica canal por canal al principio de la mezcla.

* **Nivel RMS vs. PLR**

  * La mezcla no se evalúa únicamente por RMS o competitividad de volumen.
  * Aparece el parámetro PLR:

    * Peak to Loudness Ratio;
    * Factor de Cresta;
    * distancia entre pico y promedio.
  * Referencia conservada:

    * una buena mezcla Pop/Rock debería sostener aproximadamente 13 a 15 LU de PLR.
  * Si se aplastan todos los picos para levantar RMS antes del mastering, la mezcla pierde impacto vital.

* **Corrección digital útil vs. mutilación**

  * Denoisers como Waves X-Noise pueden reducir ruido constante.
  * Si se intenta eliminar todo el ruido elevando demasiado el threshold:

    * el algoritmo puede comerse transientes útiles;
    * aparecen artefactos;
    * la guitarra puede sonar artificial o con chirridos acuáticos.
  * Criterio:

    * atenuar ruido;
    * no borrar el instrumento junto con el ruido;
    * tolerar algo de fondo si preserva la musicalidad.

## 4. Flujo de trabajo integrador y toma de decisiones en mezcla

* **Selección de la canción hilo conductor**

  * Para álbumes o proyectos de varias canciones:

    * no empezar cada canción desde cero;
    * elegir primero la canción más representativa;
    * mezclarla hasta aprobación;
    * convertirla en molde del proyecto.
  * El molde incluye:

    * ruteos;
    * consola;
    * subgrupos;
    * niveles base;
    * EQs base;
    * compresores de bus;
    * arquitectura de efectos;
    * criterios de planos.
  * Después se usa *Import Session Data* o función equivalente para trasladar esa estructura a la siguiente canción.
  * En la sesión siguiente:

    * se importa el bounce estéreo del primer tema;
    * se coloca como referencia dentro del multipista;
    * puede alinearse estribillo con estribillo;
    * se hacen comparaciones alternando Solo/bypass cruzado;
    * se verifica que el sonido del disco no se pierda.

* **Preparación de sesión**

  * Ajustar niveles antes de procesar:

    * usar Clip Gain;
    * buscar headroom suficiente;
    * evitar entrar demasiado fuerte a consolas virtuales.
  * Atajo operativo visual:

    * la forma de onda puede ocupar aproximadamente 1/3 del alto vertical del track;
    * esto suele ubicar picos alrededor de -6 dBFS;
    * promedios aproximados en -18/-20 dBFS.
  * Este criterio es sensible al contexto:

    * no es una métrica absoluta de medidor;
    * es un atajo visual operativo.
  * Calibración de consola virtual Neve/Lindell:

    * enviar onda senoidal a -18 dBFS desde el DAW;
    * buscar que el medidor de entrada marque +4 dBu o cero VU en equipos genéricos.

* **Limpieza inicial**

  * Limpiar subsónicas canal por canal, no en el master por costumbre.
  * Elegir filtros por contexto:

    * no aplicar valores universales;
    * escuchar la función del instrumento en la mezcla.
  * Valores del bolero conservados como contexto específico:

    * Conga HPF 70 Hz, con fundamental mencionada en 232 Hz.
    * Guitarra base HPF 45 Hz, con fundamental mencionada en 82 Hz.
    * Guitarra de arreglo HPF 160 Hz y LPF en 14 kHz para llevarla a un plano “vintage de los 70s”.
    * Voz HPF en 160 Hz.
  * Estos valores no deben formularse después como dogmas universales.

* **Orden de procesamiento en consola SSL con Split**

  * En el canal de consola debe activarse el botón *Split*.
  * Esto modifica el flujo para que la ruta sea:

    * entrada;
    * filtros;
    * dinámica VCA;
    * ecualizador.
  * La finalidad es limpiar primero ruidos/subsónicas antes de la etapa dinámica.

* **Diagnóstico antes de corregir**

  * Identificar si el problema es:

    * de frecuencia;
    * de nivel;
    * de duración;
    * de fase;
    * de ruteo;
    * de arreglo;
    * de grabación.
  * No asumir que todo se resuelve con EQ.
  * Ejemplos:

    * Tom largo: resolver duración con gate/expansor.
    * Bajo que no corta: alterar envolvente con compresor, no necesariamente sumar 800 Hz.
    * Tensión vocal puntual: usar proceso dinámico contextual, no EQ estático general.
    * Guitarra que tapa bajo: recorte contextual escuchando todo, no en Solo.
    * Sample plano: dividir bandas y generar movimiento con procesos diferenciados.

* **Jerarquía de planos**

  * Antes de procesar hay que decidir:

    * qué lidera;
    * qué acompaña;
    * qué sostiene;
    * qué debe sentirse más que escucharse.
  * Técnica diagnóstica del mute por contraste:

    * mutear una percusión secundaria;
    * si la canción sigue funcionando, su rol de fondo es correcto;
    * si al volver la percusión transforma el carácter emocional hacia algo bailable o protagónico, el nivel o plano es tóxico.
  * Este diagnóstico aparece con la conga en el bolero.

* **Ruteo de grupos**

  * Elegir grupos mono o estéreo según la física del instrumento:

    * top/bottom de redoblante a subgrupo mono porque son un único instrumento en un punto fijo del panorama;
    * tres toms a subgrupo estéreo porque ocupan posiciones distintas L/R.
  * Evitar colapsar imagen estéreo por ruteo incorrecto.

* **Compresión individual antes de grupo**

  * En coros o guitarras dobladas:

    * primero controlar tomas individuales con compresión rápida;
    * luego rutear al grupo;
    * después aplicar compresión grupal lenta y ligera para glue.
  * Reducción de grupo conservada:

    * 1 a 2 dB.
  * Compresores mencionados:

    * 1176 para control individual rápido;
    * LA-2A, Lindell 2254 o Neve 2254 para glue.

* **Efectos temporales y arquitectura de envíos**

  * Si un efecto atiende exclusivamente a una sola pista, por ejemplo delay de una voz:

    * el envío puede ponerse en ganancia unidad, 0 dB;
    * se excita el procesador al nivel operativo ideal;
    * el balance se controla con el fader de retorno del auxiliar.
  * Evitar loops:

    * si una reverb de tambor recibe señal del tambor y vuelve al mismo grupo que alimenta, puede generarse feedback/acople destructivo.
    * Los FX paralelos deben converger en una etapa posterior, como Mix de Batería o Mix Bus global, no en el subgrupo primario que los alimenta.

* **Sidechain en efectos**

  * Para delays o reverbs vocales:

    * insertar delay/reverb en auxiliar;
    * insertar compresor a la salida del efecto;
    * alimentar el sidechain desde la pista seca original;
    * mientras la voz canta, el compresor aplasta el ambiente;
    * cuando la voz calla, el release levanta la cola y rellena el espacio.
  * Esta técnica evita que las primeras repeticiones invadan la transiente o inteligibilidad de la voz.

* **Gestión de CPU, archivo y preservación**

  * No dejar instrumentos virtuales vivos en la mezcla final:

    * Perfect Drums;
    * sintes;
    * librerías;
    * cualquier instrumento MIDI dependiente de licencia o sistema operativo.
  * Regla:

    * hacer Commit/Print a audio;
    * ocultar e inactivar MIDI;
    * no borrar el MIDI de respaldo.
  * Limpiar matriz I/O:

    * borrar buses no usados;
    * borrar entradas/salidas no utilizadas.
  * Usar Strip Silence:

    * vaciar silencios;
    * crear pequeños fades automáticos;
    * permitir que Dynamic Plugin Processing apague consumo cuando no hay audio.
  * Advertencia:

    * si luego se consolida toda la pista uniendo silencios, se destruye la optimización;
    * el motor vuelve a procesar plugins durante toda la canción.
  * Al finalizar:

    * usar Save Session Copy In;
    * crear carpeta final con solo los archivos efectivamente utilizados.

* **Chequeo macro de mezcla**

  * Usar referencias internas:

    * bounce de la canción hilo conductor;
    * comparación de estribillos;
    * alternancia rápida.
  * Usar balance tonal macro:

    * generador de ruido rosa;
    * filtrado en extremos;
    * HPF en 50 Hz;
    * suavizado o caída en 5 kHz;
    * capturar curva en analizador;
    * comparar la rampa contra la mezcla.
  * Este método se plantea como alternativa empírica a plugins costosos como Tonal Balance Control.
  * Sirve para detectar tendencias groseras de balance espectral, no para reemplazar criterio musical.

## 5. Ejemplos técnicos que no deben perderse

* **Bolero: jerarquía de voz, guitarra y conga**

  * La voz y la guitarra principal ocupan el frente.
  * La conga queda atrás como soporte.
  * Si la conga sube demasiado:

    * el tema se vuelve rítmico;
    * se pierde el clima melancólico;
    * la letra y emoción dejan de mandar.
  * Prueba:

    * mutear la conga;
    * verificar si la canción sigue funcionando;
    * desmutear y evaluar si invade el plano emocional.

* **Elección de consola Neve/Lindell para bolero acústico**

  * En una formación acústica de pocos instrumentos, el docente elige modelado Neve, por ejemplo Lindell 80.
  * Motivos:

    * curvas anchas;
    * musicalidad;
    * color;
    * distorsión armónica;
    * pegamento cálido.
  * Evita SSL en ese contexto porque:

    * es más selectiva;
    * separa más;
    * puede resultar excesiva para un arreglo pequeño;
    * está mejor justificada en sesiones densas de pop/rock de muchas pistas.

* **Ecualización dinámica / matriz Mid/Side para tensión vocal**

  * Problema:

    * en el bolero, los sostenidos vocálicos generan tensión estridente entre 1.3 y 1.5 kHz;
    * bajar medios con EQ estático hunde guitarras acústicas y calidez general.
  * Técnica:

    * armar manualmente matriz M/S;
    * codificar L/R a Mid/Side con S1 MS Matrix o equivalente;
    * dividir a dos auxiliares mono:

      * Mid;
      * Side;
    * volver a sumar a auxiliar estéreo;
    * decodificar M/S;
    * aplicar +6 dB de compensación por caída matemática del ruteo.
  * En Mid:

    * insertar Waves C4;
    * usar banda en zona 1.3 a 1.5 kHz;
    * usar range negativo;
    * ataque hiper-lento, mencionado como 500 ms en la extracción;
    * release aproximado de 300 ms, asociado al largo estadístico de una sílaba;
    * evitar chafar las transientes de la púa de guitarra acústica que convive en el centro;
    * amortiguar solo vocales largas problemáticas.
  * En Side:

    * insertar Pultec EQP-1A;
    * realzar aire y brillo;
    * afectar platos, reverberaciones o guitarras laterales;
    * no hacer más brillante la voz central;
    * mantener la voz opaca, íntima o controlada en el centro.
  * Valor integrador:

    * combina eje frecuencial, dinámico, temporal y espacial;
    * corrige un problema puntual sin desarmar el Mix Bus.

* **Bajo que necesita corte sin subir volumen**

  * Problema:

    * el bajo no se lee suficientemente en mezcla densa.
  * Respuesta:

    * no asumir que hay que ecualizar en 800 Hz;
    * usar compresión para modificar físicamente la envolvente.
  * Herramientas:

    * Smack!;
    * Vertigo VSC-2;
    * compresores tipo FET/VCA.
  * Ajuste:

    * attack lento para dejar pasar la transiente;
    * release rápido;
    * creación de una cresta artificial de ataque;
    * el bajo adquiere clic, agresividad o lectura sin subir volumen masivamente.

* **Ducking multibanda Mid Only de bajo contra bombo**

  * Problema:

    * bombo y bajo compiten en el centro del low-end;
    * ducking clásico bombea todo el bajo;
    * si el bajo tiene chorus o información estéreo, se destruye el movimiento.
  * Técnica:

    * insertar Pro-MB o ecualizador dinámico/multibanda en el bajo;
    * aislar solo la banda de conflicto;
    * usar sidechain externo desde el bombo;
    * configurar la acción en Mid Only;
    * el bombo hunde microscópicamente el centro del bajo;
    * los laterales y modulaciones quedan intactos.

* **Split de bajo / crossover perfecto Linkwitz-Riley**

  * Problema:

    * dividir bajo en graves y agudos para procesarlos por separado puede degradar la suma.
  * Error:

    * usar HPF y LPF estándar en la misma frecuencia;
    * si ambos cortan a -3 dB, la zona de cruce suma +3 dB;
    * aparecen problemas de fase;
    * falla la prueba nula.
  * Procedimiento:

    * duplicar filtros de la misma pendiente en cada rama;
    * construir cruce tipo Linkwitz-Riley;
    * lograr que el punto de cruce quede a -6 dB;
    * activar Fase Lineal obligatoriamente en este caso;
    * comprobar reconstrucción plana o matemáticamente correcta.
  * Matiz:

    * esta recomendación de fase lineal aplica al split/crossover para reconstrucción, no a cualquier fuente transiente.

* **Peligro de fase lineal en guitarra acústica**

  * Problema:

    * picos hirientes o estridentes alrededor de 5 kHz en guitarra acústica.
  * Pregunta:

    * un alumno consulta si conviene usar fase lineal.
  * Corrección:

    * no usar fase lineal bajo ningún punto de vista en ese caso;
    * puede producir pre-ringing;
    * el pre-ringing arruina el ataque de la púa;
    * la solución debe considerar la naturaleza transiente del instrumento.

* **Sample estático de hip hop dividido por bandas**

  * Caso:

    * instrumental o sample *two-track* cerrado, plano y monótono;
    * contiene casi toda la música del track urbano.
  * Procedimiento:

    * rutear canal original a bus ciego/muerto, llamado “trash”;
    * sacar tres envíos pre-fader en ganancia unidad hacia auxiliares:

      * L;
      * M;
      * H.
  * Banda L:

    * pasabajos aproximadamente en 200 Hz;
    * compresión sidechain contra el kick.
  * Banda M:

    * rango aproximado de 200 Hz a 2 kHz;
    * trémolo para movimiento y ritmo;
    * ducking contra el kick;
    * envío a RVerb.
  * Banda H:

    * zona superior a 2 kHz;
    * delays ping-pong.
  * Resultado:

    * una muestra plana adquiere inmersión, groove, amplitud y movimiento.
  * Matiz:

    * es técnica creativa de diseño sonoro; sensible al contexto.

* **Reverb reverse/gated en tambor con sidechain**

  * Objetivo:

    * dar explosividad al tambor.
  * Técnica:

    * crear auxiliar con reverb en modo reverse;
    * insertar compresor a la salida de la reverb;
    * alimentar sidechain con envío directo desde tambor limpio pre-fader.
  * Resultado:

    * el compresor plancha la reverb durante el impacto;
    * el release permite que la reverb suba en los silencios;
    * se evita que la cola ensucie el golpe.

* **Delay/reverb vocal estabilizado por sidechain**

  * Problema:

    * las primeras repeticiones de delay o reverb pueden invadir la transiente de la voz;
    * un compresor estático al final del auxiliar puede reaccionar tarde o no resolver el problema musical.
  * Técnica:

    * delay/reverb en auxiliar;
    * compresor después del efecto;
    * sidechain externo desde pista seca original;
    * mientras la voz canta, el efecto se aplasta;
    * cuando la voz calla, el release levanta el ambiente.
  * Función:

    * mantener inteligibilidad del frente;
    * rellenar huecos sin ensuciar frases.

* **Triggering / refuerzo de bombo con Massey DRT y MIDI**

  * Caso:

    * bombo con bleed excesivo;
    * falta de cuerpo;
    * canal original difícil de reparar.
  * Procedimiento:

    * insertar Massey DRT en modo offline / AudioSuite;
    * ajustar sensibilidad para ignorar bleed de platillos;
    * detectar solo golpes útiles del mazo;
    * limpiar falsos positivos manualmente;
    * exportar a MIDI;
    * conservar velocities naturales;
    * cargar en batería virtual como Perfect Drums;
    * imprimir/renderizar a audio inmediatamente;
    * alinear fase contra micrófono original;
    * revisar con osciloscopio;
    * usar inversión de polaridad si hace falta.
  * Advertencia:

    * no dejar el instrumento virtual vivo;
    * imprimir a audio por preservación.

* **Compuertas en toms con sidechain filtrado**

  * Caso:

    * toms hiper-resonantes o ruidosos;
    * necesidad de acortar sin hacer fades manuales durante horas en un LP de muchos temas.
  * Técnica:

    * insertar compuerta en grupo de toms;
    * usar detector/sidechain interno con filtro pasabanda;
    * afinarlo sobre las fundamentales de los toms;
    * ejemplo conservado: HPF 55 Hz a LPF 110 Hz;
    * la compuerta abre por la madera/tambor;
    * ignora platillazos y basura espectral.
  * Vinculación con eje tridimensional:

    * no se corta necesariamente la resonancia con EQ;
    * se controla cuánto dura.

* **Ducking en overheads para regla 3:1 dinámica**

  * Problema:

    * tambor cercano procesado agresivamente;
    * en overheads entra el bleed natural del tambor;
    * esto genera conflicto tímbrico y de fase;
    * puede aparecer comb filtering.
  * Técnica:

    * insertar compresor en overheads;
    * sidechain desde pista cercana del tambor;
    * hundir momentáneamente overheads más de 9 dB cuando ataca el tambor.
  * Justificación:

    * se fuerza artificialmente una diferencia de nivel compatible con regla 3:1;
    * el problema de fase se vuelve acústica y matemáticamente despreciable;
    * evita tener que desalinear milimétricamente pistas.

* **Denoising con Waves X-Noise**

  * Caso:

    * ruido constante de amplificador o guitarra acústica.
  * Procedimiento:

    * buscar un tramo donde el ruido esté completamente solo;
    * activar Learn;
    * desactivar Learn en medio del loop para no capturar clics de salto;
    * revisar en modo Difference.
  * Advertencia:

    * no intentar borrar todo el ruido;
    * no subir threshold agresivamente;
    * riesgo de comerse transientes;
    * riesgo de artefactos artificiales.

* **Ruido rosa filtrado para diagnóstico macro**

  * Técnica:

    * insertar generador de ruido rosa;
    * filtrar extremos;
    * HPF en 50 Hz;
    * suavizado en 5 kHz;
    * capturar curva en analizador;
    * comparar mezcla contra esa rampa.
  * Uso:

    * diagnosticar balance tonal general;
    * detectar tendencias groseras;
    * no sustituye criterio de mezcla.

## 6. Preguntas de estudiantes que sí aportan contenido

* **¿La guitarra adelante y la conga atrás es gusto personal o referencia obligatoria del género?**

  * Contexto:

    * bolero melódico;
    * guitarra acústica al frente;
    * conga al fondo.
  * Aporte doctrinal:

    * el docente aclara que es decisión conceptual;
    * si la percusión queda adelante, la canción se vuelve rítmica o bailable;
    * eso puede destruir la tristeza, melancolía o intención lírica.
  * Clase fuente:

    * Clase 21, Bloque 2.

* **¿Conviene usar fase lineal para corregir frecuencias hirientes de guitarra acústica?**

  * Contexto:

    * frecuencia estridente alrededor de 5 kHz;
    * guitarra acústica o cuerda pulsada con transiente rápida.
  * Respuesta:

    * no conviene activar fase lineal en ese caso;
    * el pre-ringing puede arruinar el ataque de la púa;
    * evitar convertir la solución en un daño mayor.
  * Clase fuente:

    * Clase 21, Bloque 9.

* **¿Cuál es la diferencia entre mandar todo al Master Fader y crear un Mix Bus auxiliar previo?**

  * Aporte:

    * el Mix Bus auxiliar permite trabajar profesionalmente antes del Master Fader;
    * sirve para imprimir stems;
    * permite envíos paralelos de la mezcla entera;
    * admite inserción de procesos analógicos o procesos de mezcla.
  * Matiz:

    * el Master Fader puede reservarse para medición y análisis;
    * medidores LUFS o analizadores no necesariamente deben imprimirse.
  * Clase fuente:

    * Clase 24, Bloque 20.

* **¿No sería más rápido poner un 1176 directamente en el bus de guitarras?**

  * Contexto:

    * dos tomas de guitarra acústica;
    * necesidad de controlar picos.
  * Respuesta:

    * si se comprime el grupo, un pico de la izquierda aplasta también la derecha;
    * eso castiga señales sanas;
    * primero se controlan picos por pista;
    * luego se aplica glue grupal.
  * Clase fuente:

    * Clase 23, Bloque 6;
    * reforzado en Clase 24, Bloque 2.

* **¿Qué hacer si el artista trae un instrumental descargado de YouTube ya limitado y recortado a 0 dBFS?**

  * Contexto:

    * type beat o instrumental robado/descargado;
    * pista ya aplastada, limitada o recortada.
  * Respuesta:

    * para sumar voces y mezclar, hay que bajarla con trim;
    * ejemplo conservado: -18 dBFS;
    * el objetivo es recuperar margen operativo dentro de la consola virtual antes de enviarla al Mix Bus.
  * Clase fuente:

    * Clase 23, Bloque 30.

* **¿Duplicar una pista mono y retrasarla con Sample Delay reemplaza un doubling real?**

  * Respuesta:

    * no;
    * eso crea falso estéreo;
    * produce filtro peine fijo;
    * al colapsar a mono se evidencia la cancelación;
    * el doubling real exige tocar o cantar dos veces.
  * Clase fuente:

    * Clase 23, Bloque 10;
    * relacionado con Clase 21, Bloques 14/15.

* **¿La misma reverb para todos no hace que suenen en el mismo cuarto?**

  * Respuesta:

    * ese dogma se corrige;
    * la profundidad se construye por contraste entre recintos;
    * una reverb única puede convertirse en sopa;
    * se pueden usar ambientes distintos para batería/bajo, guitarras y voz.
  * Clase fuente:

    * Clase 24, Bloque 7;
    * relacionado con Clase 21, Bloque 7.

* **¿Es incorrecto barrer con +10 dB para buscar una frecuencia?**

  * Contexto:

    * crítica purista a ecualizar sumando mucho.
  * Respuesta del profesor:

    * “Si eso es un error, bienvenido al error”.
    * El barrido exagerado sirve para que la frecuencia dé un paso al frente.
    * Luego se vuelve a una atenuación o realce moderado.
  * Clase fuente:

    * Clase 21, Bloque 10;
    * relacionado con Clase 12 y Clase 13.

## 7. Advertencias, matices y correcciones del profesor

* **No mezclar bajo cinco criterios distintos**

  * Bandas autoproducidas:

    * cada integrante pide prioridad para su instrumento;
    * el ingeniero queda atrapado entre órdenes cruzadas.
  * Advertencia:

    * la mezcla se desarma si responde a cinco direcciones simultáneas.
  * Criterio:

    * exigir una única figura de producción;
    * una sola voz cantante;
    * una sola dirección artística.
  * Frase preservada:

    * “Es mejor ir detrás de una idea equivocada que detrás de cinco ideas correctas pero diferentes”.

* **Exceso de reverb hunde la mezcla**

  * Diagnóstico de trabajos prácticos de alumnos:

    * error repetido: abuso de colas largas e indiscriminadas.
  * Problema:

    * si la reverb no respeta el tempo o figura musical, asfixia golpes posteriores;
    * empuja todo hacia atrás;
    * reduce ataque;
    * reduce definición;
    * la canción “se hunde”.
  * Matiz:

    * no se condena la reverb;
    * se condena su exceso y falta de integración temporal.

* **No usar fase lineal de manera indiscriminada**

  * En crossover Linkwitz-Riley de bajo:

    * fase lineal se exige para reconstrucción matemática del split.
  * En guitarra acústica/transientes:

    * fase lineal puede introducir pre-ringing;
    * el ataque de púa puede arruinarse.
  * Este punto debe formularse con precisión:

    * fase lineal no es “mejor siempre”;
    * su conveniencia depende del material y objetivo.

* **No hacer ecualización contextual en Solo**

  * La ecualización para hacer espacio a otro instrumento debe decidirse en contexto.
  * Escuchar en Solo puede hacer parecer incorrecto un recorte que en mezcla es necesario.
  * Ejemplo:

    * recorte de guitarra rítmica alrededor de 280–285 Hz;
    * sola parece débil;
    * en mezcla deja espacio al bajo.

* **No poner HPF en el master “por las dudas”**

  * Problemas:

    * fase global;
    * overshot;
    * picos espurios;
    * basura subsónica arrastrada por todo el sistema;
    * subgrupos contaminados.
  * Criterio:

    * limpiar al inicio y por canal.

* **No convertir más plugins en mejor mezcla**

  * Si el problema exige parches interminables:

    * revisar arreglo;
    * revisar grabación;
    * revisar fuente;
    * revisar micrófono;
    * revisar sala.
  * La mezcla no reemplaza una buena producción.

* **No exagerar denoising**

  * X-Noise y herramientas similares necesitan perfil de ruido estable.
  * Usarlas agresivamente puede:

    * comerse transientes;
    * generar artefactos;
    * volver artificial el instrumento.
  * Criterio:

    * reducir, no mutilar.

* **No dejar proyectos atados a instrumentos virtuales**

  * Riesgos:

    * actualizaciones del sistema operativo;
    * vencimiento de licencias;
    * plugins no disponibles en el futuro;
    * imposibilidad de abrir sesión años después.
  * Regla:

    * imprimir a audio;
    * ocultar/inactivar MIDI;
    * preservar respaldo sin depender de él para reproducción inmediata.

* **No consolidar después de Strip Silence si se quiere ahorrar CPU**

  * Dynamic Plugin Processing puede apagar plugins cuando no hay audio.
  * Strip Silence crea vacíos útiles.
  * Si se consolida todo en un bloque continuo:

    * desaparecen los silencios;
    * el motor procesa durante todo el track;
    * se pierde optimización.

* **No crear loops con efectos en subgrupos**

  * Si una reverb de tambor:

    * recibe envío del tambor;
    * vuelve al mismo grupo que alimenta;
    * puede generar feedback o acople destructivo.
  * Los FX paralelos deben volver a una etapa posterior.

* **No confundir falso estéreo con producción estéreo real**

  * Duplicar y retrasar una pista mono:

    * no es doubling;
    * genera comb filtering fijo;
    * falla al colapsar a mono.
  * Doblar implica nueva interpretación humana.

* **No aplastar la mezcla antes del mastering**

  * La mezcla requiere relación saludable entre picos y promedio.
  * Referencia PLR:

    * 13 a 15 LU para Pop/Rock según la extracción.
  * Aplastar picos para RMS:

    * reduce impacto;
    * compromete la mezcla antes del mastering.

* **No hacer “mezcla Tetris” y luego pedir glue**

  * Aislar todo con filtros abruptos puede destruir la interacción.
  * El glue no se soluciona solo con compresor de bus.
  * La integración debe empezar en decisiones de filtrado, balance y arreglo.

* **Valores numéricos sensibles al contexto**

  * Los siguientes valores deben conservarse, pero no convertirse en leyes universales:

    * HPF 70 Hz en conga del bolero;
    * HPF 45 Hz en guitarra base;
    * HPF 160 Hz y LPF 14 kHz en guitarra de arreglo;
    * HPF 160 Hz en voz;
    * regla visual de 1/3 de forma de onda;
    * picos alrededor de -6 dBFS;
    * promedios -18/-20 dBFS;
    * release vocal aproximado de 300 ms;
    * rango 1.3 a 1.5 kHz para tensión de esa voz específica;
    * ataque 500 ms en C4 del caso M/S;
    * ducking de overheads mayor a 9 dB en el ejemplo de regla 3:1 dinámica;
    * filtro pasabanda 55–110 Hz para detector de toms en el ejemplo;
    * ruido rosa con HPF 50 Hz y suavizado 5 kHz.

## 8. Herramientas, referencias técnicas, configuraciones y detalles operativos

* **Pro Tools / Import Session Data**

  * Uso:

    * trasladar estructura de mezcla de una canción a otra;
    * conservar mixer, ruteos, subgrupos, niveles base, EQs y compresión grupal.
  * Aplicación:

    * álbum;
    * canción hilo conductor;
    * comparación con bounce del tema 1.

* **Save Session Copy In**

  * Uso final:

    * crear copia de sesión limpia;
    * incluir solo archivos usados;
    * preservar entregable ordenado.

* **Strip Silence**

  * Uso:

    * eliminar silencios;
    * crear fades pequeños;
    * facilitar Dynamic Plugin Processing.
  * Advertencia:

    * no consolidar después si se busca ahorro de CPU.

* **Dynamic Plugin Processing**

  * Función:

    * reducir consumo DSP/CPU cuando no hay audio en el clip.
  * Condición:

    * requiere silencios reales en la línea de tiempo.

* **Lindell / Neve 1073 / 1084 / 2254**

  * Modelado TMT mencionado.
  * Uso:

    * consola para bolero/acústico;
    * color;
    * curvas anchas;
    * pegamento.
  * Lindell/Neve 2254:

    * compresión lenta de grupo;
    * glue con 1–2 dB de reducción.

* **SSL**

  * Útil para:

    * mezclas densas;
    * selectividad;
    * precisión paramétrica.
  * En el flujo SSL:

    * activar Split;
    * ruta: entrada → filtros → dinámica → EQ.

* **1176**

  * Uso:

    * compresión individual rápida;
    * caza de picos;
    * antes de enviar al grupo.
  * No usar como primera respuesta en el bus grupal si los picos pertenecen a tomas individuales.

* **LA-2A**

  * Uso:

    * compresión lenta;
    * glue grupal;
    * reducción ligera.

* **Smack! / Vertigo VSC-2**

  * Uso:

    * modificar envolvente del bajo;
    * attack lento;
    * release rápido;
    * crear lectura sin subir volumen.

* **Pro-MB**

  * Uso:

    * ducking multibanda;
    * sidechain externo desde bombo;
    * operación Mid Only para conservar laterales del bajo.

* **Waves C4**

  * Descrito como híbrido multibanda derivado de lógica tipo RComp.
  * Uso:

    * matriz Mid;
    * tensión vocal 1.3 a 1.5 kHz;
    * range negativo;
    * ataque muy lento/500 ms;
    * release 300 ms;
    * no aplastar transientes de guitarra.

* **Pultec EQP-1A**

  * Uso:

    * canal Side de matriz M/S;
    * aire;
    * brillo;
    * platos;
    * reverbs/guitarras laterales;
    * evitar afectar la voz central.

* **S1 MS Matrix / matriz Mid/Side**

  * Procedimiento:

    * codificar L/R a M/S;
    * dividir Mid y Side por buses;
    * procesar por separado;
    * volver a estéreo;
    * decodificar;
    * compensar +6 dB por caída matemática.

* **Waves X-Noise**

  * Procedimiento:

    * capturar perfil con Learn;
    * usar tramo de ruido solo;
    * desactivar Learn en medio del loop;
    * revisar modo Difference.
  * Advertencia:

    * no erradicar todo el ruido si destruye transientes.

* **Massey DRT**

  * Uso:

    * análisis offline de transientes;
    * conversión a MIDI;
    * triggering de batería.
  * Asociado a:

    * Perfect Drums;
    * velocities naturales;
    * commit a audio;
    * alineación de fase.

* **Perfect Drums**

  * Uso:

    * instrumento virtual para disparar samples desde MIDI.
  * Advertencia:

    * imprimir a audio;
    * no dejar sesión dependiente del plugin.

* **Blue Lab BL Sample Delay**

  * Uso:

    * retardador manual por muestras o milisegundos;
    * insertado antes de reverbs de ambiente en auxiliares individuales;
    * fabricación de profundidad o predelay manual diferenciado por instrumento.
  * Diferenciar de falso estéreo destructivo:

    * como predelay de ambiente cumple función espacial;
    * duplicar una pista mono y retrasarla para simular estéreo genera filtro peine.

* **RVerb**

  * Mencionado en apertura por bandas de sample hip hop.
  * En banda media:

    * envío a RVerb como parte del diseño de movimiento e inmersión.

* **Delays ping-pong**

  * Uso:

    * banda alta del sample;
    * generar amplitud y movimiento.

* **Reverb reverse/gated**

  * Uso:

    * tambor;
    * explosividad;
    * compresión sidechain desde tambor seco.

* **Ruido rosa filtrado**

  * Configuración:

    * generador de ruido rosa;
    * HPF 50 Hz;
    * suavizado en 5 kHz;
    * captura de curva en analizador.
  * Uso:

    * diagnóstico macro de balance tonal.

* **Medidores de correlación / colapso mono**

  * Uso:

    * diagnosticar falso estéreo;
    * comprobar filtro peine;
    * revisar monocompatibilidad.

* **Osciloscopio e inversión de polaridad**

  * Uso:

    * alinear sample disparado con micrófono original;
    * verificar fase en refuerzo de batería.

* **Valores y referencias operativas preservadas**

  * -18 dBFS:

    * calibración de consola virtual hacia +4 dBu / 0 VU.
  * 1/3 de forma de onda:

    * regla visual de headroom.
  * Picos alrededor de -6 dBFS:

    * consecuencia aproximada del criterio visual.
  * Promedios -18/-20 dBFS:

    * referencia operativa contextual.
  * +10 dB:

    * barrido aditivo para localizar frecuencias.
  * 1.3 a 1.5 kHz:

    * tensión vocal del bolero.
  * 5 kHz:

    * zona hiriente de guitarra acústica en ejemplo.
  * 300 ms:

    * release estadístico de sílaba humana.
  * 500 ms:

    * ataque hiper-lento del C4 en matriz Mid.
  * +6 dB:

    * compensación de matriz M/S.
  * -6 dB:

    * punto de cruce Linkwitz-Riley.
  * +3 dB:

    * realce espurio al sumar filtros estándar a -3 dB.
  * > 9 dB:

    * ducking de overheads para forzar regla 3:1 dinámica.
  * 55–110 Hz:

    * ejemplo de detector pasabanda para toms.
  * 200 Hz:

    * división aproximada de banda Low en sample.
  * 2 kHz:

    * límite superior de banda Mid e inicio de High en ejemplo.
  * 14 kHz:

    * LPF contextual en guitarra de arreglo del bolero.
  * 70 Hz, 45 Hz, 160 Hz:

    * HPF contextuales del bolero.

## 9. Contenido dislocado que sí pertenece a M07

* **Clase 6 — Bus vs. auxiliar**

  * El bus es la ruta interna, el cable invisible.
  * El auxiliar es el canal de destino.
  * Este contenido es esencial para entender:

    * envíos;
    * retornos;
    * subgrupos;
    * matrices;
    * arquitectura de efectos;
    * Mix Bus.

* **Clase 6 — Ruteo de reverbs y peligro de loop**

  * Si la reverb de tambor vuelve al mismo grupo que la alimenta, puede producir feedback destructivo.
  * Los efectos paralelos deben volver a una etapa posterior:

    * Mix de Batería;
    * Mix Bus global.
  * Pertenece a M07 porque define plomería interna obligatoria de mezcla.

* **Clase 6 — Envíos pre-fader para alejamiento**

  * Corrige el dogma de que todo envío temporal debe ser post-fader.
  * En pre-fader:

    * baja el canal seco;
    * la reverb permanece;
    * el objeto se aleja perceptualmente.
  * Pertenece a M07 como automatización creativa de profundidad.

* **Clase 7 — PLR / Factor de Cresta**

  * La mezcla no se mide solo por RMS.
  * PLR conserva relación entre pico y promedio.
  * Referencia Pop/Rock:

    * 13 a 15 LU.
  * Pertenece a M07 porque impacta decisiones de compresión y nivel antes de mastering.

* **Clase 10 — Ducking de overheads y regla 3:1 dinámica**

  * Resuelve conflicto de fase/bleed entre tambor cercano y overheads.
  * Sidechain desde tambor al compresor en overheads.
  * Ducking >9 dB para volver despreciable el conflicto.
  * Pertenece a M07 como integración de fase, dinámica y ruteo.

* **Clase 11 — Crítica a la mezcla Tetris**

  * Aislar todo con filtros abruptos destruye interacción.
  * Luego pedir glue en el bus es contradictorio.
  * Pertenece a M07 como doctrina estética y arquitectónica de mezcla.

* **Clase 12 — Ecualización contextual prohibida en Solo**

  * El tercer motivo para filtrar es hacer lugar a otro instrumento.
  * Debe decidirse escuchando la mezcla completa.
  * Pertenece a M07 porque es mezcla real, no tratamiento aislado.

* **Clase 12 — HPF en master por las dudas**

  * Advertencia contra filtrado automático en Master.
  * Limpieza debe hacerse canal por canal.
  * Pertenece a M07 porque afecta arquitectura general y fase global.

* **Clase 12 — Ruido rosa filtrado**

  * Diagnóstico macro-espectral barato.
  * HPF en 50 Hz y suavizado en 5 kHz.
  * Pertenece a M07 como chequeo global de mezcla.

* **Clase 12 y Clase 13 — Límite de la mezcla**

  * Si se necesitan docenas de notches, el problema puede ser de arreglo o grabación.
  * La mezcla no corrige una mala partitura.
  * Pertenece a M07 como criterio de costo/beneficio y frontera técnica.

* **Clase 21 — Bolero, planos y consola**

  * Núcleo práctico de jerarquía musical.
  * Voz/guitarra al frente, conga atrás.
  * Neve/Lindell para color y pegamento.
  * Pertenece directamente a la práctica integradora.

* **Clase 22 — Batería, triggering, gates, reverb**

  * Refuerzo por capas;
  * compuertas con detector filtrado;
  * exceso de reverb;
  * gestión de recursos;
  * instrumentos virtuales impresos.
  * Pertenece directamente a M07.

* **Clase 23 — Bajo, sample, falso estéreo, denoising**

  * Bajo con envolvente alterada;
  * ducking Mid Only;
  * apertura por bandas de sample;
  * falso estéreo vs doubling;
  * X-Noise;
  * type beats a 0 dBFS.
  * Pertenece a M07 por resolución de casos reales de mezcla.

* **Clase 24 — Grupos, envíos, Mix Bus, Linkwitz-Riley**

  * Orden dinámico individual → grupo;
  * envíos a 0 dB;
  * sidechain en delays;
  * diferencia Mix Bus/Master Fader;
  * split de bajo;
  * limpieza de sesión.
  * Pertenece directamente a M07.

* **Clase 25 — Método del edificio**

  * Aunque aparece en transición a mastering, define cómo mezclar un álbum completo.
  * Import Session Data;
  * canción hilo conductor;
  * comparación con bounce;
  * continuidad sonora.
  * Pertenece a M07 como workflow estructural.

* **Clase 28 — Matriz Mid/Side híbrida**

  * Aunque aparece en cierre práctico/final, funciona como máxima intervención de mezcla:

    * tensión vocal;
    * Waves C4 en Mid;
    * Pultec en Side;
    * +6 dB de compensación;
    * resolución sin destruir cohesión.
  * Pertenece a M07 como caso avanzado de integración.

## 10. Mapa de cobertura

* **Workflow de mezcla completo**

  * Método del edificio.
  * Canción hilo conductor.
  * Import Session Data.
  * Bounce de referencia dentro de la siguiente sesión.
  * Comparación de estribillos.
  * Ajuste canción por canción sin perder sonido de álbum.
  * Save Session Copy In al final.

* **Orden de decisiones**

  * Definir dirección artística.
  * Asegurar una única voz de producción.
  * Preparar sesión y ruteo.
  * Ajustar gain staging.
  * Limpiar canales.
  * Determinar jerarquía de planos.
  * Diagnosticar problemas por eje:

    * tiempo;
    * nivel;
    * frecuencia.
  * Procesar individual antes que grupo cuando corresponda.
  * Diseñar espacialidad.
  * Chequear fase, mono, balance tonal y continuidad.
  * Archivar sesión de forma robusta.

* **Criterios para intervenir o no intervenir**

  * No procesar por costumbre.
  * No usar EQ si el problema es duración.
  * No usar fase lineal si destruye transientes.
  * No borrar todo el bleed si aporta realidad.
  * No eliminar todo el ruido si mutila el instrumento.
  * No hacer notches infinitos si el problema es de arreglo/grabación.
  * No aplastar el PLR por competitividad prematura.
  * No corregir en Solo problemas que pertenecen al contexto.

* **Mezcla técnica vs. mezcla artística**

  * Técnica:

    * ruteo;
    * fase;
    * filtros;
    * dinámica;
    * sidechain;
    * M/S;
    * CPU;
    * archivo.
  * Artística:

    * jerarquía emocional;
    * planos;
    * género;
    * tristeza vs. baile;
    * color de consola;
    * decisión de profundidad;
    * continuidad de álbum.
  * El módulo muestra que la técnica se subordina al concepto, no al revés.

* **Priorización de problemas**

  * Primero:

    * dirección artística;
    * arreglo;
    * grabación;
    * balance;
    * plano.
  * Luego:

    * correcciones técnicas;
    * dinámica;
    * EQ;
    * ruteo avanzado;
    * efectos.
  * Si la base está mal, más plugins no garantizan solución.

* **Balances, jerarquía y contexto**

  * La conga del bolero es el ejemplo principal.
  * La guitarra que se recorta para dejar bajo es ejemplo de EQ contextual.
  * El bajo que necesita lectura se corrige con envolvente.
  * La voz tensa se corrige con M/S y dinámica multibanda.
  * Los samples planos se expanden por bandas.

* **Integración de módulos anteriores**

  * M02 / flujo de señal:

    * buses;
    * auxiliares;
    * Mix Bus;
    * gain staging.
  * M03 / fase:

    * falso estéreo;
    * triggering;
    * overheads;
    * Linkwitz-Riley.
  * M04 / filtros y EQ:

    * filtros contextuales;
    * HPF por canal;
    * barrido +10 dB;
    * ruido rosa.
  * M05 / dinámica:

    * compresión individual/grupo;
    * gates;
    * sidechain;
    * ducking Mid Only.
  * M06 / espacialidad:

    * reverbs diferenciadas;
    * predelay manual;
    * envíos pre-fader;
    * profundidad por planos.
  * M07:

    * uso integrado de todo lo anterior en decisiones reales.

* **Errores comunes al mezclar por etapas**

  * Mezclar cada canción de álbum desde cero.
  * Responder a todos los miembros de una banda.
  * Ecualizar en Solo.
  * Poner HPF en master por costumbre.
  * Usar fase lineal como solución universal.
  * Insertar compresor de grupo para picos individuales.
  * Hacer falso estéreo con Sample Delay.
  * Usar denoiser agresivo.
  * Excederse con reverb.
  * Consolidar pistas tras Strip Silence.
  * Dejar instrumentos virtuales vivos.
  * Rutar reverbs de vuelta al grupo que las alimenta.
  * Usar filtros abruptos y luego pedir glue.

* **Comparación con referencias**

  * Referencia interna de álbum:

    * bounce del primer tema.
  * Referencia macro-espectral:

    * curva de ruido rosa filtrado.
  * Referencia de medición:

    * PLR;
    * LUFS/medidores en Master Fader;
    * correlación mono para falso estéreo.
  * Referencia de género:

    * bolero melancólico;
    * pop moderno limpio;
    * rock orgánico con bleed;
    * hip hop con sample estático.

* **Toma de decisiones por costo/beneficio**

  * Si la corrección destruye más de lo que arregla, no conviene.
  * Ejemplos:

    * borrar ruido hasta destruir transientes;
    * fase lineal que evita rotación pero introduce pre-ringing;
    * EQ estático que baja tensión vocal pero hunde guitarras;
    * ducking estándar que despeja bombo pero destruye bajo estéreo;
    * filtros abruptos que limpian pero eliminan pegamento;
    * notches infinitos que maquillan una mala grabación.

* **Estrategias de chequeo final de mezcla**

  * Mutear elementos secundarios para verificar plano.
  * Colapsar a mono para detectar falso estéreo.
  * Usar correlación.
  * Hacer prueba nula en splits/crossovers.
  * Comparar con bounce de canción hilo conductor.
  * Revisar PLR.
  * Revisar balance tonal con ruido rosa filtrado.
  * Reservar Master Fader para medición cuando aplique.
  * Imprimir instrumentos virtuales.
  * Limpiar sesión y guardar copia final.

## 11. Trazabilidad principal por clases

* **Clase 6**

  * Bus vs. auxiliar.
  * Peligro de loops al rutear reverbs hacia subgrupos que las alimentan.
  * Envíos pre-fader para efecto de alejamiento.
  * Arquitectura de efectos y plomería interna.

* **Clase 7**

  * PLR / Peak to Loudness Ratio.
  * Factor de Cresta.
  * Referencia Pop/Rock de 13 a 15 LU.
  * Advertencia contra aplastar picos por RMS.

* **Clase 10**

  * Ducking en overheads.
  * Sidechain desde tambor cercano.
  * Hundimiento mayor a 9 dB.
  * Regla 3:1 dinámica para reducir relevancia de conflicto de fase.

* **Clase 11**

  * Crítica a la “mezcla Tetris”.
  * Pendientes abruptas 24 a 96 dB/octava.
  * Contradicción entre aislar todo y luego buscar glue en el Mix Bus.
  * Pegamento como interacción previa, no solo compresión final.

* **Clase 12**

  * Filtrado contextual.
  * Prohibición de decidir en Solo.
  * Recorte de guitarra rítmica alrededor de 280–285 Hz para dejar espacio al bajo.
  * Advertencia contra HPF automático en Master.
  * Ruido rosa filtrado:

    * HPF 50 Hz;
    * suavizado 5 kHz;
    * curva de referencia.
  * Límite de la mezcla ante problemas de arreglo/grabación.

* **Clase 13**

  * Refuerzo de la idea de que una mala partitura o mala grabación no se arregla con mezcla.
  * Crítica a exceso de notches y cirugía permanente.
  * Relación con preproducción y arreglo.

* **Clase 21**

  * Bolero como caso integrador.
  * Jerarquía de planos:

    * voz y guitarra al frente;
    * conga atrás.
  * Pregunta sobre gusto personal vs. género.
  * Elección de Neve/Lindell sobre SSL en arreglo acústico.
  * Calibración:

    * -18 dBFS hacia +4 dBu / 0 VU.
  * Valores contextuales de filtros:

    * conga HPF 70 Hz;
    * guitarra base HPF 45 Hz;
    * guitarra arreglo HPF 160 Hz y LPF 14 kHz;
    * voz HPF 160 Hz.
  * Gestión de bandas autoproducidas.
  * Reverbs diferenciadas.
  * Compresión de efectos por sidechain.
  * Advertencia sobre fase lineal en guitarra.
  * Barrido +10 dB y frase “bienvenido al error”.
  * Blue Lab BL Sample Delay como predelay manual.
  * Doubling real vs. falso estéreo.

* **Clase 22**

  * Revisión de prácticas de alumnos.
  * Advertencia contra exceso de reverb.
  * Regla visual de headroom:

    * 1/3 del alto vertical;
    * picos alrededor de -6 dBFS;
    * promedios -18/-20 dBFS.
  * Massey DRT:

    * análisis offline;
    * sensibilidad;
    * detección de bombo;
    * MIDI;
    * Perfect Drums;
    * commit a audio;
    * alineación de fase.
  * No dejar instrumentos virtuales vivos.
  * Control de toms con compuertas y detector filtrado.
  * Problema tridimensional:

    * tiempo;
    * nivel;
    * frecuencia.
  * Bleed pop vs. rock.
  * Reverb reverse/gated con sidechain.
  * Ruteo SSL con Split:

    * entrada;
    * filtros;
    * dinámica;
    * EQ.

* **Clase 23**

  * Bajo con attack lento y release rápido mediante Smack! o Vertigo VSC-2.
  * Ducking Mid Only de bajo contra bombo con Pro-MB.
  * Pregunta sobre compresión de grupo vs. individual en guitarras.
  * X-Noise:

    * Learn;
    * Difference;
    * advertencia contra threshold excesivo.
  * Falso estéreo vs. doubling real.
  * Sample hip hop por bandas:

    * bus trash;
    * envíos pre-fader;
    * Low/Mid/High;
    * sidechain contra kick;
    * trémolo;
    * RVerb;
    * delays ping-pong.
  * Type beat limitado a 0 dBFS:

    * bajar con trim, ejemplo -18 dBFS.

* **Clase 24**

  * Import Session Data reforzado como flujo de álbum.
  * Gestión de CPU:

    * Strip Silence;
    * Dynamic Plugin Processing;
    * no consolidar.
  * Compresión individual antes de grupo:

    * 1176 individual;
    * LA-2A/Lindell 2254 grupal;
    * 1–2 dB de reducción.
  * Envíos a efectos en ganancia unidad 0 dB cuando el efecto atiende una sola pista.
  * Reverbs diferenciadas por plano.
  * Delay vocal con compresor sidechain desde voz seca.
  * Split de bajo Linkwitz-Riley:

    * evitar filtros estándar a -3 dB;
    * cruce a -6 dB;
    * fase lineal;
    * prueba nula.
  * Limpieza de I/O.
  * Save Session Copy In.
  * Mix Bus auxiliar vs. Master Fader.
  * Grupos mono vs. estéreo:

    * redoblante top/bottom mono;
    * toms estéreo.

* **Clase 25**

  * Método del edificio para álbum.
  * Canción hilo conductor.
  * Import Session Data.
  * Bounce del tema 1 como referencia.
  * Continuidad de disco.
  * Reaparición del problema de autoproducción y necesidad de una sola dirección.

* **Clase 28**

  * Diagnóstico de tensión vocal mediante barrido.
  * Zona 1.3 a 1.5 kHz.
  * Matriz M/S manual:

    * codificación;
    * Mid;
    * Side;
    * decodificación;
    * +6 dB.
  * Waves C4 en Mid:

    * range negativo;
    * attack 500 ms;
    * release 300 ms.
  * Pultec EQP-1A en Side.
  * Integración avanzada de dinámica, frecuencia y espacialidad para corregir mezcla sin destruir cohesión.
