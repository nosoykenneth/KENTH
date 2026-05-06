---

course_id: mezcla_masterizacion_kenth
module_id: M08
module_order: 8
module_title: Masterización y optimización comercial
module_slug: masterizacion-optimizacion-comercial
doc_type: source_dossier
source_origin: author_compiled_from_transcripts
filename: M08_dossier_fuente.md
version: 0.1
status: draft_source_compilation
curation_source: extraccion_exhaustiva_notebooklm_desde_clases_definitivas
ready_for_indexing: false
-------------------------

# M08 — Dossier fuente exhaustivo

## Masterización y optimización comercial

> Este documento NO es guia canonica.
> NO es FAQ.
> NO es glosario final.
> Es una fuente intermedia exhaustiva, reorganizada por modulo, construida a partir de clases definitivas corregidas.
> Su objetivo es preservar detalle, matices, ejemplos, advertencias y trazabilidad antes de condensar doctrina para el RAG.

## 1. Alcance del dossier

* Este dossier integra como núcleo principal los desarrollos de **Clase 25, 26 y 27**, donde se concentra la explicación formal del mastering, su lógica comercial, sus problemas típicos y su resolución operativa.
* También incorpora contenido que apareció fuera del bloque principal de mastering pero que pertenece claramente al módulo por función o por objetivo:

  * **Clase 5:** LUFS, ponderación K, normalización de Spotify, diferencia entre normalización y compresión, uso de clippers para preparar loudness desde mezcla.
  * **Clase 6 y Clase 24:** advertencia sobre no bajar el master fader para “entregar a -6 dB”.
  * **Clase 7:** PLR / factor de cresta como criterio de salud dinámica.
  * **Clase 8:** delimitación entre medidores de loudness para mastering y medidores de pico/RMS para gain staging de mezcla.
  * **Clase 9:** monocompatibilidad y low-end estéreo con destino vinilo.
  * **Clase 12 y 13:** criterios de diagnóstico tonal y ecualización macro suave aplicables a mastering.
  * **Clase 14:** tensión entre norma técnica de True Peak y decisiones comerciales/agresivas de la industria.
  * **Clase 19:** compresión ascendente y ecualización dinámica sobre mezcla estéreo completa.
  * **Clase 21 y Clase 28:** oversampling previo al bounce final y control de pureza matemática antes de masterizar.
* El material preserva:

  * definición de mastering,
  * distinción mezcla/mastering,
  * etapa técnica, comercial y artística,
  * traducción y entrega comercial,
  * loudness, LUFS, normalización, True Peak,
  * limitación, dither, noise shaping,
  * correcciones de fase, asimetría, DC offset, subsónicas,
  * herramientas, configuraciones, procedimientos y advertencias.
* El dossier no presupone que todas las recomendaciones sean universales:

  * cuando el material presenta valores dependientes del género, del contexto de entrega o de la intención comercial, eso se conserva como recomendación contextual y no como ley absoluta.

## 2. Núcleo conceptual del módulo

* **Masterizar = preparar un producto para su distribución.**

  * Definición de vieja escuela repetida como doctrina central.
  * El proceso se presenta en **tres etapas**:

    * **Etapa técnica:** revisar y corregir problemas que sobrevivieron a la mezcla, como:

      * nivel,
      * fase,
      * espectro,
      * subsónicas,
      * resonancias,
      * DC offset,
      * asimetrías,
      * desequilibrios macrotonales,
      * problemas de low-end o monocompatibilidad.
    * **Etapa comercial:** llevar el producto a un nivel competitivo de loudness y adaptarlo al formato de distribución real.
    * **Etapa artística:** aportar color, cohesión, redondez o “pegamento” final, solo si hace falta; no es obligatoria si la mezcla ya llegó resuelta.
* **La función del mastering no es rehacer la mezcla.**

  * El mastering trabaja sobre el total estéreo.
  * Puede poner “parches” a una mala mezcla, pero no reemplaza decisiones de producción o mezcla que debieron resolverse antes.
  * El profesor lo expresa como corrección de un malentendido estructural: si el problema real está “antes” en la cadena, el mastering no lo arregla mágicamente.
* **Mastering como trabajo de traducción final.**

  * El objetivo no es solo que “suene lindo” en el estudio.
  * El producto debe sostenerse en distribución real:

    * plataformas,
    * códecs con pérdida,
    * consumidores con normalización activada o desactivada,
    * diferentes sistemas de reproducción,
    * posibles exigencias de formato físico.
