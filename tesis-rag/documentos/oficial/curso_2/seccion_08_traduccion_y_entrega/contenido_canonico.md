---
course_id: "2"
moodle_section_id: "17"
section_id: "17"
section_number: "8"
section_slug: "traduccion_y_entrega"
section_title: "SECCIÓN 7: Traducción y entrega"
resource_type: "lesson_content"
content_type: "markdown"
layer: "canonical"
scope: "section"
source: "canonical_md"
source_origin: "course"
status: "ready_for_indexing"
visible_to_student: "true"
allowed_for_indexing: "true"
version: "v1"
legacy_axis: "Eje 7"  # solo trazabilidad de migración; NO usar como fuente
---

# EJE 7 — TRADUCCIÓN Y ENTREGA
### KENTH Academy · Mezcla y Masterización · Contenido Final de Curso

---

## SECCIÓN 1 — FUNCIÓN PRÁCTICA DEL EJE

El Eje 7 es la preparación del programa fonográfico para su distribución. Es la última instancia del proceso y el único punto donde todo procesamiento actúa simultáneamente sobre todos los elementos de la mezcla sin excepción.

No arregla mezclas. Traduce lo que hay al formato y nivel en que debe existir en el mundo. Esa distinción no es secundaria: define qué puede y qué no puede hacerse aquí.

El Eje 6 entregó la mezcla. El Eje 7 la recibe y la procesa como un sistema terminado. Cualquier problema que venga de un elemento específico —el bajo de un instrumento en particular, la reverb de una voz puntual— no puede resolverse aquí sin afectar también a todos los demás elementos que compartan esa zona frecuencial o dinámica.

El eje tiene nueve dominios:

**Definición y etapas:** qué es el mastering como proceso y en qué orden se construye.

**Preparación y reparación:** las operaciones que deben completarse antes de entrar en la cadena de procesamiento — ajuste del nivel de entrada, corrección de DC offset y asimetría de forma de onda.

**Diagnóstico y corrección espectral:** análisis del programa completo y las correcciones de carácter general: subsónicas, resonancias, balance entre canales.

**Compresión en mastering:** cómo comprimir en este contexto, con qué objetivos y en qué orden.

**Imagen estéreo y MS:** ajuste de la imagen del programa completo con procesamiento Mid/Side.

**Limitación y True Peak:** la etapa comercial que lleva el material al nivel de distribución con control de los picos de reconstrucción.

**Targets de plataformas:** qué es la normalización de las plataformas, qué implica para el master y cómo elegir el objetivo de loudness.

**Dithering y entrega digital:** la conversión final de bits y la verificación del archivo de entrega.

**Mastering de álbum:** cuando el material no es un single sino un conjunto, las decisiones cambian de escala.

---

## SECCIÓN 2 — QUÉ DEBE PODER HACER EL ALUMNO AL TERMINAR ESTE EJE

Al completar el Eje 7, el alumno es capaz de:

- Distinguir entre un problema que pertenece al mastering y uno que pertenece a la mezcla.
- Identificar las tres etapas del mastering y aplicarlas en el orden correcto.
- Realizar el trimming de nivel de entrada a la cadena antes de insertar el primer procesador.
- Detectar y corregir DC offset y asimetría de forma de onda con las herramientas adecuadas a cada caso.
- Diagnosticar el programa completo (nivel, fase, espectro) antes de procesar.
- Aplicar un HPF subsónico con criterio: solo cuando el análisis muestra energía problemática por debajo del fundamento.
- Corregir resonancias de carácter general con EQ paramétrico o dinámico, y aplicar el procesamiento en modo MS cuando el problema está localizado en Mid o Side.
- Corregir un desequilibrio de nivel entre canales con herramientas de mono maker.
- Aplicar compresión en serie con tarea diferenciada por etapa.
- Usar compresión paralela o ascendente como alternativa o complemento a la compresión descendente.
- Aplicar saturación en mastering verificando que no es perceptible como distorsión.
- Configurar el procesamiento M/S sobre el programa completo para corrección espectral o ajuste de imagen.
- Configurar un limitador de mastering con threshold y Out Ceiling, comprendiendo la relación entre ambos.
- Usar el método delta para verificar el daño introducido por el limitador.
- Medir el True Peak del programa y del archivo codificado.
- Aplicar dither correctamente: solo cuando hay reducción de profundidad de bits, una sola vez, en la conversión final.
- Interpretar los targets de LUFS de las plataformas y adaptar el objetivo del master al género.
- Masterizar un álbum con referencia cruzada activa y criterio de nivelación intencional entre canciones.

---

## SECCIÓN 3 — SUBSECCIONES FINALES DEL EJE

El orden sigue la secuencia real del proceso de mastering: orientación conceptual → preparación técnica previa → diagnóstico y corrección → procesamiento de carácter → imagen → etapa comercial → entrega digital → contexto de álbum. Cada subsección es un paso del flujo de trabajo, no solo un tema aislado.

**BLOQUE A — DEFINICIÓN Y ETAPAS**

- **7-A1** · El mastering: función, alcance y tres etapas

**BLOQUE B — PREPARACIÓN**

- **7-B1** · Trimming, DC offset y asimetría de forma de onda

**BLOQUE C — DIAGNÓSTICO Y CORRECCIÓN ESPECTRAL**

- **7-C1** · Análisis del programa y correcciones de carácter general

**BLOQUE D — COMPRESIÓN Y SATURACIÓN**

- **7-D1** · Compresión en mastering: en serie, paralela y ascendente
- **7-D2** · Saturación: carácter sin distorsión

**BLOQUE E — IMAGEN ESTÉREO Y MS**

- **7-E1** · Mid/Side y ajuste de imagen sobre el programa completo

**BLOQUE F — LIMITACIÓN Y TRUE PEAK**

- **7-F1** · Limitador de mastering, método delta y True Peak

**BLOQUE G — TARGETS Y OPTIMIZACIÓN**

- **7-G1** · Normalización de plataformas, LUFS objetivo y criterio por género

**BLOQUE H — DITHERING Y ENTREGA DIGITAL**

- **7-H1** · Dithering, noise shaping, resampleo y entrega del archivo final

**BLOQUE I — MASTERING DE ÁLBUM**

- **7-I1** · Coherencia, nivelación y referencia cruzada en el álbum

---

## SECCIÓN 4 — CURSO PRINCIPAL DEL EJE

---

### 7-A1 · EL MASTERING: FUNCIÓN, ALCANCE Y TRES ETAPAS

**Situación real**
El alumno recibe una mezcla para masterizar. El bajo de una guitarra específica suena excesivo en ciertos compases. Intenta corregirlo con EQ en el master. Al hacerlo, el bajo de todos los demás instrumentos también cambia. La corrección empeoró el balance en lugar de mejorarlo.

**Explicación operativa**
El mastering es la preparación de un programa fonográfico para su distribución. Su alcance es siempre global: cualquier procesamiento actúa sobre el conjunto, no sobre un elemento individual. Esta limitación define el tipo de problemas que el mastering puede resolver y los que no puede.

La distinción operativa fundamental: si el problema viene de un elemento específico de la mezcla (el bajo de una guitarra, la reverb de una voz, el ataque de un bombo), ese problema pertenece a la mezcla y no puede resolverse en mastering sin afectar a los demás elementos. Si el problema es de carácter general del programa (los graves de la canción completa son excesivos, hay una resonancia que aparece en toda la mezcla, el nivel promedio es insuficiente para el destino), ese sí es un problema de mastering.

El mastering no termina una mezcla. Traduce lo que hay.

**Las tres etapas**
El proceso de mastering se divide en tres etapas que tienen un orden necesario:

**Etapa técnica**
Corregir los problemas formales de la señal antes de cualquier otro procesamiento: DC offset, asimetría de forma de onda, energía subsónica problemática, resonancias de carácter general, desbalance entre canales, problemas de fase. Si estos problemas existen y no se corrigen primero, la etapa comercial los amplificará.

