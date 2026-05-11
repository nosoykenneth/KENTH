# EJE 6 — INTEGRACIÓN GLOBAL
### KENTH Academy · Mezcla y Masterización · Contenido Final de Curso

---

## SECCIÓN 1 — FUNCIÓN PRÁCTICA DEL EJE

El Eje 6 hace que todos los elementos de la mezcla funcionen como un sistema coherente, no como una suma de partes bien procesadas por separado.

Los Ejes 3, 4 y 5 definieron el carácter tonal, la energía dinámica y la posición espacial de cada elemento. Una mezcla puede tener cada instrumento perfectamente procesado y aun así sonar como una suma de elementos que no se integran. El Eje 6 es donde esa integración ocurre.

El eje tiene cinco dominios:

**Estructura de buses y stems:** cómo organizar la sesión para que las familias de instrumentos puedan procesarse como unidades, el mix bus pueda procesarse con independencia del Master Fader, y la arquitectura de la sesión soporte las decisiones de integración.

**Compresión de bus:** el compresor que opera sobre el mix bus no hace lo mismo que el compresor de canal del Eje 4. Su función es la cohesión —hacer que los elementos se muevan juntos— y tiene objetivos específicos: controlar picos, aumentar densidad, construir pegamento o reforzar el punch de la mezcla completa.

**Rango dinámico global:** qué nivel tiene la mezcla como sistema, cómo se expresa ese nivel (PLR, headroom), y qué implica para la entrega al masterizador.

**Automatización como cohesión:** la automatización en el Eje 6 no es corrección técnica puntual sino herramienta temporal: ajustar el comportamiento de la mezcla a lo largo del tiempo para que funcione como narración coherente.

**Coherencia de álbum:** cuando la mezcla es parte de un álbum, la coherencia entre canciones no ocurre sola. Requiere una práctica activa de referencia cruzada durante el proceso de mezcla.

**Límites del eje:**
- La mecánica del compresor (parámetros, circuitos, Criterio del Triángulo) ya se conoce del Eje 4 y no se repite aquí. El Eje 6 aplica esa mecánica al contexto específico del bus.
- El EQ de mastering sobre el programa completo pertenece al Eje 7. El Eje 6 incluye la verificación tonal del mix bus como paso previo a la entrega.
- El nivel de entrega de la mezcla cierra el Eje 6. El Eje 7 arranca desde lo que recibió.

---

## SECCIÓN 2 — QUÉ DEBE PODER HACER EL ALUMNO AL TERMINAR ESTE EJE

Al completar el Eje 6, el alumno es capaz de:

- Configurar una sesión con mix bus auxiliar separado del Master Fader y entender la función de cada uno.
- Organizar los instrumentos en buses de familia que incluyan sus efectos.
- Aplicar el principio de procesamiento por capas: elemento → grupo → mix bus.
- Identificar si la compresión de bus está haciendo trabajo que debería haberse resuelto en el procesamiento individual.
- Distinguir entre los cuatro objetivos de la compresión de bus (control de picos, densidad/RMS, pegamento, punch) y configurar los parámetros adecuados para cada uno.
- Activar el HPF en el sidechain del compresor de bus y entender por qué reduce el dominio del bombo sobre el detector.
- Combinar un compresor analógico para pegamento con un limitador para control de picos.
- Usar channel strips en buses de familia para cohesión tonal y dinámica.
- Calcular el PLR de una mezcla y relacionarlo con las referencias de género.
- Evaluar si el headroom de la mezcla es adecuado para la entrega al mastering.
- Gestionar el headroom sin bajar el Master Fader al exportar.
- Automatizar clip gain para correcciones de nivel nota por nota.
- Configurar envíos prefader para procesos paralelos que no deben verse afectados por la automatización del fader.
- Importar mezclas anteriores de un álbum como referencia activa durante la mezcla de una nueva canción.
- Reutilizar el esqueleto de sesión entre canciones de un mismo álbum.

---

## SECCIÓN 3 — SUBSECCIONES FINALES DEL EJE

El orden sigue la lógica de construcción: primero la estructura que permite la integración (buses y stems), luego el procesamiento de esa estructura (compresión de bus), luego la verificación del resultado global (rango dinámico), luego el movimiento temporal de la mezcla (automatización), y finalmente la coherencia entre canciones cuando hay más de una (álbum).

**BLOQUE A — ESTRUCTURA DE BUSES Y STEMS**

- **6-A1** · Mix bus, Master Fader y organización por familias
- **6-A2** · Procesamiento por capas y EQ de verificación en el mix bus

**BLOQUE B — COMPRESIÓN DE BUS**

- **6-B1** · Qué hace que un compresor de bus sea diferente: función y calibración
- **6-B2** · Los cuatro objetivos: control de picos, densidad, pegamento y punch
- **6-B3** · HPF en sidechain, cadena compresor + limitador y channel strips

**BLOQUE C — RANGO DINÁMICO GLOBAL**

- **6-C1** · PLR, headroom y resolución: qué medir y qué gestionar
- **6-C2** · Nivel de entrega para mastering

**BLOQUE D — AUTOMATIZACIÓN COMO COHESIÓN**

- **6-D1** · Automatización de clip gain, bypass de efectos y envíos prefader

**BLOQUE E — COHERENCIA DE ÁLBUM**

- **6-E1** · Referencia permanente entre canciones y reutilización del esqueleto de sesión

---

## SECCIÓN 4 — CURSO PRINCIPAL DEL EJE

---

### 6-A1 · MIX BUS, MASTER FADER Y ORGANIZACIÓN POR FAMILIAS

**Situación real**
El alumno tiene su mezcla con todos los canales enviando directamente al Master Fader. Quiere comprimir el mix bus, insertar un analizador y un medidor LUFS, y además poder imprimir el audio de la mezcla en un track de la sesión. Se da cuenta de que con la estructura actual no puede hacer todo eso de forma limpia sin crear conflictos de routing.

**Explicación operativa**
La separación entre el mix bus y el Master Fader es una decisión de organización que tiene consecuencias prácticas concretas.

**El Master Fader como punto de salida y análisis**
El Master Fader controla la salida física del sistema: la señal que llega al conversor D/A y a los monitores. Su función principal es la ganancia de salida. Los plugins de análisis —analizadores espectrales, medidores LUFS, medidores Peak, goniómetro— no deben estar en la cadena de procesamiento activa de la mezcla: son herramientas de lectura, no de transformación. Insertar los plugins de análisis en el Master Fader los mantiene fuera del procesamiento activo y permite leer la señal exactamente como sale al sistema de monitoreo.

**El mix bus auxiliar como punto de procesamiento**
Un canal auxiliar estéreo al que todos los submasters y familias envían su señal es el mix bus. Este canal es donde se insertan los procesadores activos: el compresor de bus, el EQ de verificación, el limitador de picos. Separarlo del Master Fader permite:
- Imprimir la mezcla en un track de audio dentro de la sesión sin depender de un bounce externo.
- Insertar hardware externo y volver con el audio ya procesado.
- Bajar el nivel del mix bus durante una sesión de escucha sin que esa atenuación quede impresa en la exportación.
- Imprimir stems (buses de familia por separado) con el mismo procesamiento que la mezcla completa.

