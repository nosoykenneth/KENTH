---

course_id: mezcla_masterizacion_kenth
module_id: M04
module_order: 4
module_title: Filtros y ecualización
module_slug: filtros-ecualizacion
doc_type: source_dossier
source_origin: author_compiled_from_transcripts
filename: M04_dossier_fuente.md
version: 0.1
status: draft_source_compilation
curation_source: extraccion_exhaustiva_notebooklm_desde_clases_definitivas
ready_for_indexing: false
-------------------------

# M04 — Dossier fuente exhaustivo

## Filtros y ecualización

> Este documento NO es guia canonica.
> NO es FAQ.
> NO es glosario final.
> Es una fuente intermedia exhaustiva, reorganizada por modulo, construida a partir de clases definitivas corregidas.
> Su objetivo es preservar detalle, matices, ejemplos, advertencias y trazabilidad antes de condensar doctrina para el RAG.

## 1. Alcance del dossier

* Este módulo reúne la doctrina, los ejemplos, las advertencias y los procedimientos sobre:

  * filtros de corte y su lógica real de funcionamiento,
  * ecualización de campana, shelving, tilt, notch y variantes dinámicas,
  * relación entre pendiente, polos, Q, ancho de banda y frecuencia central,
  * consecuencias temporales y eléctricas del filtrado y de la ecualización,
  * usos correctivos, tonales, quirúrgicos, musicales y contextuales,
  * comportamiento de ecualizadores digitales y modelados analógicos,
  * cruces de banda, crossovers, división espectral y reconstrucción,
  * herramientas específicas mencionadas por el profesor,
  * contenidos adelantados, tardíos o dislocados que pertenecen claramente al mismo núcleo técnico.

* El núcleo fuerte del módulo está concentrado principalmente en clases 11, 12, 13 y 14, pero también incorpora contenido relevante aparecido en:

  * clase 1,
  * clase 9,
  * clase 15,
  * clase 18,
  * clase 19,
  * clase 21,
  * clase 23,
  * clase 24,
  * clase 26,
  * clase 27,
  * clase 28.

* Este dossier conserva:

  * definiciones técnicas,
  * reglas operativas,
  * fórmulas,
  * valores numéricos,
  * demostraciones del profesor,
  * advertencias severas,
  * preguntas de estudiantes que corrigen errores de enfoque,
  * ejemplos concretos de sesiones,
  * matices donde el docente aclara que algo depende del contexto.

* Este dossier no convierte todavía el material en:

  * doctrina final cerrada,
  * lista de presets,
  * receta universal,
  * pedagogía simplificada,
  * resumen elegante a costa de detalle.

## 2. Núcleo conceptual del módulo

* **Filtro Butterworth**

  * Es la base de referencia del curso.
  * Se presenta como el diseño de filtro que cubre el 99,9% del uso cotidiano en DAWs, consolas y plugins comunes.
  * El marco práctico del módulo asume esta lógica de respuesta como estándar operativo.

* **Frecuencia de corte en filtros**

  * No es el punto visual donde “empieza a caer” la curva.
  * Es el punto exacto donde la salida ya cayó **3 dB** respecto a la entrada.
  * Ese punto equivale a **mitad de potencia**.
  * Esto cambia la forma correcta de interpretar el daño o alcance real del filtro sobre el contenido vecino.

* **Pendiente y polos**

  * La pendiente define qué tan gradual o abrupta es la atenuación.
  * Se expresa en **dB por octava**.
  * Cada polo equivale matemáticamente a **6 dB/octava**.
  * Ejemplo reforzado en clase:

    * 1 polo = 6 dB/oct,
    * 2 polos = 12 dB/oct,
    * 3 polos = 18 dB/oct,
    * 4 polos = 24 dB/oct.

* **Frecuencia de corte en shelving**

  * No se interpreta igual que en filtros de corte.
  * Según fabricante o diseño:

    * puede ser el punto donde se alcanza **la mitad de la ganancia total asignada**, o
    * el punto que queda **3 dB por debajo de la meseta** del shelf.
  * El profesor lo presenta como una convención que cambia entre diseños, especialmente en emulaciones analógicas.

* **Campana / Peak / Bell**

  * El ancho de banda real no se define por donde la curva vuelve a ganancia unidad.
  * Se define por las dos frecuencias **F1** y **F2** donde la respuesta cae **3 dB respecto al pico**.
  * Si el pico está en +9 dB, el ancho de banda se mide donde la curva llega a +6 dB a ambos lados.
  * La frecuencia central no es media aritmética:

    * es la **media geométrica**,
    * **Fc = √(F1 × F2)**.
  * Fórmula asociada:

    * **Q = Frecuencia Central / Ancho de Banda**,
    * donde ancho de banda = **F2 - F1**.

* **Q / factor de calidad**

  * Define el grado de concentración o resonancia de la banda de intervención.
  * No es la pendiente.
  * En campanas, el profesor lo trabaja como control del ancho/selectividad.
  * En filtros, su existencia real depende del diseño y de la cantidad de polos.

* **Rotación de fase por filtros y ecualización IIR**

  * Todo filtro IIR, sea filtro de corte o shelving, rota fase al alterar amplitud.
  * En la frecuencia de corte:

    * cada polo rota **45°**,
    * 12 dB/oct = **90°**,
    * 24 dB/oct = **180°**.
  * Esta rotación reordena internamente la onda compleja.

