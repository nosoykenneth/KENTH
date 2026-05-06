---

course_id: mezcla_masterizacion_kenth
module_id: M05
module_order: 5
module_title: Procesadores dinámicos
module_slug: procesadores-dinamicos
doc_type: source_dossier
source_origin: author_compiled_from_transcripts
filename: M05_dossier_fuente.md
version: 0.1
status: draft_source_compilation
curation_source: extraccion_exhaustiva_notebooklm_desde_clases_definitivas
ready_for_indexing: false
-------------------------

# M05 — Dossier fuente exhaustivo

## Procesadores dinámicos

> Este documento NO es guia canonica.
> NO es FAQ.
> NO es glosario final.
> Es una fuente intermedia exhaustiva, reorganizada por modulo, construida a partir de clases definitivas corregidas.
> Su objetivo es preservar detalle, matices, ejemplos, advertencias y trazabilidad antes de condensar doctrina para el RAG.

## 1. Alcance del dossier

* Este dossier reúne y reorganiza el material correspondiente al módulo **Procesadores dinámicos**, incluyendo:

  * doctrina base de compresión, expansión, compuertas, limitación y sidechain
  * distinciones técnicas entre arquitecturas, detectores, topologías y modos de enlace estéreo
  * procedimientos prácticos de parametrización y ruteo
  * preguntas de estudiantes que sí abren doctrina, corrigen errores o agregan técnica
  * advertencias del profesor sobre distorsión, autoengaño por volumen, orden de flujo de señal y mal uso de herramientas
  * contenido que apareció disperso en clases de mezcla, mastering, fase, EQ, efectos o training, pero que doctrinalmente pertenece a M05
* El dossier **no** busca:

  * convertir todavía el material en guía pedagógica final
  * resumir agresivamente
  * homogeneizar en exceso al punto de borrar matices, tensiones o repeticiones útiles
* El dossier **sí** conserva:

  * reglas y fórmulas cuando aparecieron
  * valores numéricos, tiempos y dB sensibles al contexto
  * analogías del profesor cuando ayudan a fijar doctrina
  * modelos concretos de compresores y plugins usados como referencia
  * distinción entre uso técnico correctivo y uso artístico deliberado

## 2. Núcleo conceptual del módulo

* **Objetivo fundacional de la compresión**

  * La compresión nace como necesidad técnica para adaptar señales con gran rango dinámico a soportes de grabación con menor rango dinámico.
  * El problema original era evitar:

    * saturación o clipping por arriba
    * piso de ruido por abajo
  * El ejemplo de fondo es la diferencia entre una fuente real con enorme rango dinámico y un soporte como vinilo o cinta.

* **Cuatro comportamientos dinámicos básicos**

  * El módulo no reduce la dinámica a “compresores” solamente.
  * Se presentan dos grandes familias y cuatro comportamientos:

    * **Compresor descendente:** reduce ganancia a lo que supera el umbral.
    * **Expansor ascendente:** aumenta ganancia a lo que supera el umbral.
    * **Expansor descendente / compuerta:** reduce ganancia a lo que queda por debajo del umbral.
    * **Compresor ascendente:** aumenta ganancia a lo que queda por debajo del umbral.
  * Esta clasificación aparece reforzada en más de una clase y sirve como marco general de todo el módulo.

* **Lógica real de acción del compresor**

  * El compresor no es “un fader automático que baja todo parejo”.
  * Su cálculo se realiza sobre el **excedente** por encima del umbral.
  * Ese excedente se divide por el **ratio**, por lo que:

    * cuanto más lejos está una parte de la señal del umbral, más severamente será castigada
    * la deformación dinámica es no lineal
    * una automatización de fader no equivale matemáticamente a una compresión

* **Parámetros nucleares**

  * **Threshold / Umbral:** nivel a partir del cual el circuito comienza a actuar.
  * **Ratio:** severidad matemática de la reducción o expansión.
  * **Attack:** velocidad con la que el procesador alcanza la reducción de ganancia una vez superado el umbral.
  * **Release:** velocidad con la que retorna a unidad cuando la señal cae por debajo del umbral.
  * **Knee:** forma de transición entre no actuar y actuar; puede ser más blanda o más dura.
  * **Make-up gain:** compensación posterior de nivel, presentada en el módulo como parámetro extremadamente delicado y potencialmente engañoso.
  * **Hold:**

    * en compresores: tiempo durante el cual se sostiene la reducción máxima antes de empezar a liberar
    * en compuertas: tiempo que la compuerta permanece abierta antes de comenzar el cierre
  * **Look-ahead:** anticipación basada en retrasar internamente la señal útil para que el detector alcance a actuar antes del transitorio real.
  * **Range:**

    * especialmente en compuertas y expansores
    * delimita cuántos dB se aplicará la caída severa
    * evita el corte brutal a silencio absoluto

