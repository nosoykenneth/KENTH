---
axis_id: "Eje 4"
axis_number: 4
axis_title: "Eje 4 - Energía y movimiento"
doc_layer: "limpio"
doc_type: "operacion_practica"
source_origin: "course"
status: "ready_for_indexing"
language: "es"
allowed_for_indexing: true
---

# EJE 4 — ENERGÍA Y MOVIMIENTO
## Extracción Forense KENTH Academy

---

## 1. COBERTURA DEL EJE

**Fuentes que lo alimentan directamente:**

| Fuente | Contenido relevante para Eje 4 |
|---|---|
| Clases 15–20 (Mezcla) | Parámetros del compresor, curvas de transferencia, feed-forward/feedback, detector peak/RMS, stereo link, circuitos, técnicas en serie/paralelo, sidechain, expansores, compuertas, ducking |
| PDF: Apunte Procesadores Dinámicos 2022 | Parámetros completos, tipos de circuito, limitadores, expansores, sidechain, ducking |
| PDF: Tipos de Compresores | Óptico, VCA, FET, Vari-mu/Delta Mu, Puente de Diodos — carácter y aplicaciones típicas |
| PDF/Diapositivas: Criterio del Triángulo | Marco metodológico de abordaje de compresión — **ATRIBUCIÓN OBLIGATORIA** |
| Seminario Compresión.txt | Co-presentación Rabinovich + Panitta (AES/CAPER 2023): criterio del triángulo, curvas de transferencia, tiempos de ataque |
| Clase 18 (Mezcla) | SSL bus compressor aplicado a objetivos distintos (picos, RMS, glue); aliasing en compresores |
| Clase 19 (Mezcla) | Fairchild/Vari-mu, ópticos (LA-2A variantes); criterio de clasificación de circuitos; compresión paralela |
| Clase 20 (Mezcla) | Expansores, compuertas, ducking, bleed, detección filtrada |
| Temario fuente (Módulo XIV) | Lista canónica: todos los subcontenidos del eje |

**Partes dislocadas:**

El **Criterio del Triángulo** aparece en el material fuente como eje central del abordaje de compresión (presentado en CAPER/AES 2023 y repetido en múltiples clases). En KENTH, si se usa ese framework, es contenido obligatoriamente atribuible; si no se usa, debe desarrollarse un marco propio equivalente.

Los **limitadores y clippers en mastering** pertenecen a Eje 7. El Eje 4 incluye solo limitadores y clippers en el contexto de mezcla por canal o grupo.

La **compresión de bus** y el **rango dinámico global de la mezcla** pertenecen a Eje 6.

El **EQ dinámico** fue deliberadamente migrado a Eje 3 por la arquitectura de KENTH.

---

## 2. MATRIZ NEUTRA DEL EJE

### BLOQUE A — PARÁMETROS Y COMPORTAMIENTO DEL COMPRESOR