**Organización por familias con efectos incluidos**
Cada familia instrumental tiene su propio bus: batería, bajo, guitarras, teclados, voces. Los efectos de esa familia —la reverb de la batería, el delay de las guitarras, la reverb de la voz— también envían al bus de esa familia, no a un bus de efectos global.

Esta estructura tiene una consecuencia importante: cuando se comprime el bus de la familia, la compresión reacciona a la suma de los instrumentos más sus efectos. La reverb de la caja y el cuerpo de la caja se comprimen como unidad, lo que produce cohesión dentro de la familia. Si los efectos fueran a un bus separado, esa integración se perdería.

**Procesamiento por capas**
El procesamiento de integración se construye en capas:
1. Procesamiento individual de cada instrumento (Ejes 3–5).
2. Compresión y EQ del bus de cada familia.
3. Compresión y procesamiento del mix bus completo.

Cada capa debe ser más sutil que la anterior. El mix bus no puede hacer trabajo que el procesamiento individual no resolvió: si hay un problema de balance o de dinámica en un elemento, la compresión de bus lo amplificará, no lo resolverá.

**Acción**
1. Crear un canal auxiliar estéreo (el mix bus) y dirigir todos los submasters hacia él.
2. En el Master Fader: insertar solo plugins de análisis (medidores, analizadores). Sin procesadores activos.
3. En el mix bus auxiliar: insertar el compresor de bus, el EQ de verificación y cualquier otro procesador activo.
4. Cada familia instrumental tiene su bus propio que incluye los efectos de esa familia.
5. El bus de cada familia envía al mix bus auxiliar.

**Verificación**
Reproducir la mezcla completa. Los plugins del Master Fader deben mostrar lecturas sin producir ningún cambio en el sonido al activarlos o desactivarlos (son análisis, no procesamiento). El mix bus debe ser el último punto donde el audio puede modificarse antes de llegar al Master Fader.

**Error frecuente**
Insertar procesadores activos (compresor, limitador, EQ) en el Master Fader mezclando la función de procesamiento con la de salida física. Si el Master Fader tiene un limitador activo, la exportación del bounce incluirá ese limitador. Si luego se quiere imprimir la mezcla sin el limitador, no hay forma de separarlo.

---

### 6-A2 · PROCESAMIENTO POR CAPAS Y EQ DE VERIFICACIÓN EN EL MIX BUS

**Situación real**
El alumno aplica una compresión muy agresiva en el mix bus porque "no pega" la mezcla. Con –8 dB de reducción de ganancia constante la mezcla suena más densa pero pierde la definición de los transitorios y los planos se aplastan. Sigue añadiendo procesamiento al mix bus creyendo que el problema está allí, cuando en realidad el problema está en el balance de los elementos individuales.

**Explicación operativa**
El procesamiento del mix bus actúa sobre el resultado de todo lo anterior. Si el procesamiento individual y de grupos está bien resuelto, el mix bus necesita poca intervención: la cohesión ya existe y el procesamiento del bus solo la refina.

Si el mix bus necesita compresión agresiva para que "suene bien", es una señal de que el problema no está en el bus sino en los elementos. La compresión de bus que corrige desequilibrios de balance o de dinámica de elementos individuales lo hace destruyendo algo de lo que estaba bien mientras "arregla" lo que estaba mal.

**El criterio de cantidad en las capas**
- El procesamiento individual puede ser el más intenso: la compresión de un bombo, el EQ de una voz, la reverb de un instrumento son decisiones de carácter y timbre que pueden ser pronunciadas.
- El procesamiento del bus de familia debe ser más sutil: su función es cohesionar los elementos de la familia, no redefinir el carácter de cada uno.
- El procesamiento del mix bus debe ser el más sutil de todos: su función es terminar de integrar todo el sistema con ajustes mínimos.

**EQ de verificación en el mix bus**
Antes de comprimir el mix bus es útil insertar un EQ de verificación y escuchar si el balance espectral global de la mezcla coincide con el de la referencia elegida para ese género. No se trata de ecualizar agresivamente: se trata de identificar si hay zonas del espectro que están sistemáticamente desequilibradas en la mezcla como sistema.

Una pequeña corrección de EQ en el mix bus puede resolver un desequilibrio espectral global que sería muy difícil de corregir canal por canal. Por ejemplo, si la mezcla en su conjunto tiene exceso de graves medios en la zona de 200–300 Hz, un pequeño corte en el EQ del mix bus puede resolver eso de forma más eficiente que recortar la misma zona en cada instrumento individual.

El EQ del mix bus no es el EQ de mastering. Es una verificación: se usa para corregir lo que el procesamiento individual no pudo equilibrar, no para moldear el carácter global de la mezcla. Si el EQ del mix bus necesita correcciones grandes, el problema está en el procesamiento individual.

**Acción**
1. Antes de comprimir el mix bus: insertar un EQ y comparar la mezcla con la referencia usando el analizador.
2. Identificar si hay zonas del espectro global sistemáticamente desequilibradas.
3. Si hay una corrección necesaria: hacerla con ganancia mínima (±2–3 dB como punto de partida).
4. Si el EQ del mix bus necesita correcciones grandes: devolver al procesamiento de los elementos individuales, no compensar en el bus.
5. Solo después de la verificación tonal: agregar la compresión de bus.

**Verificación**
Comparar la mezcla con la referencia en el analizador espectral después de las correcciones del EQ del mix bus. El balance espectral debe ser cercano al de la referencia. La diferencia perceptual entre la mezcla y la referencia debe deberse principalmente a decisiones artísticas (carácter de los instrumentos, tipo de producción), no a desequilibrios espectrales sistemáticos.

**Error frecuente**
Usar la compresión de bus como primera herramienta de integración antes de verificar el balance espectral y dinámico de la mezcla. Un compresor de bus que actúa sobre una mezcla con desequilibrios no resueltos puede mejorar la cohesión pero amplificará los desequilibrios existentes en la dinámica del conjunto.

---

### 6-B1 · QUÉ HACE QUE UN COMPRESOR DE BUS SEA DIFERENTE: FUNCIÓN Y CALIBRACIÓN

**Situación real**
El alumno inserta el compresor de canal que usó en el bombo —un FET rápido— en el mix bus. La mezcla pierde los transitorios de la batería y el conjunto suena aplastado aunque el ratio sea el mismo que usó en el canal del bombo. El problema no es el ratio: es que los compresores de canal y los compresores de bus están optimizados para resolver problemas diferentes.

**Explicación operativa**
Un compresor de bus recibe señales de múltiples fuentes de naturaleza muy diferente simultáneamente: los transitorios del bombo, el nivel promedio sostenido de la voz, los rebotes de las guitarras, la continuidad del bajo, los platillos. Todas esas señales llegan al detector del compresor al mismo tiempo y con distintos niveles y duraciones.

