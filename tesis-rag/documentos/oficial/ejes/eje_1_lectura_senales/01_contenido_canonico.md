---
axis_id: "Eje 1"
axis_number: 1
axis_title: "Eje 1 - Lectura de señales"
doc_layer: "canonico"
doc_type: "teoria_principal"
source_origin: "course"
status: "ready_for_indexing"
language: "es"
allowed_for_indexing: true
---

# EJE 1 — LECTURA DE SEÑALES
### KENTH Academy · Mezcla y Masterización · Contenido Final de Curso

---

## SECCIÓN 1 — FUNCIÓN PRÁCTICA DEL EJE

El Eje 1 es el primer paso del ciclo LDOV: Leer.

Antes de ecualizar, comprimir, filtrar o corregir cualquier cosa, el trabajo es saber qué hay. Sin lectura previa, toda intervención opera sobre suposiciones. Con lectura previa, las decisiones tienen base.

El Eje 1 no corrige nada. No toca el audio. Solo diagnostica.

Tiene tres dominios de lectura:

**Nivel:** cuánta energía tiene la señal y cómo se distribuye en el tiempo. Los medidores de nivel (Peak, VU, RMS, K-System, LUFS) son los instrumentos de esta lectura.

**Fase y polaridad:** cómo se relacionan dos o más señales entre sí cuando se suman. El goniómetro, el correlatómetro y la escucha en mono son los instrumentos de esta lectura.

**Espectro:** cómo se distribuye la energía de la señal por frecuencia. El analizador espectral es el instrumento de esta lectura.

Los tres dominios operan sobre la cadena calibrada del Eje 0. Sin esa base, las lecturas no tienen contexto de referencia.

---

## SECCIÓN 2 — QUÉ DEBE PODER HACER EL ALUMNO AL TERMINAR ESTE EJE

Al completar el Eje 1, el alumno es capaz de:

- Leer una señal con un medidor Peak e identificar si hay clipping o riesgo de clipping en la cadena.
- Leer una señal con un medidor VU y entender qué representa esa lectura y qué no representa.
- Distinguir cuándo usar Peak, VU, RMS o LUFS según el objetivo diagnóstico.
- Calibrar un plugin de modelado analógico al estándar AES o EBU según corresponda.
- Diagnosticar una inversión de polaridad por escucha y por lectura de instrumentos.
- Distinguir entre inversión de polaridad y desfasaje, y saber cómo identificar cada uno.
- Leer un goniómetro e interpretar la forma geométrica que produce la señal.
- Leer un correlatómetro e identificar cuándo la correlación indica riesgo para la monocompatibilidad.
- Diagnosticar comb filtering por escucha y por firma espectral en el analizador.
- Configurar el analizador espectral según el objetivo diagnóstico: escala, resolución FFT, ventana, promediado.
- Detectar energía subsónica, picos de resonancia, sibilancias o problemas de balance tonal global usando el analizador.
- Usar una referencia comercial en el analizador para comparar el balance tonal de la mezcla en curso.

---

## SECCIÓN 3 — SUBSECCIONES FINALES DEL EJE

Las subsecciones siguen el orden de los dominios de lectura: nivel primero (es lo más inmediato), luego fase y polaridad (lectura relacional), luego espectro (lectura de densidad y distribución). Dentro del bloque de nivel, los medidores básicos preceden a los sistemas de sonoridad integrada porque estos últimos requieren entender los primeros.

**BLOQUE A — MEDICIÓN DE NIVEL**

- **1-A1** · Peak, VU y RMS: qué mide cada uno y cuándo usar cada uno
- **1-A2** · Sonoridad integrada: K-System y LUFS

**BLOQUE B — FASE Y POLARIDAD**

- **1-B1** · Polaridad: diagnóstico y lectura
- **1-B2** · Fase y comb filtering: diagnóstico espectral y relacional

**BLOQUE C — ANÁLISIS ESPECTRAL**

- **1-C1** · El analizador espectral: configuración para diagnóstico
- **1-C2** · Imagen estéreo: goniómetro y correlatómetro

---

## SECCIÓN 4 — CURSO PRINCIPAL DEL EJE

---

### 1-A1 · PEAK, VU Y RMS: QUÉ MIDE CADA UNO Y CUÁNDO USAR CADA UNO

**Situación real**
El alumno tiene un track de batería en el que el medidor de la DAW nunca supera –6 dBFS pero el sonido se percibe como compacto y denso. Otro track de sintetizador casi no mueve el medidor pero suena presente. Un tercero permanentemente toca –1 dBFS. Las tres situaciones requieren lecturas distintas para entenderse.

**Explicación operativa**
Los medidores de nivel capturan la señal con distintas velocidades y distintos promedios. Ninguno da toda la información solo. El problema no es cuál es mejor: es cuál responde a la pregunta que se está haciendo.

**Medidor Peak (PPM)**
Respuesta prácticamente instantánea. Captura el máximo nivel alcanzado muestra a muestra. No dice nada sobre el nivel promedio percibido de la señal: solo dice hasta dónde llegó el pico más alto. Su función en el flujo de trabajo es proteger la cadena de conversión D/A y la exportación. El retensor de picos (hold) muestra en valor numérico exacto el máximo alcanzado desde que se lo reinició.