| # | Tema | Subtema | Concepto técnico | Definición neutra | Fórmula / Relación | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|---|
| 4A-01 | Compresor | Downward / Upward | Modos de compresión | Compresión descendente (downward): reduce la ganancia de lo que supera el umbral. Compresión ascendente (upward): aumenta la ganancia de lo que queda por debajo del umbral, reduciendo el rango dinámico desde abajo | — | La compresión descendente es la más común. La ascendente puede combinarse con la descendente para lograr una dinámica más controlada y naturalmente nivelada; aumento del ruido de fondo es el efecto adverso principal | La compresión ascendente en paralelo puede dar más sustento a los pasajes bajos sin alterar la agresividad de los picos | Usar la compresión ascendente sin considerar que eleva también el piso de ruido | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4A-02 | Compresor | Curva de transferencia | Threshold (umbral) | Nivel a partir del cual el compresor comienza a actuar. En compresión descendente: todo lo que supere el umbral recibe reducción de ganancia. El valor de threshold en un plugin no equivale directamente a dBFS; depende del diseño interno | — | No definir el umbral solo por cálculo; confirmar por percepción que el compresor está reaccionando al contenido deseado y no a otra cosa (bajos frecuencias, bleed, etc.) | El umbral numérico en dos compresores distintos puede producir resultados muy diferentes; el medidor de reducción de ganancia es la referencia correcta | Fijar el umbral basándose solo en el valor numérico del panel sin verificar qué está disparando el compresor | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4A-03 | Compresor | Curva de transferencia | Ratio (relación de compresión) | Relación entre el cambio en el nivel de entrada y el cambio en el nivel de salida cuando la señal supera el umbral. Ratio 2:1: por cada 2 dB sobre el umbral, solo sube 1 dB en la salida. Ratio ∞:1: ningún incremento de señal pasa del umbral → limitación | — | Orientación aproximada: ≤2:1 compresión suave; 4:1 compresión media; ≥8:1 compresión dura; ≥20:1 limitación | En algunos compresores (SSL), cambiar el ratio también cambia el knee, lo que modifica el carácter completo de la respuesta más allá de la "cantidad" de compresión | Subir el ratio para "comprimir más" sin considerar que algunos compresores cambian el tipo de knee al cambiar el ratio | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4A-04 | Compresor | Curva de transferencia | Knee (rodilla) | La transición entre zona sin compresión y zona con compresión. Hard knee: transición abrupta exactamente en el umbral. Soft knee: transición gradual que comienza antes del umbral y alcanza el ratio completo gradualmente | — | Hard knee: control de picos percusivos, limitación. Soft knee: voces, vientos, cuerdas, buses; compresión menos obvia y más natural. El tamaño del knee puede ser variable en algunos procesadores digitales | Un soft knee amplio puede estar comprimiendo antes del umbral nominal marcado; si el compresor "parece reaccionar antes de lo esperado", verificar el tipo de knee | Aplicar hard knee en todos los casos porque es "más directo" y perder musicalidad en material no percusivo | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4A-05 | Compresor | Curva de transferencia | Curvas vintage | Algunos compresores analógicos tienen curvas de transferencia no estándar: comprimen con soft en un rango y luego retoman una relación más definida en niveles mayores. Esta no-linealidad es parte de su carácter musical | — | Las curvas vintage no se ajustan a las categorías hard/soft estándar; su comportamiento real debe evaluarse con el material | Las curvas vintage producen sonidos que los compresores de curva estándar no pueden replicar exactamente aunque se usen los mismos valores | Clasificar un compresor vintage como soft o hard knee simplemente por cómo se siente, sin entender que su curva de transferencia puede ser híbrida | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4A-06 | Compresor | Envolventes | Tiempo de ataque | El tiempo de ataque es el tiempo que tarda el compresor en alcanzar la reducción de ganancia objetivo desde que la señal supera el umbral. La reducción comienza desde el primer ciclo; el ataque es cuánto tarda en llegar, no cuánto espera para empezar | Criterio 63%: tiempo para alcanzar el 63% de la reducción (analógico clásico). Criterio 10/90%: tiempo entre 10% y 90% de la reducción (digital frecuente). Algunos VCA miden ms para reducir X dB específicos | Ataque rápido en percusivos para controlar picos; pero si es demasiado rápido se sacrifica la transiente y se pierde impacto. Ataque lento deja pasar la transiente y permite impacto natural | El tiempo de ataque entre distintos compresores no es comparable directamente si usan criterios diferentes (63% vs 10/90%). "10 ms" en un compresor no equivale a "10 ms" en otro de otra topología | Asumir que el tiempo de ataque es cuánto espera el compresor antes de actuar | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4A-07 | Compresor | Envolventes | Tiempo de release | El tiempo de release es el tiempo que tarda el compresor en liberar la reducción de ganancia una vez que la señal vuelve por debajo del umbral. Un release demasiado rápido puede generar bombeo (pumping). Un release demasiado lento puede mantener la señal comprimida más de lo necesario | — | Release rápido: señales con transitorios rápidos y separados. Release lento: señales sostenidas o para compresión continua de RMS. Auto-release: muchos compresores adaptan el release al contenido del programa | La relación entre el release y el tempo del material es crucial: un release que coincide con el pulso musical puede hacer que la compresión "respire" al ritmo de la canción | Fijar el release al mínimo posible en todos los casos esperando "más control" | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4A-08 | Compresor | Envolventes | Hold y Look-ahead | Hold: tiempo mínimo durante el cual la compresión se mantiene activa después del ataque, evitando saltos bruscos en la reducción de ganancia. Look-ahead: el detector lee la señal con anticipación, permitiendo que el compresor reaccione antes de que llegue el pico a la salida; reduce distorsión en señales de transiente rápido | — | Hold es especialmente útil en compuertas para evitar que se cierren entre sílabas. Look-ahead aumenta la latencia del procesador; compensar siempre con la opción de retardo automático del DAW | Look-ahead no es lo mismo que soft knee: look-ahead habla de anticipación temporal; knee habla de la forma de entrada de la compresión alrededor del umbral | Confundir look-ahead con knee, o usar look-ahead sin compensar la latencia añadida en el DAW | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4A-09 | Compresor | Envolventes | Parámetros encadenados | En un compresor, los parámetros interactúan: cambiar uno modifica cómo se comportan los demás. A diferencia del EQ (donde una banda afecta una zona puntual sin cambiar el resto), en el compresor cada parámetro define el contexto en el que opera el siguiente | — | No ajustar los parámetros de forma secuencial e independiente; verificar el resultado completo después de cada cambio | Un release que funciona bien con ratio 4:1 puede producir bombeo o exceso de compresión con ratio 10:1 aunque el release no haya cambiado | Tratar los parámetros del compresor como knobs independientes sin verificar la interacción entre ellos | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4A-10 | Compresor | Parámetros avanzados | Makeup gain | Ganancia de salida que compensa la reducción de nivel producida por la compresión. Algunos compresores tienen auto makeup que intenta compensar automáticamente. El makeup siempre debe partirse desde 0 al cargar el plugin para evaluar el efecto real de la compresión sin ilusión de mejora por nivel | — | Cargar cualquier compresor con makeup en 0; evaluar la compresión; luego compensar el nivel. Comparar siempre en igualdad de nivel antes de aprobar el procesamiento | Si el compresor viene con makeup activo por defecto, lo que "suena mejor" puede ser simplemente que suena más fuerte. En ese caso la compresión puede no estar mejorando nada | Cargar el compresor con el preset de fábrica (que puede incluir makeup activo) y aprobar el resultado sin comparar en igualdad de nivel | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4A-11 | Compresor | Circuito detector | Feed-forward vs feedback | Feed-forward: el detector lee la señal de entrada (antes de la reducción de ganancia). Suele ser más predecible y agresivo. Feedback: el detector lee la señal de salida (después de la reducción). Produce un sistema de retroalimentación que tiende a ser más musical y estable, pero menos preciso | — | No hay correlación fija entre arquitectura feed-forward/feedback y el tipo de circuito de reducción (VCA, FET, etc.); los fabricantes combinan según diseño | Un compresor feedback puede sonar más suave no porque comprima menos, sino porque la retroalimentación suaviza la respuesta | Asumir que feed-forward es siempre más rápido o que feedback es siempre más lento | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4A-12 | Compresor | Circuito detector | Detector Peak vs RMS | El detector puede responder a picos instantáneos (peak) o al promedio energético de la señal (RMS). Peak: seguimiento rápido de variaciones instantáneas; puede producir más disparos y más distorsión. RMS: respuesta más estable; más cercana a la percepción de nivel sostenido | — | Detector peak para control de picos y señales percusivas. Detector RMS para señales sostenidas y buses; compresión más musical y menos obvia | Un detector RMS puede parecer "más suave" aunque esté comprimiendo tanto como uno peak porque reacciona al promedio, no a los transitorios | Seleccionar el detector sin considerar el tipo de señal que se va a comprimir | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4A-13 | Compresor | Estéreo | Stereo link vs Dual mono | Stereo link: los sidechains de L y R se unen; un evento fuerte en un canal puede hacer reaccionar a ambos. Mantiene la imagen estéreo estable. Dual mono: cada canal reacciona independientemente; la imagen puede desbalancearse si solo un lado supera el umbral | — | Usar stereo link para material estéreo cuando se quiere preservar la imagen. Dual mono para procesamiento selectivo o creativo donde se quiere que cada canal responda de forma independiente | Algunos compresores permiten link porcentual, no solo estéreo o dual mono absolutos, lo que da mayor flexibilidad | Usar dual mono en material estéreo sin considerar que puede comprimir más un canal que otro y rotar la imagen | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4A-14 | Compresor | Distorsión y aliasing | THD, IMD y aliasing en procesadores dinámicos | Los compresores, especialmente los analógicos y sus modelados, introducen distorsión armónica (THD), distorsión por intermodulación (IMD) y —en procesadores digitales— aliasing cuando no hay oversampling. Cada tipo de distorsión tiene un carácter diferente: el aliasing es inarmónico y no se puede filtrar a posteriori | — | Activar oversampling en compresores que lo ofrecen, especialmente en compresores de modelado analógico con circuitos no lineales. Verificar cuánta distorsión introduce el compresor antes de aprobar su uso en una cadena | El aliasing en un compresor es distinto al del EQ: el compresor procesa de forma dinámica y el aliasing puede variar en función del nivel y la reducción de ganancia | Asumir que todos los compresores de una misma marca tienen el mismo nivel de aliasing | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE B — CIRCUITOS ANALÓGICOS Y SU CARÁCTER

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio de clasificación | Carácter general | Aplicaciones típicas | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|
| 4B-01 | Circuitos | Criterio de clasificación | Qué define el tipo de compresor | Un compresor se clasifica según el elemento que realiza la reducción de ganancia, no según los componentes presentes en el circuito general. Tener válvulas no equivale a ser valvular: si la reducción la hace un elemento óptico, el compresor es óptico aunque tenga válvulas en la etapa de amplificación | El elemento que realiza la reducción de ganancia define el tipo | — | — | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4B-02 | Circuitos | Óptico | Compresores ópticos (opto) | La reducción de ganancia la realiza un elemento óptico: una fuente de luz (LED o lámpara) cuya intensidad varía con el nivel de señal, y un receptor fotosensible (fotorresistencia) que controla la ganancia. Las envolventes dependen del comportamiento físico del sistema óptico (velocidades de encendido/apagado del elemento de luz) | Elemento de reducción: fotorresistencia / célula óptica (T4 en LA-2A) | Respuesta lenta, dependiente del programa. Muy musical. Adecuado para voces, vientos, cuerdas; no para control de transitorios percusivos rápidos | Voces, vientos, cuerdas frotadas, buses cuando se busca suavidad. No recomendado para control preciso de batería | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4B-03 | Circuitos | VCA | Compresores VCA (Voltage Controlled Amplifier) | La reducción de ganancia la realiza un amplificador controlado por voltaje. Las envolventes son determinadas por el circuito electrónico, no por la física de un componente pasivo como en los ópticos. Alta versatilidad de envolventes. Distintos chips VCA producen caracteres muy diferentes entre sí | Elemento de reducción: chip VCA | Muy versátiles. El carácter varía significativamente según el diseño (un VCA de API es muy diferente al de SSL aunque ambos sean VCA). Aptos para control de transitorios y para buses | Control de batería, canales individuales, buses. El SSL bus compressor y el API 2500 son VCA con caracteres opuestos | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4B-04 | Circuitos | FET | Compresores FET (Field Effect Transistor) | La reducción de ganancia la realiza un transistor de efecto de campo. Envolventes extremadamente rápidas. La disposición feedback del detector produce compresión dependiente del programa, suavizando el comportamiento a pesar de la velocidad | Elemento de reducción: FET | Ataque muy rápido; comportamiento musical por el feedback. Agrega color y carácter marcados. Versátil: puede operar desde sutil hasta extremadamente agresivo ("all buttons") | Batería (room, close mics), bajo, voces con carácter, compresión paralela. No recomendado para bus de mezcla en general | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4B-05 | Circuitos | Vari-mu / Delta Mu | Compresores valvulares (Vari-mu) | La reducción de ganancia la realizan directamente las válvulas, que modifican su amplificación según el nivel de señal. Respuesta más lenta que otros tipos. Carácter muy cálido. La disposición feedback los convierte en compresores dependientes del programa | Elemento de reducción: válvulas en el circuito de ganancia | Sonido cálido, suave, musical. Excelente para buses, mezclas completas, voces, bajo. El pegamento (glue) de un valvular es difícil de igualar con otros tipos. Incluso sin comprimir puede aportar coloración por saturación armónica valvular | Buses de mezcla, masterización, voces y bajo cuando se busca calidez y pegamento | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4B-06 | Circuitos | Puente de diodos | Compresores de puente de diodos | La reducción de ganancia la realiza un puente de diodos. El sidechain usa una versión rectificada (CC) de la señal de audio. Envolventes muy rápidas con alta no-linealidad, lo que produce un carácter muy musical y distinto | Elemento de reducción: puente de diodos | Envolventes rápidas. Alta no-linealidad → carácter musical muy propio. Modelo representativo: Neve 5254 | Cuando se busca carácter músical específico distinto al de los otros tipos; batería, buses | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE C — OBJETIVOS Y TÉCNICAS DE COMPRESIÓN

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|
| 4C-01 | Objetivos | Técnicos | Objetivos técnicos de la compresión | Cuatro objetivos técnicos diferenciados: (1) limitación de picos: contener transitorios que superen umbrales críticos, (2) nivelación de picos: controlar inconsistencias de dinámica en una interpretación, (3) incremento del nivel RMS: aumentar la densidad percibida de la señal, (4) nivelación de señal completa: uniformizar todo el rango dinámico | — | El objetivo debe definirse antes de elegir los parámetros. No hay una configuración universal; el mismo objetivo puede requerir parámetros muy diferentes según el tipo de señal | Confundir limitación de picos (ataque rápido, ratio alto, umbral alto) con nivelación de señal completa (ataque lento, ratio bajo, umbral bajo) conduce a resultados que deshacen el trabajo de mezcla | Aplicar la misma configuración de compresor a todos los objetivos esperando resultados similares | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4C-02 | Objetivos | Artísticos | Objetivos artísticos de la compresión | Objetivos donde la compresión contribuye al carácter sonoro: (1) impacto: reforzar el punch de transitorios percusivos, (2) color: la distorsión y el comportamiento del circuito modifican el timbre de la señal, (3) distorsión controlada: el saturation armónico del compresor como efecto intencional, (4) pegamento (glue): integrar elementos dispares en un conjunto cohesionado | — | Los objetivos artísticos a menudo requieren modelado analógico para aprovechar el carácter del circuito | Un compresor puede agregar impacto a una percusión dejando pasar la transiente (ataque lento) y luego construyendo el cuerpo del sonido en la liberación | Comprimir con objetivos artísticos usando compresores transparentes (como algunos digitales) que no aportan color ni distorsión útil | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4C-03 | Técnicas | Paralela | Compresión en paralelo | Mezclar la señal original sin comprimir con una copia comprimida de forma agresiva. El resultado preserva los transitorios y la dinámica del original mientras añade el cuerpo y la densidad de la compresión | Control de mezcla (wet/dry o mix en el plugin): ajustar la proporción entre señal original y señal comprimida | La señal comprimida en paralelo puede ser muy agresiva porque la mezcla con el original suavizará el resultado; esto permite comprimir más sin destruir los transitorios | La compresión paralela analógica puede introducir una leve rotación de fase entre la señal original y la comprimida; normalmente no es relevante en práctica real | Mezclar en paralelo con una compresión moderada que apenas se escucha sola; el resultado será inaudible mezclado con el original | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4C-04 | Técnicas | Serie | Compresión en serie | Aplicar dos o más compresores en cadena, cada uno con una tarea específica. El primero puede controlar los picos más extremos; el segundo trabaja sobre el promedio con mayor musicalidad porque ya no necesita gestionar los picos extremos | — | Primero el compresor más rápido o más agresivo (VCA, FET) para los picos; segundo el más musical (óptico, valvular) para el carácter y el cuerpo | Un compresor que trabaja sobre un material ya controlado puede operar de forma mucho más musical y sutil que si tuviera que gestionar él solo todo el rango dinámico | Poner dos compresores en serie sin definir la tarea de cada uno; el resultado suele ser sobrecompresión no intencional | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4C-05 | Técnicas | Sidechain | Filtrado interno en el sidechain | Algunos compresores permiten colocar un filtro HPF antes del detector para que las frecuencias bajas no sean la causa principal de los disparos de compresión. Si el bombo domina el detector, el compresor reacciona como si todo el material subiera de nivel cuando solo hay un golpe de bombo | — | Activar el HPF del sidechain en compresores de buses o grupos de batería cuando las bajas frecuencias disparan el compresor de forma excesiva | Un HPF en el sidechain de un bus compressor que procesa material completo puede hacer que la compresión sea más musical y transparente porque el compresor ya no "ve" tanto el bombo como la causa del disparo | No verificar qué está disparando el compresor antes de ajustar el threshold; el sidechain sin HPF en material complejo puede estar respondiendo principalmente al bombo | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4C-06 | Técnicas | Sidechain externo | Sidechain externo (external sidechain / key input) | Conectar una señal externa al detector del compresor para que esa señal sea la que dispara la reducción de ganancia, en lugar de la señal que se está comprimiendo. El compresor actúa sobre la señal de audio del canal, pero reacciona a la señal externa | — | Ducking: la señal de voz va al sidechain del compresor de la música; cuando la voz sube, la música baja. Compuerta disparada externamente: el bombo dispara la compuerta de otro elemento | El sidechain externo permite que un elemento "domine" dinámicamente a otro sin que haya interacción directa entre sus señales de audio | Conectar la señal de disparo al sidechain y olvidarse de verificar el nivel con el que llega; si llega demasiado bajo, el detector no reacciona | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4C-07 | Técnicas | Timbre y envolvente | Compresión y reconocimiento auditivo | Todo sonido se reconoce por su timbre y su envolvente. Un compresor que modifica la envolvente de forma excesiva también modifica el timbre percibido. La sobrecompresión puede hacer un sonido irreconocible o perder su definición aunque "suene denso" | — | Verificar que la compresión no ha cambiado el timbre del instrumento de forma no deseada, comparando con el original en igualdad de nivel | Cuando un compresor hace que un bombo "suene más grande" pero pierda su golpe, no es necesariamente mejor resultado: el impacto depende de la envolvente, no del nivel | Aprobar la compresión solo por nivel percibido sin verificar que la envolvente del instrumento sigue siendo reconocible | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE D — EL CRITERIO DEL TRIÁNGULO *(ATRIBUIBLE)*