* **Sidechain / cadena lateral**

  * El detector no necesariamente escucha lo mismo que sale por audio útil.
  * La cadena lateral puede:

    * leer una copia interna de la propia señal
    * recibir una señal externa por **Key Input**
    * ser filtrada para ignorar ciertas zonas espectrales
  * El módulo insiste en que muchas decisiones dinámicas correctas dependen más de **qué oye el detector** que del ratio en sí.

* **De-esser como caso particular**

  * El de-esser es presentado como un compresor cuyo sidechain está filtrado para reaccionar desproporcionadamente ante la banda de sibilancia humana, aproximadamente entre 4 y 10 kHz.
  * Se enfatiza que su lógica es dinámica, no meramente ecualizadora estática.

## 3. Distinciones clave del módulo

* **Uso técnico vs uso artístico de la compresión**

  * **Uso técnico**

    * busca controlar picos o estabilizar sin que se note el efecto
    * attack y release deben “copiar en espejo” la envolvente del problema
    * se usa para corrección o control
  * **Uso artístico**

    * busca que la compresión se note
    * puede generar bombeo, swing, golpe, timbre, carácter o distorsión armónica
    * el release puede ajustarse rítmicamente respecto al tempo para lograr groove

* **Detector Peak vs detector RMS**

  * **Peak**

    * sigue variaciones instantáneas
    * ideal para transientes
    * con mayor riesgo de distorsión si se usa con envolventes violentas
  * **RMS**

    * lee promedio de energía
    * genera respuesta más estable
    * la aguja o reducción debe comportarse como una “ameba” o “babosa”, no nerviosa
  * Esta distinción se conecta con la diferencia entre:

    * caza de picos
    * nivelación
    * glue o pegamento

* **Feed-forward vs feedback**

  * **Feed-forward**

    * el sidechain toma la señal antes del elemento reductor de ganancia
    * suele ser más agresivo y preciso
  * **Feedback**

    * el sidechain toma la lectura después de que la señal fue comprimida
    * típico de equipos vintage
    * tiende a ser más estable y suave

* **Compresor multibanda vs ecualizador dinámico**

  * **Multibanda**

    * divide la señal completa mediante crossovers
    * implica rotación de fase estructural
    * usa ratios por zonas anchas del espectro
    * orientado a control global o por bandas extensas
  * **EQ dinámico**

    * usa campanas o shelves individuales
    * trabaja con un parámetro de range en lugar de ratio clásico por banda
    * no necesita crossovers globales
    * sirve mejor para cirugía puntual e intermitente
  * Se refuerza que:

    * multibanda = más útil para control global, incluso en mix bus
    * EQ dinámico = mejor para problemas específicos como sibilancias, resonancias o notas problemáticas

* **Ducking vs sidechain como término**

  * El módulo trata el ducking como técnica específica nacida en broadcasting:

    * una señal A baja cuando el compresor es disparado por una señal B
  * El profesor lo presenta como un caso concreto de uso de sidechain externo, y en ciertas clases lo llama “falsamente sidechain” cuando en realidad se refiere al uso más popular del término.

* **Estéreo linkeado, dual mono y link porcentual**

  * **Dual mono**

    * cada canal se comprime por separado
    * útil en señales mono aisladas
    * riesgoso en buses estéreo porque puede desarmar la imagen
  * **Link 100%**

    * cualquier exceso en un canal arrastra la reducción del otro
    * protege la imagen estéreo
    * puede hacer que un evento fuerte paneado a un lado hunda indebidamente información del otro
  * **Link porcentual**

    * compromiso intermedio
    * un canal arrastra parcialmente al otro
    * conserva mejor espacialidad sin dejar saltos bruscos

* **Topologías clásicas y clasificación correcta**

  * La clasificación no se hace por marketing ni por el hecho de que un equipo tenga válvulas en otra parte del circuito.
  * Se clasifica por el elemento que **efectivamente realiza la reducción de ganancia**.
  * Distinciones nucleares:

    * **Óptico**
    * **FET**
    * **VCA**
    * **Vari-Mu / valvular puro**
    * **Puente de diodos**

* **Opto vs Electro en el Renaissance Compressor**

  * No es un simple nombre de color.
  * Determina la curva de release:

    * **Opto:** recuperación exponencial; vuelve rápido al principio y cada vez más lento al final
    * **Electro:** comportamiento más lineal, con retorno final más veloz
  * Se presenta como una diferencia de musicalidad y balística, no solo de tono.

## 4. Compresión, expansión y lógica de control dinámico