* **Overshot / sobreimpulso**

  * Al filtrar, especialmente con high-pass, los picos pueden subir aunque se esté quitando contenido espectral.
  * El RMS o la energía total pueden mantenerse estables o bajar, mientras el pico sube.
  * El fenómeno se atribuye a:

    * rotación de fase,
    * reordenamiento temporal interno,
    * overshot propio del diseño del filtro.

* **Fase lineal**

  * Evita la rotación relativa de fase entre frecuencias.
  * Lo logra reordenando la energía en el tiempo para que todas las frecuencias salgan sincronizadas.
  * Costos fuertes asociados:

    * latencia muy alta,
    * **pre-ringing**,
    * posible ensuciamiento del ataque en material transiente.
  * El módulo no la presenta como superior por defecto, sino como otro tipo de compromiso.

* **Pre-ringing**

  * Artefacto donde aparece energía oscilatoria artificial **antes** del transitorio.
  * Se plantea como uno de los daños más serios de la fase lineal, especialmente en material muy percusivo.

* **Tres motivos técnicos para usar un filtro**

  * **Protección técnica/térmica**

    * control de subsónicas,
    * excursiones,
    * headroom del sistema,
    * fatiga de parlantes.
  * **Atenuar lo que está por debajo del registro útil**

    * quitar basura que no aporta musicalmente al instrumento.
  * **Atenuar dentro del registro del instrumento lo que estorba a otro elemento**

    * uso contextual,
    * no aislado,
    * orientado a convivencia en mezcla.

* **Ecualización correctiva**

  * Parte de la lógica: “tengo un problema”.
  * Busca:

    * resonancias molestas,
    * desbalances,
    * enmascaramientos,
    * sectores ofensivos.
  * Suele ser:

    * sustractiva,
    * estrecha,
    * quirúrgica,
    * transparente.

* **Ecualización tonal / estética**

  * Parte de la lógica: “me gustaría que…”.
  * Busca:

    * cuerpo,
    * aire,
    * color,
    * presencia,
    * balance general.
  * Suele ser:

    * aditiva,
    * ancha,
    * musical,
    * apoyada en shelving o curvas de carácter.

* **Ecualización dinámica**

  * Se usa cuando el problema frecuencial es **ocasional** o intermitente.
  * Opera con umbral y rango de acción.
  * Se activa solo cuando esa banda supera el límite fijado.

* **Ecualización estática**

  * Se usa cuando el problema es **permanente**.
  * El recorte o realce queda fijo.

* **Ecualizador dinámico vs compresor multibanda**

  * El multibanda:

    * divide por **crossovers**,
    * trabaja regiones más rígidas del espectro,
    * usa ratios.
  * El ecualizador dinámico:

    * usa campanas o shelves dinámicos,
    * no requiere crossovers para funcionar,
    * trabaja zonas más localizadas,
    * suele gobernarse por **range**.

* **Ecualizadores simétricos**

  * La forma del boost y del cut es la misma, espejada.

* **Ecualizadores asimétricos**

  * En modelados analógicos:

    * el corte suele cerrarse más y ser más selectivo,
    * el boost suele abrirse más y ser más musical.
  * Esta asimetría se presenta como una de las bases del “carácter”.

* **Q constante**

  * La anchura de la campana no cambia al variar la ganancia.

* **Q proporcional**

  * Al subir o bajar más ganancia, la campana se afila y estrecha.

* **Tipos de ecualizador analógico**

  * **Gráfico**

    * el fabricante fija frecuencia y ancho,
    * el usuario mueve ganancia.
  * **Semiparamétrico**

    * el usuario controla frecuencia y ganancia,
    * el ancho viene predeterminado.
  * **Paramétrico**

    * control total de frecuencia, ganancia y Q.

* **Filtro All-Pass / pasa-todo / rotor de fase**

  * No corta frecuencias.
  * No modifica amplitud.
  * Reordena la relación de fase en torno a una zona y sus adyacencias.
  * Su función en el módulo aparece ligada a:

    * corrección de asimetrías,
    * recuperación de headroom acústico,
    * manipulación de la simetría de la onda sin ecualizarla.

* **Curva Tilt**

  * Curva suave de pivote.
  * Si sube graves, baja agudos; si sube agudos, baja graves.
  * Se presenta como muy útil en mastering y balance tonal porque permite sensación de mayor grave **por contraste**, sin inyectar tanta energía real en el low-end.

* **Pultec EQP-1A**

  * Ecualizador pasivo y de programa.
  * “Valvular” por la etapa de ganancia posterior que compensa la pérdida del circuito pasivo.
  * La “curva Pultec” en graves no es una resonancia simple:

    * combina un **boost** en campana con una **attenuate** tipo shelf sobre la misma zona,
    * realza la fundamental y limpia la vecina superior.

## 3. Distinciones clave del módulo

* **Filtro real vs muro ideal**

  * El módulo insiste en que un filtro estándar no es un brickwall perfecto.
  * Elegir 1000 Hz no significa que todo lo de abajo desaparece y todo lo de arriba queda intacto.
  * Siempre hay transición gradual definida por pendiente.