**Etapa comercial**
Llevar el programa al nivel de sonoridad adecuado para el destino de distribución. Es la etapa donde se aplica la compresión de carácter, la limitación y se alcanza el objetivo de LUFS integrados del master. No puede realizarse correctamente si la etapa técnica no está resuelta.

**Etapa artística** *(optativa)*
Añadir carácter, color o modificaciones tímbricas y dinámicas deliberadas que van más allá de corregir problemas. Puede ser mínima o innecesaria si la mezcla llegó bien terminada. No toda mezcla necesita una intervención artística en mastering: si el material ya tiene el carácter que busca, forzar procesamiento artístico puede quitarle algo que funcionaba.

El orden importa. No se puede optimizar el nivel de un programa que tiene DC offset sin amplificar ese problema. No se puede añadir carácter artístico a un programa que tiene resonancias sin magnificarlas.

**Acción**
1. Al recibir la mezcla: antes de abrir la cadena de procesamiento, diagnosticar si hay problemas técnicos que deben resolverse primero.
2. Solo después del diagnóstico técnico: planificar la etapa comercial.
3. Evaluar si la mezcla necesita intervención artística o si el material ya tiene el carácter adecuado.

**Verificación**
Si al finalizar el mastering hay elementos individuales del programa que suenan mal pero la mezcla completa está bien balanceada, el problema estaba en la mezcla y debería volver al mixdown. El mastering no lo puede resolver sin afectar lo que estaba bien.

**Error frecuente**
Aplicar procesamiento artístico antes de resolver la etapa técnica. Un saturador aplicado sobre un programa con DC offset amplifica el desplazamiento. Un limitador aplicado sobre un programa con resonancias hace que esas resonancias dominen el disparo del limitador.

---

### 7-B1 · TRIMMING, DC OFFSET Y ASIMETRÍA DE FORMA DE ONDA

**Situación real**
El alumno abre la mezcla en el master. Los picos están a –0,5 dBFS y los LUFS integrados están a –10. El primer procesador de la cadena es un compresor valvular calibrado para operar a +4 dBu (–20 dBFS). La mezcla entra al compresor 10 dB por encima del nivel para el que fue diseñado. El compresor no suena bien —satura antes de comprimir musicalmente— pero el alumno no sabe por qué.

**Explicación operativa**

**Trimming**
Antes de entrar en la cadena de procesamiento, el nivel de la mezcla debe ajustarse para que los procesadores reciban la señal dentro de su rango óptimo de trabajo. Este ajuste se hace con el clip gain o trim del archivo, no con el fader de la sesión.

El objetivo: si la cadena incluye procesadores de modelado analógico calibrados a estándar AES (–20 dBFS = 0 VU = +4 dBu), la mezcla debe llegar a ~–20 a –23 LUFSi antes del primer procesador. Si los picos superan significativamente ese nivel, hay que reducir la ganancia de clip antes de continuar.

Este es el punto de partida que el Eje 6 estableció: la mezcla debe llegar al mastering ya en ese rango. Si no llegó así, el trimming es la primera operación del Eje 7.

**DC offset**
El DC offset es una componente de corriente continua que desplaza toda la forma de onda de la señal fuera de su posición de reposo centrada en cero. En la práctica, esto significa que la forma de onda no cruza el eje de cero de forma simétrica: toda la señal está desplazada hacia el semiciclo positivo o negativo.

Consecuencias del DC offset:
- Clipping asimétrico: se llega al techo digital antes en el semiciclo donde está el desplazamiento.
- Carga térmica innecesaria en los transductores.
- Respuesta desigual de los procesadores dinámicos: el compresor "ve" un nivel diferente en cada semiciclo.

Diagnóstico: las estadísticas del archivo de audio (en la mayoría de los DAWs) muestran el porcentaje de DC offset. Si el valor es insignificante (≤ 0,0xx%), no hay problema. Si alcanza valores enteros o claramente significativos (~1% o más), corregir.

Corrección: un HPF con frecuencia de corte muy baja (5–10 Hz) elimina la componente continua sin afectar el audio útil. Algunas herramientas de edición (como iZotope RX) tienen una función específica de corrección de DC offset.

**Asimetría de forma de onda**
La asimetría es un fenómeno diferente al DC offset. La señal asimétrica está correctamente centrada en cero (no hay desplazamiento) pero sus picos tienden más hacia el semiciclo positivo o negativo. La causa es la relación de fase entre los componentes frecuenciales de la señal: la suma de todas las frecuencias con sus fases específicas produce una distribución asimétrica de picos.

Consecuencia: si se quiere subir el nivel del programa, se llega antes al techo del lado más cargado, reduciendo el headroom útil antes de lo esperado.

Corrección: un filtro AllPass que rota la fase de ciertas frecuencias y sus adyacentes, redistribuyendo la suma de picos sin modificar la amplitud de ninguna componente. El AllPass no elimina energía ni modifica el espectro: solo cambia las relaciones de fase entre frecuencias, lo que modifica cómo se suman los picos.

**La distinción crítica**
DC offset y asimetría son fenómenos distintos con correcciones distintas:
- DC offset: toda la forma de onda está desplazada → HPF o herramienta de corrección de offset.
- Asimetría: la forma de onda está centrada pero los picos no son simétricos → AllPass.

Si hay ambos problemas: corregir primero el DC offset (HPF) y luego la asimetría (AllPass). El AllPass no puede eliminar una componente de corriente continua.

**Acción**
1. Abrir el archivo de mezcla y verificar las estadísticas: nivel de DC offset, LUFS integrados, Peak.
2. Si los LUFS integrados no están en el rango –20 a –23 LUFSi: ajustar con clip gain.
3. Si hay DC offset significativo: aplicar HPF a 5–10 Hz o herramienta específica.
4. Si hay asimetría visible en el osciloscopio o los picos son claramente desiguales entre semiciclos: aplicar AllPass en la frecuencia donde la asimetría es más pronunciada.
5. Verificar el resultado de cada corrección antes de continuar.

**Verificación**
Después del trimming: leer los LUFS integrados con el medidor. Deben estar en el rango objetivo. Después de la corrección de DC offset: las estadísticas del archivo deben mostrar un valor de offset despreciable. Después de la corrección de asimetría: el osciloscopio debe mostrar picos más equilibrados entre semiciclos.

**Error frecuente**
Confundir asimetría con DC offset y aplicar un HPF a 5 Hz cuando el problema requiere AllPass. El HPF elimina la componente continua (DC offset) pero no redistribuye los picos asimétricos; la asimetría permanece. Aplicar AllPass cuando el problema es DC offset: el AllPass modifica las relaciones de fase pero no elimina la corriente continua.

---

### 7-C1 · ANÁLISIS DEL PROGRAMA Y CORRECCIONES DE CARÁCTER GENERAL

**Situación real**
El alumno tiene el programa preparado (trimming correcto, sin DC offset, sin asimetría). Antes de procesar, necesita saber qué tiene. Inserta el EQ sin mirar el analizador y comienza a hacer correcciones "a oído". Después de varios ajustes nota que la mezcla tiene un problema de subsónicas que ninguna de sus correcciones tocó, porque no lo diagnosticó antes de intervenir.

**Explicación operativa**
El diagnóstico en mastering sigue la misma lógica que en el Eje 1: nivel, fase, espectro. La diferencia es que aquí el análisis es del programa completo, no de elementos individuales. Los instrumentos de lectura son los mismos: medidores de nivel (LUFS, Peak, True Peak), goniómetro y correlatómetro para la imagen y la correlación, analizador espectral para el balance frecuencial.

Antes de insertar el primer procesador activo: analizar. El análisis lleva minutos; una corrección sin diagnóstico puede llevar mucho más tiempo deshacerse de sus consecuencias.

**Filtrado de subsónicas**
La energía por debajo del fundamento de la canción (frecuencias muy bajas que ningún instrumento produce intencionalmente) no aporta información musical y carga los transductores de reproducción doméstica. En mastering, el HPF subsónico no es obligatorio por defecto: es necesario solo si el análisis muestra energía problemática en esa zona.

