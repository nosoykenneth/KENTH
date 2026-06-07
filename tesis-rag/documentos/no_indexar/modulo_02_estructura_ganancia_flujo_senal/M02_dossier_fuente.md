---

course_id: mezcla_masterizacion_kenth
module_id: M02
module_order: 2
module_title: Estructura de ganancia y flujo de señal
module_slug: estructura-ganancia-flujo-senal
doc_type: source_dossier
source_origin: author_compiled_from_transcripts
filename: M02_dossier_fuente.md
version: 0.1
status: draft_source_compilation
curation_source: extraccion_exhaustiva_notebooklm_desde_clases_definitivas
ready_for_indexing: false
-------------------------

# M02 — Dossier fuente exhaustivo

## Estructura de ganancia y flujo de señal

> Este documento NO es guia canonica.
> NO es FAQ.
> NO es glosario final.
> Es una fuente intermedia exhaustiva, reorganizada por modulo, construida a partir de clases definitivas corregidas.
> Su objetivo es preservar detalle, matices, ejemplos, advertencias y trazabilidad antes de condensar doctrina para el RAG.

## 1. Alcance del dossier

* Este módulo reúne el núcleo técnico relativo a:

  * niveles de señal y referencias en dB
  * estructura de ganancia analógica y digital
  * headroom
  * relación entre nivel de entrada, nivel promedio, nivel pico y nivel de salida
  * flujo de señal dentro de canales, buses, auxiliares, subgrupos y master
  * lectura correcta de medidores según tipo de material
  * correcciones operativas cuando una cadena o suma se sale de nivel
  * adaptación entre dominios eléctricos y digitales
* También incorpora contenido que apareció fuera de la clase central del módulo pero que pertenece claramente a M02:

  * calibración real de plugins de modelado analógico
  * arquitectura Mix Bus vs Master Fader
  * pérdida de resolución al exportar
  * alteraciones del recorrido interno en canales tipo SSL
  * overshoot de filtros y su efecto sobre procesos posteriores
  * compensación obligatoria de nivel en inserciones posteriores del curso
* Quedan dentro del alcance:

  * ejemplos del profesor
  * matices
  * contraejemplos
  * preguntas de estudiantes que corrigen malentendidos
  * valores numéricos y fórmulas
  * advertencias contra recetas simplificadas
* Quedan fuera como capa final:

  * redacción de doctrina consolidada “bonita”
  * FAQ final
  * glosario final
  * formulación cerrada de reglas universales cuando el material las presenta como dependientes del contexto

## 2. Núcleo conceptual del módulo

* **El decibel es una comparación, no una medida absoluta.**

  * El dB expresa relación logarítmica entre un dato y una referencia.
  * Un decibel “referenciado” fija un 0 dB en un valor eléctrico o digital concreto e inamovible.
* **Referencias de decibeles eléctricos y digitales.**

  * 0 dBW = 1 W
  * 0 dBm = 1 mW
  * 0 dBV = 1 V
  * 0 dBu = 0,775 V
  * 0 dBFS = máximo valor codificable en el dominio digital de coma fija
* **Principio matemático de potencia vs voltaje.**

  * Para potencia: `dB = 10 · log10(dato/referencia)`
  * Para voltaje: `dB = 20 · log10(dato/referencia)`
  * Duplicar potencia = +3 dB
  * Duplicar voltaje = +6 dB
  * Regla mnemotécnica: **“Para potencia, el doble son tres; para todo lo demás, son seis”.**
* **Tres niveles de señal en audio.**

  * **Nivel de micrófono:** extremadamente bajo; muy vulnerable al ruido térmico.
  * **Nivel de línea:** nivel operativo donde se comunican equipos y donde ocurre casi todo el procesamiento.
  * **Nivel de amplificación:** etapa final que mueve físicamente el parlante.
* **Función del preamplificador.**

  * Convierte señal de micrófono en señal de línea.
  * Su trabajo no es “hacer que el micrófono exista”, sino llevar una señal diminuta a un voltaje utilizable sin destruir relación señal/ruido ni saturar el circuito.