Un compresor de canal tiene que gestionar solo la dinámica de una fuente específica, relativamente homogénea. Sus parámetros pueden ajustarse a las características precisas de esa fuente.

Un compresor de bus tiene que gestionar esa señal compleja sin destruir ninguna de sus partes. Su virtud no es la velocidad ni la precisión quirúrgica: es la capacidad de amalgamar señales diversas de forma musical y estable, produciendo la sensación de que la mezcla "respira como un sistema" en lugar de ser una suma de elementos que se mueven de forma independiente.

Usar un compresor de canal muy rápido (FET, por ejemplo) directamente en el mix bus produce exactamente el problema descrito: el bombo, por ser el transitorio más fuerte, domina el detector y comprime toda la mezcla cada vez que pega, aplastando los transitorios de todos los demás instrumentos también.

**Calibración del threshold en compresores analógicos y modelados**
Los compresores analógicos históricos de bus —y sus modelados— tienen una escala de threshold que no equivale directamente a dBFS. En el hardware original, el threshold está referenciado a valores eléctricos (+4 dBu como nivel de línea estándar). Un threshold en "máximo" en el panel del compresor puede seguir reaccionando a señales que en dBFS estarían a –15 o –16 dBFS.

La referencia correcta para calibrar el threshold no es el número del panel: es el medidor de reducción de ganancia. El comportamiento del compresor debe evaluarse observando cuándo y cuánto reduce el GR, no leyendo el valor numérico del threshold como si fuera dBFS.

**Acción**
1. Al elegir el compresor de bus: priorizar uno diseñado para gestionar señales compuestas (VCA de bus, valvular) sobre uno de canal muy rápido.
2. Al calibrar el threshold: observar el GR mientras la mezcla suena. El threshold correcto es el que produce la reducción en los momentos que se quiere controlar.
3. Activar el stereo link para preservar la imagen estéreo.
4. Verificar que el compresor no aplana los transitorios percusivos de la mezcla antes de aprobar la configuración.

**Verificación**
Con el compresor activo y el bypass alternado a nivel compensado: la mezcla con el compresor activo debe sonar más cohesionada y densa sin perder los transitorios percusivos. Si los transitorios de la batería desaparecen con el compresor activo, el ataque es demasiado rápido para el contexto del mix bus.

**Error frecuente**
Interpretar la escala del threshold de un compresor analógico modelado como dBFS y calibrar en consecuencia. Si se espera que –10 en el panel equivale a –10 dBFS, el compresor puede estar completamente por encima o por debajo del nivel real del bus, no produciendo ninguna reducción o produciendo compresión constante e indeseada.

---

### 6-B2 · LOS CUATRO OBJETIVOS: CONTROL DE PICOS, DENSIDAD, PEGAMENTO Y PUNCH

**Situación real**
El alumno sabe que debe comprimir el mix bus pero no sabe qué quiere lograr con esa compresión. Prueba distintas configuraciones y el resultado varía drásticamente. No entiende por qué los mismos parámetros producen resultados tan diferentes.

**Explicación operativa**
La compresión del mix bus puede perseguir cuatro objetivos distintos, y cada uno requiere una configuración diferente. Confundir los objetivos produce resultados que no sirven para ninguno de los cuatro.

**Objetivo 1: Control de picos**
Gestionar los picos más extremos para preservar headroom sin comprimir el promedio. El compresor actúa solo en los momentos de mayor energía.

Configuración orientativa: ataque entre 1 y 3 ms, release rápido, ratio alto (≥8:1), threshold alto. Sin makeup gain. El GR solo se mueve en los picos.

El riesgo: un ataque demasiado rápido en material percusivo elimina los transitorios de la batería y reduce el impacto de la mezcla. El punto de ataque correcto para control de picos en el mix bus es más lento que el que se usaría para el mismo objetivo en un canal de batería individual.

**Objetivo 2: Densidad / trabajo sobre el promedio**
Aumentar la densidad percibida y la estabilidad de la mezcla completa, trabajando sobre el nivel promedio sostenido más que sobre los picos.

Configuración orientativa: ratio bajo (2:1), ataque muy lento, release largo (en torno a 300 ms como referencia de partida), reducción de ganancia más continua. Con makeup gain. El GR se desplaza lentamente siguiendo el promedio de la señal, sin "saltar" con cada golpe percusivo.

El release de ~300 ms tiene respaldo en la duración promedio de la sílaba hablada: es un punto de referencia que históricamente produce buen comportamiento en material vocal. No es una regla fija.

**Objetivo 3: Pegamento (glue)**
Hacer que los elementos de la mezcla se muevan dinámicamente juntos, especialmente alrededor del elemento protagonista (en la mayoría de las producciones vocales, la voz).

Configuración orientativa: ratio 2:1 o 4:1, ataque lento (~30 ms), release ~300 ms. La reducción de ganancia hace que el comportamiento dinámico del mix bus quede guiado por el elemento que tiene más presencia sostenida. Con ataque lento, los transitorios del bombo pasan sin disparar el compresor; la voz, con su dinámica sostenida, es quien gestiona la reducción.

El resultado es que cuando la voz sube, la mezcla baja levemente; cuando la voz cae, la mezcla respira. La sensación perceptual es que todo "respira junto" con el protagonista.

**Objetivo 4: Punch**
Aumentar la sensación de golpe en la mezcla completa. El compresor deja pasar el transitorio libre, comprime el cuerpo, y genera más contraste entre el ataque y el decay de cada golpe.

Configuración orientativa: ataque lento (para dejar pasar el transitorio), release rápido (para que la ganancia se recupere antes del siguiente golpe), ratio medio-alto, makeup moderado.

El punch del mix bus no rehace el punch de los instrumentos individuales: empuja levemente el carácter percusivo de la suma. Si el bombo individual no tiene punch, el mix bus no lo genera desde cero.

**Nota sobre el Criterio del Triángulo**
Los cuatro objetivos descritos son coherentes con el marco del Criterio del Triángulo (Rabinovich y Panitta, AES/CAPER 2023) aplicado al contexto del mix bus: las señales complejas del mix bus tienen características que se distribuyen entre las tres zonas del triángulo simultáneamente, y la configuración del compresor de bus determina a cuál de esas zonas se prioriza. El Criterio del Triángulo fue introducido en el Eje 4 y no se desarrolla de nuevo aquí; su aplicación al mix bus sigue el mismo principio.

**Acción**
1. Definir el objetivo del compresor de bus antes de ajustar cualquier parámetro.
2. Usar la tabla de configuración orientativa como punto de partida.
3. Verificar que el GR se comporta de acuerdo con el objetivo: activo principalmente en picos para el objetivo 1; movimiento lento y continuo para el objetivo 2; guiado por la voz para el objetivo 3; libera rápidamente entre golpes para el objetivo 4.