**Medidor VU**
Integra la señal con una constante de aproximadamente 300 ms y una balística de retorno deliberadamente lenta. No captura transitorios cortos: si la batería tiene un golpe de 5 ms, el VU no lo verá. Muestra el nivel promedio sostenido de la señal, que es el que se aproxima a la percepción auditiva de intensidad para señales de contenido continuo. Su utilidad en mezcla es leer el nivel de trabajo de las señales que el oído "pesa", no las que impactan.

**Medidor RMS**
Calcula la raíz cuadrática media de la señal en una ventana temporal configurable. Más preciso que el VU para comparaciones cuantitativas de nivel sostenido. Su limitación es que las comparaciones entre medidores RMS de distintos plugins solo son válidas si usan el mismo tiempo de integración.

**Teoría mínima**
Un medidor Peak puede mostrar –6 dBFS mientras el VU marca –12 dBVU. Ambas lecturas son correctas y se refieren a cosas distintas. El peak describe el transitorio más agudo; el VU describe el peso sostenido. En señales percusivas, la diferencia entre ambas lecturas puede ser de 6 a 10 dB o más.

**Acción**
1. Colocar un medidor Peak con retensor activo en la salida de la sesión para verificar en cualquier momento el máximo alcanzado.
2. Colocar un medidor VU o RMS en los tracks de referencia para evaluar el nivel de trabajo de cada elemento.
3. Para plugins de modelado analógico: leer el VU del plugin e identificar si el nivel de entrada corresponde al estándar del plugin (ver subsección 1-A2 y Eje 0-B2).
4. Al exportar: verificar que el Peak no supere el techo de destino antes de confirmar la exportación.

**Verificación**
Reproducir un pasaje con batería completa. Observar simultáneamente el medidor Peak y el VU. Verificar que la diferencia entre ambas lecturas tiene sentido para el tipo de señal: en batería, es esperable una diferencia notable. Si el VU muestra casi lo mismo que el Peak en un signal de batería, hay compresión excesiva o los transitorios son demasiado reducidos.

**Error frecuente**
Usar el medidor Peak de la DAW como referencia de nivel de trabajo y mezclar con todo "en verde". Las barras de la DAW son medidores Peak, no VU ni RMS. Una señal que nunca toca el rojo puede estar siendo recibida por los procesadores a un nivel muy inferior o muy superior al que fue diseñado para ellos.

---

### 1-A2 · SONORIDAD INTEGRADA: K-SYSTEM Y LUFS

**Situación real**
El alumno termina una mezcla y la compara con un track de referencia comercial. La referencia suena más fuerte aunque los picos de ambas estén al mismo nivel. No sabe cómo cuantificar esa diferencia ni a qué apuntar.

**Explicación operativa**
El oído no percibe el nivel de la misma manera que un medidor Peak. Percibe el peso sostenido de la señal en el tiempo, ponderado por la sensibilidad frecuencial del oído. Un material muy comprimido puede tener picos moderados pero una densidad sostenida muy alta. Un material con mucho rango dinámico puede tener picos altos pero percibirse menos presente.

Existen dos sistemas para leer la sonoridad en términos que se acercan a la percepción:

**K-System (Bob Katz)**
Sistema de tres escalas RMS calibradas a 85 dBSPL en ponderación C en el punto de escucha. Lo que cambia entre las escalas es dónde se posiciona el 0 dB del medidor respecto al techo digital:

- K-20: 0 dB = –20 dBFS. Para material de amplio rango dinámico (clásica, teatro, cine).
- K-14: 0 dB = –14 dBFS. Para producción de alta fidelidad (pop, rock, jazz).
- K-12: 0 dB = –12 dBFS. Para material de broadcast o producción densa.

**LUFS / LKFS**
Sistema normalizado por estándares internacionales (EBU R128, ITU-R BS.1770) para medir sonoridad integrada. LUFS y LKFS son equivalentes. Se presentan en tres vistas:

- Momentary (400 ms): reacción muy rápida, muestra la sonoridad instantánea.
- Short-Term (~1–3 s): lectura de tendencia a corto plazo.
- Integrated: promedio del programa completo. Es la lectura relevante para entrega a plataformas de streaming.

El True Peak (dBTP) mide los picos que ocurren entre muestras (inter-sample peaks), que se hacen visibles al reconvertir el audio a formatos comprimidos. El True Peak es el parámetro de control de techo en la entrega.

**Teoría mínima**
El LUFS integrado de un programa no determina cuánto espacio hay disponible para transitorios: eso lo fija el True Peak. LUFS e target de plataforma son dos parámetros distintos. Un material puede cumplir el target LUFS de Spotify (–14 LUFS integrado) y aun así tener True Peaks que excedan el límite aceptable (–1 dBTP).

**Acción**
1. Insertar un medidor LUFS en el bus de salida con lectura Integrated activa desde el inicio de la reproducción de referencia.
2. Al terminar una mezcla, registrar el LUFS integrado antes de entregar para mastering.
3. Si el destino del proyecto ya es conocido, verificar el target de la plataforma correspondiente.
4. Si se trabaja con K-System: seleccionar la escala según el tipo de material y calibrar el nivel de monitoreo según el estándar (85 dBSPL en ponderación C).