* **Nivel operativo analógico.**

  * En equipos profesionales, el nivel operativo típico es **+4 dBu** (aprox. 1,23 V).
  * En equipos domésticos o semiprofesionales, el nivel operativo típico es **-10 dBV** (aprox. 0,32 V).
  * La diferencia no define calidad moral del equipo; define sensibilidad y marco operativo.
* **0 VU como nivel medio de trabajo, no como techo.**

  * En hardware analógico, 0 VU representa la zona media ideal de operación.
  * No es el máximo.
  * Ahí se espera la mejor relación señal/ruido y el comportamiento armónico previsto del equipo.
* **Headroom y nivel operativo no son lo mismo.**

  * El headroom es margen libre antes de saturar.
  * El nivel operativo es la zona promedio óptima donde conviene hacer trabajar la señal.
* **Estructura de ganancia como relación entre etapas, no como un número aislado.**

  * No se reduce a “poner todo a -18”.
  * Implica que cada eslabón reciba una señal coherente con su rango operativo.
  * Implica además compensar cada cambio de nivel introducido por el procesamiento.
* **Clipping interno vs clipping de entrada/salida.**

  * El motor interno del DAW trabaja en 32, 48 o 64 bit float.
  * Dentro de ese entorno pueden aparecer valores por encima de 0 dBFS sin que la señal se destruya automáticamente.
  * Pero conversores ADC/DAC y archivos finales en coma fija sí tienen límite duro en 0 dBFS.
  * Lo que entra al conversor o sale hacia él no puede superar 0 dBFS sin recorte.
* **La estructura de ganancia incluye la arquitectura de ruteo.**

  * No es solo una cuestión de números.
  * También depende de por dónde circula la señal, en qué orden pasan los procesos y qué recibe cada etapa.

## 3. Distinciones clave del módulo

* **Potencia vs voltaje**

  * Potencia duplica = +3 dB.
  * Voltaje duplica = +6 dB.
  * Esta diferencia es estructural; no es un detalle menor de fórmula.
* **Equipo profesional vs doméstico/semiprofesional**

  * Profesional: +4 dBu.
  * Doméstico/semiprofesional: -10 dBV.
  * Mezclarlos sin adaptar puede producir:

    * saturación al entrar de pro a doméstico
    * ruido de fondo excesivo al entrar de doméstico a pro
  * El switch **+4 / -10** existe precisamente para adaptar sensibilidad.
* **Micrófono vs línea vs amplificación**

  * Micrófono no debe entrar directo a un dominio pensado para línea sin preamplificación apropiada.
  * Línea no debe regresar a entrada de micrófono o de instrumento como si nada.
* **Bus vs auxiliar**

  * El **bus** es la ruta interna, el conducto.
  * El **auxiliar** es el canal que recibe esa ruta y permite procesarla y volver a rutearla.
  * El bus por sí solo no necesita salida física.
* **Proceso vs efecto**

  * **Proceso:** modifica la señal entera; típicamente se inserta.

    * EQ
    * filtro
    * compresor
  * **Efecto:** agrega contenido nuevo; típicamente se usa en paralelo mediante envío.

    * reverb
    * delay
  * Matiz: un compresor usado en paralelo, aunque siga siendo proceso, funciona perceptualmente como un efecto paralelo.
* **Prefader vs postfader**

  * **Postfader:** para efectos como reverb/delay cuando se quiere que el envío acompañe los cambios del canal.
  * **Prefader:** para compresión paralela y mezclas de monitoreo, donde el movimiento del fader principal no debe alterar la señal que alimenta el proceso paralelo.
* **PFL vs AFL**

  * **PFL:** mide antes del fader; es el modo correcto para grabar y estructurar ganancia.
  * **AFL:** mide después del fader; puede ocultar el nivel real que entra a la cadena.
* **Lectura Peak vs VU/RMS**

  * Percusivos: se controlan por **picos**.
  * No percusivos: se evalúan por **VU/RMS**.
  * Usar VU para señales percusivas lleva a lecturas engañosas por la balística del medidor.
* **Nivel pico vs nivel promedio**

  * El pico aislado no equivale al estado global de la señal.
  * La media/energía sostenida define muchas decisiones de trabajo.
  * Esto es clave para no destruir una estructura bien hecha persiguiendo un pico errático.