* **Pendiente vs Q**

  * No son el mismo parámetro.
  * La pendiente define caída por octava.
  * El Q define resonancia/ancho/selectividad.
  * El profesor corrige que algunos plugins usan mal el mando “Q” para endurecer la pendiente y eso genera hábito conceptual incorrecto.

* **6 dB/oct vs 12 dB/oct o más**

  * En 6 dB/oct no hay control real de Q según la lógica explicada.
  * Para controlar resonancia/Q se requiere, como mínimo, estructura de **2 polos**.

* **Frecuencia de corte en filtros vs frecuencia de corte en shelving**

  * En filtros:

    * punto de **-3 dB** respecto a entrada.
  * En shelves:

    * mitad de ganancia asignada o 3 dB por debajo de la meseta, según diseño.

* **Campana correctiva vs shelving tonal**

  * La campana aparece asociada al trabajo de:

    * localizar,
    * aislar,
    * recortar,
    * corregir.
  * El shelving aparece asociado al trabajo de:

    * cuerpo,
    * aire,
    * inclinación del balance,
    * color general.

* **Ecualización correctiva vs estética**

  * Correctiva:

    * “hay un problema”.
  * Estética:

    * “me gustaría que…”.
  * El módulo separa ambas lógicas para evitar confundir cirugía con color.

* **Ecualización estática vs dinámica**

  * Estática:

    * problema permanente.
  * Dinámica:

    * problema ocasional.
  * Ejemplos recurrentes:

    * sibilancia,
    * platillos intermitentemente ofensivos,
    * estridencia vocal puntual.

* **Ecualizador dinámico vs multibanda**

  * Multibanda:

    * bandas divididas por crossovers,
    * ratios,
    * arquitectura de compresión por zonas.
  * Dynamic EQ:

    * bandas localizadas,
    * campanas o shelves,
    * control más fino y menos rígido del espectro.

* **Digital transparente vs analógico/modelado**

  * El ecualizador digital moderno se presenta como:

    * inmaculado,
    * preciso,
    * quirúrgico,
    * ideal para corrección.
  * El modelado analógico se presenta como:

    * más musical en muchos casos,
    * más orgánico,
    * no necesariamente exacto matemáticamente,
    * útil por color, forma de curva, THD o comportamiento asimétrico.

* **API vs Neve**

  * API:

    * transiente muy rápida,
    * “patada en el estómago” en graves,
    * brillo que puede volverse “navaja”.
  * Neve:

    * grave más pesado, de “empujón”,
    * agudo más sedoso,
    * clásicamente descrito como “seda”.

* **Q constante vs Q proporcional**

  * Q constante:

    * el ancho no cambia con la ganancia.
  * Q proporcional:

    * cuanto mayor la intervención, más angosta se vuelve la campana.

* **Simétrico vs asimétrico**

  * Simétrico:

    * boost y cut son espejo.
  * Asimétrico:

    * la topología cambia la forma según si suma o resta.

* **Low shelf negativo vs high-pass**

  * Se corrige el mito de que el shelf “salva la fase”.
  * Ambos, si son IIR, rotan fase al alterar amplitud.
  * La diferencia no es que uno preserve fase y otro no, sino su forma de intervención.

* **DC Offset vs asimetría**

  * **DC Offset**

    * corriente continua parásita,
    * frecuencia de 0 Hz,
    * desplaza toda la onda del centro,
    * se corrige con HPF muy bajo.
  * **Asimetría**

    * la onda está centrada,
    * pero los picos se cargan hacia un lado,
    * proviene de relación interna de fase entre armónicos,
    * se corrige con all-pass, no con HPF.

* **HPF/LPF estándar vs Linkwitz-Riley**

  * Un HPF y LPF estándar, cortando ambos a -3 dB en el mismo punto, no reconstruyen neutralmente al recombinarse.
  * Generan refuerzo y problemas de fase.
  * Para reconstrucción correcta, el módulo exige cruce **Linkwitz-Riley** a **-6 dB** y, preferiblemente, fase lineal.

* **Filtro audible vs filtro en sidechain**

  * Un filtro puede usarse para alterar el audio escuchado.
  * También puede usarse solo en el detector de dinámica para que el compresor “vea” ciertas zonas y ignore otras.
  * Esto pertenece al módulo como extensión de la lógica de filtrado dentro de circuitos de control.

## 4. Filtros, ecualización y lógica de intervención

* **Lógica general de decisión**

  * El módulo se opone al filtrado por costumbre.
  * Primero se analiza.
  * Luego se decide si:

    * hay basura subsónica real,
    * hay material fuera del registro útil,
    * existe enmascaramiento contextual,
    * existe riesgo térmico o de excursión,
    * existe problema permanente o solo ocasional.

* **Criterio para no filtrar por reflejo**

  * Si la basura está **20 a 30 dB** por debajo de la fundamental útil, se presenta como inofensiva.
  * Si no molesta térmicamente ni genera problema real, no hace falta filtrar.
  * Esta regla se usa para desmontar el hábito de poner HPF a todos los canales “por las dudas”.

* **Tres razones operativas para filtrar**

  * **Protección**

    * controlar subgraves inútiles,
    * proteger parlantes,
    * ganar headroom útil.
  * **Limpieza por debajo del registro**

    * sacar lo que el instrumento no necesita.
  * **Espacio contextual**

    * abrir hueco a otro instrumento sin mutilar todo el espectro.