El criterio: si en el analizador la curva espectral desciende de forma continua desde el fundamento del bajo o del bombo hacia las frecuencias más bajas, sin acumulación visible, no hay problema de subsónicas. Si hay energía que sube o se sostiene en la zona de 20–40 Hz sin corresponder a ningún instrumento del programa, aplicar HPF suave (pendiente de 12–18 dB/oct) con la frecuencia de corte justo por debajo del fundamento más grave del programa.

**Corrección de resonancias**
Las resonancias en mastering son problemas frecuenciales de carácter general: energía en exceso en una frecuencia que afecta a toda la canción. El diagnóstico: el analizador muestra un pico que persiste durante todo el programa o durante pasajes amplios, y que al escucharse en solo (con barrido de EQ o con notch) es claramente audible como un exceso que colorea el programa.

La corrección depende del tipo de resonancia:
- Resonancia estática (presente todo el tiempo): EQ paramétrico con Q adecuado a la anchura del problema.
- Resonancia intermitente (aparece en ciertos momentos): EQ dinámico que solo actúa cuando la resonancia supera el umbral.

Si la resonancia está principalmente en el contenido central de la imagen (Mid) y no en los laterales, el procesamiento en modo M/S permite corregirla en el Mid sin afectar el Side. Si está distribuida por igual en toda la imagen, el EQ convencional es suficiente.

**Corrección de balance L/R**
Si la mezcla tiene más energía en un canal que en el otro, el oyente percibe que el programa "se apoya" en un lado. Este problema puede aparecer cuando el bombo, el bajo o el tambor fueron mezclados fuera del centro, lo que produce un desequilibrio especialmente evidente en las bajas frecuencias.

En mastering, la corrección disponible es el **mono maker**: una herramienta que pasa gradualmente a mono por debajo de una frecuencia de corte específica, centrando los graves sin tocar los medios ni los agudos. El resultado es que las frecuencias bajas —que son omnidireccionales y se esperan al centro— quedan simétricas entre canales.

Si el desequilibrio viene de un elemento paneado incorrectamente en la mezcla, la solución correcta es devolver el material al mixdown. El mono maker puede atenuar el síntoma pero no resuelve el problema de origen.

**Acción**
1. Con el material preparado: abrir el analizador espectral, el goniómetro y el correlatómetro, y el medidor LUFS.
2. Reproducir el programa completo observando los instrumentos de lectura sin procesar nada.
3. Registrar: ¿hay energía subsónica problemática? ¿Hay resonancias visibles y audibles? ¿El goniómetro muestra desequilibrio entre canales? ¿El correlatómetro muestra problemas de correlación en alguna zona frecuencial?
4. Con el diagnóstico claro: aplicar las correcciones en el orden que corresponde a la etapa técnica.

**Verificación**
Después de cada corrección de la etapa técnica: verificar que el problema diagnosticado se redujo sin introducir problemas nuevos. Un HPF subsónico que afecta el fundamento del bombo o del bajo fue colocado demasiado alto. Un notch que elimina una resonancia también recorta el timbre de los instrumentos que son útiles en esa frecuencia: verificar que la Q fue mínima.

**Error frecuente**
Comenzar el procesamiento de mastering sin diagnóstico técnico previo, aplicando EQ o compresión "por defecto" sobre un programa que puede tener problemas técnicos no identificados. Un compresor aplicado sobre un programa con resonancias hará que esas resonancias dominen el disparo del compresor y amplifique su impacto.

---

### 7-D1 · COMPRESIÓN EN MASTERING: EN SERIE, PARALELA Y ASCENDENTE

**Situación real**
El alumno quiere que el master suene más denso y cohesionado. Inserta un compresor con ratio 4:1 y ataque rápido. El resultado es una mezcla más nivelada pero que perdió el impacto de la batería. Sube el ataque. Ahora la batería tiene impacto pero el cuerpo de la mezcla sigue sin tener la densidad que buscaba. Un solo compresor no puede resolver ambos objetivos simultáneamente.

**Explicación operativa**
La compresión en mastering actúa sobre el programa completo, lo que significa que las decisiones de parámetros deben considerar simultáneamente todos los instrumentos del programa. Lo que funciona para comprimir la voz en el Eje 4 puede destruir los transitorios de la batería si se aplica al mix con las mismas configuraciones.

El principio que organiza la compresión de mastering: varios pasos pequeños producen mejor resultado que un salto grande en pocos pasos. Distribuir la reducción de ganancia en más de un compresor, con cada uno haciendo menos, permite que cada compresor opere de forma más musical y produce menos coloración negativa que un único compresor forzado a hacer todo el trabajo.

**Compresión en serie**
Dos compresores en cadena con tareas diferenciadas:

*Primer compresor — carácter y consistencia:* un compresor de respuesta lenta, dependiente del programa (Vari-mu, valvular). Su tarea es añadir pegamento, calidez y consistencia general al programa. Reducción de ganancia moderada (1–3 dB), actuando sobre el promedio. Con el programa ya parcialmente nivelado por este compresor, el siguiente trabaja en mejores condiciones.

*Segundo compresor — control de picos percusivos:* un compresor de respuesta más rápida y precisa (VCA). Su tarea es controlar los picos que el primer compresor no gestionó. El primer compresor ya redujo la variabilidad dinámica del programa; el segundo solo tiene que manejar el rango residual.

**Compresión paralela en mastering**
Mezclar el programa original con una copia muy comprimida puede subir el nivel de los pasajes más suaves sin aplastar los más fuertes. La rama comprimida eleva los valles dinámicos; al mezclarse con el original, los picos del original se preservan.

El costo en mastering: las envolventes muy rápidas en la compresión paralela pueden introducir aliasing y distorsión inarmónica. Envolventes más lentas en la rama comprimida producen resultados más transparentes.

**Compresión ascendente**
Levanta el nivel de los pasajes más bajos sin tocar los más fuertes. Es lo opuesto a la compresión descendente: actúa por debajo del umbral aumentando la ganancia de lo que no llega a ese umbral. Es una alternativa más transparente que la compresión paralela para aumentar la densidad de los pasajes suaves, porque no introduce el costo de aliasing de la compresión paralela agresiva.

**Acción**
1. Antes de cualquier compresión: verificar que la etapa técnica está resuelta.
2. Para compresión en serie: insertar el compresor musical (valvular u óptico) primero, con reducción moderada y envolventes lentas. Verificar el resultado antes de continuar.
3. Insertar el segundo compresor (VCA o FET) para el control de picos residuales.
4. Verificar con bypass a nivel compensado en cada etapa.
5. Si se quiere aumentar la densidad de los pasajes suaves con mínima distorsión: evaluar compresión ascendente antes de la compresión paralela agresiva.

**Verificación**
Con la cadena de compresión completa: bypass total a nivel compensado. La diferencia debe ser perceptible como mayor cohesión y densidad, no como pérdida de transitorios o aplastamiento del programa. Si con bypass el programa suena más dinámico sin perder cohesión, la compresión está haciendo demasiado.

**Error frecuente**
Intentar resolver con un único compresor tanto el objetivo de carácter y consistencia (que requiere respuesta lenta, envolventes musicales) como el control de picos (que requiere respuesta rápida y precisión). El resultado es siempre un compromiso que no sirve bien para ninguno de los dos objetivos.

---

### 7-D2 · SATURACIÓN: CARÁCTER SIN DISTORSIÓN

**Situación real**
El alumno aplica un saturador en el master para añadir "calor". La mezcla suena diferente, pero al comparar con bypass a nivel compensado, la diferencia que escucha es difícil de separar de un simple cambio de nivel. No sabe si está añadiendo carácter real o simplemente subiendo el volumen.

**Explicación operativa**
La saturación en mastering es la adición de distorsión armónica deliberada al programa completo. En cantidades muy pequeñas —décimas de dB de THD— puede añadir riqueza armónica, aumentar la densidad percibida de los pasajes más suaves y aportar una sensación de "calor" o "presencia" que los procesadores dinámicos no generan.

El segundo armónico (el doble de cada frecuencia fundamental) produce una sensación de calidez y musicalidad. En cantidades controladas, es prácticamente indetectable como distorsión pero contribuye al "color" del programa.