* **Master Fader vs Mix Bus**

  * El material separa ambas funciones.
  * El Mix Bus puede usarse como canal auxiliar central donde llega la mezcla.
  * El Master Fader queda como punto final de control físico y análisis.
* **Clipping analógico vs clipping digital**

  * En analógico, el acercamiento o superación del nivel operativo puede implicar coloración o distorsión del circuito.
  * En digital de entrada/salida, superar 0 dBFS implica recorte duro de la forma de onda.
* **“0 VU = -18 dBFS” como estándar general vs calibración real por plugin**

  * Puede funcionar en ciertos equipos y plugins clásicos.
  * No es verdad universal.
  * La calibración debe medirse cuando el comportamiento del plugin lo amerita.

## 4. Flujo operativo y lógica del recorrido de señal

* **Cadena básica de nivel**

  * Micrófono/instrumento
  * preamplificación
  * nivel de línea
  * procesamiento
  * subgrupos / buses / auxiliares
  * mix bus
  * master / salida / conversión
* **Regla eléctrica central**

  * **“Línea se comunica únicamente con línea”.**
  * Un previo externo ya entrega nivel de línea.
  * Una pedalera activa que saca línea debe entrar a línea.
  * Volver a meter esas señales en entrada de micrófono o instrumento genera problemas de impedancia y distorsión.
* **Orden operativo al preparar una señal en mezcla**

  * Primero se corrige nivel de entrada real con:

    * Clip Gain
    * AudioSuite Gain
    * Trim en primera ranura
  * Después se procesa.
  * El fader no se usa para arreglar una entrada mal nivelada.
* **Razón de esa prioridad**

  * Las inserciones suelen ser prefader.
  * Si la señal ya entró demasiado fuerte al primer plugin, bajar el fader después no arregla la saturación previa.
* **Gain staging activo**

  * Cada plugin que sube nivel obliga a corregir su salida.
  * La señal debe salir de un proceso aproximadamente en el mismo marco operativo en que entró, salvo decisión deliberada y controlada.
* **Flujo dentro de grupos y sumas**

  * Canales individuales pueden estar correctos por separado.
  * La suma puede sobrecargar el grupo.
  * La corrección debe ocurrir a nivel de suma antes de los procesos grupales si el problema nace ahí.
* **Lógica de envíos**

  * Reverb/delay:

    * envío postfader
    * el nivel del efecto acompaña al canal
  * Paralelo dinámico/monitoreo:

    * envío prefader
    * el fader no altera el umbral o balance paralelo
* **Arquitectura macro recomendada**

  * Subgrupos → canal auxiliar de **Mix Bus** → Master Fader
  * Esto permite:

    * insertar hardware
    * grabar mezcla en un track interno
    * imprimir stems
    * reservar el Master Fader para control final y metering
* **Split en canales SSL**

  * Ruta por defecto problemática:

    * Entrada → Dinámica → Filtros/EQ
  * Ruta recomendada:

    * Entrada → Filtros → Dinámica → EQ
  * La intención es que el compresor no reaccione a información que luego será filtrada.
* **Impacto del filtrado sobre etapas posteriores**

  * Filtrar puede generar overshoot por rotación de fase.
  * Aunque el RMS no suba, el pico sí puede subir.
  * Eso altera el comportamiento de compresores o lectores por pico colocados después.
* **Exportación como tramo final del flujo**

  * Mezcla interna float y archivo final fixed-point no son el mismo territorio.
  * Una decisión de nivel en el bounce afecta resolución real.
  * Bajar el master para “cumplir con -6” no es un simple gesto visual; puede destruir resolución.

## 5. Ejemplos técnicos que no deben perderse

* **Ejemplo de suma saturada en subgrupo**

  * Caso: top y bottom de tambor están bien individualmente, pero el subgrupo queda “al rojo vivo”.
  * Soluciones expuestas:

    * mover faders enlazados
    * usar VCA
    * insertar Trim en la primera ranura del grupo
  * La opción preferida del profesor es el Trim en el grupo porque:

    * conserva balances previos
    * corrige la suma antes del procesamiento grupal
    * entrega señal bien nivelada a plugins posteriores
* **Ejemplo matemático de potencia vs voltaje**

  * En dBW:

    * 1 W a 2 W = +3 dB
    * 1 W a 10 W = +10 dB
  * En dBV:

    * 1 V a 2 V = +6 dB
    * 1 V a 4 V = +12 dB