| # | Concepto | Descripción neutra | Acción |
|---|---|---|---|
| 4D-01 | Marco de abordaje sistemático | Sistema que relaciona el nivel de trabajo de una señal con el objetivo de compresión y los parámetros más adecuados para alcanzarlo. Aplicable a canales individuales, grupos y buses, no solo a la mezcla completa | USAR CON ATRIBUCIÓN |
| 4D-02 | Zona alta del triángulo (percusiones) | Señales de nivel alto, corta duración, transitorios fuertes. Parámetros orientativos: ratio alto, hard knee, umbral alto, envolventes rápidas | USAR CON ATRIBUCIÓN |
| 4D-03 | Zona media del triángulo (melodías) | Señales de nivel medio, duración intermedia. Parámetros orientativos: ratio medio, knee medio, umbral medio, envolventes moderadas | USAR CON ATRIBUCIÓN |
| 4D-04 | Zona baja del triángulo (sustento) | Señales de nivel bajo, mayor duración, más sostenidas. Parámetros orientativos: ratio bajo, soft knee, umbral bajo, envolventes lentas | USAR CON ATRIBUCIÓN |
| 4D-05 | Advertencia de uso | El triángulo es un punto de partida, no una receta cerrada. Una misma señal (p.ej., un bombo) puede requerir simultáneamente tratamiento en distintas zonas según el objetivo. El método orienta el primer ajuste; el oído ajusta desde ahí | USAR CON ATRIBUCIÓN |