* **Intervenir en contexto y no en solo**

  * Para decisiones de convivencia entre instrumentos, el módulo insiste en escuchar la mezcla entera.
  * Ejemplo reiterado:

    * para saber dónde la guitarra ensucia al bajo, se busca con filtro invertido en contexto.

* **Método de barrido aditivo**

  * Se arma una campana de **+10 dB**.
  * Se barre desde fuera del problema hacia adentro.
  * Cuando el defecto “sale al frente”:

    * se cierra el Q,
    * se hace un barrido más fino,
    * luego se revierte a corte razonable.
  * La justificación perceptiva dada:

    * **10 dB** se perciben aproximadamente como el doble de volumen.

* **Uso del filtro invertido para diagnóstico contextual**

  * En vez de cortar a ciegas:

    * se realza la zona sospechosa,
    * se escucha en contexto dónde el instrumento estorba,
    * se revierte el movimiento a sustractivo.
  * El módulo lo usa para trabajo de guitarras frente al bajo.

* **Orden de inserción recomendado**

  * Primeros slots:

    * EQ correctiva,
    * digital,
    * transparente,
    * sustractiva.
  * Slots posteriores:

    * EQ tonal,
    * consolas analógicas,
    * curvas amplias,
    * color.
  * En SSL:

    * se recomienda alterar el flujo con **Split** para que la ruta quede **Entrada -> Filtros -> Dinámica -> EQ**,
    * evitando que el compresor reaccione a graves que de todas formas luego serán cortados.

* **Pendientes suaves como criterio general**

  * Se favorecen pendientes de **6 a 12 dB/oct** cuando el objetivo es musicalidad y naturalidad.
  * Las pendientes muy agresivas se tratan como herramientas excepcionales o de diagnóstico, no como norma de mezcla tonal.

* **Shelving como segunda etapa**

  * Se valida su uso como etapa posterior a la corrección quirúrgica.
  * Se lo ubica en la lógica de balance tonal y musicalidad.

* **Tilt como herramienta tonal inteligente**

  * Cuando la mezcla necesita “más grave”, el módulo propone muchas veces inclinar el balance antes que inyectar low-end real.
  * Se usa para:

    * aumentar sensación de peso,
    * no disparar innecesariamente al limitador,
    * conservar headroom.

* **Ecualización dinámica como corrección temporal**

  * Se reserva para eventos intermitentes.
  * La lógica es no destruir todo el material por corregir un fenómeno que aparece solo a ratos.

* **Cruce de bandas como operación delicada**

  * Cuando se parte una señal en grave/agudo, el módulo no lo trata como una ecualización simple.
  * Lo trata como un problema de reconstrucción matemática y de suma acústica.
  * De ahí el énfasis en Linkwitz-Riley y fase lineal.

* **Filtro en sidechain**

  * Se usa para que el detector del compresor responda a ciertas bandas y no a otras.
  * Ejemplo expuesto:

    * aislar la zona media de una trompeta para disparar compresión del conjunto sin ecualizar la salida audible.
  * Se integra aquí como uso funcional del filtrado fuera de la corrección tonal directa.

* **Tilt antes del detector**

  * En el API 2500 aparece la curva Tilt en el detector como forma de quitar peso a graves y hacer que la compresión reaccione más naturalmente a medios/agudos.
  * Se presenta como uso avanzado de una lógica de ecualización aplicada a balística, no a tono directo.

## 5. Ejemplos técnicos que no deben perderse

* **Demostración de overshot con ruido blanco**

  * Se envía ruido blanco a **-20 dB**.
  * Se inserta un High-Pass de **24 dB/oct** en **20 Hz**.
  * Resultado mostrado:

    * el pico de salida sube a **-14.6 dB**,
    * el RMS se mantiene en **-23.1**.
  * La conclusión del profesor:

    * se está sacando información,
    * pero el pico sube por reorganización temporal y rotación de fase,
    * no porque la señal tenga más energía útil ni “suene más fuerte”.

* **Ejemplo de bombo**

  * Fundamental referida: **45-50 Hz**.
  * Se coloca HPF en **24 Hz a 18 dB/oct**.
  * La intención:

    * no tocar la parte útil,
    * remover basura subsónica,
    * preservar la envolvente general.

* **Ejemplo de tambor**

  * Fundamental referida: **230 Hz**.
  * Se observa una “V” en **31 Hz**.
  * Se filtra en **100 Hz** copiando la envolvente.
  * La lógica:

    * la señal útil queda a la derecha,
    * lo subsónico queda a la izquierda,
    * el corte se decide por lectura combinada de analizador y criterio musical.

* **Ejemplo de bajo**

  * Fundamental referida: **41 Hz**.
  * Ejemplo operativo: HPF en **20 Hz a 18 dB/oct**.
  * Este valor aparece como ejemplo pedagógico y no como preset universal.

* **Ejemplo de guitarra acústica base**

  * HPF referido en **45 Hz**.
  * Se usa como caso de preservar lo útil y limpiar lo que no corresponde al registro real.