* **Ejemplo de calibración extrema en plugin analógico**

  * En el compresor Summit Audio TLA-100A, al llevar la aguja a 0 VU, la salida digital real queda alrededor de **-7 dBFS**.
  * Esto destruye la receta automática de “0 VU = -18 dBFS para todo”.
* **Ejemplo de senoidal pura vs onda compleja**

  * Una senoidal a -18 dBFS puede marcar 0 VU exactos.
  * Si se suman varias senoidales distintas, la aguja sube.
  * Al compensar con trim para volver a 0 VU, el medidor digital queda cerca de **-15 dBFS**.
  * Esto se usa para mostrar que el comportamiento de señales complejas no coincide linealmente con la regla aplicada a tonos puros.
* **Ejemplo del “tercio del dibujo”**

  * Ajustar visualmente el clip hasta que la forma de onda ocupe aprox. un tercio de la altura.
  * Ese atajo suele dejar:

    * picos cercanos a -6 dBFS
    * promedios en una zona operativa razonable
  * Se presenta como método rápido, no como ley matemática.
* **Ejemplo de error de exportación**

  * Bajar 6 dB el Master Fader al exportar a 24 bits implica perder 1 bit de resolución.
  * En la explicación del profesor:

    * se pasa de usar aprox. 8 millones de escalones por semiciclo a 4 millones
* **Ejemplo de Mix Bus saludable con pico relativamente alto**

  * En un bolero acústico, el Mix Bus mostraba aprox. **-2,8 dBFS de pico** y **-20 RMS**.
  * La corrección del profesor es que eso no obliga a bajar todo a -6 dBFS.
  * Si el promedio es sano y no hay clipping, perseguir otro pico por norma rígida es un error.
* **Ejemplo de pico aislado en señal no percusiva**

  * Si un bajo está bien en RMS/VU pero tiene un golpe aislado desbordado, no se debe bajar todo el track.
  * La corrección se hace sobre el evento puntual:

    * edición
    * compresión específica
    * limitación ligera

## 6. Preguntas de estudiantes que sí aportan contenido

* **¿Se corrige el headroom con el fader o con la ganancia previa?**

  * La pregunta permite fijar una regla central:

    * el fader no corrige estructura de ganancia de entrada
    * el ajuste debe hacerse antes del fader
  * El argumento técnico es que las inserciones son prefader.
* **¿No se puede grabar alto mientras no llegue a 0 y luego bajar en mezcla?**

  * La respuesta aclara que el problema no es solo digital.
  * El previo analógico tiene una zona operativa.
  * Grabar demasiado alto puede empujar el circuito fuera de su zona ideal y aumentar distorsión analógica, sobre todo en interfaces medias.
* **¿Qué pasa si una pista fue grabada muy baja y además va a sonar baja en la mezcla?**

  * La respuesta introduce la relación señal/ruido.
  * No siempre es un problema fatal.
  * Depende de la cadena:

    * con equipo de alta gama y ruido térmico muy bajo, puede ser tolerable
    * con interfaces medias o hardware ruidoso, la señal útil queda enterrada
* **¿Qué pasa si uso un pre externo y luego entro a la interfaz?**

  * La respuesta consolida la regla:

    * salir del pre externo = ya estoy en línea
    * por tanto debo entrar a línea, no a micrófono
* **Preguntas sobre envíos y ruteo paralelo**

  * Permiten fijar que:

    * efectos temporales/espaciales van postfader
    * compresión paralela y monitoreo van prefader
  * La razón no es caprichosa; responde a cómo afectan las automatizaciones y el umbral de los procesos paralelos.

## 7. Advertencias, matices y correcciones del profesor

* **No usar el fader para arreglar una señal que ya entra mal a la cadena.**

  * Si la señal llega “al rojo vivo” al plugin, bajar el fader después no arregla nada.
  * La corrección debe ser:

    * Clip Gain
    * AudioSuite Gain
    * Trim al inicio
* **Mito: “la estructura de ganancia es poner todos los picos a -18 dBFS”.**

  * Corrección:

    * eso no define estructura de ganancia
    * -18 dBFS como equivalencia exacta sirve para senoidal pura
    * en música, lo relevante es el promedio
    * en señales complejas, 0 VU puede acercarse más a -20 RMS