---

### BLOQUE E — EXPANSORES, COMPUERTAS Y HERRAMIENTAS DE UMBRAL INFERIOR

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|
| 4E-01 | Expansores | Descendente | Expansor descendente | Lo contrario de la compresión: actúa por debajo del umbral, reduciendo más el nivel de lo que ya está bajo. A mayor expansión, más se reduce lo que no alcanza el umbral | Equivalencia: expansión suave ~2:1 → expansión media ~1:4 → expansión dura ~1:8 → compuerta ~1:20 | El ratio en un expansor conviene interpretarse al revés: por cada 1 dB que la señal quede bajo el umbral, baja [ratio] dB en la salida | Un expansor descendente puede usarse como alternativa más musical a una compuerta; reduce gradualmente en lugar de cortar abruptamente | Aplicar ratio de expansión muy alto esperando el efecto de una compuerta sin que se escuche el cierre abrupto | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4E-02 | Expansores | Ascendente | Expansor ascendente | Actúa por encima del umbral, aumentando la ganancia de lo que supera el umbral en lugar de reducirla. Extiende el rango dinámico hacia arriba. Puede combinarse con compresión descendente para lograr una dinámica más controlada sin perder musicalidad | — | Usar para recuperar dinámica en material sobrecomprimido o para enfatizar los transitorios que el compresor descendente ha reducido | El expansor ascendente en paralelo con el compresor descendente puede crear una dinámica que se siente muy natural aunque el procesamiento sea complejo | Confundir expansor ascendente con upward compression | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4E-03 | Compuerta | Definición y parámetros | Compuerta (gate) | Un expansor llevado a su expresión máxima (ratio ~1:100 o infinito). Cierra completamente la salida cuando la señal cae por debajo del umbral. Parámetros: threshold, attack, release, hold, range, y a veces filtro antepuesto al detector | — | Usar hold para evitar que la compuerta se cierre entre sílabas o durante el cuerpo de un sonido percusivo. El filtro antepuesto al detector permite que solo una frecuencia específica dispare la apertura | En batería con mucho bleed, una compuerta filtrada al detector puede abrirse solo cuando detecta la fundamental del instrumento objetivo, ignorando el bleed de otros elementos | Configurar el umbral demasiado alto y que la compuerta "se coma" parte del cuerpo del sonido porque se cierra antes de que el instrumento haya terminado | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4E-04 | Compuerta | Bleed | Compuertas y bleed en batería | En batería acústica, el bleed de otros elementos puede disparar una compuerta o impedir que se cierre correctamente. Si un platillo suena exactamente al mismo tiempo que el tambor, ninguna compuerta puede separarlos por nivel | — | Usar el filtro del detector centrado en la fundamental del instrumento objetivo para discriminar el disparo. Aceptar que si dos sonidos ocurren simultáneamente a niveles similares, la compuerta no puede distinguirlos | La fundamental del tambor detectada con el analizador (~178 Hz en un caso típico) puede usarse como frecuencia central del filtro del detector | Esperar que la compuerta resuelva bleed de elementos que ocurren exactamente al mismo tiempo que el instrumento objetivo | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4E-05 | Ducking | Sidechain externo | Ducking | Reducción dinámica del nivel de un elemento (p.ej., música) disparada por la presencia de otro (p.ej., voz). Se logra conectando la señal de disparo al sidechain externo del compresor del elemento que debe "ceder" | — | En mezcla para video o podcast: la música reduce nivel cuando la voz está presente. En mezcla musical: puede usarse para que el bombo cree espacio en el bajo mediante sidechain | Para ducking con voz, usar un auxiliar paralelo de la voz (sin reverb) como señal de disparo para evitar que la reverb de la voz también dispare el ducking | Conectar la señal de voz con sus efectos al sidechain, haciendo que la reverb de la voz también dispare la reducción de la música | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE F — LIMITADORES Y CLIPPERS (EN MEZCLA)

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|
| 4F-01 | Limitador | Definición | Limitador en mezcla | Un compresor con ratio muy alto (≥20:1 o ∞:1) y envolventes rápidas. La señal no puede superar el umbral en la salida. En mezcla: protege canales o grupos de picos extremos y puede usarse como herramienta de densidad | Threshold, release, output ceiling | En mezcla por canal: usar limitadores para contener transitorios que un compresor normal no alcanza a controlar sin sobrecomprimir todo el material. En buses: con precaución; puede destruir transitorios si el ataque es demasiado rápido | Un limitador de canal puede abrir espacio en la mezcla al contener solo los picos más extremos sin tocar el RMS del instrumento | Usar el limitador en todos los canales como práctica estándar en lugar de gestionar el gain staging correctamente | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 4F-02 | Clipper | Definición y diferencia | Clipper vs limitador | El limitador reduce la ganancia de la señal para que no supere el umbral (compresión extrema). El clipper recorta la forma de onda directamente cuando supera el umbral, produciendo saturación armónica. La diferencia fundamental: el limitador actúa sobre la ganancia; el clipper actúa sobre la forma de onda | — | El clipper produce distorsión armónica incluso a baja cantidad de recorte; esto puede aumentar la densidad percibida de la señal. El limitador puede sonar más transparente pero puede introducir bombeo si el ataque es rápido. Ambos tienen aplicaciones específicas | Un pequeño uso del clipper en elementos percusivos puede aumentar el punch percibido sin la pérdida de transitorios del limitador rápido | Usar limitador y clipper indistintamente creyendo que tienen el mismo efecto en el material | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