**Verificación**
Comparar con bypass a nivel compensado después de ajustar cada objetivo. La diferencia perceptual debe ser coherente con el objetivo: en el objetivo 3 (pegamento), la mezcla debe sonar más cohesionada; en el objetivo 4 (punch), los golpes percusivos deben sentirse más definidos. Si la diferencia perceptual no corresponde al objetivo, el compresor está produciendo otro resultado.

**Error frecuente**
Usar el mismo compresor de bus con la misma configuración para los cuatro objetivos. Los parámetros del objetivo 1 (ataque rápido, ratio alto, threshold alto) producen el efecto opuesto al objetivo 3 (pegamento): con ataque rápido, el bombo domina la reducción y la mezcla "respira" al ritmo del bombo en lugar de al ritmo de la voz.

---

### 6-B3 · HPF EN SIDECHAIN, CADENA COMPRESOR + LIMITADOR Y CHANNEL STRIPS

**Situación real**
El alumno nota que cada vez que el bombo pega, el nivel de la voz cae levemente. El compresor de bus está reaccionando principalmente al bombo, no al balance general de la mezcla. El HPF del sidechain no está activo.

**Explicación operativa**

**HPF en el sidechain del compresor de bus**
El bombo y el bajo concentran la mayor energía de la mezcla en la zona de graves. Si el detector del compresor de bus recibe la señal completa —incluidos esos graves—, el bombo domina el detector: cada golpe de bombo produce una reducción de ganancia que afecta a toda la mezcla.

Activar un filtro HPF antes del detector del compresor de bus elimina las frecuencias bajas de la señal de detección sin tocar la señal de audio que se está comprimiendo. El compresor sigue comprimiendo la señal completa, incluyendo los graves; solo ya no los usa como criterio de disparo. El detector reacciona más a los medios-agudos —donde están la voz y los elementos melódicos—, produciendo una compresión más musical y transparente.

Si el compresor de bus no tiene HPF del sidechain integrado, puede construirse con un canal auxiliar filtrado enviado al sidechain externo del compresor.

**Cadena compresor + limitador**
Un solo compresor no puede gestionar simultáneamente los picos extremos y el promedio de la mezcla con la misma musicalidad. Si se configura para picos (ataque rápido), aplana los transitorios. Si se configura para promedio (ataque lento), permite que los picos extremos pasen al bus sin control.

La combinación de un compresor musical para el objetivo de glue/densidad con un limitador digital para el control de picos extremos resuelve ambos problemas:
- El compresor analógico (o de modelado) gestiona el carácter y la cohesión con sus envolventes lentas.
- El limitador digital transparente actúa solo en los picos más extremos sin interferir con el trabajo musical del compresor.

Algunos equipos históricos integran ambas funciones en un solo dispositivo (como el Neve 2254). Sus modelados replican esa integración.

**Channel strips en buses de familia**
Un channel strip completo —filtros + EQ + compresor integrados en un solo strip— aplicado a un bus de familia aporta cohesión tonal y dinámica a esa familia a través de la coloración característica del circuito. La elección del strip (SSL, Neve, API) define el carácter sonoro de la familia completa, no solo de un elemento.

La posición del strip en la cadena de inserts del bus importa: los filtros de limpieza digital deben ir antes del strip analógico para que el strip no procese contenido (subsónicas, ruido de alta frecuencia) que se va a eliminar de todos modos. Si el strip analógico ve las subsónicas antes de que el HPF las quite, las colorea y las amplifica antes de filtrarlas.

**Acción**
1. Activar el HPF del sidechain del compresor de bus antes de cualquier otra configuración.
2. Verificar que el GR ya no "salta" principalmente con cada golpe de bombo sino que responde al balance general de la mezcla.
3. Para control simultáneo de promedio y picos: insertar el compresor analógico para glue, seguido de un limitador digital transparente con threshold por encima del nivel promedio.
4. Para buses de familia con channel strip: colocar los filtros de limpieza antes del strip, y el strip como primer procesador analógico.

**Verificación**
Con el HPF del sidechain activo: reproducir un pasaje con bombo prominente y verificar que el nivel de la voz ya no cae cuando pega el bombo. Si la voz sigue hundiéndose con el bombo, el HPF del sidechain puede no estar activo o la frecuencia de corte es demasiado baja para filtrar la energía del bombo.

**Error frecuente**
No usar el HPF del sidechain y luego intentar resolver el "respirado" excesivo de la mezcla ajustando el ataque y el release del compresor. El respirado causado por el dominio del bombo sobre el detector no se resuelve con envolventes: se resuelve con el HPF del sidechain.

---

### 6-C1 · PLR, HEADROOM Y RESOLUCIÓN: QUÉ MEDIR Y QUÉ GESTIONAR

**Situación real**
El alumno termina la mezcla. Los picos del bus están a –0,3 dBFS. El masterizador le pide que entregue con al menos –6 dBFS de headroom. El alumno baja el Master Fader 6 dB y exporta. No sabe que acaba de reducir la resolución de bits disponible de la mezcla a la mitad.

**Explicación operativa**
El nivel de la mezcla como sistema se describe con tres métricas distintas que miden cosas diferentes:

**PLR (Peak to Loudness Ratio)**
La diferencia entre el nivel de pico máximo y la sonoridad integrada (LUFS integrados). Expresa cuánto espacio dinámico tiene la mezcla como sistema: qué tan más fuerte puede ser el pico más extremo que el promedio de la señal.

PLR = Peak (dBFS) – LUFS integrados

Una mezcla con picos a –1 dBFS y LUFS integrados de –15 tiene un PLR de 14 LU. Orientaciones por género:
- Pop/rock con batería: ~13–15 LU.
- Material acústico o jazz: hasta ~18 LU.
- Música electrónica muy comprimida: PLR menor, <10 LU.

El PLR es una descripción del rango dinámico de la mezcla antes del mastering. No es un objetivo mecánico a alcanzar; es una referencia para evaluar si la mezcla tiene el rango dinámico coherente con el género y con la cantidad de compresión aplicada.

**Headroom**
El margen entre el nivel de pico máximo y 0 dBFS. Un headroom adecuado en la entrega permite que los procesadores de mastering reciban la señal en un rango donde operar con comodidad. Si la mezcla llega con picos a –0,3 dBFS, el primer procesador analógico de la cadena de mastering puede saturar antes de que el masterizador haya tenido la oportunidad de calibrar su gain staging.

El objetivo de headroom no es un número mecánico (–6 dBFS). El objetivo es que la mezcla llegue al mastering con suficiente espacio para que los procesadores de mastering operen en su rango óptimo. Una mezcla con picos a –3 dBFS y buen PLR puede ser perfectamente válida. Una mezcla con picos a –0,3 dBFS puede ser problemática no por el número sino por lo que implica para los procesadores del masterizador.