**Verificación**
Comparar el LUFS integrado de la mezcla con el de la referencia comercial elegida. La diferencia cuantifica el gap de sonoridad. Si la referencia está a –9 LUFS y la mezcla está a –18 LUFS, hay 9 LU de diferencia, no un problema de EQ ni de compresión en primer lugar.

**Error frecuente**
Usar la lectura Momentary del medidor LUFS como indicador de nivel de mezcla. La lectura Momentary oscila con el material y no representa el nivel integrado del programa. Tomar decisiones de nivel con la lectura Momentary equivale a mezclar mirando el peak: no informa sobre el peso global de la mezcla.

---

### 1-B1 · POLARIDAD: DIAGNÓSTICO Y LECTURA

**Situación real**
El alumno graba batería con micrófonos de overhead y un micrófono de bombo. La suma suena opaca y el bombo pierde cuerpo cuando todos los micrófonos están activos. En el solado individual cada micrófono suena bien. El problema está en la relación entre señales, no en cada señal por separado.

**Explicación operativa**
La inversión de polaridad es una de las causas más comunes de pérdida de nivel y timbre al sumar señales. Es también la más fácil de diagnosticar y corregir. Antes de cualquier procesamiento, es el primer chequeo.

La polaridad es binaria: una señal tiene polaridad normal o polaridad invertida. Invertir la polaridad significa invertir el signo de toda la señal: lo que era positivo pasa a negativo, y viceversa. Esto es diferente del desfasaje: la polaridad invierte todas las frecuencias por igual; el desfasaje afecta a cada frecuencia de forma distinta según la diferencia temporal.

El botón rotulado con "∅" en consolas y plugins habitualmente invierte polaridad, no fase. Es importante llamar a cada cosa por su nombre porque el diagnóstico y la corrección son distintos.

**Teoría mínima**
Dos señales idénticas con polaridad opuesta se cancelan completamente al sumarse. El resultado es silencio. En la práctica, las señales rara vez son idénticas, por lo que la cancelación es parcial: hay pérdida de nivel y cambio de timbre pero no silencio total.

En una señal estéreo, si uno de los dos canales tiene polaridad invertida respecto al otro, hay dos síntomas:
1. Al colapsar a mono, los graves desaparecen o se reducen drásticamente, porque las frecuencias bajas son omnidireccionales y ambos canales se cancelan en esa zona.
2. La imagen estéreo puede percibirse extrañamente ancha, difusa o incómoda.

**Acción**
1. Con todos los micrófonos de una fuente activos, colapsar la mezcla a mono.
2. Comparar el nivel y el timbre con la escucha en estéreo. Si en mono hay pérdida evidente de nivel o de graves, hay inversión de polaridad o desfasaje.
3. Para aislar el problema: silenciar los micrófonos de uno en uno mientras se escucha en mono. Cuando el problema mejore al silenciar un micrófono específico, ese es el de polaridad invertida.
4. Invertir la polaridad del micrófono identificado con el botón ∅ y verificar que la suma en mono mejora.

**Verificación**
Después de la corrección, la suma en mono debe sonar al menos tan llena y presente como cualquiera de las señales individuales. Si la suma en mono suena más llena y densa que en estéreo, el material no tenía imagen estéreo real: era básicamente mono.

**Error frecuente**
Llamar a la inversión de polaridad "problema de fase" y aplicar un rotor de fase o un alineador temporal como corrección. Si el problema es de polaridad, la corrección es el botón ∅. Si se aplica rotación de fase a un problema de polaridad, el resultado en mono sigue siendo cancelación, solo que desplazada en frecuencia.

---

### 1-B2 · FASE Y COMB FILTERING: DIAGNÓSTICO ESPECTRAL Y RELACIONAL

**Situación real**
El alumno mezcla los overheads de batería con el resto de los micrófonos y nota que el sonido general tiene un carácter metálico o "robótico" difícil de corregir con EQ. Cualquier ajuste de frecuencias parece no resolver el problema. Al colapsar a mono el problema empeora drásticamente. No hay inversión de polaridad: los botones ∅ no cambian la situación.

**Explicación operativa**
El desfasaje entre dos micrófonos que captan la misma fuente produce comb filtering: un patrón de cancelaciones y sumas alternadas que se distribuye a lo largo del espectro. El resultado es una coloración tímbrica que no puede resolverse con EQ porque no es un problema de amplitud de frecuencias: es un problema temporal.

La firma del comb filtering en el analizador espectral es reconocible: una serie de cancelaciones periódicas equidistantes en frecuencia, que visualmente recuerdan los dientes de un peine.

**Teoría mínima**
Cuando dos señales coherentes (misma fuente) llegan con una diferencia temporal Δt, las frecuencias donde la diferencia equivale a medio ciclo (λ/2) se cancelan; las donde equivale a un ciclo completo (λ) se suman. La primera cancelación ocurre en:

f₁ = 1 / (2 × Δt)

Las siguientes cancelaciones están en los múltiplos impares: 3×f₁, 5×f₁, 7×f₁, etc.

Con una diferencia temporal de 5 ms, la primera cancelación está en 100 Hz. Las siguientes en 300, 500, 700 Hz... Eso explica el timbre metálico o resonante: el espectro está perforado a intervalos regulares.