## 3. CONTENIDO ATRIBUIBLE DEL EJE

| Bloque | Atribución requerida | Obligación específica |
|---|---|---|
| **Criterio del Triángulo** (El Criterio del Triángulo — Enfoque Metodológico de la Compresión) | Autoría: Pablo Rabinovich y Pablo Panitta. Presentado en AES/CAPER 2023 (Argentina). Está documentado en diapositivas y en el seminario de compresión transcrito | **OBLIGACIÓN ARQUITECTURAL**: si KENTH enseña la lógica de este framework (abordaje sistemático por nivel/duración de la señal → orientación de parámetros), debe incluir crédito nominativo: "Basado en el Criterio del Triángulo de Pablo Rabinovich y Pablo Panitta (AES/CAPER 2023)". No es suficiente un agradecimiento genérico. El crédito debe estar en el material del eje donde se use. **Alternativa válida**: desarrollar un framework propio de abordaje de la compresión y no utilizar el de los autores fuente |
| PDF: Apunte Procesadores Dinámicos 2022 | Autoría: Pablo Rabinovich. La doctrina técnica (parámetros, tipos de circuito, comportamiento) es de dominio general del campo | Reformular; no copiar la formulación del apunte |
| PDF: Tipos de Compresores | Autoría: Pablo Rabinovich. Los perfiles de circuito son del dominio técnico general; las formulaciones específicas del apunte son del autor | Reformular; los perfiles de carácter por circuito pueden reutilizarse como doctrina general |
| Modelos específicos (LA-2A, 1176, API 2500, Fairchild, Manley Variable Mu, SSL Bus Compressor) | Hardware de distintos fabricantes (Teletronix/Universal Audio, API Technologies, Fairchild/Universal Audio, Manley, SSL). La doctrina del campo sobre su carácter es ampliamente documentada independientemente del autor fuente | No requiere atribución al docente fuente; sí nombrar los fabricantes originales al introducir los modelos |