**El costo de bits de bajar el Master Fader**
Cada 6 dB de reducción de nivel cuesta 1 bit de resolución. Un archivo de 24 bits tiene un rango dinámico teórico de ~144 dB. Si se baja el Master Fader 6 dB antes de exportar, la señal se mueve al rango de 23 bits (~138 dB). La diferencia perceptual entre 24 y 23 bits es mínima, pero el principio es importante: cada vez que se reduce el nivel mediante el Master Fader antes del bounce, se está trabajando con menos escalones de cuantización disponibles que los que el formato permite.

La solución es gestionar el headroom durante el proceso de mezcla, no al final. Si la mezcla tiene sus picos demasiado cerca de 0 dBFS, hay que reducir el nivel a través del gain staging de los elementos o de los buses durante la sesión.

**Acción**
1. Al terminar la mezcla: medir el PLR con el medidor LUFS integrado.
2. Comparar el PLR con las referencias del género.
3. Verificar el headroom disponible (diferencia entre el pico máximo y 0 dBFS).
4. Si el headroom es insuficiente para la entrega: ajustar la ganancia de los clips o de los buses durante la sesión, no bajar el Master Fader al exportar.
5. El Master Fader debe quedarse en 0 dB para el bounce final.

**Verificación**
Reproducir la mezcla completa en loop y observar simultáneamente el medidor LUFS integrado y el medidor Peak. Al final del loop, el LUFS integrado muestra la sonoridad promedio del programa. El PLR = valor del Peak – valor del LUFS integrado. Si el PLR no corresponde al rango esperado para el género, evaluar si hay sobrecompresión en el mix bus o en los procesadores de canal.

**Error frecuente**
Bajar el Master Fader mecánicamente al terminar la mezcla para "dar headroom" sin considerar las consecuencias sobre la resolución. El headroom debe gestionarse durante la mezcla, no corregirse en el último paso del bounce.

---

### 6-C2 · NIVEL DE ENTREGA PARA MASTERING

**Situación real**
El alumno entrega su mezcla al masterizador. La mezcla llega con LUFS integrados de –10 y picos a –0,2 dBFS. El masterizador le informa que la señal tiene muy poco headroom y que los primeros procesadores de su cadena están saturando.

**Explicación operativa**
La mezcla que llega al mastering es el input de toda la cadena de procesamiento del masterizador. Si ese input llega con poco headroom o con un nivel promedio demasiado alto, los procesadores de mastering —especialmente los de modelado analógico— reciben más señal de la que necesitan para operar en su rango de trabajo, y la señal puede saturar antes de que el masterizador pueda hacer su trabajo.

El objetivo de nivel de entrega no es "que suene fuerte" o "que el medidor esté alto". El objetivo es que la mezcla llegue con suficiente headroom para que la cadena de mastering opere cómodamente desde su primer eslabón.

**Referencia de entrega: –20 a –23 LUFSi**
Una mezcla con LUFS integrados en el rango de –20 a –23 tiene suficiente headroom para que los procesadores analógicos del masterizador reciban la señal cerca del nivel para el que fueron calibrados (+4 dBu estándar profesional, equivalente a –20 dBFS en el estándar AES). Esa referencia no es arbitraria: es el nivel de trabajo de la mayoría de los procesadores analógicos y sus modelados.

Si los picos de la mezcla en ese rango están entre –6 y –10 dBFS, hay headroom suficiente. Si los picos rozan 0 dBFS mientras la mezcla está en –20 LUFSi, hay una mezcla de PLR muy alto (20 LU), lo que es inusual en material de producción moderna pero puede ocurrir en material acústico sin compresión.

**Ajuste de ganancia previo a la entrega**
Si la mezcla terminada tiene más nivel del adecuado para la entrega (por ejemplo, picos a –0,5 dBFS y LUFS integrados de –10), la solución es ajustar la ganancia de clip de los elementos o de los buses durante la sesión para bajar el nivel general antes de exportar, no bajar el Master Fader.

Este ajuste debe hacerse dentro de la sesión, con el audio a plena resolución, antes del bounce. El bounce siempre sale con el Master Fader en 0 dB.

**Acción**
1. Al terminar la mezcla: leer el LUFS integrado del programa completo.
2. Si los LUFS integrados están en el rango de –20 a –23: el nivel de entrega es adecuado.
3. Si están por encima (por ejemplo, –10 a –15 LUFSi): la mezcla tiene demasiado nivel medio para la entrega al mastering. Reducir ajustando la ganancia de los buses o de los clips, no el Master Fader.
4. Verificar que los picos no superen los –0,5 a –1 dBFS para dejar algo de margen.
5. Exportar con el Master Fader en 0 dB.

**Verificación**
Después del bounce: abrir el archivo exportado en el DAW y verificar que los picos máximos y los LUFS integrados están dentro del rango esperado. Si el archivo exportado tiene los picos a –6 dBFS exactos con el Master Fader en 0 dB, el headroom fue gestionado correctamente durante la sesión.

**Error frecuente**
Entregar la mezcla con LUFS integrados de –8 o –10 esperando que el masterizador "solo le suba el volumen". El mastering no es subir el volumen: es procesar la señal con herramientas que tienen puntos de trabajo específicos. Si la señal llega con demasiado nivel, el masterizador no tiene espacio para operar sin saturar o sin comprimir agresivamente desde el inicio de la cadena.

---

### 6-D1 · AUTOMATIZACIÓN DE CLIP GAIN, BYPASS DE EFECTOS Y ENVÍOS PREFADER

**Situación real**
El alumno tiene una voz con una frase donde la primera sílaba es demasiado fuerte en relación con el resto. En lugar de dibujar una línea de automatización del fader, podría ajustar directamente el nivel del clip de audio en esa sílaba con mucho más rapidez y precisión. También tiene un delay que debería estar presente solo en ciertos momentos de la canción —en el final de cada frase vocal— pero que si está siempre activo satura el espacio de la mezcla.

**Explicación operativa**
La automatización en el contexto de la integración global es una herramienta de cohesión temporal: ajusta el comportamiento de la mezcla a lo largo del tiempo para que funcione como un sistema coherente de principio a fin. No es solo corrección técnica puntual; es la herramienta que da forma narrativa a la mezcla.

**Automatización de clip gain**
La ganancia de clip se ajusta directamente sobre el audio, segmento a segmento o nota por nota, antes de que la señal llegue a los procesadores del canal. Para correcciones pequeñas de nivel en puntos específicos del material —una sílaba demasiado fuerte, una nota de guitarra que sobresale, un par de palabras que quedan enterradas—, ajustar la ganancia del clip es más eficiente y más preciso que dibujar curvas de fader.

La ventaja: el clip gain no dibuja curvas suaves sobre el fader que pueden interactuar con la automatización del fader de formas complejas. Opera directamente sobre el audio antes del procesamiento del canal. El compresor del canal recibe la señal ya ajustada, lo que puede producir resultados más consistentes que comprimir una señal con picos variables.