La cancelación total solo ocurre si ambas señales tienen el mismo nivel. Si hay diferencia de nivel entre los micrófonos, la cancelación es parcial. La regla 3:1 en microfonía aprovecha este principio: si la distancia entre dos micrófonos es al menos tres veces la distancia de cada micrófono a su fuente, hay más de 9,5 dB de diferencia de nivel entre ambas capturas, lo que reduce el comb filtering a niveles mínimos.

**Acción**
1. Colapsar a mono para revelar el comb filtering. En estéreo puede estar oculto; en mono las señales se suman y el efecto se hace audible y visible.
2. Abrir el analizador espectral en la suma en mono y buscar el patrón de cancelaciones periódicas equidistantes.
3. Si el patrón está presente: identificar la frecuencia de la primera cancelación y calcular la diferencia temporal aproximada (Δt = 1 / (2 × f₁)).
4. La corrección —alineación temporal, rotor de fase, o ajuste de la posición del micrófono— pertenece al Eje 2. El Eje 1 solo diagnostica y cuantifica el problema.

**Verificación**
El diagnóstico está completo cuando: (1) el patrón periódico es visible en el analizador, (2) se puede estimar la diferencia temporal que lo produce, y (3) se puede confirmar qué par de micrófonos lo genera. Todo lo demás es Eje 2.

**Error frecuente**
Intentar corregir el comb filtering con EQ: recortar las frecuencias canceladas. No funciona porque las cancelaciones son interactivas: dependen de la suma de ambas señales, no de la amplitud de una sola. Cualquier EQ aplicado sobre una de las señales desplaza la amplitud pero no cambia el patrón temporal que produce el efecto.

---

### 1-C1 · EL ANALIZADOR ESPECTRAL: CONFIGURACIÓN PARA DIAGNÓSTICO

**Situación real**
El alumno abre el analizador espectral y ve una curva en tiempo real que cambia constantemente. No sabe si lo que ve representa lo que escucha, ni cómo configurarlo para que la lectura sea útil para tomar decisiones.

**Explicación operativa**
El analizador espectral representa la distribución de energía de la señal por frecuencia. Pero lo que muestra depende en gran parte de cómo está configurado. Con la configuración incorrecta, el analizador muestra ruido visual en lugar de información diagnóstica.

Hay cuatro variables clave:

**Escala (lineal vs logarítmica)**
La escala logarítmica distribuye las frecuencias por décadas: de 20 a 200 Hz, de 200 a 2000 Hz, de 2000 a 20000 Hz. Así es como el oído percibe la frecuencia. La escala lineal distribuye las frecuencias de manera uniforme en Hz, lo que da mucho espacio a las frecuencias altas y colapsa los graves. Para análisis de balance tonal general: logarítmica siempre. Para inspeccionar problemas específicos de muy alta frecuencia: lineal.

**Resolución FFT**
El analizador procesa la señal en bloques. El tamaño del bloque (expresado en número de muestras) define la resolución espectral. Un bloque mayor da más resolución por Hz pero tarda más en calcularse. Una buena referencia de partida es 8192 puntos, que equilibra resolución y seguimiento temporal. Para detectar problemas de muy baja frecuencia, aumentar. Para ver comportamiento dinámico rápido, reducir.

**División por octava vs FFT**
El análisis por 1/3 de octava promedia la energía en bandas perceptualmente relevantes. Es más estable visualmente y más cercano a lo que se escucha. El análisis FFT da resolución por Hz, útil para localizar problemas específicos. Para evaluar el balance global de una mezcla: 1/3 de octava. Para encontrar qué frecuencia exacta es problemática: FFT.

**Tilt**
El espectro de una mezcla bien balanceada no es plano: tiene más energía en graves que en agudos, porque así está construida la música y así funciona la física del sonido. Un analizador sin Tilt siempre mostrará la zona de graves como más alta que los agudos, incluso en mezclas bien balanceadas. El Tilt compensa esa pendiente y permite comparar el balance espectral de la mezcla con referencias en la misma escala.

**Teoría mínima**
Lo que el analizador muestra como "plano" no suena plano. El oído no percibe energía lineal: percibe energía logarítmica por octava. Una curva que parece plana en el analizador sin Tilt puede sonar brillante y delgada. Hay que leer el analizador siempre en relación con una referencia, no como representación absoluta del balance.

**Acción**
**Configuración para análisis de balance tonal general:**
- Escala: logarítmica
- División: 1/3 de octava
- Tilt: activado (~3 dB/octava)
- Average Time: moderado (suficiente para leer tendencia sin congelar el movimiento)
- Ventana: Hanning

**Configuración para detectar un problema específico de frecuencia:**
- Escala: logarítmica (o lineal para alta frecuencia)
- Modo: FFT
- Tamaño de bloque: 8192 o mayor
- Ventana: Hanning como punto de partida; Blackman-Harris para investigar artefactos de bajo nivel

**Para detectar contenido subsónico:**
- Extender el rango del analizador hasta –144 dB y hasta 20 Hz o menos
- Activar FFT con bloque grande para resolución en graves

**Verificación**
Cargar una mezcla de referencia comercial del género trabajado junto al material en curso. Leer ambas con la misma configuración. Las diferencias en el analizador deben coincidir con las diferencias percibidas al escuchar. Si el analizador muestra diferencias que el oído no detecta, verificar la configuración del analizador antes de tomar decisiones de EQ.