El criterio de cantidad: si la saturación es audible como distorsión identificable, hay demasiada. La saturación de mastering opera en el límite de la percepción. Su efecto real se percibe como "el programa suena más presente" o "más cálido", no como "hay distorsión en el programa".

La trampa del nivel: cualquier saturador que añade armónicos también sube el nivel percibido, aunque sea mínimamente. Si se compara con bypass sin compensar el nivel, lo que se percibe como "mejora" puede ser simplemente más volumen. La comparación válida es siempre con nivel compensado.

**Posición en la cadena**
La saturación puede colocarse antes o después de los compresores según el objetivo:
- Antes de los compresores: los armónicos generados por la saturación son gestionados por el compresor. El compresor procesa un programa ya coloreado.
- Después de los compresores: los armónicos se añaden al material ya procesado dinámicamente.

En mastering la posición más habitual es antes del limitador: la saturación añade carácter y el limitador controla el ceiling. Si la saturación va después del limitador, los armónicos pueden superar el ceiling establecido.

**Acción**
1. Aplicar la saturación con una cantidad mínima (empezar desde el punto más bajo audible).
2. Verificar con bypass a nivel compensado: la diferencia debe ser de timbre y densidad, no de volumen.
3. Si la diferencia desaparece al compensar el nivel, la cantidad de saturación es irrelevante o cero.
4. Si la diferencia es audible como distorsión identificable, reducir la cantidad.

**Verificación**
Reproducir el pasaje más dinámico del programa con y sin saturación a nivel compensado. Si el programa con saturación suena más "presente" o "cálido" sin sonar distorsionado, la saturación está funcionando correctamente. Si la diferencia es principalmente de nivel, la cantidad de saturación no está produciendo carácter real.

**Error frecuente**
Aprobar la saturación sin compensar el nivel al comparar con bypass. La ilusión de mejora producida por el aumento de nivel puede llevar a aplicar más saturación de la necesaria, acumulando distorsión en el programa que solo se percibe como tal cuando se escucha en contexto de distribución.

---

### 7-E1 · MID/SIDE Y AJUSTE DE IMAGEN SOBRE EL PROGRAMA COMPLETO

**Situación real**
El alumno escucha el master y nota que los graves del programa están ligeramente desequilibrados entre canales: hay más energía en el lateral izquierdo en la zona de 60–80 Hz. También hay una resonancia de la caja que aparece en toda la mezcla pero principalmente en la imagen central, no en los laterales. Necesita dos correcciones que operan en partes diferentes del campo estéreo.

**Explicación operativa**
El procesamiento Mid/Side en mastering usa exactamente la misma mecánica de codificación y decodificación que en el Eje 5. La diferencia es el escenario: en mastering, el M/S opera sobre el programa completo entregado. Cualquier intervención en el Mid afecta simultáneamente a la voz, el bombo, el bajo y cualquier otro elemento central del programa. Cualquier intervención en el Side afecta a todo el contenido lateral.

**Correcciones espectrales con MS**
Si una resonancia está principalmente en el Mid (contenido central del programa), aplicar el EQ correctivo en el canal Mid del procesamiento M/S evita modificar el Side. Si estuviera en los laterales, se corrige en el Side sin tocar el Mid.

**Ajuste de imagen estéreo**
La imagen estéreo del programa puede ajustarse de forma global mediante el procesamiento M/S:
- Aumentar el nivel del Side: amplía la imagen.
- Reducir el nivel del Side: estrecha la imagen.
- Combinar con procesamiento por bandas de frecuencia: mantener los graves más centrados (reducir el Side en graves) y abrir la imagen a medida que sube la frecuencia.

La práctica de mantener los graves más centrados en mastering tiene base perceptual y técnica: los graves son omnidireccionales y el cerebro no los localiza con precisión (como ya se vio en Eje 5), y la energía de baja frecuencia en el Side puede introducir problemas en la reproducción en sistemas mono. Al reducir el Side en graves, el peso del programa aumenta perceptualmente porque la energía que estaba distribuida entre dos canales de forma menos eficiente se concentra en la imagen central.

**Límites del MS en mastering**
El procesamiento M/S en mastering es quirúrgico pero global. No puede corregir un elemento específico que está en el Mid sin afectar a todos los demás elementos del Mid simultáneamente. Si el bajo de una guitarra puntual está desbalanceado, el MS en mastering no puede aislarlo: ese problema pertenece a la mezcla.

**Acción**
1. Al identificar una resonancia que está principalmente en el Mid: activar el procesamiento M/S, verificar que la resonancia está efectivamente en el Mid (el analizador en el canal M debe mostrar el pico; el canal S, no), aplicar la corrección en el Mid.
2. Para ajuste de imagen estéreo: evaluar en el goniómetro si la imagen es adecuada para el género y el destino.
3. Para centrar los graves: aplicar reducción del Side en la zona de frecuencias graves con la pendiente adecuada para que la transición sea gradual y musical.

**Verificación**
Con el procesamiento M/S activo: decodificar de vuelta a L/R y comparar con bypass a nivel compensado. Las correcciones deben ser perceptibles en el área del espectro donde se aplicaron y no deben cambiar el carácter del programa en las zonas no intervenidas.

**Error frecuente**
Usar el procesamiento MS en mastering para corregir problemas de elementos individuales que pertenecen a la mezcla. Si el bombo específico tiene más nivel en el canal izquierdo y se intenta corregir con MS, la reducción del Side en esa zona frecuencial también afecta a todos los demás instrumentos que tienen contenido lateral en esa misma frecuencia.

---

### 7-F1 · LIMITADOR DE MASTERING, MÉTODO DELTA Y TRUE PEAK

**Situación real**
El alumno inserta el limitador de mastering. Gira el threshold a fondo esperando que "suene más fuerte". El resultado es un programa aplastado. No entiende cómo funciona el limitador ni qué relación tiene el threshold con el nivel de salida. Tampoco sabe cómo verificar si el limitador está introduciendo distorsión.

**Explicación operativa**
El limitador de mastering es la herramienta de la etapa comercial. Su función es subir la ganancia del programa y simultáneamente limitar lo que supera el umbral, de forma que el programa llegue al destino de distribución al nivel de sonoridad adecuado sin superar el techo de pico establecido.

**Cómo funciona el threshold en el limitador de mastering**
En un limitador de mastering, el threshold no es simplemente el punto donde empieza la limitación: es el control de cuánta ganancia se aplica al programa. Bajar el threshold X dB sube la ganancia del programa X dB pero limita lo que supera ese umbral. El Out Ceiling establece el techo de pico de salida.

El flujo correcto:
1. Definir el objetivo de LUFS integrados del master (según el género y el destino).
2. Medir los LUFS integrados actuales del programa.
3. Estimar cuántos dB de ganancia se necesitan para alcanzar el objetivo.
4. Usar el threshold para aplicar esa ganancia; usar el Out Ceiling para establecer el techo de pico.

Sin definir el objetivo primero, el ajuste del threshold es arbitrario.

**Método delta para verificar el limitador**
El limitador introduce inevitablemente algún cambio en la señal: acorta transitorios, puede producir distorsión si trabaja demasiado, altera las envolventes. Para evaluar qué modificó el limitador, se usa el método delta:

1. Tomar la señal original (sin limitar) y la señal limitada.
2. Invertir la polaridad de la señal limitada.
3. Sumar ambas señales. El resultado es la diferencia entre original y limitado: lo que el limitador modificó.
4. Escuchar esa diferencia al mismo nivel que la señal original.

Si el delta suena principalmente a transitorios levemente recortados (especialmente en los ataques de la batería y los picos de pizca de la guitarra), el limitador está trabajando de forma razonable. Si el delta suena a distorsión generalizada, hay sobrecompresión: el limitador está modificando más de lo aceptable.

**Release del limitador y distorsión**
Un release demasiado rápido en el limitador puede generar distorsión cuando la señal tiene componentes de baja frecuencia de período largo. Si el release es tan rápido que el limitador actúa sobre porciones largas de onda de baja frecuencia (no solo sobre picos breves), produce distorsión armónica no deseada.