* **Ejemplo de guitarra de arreglo / contextual**

  * Se usa filtro invertido para detectar dónde ensucia al bajo.
  * El punto hallado en el ejemplo es **285 Hz**.
  * Luego se invierte a corte.
  * Además se añade un **Low-Pass** para empujar la guitarra hacia atrás en el plano espacial.
  * También aparecen referencias de HPF en **160 Hz** o **285 Hz** según la función de la guitarra dentro del arreglo.

* **Ejemplo de hi-hat / platos**

  * HPF muy suave en **80 Hz a 6 dB/oct**.
  * Se usa como ejemplo de pendiente leve y comportamiento musical.

* **Cálculo de campana**

  * Si se aplican **+9 dB en 500 Hz**:

    * el ancho de banda se mide donde la curva cae a **+6 dB**,
    * la frecuencia central no se saca por promedio aritmético,
    * sino por media geométrica.

* **Construcción del crossover perfecto para bajo**

  * El módulo demuestra que usar HPF + LPF estándar en la misma frecuencia:

    * refuerza la zona de cruce,
    * falla la prueba nula,
    * introduce problema de fase.
  * Solución expuesta:

    * Linkwitz-Riley,
    * cruce a **-6 dB**,
    * duplicación de filtros,
    * fase lineal para reconstrucción perfecta.

* **Curva Pultec en graves**

  * Aplicar simultáneamente **Boost** y **Attenuate** en la misma frecuencia baja, por ejemplo **60 Hz**.
  * Resultado descrito:

    * gran realce en la fundamental,
    * valle o ahuecamiento inmediato en la zona vecina superior,
    * se menciona como ejemplo una limpieza alrededor de **600 Hz**.
  * La fuente la trata como asimetría propia del circuito, no como una resonancia común.

* **Tilt para sensación de más graves**

  * En vez de sumar low shelf de forma bruta:

    * se bajan sutilmente los agudos,
    * el grave se percibe mayor por contraste,
    * se evita castigar de más al limitador.

* **Pseudo-ecualizador multibanda para espacialidad**

  * Se crea desde ruteo y filtros, no desde un plugin multibanda convencional.
  * Procedimiento expuesto:

    * track a bus muerto,
    * tres envíos prefader,
    * separación por filtros:

      * graves,
      * medios,
      * agudos.
  * Referencias de bandas del ejemplo:

    * graves: hasta **200 Hz**,
    * medios: **200 Hz – 2 kHz**,
    * agudos: desde **2 kHz**.
  * Tratamientos posteriores del ejemplo:

    * medios con trémolo y reverb,
    * agudos con ping pong delay,
    * graves con sidechain respecto al bajo.

* **Matriz Mid/Side con EQ correctiva y estética**

  * Para una intro de bolero:

    * se codifica a M/S,
    * en Mid se usa **C4** cerrando una banda en **1.3–1.5 kHz** con range negativo para calmar sostenidos vocálicos tensos,
    * en Side se usa **Pultec EQP-1A** para subir brillo y aire a platos y guitarras, preservando intacta la opacidad de la voz en el centro.
  * Se presenta como ejercicio de alto valor práctico dentro del módulo.

## 6. Preguntas de estudiantes que sí aportan contenido

* **“¿Es mayor en volumen o se agota la señal o qué pasa?”**

  * Surge al ver que el pico sube cuando se filtra ruido blanco.
  * Aporta porque obliga al docente a precisar:

    * sube el nivel de pico,
    * no sube el RMS,
    * no equivale a más volumen promedio,
    * el fenómeno es físico y medible en el medidor.

* **“¿No conviene poner directamente un filtro en el Mix Bus/Master para controlar el low-end?”**

  * Aporta porque el profesor responde negativamente como criterio general.
  * La aclaración:

    * si podía limpiarse en cada pista según su registro, llegar con basura al master es un error de base,
    * el master no debería cargar restos evitables de guitarras, violines u otras pistas que ya podían haberse ordenado antes.

* **“¿Por qué en un filtro de 6 dB por octava no se puede ajustar el Q?”**

  * Aporta porque fija la separación entre:

    * pendiente,
    * estructura de polos,
    * posibilidad matemática de resonancia/Q.
  * Refuerza la idea de que 6 dB/oct no ofrece ese control.

* **“¿Es un error exagerar la ganancia buscando una frecuencia problemática?”**

  * Aporta porque valida el barrido aditivo fuerte como herramienta de localización.
  * El profesor lo respalda con el valor de **+10 dB** para hacer que el problema dé “un paso al frente”.

* **“¿Se puede usar un shelving como segunda etapa de ecualización?”**

  * Aporta porque ordena el flujo:

    * primero campana correctiva,
    * después shelving tonal.

## 7. Advertencias, matices y correcciones del profesor

* **Pendientes muy abruptas**

  * Se advierte contra usar **48 o 96 dB/oct** por defecto.
  * Razones dadas:

    * no suenan naturales,
    * no representan comportamiento acústico habitual,
    * generan overshot severo,
    * producen mucha rotación de fase,
    * entran en resonancia fuerte e inarmónica en la frecuencia de corte.
  * El módulo favorece pendientes suaves como regla general de musicalidad.