---

## 4. BLOQUEOS DEL EJE

| Bloque bloqueado | Tipo de riesgo | Por qué no debe pasar |
|---|---|---|
| Descripción del Vari-mu como "cremoso" | EXPRESIÓN NO REUTILIZABLE | Formulación oral muy marcada y reconocible del docente fuente |
| Comparación API 2500 vs SSL bus compressor como "agresivo vs musical" en esos términos exactos | EXPRESIÓN NO REUTILIZABLE | Formulación específica del docente; evaluación comparativa subjetiva con su framing propio |
| Anécdota sobre aprender a manejar el Fairchild: "las primeras veces no pegaba pie con bola" | EXPRESIÓN NO REUTILIZABLE | Historia personal del docente fuente; tono oral marcado |
| Comparación del aprendizaje de la compresión con "aprender a andar en bicicleta" | EXPRESIÓN NO REUTILIZABLE | Analogía oral del docente; formulación identificable |
| Referencia al blog del instituto y el artículo sobre SSL | EXPRESIÓN NO REUTILIZABLE | Referencia autobiográfica del docente fuente |
| Criterio del Triángulo usado sin atribución | MÉTODO ATRIBUIBLE BLOQUEADO SIN ATRIBUCIÓN | Obligación arquitectural explícita; usarlo sin crédito viola las condiciones de la autorización |
| Secuencia pedagógica del temario fuente: parámetros → curvas → circuitos → triángulo → modelados → expansores/compuertas | ESTRUCTURA NO REUTILIZABLE | Orden de exposición del curso fuente reconocible |
| Formulaciones orales: "se come la transiente", "babosa o ameba", "choclo muy constante" | EXPRESIÓN NO REUTILIZABLE | Tono oral muy marcado del docente fuente |
| Descripción del Fairchild como "20 válvulas" y la anécdota de su mantenimiento | EXPRESIÓN NO REUTILIZABLE | Dato situado en el contexto personal del docente |

---

## 5. VACÍOS Y TENSIONES DEL EJE

| Tipo | Descripción | Implicación para redacción |
|---|---|---|
| **Vacío** | Los **clippers en mezcla** están mencionados en la arquitectura de KENTH y en el temario fuente (Training), pero tienen cobertura muy escasa en las transcripciones de las clases de Mezcla (aparecen principalmente en las clases de Training y Mastering). La distinción limitador/clipper se menciona pero no tiene un desarrollo propio extendido | Al redactar: la doctrina técnica está disponible; construir los criterios de uso en mezcla desde doctrina general o fuentes externas |
| **Vacío** | Las **técnicas artísticas específicas de compresión por instrumento** (cómo comprimir un bombo, un tambor, una voz, una guitarra eléctrica con parámetros detallados) tienen cobertura parcial en clases de Training pero escasa en las clases teóricas de Mezcla | Al redactar: el marco teórico está disponible; los casos de aplicación por instrumento deberán construirse editorialmente o extenderse con clases de Training |
| **Vacío relativo** | El **Puente de diodos** y sus modelos representativos tienen cobertura muy breve en las fuentes (una mención en el PDF de tipos de compresores). Hay poca doctrina práctica sobre cuándo y cómo usarlo en mezcla | Reducir a doctrina mínima o construir desde fuentes externas |
| **Tensión crítica de atribución** | El Criterio del Triángulo es el marco central de toda la enseñanza de compresión del curso fuente. Si KENTH lo usa, la atribución es obligatoria. Si no lo usa, necesita desarrollar un framework alternativo propio para el abordaje sistemático de la compresión. No existe en las fuentes una doctrina de abordaje de compresión desvinculada del Triángulo | **Decisión editorial obligatoria**: antes de redactar el Eje 4, definir si KENTH usará el Criterio del Triángulo con atribución o desarrollará su propio marco |
| **Tensión de límite** | La **compresión de bus** en mezcla y el **rango dinámico global** pertenecen a Eje 6, pero en las fuentes (Clase 18) el SSL bus compressor se enseña en el bloque de técnicas de compresión dentro de las clases de mezcla principal. El contenido es el mismo; la diferencia es el escenario de uso (canal individual vs bus de mezcla) | Al redactar Eje 4: introducir bus compressor como concepto de aplicación de lo aprendido, con nota explícita de que el uso en bus de salida y el rango dinámico global se desarrollan en Eje 6 |
| **Tensión de cruce con Eje 3** | El **EQ dinámico** fue deliberadamente ubicado en Eje 3 (herramienta espectral) aunque tenga comportamiento temporal. Esto puede confundir al alumno que espera verlo en Eje 4 junto al compresor. El cruce debe declararse explícitamente | Al redactar Eje 4: incluir una nota de orientación al inicio del eje declarando que el EQ dinámico y el de-esser pertenecen a Eje 3 y no se repiten aquí |
| **Tensión de cruce con Eje 2** | El **sidechain con filtros** (HPF en el sidechain, EQ en el sidechain) cruza con los filtros de Eje 2. Los filtros como herramienta de control del detector son un uso funcional de los filtros dentro de Eje 4 | Al redactar: declarar el cruce; los filtros en sidechain son una aplicación funcional de los filtros (Eje 2) al servicio del compresor (Eje 4) |