**Error frecuente**
Leer el analizador FFT de resolución baja y tomar sus anomalías como problemas reales del audio. Una FFT de 512 puntos a 44.1 kHz tiene una resolución de ~86 Hz por barra. Una depresión en esa barra no significa que haya un problema en una frecuencia específica: significa que esa barra incluye 86 Hz de rango.

---

### 1-C2 · IMAGEN ESTÉREO: GONIÓMETRO Y CORRELATÓMETRO

**Situación real**
La mezcla suena con buena amplitud estéreo en los auriculares pero al escucharla en monitores se percibe extraña, sin centro definido, con la imagen desplazada o incómoda. El alumno no sabe si el problema es real o si es el sistema de escucha.

**Explicación operativa**
El goniómetro y el correlatómetro son instrumentos de lectura de la relación entre los canales L y R de la señal estéreo. Uno es visual (goniómetro), el otro es numérico (correlatómetro), pero los dos responden a la misma pregunta: ¿cómo se relacionan los dos canales y qué pasará cuando se sumen en mono?

**Goniómetro**
Representa la relación de fase entre L y R en un sistema de ejes rotados 45°. La señal dibuja una forma geométrica cuya interpretación es la siguiente:

- Línea vertical estrecha: señal perfectamente mono (L = R). El material está centrado.
- Óvalo vertical (más ancho que alto): imagen estéreo saludable. Hay diferencias entre canales pero la correlación es positiva.
- Círculo: correlación de 90°. Las señales son independientes. Todavía hay suma (+3 dB), pero es el umbral de advertencia.
- Óvalo horizontal (más ancho que alto, tendiendo a horizontal): correlación mayor de 90°. Las señales empiezan a cancelarse al colapsar a mono.
- Línea horizontal: correlación de 180°. Las señales son opuestas. Cancelación total en mono.

Una inclinación del óvalo hacia la izquierda o la derecha indica paneo: hay más energía en uno de los canales.

**Correlatómetro**
Mide el coeficiente de correlación entre L y R en una escala de +1 a –1:

- +1 = 0°. Señales idénticas. Suma = +6 dB.
- 0 = 90°. Sin correlación. Suma = +3 dB.
- –1 = 180°. Señales opuestas. Cancelación total.

El promedio de la lectura importa más que los picos instantáneos. Si el promedio se sostiene cerca de 0 (90°), los picos de la dinámica llevan regularmente la correlación a zona negativa, con pérdida real al colapsar a mono.

**Teoría mínima**
En 90° todavía hay +3 dB de suma. El problema no es que la correlación llegue a 90° en algunos transitorios: eso es esperable en señales estéreo con contenido independiente en cada canal. El problema es que el promedio se sitúe en 90° de forma sostenida, porque significa que buena parte del tiempo la señal opera en un rango donde la monocompatibilidad es precaria.

**Acción**
1. Colocar goniómetro y correlatómetro en el bus de salida estéreo antes de comenzar a evaluar la imagen.
2. Reproducir el programa completo y observar la forma promedio del goniómetro.
3. Registrar la tendencia del correlatómetro durante el pasaje más denso de la mezcla.
4. Si el promedio del correlatómetro se sostiene cerca de 0 o en negativo: colapsar a mono y escuchar qué se pierde. Eso indica dónde está el problema.
5. Si el goniómetro muestra un óvalo muy ancho o tendiendo a horizontal: verificar si hay inversión de polaridad entre canales (ver subsección 1-B1).

**Verificación**
Colapsar la mezcla a mono y comparar con la escucha estéreo. Una pérdida de graves en mono con imagen ancha en estéreo: probablemente hay inversión de polaridad entre L y R. Una pérdida de medios o de presencia en mono: hay señales con desfasaje en esa zona frecuencial. Si en mono suena casi igual que en estéreo: la mezcla era básicamente mono aunque sonara ancha en auriculares.

**Error frecuente**
Interpretar el óvalo ancho del goniómetro siempre como señal de buena imagen estéreo. Un óvalo excesivamente ancho puede ser el síntoma de polaridad invertida entre canales o de señales artificialmente ensanchadas con desfase de fase que no resistirán la reproducción en mono.

---

## SECCIÓN 5 — DOSSIER CANÓNICO DE APOYO

---

### MEDIDORES DE NIVEL

**Peak (PPM)**
Velocidad de respuesta prácticamente instantánea. Detecta el valor máximo de muestra a muestra. No refleja el nivel percibido: una señal con transitorios muy altos y cuerpo reducido puede mostrar niveles Peak altos mientras se percibe como delgada. El retensor de picos (hold) muestra el valor máximo alcanzado desde el último reinicio en valor numérico exacto. Útil para detectar clipping en la cadena y para verificar el headroom disponible antes de la exportación.

**VU**
Integración temporal de ~300 ms con balística de retorno deliberadamente lenta. Diseñado para aproximarse a la percepción auditiva de intensidad en señales sostenidas. No captura transitorios cortos: en señales percusivas, la diferencia entre la lectura VU y el Peak puede ser de 6 a 10 dB o más. Calibración de referencia: 0 VU = +4 dBu (profesional) / –10 dBV (semipro). En digital: 0 VU = –20 dBFS (estándar AES RP155) o –18 dBFS (estándar EBU R68).