* **Método del Triángulo**

  * El docente propone un triángulo mental:

    * base = tiempo
    * altura = amplitud
  * Tres zonas principales:

    * **Zona alta (picos / transientes)**

      * objetivo: limitación o caza de picos
      * umbral alto
      * ratio alto
      * hard knee
      * attack rápido
      * release rápido
    * **Zona media (melodía)**

      * objetivo: nivelación
      * umbral medio
      * ratio medio
      * knee medio o suave
      * envolventes medias
    * **Zona baja (sustento / base / densidad)**

      * objetivo: incremento de RMS o densidad
      * umbral bajo
      * ratio bajo
      * soft knee
      * attack lento
      * release lento
  * Regla explícita:

    * un solo compresor no debe intentar resolver las tres zonas a la vez
    * si se buscan varios objetivos, se encadenan compresores en serie
    * ejemplo doctrinal: un **LA-2A** para ablandar o nivelar y luego un **1176** para cazar picos

* **Attack y Release: definición operativa correcta**

  * El módulo corrige de forma frontal el mito de internet:

    * no son tiempos de espera
    * no son delays previos a actuar
  * Son velocidades de transición.
  * Analogía del auto:

    * si un auto va a 100 km/h y debe bajar a 60, no “espera” antes de frenar
    * tarda un tiempo en desacelerar progresivamente
  * Esta analogía se usa para fijar la idea de que el cambio de ganancia es gradual, no un interruptor.

* **Hold y Look-ahead**

  * **Hold**

    * en compresión: sostiene el máximo de reducción antes de liberar
    * ayuda a estabilizar la onda y a bajar distorsión
    * en compuertas: sostiene apertura antes del cierre
  * **Look-ahead**

    * no implica ver el futuro
    * el circuito retrasa la señal útil para dar tiempo al detector
    * requiere compensación de delay dentro del DAW

* **Expansión ascendente**

  * No se presenta como exotismo teórico sino como recurso práctico.
  * Puede usarse en paralelo para empujar transientes hacia arriba sin subir el fader general.
  * Aplicación ejemplificada:

    * batería ahogada en un estribillo
    * envío prefader
    * procesador configurado como expansor ascendente
    * attack y release rápidos para “agarrar solo el golpe”

* **Compresión paralela**

  * Definida como envío de la señal limpia prefader a un auxiliar.
  * En la rama paralela se aplica compresión extrema.
  * Luego se hace blend con la original.
  * Resultado buscado:

    * traer la fuente al frente
    * engrosar
    * extraer detalles mínimos
    * añadir armónicos y carácter
    * sin destruir los picos de la señal seca
  * Se insiste en que esta técnica puede ser:

    * correctiva en ciertos casos
    * claramente artística en otros, especialmente en voz

* **Compuertas y expansión descendente**

  * No se limitan a “sacar ruido”.
  * También sirven para:

    * esculpir tiempo
    * modificar transientes
    * diseñar cola y duración
    * reconfigurar el timbre percusivo
  * La compuerta extrema se explica como una “llave”:

    * ratio 1:100
    * o pasa o no pasa
  * El parámetro **Range** permite hacer esta lógica menos brutal.

* **Ducking y control por cadena lateral externa**

  * Ejemplos doctrinales:

    * bajo que se comprime cuando golpea el bombo
    * música que baja cuando entra la voz
  * El módulo amplía esto a:

    * ducking multibanda
    * ducking en matriz Mid
    * ducking sobre colas de delay y reverb
    * ducking como solución de fase y limpieza temporal
  * Punto fuerte:

    * muchas veces el resultado depende de estabilizar la señal que dispara el sidechain, no solo de cambiar ratio o threshold

* **Limitación**

  * Se presenta como zona extrema de la compresión.
  * La clasificación general ubica la limitación desde ratios altos, pero en mastering el módulo distingue además una lógica propia:

    * un limitador genuino tiene ataque imperativamente instantáneo
    * ciertas perillas llamadas “attack” en limitadores comerciales suelen ser en realidad:

      * anticipación
      * inicio de release adaptativo
      * o parámetros de otra capa interna
  * La tensión central del limitador de mastering se ubica entre:

    * distorsión
    * preservación del ciclo grave
    * loudness comercial

## 5. Ejemplos técnicos que no deben perderse

* **Compresión paralela artística de voz con LA-2A**

  * Voz enviada prefader a auxiliar.
  * Inserción de Teletronix LA-2A.
  * Reducción extrema de 10 a 20 dB.
  * Luego se sube esa rama y se mezcla con la original.
  * Efectos buscados:

    * traer la voz al frente
    * rescatar respiraciones y detalles interpretativos
    * engrosar medios-bajos
    * añadir “arenilla” y calidez
  * El ejemplo se presenta como decisión estética, no como control quirúrgico.

* **Aliasing por compresión y mitigación con Oversampling + Hold**

  * El docente pasa una senoidal de 1000 Hz a -18 dBFS por un compresor reduciendo 3 dB.
  * Se demuestra que la simple acción de la envolvente ya genera distorsión armónica y aliasing.
  * Para procesos limpios, especialmente en mastering:

    * activar oversampling
    * mínimo 4x en sesiones a 44.1/48 kHz
    * usar hold, por ejemplo 1 ms, para estabilizar la reducción