---

## 6. PAQUETE LIMPIO DEL EJE

### EJE 4 — ENERGÍA Y MOVIMIENTO · Paquete limpio para proyecto generativo

---

**FUNCIÓN DEL EJE:** Controlar el comportamiento energético de las señales en el tiempo: impacto, densidad, expresión y movimiento dinámico. Sin control dinámico, la mezcla carece de energía dirigida.

**ADVERTENCIA ANTES DE REDACTAR:** Resolver la tensión crítica de atribución del Criterio del Triángulo antes de iniciar la redacción.

---

#### BLOQUE A — PARÁMETROS DEL COMPRESOR

**Doctrina reutilizable:**
- Compresión downward: reduce la ganancia de lo que supera el umbral. Compresión upward: aumenta la ganancia de lo que queda por debajo del umbral
- Threshold: nivel a partir del cual el compresor actúa. El valor numérico del panel no equivale directamente a dBFS; el medidor de reducción de ganancia es la referencia correcta
- Ratio: relación entre cambio de entrada y de salida sobre el umbral. Escalas orientativas: ≤2:1 suave; 4:1 medio; ≥8:1 duro; ≥20:1 limitación
- El ratio puede cambiar el comportamiento del knee en algunos compresores; verificar siempre el resultado completo al modificar el ratio
- Knee: transición entre zona sin compresión y zona con compresión. Hard knee: transición abrupta. Soft knee: transición gradual que comienza antes del umbral. Algunos compresores tienen curvas vintage que son híbridas entre ambos
- Tiempo de ataque: cuánto tarda en llegar la reducción de ganancia, no cuánto espera. La reducción comienza desde el primer ciclo. Criterio 63%: analógico clásico. Criterio 10/90%: digital frecuente. Comparar tiempos entre distintos compresores solo si usan el mismo criterio
- Tiempo de release: tiempo para liberar la reducción. Release muy rápido → bombeo (pumping). Release muy lento → compresión sostenida indeseada. Auto-release adapta al contenido
- Hold: mínimo tiempo de compresión activa; evita saltos bruscos. Look-ahead: el detector lee con anticipación; reduce distorsión en transitorios rápidos; añade latencia que debe compensarse
- Los parámetros del compresor interactúan: cambiar uno modifica cómo operan los demás
- Makeup gain: siempre partir desde 0 al cargar un compresor. Comparar con bypass en igualdad de nivel antes de aprobar
- Feed-forward: detector lee la señal de entrada; más predecible y agresivo. Feedback: detector lee la señal de salida; más estable y musical
- Detector peak: responde a variaciones instantáneas; más rápido; más distorsión posible. Detector RMS: responde al promedio energético; más musical; no hay correlación fija entre tipo de detector y arquitectura feed-forward/feedback
- Stereo link: ambos canales reaccionan juntos; preserva la imagen estéreo. Dual mono: cada canal reacciona independientemente; puede desbalancear la imagen
- THD, IMD y aliasing en procesadores dinámicos: el aliasing es inarmónico y no filtrable. Activar oversampling cuando esté disponible en compresores con circuitos no lineales

**Atribuciones:** modelos de hardware específicos → fabricantes originales

**Advertencias:**
- LÍMITE Eje 4 / Eje 6: la compresión de bus de salida y el rango dinámico global pertenecen a Eje 6
- LÍMITE Eje 4 / Eje 7: limitadores y clippers en mastering pertenecen a Eje 7
- CRUCE → EJE 3: EQ dinámico y de-esser viven en Eje 3; no se desarrollan en Eje 4

---

#### BLOQUE B — CIRCUITOS

**Doctrina reutilizable (reformular sin reproducir las descripciones del autor fuente):**

Un compresor se clasifica por el elemento que realiza la reducción de ganancia, no por los componentes presentes en el resto del circuito.

| Tipo | Mecanismo de reducción | Carácter general reformulable | Aplicaciones orientativas |
|---|---|---|---|
| Óptico | Elemento óptico (lámpara + fotorresistencia) | Respuesta lenta dependiente del programa; muy musical | Voces, vientos, cuerdas, buses suaves |
| VCA | Amplificador controlado por voltaje | Alta versatilidad; el carácter varía mucho entre modelos del mismo tipo | Control de batería, canales individuales, buses (muy variable por modelo) |
| FET | Transistor de efecto de campo | Ataque muy rápido; feedback produce musicalidad; agrega color marcado | Batería (rooms, close), bajo, voces con carácter, compresión paralela |
| Vari-mu / Delta Mu | Válvulas en el circuito de ganancia | Respuesta lenta; carácter cálido; pegamento excelente en buses | Buses, mezclas completas, voces/bajo cuando se busca calidez |
| Puente de diodos | Puente de diodos; sidechain rectificado | Envolventes rápidas; alta no-linealidad; carácter musical muy propio | Cuando se busca carácter específico distinto a los otros tipos |