**RMS**
Raíz cuadrática media de la señal en una ventana temporal configurable. Más preciso que el VU para comparaciones cuantitativas. La compensación AES-17 define cómo medir el nivel RMS de señales de tono puro (señales de prueba), con una corrección de 3 dB para alinear la lectura de señales senoidales con la de ruido. Las comparaciones entre medidores RMS de distintos plugins solo son válidas si usan el mismo tiempo de integración.

**K-System (Bob Katz)**
Tres escalas RMS calibradas a 85 dBSPL en ponderación C en el punto de escucha:
- K-20: 0 dB = –20 dBFS. Material de amplio rango dinámico.
- K-14: 0 dB = –14 dBFS. Producción pop/rock de alta fidelidad.
- K-12: 0 dB = –12 dBFS. Broadcast.

La calibración SPL requiere un generador de tono de referencia y un medidor de nivel acústico. La escala se elige según el destino y el rango dinámico esperado del material, no según preferencia personal.

**LUFS / LKFS**
Equivalentes. Normalizados por EBU R128 / ITU-R BS.1770. Medición ponderada por sensibilidad frecuencial del oído (ponderación K), integrada en el tiempo.

| Tipo | Ventana temporal | Uso |
|---|---|---|
| Momentary | 400 ms | Seguimiento instantáneo de sonoridad |
| Short-Term | ~1–3 s | Tendencia a corto plazo |
| Integrated | Programa completo | Referencia de entrega a plataformas |

True Peak (dBTP): mide picos entre muestras. Relevante porque la reconversión a MP3/AAC puede crear clipping en esos picos aunque el archivo PCM no lo muestre. Los targets habituales para True Peak en entrega son –1 dBTP o –2 dBTP.

**Suma coherente y no coherente**

| Tipo de señal | Diferencia de nivel | Resultado |
|---|---|---|
| Coherente (misma fuente) | 0 dB | Depende de la fase: 0° → +6 dB / 90° → +3 dB / 120° → ~0 dB / 180° → cancelación |
| No coherente (fuentes distintas) | 0 dB | +3 dB siempre |
| Coherente o no coherente | 6 dB | ~+1 dB respecto a la más alta |
| Coherente o no coherente | 10 dB o más | La suma es prácticamente igual a la señal más intensa |

---

### FASE Y POLARIDAD

**Polaridad**
Binaria. Invierte el signo de toda la señal por igual en todas las frecuencias. No es equivalente a un desfasaje de 180°: el desfasaje afecta cada frecuencia según la relación entre la diferencia temporal y el período de cada frecuencia; la inversión de polaridad afecta todas las frecuencias simultáneamente con el mismo resultado.

Síntomas de inversión de polaridad en una señal individual:
- Al escucharla sola: no produce cambio perceptual de timbre (la onda es igual pero con signo opuesto).
- Al sumarla con otra señal de la misma fuente: pérdida de nivel o cancelación.

Síntomas de inversión de polaridad entre L y R en una señal estéreo:
- En estéreo: imagen puede percibirse extrañamente ancha o con sensación de incomodidad espacial.
- Al colapsar a mono: pérdida significativa de graves (frecuencias omnidireccionales que se cancelan entre canales).

**Fase y comb filtering**

| Diferencia temporal (Δt) | Primera cancelación | Zona afectada |
|---|---|---|
| 1 ms | 500 Hz | Medios-agudos |
| 2 ms | 250 Hz | Medios |
| 5 ms | 100 Hz | Bajos-medios |
| 10 ms | 50 Hz | Bajos |

Entre 1 y ~20 ms: el comb filtering produce coloración tímbrica audible (metálico, robótico, similar a flanger o chorus). Por encima de ese rango: las señales comienzan a percibirse separadas (eco, pre-delay).

La cancelación total requiere señales de la misma amplitud. La regla 3:1 establece que la distancia entre dos micrófonos debe ser al menos 3 veces la distancia de cada micrófono a la fuente, lo que genera más de 9,5 dB de diferencia de nivel y reduce el comb filtering a valores mínimos.

---

### ANALIZADOR ESPECTRAL

**Parámetros y criterios de configuración**

| Parámetro | Opción | Cuándo usarla |
|---|---|---|
| Escala | Logarítmica | Siempre para balance tonal general |
| Escala | Lineal | Para inspección de alta frecuencia específica |
| División | 1/3 de octava | Balance global, comparación con referencias |
| División | FFT | Localización de problemas específicos de frecuencia |
| FFT size | ~8192 | Equilibrio general |
| FFT size | 16384 o mayor | Diagnóstico de muy baja frecuencia |
| Tilt | ~3 dB/octava | Para comparar con referencias en escala natural |
| Ventana | Hanning | Análisis general |
| Ventana | Blackman-Harris | Detección de artefactos y distorsión de bajo nivel |

**Goniómetro — referencia de formas**

| Forma | Correlación | Interpretación |
|---|---|---|
| Línea vertical | +1 (0°) | Señal mono |
| Óvalo vertical | Positiva | Imagen estéreo saludable |
| Círculo | 0 (90°) | Señales independientes, umbral de advertencia |
| Óvalo horizontal | Negativa | Riesgo de cancelación en mono |
| Línea horizontal | –1 (180°) | Cancelación total en mono |