* **Loudness moderno medido en LUFS.**

  * LUFS = *Loudness Units relative to Full Scale*.
  * La medición usa **Ponderación K**, que da más peso a medios-altos y agudos para aproximarse a la percepción humana.
  * 1 LU equivale a 1 dB, pero en un marco perceptual ponderado.
  * La métrica relevante para plataformas es el **LUFS Integrado**, es decir, el promedio de la canción completa.
* **Normalización de plataformas.**

  * Spotify aparece como caso principal:

    * transmite en torno a **-14 LUFS integrados**,
    * aplica **normalización de ganancia**,
    * no aplica compresión de rango dinámico al archivo por el solo hecho de normalizar.
  * Distinción doctrinal:

    * una cosa es **compresión de datos** (WAV a AAC/OGG/MP3),
    * otra cosa es **normalización de ganancia**.
* **True Peak como criterio comercial real.**

  * La medición de muestra digital no alcanza por sí sola.
  * El mastering debe contemplar picos interesample y el rebote de reconstrucción analógica/codificación.
  * El margen técnico repetido como referencia es **-1 dBTP** para streaming, precisamente porque la codificación con pérdida puede elevar picos y provocar clipping.
* **Álbum vs canción.**

  * El mastering de una canción aislada no equivale al mastering de un álbum.
  * En álbum:

    * debe sostenerse una estructura común de:

      * nivel base,
      * balance macro,
      * coherencia tímbrica,
      * sensación de “sonido del disco”.
    * lo que cambia entre canciones no debe destruir esa continuidad estructural.
* **El archivo final real no es el WAV de trabajo.**

  * El consumidor no escucha el WAV de 24 bits del estudio.
  * Escucha una versión codificada por plataforma.
  * Por eso el mastering comercial moderno incluye:

    * prever la codificación,
    * simularla,
    * audicionar artefactos,
    * dejar margen de seguridad real.

## 3. Distinciones clave del módulo

* **Mezcla vs mastering**

  * **Mezcla:** trabajo interno sobre elementos individuales y buses; allí se resuelven decisiones macro de balance, color, espacio, arreglo interno y preparación del material.
  * **Mastering:** trabajo sobre la suma estéreo o producto final; no debe cargar correcciones que pertenecían a la mezcla salvo como parche excepcional.
  * Regla que se repite:

    * lo que pueda solucionarse antes, debe resolverse antes;
    * el mastering no es el lugar para “operar el cerebro” cuando el problema estaba en otro órgano del proceso.
* **Canción vs álbum**

  * Canción = libertad mayor en decisiones aisladas.
  * Álbum = estructura compartida.
  * La analogía del edificio fija que:

    * columnas, ascensor y estructura deben coincidir,
    * la decoración de cada piso puede variar.
  * Aplicado al módulo:

    * el sonido base del disco debe permanecer,
    * la identidad de cada tema puede moverse dentro de ese marco.
* **LUFS / loudness vs pico**

  * Pico y loudness no son lo mismo.
  * Se puede tener un pico alto sin una sonoridad integrada alta.
  * La etapa comercial trabaja sobre loudness percibido, no solo sobre lectura instantánea de pico.
* **Normalización de ganancia vs compresión de datos**

  * Spotify “comprime” en el sentido de codificar datos para transmisión.
  * Spotify **normaliza** el nivel de reproducción.
  * No “aplana” el rango dinámico del tema por hacer match de nivel.
* **DC Offset vs asimetría de onda**

  * **DC Offset:**

    * toda la señal está corrida respecto del eje central,
    * equivale a frecuencia 0 Hz,
    * roba headroom,
    * se corrige con HPF ultrabajo o herramienta dedicada.
  * **Asimetría:**

    * la onda está centrada, pero un semiperiodo sobresale más que el otro,
    * suele venir de relaciones de fase internas entre armónicos,
    * típica en voces o vientos,
    * se corrige con **All-Pass / rotador de fase**, no con HPF.
* **Truncado vs dithering**

  * **Truncado:** bajar de 24 a 16 bits sin tratamiento; produce errores de cuantización, rugosidad y distorsión severa.
  * **Dither:** añadir ruido aleatorio para preservar información de bajo nivel y transformar distorsión áspera en ruido controlado.
  * **Noise Shaping:** redistribuir espectralmente ese ruido hacia zonas menos sensibles del oído.
* **VCA vs Vari-Mu en compresión de mastering**

  * **VCA:**

    * elegido cuando se busca transparencia,
    * trabajo clínico,
    * reducción suave,
    * glue casi invisible.
  * **Vari-Mu / valvular:**

    * elegido cuando hace falta algo más de color, redondez, densidad o armónicos,
    * introduce huella tímbrica y no se presenta como transparente absoluta.