La relación: release más corto → más volumen posible, más riesgo de distorsión en graves. Release más largo → menos distorsión, menos ganancia posible. El equilibrio depende del contenido frecuencial del material y del objetivo de sonoridad.

**True Peak**
El True Peak (dBTP) mide los picos de reconstrucción analógica que ocurren entre muestras del archivo digital. Un archivo puede tener todos sus picos de muestra dentro del ceiling establecido y aun así producir clipping durante la conversión D/A o la codificación a MP3/AAC, porque esos procesos reconstruyen la señal continua y los picos entre muestras pueden superar 0 dBFS.

El ceiling del limitador debe establecerse como True Peak, no como Peak convencional. El valor habitual para distribución en streaming es –1 dBTP: ese margen protege contra el overshooting que ocurre durante la codificación.

Advertencia adicional: el archivo WAV de entrega con True Peak en –1 dBTP puede producir picos superiores a 0 dBFS en el archivo MP3/AAC resultante, porque el proceso de codificación introduce su propio overshooting. Verificar el True Peak del archivo codificado, no solo del archivo de entrega.

**Acción**
1. Definir el objetivo de LUFS integrados antes de ajustar el threshold.
2. Ajustar el threshold del limitador hasta alcanzar el objetivo de LUFS.
3. Establecer el Out Ceiling en –1 dBTP como punto de partida.
4. Verificar con el método delta si el limitador está introduciendo distorsión aceptable.
5. Si el delta indica distorsión: evaluar si el release es demasiado rápido para el material.
6. Exportar el archivo de entrega y verificar el True Peak del archivo codificado (MP3/AAC).

**Verificación**
Comparar la señal limitada con la original a nivel compensado. La señal limitada debe sonar más densa y nivelada sin perder los transitorios percusivos de la mezcla. El delta del método delta debe sonar principalmente a picos de batería levemente recortados, no a distorsión generalizada del cuerpo de la mezcla.

**Error frecuente**
Establecer el Out Ceiling del limitador como Peak convencional en lugar de True Peak. Un Out Ceiling de 0,0 dBFS en Peak convencional puede producir True Peaks de +0,5 a +1 dBTP o más, especialmente en material con mucho contenido de alta frecuencia o con muchos transitorios. Al codificar ese archivo a MP3/AAC, el overshoot se amplifica y el archivo final puede saturar.

---

### 7-G1 · NORMALIZACIÓN DE PLATAFORMAS, LUFS OBJETIVO Y CRITERIO POR GÉNERO

**Situación real**
El alumno masteriza una canción a –8 LUFSi pensando que "suena más fuerte y es más competitivo". Al subirla a Spotify, suena exactamente igual de fuerte que una canción masterizada a –14 LUFSi. No entiende qué pasó con el nivel que tanto trabajó.

**Explicación operativa**
Las principales plataformas de streaming miden el LUFS integrado del material y ajustan el volumen de reproducción para igualarlo a su target interno. Si el material llega por encima del target, la plataforma baja el volumen de reproducción. Si llega por debajo, algunas plataformas lo suben (no todas) o lo reproducen como está.

Esto es ganancia de reproducción: la plataforma no comprime el audio, no procesa la señal, no añade ni quita calidad. Solo ajusta a cuánto volumen se reproduce.

Consecuencia práctica: masterizar a –8 LUFSi para Spotify produce exactamente la misma experiencia de escucha que masterizar a –14 LUFSi, porque Spotify bajará el material de –8 al mismo volumen. La diferencia es que el material de –8 LUFSi tiene menos rango dinámico —se usó más compresión y limitación para alcanzar ese nivel— y esa dinámica ya no puede recuperarse.

**Valores de referencia por plataforma** *(sujetos a cambio; verificar siempre en la documentación oficial de cada plataforma antes de publicar)*

| Plataforma | Target aproximado |
|---|---|
| Spotify | –14 LUFSi |
| Apple Music | –16 LUFSi |
| YouTube | –14 LUFSi |
| Tidal | –14 LUFSi |
| Broadcast EBU R128 | –23 LUFSi |

Estos valores pueden actualizarse. La documentación oficial de cada plataforma es la fuente definitiva.

**El target de LUFS depende del género**
No existe un target de LUFS "correcto" universal. El nivel adecuado del master depende del género y del contexto de escucha:

- Música electrónica, trap, reggaetón: tienden a masters más comprimidos y densos, entre –8 y –10 LUFSi. El rango dinámico intencional es menor.
- Pop/rock con batería acústica: típicamente entre –10 y –14 LUFSi, con PLR de 10–14 LU.
- Jazz, música acústica, orquestal: pueden llegar a –16 a –18 LUFSi con PLR de 16–18 LU o más.

Llevar un material a –10 LUFSi no implica necesariamente sacrificar dinámica. Depende de cuánta compresión y limitación se aplicó para llegar ahí. Con el procesamiento correcto, es posible alcanzar –10 LUFSi con un PLR de 10–12 LU, lo que sigue siendo un material dinámico.

**Acción**
1. Antes de comenzar el master: identificar el género del material y el destino de distribución principal.
2. Elegir el objetivo de LUFS considerando el género, no solo el target de la plataforma.
3. Verificar el PLR resultante: un PLR demasiado bajo para el género es señal de sobrecompresión.
4. Consultar la documentación oficial de la plataforma antes de publicar para confirmar los targets actuales.

**Verificación**
Al terminar el master: medir el LUFS integrado del programa completo. Verificar que el PLR resultante (Peak – LUFS integrado) es coherente con el género. Si el PLR es significativamente menor que el rango esperado para ese género, evaluar si hay sobrecompresión en la cadena.

**Error frecuente**
Masterizar lo más fuerte posible creyendo que superar el target de la plataforma da ventaja competitiva. En plataformas con normalización activa, el resultado es que el material se reproduce al mismo volumen que el material bien masterizado, pero con menos dinámica. El "loudness war" no produce ventaja en plataformas con normalización.

---

### 7-H1 · DITHERING, NOISE SHAPING, RESAMPLEO Y ENTREGA DEL ARCHIVO FINAL

**Situación real**
El alumno exporta el master para CD. El proyecto está a 24 bits, 44.1 kHz. El destino requiere 16 bits. Exporta sin dithering "para mantener la señal limpia". No sabe que acaba de introducir distorsión de cuantización en el archivo que es más perceptible que el ruido del dithering.

**Explicación operativa**
El dithering y el resampleo son las últimas operaciones del proceso de mastering, aplicadas en la conversión final al formato de entrega. Pertenecen al mismo territorio de la cadena digital que fue introducido en el Eje 0-B; aquí se aplican al contexto específico de la entrega del master.

**Dithering: qué es y cuándo se aplica**
Al reducir la profundidad de bits de una señal digital (de 24 bits a 16 bits, por ejemplo), cada muestra de amplitud que estaba representada con 24 escalones de resolución ahora debe representarse con 16. Las muestras que no coinciden exactamente con ningún escalón de 16 bits deben redondearse al más cercano. Ese redondeo introduce distorsión de cuantización: una distorsión no lineal que se percibe como un sonido áspero y desagradable en los pasajes suaves.

El dithering añade ruido aleatorio de muy bajo nivel antes de la conversión. Ese ruido hace que el redondeo se distribuya de forma estadísticamente aleatoria entre los escalones disponibles, convirtiendo la distorsión de cuantización no lineal en ruido lineal. El ruido es más perceptible en los pasajes de mayor silencio, pero es menos molesto que la distorsión de cuantización.

**Cuándo se aplica el dither:**
- Solo cuando hay reducción de profundidad de bits (24→16, 32→16, 32→24).
- Solo una vez, en la conversión final al formato de entrega definitivo.
- No se aplica si se exporta a la misma profundidad de bits.
- No se aplica en exportaciones intermedias de trabajo.

Para la entrega a plataformas de streaming en 24 bits: no aplicar dither (no hay reducción de profundidad). Para entrega en CD (16 bits): aplicar dither en la conversión 24→16.