* **Ducking estabilizado mediante copia comprimida de la voz**

  * Problema:

    * si la voz que dispara el ducking tiene demasiada dinámica, la música sube y baja erráticamente
  * Solución:

    * crear un auxiliar paralelo de la voz
    * comprimir esa copia de forma brutal
    * usar esa copia estabilizada como Key Input del compresor de la música

* **Expansión ascendente paralela en batería**

  * Aplicada cuando la batería pierde golpe en el estribillo.
  * En vez de subir el fader general:

    * envío prefader
    * expansión ascendente o compresor configurado para empujar transientes
    * attack y release rápidos
  * El resultado es recuperación de la transiente y del punch sin consumir masivamente el headroom.

* **Gate en bombo con filtro en detector**

  * Para sacar bleed del tambor o de platos dentro del micrófono del bombo:

    * ratio extremo tipo llave
    * low-pass en detector hasta alrededor de 80 Hz
    * ataque ajustado para alterar el clic del mazo
    * hold para dejar pasar la resonancia natural del cuerpo antes del cierre
  * El ejemplo enseña simultáneamente:

    * eliminación de bleed
    * modelado tímbrico
    * control de cola

* **Ducking multibanda en Mid para conflicto bombo-bajo**

  * Se usa Pro-MB u otro multibanda con sidechain externo desde el bombo.
  * Solo se afecta la banda problemática.
  * El procesamiento se restringe a la sección **Mid**.
  * Se preserva la información lateral y aguda del bajo mientras se despeja el centro.

* **Ecualización dinámica híbrida en Mid para tensión vocal**

  * En una masterización de bolero se detecta tensión vocal en 1.3–1.5 kHz.
  * Para no hundir guitarras ni platillos:

    * matriz M/S
    * Waves C4 solo en el canal Mid
    * ataque muy lento para dejar pasar transientes útiles
    * release de 300 ms
    * uso de range negativo
  * Se presenta como caso fino de parametrización dinámica selectiva dentro de una mezcla ya cerrada.

* **Ducking en Overheads para volver despreciable el comb filtering**

  * Problema:

    * un tambor cercano compite en fase con su bleed en overheads
  * En lugar de seguir rotando fase:

    * se inserta un compresor en overheads
    * disparado por sidechain desde el tambor cercano
    * ataque rapidísimo
    * atenuación superior a 9 dB en el instante del golpe
  * La lógica invocada es que la diferencia de nivel vuelve la interferencia acústicamente despreciable por la regla 3:1.

* **Clippers en mezcla y limitador en etapa comercial**

  * Para obtener loudness alto sin destruirlo todo en el limitador final:

    * el clipping se distribuye antes, en grupos de batería o elementos percusivos
  * El clipper:

    * recorta físicamente la transiente
    * genera armónicos impares
    * aumenta la percepción subjetiva de volumen
  * Así se alivia la carga del limitador de mastering.

* **Diseño de punch en el bajo**

  * El docente aclara que ecualizar en 800 Hz no siempre basta.
  * Puede ser necesario **forzar una transiente física**.
  * Dos vías ejemplificadas:

    * VCA tipo Smack! o Vertigo con attack lento y release rápido para dejar salir la transiente
    * expansor ascendente con attack rápido para empujar el arranque de la nota y luego comprimir el cuerpo

* **Compresión sobre colas de delay y reverb**

  * En vez de depender del predelay del efecto:

    * se inserta un compresor después del delay o de la reverb
    * el detector es disparado por la pista seca original
  * Mientras el instrumento canta o golpea, el efecto queda planchado.
  * Cuando el instrumento calla, el release permite que el efecto suba y ocupe el silencio.

## 6. Preguntas de estudiantes que sí aportan contenido

* **Sobre el release rítmico**

  * Pregunta: si se usa el compresor rítmicamente, ¿el release debe ajustarse al swing o al tempo?
  * Aporte doctrinal:

    * sí, cuando el uso es artístico
    * no bajo la misma lógica cuando el uso es técnico
    * en uso técnico el release debe copiar la envolvente del problema para que no se note

* **Sobre el ataque ultrarrápido en 1176**

  * Pregunta: si quiero atrapar picos rápidos, ¿por qué no usar el ataque al máximo de rapidez?
  * Aporte doctrinal:

    * porque un FET ultrarrápido puede comerse toda la transiente
    * eso destruye definición y altera el timbre
    * controlar un pico no equivale a borrar la identidad del golpe

* **Sobre compuertas y ruido eléctrico continuo**

  * Pregunta: ¿una compuerta sirve para quitar el hiss o hum de un amplificador mientras el instrumento está tocando?
  * Aporte doctrinal:

    * no
    * la compuerta solo silencia cuando la señal cae por debajo del umbral
    * cuando la fuente toca y supera el umbral, el ruido incrustado pasa con ella
    * para ruido embebido se requiere de-noiser, no dinámica de amplitud