---

## SECCIÓN 6 — REGLAS PARA RAG

### Qué indexar

- Taxonomía completa de medidores: Peak, VU, RMS, K-System, LUFS — con definiciones funcionales y criterios de uso.
- Calibración VU: estándares AES y EBU con tabla de equivalencias.
- Tabla de resultados de suma coherente y no coherente por ángulo de fase.
- Diagnóstico de polaridad: método de colapso a mono, síntomas en mono y en estéreo.
- Distinción polaridad vs fase: definición operativa de cada una.
- Diagnóstico de comb filtering: firma espectral, fórmula de primera cancelación, rango de percepción tímbrica.
- Regla 3:1: definición y criterio operativo.
- Configuración del analizador espectral: tabla de parámetros por objetivo diagnóstico.
- Goniómetro: tabla de formas y correlaciones.
- Correlatómetro: escala, valores de referencia, criterio de promedio.
- LUFS: tipos de medición, relevancia de Integrated vs Momentary, True Peak.

### Qué no indexar

- Corrección de polaridad, alineación temporal, rotor de fase: pertenecen a Eje 2.
- Uso del VU para ajustar el gain staging por elemento/procesador: pertenece a Eje 2.
- Ley de panorama y suma coherente como fundamento del paneo: pertenece a Eje 5.
- Anécdotas, ejemplos personales o formulaciones orales del autor fuente.
- Recomendaciones de plugins específicos vinculadas al curso fuente.

### Etiquetado por eje
`eje:1` para todo el contenido de esta unidad.

### Etiquetado por bloque interno
`bloque:1A` — medición de nivel.
`bloque:1B` — fase y polaridad.
`bloque:1C` — análisis espectral e imagen estéreo.

### Etiquetado por fase LDOV
- Toda la unidad opera en `LDOV:Leer`. El Eje 1 es íntegramente la fase L del ciclo.
- El diagnóstico que activa el ciclo hacia Eje 2: `LDOV:Leer → trigger Eje 2`.

### Teoría mínima vs ampliación opcional

**Teoría mínima obligatoria (prioridad alta):**
- Función de Peak, VU, RMS: diferencia de balística y uso.
- Calibración AES vs EBU para VU digital.
- LUFS: diferencia entre Integrated y Momentary.
- Polaridad vs fase: distinción operativa.
- Diagnóstico de comb filtering: colapso a mono + firma espectral.
- Goniómetro y correlatómetro: lectura básica de formas y escala.
- Configuración básica del analizador: escala logarítmica + 1/3 octava + Tilt.

**Teoría de precisión útil (prioridad media):**
- Tabla de suma coherente/no coherente por ángulo.
- Fórmula de primera cancelación del comb filtering.
- Compromiso FFT: resolución vs tiempo real.
- Ventanas de análisis: Hanning vs Blackman-Harris.

**Teoría profunda opcional (IA/FAQ/anexo):**
- K-System completo con protocolo de calibración SPL.
- Compensación AES-17 en medidores RMS.
- Tipos de True Peak y algoritmos de medición.
- Detalle matemático de la FFT.
- Osciloscopio como instrumento de lectura de fase.

---

## SECCIÓN 7 — REGLAS PARA GUIONES

### Partes que deben ser demostración

- **Medidores en paralelo:** mostrar en pantalla Peak y VU sobre una misma señal percusiva, en tiempo real. El alumno debe ver que las lecturas son simultáneamente distintas y correctas.
- **Calibración de plugin de modelado:** mostrar el cambio de comportamiento del plugin al recibir señal en el punto de calibración correcto vs incorrecto (AES vs EBU).
- **Polaridad en batería:** sesión real con overheads y bombo. Colapsar a mono antes y después de corregir la polaridad. La diferencia debe ser audible en tiempo real.
- **Comb filtering:** mostrar la firma espectral en el analizador mientras se suman dos micrófonos con desfasaje. La imagen del peine debe verse claramente.
- **Goniómetro en movimiento:** material con imagen estéreo saludable, luego mismo material colapsado a mono, luego una señal con polaridad invertida entre canales para mostrar el contraste de formas.
- **Analizador con y sin Tilt:** la misma mezcla de referencia con y sin Tilt activo, para que el alumno vea por qué el Tilt es necesario para interpretar el balance.

### Partes que pueden ser explicación a cámara

- Distinción Peak vs VU: el concepto de balística. La diferencia de velocidades puede explicarse con texto y gráfico simple.
- Distinción polaridad vs fase: la explicación de por qué "∅ no es lo mismo que desfasaje" puede ser a cámara con apoyo de un gráfico de onda.
- K-System: introducción del concepto y las tres escalas. No requiere demostración extensa; con el gráfico de posición de 0 dB en el techo digital es suficiente.
- Regla 3:1: explicación del principio. La demostración completa puede ir a la capa de apoyo.

### Partes que conviene enseñar con sesión real

- Configuración del analizador paso a paso sobre una mezcla en curso.
- Diagnóstico completo de una sesión de batería: polaridad, comb filtering, lectura del goniómetro, todo en la misma sesión.
- Lectura comparada: cargar una referencia comercial en el analizador junto con el material del alumno.

### Partes que conviene mandar a la capa de apoyo