**Noise shaping**
El noise shaping redistribuye el ruido del dithering hacia las frecuencias donde el oído es menos sensible (alta frecuencia), reduciendo la percepción del ruido en las zonas de mayor sensibilidad auditiva (medios). El ruido total del sistema no disminuye; se mueve a donde molesta menos.

El noise shaping puede aplicarse en distintos grados de agresividad. Los más comunes (Tipo 1, Tipo 2) son seguros para la mayoría de los materiales. Las versiones más agresivas mueven más ruido a la alta frecuencia pero pueden aumentar el nivel de ruido audible en esa zona. Usar el grado de agresividad mínimo que produce el resultado deseado.

**Resampleo**
El resampleo cambia la frecuencia de muestreo de la señal. Si el proyecto se trabajó a 96 kHz y el destino requiere 44.1 kHz, el archivo debe resamplearse. Un resampleo de baja calidad puede introducir aliasing y artefactos.

Usar el algoritmo de resampleo de mayor calidad disponible en el DAW, o usar una aplicación externa especializada en Sample Rate Conversion (SRC). El DAW puede mostrar diferencias de calidad entre sus distintos algoritmos de resampleo; comparar los resultados antes de elegir. Para trabajos críticos, aplicaciones como r8brain o zplane Élastique ofrecen conversión de alta calidad.

**Entrega del archivo final**
Al exportar el master definitivo:
1. Verificar el sample rate correcto para el destino.
2. Verificar la profundidad de bits correcta para el destino.
3. Aplicar dither solo si hay reducción de profundidad de bits.
4. El Master Fader en 0 dB.
5. Verificar el archivo exportado: abrir el archivo y verificar los LUFS integrados, el True Peak, y la forma de onda.
6. Si el destino incluye codificación a MP3/AAC: verificar el True Peak del archivo codificado.

**Acción**
1. Determinar el sample rate y la profundidad de bits del destino.
2. Si hay reducción de profundidad: activar el dithering con noise shaping.
3. Si hay cambio de sample rate: aplicar el SRC de mayor calidad disponible.
4. Exportar con el Master Fader en 0 dB.
5. Abrir el archivo exportado y verificar.
6. Si se codificará a formato comprimido: verificar el True Peak del archivo codificado final.

**Verificación**
Abrir el archivo exportado en el DAW. Los LUFS integrados deben coincidir con el objetivo. El True Peak debe estar dentro del ceiling establecido. La forma de onda no debe mostrar clipping. Si el archivo suena diferente al reproducirlo del export vs reproducir el proyecto del DAW, verificar la cadena de exportación (dithering innecesario, resampleo con artefactos, Master Fader incorrecto).

**Error frecuente**
Aplicar dither en cada exportación "por si acaso". Si el archivo se está exportando a la misma profundidad de bits (por ejemplo, exportar el proyecto de 32 bit float a 24 bits para guardar un backup antes de la exportación final), no se aplica dither. El dither se aplica solo en la conversión final al formato de entrega definitivo. Aplicar dither en etapas intermedias acumula ruido innecesario.

---

### 7-I1 · COHERENCIA, NIVELACIÓN Y REFERENCIA CRUZADA EN EL ÁLBUM

**Situación real**
El alumno masteriza cuatro canciones de un EP. La primera es una balada acústica; la segunda es rock; la tercera es electrónica; la cuarta es un tema de pop con orquesta. Masteriza cada una de forma aislada, optimizando cada canción individualmente. Al escuchar el EP completo, la transición de la tercera a la cuarta canción produce un cambio brutal de carácter que parece un álbum diferente.

**Explicación operativa**
El mastering de un álbum no es el mastering de varias canciones independientes. Es el mastering de un conjunto cuyas partes deben convivir con identidad recognocible como producción coherente.

La diferencia entre masterizar un single y un álbum no es técnica sino de criterio: en el single, la optimización puede maximizar esa canción sin restricciones externas. En el álbum, cada decisión debe evaluarse también en relación con el conjunto. Una canción que suena perfecta en solitario puede sonar desproporcionada dentro del álbum.

**Coherencia de álbum**
Todas las canciones del álbum deben "sonar al mismo disco" aunque difieran en carácter, densidad, intensidad y género. Coherencia no significa mismo volumen ni mismo timbre: significa identidad recognocible como producción coherente.

Esto implica que las decisiones de compresión, saturación, EQ y limitación de cada canción deben evaluarse también en relación con las demás. Si la balada acústica requiere muy poco procesamiento y la canción de electrónica requiere mucho, esas decisiones son válidas individualmente. Lo que no puede ocurrir es que el conjunto suene como si lo hubieran masterizado personas diferentes con criterios opuestos.

**Referencia cruzada permanente**
El método operativo: al masterizar la segunda canción del álbum, tener la primera ya masterizada como referencia activa en la sesión. Al masterizar la tercera, tener las dos anteriores como referencia. Comparar constantemente con las canciones ya procesadas, sección a sección.

La comparación debe hacerse de forma similar a como se hizo en el Eje 6 durante la mezcla: estrofa con estrofa, estribillo con estribillo. No escuchar las tres canciones de corrido; comparar los mismos tipos de pasajes entre canciones.

**Nivelación de álbum**
La nivelación no significa LUFS iguales en todas las canciones. Significa que los cambios de sonoridad entre canciones sean intencionales y coherentes con el concepto del álbum.

En el contexto de escucha del álbum, puede ser perfectamente válido que una balada suene más suave que un tema de rock. Lo que no puede ocurrir es que el oyente perciba un salto de nivel no intencional que interrumpa la experiencia. Si las mezclas del álbum llegaron bien calibradas desde el Eje 6, la nivelación en mastering puede ser mínima; si llegaron muy disparejas, el trimming de entrada de cada canción es más importante que el procesamiento de carácter.

**Acción**
1. Al comenzar el álbum: masterizar la primera canción completamente antes de comenzar la segunda.
2. Al comenzar la segunda: importar el audio masterizado de la primera como referencia activa.
3. Comparar sección a sección: verificar que el estribillo de la segunda tiene una relación de energía y carácter coherente con el de la primera.
4. Documentar las decisiones de cada canción: qué procesamiento se aplicó y por qué. Esa documentación permite mantener la consistencia a lo largo del álbum.
5. Al terminar todas las canciones: escuchar el álbum completo en secuencia y verificar que las transiciones entre canciones son musicalmente coherentes.

**Verificación**
Escuchar el EP o álbum completo de principio a fin, sin interrupciones. Si alguna transición entre canciones produce un cambio de carácter que suena como si cambiara el álbum, hay un problema de coherencia. La solución no es siempre ajustar la canción problemática: puede ser ajustar su relación con las canciones vecinas.

**Error frecuente**
Aplicar el mismo target de LUFS a todas las canciones del álbum mecánicamente, ignorando que algunas canciones por su naturaleza y producción deben ser más dinámicas. Igualar todos los LUFS produce un álbum donde la balada acústica suena igual de comprimida que el tema electrónico, lo que destruye la identidad de cada canción dentro del conjunto.

---

## SECCIÓN 5 — DOSSIER CANÓNICO DE APOYO

---

### DEFINICIÓN Y ETAPAS DEL MASTERING

**Distinción mastering vs mezcla**

| Tipo de problema | Herramienta |
|---|---|
| El bajo de un instrumento específico suena mal | Mezcla (Eje 4 o 3) |
| Los graves de la canción completa son excesivos | Mastering (Eje 7-C) |
| Una nota de voz suena desafinada | Mezcla (Eje 2) |
| El programa completo tiene una resonancia general | Mastering (Eje 7-C) |

**Las tres etapas**
1. Técnica: correcciones formales de la señal (DC offset, asimetría, resonancias, subsónicas, balance L/R).
2. Comercial: optimización de sonoridad para el destino (compresión, saturación, limitación, targets).
3. Artística (optativa): carácter y color deliberados si el material lo necesita.

El orden es necesario. La etapa técnica siempre precede a la comercial.

---