* **Mono Maker vs corrección temporal**

  * Colapsar a mono una banda grave con problema de fase no siempre corrige; puede empeorar.
  * Si el problema es temporal, debe corregirse con tiempo.
  * El docente insiste en que problemas de fase son, en esencia, problemas de tiempo.
* **Alta frecuencia de muestreo vs mayor fidelidad real**

  * No se acepta la idea de que 192 kHz “dibuja mejor” la onda audible.
  * La utilidad práctica de sample rates altos se liga al desplazamiento de Nyquist para mitigar aliasing, no a una supuesta superioridad visual de la forma de onda audible.
  * La mejora de calidad se ubica más en el **oversampling interno de plugins** críticos que en forzar conversores modestos a 192 kHz.

## 4. Masterización, traducción y lógica de optimización final

* **La cadena de mastering se entiende como cierre técnico-comercial, no como rutina fija obligatoria.**

  * No siempre hace falta volver a comprimir si la mezcla ya llega resuelta.
  * Puede bastar con:

    * trim inicial,
    * control técnico puntual,
    * una compresión muy ligera o ninguna,
    * limitación bien distribuida,
    * control de entrega/códec/dither.
* **Medición offline de LUFS integrados.**

  * El docente privilegia medir fuera de línea.
  * Secuencia doctrinal:

    * primero escuchar con criterio artístico,
    * luego medir offline para obtener el valor matemático frío.
  * Motivo:

    * evitar fatiga auditiva,
    * evitar acostumbramiento,
    * no “normalizar” errores por sobreexposición.
* **Trimming inicial y emparejamiento del álbum.**

  * Antes de la cadena de color o compresión, se ajusta la ganancia de entrada de las canciones.
  * Objetivo:

    * que reaccionen parecido frente a compresores, saturaciones o umbrales,
    * homogeneizar la entrada del disco al proceso.
  * Se menciona como referencia de trabajo un promedio de entrada tipo **-18 LUFS integrados**, usado como nivel común de alimentación, no como target final de entrega.
* **Optimización final no equivale a aplastar.**

  * La etapa comercial busca volumen competitivo, pero el módulo insiste en:

    * no destruir transientes,
    * no matar espacialidad,
    * no borrar factor de cresta,
    * no convertir el limitador en un devorador de la canción.
* **Limitación multietapa.**

  * Si el salto de nivel requerido es alto, se reparte:

    * primera etapa multibanda para absorber una parte importante del esfuerzo,
    * segunda etapa single-band para remate fino,
    * eventualmente una etapa vintage muy leve para color y densidad.
  * Lógica:

    * no cargar 10 dB o cifras similares a un solo aparato final.
* **Comparación isométrica obligatoria.**

  * Cualquier mejora debe audicionarse al mismo volumen exacto.
  * El umbral/gain de entrada y la salida/ceiling deben compensarse.
  * Sin esa compensación, el operador confunde “más fuerte” con “mejor”.
* **True Peak y traducción a plataformas.**

  * Dejar **-1 dBTP** aparece como referencia fuerte para streaming.
  * La razón no es solo normativa:

    * el códec con pérdida puede elevar picos,
    * el archivo aparentemente sano puede romperse en reproducción real.
* **Mastering pensado contra el archivo codificado, no solo contra el WAV.**

  * Hay que escuchar o simular:

    * AAC,
    * MP3,
    * residuos del codec,
    * subida de True Peak.
  * El WAV no es criterio suficiente de validación comercial.
* **Relación entre loudness y contexto de reproducción real.**

  * El módulo no apoya usar ciegamente **-14 LUFS** como target de mastering.
  * Razón doctrinal:

    * si la normalización está activa, el exceso de loudness puede ser bajado por la plataforma;
    * pero si el usuario la desactiva, un tema entregado tímidamente a -14 LUFS puede quedar diminuto frente a masters comerciales agresivos.
  * Punto de compromiso repetido:

    * **alrededor de -10 LUFS integrados** para pop/rock,
    * con advertencia de que urbano puede escalar a **-8 LUFS**,
    * y que esto sigue siendo sensible al género y a la intención.
* **Compresión ascendente como vía menos destructiva.**

  * En lugar de bajar picos y luego subir maquillaje, se puede elevar información de bajo nivel:

    * colas,
    * respiraciones,
    * sostenidos,
    * reverbs,
    * microdetalle.
  * Resultado buscado:

    * más densidad,
    * más RMS/loudness,
    * menos destrucción de crestas fuertes.
* **Dither al final del flujo cuando el formato lo exige.**

  * Si la entrega final debe ser 16 bits, el dither se ubica al final.
  * No se presenta como decoración ni como mejora cosmética, sino como corrección obligatoria frente al cambio de resolución.