- Detalle matemático de la FFT: tamaño de bloque, resolución espectral, fórmulas completas.
- Protocolo completo de calibración SPL del K-System.
- Tipos de ventanas de análisis con descripción técnica extendida.
- Compensación AES-17 en medidores RMS.
- Osciloscopio como instrumento de lectura (mención en curso; desarrollo en apoyo).

---

## SECCIÓN 8 — CAPA DE APOYO POR IA

### Temas que conviene dejar listos para profundización vía IA

- Cálculo del comb filtering a partir de una diferencia temporal conocida: el alumno introduce Δt y la IA calcula las frecuencias canceladas.
- Comparación de medidores RMS con distintos tiempos de integración.
- Protocolo paso a paso de calibración del K-System con medidor SPL.
- Diferencia técnica entre LKFS e LUFS y su historia normativa.
- Tipos de True Peak y por qué ocurren los picos entre muestras.
- Funcionamiento matemático de la FFT para quien quiera profundizar.
- Tipos de ventanas de análisis: descripción extendida de Hanning, Hamming, Blackman-Harris, Flat-top.
- Diferencias entre distintos tipos de osciloscopio para lectura de fase.

### Ejemplos de preguntas que el alumno podría hacerle a la IA

- "¿Cuáles son las frecuencias canceladas si hay una diferencia temporal de 3 ms entre dos micrófonos?"
- "¿Por qué el VU tiene una balística de retorno lenta? ¿Cuál es el fundamento de esa decisión de diseño?"
- "Explícame el K-System de Bob Katz con más detalle: ¿cómo se calibra correctamente?"
- "¿Cuándo tiene sentido usar True Peak en lugar de Peak estándar?"
- "¿Qué diferencia hay en práctica entre usar una ventana Hanning y una Blackman-Harris para analizar una mezcla?"
- "Mi correlatómetro promedia alrededor de 0,3 durante el estribillo. ¿Es problemático?"
- "¿Cómo puedo comparar el LUFS integrado de mi mezcla con el target de Spotify?"
- "Mi goniómetro muestra un óvalo inclinado hacia la derecha. ¿Qué puede estar causándolo?"

---

## SECCIÓN 9 — BLOQUES QUE REQUIEREN ATRIBUCIÓN EXPLÍCITA

### K-System
**Obligación:** el K-System fue diseñado por Bob Katz. Si se presenta el sistema con sus tres escalas (K-20, K-14, K-12) y su metodología de calibración a 85 dBSPL en ponderación C, la atribución es obligatoria.

**Formulación sugerida para el curso:**
> "El K-System fue desarrollado por Bob Katz como sistema de medición de sonoridad calibrada. Las tres escalas —K-20, K-14 y K-12— establecen un punto de referencia de trabajo en relación con el headroom disponible y el tipo de material."

La atribución debe aparecer en el cuerpo del curso en el momento en que se presenta el sistema, no solo al final del módulo ni en un agradecimiento genérico.

### LUFS / EBU R128 / ITU-R BS.1770
No requiere atribución al autor fuente. Citar como normativa publicada:
> "Según EBU R128 / ITU-R BS.1770"

### Tabla de suma coherente/no coherente
El contenido técnico es de dominio general. Si se usa la tabla en la formulación específica del autor fuente, requiere atribución y reformulación. La tabla presentada en este dossier es una reformulación propia de los datos técnicos y no requiere atribución.

---

## SECCIÓN 10 — CONTINUIDAD CON OTROS EJES

**De dónde viene este eje**
El Eje 1 viene del **Eje 0 — Campo de decisión**.

El cruce es directo: los instrumentos de lectura del Eje 1 (medidores, analizador, goniómetro, correlatómetro) operan sobre la cadena calibrada que establece el Eje 0. Los valores de calibración AES/EBU y el principio de gain staging ya deben conocerse de Eje 0-B antes de interpretar las lecturas del Eje 1. Sin esa base, el VU del plugin no dice nada: no hay referencia para interpretarlo.

**A qué eje prepara**
El Eje 1 prepara directamente al **Eje 2 — Integridad de la señal**.

El cruce funciona así:
- El Eje 1 diagnostica los problemas que requieren corrección antes de procesar.
- El Eje 2 opera esos diagnósticos: corrige la polaridad, alinea temporalmente las señales, resuelve el desfasaje, aplica el gain staging por elemento.

Cada diagnóstico del Eje 1 activa una acción específica del Eje 2:

| Diagnóstico (Eje 1) | Corrección (Eje 2) |
|---|---|
| Inversión de polaridad | Botón ∅ en el micrófono correcto |
| Comb filtering entre micrófonos | Alineación temporal / rotor de fase |
| Desfasaje entre señales | Alineación temporal / rotor de fase |
| Nivel de trabajo incorrecto en plugin | Gain staging por elemento |

**Nota de transición para el alumno**
El Eje 1 no toca nada. Solo diagnostica. Si durante el Eje 1 se detecta un problema, se registra, se cuantifica y se describe. La intervención ocurre en el Eje 2. La razón de ese orden: mezclar con un diagnóstico claro es radicalmente más eficiente que intervenir a ciegas y corregir sobre la marcha.

---

*KENTH Academy — Eje 1 · Versión de producción v1.0*
*Generado desde arquitectura congelada v1.0-final y paquete limpio Eje 1.*