**Automatización de bypass de efectos**
Activar y desactivar efectos en momentos específicos de la canción es una herramienta de integración espacial y temporal. Un delay en la voz que solo aparece al final de cada frase —y no durante la frase— crea espacialidad sin saturar la mezcla permanentemente. El delay existe en el espacio de la canción pero no compite con la claridad de la voz durante la interpretación.

La técnica: automatizar el bypass del efecto para que se active solo en los momentos donde contribuye y se desactive en los demás.

**Prefader vs postfader para procesos paralelos**
Los envíos a efectos paralelos (compresión paralela, efectos en send) pueden ser postfader o prefader:

- **Postfader:** el nivel del envío al efecto varía con el fader del canal. Si se automatiza el fader de la voz, el nivel que llega a la reverb de la voz también cambia. Para efectos de ambiencia (reverb, delay), este comportamiento es habitualmente el correcto: la reverb debe moverse junto con el instrumento.

- **Prefader:** el nivel del envío al efecto no varía con el fader del canal. Si se automatiza el fader de la voz, la reverb sigue recibiendo la misma señal. Para procesos paralelos donde el procesamiento debe ser independiente del movimiento del fader —compresión paralela, efectos con nivel estable independientemente de la dinámica del canal—, el envío debe ser prefader.

Error habitual: configurar el envío de compresión paralela como postfader. Al automatizar el fader del canal para bajar un instrumento en ciertos momentos, el nivel de la rama comprimida también baja, y la compresión paralela pierde su función.

**Acción**
1. Para correcciones de nivel nota por nota: usar clip gain, no automatización del fader.
2. Para efectos que deben aparecer en momentos específicos: automatizar el bypass del plugin.
3. Para efectos de ambiencia: envíos postfader.
4. Para compresión paralela y procesos que deben mantenerse independientes del fader: envíos prefader.
5. Verificar la configuración de prefader/postfader de cada envío antes de automatizar.

**Verificación**
Al automatizar el fader de un canal: reproducir la sección y verificar cómo reaccionan los efectos del canal. Si la reverb del instrumento sube y baja con el fader como se espera: envío postfader correcto. Si el nivel de la compresión paralela también cambia cuando se automatiza el fader: el envío no está en prefader y debe corregirse.

**Error frecuente**
Usar la automatización del fader para correcciones pequeñas de nivel que deberían resolverse con clip gain. Las líneas de automatización del fader se dibujan sobre la señal después del procesamiento del canal. Para correcciones de nivel que necesitan afectar el comportamiento del compresor o del EQ (porque la señal llega diferente al canal), la corrección correcta es en el clip gain antes del procesamiento.

---

### 6-E1 · REFERENCIA PERMANENTE ENTRE CANCIONES Y REUTILIZACIÓN DEL ESQUELETO DE SESIÓN

**Situación real**
El alumno termina de mezclar tres canciones de un EP. Cada canción suena bien individualmente. Al escucharlas en secuencia, la primera tiene graves muy presentes, la segunda tiene la voz muy adelante y brillante, y la tercera tiene la batería prominente y los graves moderados. Suenan como tres discos diferentes mezclados por tres personas distintas. El problema no está en ninguna canción: está en que se mezclaron de forma aislada sin referencia cruzada.

**Explicación operativa**
Mezclar un álbum requiere más que hacer que cada canción suene bien por separado. Requiere que el conjunto suene como una obra coherente con identidad propia. Esa coherencia no surge automáticamente de mezclar bien cada canción: requiere una práctica activa de referencia cruzada durante el proceso.

**Referencia permanente durante la mezcla del álbum**
Al comenzar a mezclar la segunda canción de un álbum, importar el audio estéreo de la primera canción ya mezclada a la sesión como referencia activa. Al mezclar la tercera, importar las dos anteriores. El objetivo es tener siempre el contexto del álbum disponible en la misma sesión para comparar directamente.

La comparación no se hace escuchando el álbum completo de principio a fin: se compara sección a sección con el mismo tipo de material. El estribillo de la canción en curso se compara con el estribillo de las anteriores; la estrofa con la estrofa. Si el estribillo de la canción 3 tiene más energía que el de las canciones 1 y 2, hay una decisión a tomar: es una diferencia intencional que forma parte del carácter individual de esa canción, o es un desequilibrio que hay que corregir.

La coherencia de álbum no significa que todas las canciones suenen igual. Significa que comparten una identidad reconocible que las hace pertenecer al mismo disco.

**Reutilización del esqueleto de sesión**
La arquitectura de la sesión —el routing, los buses de familia, los grupos, el procesamiento base del mix bus— puede y debe reutilizarse entre canciones usando la función de importación de datos de sesión del DAW. Al importar la arquitectura de la sesión de la primera canción a la segunda, se obtiene:
- Los mismos buses de familia con los mismos nombres.
- La misma estructura de routing.
- Los mismos plugins instalados en los mismos puntos de la cadena.

Los parámetros de cada plugin pueden ajustarse para la nueva canción; la arquitectura base es consistente. Esa consistencia estructural contribuye a la coherencia del álbum incluso antes de que empiece el ajuste creativo de cada canción.

**Acción**
1. Al comenzar la segunda canción del álbum: importar el audio estéreo de la primera como track de referencia en la sesión.
2. Al comparar: hacerlo sección a sección (estrofa con estrofa, estribillo con estribillo) con solos.
3. Documentar las diferencias identificadas: cuáles son intencionales y cuáles son desequilibrios.
4. Para la estructura de sesión: usar la función de importación de datos de sesión del DAW para replicar el routing y los buses de la primera canción.
5. Ajustar los parámetros de cada plugin para la nueva canción desde la base compartida.

**Verificación**
Al terminar cada canción del álbum: escuchar las tres o cuatro últimas canciones en secuencia sin correcciones. Si la transición entre canciones produce un cambio pronunciado en la percepción del balance espectral, del nivel de la voz o de la energía de la batería, hay un desequilibrio de coherencia que hay que corregir antes de entregar al mastering.

**Error frecuente**
Mezclar cada canción del álbum de forma completamente aislada y esperar que el mastering uniformice el conjunto. El mastering puede ajustar el nivel entre canciones y hacer pequeñas correcciones espectrales, pero no puede transformar tres mezclas que suenan como discos diferentes en un álbum coherente. La coherencia debe construirse durante la mezcla, no delegarse al mastering.

---

## SECCIÓN 5 — DOSSIER CANÓNICO DE APOYO

---

### ESTRUCTURA DE BUSES Y STEMS

**Separación mix bus / Master Fader**

| Punto | Función | Qué va ahí |
|---|---|---|
| Master Fader | Salida física y análisis | Plugins de análisis exclusivamente (medidores, analizadores) |
| Mix bus auxiliar | Procesamiento activo | Compresor de bus, EQ, limitador |
| Buses de familia | Integración por grupo | Compresor de grupo, EQ de familia, efectos de la familia |

**Principio de capas**
Cada capa de procesamiento debe ser más sutil que la anterior. La compresión del mix bus no corrige lo que el procesamiento individual no resolvió: lo amplifica.