* **Sobre necesidad de comprimir otra vez en mastering**

  * Pregunta: si el mix bus ya fue comprimido para glue, punch o RMS, ¿es obligatorio volver a comprimir en mastering?
  * Aporte doctrinal:

    * no existe obligación
    * si la mezcla ya tiene consistencia dinámica, el mastering puede ir directo a limitación
    * o requerir apenas compresión ultratransparente de medio decibel
    * se rechaza la cadena fija por dogma

* **Sobre fase en compresión paralela**

  * Pregunta: ¿mezclar señal limpia con señal paralela comprimida trae problemas de fase?
  * Aporte doctrinal:

    * sí puede haber microalteraciones porque muchos compresores analógicos o sus modelados no son totalmente planos en fase
    * esa microalteración suele ser parte del color deseado
    * rara vez es destructiva por sí sola
    * el riesgo aumenta si además se insertan EQ de fase no lineal extrema en la rama paralela

## 7. Advertencias, matices y correcciones del profesor

* **No evaluar dinámica a más volumen**

  * Regla de cátedra:

    * toda comparación debe hacerse al mismo volumen percibido
  * Motivo:

    * por curvas isofónicas, lo más fuerte suele parecer mejor aunque esté peor
  * Se exige igualar salida del procesador o out ceiling antes del A/B.
  * El mismo criterio se extiende al mastering con limitadores.

* **Peligro del make-up gain**

  * No debe compensarse automáticamente la reducción de ganancia solo porque el manual lo sugiera.
  * El make-up sube:

    * susurros
    * respiraciones
    * bleed
    * ruido de fondo
    * barullo de sala
    * platos o sibilancias que no eran el problema original
  * El módulo insiste en que un control de picos no debe convertirse ciegamente en una subida global de todo el canal.

* **Envolventes rápidas en graves = distorsión**

  * Advertencia fuerte:

    * ataques y releases demasiado rápidos en material grave mutilan el ciclo físico de la onda
  * Regla conservada:

    * attack > semiperíodo de la frecuencia más grave
    * release > período
  * Ejemplo explicitado:

    * 41 Hz ≈ 24 ms de período y ≈ 12 ms de semiperíodo
  * Se aclara que esta formulación requiere prudencia contextual, pero la doctrina central es firme:

    * los graves prohíben envolventes hiperrápidas si se quiere evitar ronquido y distorsión

* **Compuertas en material melódico**

  * El profesor las llama fenómenos antinaturales si se usan mal.
  * Riesgo:

    * mutilar crecimiento de consonantes o envolventes suaves
    * convertir acústicamente una “D” en “T”
  * Se presentan como brillantes en batería y peligrosas en voces, cuerdas, vientos o material de aire.

* **El ratio en ciertos analógicos altera también el knee**

  * En SSL y 1176, cambiar ratio no solo cambia la matemática de reducción.
  * También modifica físicamente la rodilla.
  * Resultado:

    * el aparato cambia de comportamiento musical
    * al subir ratio puede parecer incluso que comprime menos antes del punto duro, porque la transición se endurece

* **No creer que todos los milisegundos significan lo mismo**

  * Los fabricantes usan criterios distintos:

    * 10/90%
    * 63%
    * primeros 3 dB
    * incluso 40% en algunos casos mencionados
  * Consecuencia:

    * “30 ms” en un equipo no equivale a “30 ms” en otro
  * Mandato del módulo:

    * dejar de comprimir mirando números
    * ajustar a oído y por efecto real

* **LA-2A no es valvular en la clasificación topológica**

  * Aunque tenga tubos en su etapa de ganancia, la reducción la realiza la célula óptica T4.
  * Por tanto:

    * es **óptico**
    * no Vari-Mu
  * Vari-Mu real: Fairchild o Manley.

* **SSL no colorea masivamente por existir**

  * El mito del gran color SSL es corregido con medición.
  * Se reporta que:

    * el botón Analog inyecta hiss alrededor de -130 dB
    * la distorsión armónica en reposo puede estar por debajo de -100 dB
  * Se atribuye gran parte del placebo al make-up gain activado por defecto en ciertos plugins.

* **Sibilancia y compresión**

  * La “S” tiene menos amplitud física que las vocales abiertas.
  * El compresor aplasta las vocales, pero muchas veces deja relativamente intacta la “S”.
  * Luego el make-up la sube hasta volverla filosa.
  * Consecuencia doctrinal:

    * compresión vocal estática suele exigir de-esser o EQ dinámico
    * no se corrige con EQ estático fijo si la sibilancia es intermitente

* **Filtros antes del compresor pueden alterar la detección**

  * Todo filtro, especialmente de pendiente abrupta, reordena la onda por rotación de fase.
  * Eso puede generar overshoot.
  * Si luego un detector Peak lee esa señal:

    * reaccionará a picos nuevos que antes no estaban
    * aunque el RMS no haya cambiado
  * Esto obliga a considerar seriamente el orden de cadena.