* **La traducción puede incluir restricciones de formato.**

  * Caso físico mencionado:

    * vinilo requiere low-end muy centrado y controlado.
  * Caso digital:

    * plataformas y códecs exigen validar picos, artefactos y sonoridad.

## 5. Ejemplos técnicos que no deben perderse

* **Ejemplo de limitación multietapa**

  * Escenario mostrado: necesidad de subir aproximadamente **10 dB**.
  * Solución ejemplificada:

    * **Waves L3 Multimaximizer** para unos **7 dB** repartidos en bandas,
    * luego **FabFilter Pro-L 2** para los **3 dB** restantes,
    * opcionalmente un **Ozone Vintage Limiter** aportando alrededor de **1 dB** de color.
  * Lo importante no es solo la combinación concreta, sino el principio:

    * distribuir trabajo,
    * no reventar transientes,
    * evitar distorsión de intermodulación masiva.
* **Ejemplo de simulación de códec**

  * Archivo sano en WAV/CD:

    * 44.1 kHz / 16 bits,
    * picos en torno a **-0.3 dBFS**.
  * Al simular codificación:

    * AAC 256 kbps,
    * MP3 128 kbps,
    * el archivo puede elevar su True Peak hasta **+1.4 dBTP** en el caso mostrado para MP3 128.
  * Diagnóstico:

    * el WAV “correcto” no garantiza seguridad de reproducción final.
* **Ejemplo de evaluación por Delta**

  * Se duplica el master.
  * Un canal queda con limitador activo y otro en bypass compensado.
  * Se invierte polaridad y se escucha solo la diferencia.
  * Lectura didáctica:

    * si aparecen solo clics o transientes cortas, el limitador está cazando picos sanamente;
    * si aparece “media canción” con cuerpo, reverbs y sostenimientos, el limitador está comiéndose música.
* **Ejemplo de dithering con senoide microscópica**

  * Senoidal muy débil en 24 bits reducida a 16 bits.
  * Tres comparaciones:

    * **Truncado:** la onda suena quebrada, áspera, casi cuadrada.
    * **Dither:** baja la rugosidad, reaparece la señal útil, aparece siseo.
    * **Dither + Noise Shaping:** el ruido se desplaza a zonas menos sensibles y el resultado percibido mejora notablemente.
* **Ejemplo de corrección de fase en subgraves**

  * En el goniómetro se detecta bajo muy abierto y en contrafase por debajo de **120 Hz**.
  * En vez de usar Mono Maker:

    * se aísla la banda,
    * se aplica **Offset temporal**,
    * en el ejemplo se mueve un canal aproximadamente **5 ms**,
    * el correlator vuelve a zona positiva sin destruir la información.
* **Ejemplo de diagnóstico espectral de subsónicas**

  * En RX se analiza el archivo completo con FFT alta.
  * Criterio visual:

    * si el extremo grave dibuja una pendiente sana y claramente descendente, no se filtra “por las dudas”;
    * si aparece acumulación anómala hacia la izquierda, sí se considera corrección.
* **Ejemplo de asimetría vs DC**

  * Señal visualmente “rara” no siempre implica DC Offset.
  * Caso doctrinal:

    * si toda la señal está corrida: HPF ultrabajo / herramienta DC.
    * si está centrada pero con picos desparejos: All-Pass.
* **Ejemplo de micro-clippings de mezcla**

  * Si el archivo recibido tiene microclippings percusivos aislados de alrededor de **+0.2 dB**:

    * no se baja el fader general de la mezcla exportada,
    * se corrige en el entorno de mastering a **32/64 bit float** con trim digital,
    * porque castigar todo el archivo en punto fijo sería peor que el problema puntual.

## 6. Preguntas de estudiantes que sí aportan contenido

* **Sobre fatiga auditiva en la etapa comercial**

  * Pregunta: si al masterizar conviene bajar el monitoreo para no cansar el oído.
  * Respuesta doctrinal que aporta contenido:

    * sí,
    * si se agregan 10 dB de loudness y no se baja físicamente el monitoreo, se destruye el criterio y se pone en riesgo el oído.
* **Sobre la exigencia de entregar picos a -6 dB**

  * Pregunta: qué hacer si cliente o masterizador exige estrictamente ese headroom.
  * Contenido doctrinal derivado:

    * no bajar el master fader en exportación a 24 bits punto fijo,
    * el mastering puede atenuar internamente en float sin pérdida,
    * bajar 6 dB en el archivo fijo equivale a perder **1 bit** de resolución.