**Atribuciones:** modelos específicos → fabricantes históricos (Teletronix/Universal Audio, API, UREI/Universal Audio, Fairchild, Manley, SSL, Neve)

---

#### BLOQUE C — OBJETIVOS Y TÉCNICAS

**Doctrina reutilizable:**

Objetivos técnicos: limitación de picos, nivelación de picos, incremento de RMS, nivelación de señal completa.
Objetivos artísticos: impacto, color, distorsión controlada, pegamento (glue).

El objetivo debe definirse antes de elegir parámetros. No existe configuración universal.

- Compresión en paralelo: mezclar señal original con copia muy comprimida. Preserva transitorios del original; añade cuerpo y densidad. La copia comprimida puede ser agresiva porque la mezcla con el original suavizará el resultado
- Compresión en serie: primer compresor gestiona los picos extremos; segundo compresor trabaja de forma más musical sobre el promedio con material ya controlado
- HPF en sidechain: evita que las bajas frecuencias dominen el detector en compresores de buses o grupos
- Sidechain externo / key input: la señal de disparo determina cuándo actúa el compresor. Permite ducking y compuertas disparadas externamente
- Ducking: la presencia de una señal (voz) reduce la ganancia de otra (música) mediante sidechain externo. Para ducking de voz, usar la señal sin reverb como disparo
- Compresión y timbre: el compresor modifica la envolvente y por tanto el timbre percibido. Sobrecomprimir puede hacer un sonido irreconocible. Verificar siempre comparando con el original en igualdad de nivel

**Advertencias:**
- DECISIÓN EDITORIAL OBLIGATORIA: si se usa el Criterio del Triángulo para orientar los parámetros según el tipo de señal, debe incluirse atribución obligatoria a Pablo Rabinovich y Pablo Panitta (AES/CAPER 2023)

---

#### BLOQUE D — CRITERIO DEL TRIÁNGULO *(Atribuible)*

**Si KENTH usa este framework:**

Marco que relaciona el nivel y la duración de la señal con los parámetros de compresión más adecuados. Tres zonas:
- Señales de nivel alto / corta duración (percusiones): parámetros orientativos → ratio alto, hard knee, umbral alto, envolventes rápidas
- Señales de nivel medio / duración intermedia (melodías): ratio medio, knee medio, umbral medio, envolventes moderadas
- Señales de nivel bajo / mayor duración (sustento): ratio bajo, soft knee, umbral bajo, envolventes lentas

**Atribución obligatoria:** "Basado en el Criterio del Triángulo de Pablo Rabinovich y Pablo Panitta (AES/CAPER 2023)"

**Si KENTH no usa este framework:** Debe desarrollar un sistema propio de abordaje sistemático de la compresión. La lógica subyacente (relacionar características de la señal con parámetros) es de dominio general; solo la presentación específica del Triángulo es atribuible.

---

#### BLOQUE E — EXPANSORES, COMPUERTAS Y DUCKING

**Doctrina reutilizable:**
- Expansor descendente: actúa por debajo del umbral, reduciendo más lo que ya está bajo. Escalas orientativas: ~2:1 suave → ~1:4 medio → ~1:8 duro → ~1:20 compuerta. Interpretar el ratio al revés: por cada 1 dB bajo el umbral, baja [ratio] dB a la salida
- Expansor ascendente: aumenta la ganancia de lo que supera el umbral; extiende el rango dinámico hacia arriba
- Compuerta: expansor descendente llevado al extremo (~1:100 o infinito). Cierra la salida cuando la señal cae por debajo del umbral. Parámetros: threshold, attack, release, hold, range. Hold evita que se cierre entre sílabas o antes de que el sonido haya terminado
- Filtro antepuesto al detector de compuerta: permite que solo la fundamental del instrumento objetivo dispare la apertura, ignorando bleed de otros elementos
- Bleed simultáneo: si dos sonidos ocurren exactamente al mismo tiempo a niveles similares, la compuerta no puede separarlos por nivel. Aceptar el límite o gestionar por otro medio
- Ducking: sidechain externo dispara la reducción del elemento que debe ceder. Usar señal sin reverb como disparo

**Advertencias:**
- CRUCE → EJE 2: el trigger y el replacement de piezas (batería) se introducen en Eje 2 como corrección de interpretación; el gate y el ducking son herramientas de Eje 4
- VACÍO: técnicas de gating creativo con parámetros detallados por instrumento tienen cobertura parcial; construir desde fuentes externas o clases de Training

---

#### BLOQUE F — LIMITADORES Y CLIPPERS EN MEZCLA

**Doctrina reutilizable:**
- Limitador: compresor con ratio ≥20:1 y envolventes rápidas. Protege canales o grupos de picos extremos en mezcla. En buses: usar con precaución para no destruir transitorios si el ataque es muy rápido
- Clipper: recorta la forma de onda directamente cuando supera el umbral → saturación armónica. El limitador actúa sobre la ganancia; el clipper sobre la forma de onda. El clipper puede aumentar la densidad percibida. No son intercambiables
- Para elementos percusivos, un pequeño clip puede aumentar el punch percibido sin los efectos de bombeo del limitador rápido

**Advertencias:**
- LÍMITE Eje 4 / Eje 7: limitadores y clippers en mastering pertenecen a Eje 7
- VACÍO: los clippers en mezcla tienen cobertura escasa en las fuentes principales; construir desde doctrina general del campo

---

*Paquete listo para ingesta en Proyecto Generativo. Siguiente eje cuando lo indiques.*