* **El compresor del SSL no debería recibir subsónicos innecesarios**

  * Regla operativa:

    * en channel strip SSL conviene usar **Split**
    * reordenando a Entrada → Filtros → Dinámica → EQ
  * Justificación:

    * si el detector recibe primero toda la basura subsónica, comprimirá por información inútil

* **El limitador real no tiene ataque “usable” en sentido clásico**

  * Un limitador de mastering genuino actúa desde la primera muestra.
  * Las perillas llamadas attack en ciertas interfaces suelen nombrar otra cosa.
  * El parámetro realmente peligroso frente al subgrave es el release.

* **No todo problema temporal se corrige con EQ**

  * Si el tom resuena demasiado, el problema puede no ser la frecuencia sino el tiempo que dura.
  * En ese caso el EQ destruye identidad tonal.
  * La corrección correcta se desplaza a gate, hold y release.

## 8. Herramientas, referencias técnicas, configuraciones y detalles operativos

* **Topologías y modelos citados**

  * **Ópticos**

    * Teletronix LA-2A
    * modelados mencionados: UAD, Waves, IK Multimedia
    * célula T4, ataque fijo, liberación de dos etapas, musicalidad alta
  * **FET**

    * 1176
    * muy veloz, con carácter y distorsión armónica marcada
    * ratio interactivo con knee
  * **VCA**

    * SSL Bus Compressor
    * API 2500
    * Vertigo VSC-2
    * Smack! en uso práctico
    * orientación a precisión, glue, punch y control de grupos
  * **Vari-Mu / valvulares puros**

    * Fairchild 670
    * Manley Vari-Mu
    * lentos, cremosos, asociados a pegamento global
  * **Puente de diodos**

    * Neve 2254
    * compresor y limitador separados dentro de la misma unidad
  * **Digitales quirúrgicos**

    * FabFilter Pro-C 2
    * FabFilter Pro-MB
    * FabFilter Pro-Q 4
    * Waves C4
    * Renaissance Compressor
    * herramientas destacadas por oversampling, hold, look-ahead, M/S, sidechain externo y precisión

* **Carácter resumido de topologías**

  * **LA-2A / óptico**

    * lento
    * release físico tipo lámpara/fotorresistencia
    * rey en voces, cuerdas y vientos
    * inútil para control quirúrgico de batería
  * **1176 / FET**

    * ideal para picos rápidos, guitarras percusivas y rooms
    * si se exagera el ataque puede destruir la transiente
  * **VCA de bus**

    * aptos para administrar varias señales al mismo tiempo
    * asociados a glue y punch
  * **Vari-Mu**

    * utilizados para consistencia y amalgama global
  * **Puente de diodos**

    * carácter más raro y menos “patada”; comparación sensorial conservada:

      * API en graves puede sentirse como “patada en el estómago”
      * Neve 2254 más como “empujón”

* **Configuraciones operativas conservadas**

  * **Oversampling en dinámica**

    * mínimo 4x a 44.1/48 kHz para usos exigentes
    * en limitación de mastering, tanto como la máquina tolere offline
  * **Hold**

    * ejemplo operativo preservado: 1 ms para estabilizar compresión limpia
  * **1176**

    * ataque y release invertidos respecto a la intuición moderna:

      * hacia la derecha = más rápido
    * modo **All Buttons**:

      * compresión extrema
      * alta distorsión
      * posible comportamiento anómalo en la curva
      * usado en rooms de batería y efectos agresivos
  * **API 2500**

    * circuito **Thrust**:

      * Normal / Mid / Loud
      * filtro tilt previo al detector
      * evita que graves hundan indebidamente la mezcla
  * **Stereo Link porcentual**

    * ejemplo doctrinal: 50% o 70% como compromiso útil en buses estéreo
  * **Fairchild 670**

    * posición 1: attack 200 μs / release 300 ms
    * posición 4: release hasta 5 s y comportamiento muy lento
    * posiciones 5 y 6: auto-release dependiente del programa, con recuperaciones totales de 10 a 25 s en material complejo
  * **Release de 300 ms**

    * presentado como punto de partida prudente en voces o en glue que persiga lenguaje/sílaba
    * conectado a la duración estadística de una sílaba y a la balística tipo VU
    * no debe leerse como ley universal

* **Ratios y rangos preservados**

  * Compresión suave: hasta 2:1
  * Compresión media: alrededor de 4:1
  * Compresión dura: desde 8:1
  * Limitación: desde 10:1 o 20:1
  * Compuerta dura tipo llave: 1:100
  * Range de 60 dB en gate:

    * equivale a atenuar un millón de veces
    * asegura silencio acústico práctico
  * Ejemplo explicativo de range:

    * threshold -20 dB y range -10 dB
    * la caída fuerte opera de -20 a -30 dB
    * por debajo, la señal vuelve a 1:1 pero desplazada 10 dB hacia abajo