### PREPARACIÓN Y REPARACIÓN

**Trimming**
Ajustar el clip gain de entrada para que los procesadores reciban la señal en su rango óptimo. Objetivo: ~–20 a –23 LUFSi si la cadena incluye procesadores de modelado analógico calibrados a AES.

**DC offset vs asimetría**

| Fenómeno | Descripción | Diagnóstico | Corrección |
|---|---|---|---|
| DC offset | Toda la forma de onda desplazada del cero | Estadísticas del archivo: valor de offset | HPF a 5–10 Hz |
| Asimetría | Señal centrada, picos desiguales entre semiciclos | Osciloscopio: distribución asimétrica | Filtro AllPass |

Si hay ambos: corregir DC offset primero (HPF), luego asimetría (AllPass).

---

### CORRECCIÓN ESPECTRAL

**HPF subsónico**
No es obligatorio por defecto. Solo si el análisis muestra energía problemática por debajo del fundamento de la canción. Pendiente: 12–18 dB/oct.

**Resonancias**
Estáticas: EQ paramétrico con Q mínimo necesario.
Intermitentes: EQ dinámico.
Localizadas en Mid: EQ en modo M/S, canal Mid.

**Balance L/R**
Desequilibrio en graves: mono maker con frecuencia de corte apropiada.

---

### COMPRESIÓN Y SATURACIÓN

**Compresión en serie**
1er compresor → carácter y consistencia: valvular/óptico, envolventes lentas, reducción moderada.
2do compresor → control de picos: VCA, más preciso, actúa sobre el rango residual.

**Compresión paralela en mastering**
Envolventes lentas en la rama comprimida para evitar aliasing. Sube los pasajes suaves sin aplastar los fuertes.

**Saturación**
Si es audible como distorsión: hay demasiada.
Comparar siempre con bypass a nivel compensado.

---

### LIMITACIÓN Y TRUE PEAK

**Limitador de mastering**
- Threshold = control de ganancia de entrada.
- Out Ceiling = techo de salida (True Peak).
- Primero definir el objetivo de LUFS; luego ajustar el threshold.

**Método delta**
Invertir la polaridad de la señal limitada y sumarla con la original. El resultado es lo que el limitador modificó. Escuchar a bajo nivel.

**True Peak**

| Formato | Verificación necesaria |
|---|---|
| WAV/AIFF de entrega | –1 dBTP como punto de partida |
| MP3/AAC codificado | Verificar True Peak del archivo codificado; puede superar el del WAV |

---

### TARGETS Y NORMALIZACIÓN

**Normalización de plataformas**
Ajusta el volumen de reproducción (ganancia), no comprime ni procesa el audio.

**Targets orientativos** *(verificar en documentación oficial de cada plataforma)*

| Plataforma | LUFS integrado |
|---|---|
| Spotify | –14 LUFSi |
| Apple Music | –16 LUFSi |
| YouTube | –14 LUFSi |
| EBU R128 (broadcast) | –23 LUFSi |

**Criterio por género**

| Género | LUFS orientativo |
|---|---|
| Electrónica / Trap / Reggaetón | –8 a –10 LUFSi |
| Pop/Rock con batería | –10 a –14 LUFSi |
| Jazz / Acústico / Orquestal | –14 a –18 LUFSi o más |

---

### DITHERING Y ENTREGA DIGITAL

**Cuándo aplicar dither**
- Solo cuando hay reducción de profundidad de bits.
- Solo una vez, en la conversión final.
- No en exportaciones intermedias.
- No si se exporta a la misma profundidad.

**Noise shaping**
Redistribuye el ruido del dither a frecuencias de menor sensibilidad auditiva. No reduce el ruido total; lo mueve.

**Resampleo**
Cambio de SR: usar el algoritmo SRC de mayor calidad disponible. Para trabajos críticos: aplicación externa especializada.

---

## SECCIÓN 6 — REGLAS PARA RAG

### Qué indexar

- Distinción mastering vs mezcla: tabla de tipos de problemas y herramientas.
- Las tres etapas del mastering con orden necesario.
- Trimming: objetivo de nivel de entrada (~–20 a –23 LUFSi).
- DC offset vs asimetría: tabla de diagnóstico y corrección.
- HPF subsónico: criterio de uso (no automático).
- Corrección de resonancias: estáticas vs intermitentes; EQ convencional vs MS.
- Balance L/R y mono maker: función y criterio.
- Compresión en serie en mastering: dos etapas con funciones diferenciadas.
- Compresión paralela y ascendente en mastering.
- Saturación en mastering: criterio de cantidad.
- MS en mastering: diferencia con MS en mezcla; alcance global.
- Ajuste de imagen estéreo por bandas en mastering.
- Limitador de mastering: threshold como control de ganancia, Out Ceiling como techo.
- Método delta: procedimiento y criterio de evaluación.
- Release del limitador y distorsión en graves.
- True Peak: definición, valor orientativo, verificación del archivo codificado.
- Normalización de plataformas: solo ajuste de volumen, no procesamiento.
- Tabla de targets de LUFS por plataforma con nota de verificación obligatoria.
- Criterio de LUFS objetivo por género.
- Dithering: definición, cuándo se aplica, una sola vez.
- Noise shaping: función, no reduce ruido total.
- Resampleo: SRC de calidad y fuentes externas.
- Mastering de álbum vs single: criterio de referencia cruzada.
- Nivelación de álbum: no LUFS iguales, sino cambios intencionales.

### Qué no indexar

- Mecánica del compresor (parámetros, tipos de circuito): pertenece a Eje 4.
- Mecánica del EQ (tipos, parámetros): pertenece a Eje 3.
- Mecánica M/S (codificación/decodificación): pertenece a Eje 5.
- Doctrina de bits, coma fija/flotante: introducida en Eje 0-B.
- Nivel de entrega de la mezcla al mastering: pertenece a Eje 6.
- Formulaciones orales del autor fuente (bloqueadas).

### Etiquetado por eje
`eje:7` para todo el contenido de esta unidad.

### Etiquetado por bloque interno
`bloque:7A` — definición y etapas.
`bloque:7B` — preparación y reparación.
`bloque:7C` — diagnóstico y corrección espectral.
`bloque:7D` — compresión y saturación.
`bloque:7E` — imagen estéreo y MS.
`bloque:7F` — limitación y True Peak.
`bloque:7G` — targets y optimización.
`bloque:7H` — dithering y entrega digital.
`bloque:7I` — mastering de álbum.

### Etiquetado por fase LDOV
El mastering completo es una instancia del ciclo LDOV aplicada al programa final:
- Diagnóstico técnico del programa: `LDOV:Leer`.
- Decisión de qué corregir, qué comprimir, qué nivel objetivo: `LDOV:Decidir`.
- Aplicación de la cadena de mastering: `LDOV:Operar`.
- Verificación con método delta, comparación con referencias, escucha del álbum: `LDOV:Verificar`.

### Teoría mínima vs ampliación opcional

**Teoría mínima obligatoria (prioridad alta):**
- Distinción mastering vs mezcla.
- Las tres etapas y su orden.
- Trimming: objetivo y herramienta.
- DC offset vs asimetría: diagnóstico y corrección.
- HPF subsónico: criterio de uso.
- Compresión en serie: dos etapas con funciones diferenciadas.
- Limitador: threshold como control de ganancia, Out Ceiling como techo.
- Método delta.
- True Peak: valor orientativo y verificación del codificado.
- Normalización de plataformas: no procesa, solo ajusta volumen.
- Dithering: cuándo se aplica.
- Criterio de referencia cruzada en álbum.

**Teoría de precisión útil (prioridad media):**
- Asimetría de forma de onda: causa física y corrección con AllPass.
- MS en mastering: corrección en Mid vs Side y ajuste de imagen.
- Compresión paralela y ascendente: diferencias y costos.
- Noise shaping: función y limitaciones.
- Release del limitador y distorsión en graves.
- Nivelación de álbum: criterio de cambios intencionales.