---

### COMPRESIÓN DE BUS

**Cuatro objetivos diferenciados**

| Objetivo | Ataque | Release | Ratio | Makeup | GR se mueve |
|---|---|---|---|---|---|
| Control de picos | 1–3 ms | Rápido | ≥8:1 | No | Solo en picos extremos |
| Densidad / RMS | Muy lento | ~300 ms | 2:1 | Sí | Lentamente, siguiendo el promedio |
| Pegamento (glue) | ~30 ms | ~300 ms | 2:1 o 4:1 | Sí | Guiado por el protagonista (voz) |
| Punch | Lento | Rápido | Medio-alto | Moderado | Libera rápidamente entre golpes |

**HPF en sidechain del compresor de bus**
Activa el filtro del detector para eliminar las frecuencias graves de la señal de detección. El compresor sigue procesando la señal completa; solo deja de usar los graves como criterio de disparo.

**Cadena compresor + limitador**
Compresor analógico (o modelado): gestiona el carácter y la cohesión con envolventes lentas.
Limitador digital transparente: controla picos extremos sin interferir con el trabajo del compresor.

**Calibración del threshold en analógicos y modelados**
La escala del threshold no es dBFS. Calibrar con el medidor de GR observando cuándo y cuánto reduce.

---

### RANGO DINÁMICO GLOBAL

**PLR (Peak to Loudness Ratio)**
PLR = Peak (dBFS) – LUFS integrados.

| Género | PLR orientativo |
|---|---|
| Pop/rock con batería | ~13–15 LU |
| Material acústico / jazz | Hasta ~18 LU |
| Electrónica densa | <10 LU |

**Headroom y resolución**
- 6 dB de reducción = 1 bit de resolución.
- Gestionar el headroom durante la mezcla, no bajando el Master Fader al exportar.
- Nivel de entrega al mastering: ~–20 a –23 LUFSi.
- Master Fader en 0 dB para el bounce final.

---

### AUTOMATIZACIÓN COMO COHESIÓN

**Clip gain vs automatización de fader**

| Herramienta | Cuándo usarla | Por qué |
|---|---|---|
| Clip gain | Correcciones de nivel nota por nota o segmento a segmento | Opera antes del procesamiento; afecta cómo recibe la señal el compresor |
| Automatización de fader | Movimientos de nivel de mayor duración en la mezcla | Opera después del procesamiento del canal |

**Envíos prefader vs postfader**

| Tipo de envío | Comportamiento con la automatización del fader | Cuándo usarlo |
|---|---|---|
| Postfader | El envío al efecto varía con el fader | Efectos de ambiencia (reverb, delay): el efecto sigue al instrumento |
| Prefader | El envío al efecto es independiente del fader | Compresión paralela y procesos que deben mantenerse estables |

---

## SECCIÓN 6 — REGLAS PARA RAG

### Qué indexar

- Separación mix bus / Master Fader: función de cada punto.
- Organización por familias con efectos incluidos: por qué y cómo.
- Principio de capas: cantidad de procesamiento por nivel en la jerarquía.
- Función diferencial del compresor de bus vs compresor de canal.
- Calibración del threshold en analógicos: GR como referencia, no el número del panel.
- HPF en sidechain del compresor de bus: función y criterio de uso.
- Tabla de cuatro objetivos de bus compression con configuración orientativa.
- Cadena compresor + limitador en el mix bus.
- Channel strips en buses de familia: posición en la cadena.
- PLR: definición, fórmula y referencias orientativas por género.
- Headroom: criterio de gestión durante la mezcla vs al exportar.
- Relación 6 dB / 1 bit: justificación de no bajar el Master Fader.
- Nivel de entrega para mastering: –20 a –23 LUFSi.
- Clip gain vs automatización de fader: criterio de uso.
- Prefader vs postfader: tabla de criterios.
- Automatización de bypass de efectos: función en la integración temporal.
- Referencia permanente entre canciones del álbum: método operativo.
- Reutilización del esqueleto de sesión entre canciones del álbum.

### Qué no indexar

- Mecánica del compresor (parámetros, circuitos, tipos de detector): pertenece a Eje 4.
- EQ de mastering sobre el programa completo: pertenece a Eje 7.
- Limitadores y clippers en masterización: pertenece a Eje 7.
- Formulaciones orales del autor fuente (bloqueadas).
- Analogías arquitectónicas del docente fuente.

### Etiquetado por eje
`eje:6` para todo el contenido de esta unidad.

### Etiquetado por bloque interno
`bloque:6A` — estructura de buses y stems.
`bloque:6B` — compresión de bus.
`bloque:6C` — rango dinámico global.
`bloque:6D` — automatización.
`bloque:6E` — coherencia de álbum.

### Etiquetado por fase LDOV
- Lectura del estado global (PLR, LUFS, imagen en el goniómetro): `LDOV:Leer`.
- Decisión de configuración del compresor de bus, nivel de entrega, estructura de álbum: `LDOV:Decidir`.
- Configuración del mix bus, automatización, exportación: `LDOV:Operar`.
- Verificación en contexto completo, comparación con referencia, escucha del álbum en secuencia: `LDOV:Verificar`.

### Teoría mínima vs ampliación opcional

**Teoría mínima obligatoria (prioridad alta):**
- Separación mix bus / Master Fader: función y estructura.
- Principio de capas: cantidad por nivel.
- HPF en sidechain del compresor de bus.
- Tabla de cuatro objetivos de bus compression.
- PLR: definición y referencias orientativas.
- Relación 6 dB / 1 bit.
- Nivel de entrega: –20 a –23 LUFSi.
- Clip gain vs fader: criterio de uso.
- Prefader vs postfader: tabla.

**Teoría de precisión útil (prioridad media):**
- Calibración del threshold en analógicos: diferencia con dBFS.
- Cadena compresor + limitador: función de cada etapa.
- Channel strips en buses de familia: posición y criterio.
- Automatización de bypass de efectos: función temporal.
- Método de referencia permanente en álbum.

**Teoría profunda opcional (IA/FAQ/anexo):**
- Comparativa de compresores de bus históricos: SSL, Neve, API.
- Fundamento estadístico del release de ~300 ms.
- Diferencias entre distintos algoritmos de limitación para el mix bus.
- Técnicas avanzadas de automatización como expresión.

---

## SECCIÓN 7 — REGLAS PARA GUIONES

### Partes que deben ser demostración

- **Separación mix bus / Master Fader:** mostrar en pantalla la estructura de routing con el mix bus auxiliar y el Master Fader como punto de análisis.
- **Cuatro objetivos del compresor de bus:** demostración con el mismo compresor configurado para cada objetivo en secuencia, escuchando la diferencia de comportamiento del GR y el impacto en la mezcla.
- **HPF en sidechain activo vs desactivado:** reproducir un pasaje con bombo prominente y mostrar cómo el GR deja de "saltar" con el bombo al activar el HPF del sidechain.
- **Clip gain vs automatización de fader:** mostrar las dos herramientas sobre la misma corrección y comparar la eficiencia y el resultado.
- **PLR en tiempo real:** mostrar el medidor LUFS integrado y el Peak en la mezcla completa. Calcular el PLR y compararlo con la referencia del género.
- **Headroom y el Master Fader:** demostración de por qué bajar el Master Fader 6 dB antes del bounce es diferente a gestionar el headroom durante la mezcla.