* **La falacia de la “mezcla Tetris”**

  * El profesor rechaza filtrar violentamente todos los elementos para que encajen como piezas que no se tocan.
  * La crítica de fondo:

    * se destruye el tejido natural entre instrumentos,
    * luego resulta contradictorio querer “pegar” todo con compresión glue después de haber roto esa interacción.

* **Ecualizar después de alinear baterías**

  * Si se alineó milimétricamente un kit para evitar comb filtering, insertar EQ IIR después vuelve a alterar la relación temporal.
  * El módulo lo trata como advertencia severa sobre orden de trabajo y consecuencias invisibles de la EQ.

* **Fase lineal no equivale a solución perfecta**

  * Evita un daño, pero introduce otros:

    * latencia grande,
    * pre-ringing.
  * El criterio expresado es que a veces hay que elegir qué daño asumir.
  * Se sugiere prudencia especial en material transiente y en zonas centrales delicadas.

* **Pultec en agudos, modo Sharp**

  * Advertencia severa.
  * Si se combinan:

    * boost agudo alto,
    * attenuate alta,
    * ancho en modo **Sharp**,
  * la curva se comporta como un pasabajos hiperresonante.
  * Riesgo descrito:

    * fatiga extrema,
    * pico muy concentrado de **+20 a +25 dB**,
    * daño físico posible al tweeter.

* **No filtrar “por las dudas”**

  * Filtrar por precaución en mastering o mezcla no es ley.
  * Puede:

    * robar headroom,
    * elevar picos,
    * obligar al limitador a trabajar más,
    * no aportar mejora audible real.
  * Se insiste en:

    * primero analizar,
    * luego decidir.

* **No confundir low shelf con solución “sin daño de fase”**

  * El módulo desmonta ese mito.
  * Todo IIR que modifica amplitud rota fase.

* **No creer que plugins digitales nativos “no sirven”**

  * El profesor corrige ese prejuicio.
  * Su neutralidad se presenta como ventaja estructural para cirugía.

* **No ecualizar mirando la serigrafía**

  * En hardware clásico y modelados:

    * el número de la perilla no garantiza exactitud matemática,
    * puede haber actuación colateral,
    * tolerancias y redes de diseño alejan la acción real de lo que parece impreso.
  * La consigna explícita es escuchar, no fiarse del dibujo.

* **No confundir necesidad de mucha cirugía con virtud de mezcla**

  * Si se requieren docenas de notch muy estrechos, el módulo lo interpreta como síntoma de mala fuente:

    * mala microfonía,
    * mala sala,
    * mala librería,
    * mala captura.
  * Se repite la idea:

    * no hay nada que compita con grabar bien.

* **No aceptar ciegamente automatismos**

  * El botón **Learn** en crossovers puede ubicar técnicamente bien los cruces en valles espectrales.
  * Pero eso no garantiza que sean los puntos musicales útiles para la intención del operador.

* **No usar valores de ejemplo como preset**

  * El módulo da varios números de HPF, pendientes y frecuencias.
  * Se deben conservar como ejemplos de criterio, no como reglas universales fijas.

* **No confundir DC Offset con asimetría**

  * Pueden parecerse visualmente.
  * El tratamiento correcto es distinto.
  * Corregir uno con la herramienta del otro es error de laboratorio.

## 8. Herramientas, referencias técnicas, configuraciones y detalles operativos

* **FabFilter Pro-Q 3 / Pro-Q 4**

  * Referencia principal de EQ digital transparente y quirúrgica.
  * Se destaca porque:

    * separa correctamente Q y pendiente,
    * ofrece fase lineal,
    * en Pro-Q 4 se mencionan funciones de ecualización dinámica con ataque y release.
  * Aparece como herramienta fuerte para corrección.

* **Waves Q1 / Q10**

  * Presentados como EQ digitales.
  * La línea gris se describe como aséptica y digital.

* **Waves Renaissance EQ**

  * Presentado como más musical y resonante.
  * Se le atribuyen curvas tipo “S” y comportamiento más cercano a lo analógico.

* **Bertom Curve Analyzer**

  * Se inserta antes y después de un procesador para observar la curva real.
  * Sirve para ver qué está haciendo realmente el EQ o filtro sin depender del ruido blanco.

* **Soothe / iZotope Ozone**

  * Se mencionan como herramientas válidas para resonancias o trabajo espectral.
  * La advertencia asociada:

    * no usar por defecto,
    * no usar con presets ciegos,
    * primero confirmar problema real.

* **API 560**

  * Ejemplo de EQ gráfico.

* **API 550A / 550B**

  * Semiparamétricos.
  * Rasgos asociados:

    * no solapamiento en ciertos diseños,
    * trabajo por pasos que facilita recall,
    * carácter de transiente muy veloz.

* **Neve 1073 / 1084 / 1081**

  * Asociados a:

    * pesadez en graves,
    * agudos sedosos,
    * compresión armónica agradable.
  * Se menciona **Lindell Serie 80** como emulación destacada con tecnología **TMT** y control **THD**.

* **Harrison 32C**

  * Semiparamétrico.
  * Presentado como extremadamente musical.
  * Soporta movimientos grandes sin sonar mal.
  * Se lo compara con un “autopolish” o “revividor”.

* **Pultec EQP-1A**

  * EQ pasivo de programa.
  * Fuerte en extremos del espectro.
  * Relevante por:

    * curva Pultec en graves,
    * riesgos de su zona aguda en modo Sharp.