**Teoría profunda opcional (IA/FAQ/anexo):**
- Matemática del dithering: probabilidades y distribución estadística del ruido.
- Algoritmos de SRC y comparativa de calidad.
- Distorsión de intermodulación en limitadores.
- Historia y doctrina del libro "El arte y la ciencia del mastering" de Bob Katz.
- Comparativa de limitadores de mastering por algoritmo y carácter.
- Detalle técnico del overshoot en codificación MP3/AAC.

---

## SECCIÓN 7 — REGLAS PARA GUIONES

### Partes que deben ser demostración

- **Etapa técnica vs comercial:** mostrar el diagrama de flujo del proceso de mastering y demostrar con un ejemplo real qué ocurre cuando se aplica compresión antes de corregir una resonancia (la resonancia se amplifica).
- **Trimming:** mostrar el medidor LUFS antes y después del trimming. Demostrar en el compresor analógico la diferencia de comportamiento con señal correctamente calibrada vs señal excesiva.
- **DC offset y asimetría:** mostrar en el osciloscopio/estadísticas un archivo con DC offset y uno con asimetría. Demostrar la corrección de cada uno con la herramienta correcta.
- **Método delta:** demostrar el procedimiento completo (polaridad invertida + suma) y escuchar el delta a bajo nivel.
- **True Peak del archivo codificado:** mostrar el True Peak del WAV vs el True Peak del MP3 resultante del mismo archivo. La diferencia debe ser visible.
- **Normalización de plataformas:** demostrar que un master a –8 LUFSi y otro a –14 LUFSi se escuchan al mismo volumen en Spotify.

### Partes que pueden ser explicación a cámara

- Las tres etapas del mastering: descripción con diagrama.
- Distinción mastering vs mezcla: tabla de tipos de problemas.
- Dithering: concepto con visualización del ruido de cuantización vs ruido de dither.
- Normalización de plataformas: concepto de ganancia de reproducción.

### Partes que conviene enseñar con sesión real

- Mastering de una canción completa desde el trimming hasta la exportación.
- Mastering de dos canciones de un álbum con referencia cruzada activa.
- Verificación del True Peak del archivo codificado después de la exportación.

### Partes que conviene mandar a la capa de apoyo

- Matemática del dithering y distribución estadística.
- Comparativa de algoritmos SRC.
- Historia y doctrina del libro de Bob Katz.
- Comparativa de limitadores de mastering por algoritmo.

---

## SECCIÓN 8 — CAPA DE APOYO POR IA

### Temas que conviene dejar listos para profundización vía IA

- Matemática del dithering: cómo la adición de ruido aleatorio convierte distorsión de cuantización en ruido lineal.
- Algoritmos de Sample Rate Conversion: diferencias técnicas y comparativa de calidad entre SRC internos y externos.
- Limitadores de mastering: comparativa de caracteres (FabFilter Pro-L 2, Izotope Ozone, Waves L2, Oxford Limiter).
- Overshoot en codificación MP3/AAC: mecanismo técnico y por qué ocurre.
- "El arte y la ciencia del mastering" de Bob Katz: síntesis de los conceptos principales del libro.
- Distorsión de intermodulación en limitadores: cuándo ocurre y cómo afecta el material.
- Técnicas avanzadas de compresión ascendente en mastering.
- Noise shaping agresivo: cuándo produce artefactos y cómo detectarlos.

### Ejemplos de preguntas que el alumno podría hacerle a la IA

- "¿Cómo sé si mi mezcla tiene DC offset o asimetría de forma de onda? ¿Cómo los distingo visualmente?"
- "¿Cuándo tiene sentido usar compresión ascendente en lugar de compresión paralela en mastering?"
- "Explícame el método delta con más detalle: ¿cómo configuro exactamente la inversión de polaridad y la suma?"
- "¿Qué diferencia hay en práctica entre un limitador de mastering con release automático y uno con release manual?"
- "¿Por qué el True Peak del archivo codificado puede ser mayor que el del WAV de entrega?"
- "¿Cuál es el target de LUFS más adecuado para un EP de jazz con cuarteto acústico?"
- "Explícame cómo funciona la normalización de Spotify a –14 LUFS. ¿Qué pasa exactamente con un material que llega a –8 LUFS?"
- "¿Dónde aplico dither si estoy exportando a 24 bits para streaming y luego haciendo una copia a 16 bits para CD?"

---

## SECCIÓN 9 — BLOQUES QUE REQUIEREN ATRIBUCIÓN EXPLÍCITA

### PDF: Apunte Mastering 2022
Autoría: Pablo Rabinovich. La clasificación en tres etapas, el flujo de procesos habituales y los criterios de filtrado y compresión son del apunte. La doctrina técnica subyacente es de dominio general del campo. Todo el contenido de este eje está reformulado desde esa doctrina sin reproducir la formulación del apunte.

**Nota sobre la terminología de las etapas:** el apunte llama a las etapas "Técnica / Estética / Comercial". Las clases de mastering las llaman "Técnica / Comercial / Artística". La lógica subyacente es idéntica. En este eje se usa la terminología Técnica / Comercial / Artística, que es la que aparece con más consistencia en las transcripciones de clase.

### Método delta
Técnica estándar del campo de mastering, ampliamente documentada en fuentes independientes. No requiere atribución al autor fuente.

### Concepto de coherencia de álbum
La formulación "bajo un mismo techo" es del autor fuente. El concepto de coherencia de álbum es de dominio general del campo. La formulación usada en este eje ("sonar al mismo disco") es reformulación propia que no reproduce la expresión del autor fuente.

### Bob Katz
Si se recomienda el libro "El arte y la ciencia del mastering" como referencia bibliográfica: citar a Bob Katz como autor. No es contenido del curso fuente; es una referencia externa independiente.

---

## SECCIÓN 10 — CONTINUIDAD CON OTROS EJES

**De dónde viene este eje**
El Eje 7 viene del **Eje 6 — Integración global**.

La mezcla que entrega el Eje 6 es el input del Eje 7. El nivel de entrega (–20 a –23 LUFSi), el PLR coherente con el género, el headroom preservado y la coherencia del álbum son condiciones que el Eje 6 estableció. Si la mezcla llegó con esas condiciones satisfechas, la etapa técnica del mastering puede ser mínima y la etapa comercial puede enfocarse en optimizar sin tener que corregir primero.

Cruces activos con ejes anteriores:
- **Eje 0-B:** la doctrina de bits, coma fija/flotante y headroom digital fue introducida allí. El dithering y el resampleo son su aplicación en el contexto de la entrega final.
- **Eje 1:** los instrumentos de lectura (LUFS, Peak, True Peak, goniómetro, correlatómetro, analizador) son los mismos del Eje 1. El diagnóstico de mastering usa exactamente las mismas herramientas.
- **Eje 3:** el EQ de mastering aplica los mismos principios del Eje 3 en el contexto del programa completo.
- **Eje 4:** la compresión de mastering usa los mismos principios del Eje 4. Los circuitos, los parámetros y el Criterio del Triángulo no se repiten aquí; se aplican.
- **Eje 5:** la mecánica M/S fue introducida allí. El MS de mastering aplica esa misma mecánica sobre el programa completo entregado.

**El Eje 7 cierra el ciclo**
El Eje 7 no prepara ningún eje posterior: es el cierre del ciclo completo. El producto del Eje 7 es el master entregado para distribución. El proceso que comenzó con la calibración del sistema de escucha en el Eje 0 termina aquí, con el archivo que llegará al oyente.

El ciclo LDOV (Leer, Decidir, Operar, Verificar) que ha organizado la lógica de cada eje se completa en el mastering: el Eje 7 lee el programa completo, decide qué necesita, opera la cadena de mastering, y verifica la entrega. Es el LDOV a escala del proceso completo.

---

*KENTH Academy — Eje 7 · Versión de producción v1.0*
*Generado desde arquitectura congelada v1.0-final y paquete limpio Eje 7.*

---

*TODOS LOS EJES (0–7) HAN SIDO PRODUCIDOS.*
*Proyecto KENTH Academy — Capa Generativa Canónica y Diseño Pedagógico Final completo.*