* **No usar VU para señales percusivas.**

  * La lectura por VU en material percusivo es engañosa.
  * Para transientes rápidas se debe usar Peak.
  * El VU/RMS queda reservado para material sostenido.
* **Los ~6 dB de headroom no son norma universal.**

  * Aparecen como práctica útil y frecuente.
  * No se presentan como estándar obligatorio AES/EBU/SMPTE.
  * En material muy dinámico se sugiere incluso pensar en márgenes mayores, como 12 dB.
* **Mito: “para mastering hay que entregar clavadito a -3 o -6 dBFS de pico”.**

  * Corrección:

    * no se establece como estándar universal obligatorio
    * si la mezcla no clipea, puede terminar en -2,3, -2,8, -0,4, etc.
    * bajar todo solo por cumplir ese pico puede ser un error técnico
* **No bajar el Master Fader al exportar a 24 bits para “crear headroom”.**

  * Eso destruye resolución.
  * La corrección correcta es entregar la mezcla sin clipping y ajustar trim en un entorno float posterior si hace falta.
* **Mito: “si un medidor marca +3 en el master, entonces están saliendo +3 dB por encima de cero”.**

  * Corrección:

    * no existe salida útil por encima de 0 dBFS en el conversor
    * ese +3 significa que hubo 3 dB recortados
* **Mito: “si no uso preamplificador, el micrófono no suena”.**

  * Corrección:

    * sí genera señal
    * el problema es que esa señal es ínfima y, al intentar levantarla después, se levanta junto con el ruido térmico
* **Mito: “la ficha XLR o TRS define el tipo de señal”.**

  * Corrección:

    * el conector no define por sí mismo si la señal es balanceada, de línea, micrófono o instrumento
    * una ficha puede transportar una cosa u otra según cómo esté cableado y qué circuito haya detrás
* **Ojo con asumir la misma calibración en todos los plugins de modelado analógico.**

  * Casos mencionados:

    * Softube CL 1B cercano a 0 VU = -18 dBFS
    * LA-2A / UAD alrededor de -15 dBFS
    * Summit TLA-100A alrededor de -7 dBFS
  * Conclusión:

    * no aplicar recetas de internet ciegamente
    * medir el plugin o corregir con trim
* **Ojo con el flujo interno predeterminado de ciertos canales.**

  * En SSL, dejar dinámica antes de filtros puede hacer que el compresor reaccione a subsónicos o basura que luego será eliminada.
* **No confundir pico alto aislado con mezcla mal estructurada.**

  * Si el promedio está sano, bajar toda la mezcla por un pico suelto puede ser una mala decisión.
* **No significa que grabar bajo sea siempre un error.**

  * Depende del ruido propio de la cadena.
  * La doctrina no se presenta como absolutismo ciego.
* **La compensación de nivel en plugins no es opcional si se quiere escuchar objetivamente.**

  * Si un proceso sube 10 dB, debe compensarse 10 dB a la salida.
  * De lo contrario se confunde “más fuerte” con “mejor”.

## 8. Herramientas, referencias técnicas, configuraciones y detalles operativos

* **Herramientas de control de nivel previo**

  * Clip Gain
  * AudioSuite Gain
  * Trim
* **Herramientas de medición**

  * VU meters
  * medidores RMS
  * medidores Peak
  * Waves PAZ Meters
  * analizadores y medidores colocados en Master Fader como herramientas de observación
* **Herramientas de diagnóstico de calibración**

  * generador de oscilador
  * uso de senoidal de 1000 Hz a nivel definido, por ejemplo -18 dBFS
* **Herramientas de control grupal**

  * VCA para mover varios faders conservando proporciones
  * subgrupos/buses para sumar y procesar
  * auxiliares para recibir buses y procesar rutas internas
* **Plugins y equipos mencionados en relación con calibración o flujo**

  * FabFilter Pro-Q
  * Teletronix LA-2A
  * Universal Audio 1176
  * Summit Audio TLA-100A
  * Neve 2254
  * SSL E/G