### Partes que pueden ser explicación a cámara

- Principio de capas (procesamiento por nivel de bus): concepto con diagrama.
- Relación 6 dB / 1 bit: explicación técnica con gráfico de escala de bits.
- Prefader vs postfader: descripción con diagrama de señal.
- Método de referencia permanente en álbum: descripción del flujo operativo.

### Partes que conviene enseñar con sesión real

- Configuración completa del mix bus desde cero: routing, EQ de verificación, compresor de bus, limitador.
- Mezcla de dos canciones del mismo álbum con referencia cruzada activa.
- Preparación del bounce final: verificación de PLR, headroom, exportación con Master Fader en 0 dB.

### Partes que conviene mandar a la capa de apoyo

- Comparativa técnica extendida de compresores de bus históricos.
- Fundamento estadístico del release de ~300 ms.
- Técnicas avanzadas de automatización como herramienta expresiva.
- Diferencias técnicas entre algoritmos de limitación para el mix bus.

---

## SECCIÓN 8 — CAPA DE APOYO POR IA

### Temas que conviene dejar listos para profundización vía IA

- Comparativa de compresores de bus históricos: SSL G Bus Compressor, Neve 2254, API 2500, Manley Variable Mu en el contexto del mix bus.
- Fundamento estadístico del release de ~300 ms: origen de la referencia en la duración de la sílaba hablada.
- Automatización expresiva avanzada: riding del fader como herramienta de interpretación de la mezcla.
- Diferencias entre algoritmos de limitación transparente para el mix bus vs limitadores con carácter.
- Técnicas de exportación y bounce por instrumento: stems vs mezcla completa.
- Gestión del headroom en cadenas con hardware externo en el mix bus.

### Ejemplos de preguntas que el alumno podría hacerle a la IA

- "¿Cuál es la diferencia entre comprimir el mix bus con un SSL G Bus Compressor y con un Neve 2254?"
- "¿Por qué el release de 300 ms se usa como referencia para el glue del mix bus? ¿Tiene fundamento técnico o es una convención?"
- "¿Cómo exporto los stems de mi mezcla manteniendo el procesamiento del mix bus en cada uno?"
- "Explícame la diferencia entre usar clip gain y la automatización del fader para corregir una sílaba demasiado fuerte en una voz."
- "¿Cuándo conviene usar un limitador transparente en el mix bus en lugar del compresor para el control de picos?"
- "¿Cómo importo los datos de sesión de una canción a otra en [mi DAW] para reutilizar el esqueleto de la sesión?"
- "Mi PLR es de 8 LU en una mezcla de pop/rock. ¿Qué implica eso y qué puedo ajustar?"
- "¿Qué pasa con la resolución de la mezcla si exporto bajando el Master Fader 3 dB en lugar de 6?"

---

## SECCIÓN 9 — BLOQUES QUE REQUIEREN ATRIBUCIÓN EXPLÍCITA

### Release de ~300 ms como referencia para glue
Este dato —la duración promedio de la sílaba hablada como fundamento del release de ~300 ms para glue vocal— aparece en las fuentes como observación del autor fuente. El dato estadístico es de dominio general; la formulación específica como criterio operativo proviene de Rabinovich. Se presenta en el curso como referencia de partida sin citar textualmente la formulación del autor fuente.

### Nivel de entrega –20 a –23 LUFSi
Esta recomendación operativa específica aparece en el PDF de Mastering 2022 del autor fuente. El principio técnico subyacente (headroom para procesadores de mastering y compatibilidad con el estándar AES) es de dominio general. Se presenta en el curso reformulada desde el principio técnico.

### Criterio del Triángulo aplicado al mix bus
Si se menciona el Criterio del Triángulo en el contexto del mix bus, la atribución a Pablo Rabinovich y Pablo Panitta (AES/CAPER 2023) ya está establecida desde el Eje 4. No requiere nuevo desarrollo ni nueva atribución; solo una referencia al marco ya introducido.

### Método de referencia permanente en álbum
La práctica de importar las mezclas anteriores como referencia activa mientras se trabaja la siguiente canción aparece en las fuentes como práctica del autor fuente. El principio de trabajar con referencias es de dominio general del campo. La formulación presentada en este eje está reformulada sin reproducir la formulación oral ni los ejemplos anecdóticos del docente fuente.

### Modelos de hardware
Los modelos de compresores de bus mencionados en el dossier (SSL G Bus Compressor, Neve 2254, API 2500, Manley Variable Mu) llevan atribución a sus fabricantes: Solid State Logic, AMS Neve, API Technologies, Manley Laboratories.

---

## SECCIÓN 10 — CONTINUIDAD CON OTROS EJES

**De dónde viene este eje**
El Eje 6 viene de los **Ejes 3, 4 y 5** en conjunto.

El Eje 6 no opera sobre un solo aspecto de la señal: opera sobre el resultado integrado de todo lo anterior. El carácter tonal (Eje 3), la energía dinámica (Eje 4) y la posición espacial (Eje 5) de cada elemento están ya definidos cuando el Eje 6 interviene. La función del Eje 6 es hacer que ese conjunto funcione como sistema.

Cruce con Eje 4: la mecánica del compresor (parámetros, circuitos, Criterio del Triángulo) se conoce del Eje 4. El Eje 6 no la repite; la aplica al contexto específico del bus con sus objetivos propios.

Cruce con Eje 1: los instrumentos de medición del Eje 1 (LUFS, Peak, goniómetro, correlatómetro) son las herramientas de lectura del Eje 6. El PLR se calcula con el medidor LUFS integrado; el headroom se verifica con el medidor Peak; la imagen se monitorea con el goniómetro.

**A qué eje prepara**
El Eje 6 prepara directamente al **Eje 7 — Masterización**.

La mezcla que entrega el Eje 6 es el input de toda la cadena de mastering. El nivel de entrega (–20 a –23 LUFSi), el PLR coherente con el género, el headroom preservado y la coherencia del álbum son condiciones que el Eje 6 establece para que el Eje 7 pueda operar correctamente.

El Eje 7 recibe lo que el Eje 6 entregó. Si la mezcla llega con desequilibrios espectrales, poco headroom o LUFS integrados muy altos, el masterizador los encontrará en el input de su cadena. El mastering puede hacer ajustes, pero no puede reconstruir lo que la mezcla no construyó. La responsabilidad de la calidad de la entrega pertenece al Eje 6.

---

*KENTH Academy — Eje 6 · Versión de producción v1.0*
*Generado desde arquitectura congelada v1.0-final y paquete limpio Eje 6.*