* **Pultec MQ-5**

  * Se menciona como alternativa ligada a medios y a una lógica de curva “smile”.

* **Warming de Kiive Audio**

  * Se menciona como alternativa gratuita en el contexto Pultec.

* **C4**

  * Aparece en trabajo Mid/Side como herramienta de control correctivo de una banda vocal en 1.3–1.5 kHz.

* **iZotope RX**

  * Se menciona para diagnóstico de estadísticas de forma de onda en el análisis de DC Offset y asimetría.

* **API 2500**

  * Se menciona por el uso de curva Tilt en el detector.

* **Configuraciones y detalles operativos clave**

  * **Q y pendiente**

    * 6 dB/oct no ofrece control real de Q según el marco expuesto.
  * **Fase lineal**

    * reservarla para usos justificados,
    * validar en material percusivo,
    * asumir latencia y pre-ringing.
  * **SSL Split**

    * mover filtros antes del detector/dinámica en el flujo del canal cuando corresponda.
  * **Linkwitz-Riley**

    * para split correcto:

      * cruce a -6 dB,
      * duplicación de filtros,
      * preferencia por fase lineal.
  * **Band-pass abrupto como diagnóstico**

    * se usa incluso con **48 dB/oct** para aislar bandas en problemas de correlación/fase, no como regla de mezcla tonal.
  * **Filtro All-Pass**

    * validación auditiva obligatoria,
    * porque reordenar armónicos puede corregir asimetría, pero también alterar timbre si se usa sin control.

## 9. Contenido dislocado que sí pertenece a M04

* **Clase 1 — demostración adelantada de overshot**

  * Se muestra antes del núcleo del módulo que filtrar puede elevar picos aunque se quite información.
  * Queda como una de las pruebas físicas más importantes del curso sobre consecuencias del filtrado.

* **Clase 9 — filtro pasabanda abrupto para diagnóstico de fase**

  * Uso de band-pass de alta pendiente antes de correlatómetros.
  * Sirve para aislar visualmente bandas conflictivas que quedarían enmascaradas por la dominancia del grave.
  * Es complemento de diagnóstico, no recomendación tonal de mezcla.

* **Clase 15 — frontera entre EQ dinámica y procesadores dinámicos**

  * Diferencia entre multibanda y dynamic EQ.
  * Uso de filtros en sidechain del compresor.
  * Pertenece al módulo porque extiende la lógica de filtrado/ecualización al circuito de control dinámico.

* **Clase 18 — tilt en detector del API 2500**

  * Uso de curva Tilt previa al detector para que el compresor no sea dominado por graves.
  * Complementa el uso tonal de Tilt con una aplicación balística.

* **Clase 19 — regla temporal de EQ estática vs dinámica**

  * Se incorpora como núcleo porque establece el criterio de elección según permanencia o intermitencia del problema.

* **Clase 21 — orden de inserción**

  * Reafirma que la corrección sustractiva va antes y la coloración/tono después.

* **Clase 23 — pseudo multibanda por ruteo**

  * Fraccionamiento del espectro con filtros para diseño espacial.
  * Complemento práctico de alto valor por mostrar que el módulo no se limita a “limpiar”, sino también a diseñar movimiento y profundidad.

* **Clase 24 — crossover perfecto / split**

  * Núcleo fuerte del módulo.
  * Demuestra que dividir y recombinar no es trivial.
  * Introduce Linkwitz-Riley y fase lineal como condiciones de reconstrucción correcta.

* **Clase 26 — mastering, all-pass, DC Offset, Learn**

  * Refuerza:

    * que filtrar por defecto en mastering puede ser contraproducente,
    * la diferencia radical entre HPF y All-Pass,
    * el criterio de prudencia frente al botón Learn en crossovers.
  * Es uno de los aportes más técnicos y de laboratorio del módulo.

* **Clase 27 — refuerzo del uso de Tilt**

  * Reaparece la lógica de inclinar el balance como corrección eficiente del peso percibido.

* **Clase 28 — Mid/Side con EQ correctiva y estética**

  * Núcleo práctico avanzado del módulo.
  * Integra:

    * EQ dinámica,
    * Pultec,
    * M/S,
    * separación entre centro y lados,
    * corrección y embellecimiento en paralelo dentro de una misma estrategia.

## 10. Mapa de cobertura

* **Definiciones y fundamentos**

  * Butterworth.
  * Frecuencia de corte en filtros.
  * Frecuencia de corte en shelving.
  * Pendiente, polos.
  * Ancho de banda, frecuencia central, Q.
  * Rotación de fase por polo.
  * Fase lineal y pre-ringing.

* **Tipologías y comportamientos**

  * HPF / LPF.
  * Bell / Peak.
  * Shelving.
  * Tilt.
  * Notch.
  * All-Pass.
  * Band-pass.
  * Simétrico vs asimétrico.
  * Q constante vs proporcional.
  * Gráfico / semiparamétrico / paramétrico.

* **Lógica de intervención**

  * Protección técnica.
  * Limpieza bajo registro útil.
  * Espacio contextual.
  * Corrección vs tono.
  * Estática vs dinámica.
  * EQ dinámica vs multibanda.
  * Corrección primero, color después.