* **Configuraciones operativas**

  * medidores en **PFL** al grabar y al estructurar ganancia
  * envíos **postfader** para reverb/delay
  * envíos **prefader** para compresión paralela y monitoreo
  * uso del switch **+4 / -10** al adaptar equipamiento
  * uso del botón **Split** en SSL para reordenar el flujo interno
* **Valores y referencias técnicas relevantes**

  * 0 dBW = 1 W
  * 0 dBm = 1 mW
  * 0 dBV = 1 V
  * 0 dBu = 0,775 V
  * profesional: +4 dBu ≈ 1,23 V
  * semiprofesional/doméstico: -10 dBV ≈ 0,32 V
  * duplicar potencia = +3 dB
  * duplicar voltaje = +6 dB
  * 0 dBFS = techo digital de entrada/salida en coma fija
  * 1 bit ≈ 6 dB
  * 16 bits ≈ 65.536 escalones pico a pico
  * 24 bits ≈ 16 millones de escalones pico a pico
* **Equivalencias de calibración que requieren prudencia**

  * senoidal pura:

    * 0 VU = -18 dBFS
    * también se menciona alrededor de -21 dB RMS
  * señal musical compleja:

    * 0 VU cercano a -20 dB RMS
    * en el ejemplo de suma de senoidales, 0 VU quedó cerca de -15 dBFS
  * caso excepcional:

    * Summit TLA-100A: 0 VU ≈ -7 dBFS
* **Detalle eléctrico complementario**

  * Regla 8:1 de impedancia:

    * la impedancia del auricular debería ser aprox. ocho veces mayor que la impedancia de salida del amplificador
  * Se presenta como criterio para preservar respuesta y damping en la escucha.
* **Detalles operativos de exportación**

  * bajar 6 dB al Master Fader en bounce a 24 bits = perder 1 bit de resolución
  * el ajuste de nivel posterior conviene hacerlo en entorno 32/64 bit float, no en el archivo fijo ya impreso

## 9. Contenido dislocado que sí pertenece a M02

* **Trampa del 0 VU aplicada a ondas musicales**

  * El material reitera fuera de la clase central que la equivalencia 0 VU = -18 dBFS no debe trasladarse automáticamente a música real.
  * Se insiste en que la estructura debe pensarse por promedio y densidad, no por una regla dogmática aislada.
* **Pérdida de resolución al exportar**

  * Aunque aparece en bloques de mastering, pertenece de lleno a este módulo porque explica qué ocurre en el último tramo del flujo de señal cuando se abandona el entorno float y se imprime a coma fija.
* **Split en SSL como decisión de flujo**

  * Aunque aparece asociado a ecualización/canales, en realidad es una decisión de arquitectura de recorrido de señal dentro del canal.
* **Overshoot de filtros**

  * Filtrar no siempre “baja” la exigencia dinámica.
  * La rotación de fase puede subir picos y cambiar el comportamiento del siguiente proceso.
  * Esto conecta directamente EQ/filtros con estructura de ganancia.
* **Arquitectura Mix Bus vs Master Fader**

  * Se propone que todos los subgrupos lleguen a un auxiliar de Mix Bus.
  * El Master Fader queda como control final físico y como hogar de herramientas de análisis que no deben alterar el proceso.
  * Esto afecta directamente el orden macro del flujo de señal.
* **Atajo visual del tercio del dibujo**

  * Aparece reforzado en clases posteriores como método práctico rápido para preparar tracks antes del procesamiento.
* **Compensación obligatoria de nivel en limitadores, maximizadores y procesos de mastering**

  * Aunque aparezca en etapas avanzadas, pertenece a M02 porque prolonga el mismo principio:

    * cualquier proceso que sube nivel debe compensarse para no engañarse ni desarmar la estructura.
* **Impedancia y factor de damping**

  * Aunque entra por el lado de la escucha, sigue siendo parte del flujo eléctrico y de la transferencia de nivel.
* **Irrelevancia de forzar el Mix Bus a -6 si el promedio está sano**

  * En clase posterior se corrige otra vez el mismo error:

    * no bajar toda la mezcla solo por perseguir un pico arbitrario si el promedio, el factor de cresta y la ausencia de clipping ya indican una estructura coherente.

## 10. Mapa de cobertura