* **Sobre volver a comprimir en mastering**

  * Pregunta: si ya hubo compresores en mix bus para glue, punch o RMS, si es obligatorio volver a comprimir.
  * Respuesta:

    * no es obligatorio,
    * puede no hacer falta,
    * o puede bastar una compresión ultra suave de 1 a 2 dB si se busca un matiz final.
* **Sobre dither y aliasing**

  * Pregunta: si una señal ya tiene aliasing, si conviene evitar dither para no agregar más ruido.
  * Respuesta:

    * son fenómenos distintos,
    * no usar dither por ese motivo lleva a truncado,
    * el truncado produce una degradación peor.
* **Sobre coherencia de un disco grabado por varios productores**

  * Pregunta: si mastering puede unificar un álbum grabado por distintas personas y estudios.
  * Respuesta doctrinal:

    * puede intentar emparejar,
    * pero no puede reconstruir una preproducción inexistente ni igualar mágicamente decisiones base que nunca se unificaron.
* **Sobre la comparación del dither con el granulado fotográfico**

  * Intervención de alumno aceptada por el docente.
  * Aporta una equivalencia perceptual válida:

    * introducir “ruido” puede preservar estructura y evitar una degradación peor.
* **Sobre si el masterizador debe entregar obedeciendo solo el target de plataforma**

  * La discusión alrededor de Spotify y -14 LUFS deja asentado que la respuesta es contextual y que la plataforma no agota la realidad comercial del máster.

## 7. Advertencias, matices y correcciones del profesor

* **No usar el mastering como excusa para arreglar una mezcla fallida**

  * Es una advertencia estructural, no solo estética.
  * El mastering pone parches sobre el total; no reemplaza resolución de problemas previos.
* **No masterizar ciegamente a -14 LUFS “porque lo dice Spotify”**

  * La normalización puede desactivarse.
  * Si eso ocurre, el tema conservador queda pequeño frente a competencia más agresiva.
  * El módulo propone un enfoque de compromiso, no obediencia literal al target de plataforma.
* **No poner un clipper en el master para resolver volumen extremo**

  * Si el clipper actúa sobre el estéreo completo, distorsiona simultáneamente todo lo que coincida con el pico del bombo o la percusión.
  * La doctrina es ubicar clippers en mezcla, especialmente en buses percusivos.
* **No insertar HPF a 20 Hz “por las dudas”**

  * Todo filtro rota fase.
  * Puede producir overshoot y levantar picos sin sumar volumen útil.
  * Solo se filtra si el diagnóstico espectral completo lo justifica.
* **No bajar el master fader para exportar headroom en punto fijo**

  * Es una advertencia técnica mayor.
  * Se repite con carácter casi normativo.
  * El daño por pérdida de resolución se considera innecesario y peor que el supuesto beneficio.
* **No comparar limitadores a distinto volumen**

  * Es la trampa psicoacústica central del módulo comercial.
  * Sin compensación exacta, cualquier comparación queda sesgada.
* **No creer que el ataque del limitador de mastering es una perilla “creativa” típica**

  * Un limitador real trabaja a ataque instantáneo.
  * Si hay perilla de attack, probablemente esté nombrando otra cosa o una abstracción comercial.
* **No cerrar a mono el grave problemático sin antes diagnosticar el origen**

  * Si el problema es temporal, colapsar a mono puede borrar el bajo por cancelación.
* **No asumir que el botón Learn resuelve musicalmente la banda multibanda**

  * El análisis matemático puede ubicar crossovers donde conviene al algoritmo.
  * Eso no garantiza que coincida con el punto musical que el tema necesita.
* **No olvidar el modo 1:1 activado en Pro-L 2 antes del bounce**

  * Error operativo concreto:

    * sirve para comparar,
    * no para entregar.
* **No creer que el limitador colorea solo por estar insertado**

  * En reposo, un limitador genuino se muestra transparente.
  * El engaño suele venir del aumento de volumen al activarlo con ganancia ya aplicada.
* **No asumir que 192 kHz es automáticamente más “pro”**

  * En hardware medio o bajo puede empeorar precisión.
  * El criterio correcto del módulo es usar sample rates razonables y oversampling donde haga falta.
* **No igualar todos los géneros con el mismo nivel medio**

  * El PLR y el loudness objetivo dependen del material.
  * El módulo da referencias, no una planilla universal cerrada.
* **Matiz sobre True Peak y realidad comercial**

  * La regla técnica pide margen.
  * Pero se reconoce que existen masters comerciales premiados con True Peaks positivos.
  * El profesor no borra esta tensión: la presenta como choque entre especificación técnica y decisión estética/comercial agresiva.