* **Ruteos y arquitectura operativa**

  * **HPF manual para sidechain**

    * si el compresor no tiene filtro de sidechain:

      * enviar mezcla a auxiliar prefader
      * filtrar graves en esa copia
      * mandar esa copia por bus ciego al Key Input
    * el compresor sigue procesando todo el programa, pero comandado por señal depurada
  * **M/S en dinámica**

    * usado para:

      * ducking selectivo del bajo frente al bombo solo en Mid
      * control de tensión vocal en 1.3–1.5 kHz solo en Mid
    * propósito:

      * preservar lados y apertura mientras se corrige el centro
  * **Jerarquía individual vs grupal**

    * en guitarras dobladas o coros múltiples:

      * primero control individual de microdinámica
      * luego compresión grupal lenta y suave para glue
    * se prohíbe como primera instancia comprimir el bus si eso hará que una toma sana pague por el pico de otra

* **Diagnóstico operativo**

  * **Botón Listen del sidechain**

    * permite oír qué está comandando realmente al compresor
    * revela si el detector está siendo arrastrado por subgraves, toms u otra información parásita
  * **Compensación isométrica de nivel**

    * bajar la salida en proporción a la ganancia percibida que se ganó
    * condición obligatoria para juzgar si la mejora es real
  * **Modo Delta / inversión de polaridad**

    * duplicar master
    * quitar limitador a una copia
    * igualar niveles
    * invertir polaridad
    * residuo:

      * solo clics = limitador capturando picos de forma sana
      * media canción = limitación destructiva

## 9. Contenido dislocado que sí pertenece a M05

* **Clase 28 — tensión vocal controlada con dinámica híbrida**

  * Waves C4 en matriz Mid/Side únicamente en Mid.
  * Banda problemática en 1.3–1.5 kHz.
  * Ataque lento para dejar pasar transientes útiles.
  * Release de 300 ms.
  * Range negativo.
  * Pertenece a M05 porque el núcleo del ajuste no es meramente tonal sino de **envolvente y disparo dinámico selectivo**.

* **Clase 10 — ducking en overheads para mitigar comb filtering**

  * Compresor en overheads disparado desde el tambor cercano.
  * Ataque rapidísimo y caída superior a 9 dB durante el golpe.
  * Pertenece a M05 porque resuelve un problema de fase mediante una decisión puramente dinámica.

* **Clase 5 y Clase 25 — clipping distribuido antes del limitador final**

  * Se enseña que el limitador comercial no debe cargar solo con todos los picos.
  * El clipping previo en grupos o elementos percusivos pertenece a M05 por tratarse de control extremo de transientes y loudness por etapas.

* **Clase 11 — overshoot por filtros y reacción errática del detector Peak**

  * Se advierte que el detector dinámico depende físicamente del tratamiento previo.
  * El problema aparece fuera del núcleo de dinámica, pero doctrinalmente pertenece a M05 porque condiciona la respuesta del compresor.

* **Clase 14 — orden del flujo de señal con botón Split en SSL**

  * El routing correcto se fija para que filtros limpien la señal antes de que el detector la lea.
  * Aunque surge en arquitectura de canal, es contenido funcionalmente central para dinámica.

* **Clase 22 — gate como sintetizador de tiempo**

  * Cuando un tom dura demasiado, el error es intentar “matarlo” por EQ.
  * El docente recoloca la solución en hold y release.
  * Pertenece a M05 porque redefine la compuerta como herramienta de diseño temporal.

* **Clase 23 — sidechain HPF manual y ducking multibanda en Mid**

  * Dos aportes operativos relevantes:

    * construcción manual de sidechain filtrado
    * conflicto bombo-bajo resuelto solo en banda y solo en Mid
  * Ambos son extensión avanzada del control dinámico.

* **Clase 22 y 24 — compresión disparada sobre colas de efectos**

  * Control dinámico aplicado a reverbs y delays usando la pista seca como disparador.
  * Complemento claro de M05 porque se basa en sidechain externo y release musical.

* **Clase 24 — jerarquía entre compresión individual y compresión de grupo**

  * Control individual de picos antes de glue grupal.
  * Reubica la dinámica dentro del flujo de mezcla y de la relación micro/macro dinámica.

* **Clase 27 — diagnóstico clínico de limitación**

  * Validación por igualdad de volumen y por Delta.
  * Aclara además que el supuesto “attack” del limitador suele ser engañoso y que la verdadera zona crítica frente al subgrave es el release.
  * Aunque aparezca en mastering, pertenece directamente al núcleo de M05.

## 10. Mapa de cobertura

* **Fundamentos y definición**

  * origen técnico de la compresión
  * cuatro comportamientos dinámicos básicos
  * lógica no lineal del compresor

* **Parámetros y constantes**

  * threshold
  * ratio
  * attack
  * release
  * knee
  * hold
  * look-ahead
  * range
  * make-up gain