* **Núcleo duro del módulo**

  * decibeles referenciados y fórmulas logarítmicas
  * niveles de señal: micrófono, línea, amplificación
  * preamplificación y relación señal/ruido
  * nivel operativo (+4 dBu / -10 dBV)
  * 0 VU, dBFS y relación entre promedio y pico
  * headroom en señales percusivas y no percusivas
  * lectura correcta de Peak vs VU/RMS
  * corrección previa al fader
  * gain staging activo
  * buses, auxiliares, envíos, subgrupos, VCA
  * prefader/postfader
  * PFL/AFL
  * clipping digital de entrada/salida
  * motor float interno vs límite fijo de conversión/exportación
* **Núcleo reforzado desde clases dislocadas**

  * calibración real de plugins analógicos
  * falsa universalidad de 0 VU = -18 dBFS
  * no perseguir -6 dBFS de pico como dogma
  * Mix Bus como arquitectura central de la sesión
  * compensación de salida en procesos que elevan nivel
  * Split en SSL como corrección de ruta
* **Complementos importantes**

  * regla visual del tercio del dibujo
  * overshoot de filtros y su impacto en procesos posteriores
  * regla 8:1 de impedancia y damping en auriculares
* **Tensiones o puntos que requieren formulación prudente posterior**

  * “0 VU = -18 dBFS”:

    * válido en contextos específicos
    * no universal
  * “dejar picos en -6 dBFS”:

    * útil como práctica frecuente
    * no estándar obligatorio
  * “grabar bajo está mal”:

    * depende del ruido de la cadena
  * “el pico manda”:

    * no necesariamente; el promedio y el contexto también mandan
  * “un plugin analógico responde como otro”:

    * falso; la calibración puede variar mucho

## 11. Trazabilidad principal por clases

* **Clase 1**

  * corrección temprana del mito de que estructura de ganancia equivale a poner picos en -18
  * primer refuerzo de la trampa de 0 VU aplicado a señal musical
* **Clase 3**

  * regla 8:1 de impedancia
  * relación entre salida de auriculares, damping y respuesta final
* **Clase 4**

  * base matemática y eléctrica del módulo
  * dB referenciados
  * fórmulas de potencia y voltaje
  * referencias 0 dBW, dBm, dBV, dBu, dBFS
  * niveles de micrófono, línea y amplificación
  * +4 dBu vs -10 dBV
  * clipping digital de entrada/salida
  * preamplificador
  * regla “línea con línea”
  * corrección de mitos sobre conectores y master por encima de 0
* **Clase 6**

  * estructura práctica de ganancia en mezcla
  * procesos vs efectos
  * bus vs auxiliar
  * prefader/postfader
  * headroom percusivo
  * no usar fader para arreglar entrada
  * PFL/AFL
  * saturación en subgrupos
  * Trim, Clip Gain y VCA
  * primer desarrollo fuerte del gain staging activo
* **Clase 7**

  * medición correcta según tipo de material
  * Peak vs VU/RMS
  * relación señal/ruido y grabación baja
  * tercio del dibujo
  * compensación de salida de plugins
  * medición de calibración de plugins analógicos
  * excepción extrema del Summit TLA-100A
  * corrección del tratamiento de picos aislados
* **Clase 8**

  * refuerzo del uso de medidores RMS/VU y Peak
* **Clase 11**

  * overshoot de filtros y efecto sobre procesos posteriores
* **Clase 12**

  * corrección del error de bajar una mezcla sana solo por un pico que no llega a clipping
  * relevancia del promedio y del factor de cresta
* **Clase 14**

  * Split en SSL
  * nueva demostración de 0 VU con onda compleja
  * refuerzo de calibración no universal
* **Clase 21**

  * Mix Bus vs Master Fader
  * consolidación del tercio del dibujo como atajo práctico
* **Clase 22**

  * refuerzo del tercio del dibujo
* **Clase 25**

  * mantener nivel de grabación consistente en un álbum
  * diferencia entre motor float y exportación fixed-point
  * pérdida de 1 bit al bajar 6 dB en bounce
  * demolición del mito de entregar a -6 por obligación
* **Clase 27**

  * compensación obligatoria de nivel en limitadores/maximizadores
  * extensión del gain staging activo a etapas avanzadas del flujo