* **Matiz sobre etapa artística**

  * Puede no existir.
  * Si la mezcla llegó perfecta, no hace falta inyectar color “porque sí”.

## 8. Herramientas, referencias técnicas, configuraciones y detalles operativos

* **Herramientas de medición y análisis**

  * **Youlean Loudness Meter**

    * usado para LUFS integrados, short-term, momentary y True Peak,
    * preferentemente en modo offline / AudioSuite para no gastar oído.
  * **WLM u otros medidores de loudness**

    * delimitados como herramientas propias del flujo de mastering,
    * no apropiadas para gain staging de pistas individuales de mezcla.
  * **PAZ u otros medidores de pico/RMS convencionales**

    * señalados como más adecuados para etapas tempranas de estructura de ganancia.
* **Herramientas de diagnóstico/reparación**

  * **iZotope RX**

    * análisis de espectro de selección completa,
    * estadísticas de forma de onda,
    * detección/corrección de DC Offset,
    * análisis de subsónicas,
    * lectura de asimetrías.
* **Herramientas de mastering / procesamiento**

  * **iZotope Ozone**

    * módulo Imager,
    * Offset temporal,
    * Recover Sides,
    * simulación de códec,
    * Learn en crossovers,
    * Vintage Limiter,
    * Maximizer con tecnología IRC4 multibanda interna.
  * **FabFilter Pro-L 2**

    * limitador final single-band,
    * modo 1:1,
    * modo Delta,
    * filtro DC offset integrado,
    * oversampling escalable,
    * dithering.
  * **Waves L3 Multimaximizer**

    * limitador multibanda de 5 bandas,
    * primera etapa de maximización gruesa,
    * permite priorizar/gain por zona frecuencial.
  * **Vertigo VSC-2**

    * compresión VCA transparente,
    * modo soft,
    * feed-forward,
    * uso típico: 1 a 2 dB casi invisibles antes de limitación.
  * **Neve 33609 / Pulsar Mu / Fairchild / Manley**

    * familia de compresores con color,
    * usados cuando se quiere redondez, armónicos o pegamento menos clínico.
  * **Waves MV2 / MB2 y expansores ascendentes tipo Pro-MB**

    * usados para compresión ascendente y recuperación de densidad sin decapitar transientes.
* **Configuraciones operativas repetidas**

  * bajar monitoreo al entrar en la etapa comercial,
  * usar oversampling alto en limitación severa,
  * activar oversampling al máximo antes del bounce offline final si la mezcla no pudo sostenerlo en tiempo real,
  * desactivar modo 1:1 antes de exportar,
  * usar HPF en sidechain de compresor VCA alrededor de **60 Hz** cuando se busca glue sin que el grave lo sobreactive,
  * usar ataque lento y release lento/auto en compresión VCA muy suave.
* **Valores y referencias que el módulo trae con formulación prudente**

  * **-14 LUFS integrados:** normalización típica de Spotify; no usar ciegamente como target de mastering.
  * **-10 LUFS integrados:** referencia de compromiso comercial para pop/rock en esta cátedra.
  * **-8 LUFS integrados:** posible zona de urbano/agresivo, con costo dinámico implícito.
  * **-1 dBTP:** techo técnico fuerte para streaming.
  * **PLR 13–15 LU:** rango sano para pop/rock según la referencia del profesor.
  * **PLR 18 LU:** posible en material acústico.
  * **<120 Hz:** banda crítica citada para low-end, monocompatibilidad y vinilo.
  * **5 ms:** ejemplo de offset temporal usado en corrección de fase de subgraves.
  * **5 Hz:** ejemplo de HPF ultrabajo para DC Offset.
  * **1 bit = 6 dB**
  * **16 bits = 65,536 escalones**
  * **24 bits = ~16.7 millones de escalones**
* **Detalles técnicos conceptuales**

  * el True Peak anticipa picos interesample;
  * el oversampling se usa para bajar aliasing en procesos no lineales y limitación severa;
  * la ponderación K hace que un exceso de agudos influya en la lectura de loudness;
  * Recover Sides permite no destruir completamente la amplitud lateral al estrechar una banda;
  * el uso de Tilt EQ y shelving resonante aparece como recurso macrotonal suave apto para mastering;
  * la curva de ruido rosa filtrado se plantea como referencia empírica de balance tonal cuando no se dispone de herramientas especializadas.

## 9. Contenido dislocado que sí pertenece a M08