* **Fenómenos y riesgos**

  * Overshot.
  * Rotación de fase.
  * Desalineación de batería tras ecualizar.
  * Pre-ringing.
  * Resonancia inarmónica por pendientes extremas.
  * Riesgo físico de tweeter con Pultec Sharp.
  * Pérdida de headroom por filtrado “por las dudas”.

* **Diagnóstico**

  * V corta subsónica.
  * Barrido aditivo.
  * Diagnóstico contextual con filtro invertido.
  * Mala microfonía detectada por exceso de notch.
  * DC Offset vs asimetría.
  * Serigrafía imprecisa de hardware.
  * Pasabanda abrupto antes de correlator.

* **Aplicaciones específicas**

  * Bombo.
  * Tambor.
  * Bajo.
  * Guitarras.
  * Hi-hat / platos.
  * Split de bajo.
  * Diseño espacial multibanda.
  * M/S correctivo-estético.
  * Filtros en sidechain.
  * Tilt en detector.

* **Herramientas y modelos mencionados**

  * FabFilter Pro-Q 3 / 4.
  * Waves Q1 / Q10 / Renaissance EQ.
  * Bertom Curve Analyzer.
  * Soothe.
  * iZotope Ozone.
  * API 560 / 550A / 550B.
  * Neve 1073 / 1084 / 1081.
  * Lindell Serie 80.
  * Harrison 32C.
  * Pultec EQP-1A / MQ-5.
  * Kiive Warming.
  * C4.
  * iZotope RX.
  * API 2500.

* **Zonas que requieren formulación prudente posterior**

  * Frecuencias concretas de HPF mostradas en ejemplos de sesión.
  * Diferencia útil de 20–30 dB entre basura y fundamental.
  * Relación aproximada de valle Pultec hacia una zona diez veces superior.
  * Recomendaciones de uso de fase lineal según material.
  * Uso de pendientes extremas solo en diagnóstico o casos muy justificados.

## 11. Trazabilidad principal por clases

* **Clase 1**

  * Demostración adelantada de overshot con ruido blanco.
  * Pregunta del estudiante sobre si aumenta volumen o no.
  * Advertencia inicial sobre no confiar ciegamente en números/serigrafía.

* **Clase 9**

  * Uso de pasabanda abrupto para diagnóstico de fase en correlación.

* **Clase 11**

  * Núcleo técnico de filtros:

    * Butterworth,
    * frecuencia de corte,
    * pendiente y polos,
    * Q vs pendiente,
    * overshot,
    * rotación de fase,
    * pendientes extremas,
    * mezcla Tetris,
    * destrucción de alineación de fase,
    * shelving también rota fase,
    * fase lineal, latencia y pre-ringing.

* **Clase 12**

  * Núcleo práctico de filtros en mezcla:

    * tres razones para usar filtros,
    * criterio para no filtrar por costumbre,
    * ejemplos de bombo, tambor, bajo y guitarras,
    * diagnóstico de la “V corta”,
    * filtro invertido en contexto,
    * crítica a limpiar todo desde el master,
    * corrección contra la mezcla Tetris.

* **Clase 13**

  * Núcleo de ecualización:

    * campana, ancho de banda y frecuencia central,
    * frecuencia de corte en shelving,
    * correctiva vs tonal,
    * shelving como segunda etapa,
    * tilt,
    * simétrico vs asimétrico,
    * Q constante vs proporcional,
    * tipos de EQ analógico,
    * Harrison 32C,
    * API vs Neve,
    * barrido aditivo,
    * advertencia sobre serigrafía,
    * exceso de notch como síntoma de mala fuente.

* **Clase 14**

  * Núcleo de ecualizadores de programa y flujo analógico:

    * validez de EQ digitales modernos,
    * SSL Split,
    * Pultec EQP-1A,
    * curva Pultec,
    * riesgo severo en agudos con modo Sharp,
    * Pultec MQ-5,
    * advertencias sobre gráfica y lectura visual.

* **Clase 15**

  * Diferencia entre multibanda y dynamic EQ.
  * Filtrado antepuesto al detector en sidechain.

* **Clase 18**

  * Tilt aplicado al detector del API 2500.

* **Clase 19**

  * Regla de ecualización estática vs dinámica según permanencia del problema.

* **Clase 21**

  * Refuerzo del orden de inserción:

    * corrección primero,
    * tono/color después.

* **Clase 23**

  * Pseudo-ecualizador multibanda para espacialidad mediante filtros y ruteo.

* **Clase 24**

  * Construcción del crossover perfecto.
  * HPF/LPF estándar vs Linkwitz-Riley.
  * Necesidad de -6 dB y fase lineal para reconstrucción correcta.

* **Clase 26**

  * Advertencia contra filtrar por defecto en mastering.
  * Overshot y headroom en etapa comercial.
  * Diferencia DC Offset vs asimetría.
  * All-Pass como rotor de fase.
  * Evaluación crítica del botón Learn en crossovers.

* **Clase 27**

  * Refuerzo del uso de Tilt como corrección eficiente del balance.

* **Clase 28**

  * Ejercicio práctico avanzado en matriz Mid/Side:

    * C4 dinámico correctivo en Mid,
    * Pultec estético en Side,
    * separación entre corrección y embellecimiento dentro de un mismo montaje.