* **Lógica de detección y arquitectura**

  * detector Peak y RMS
  * feed-forward y feedback
  * listen de sidechain
  * filtrado del detector
  * HPF manual para key input
  * orden correcto de flujo antes de dinámica

* **Familias de procesadores**

  * compresor descendente
  * compresor ascendente
  * expansor ascendente
  * expansor descendente
  * compuerta
  * limitador
  * compresor multibanda
  * de-esser
  * ecualizador dinámico como herramienta emparentada

* **Topologías y modelos**

  * óptico / LA-2A
  * FET / 1176
  * VCA / SSL, API 2500, Vertigo
  * Vari-Mu / Fairchild, Manley
  * puente de diodos / Neve 2254
  * digitales quirúrgicos / Pro-C 2, Pro-MB, Pro-Q 4, C4, Renaissance Compressor

* **Aplicaciones correctivas**

  * caza de picos
  * control de bleed con gate
  * de-essing
  * ducking puntual
  * corrección de resonancias intermitentes con EQ dinámico
  * resolución de enmascaramiento bombo-bajo en Mid
  * control temporal de colas y resonancias

* **Aplicaciones artísticas**

  * compresión paralela
  * expansión ascendente para punch
  * glue de bus
  * bombeo y swing
  * coloración armónica deliberada
  * diseño de envolvente en bajo, batería, rooms y voces

* **Advertencias mayores**

  * make-up gain engañoso
  * autoengaño por volumen
  * distorsión por envolventes rápidas en graves
  * compuertas antinaturales en material melódico
  * valores en ms no comparables entre plugins
  * ratio que altera knee en ciertos analógicos
  * overshoot por filtros antes del detector
  * limitación destructiva en mastering

* **Diagnóstico y validación**

  * escucha con niveles igualados
  * monitoreo del detector
  * Delta por inversión de polaridad
  * juicio crítico de residual dinámico

## 11. Trazabilidad principal por clases

* **Clase 5**

  * clipping distribuido en mezcla como alivio previo al limitador final

* **Clase 10**

  * ducking en overheads para volver despreciable el conflicto de fase con micros cercanos

* **Clase 11**

  * overshoot de filtros y su efecto sobre detectores Peak posteriores

* **Clase 14**

  * regla de flujo en SSL con Split: filtros antes de dinámica

* **Clase 15**

  * objetivo fundacional de la compresión
  * matemática real del compresor
  * definiciones correctas de attack y release
  * detectores Peak/RMS
  * feed-forward vs feedback
  * link estéreo y dual mono
  * make-up gain
  * de-esser
  * multibanda vs EQ dinámico
  * autoengaño por volumen
  * escucha del detector

* **Clase 16**

  * uso técnico vs artístico
  * método del triángulo
  * hold y look-ahead
  * aliasing por dinámica
  * oversampling y hold
  * ducking estable con copia comprimida
  * expansión ascendente paralela
  * distorsión por envolventes rápidas en graves

* **Clase 17**

  * topología óptica
  * LA-2A en profundidad
  * 1176 en profundidad
  * compresión paralela de voz
  * modo All Buttons
  * aclaración de que LA-2A no es Vari-Mu
  * interacción ratio/knee en analógicos

* **Clase 18**

  * VCA de bus
  * SSL, API, carácter y transparencia
  * glue y punch
  * thrust / tilt del detector
  * link porcentual
  * Neve 2254
  * release de 300 ms como punto de partida prudente
  * make-up y sibilancia

* **Clase 19**

  * refuerzo de las cuatro familias dinámicas
  * Vari-Mu y Fairchild
  * compresión paralela y microfase/color
  * valores de auto-release del Fairchild
  * oversampling en dinámica severa
  * sibilancia y necesidad de dinámica selectiva

* **Clase 20**

  * compuertas y expansión descendente
  * ratio 1:100
  * range
  * limitaciones de gate frente a ruido embebido
  * gate en bombo con detector filtrado y hold

* **Clase 22**

  * modo All Buttons reaparece
  * compuertas como herramientas de tiempo
  * compresión disparada sobre colas de efectos

* **Clase 23**

  * VCA práctico en bajo
  * diseño de punch
  * ducking multibanda en Mid
  * fabricación manual de HPF para sidechain

* **Clase 24**

  * compresión disparada sobre reverbs/delays
  * jerarquía entre compresión individual y de grupo

* **Clase 25**

  * clipping en mezcla como preparación de loudness comercial

* **Clase 26**

  * compresión en mastering no obligatoria
  * aclaración sobre falso attack en limitadores

* **Clase 27**

  * validación por igualdad de volumen
  * diagnóstico Delta
  * distorsión del limitador por release en subgraves

* **Clase 28**

  * ecualización dinámica híbrida en Mid para tensión vocal
  * refuerzo de distinción entre multibanda y EQ dinámico
  * uso prudente de release de 300 ms en contexto vocal