* **Clase 5 — Ponderación K, LUFS y normalización**

  * LUFS usa ponderación K.
  * La ponderación privilegia medios-altos y agudos.
  * Subir agudos innecesariamente puede inflar la lectura de loudness.
  * Spotify:

    * normaliza,
    * no comprime rango dinámico por esa acción,
    * baja o sube el nivel según corresponda.
  * También desde esta clase queda fijada la regla de que el loudness comercial fuerte no debe recaer todo en el limitador del máster.
* **Clase 5 — Clippers en mezcla vs mastering**

  * El clipper debe trabajar en buses percusivos durante mezcla.
  * En mastering estéreo distorsionaría conjuntamente bombo, bajo, voz y demás elementos que compartan ese instante.
  * Este punto no es accesorio: define cómo se prepara el headroom para la etapa final.
* **Clase 6 / Clase 24 / Clase 7 — No bajar el fader para “entregar a -6”**

  * Reaparece fuera del bloque principal como doctrina fuerte.
  * Se conserva porque organiza la interfaz entre mezcla y mastering.
  * El mastering opera en float; la mezcla exportada en fijo no debe regalar resolución.
* **Clase 7 — PLR / factor de cresta**

  * Se incorpora porque da una lectura cuantitativa del daño o salud dinámica tras la maximización.
  * No se presenta como cifra universal, sino sensible a género.
* **Clase 8 — Qué medidores pertenecen al mastering**

  * Los medidores de loudness no son para ajustar entradas de pistas individuales.
  * Su lugar natural es la evaluación de sonoridad global del producto final.
* **Clase 9 — Monocompatibilidad en graves y destino vinilo**

  * Si el grave estéreo queda muy abierto, un máster destinado a vinilo puede ser inviable físicamente.
  * Pero incluso aquí la corrección correcta sigue siendo temporal si el origen es desfasaje, no colapso ciego a mono.
* **Clase 12 — Curva de ruido rosa filtrado como referencia tonal**

  * Recurso empírico de diagnóstico macro.
  * Consiste en:

    * generar ruido rosa,
    * filtrarlo suavemente cerca de **50 Hz** y **5 kHz**,
    * capturar su “foto” espectral,
    * comparar la pendiente macro del master contra esa rampa.
  * Se conserva como complemento diagnóstico, no como ley exclusiva.
* **Clase 13 — Shelving resonante y Tilt EQ**

  * Se incorpora por su uso específicamente macrotonal en mastering.
  * Un Tilt permite mover todo el balance con suavidad.
  * Un Low Shelf con resonancia mínima puede aumentar peso y a la vez generar un microvalle que limpie barro y resalte el impacto del bombo de forma psicoacústica.
* **Clase 14 — True Peak técnico vs criterio estético/comercial**

  * Aunque la regla técnica para plataformas se sostiene en **-1 dBTP**, se reconoce que la industria real a veces publica o premia masters con clipping y True Peaks positivos.
  * Este cruce se conserva porque muestra que el módulo no simplifica el choque entre técnica y mercado.
* **Clase 19 — Compresión ascendente**

  * Pasa a este módulo por función directa de maximización menos destructiva.
  * Herramientas citadas:

    * Waves MV2 / MB2,
    * expansores ascendentes tipo Pro-MB.
  * Objetivo:

    * aumentar densidad, RMS y presencia de detalle sin aplastar las crestas principales.
* **Clase 19 — Ecualización dinámica sobre mezcla estéreo**

  * Caso concreto:

    * los platillos solo se vuelven dolorosos cuando aparecen.
  * Regla:

    * no usar EQ estática que perjudique todo el track,
    * usar EQ dinámica que actúe solo cuando el problema se manifiesta.
  * Esto se integra al módulo por su lógica de corrección “no dañar lo sano” sobre el archivo estéreo final.
* **Clase 21 y Clase 28 — Oversampling máximo antes del bounce final**

  * Si durante mezcla no hubo CPU para trabajar en oversampling alto, debe activarse al máximo antes del bounce offline final.
  * El objetivo es entregar al mastering un archivo más limpio en términos de aliasing y cálculo no lineal.
* **Clase 12 / Clase 26 — Overshoot por filtrado**

  * La advertencia sobre overshoot inducido por HPF global no solo pertenece a EQ; impacta directamente el headroom del mastering.
* **Clase 28 — RX y control técnico**

  * Se refuerza el uso de RX como estación de análisis y reparación técnica previa o complementaria al mastering.
  * Su presencia dislocada no quita pertenencia al módulo.

## 10. Mapa de cobertura

* **Definición general de mastering**

  * Clases 25 y 26.
* **Etapas del mastering: técnica, comercial, artística**

  * Clases 25 y 26.
* **Diferencia mezcla vs mastering**

  * Clases 25, 26 y soporte tangencial de Clase 19.
* **Lógica de álbum vs canción**

  * Clase 25, con refuerzo tangencial en Clase 22.
* **LUFS, ponderación K y normalización**

  * Clases 25 y 5.
* **Targets de loudness y su uso prudente**

  * Clases 25, 26 y 5.
* **True Peak y clipping por codificación**

  * Clases 27, 26 y complemento de Clase 14.
* **Medición offline y fatiga auditiva**

  * Clase 26.
* **Trimming inicial / emparejamiento de álbum**

  * Clase 26.
* **Limitación multietapa**

  * Clase 27.
* **Comparación isométrica y autoengaño por volumen**

  * Clase 27.
* **Modo Delta como diagnóstico**

  * Clase 27, con referencia tangencial en Clase 26.
* **Compresión previa al limitador**

  * Clase 26 y apoyo de Clase 19.
* **Compresión ascendente**

  * Clase 19 y refuerzo en Clase 26.
* **DC Offset, asimetría y correcciones respectivas**

  * Clase 26 y apoyo operativo de Clase 28.
* **Subsónicas, HPF y overshoot**

  * Clase 26 y Clase 12.
* **Monocompatibilidad, low-end y corrección temporal**

  * Clase 26 y Clase 9.
* **Códec final, artefactos y simulación**

  * Clase 27.
* **Dither y Noise Shaping**

  * Clase 27.
* **No bajar el fader para exportar headroom**

  * Clase 25, Clase 6, Clase 24 y apoyo tangencial en Clase 7.
* **PLR / factor de cresta**

  * Clase 7.
* **Clippers en mezcla, no en master**

  * Clase 5 y Clase 25.
* **Balance tonal macro, ruido rosa, Tilt y shelving**

  * Clases 12 y 13.
* **Oversampling antes del bounce final**

  * Clases 21 y 28.
* **Herramientas de loudness vs herramientas de gain staging**

  * Clase 8.

## 11. Trazabilidad principal por clases

* **Clase 25**

  * definición de mastering,
  * tres etapas,
  * álbum vs canción,
  * mito de que mastering arregla mezcla,
  * LUFS y streaming,
  * peligro de targetear -14 LUFS ciegamente,
  * sample rate y Nyquist,
  * resolución en bits,
  * no bajar master fader para entregar a -6.
* **Clase 26**

  * medición offline,
  * trim inicial,
  * Recover Sides,
  * análisis técnico de espectro,
  * HPF y overshoot,
  * corrección temporal de low-end,
  * botón Learn y límites del automatismo,
  * DC Offset vs asimetría,
  * compresores VCA / Vari-Mu,
  * monitoreo y fatiga auditiva,
  * compresión suave previa al limitador.
* **Clase 27**

  * comparación isométrica,
  * diagnóstico Delta,
  * transparencia del limitador en reposo,
  * ataque real de limitadores,
  * distorsión de graves por release,
  * True Peak,
  * simulación de códec,
  * limitación multietapa,
  * oversampling en limitación,
  * dithering y noise shaping,
  * uso operativo de Pro-L 2.
* **Clase 5**

  * ponderación K,
  * LUFS,
  * normalización de Spotify,
  * distinción normalización/compresión,
  * preparación de loudness con clipper en mezcla.
* **Clase 6 / Clase 24**

  * refuerzo de la regla: no bajar el master fader para “regalar headroom”.
* **Clase 7**

  * PLR / factor de cresta como criterio de salud dinámica.
* **Clase 8**

  * delimitación de WLM/LUFS como herramientas de mastering y no de gain staging interno.
* **Clase 9**

  * low-end estéreo, monocompatibilidad y restricción de vinilo.
* **Clase 12**

  * referencia tonal con ruido rosa filtrado,
  * advertencia sobre filtrado global y sus efectos colaterales.
* **Clase 13**

  * Tilt EQ,
  * shelving resonante como recurso macrotonal de mastering.
* **Clase 14**

  * tensión entre norma técnica de True Peak y realidad comercial con masters clippeados.
* **Clase 19**

  * compresión ascendente,
  * uso de MV2/MB2 y equivalentes,
  * ecualización dinámica sobre la mezcla estéreo cuando el problema es intermitente.
* **Clase 21**

  * oversampling máximo antes del bounce offline final.
* **Clase 22**

  * refuerzo tangencial de la lógica de álbum como estructura compartida.
* **Clase 28**

  * refuerzo operativo del uso de RX y del control técnico previo/complementario al mastering,
  * recordatorio de oversampling máximo antes de exportar si durante mezcla no pudo sostenerse.
