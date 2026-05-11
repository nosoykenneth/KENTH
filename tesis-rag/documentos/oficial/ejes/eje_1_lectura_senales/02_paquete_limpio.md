---
axis_id: "Eje 1"
axis_number: 1
axis_title: "Eje 1 - Lectura de señales"
doc_layer: "limpio"
doc_type: "operacion_practica"
source_origin: "course"
status: "ready_for_indexing"
language: "es"
allowed_for_indexing: true
---

# EJE 1 — LECTURA DE SEÑALES
## Extracción Forense KENTH Academy

---

## 1. COBERTURA DEL EJE

**Fuentes que lo alimentan directamente:**

| Fuente | Contenido relevante para Eje 1 |
|---|---|
| Clases 7–11 (Mezcla) | Medición de nivel, VU, RMS, Peak, K-System, LUFS, polaridad, fase, goniómetro, correlatómetro, comb filtering, análisis espectral, configuración de analizador |
| PDF: Medidores de Nivel | Taxonomía de medidores: PPM, VU, RMS, K-System, LUFS |
| PDF: Vúmetros | Calibración VU, estándares AES/EBU, lectura en señales complejas |
| PDF: Apunte Análisis Espectral | FFT, escalas lineal/logarítmica, división por octava, configuración del analizador |
| PDF: Apunte Fase y Comb Filtering | Fase en grados, productos de suma y resta, comb filtering, regla 3:1 |
| PDF: Apunte Suma Coherente y no Coherente | Tabla de resultados según diferencia de nivel y coherencia de señales |
| Temario fuente (Módulos IX, X, XI) | Polaridad, fase/comb filtering, análisis espectral — bloques del curso fuente |

**Partes dislocadas desde otros bloques del curso fuente:**

El temario fuente agrupa en Módulo VII a los medidores de nivel **junto** al Gain Stage. En KENTH esa agrupación se rompe: los medidores van a Eje 1 y el gain staging a Ejes 0-B y 2. El docente también introduce análisis espectral (Módulo XI) **después** de filtros en el curso fuente; en KENTH, el análisis espectral entra antes de cualquier operación porque es herramienta de lectura. Hay también contenido de calibración de VU en plugins de modelado analógico que en el curso fuente forma parte de la práctica de gain staging; en KENTH esa calibración es parte de Eje 1 (lectura) pero el uso operativo del VU para controlar gain staging es Eje 2.

---

## 2. MATRIZ NEUTRA DEL EJE

### BLOQUE A — MEDICIÓN DE NIVEL

| # | Tema | Subtema | Concepto técnico | Definición neutra | Fórmula / Relación | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|---|
| 1A-01 | Medidor Peak (PPM) | Balística | Medidor de pico instantáneo | Rastrea el nivel máximo instantáneo de la señal. Velocidad de subida casi instantánea. Detecta transitorios que superan umbrales de clipping | — | Usar para detectar clipping y proteger la cadena de conversión D/A y la exportación | Un retensor de picos (hold) captura el valor máximo alcanzado y lo muestra en valor numérico exacto | Asumir que el peak medidor muestra el nivel promedio percibido de la señal | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1A-02 | Medidor VU | Integración | VU: integración de 300 ms | El VU promedia la señal con una constante de integración de ~300 ms y una balística de retorno demorada deliberadamente. No captura transitorios cortos; se aproxima a la percepción auditiva de nivel sostenido | — | Calibración estándar: 0 VU = +4 dBu (profesional) / –10 dBV (semiprofesional). En digital: 0 VU = –20 dBFS (AES) o –18 dBFS (EBU) | En una señal percusiva, el VU puede mostrar –2 dBVU mientras el pico real llega a –6 dBFS; el medidor de picos completará la lectura | Usar el VU como único medidor en señales con transitorios fuertes (batería, percusión) | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1A-03 | Medidor VU | Calibración en modelado analógico | Calibración de plugins de modelado | Los plugins de modelado analógico tienen un punto de trabajo óptimo que depende del nivel de entrada al plugin. Ese punto se establece según el estándar que el plugin emula (AES o EBU). El medidor VU del plugin indica el nivel relativo a esa referencia | AES: +4 dBu = 0 VU = –20 dBFS · EBU: 0 dBu = 0 VU = –18 dBFS | Verificar qué estándar usa el plugin antes de calibrar el nivel de entrada. La balística del VU del plugin también puede variar respecto al estándar analógico original | Si el nivel de entrada al plugin es muy diferente al punto de calibración, el modelado no opera como fue diseñado | Calibrar todos los plugins VU al mismo estándar sin verificar cuál implementa cada uno | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1A-04 | Medidor RMS | Compensación AES-17 | RMS y compensación AES-17 | El medidor RMS calcula la raíz cuadrática media de la señal en un ventana temporal. La compensación AES-17 define cómo se mide el nivel RMS de señales con tono de prueba, estableciendo una corrección de 3 dB para alinear la lectura de señales senoidales con la de señales de ruido | RMS = √(media de los cuadrados de las muestras en la ventana) | Comparar niveles RMS entre fuentes distintas exige que ambas mediciones usen el mismo tiempo de integración y la misma compensación | El RMS da mejor idea del peso perceptual de una señal sostenida que el Peak; el Peak protege contra clipping | Comparar RMS de plugins con distintos tiempos de integración como si fueran equivalentes | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1A-05 | K-System | Calibración de nivel | Sistema K (Bob Katz) | Sistema de medición de sonoridad que establece tres escalas RMS calibradas a 85 dBSPL (ponderación C) en el punto de escucha. El valor 0 dB del calibre se posiciona a distinta distancia del techo digital según el tipo de material | K-20: 0 dB = –20 dBFS (amplio rango dinámico: teatro, orquesta) · K-14: 0 dB = –14 dBFS (producción de alta fidelidad: pop, rock) · K-12: 0 dB = –12 dBFS (material de difusión: broadcast) | Elegir la escala K según el destino y el rango dinámico esperado del material | K-20 deja el mayor headroom; K-12 trabaja más cerca del techo y es adecuado para material ya comprimido para broadcast | Usar K-14 para todo sin considerar el destino ni el rango dinámico del material | MÉTODO O CONTENIDO ATRIBUIBLE | USAR CON ATRIBUCIÓN |
| 1A-06 | LUFS / LKFS | Sonoridad integrada | Medición de sonoridad integrada | LUFS (Loudness Units Full Scale) / LKFS son equivalentes: miden la sonoridad ponderada según la sensibilidad frecuencial del oído (ponderación K), integrada en el tiempo. Es el estándar de entrega para plataformas de streaming y broadcast (ITU-R BS.1770 / EBU R128) | LUFS ≈ LKFS = 1 LU. Tipos: Momentary (400 ms), Short-Term (1–3 s), Integrated (programa completo) · True Peak: picos entre muestras, medidos en dBTP | El LUFS integrado determina si el material cumple el target de la plataforma de destino. El True Peak protege contra artefactos en la reconversión a MP3/AAC | Un material muy comprimido puede tener LUFS integrado alto aunque los peaks sean moderados | Usar solo la lectura Momentary como referencia de nivel de mezcla (mide sonoridad puntual, no global) | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1A-07 | Suma de señales | Coherencia | Suma coherente vs no coherente | Señales coherentes (misma fuente): su suma depende de la relación de fase. Señales no coherentes (fuentes distintas): la suma es de potencias (+3 dB máximo si niveles iguales). La suma coherente puede llegar a +6 dB o cancelación total según la fase | Coherente, Δnivel = 0 dB: 0° → +6 dB / 90° → +3 dB / 120° → ~0 dB / 180° → cancelación · No coherente, Δnivel = 0 dB: +3 dB siempre | Diagnosticar si la suma de dos señales produce un resultado esperado: si la ganancia es mayor de +3 dB, hay coherencia y relación de fase favorable; si hay pérdida, hay problema de fase | Una suma que da +6 dB señala señales idénticas y en fase; una suma que da +3 dB o menos con señales similares sugiere desfasaje o incoherencia | Aplicar la regla de suma de potencias (+3 dB) a señales coherentes | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE B — DIAGNÓSTICO DE FASE Y POLARIDAD

| # | Tema | Subtema | Concepto técnico | Definición neutra | Fórmula / Relación | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|---|
| 1B-01 | Polaridad | Definición | Polaridad vs fase | La inversión de polaridad invierte el signo de toda la señal: positivos pasan a negativos y viceversa. Es binaria (normal / invertida). No es equivalente a un desfasaje de 180°: la polaridad afecta toda la señal por igual en todas las frecuencias; un desfasaje de 180° varía según la frecuencia | — | El botón rotulado "∅" en consolas y plugins habitualmente invierte polaridad, no fase. Distinguir el fenómeno antes de diagnosticar | Una inversión de polaridad en una señal mono no modifica la percepción de timbre al escucharla sola; el problema surge al sumarla con otra señal | Llamar "inversión de fase" a la inversión de polaridad y confundir el diagnóstico y la corrección | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1B-02 | Polaridad | Suma en mono | Efecto de la inversión de polaridad al sumar | Dos señales idénticas con polaridad opuesta se cancelan completamente al sumarse en mono. El diagnóstico consiste en sumar en mono y escuchar si la señal desaparece o reduce significativamente | Suma de voltajes iguales y opuestos = 0 | Chequear polaridad antes de cualquier otro procesamiento. Siempre verificar en mono cuando haya más de una señal captando la misma fuente | Si en mono desaparece casi toda la señal, hay inversión de polaridad. Si en mono se pierde solo una zona frecuencial, hay desfasaje | Invertir la polaridad de la señal incorrecta sin verificar primero qué señal es la de referencia | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1B-03 | Polaridad | Problemas en estéreo | Inversión de polaridad entre L y R | Si un canal de una señal estéreo tiene polaridad invertida respecto al otro: (1) el bajo pierde nivel al colapsar a mono porque las frecuencias graves son prácticamente omnidireccionales y ambos canales se cancelan; (2) la imagen pierde localización y se percibe como artificialmente ancha o incómoda | — | Diagnóstico: colapsar a mono y escuchar pérdida de graves; usar goniómetro (imagen horizontal extrema) | Una mezcla con inversión de polaridad entre L/R puede sonar con imagen amplia en estéreo pero perder completamente los graves al reproducirse en mono | Asumir que la imagen "ancha" de un goniómetro es siempre imagen estéreo legítima y no es un síntoma de polaridad invertida | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1B-04 | Fase | Medición en grados | Fase angular | La relación de fase entre dos señales se expresa en grados (0°–360°). Un ciclo completo equivale a 360°. Los grados se usan porque la misma diferencia temporal equivale a distintos grados según la frecuencia de la señal | 0° = inicio de ciclo / 90° = cuarto de ciclo / 180° = medio ciclo / 270° = tres cuartos de ciclo | Expresar las relaciones de fase en grados, no en milisegundos, cuando se comparan señales periódicas | La misma diferencia temporal de 5 ms produce 180° de desfasaje en 100 Hz pero 360° (suma) en 200 Hz; por eso el comb filtering cancela unas frecuencias y suma otras | Expresar todos los desfasajes en milisegundos y perder la relación con la frecuencia afectada | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1B-05 | Fase | Productos de suma | Resultados según ángulo de fase | Dos señales idénticas con distintas relaciones de fase producen resultados predecibles al sumarse | 0° → +6 dB (suma máxima) · 45° → +5,3 dB · 90° → +3 dB · 120° → ~0 dB (sin suma apreciable) · 180° → cancelación (si amplitudes iguales) | Usar estas referencias para interpretar la lectura del correlatómetro y el goniómetro | En 90° todavía hay suma útil (+3 dB); el problema no es 90° en sí mismo sino que si el promedio está en 90°, los picos llevarán la señal a 120° y más, donde ya hay pérdida real | Interpretar 90° como "zona segura" porque todavía hay +3 dB | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1B-06 | Fase | Goniómetro | Lectura del goniómetro | Visualiza la relación de fase entre L y R en un sistema de ejes rotados 45°. La forma geométrica indica el estado de la imagen estéreo y la relación de fase | Línea vertical = 0° / mono al centro · Óvalo vertical = imagen estéreo saludable · Círculo ≈ 90° · Óvalo horizontal > 90° · Línea horizontal ≈ 180° / cancelación | Colocar el goniómetro en la salida estéreo. Una inclinación lateral indica paneo; un aplanamiento horizontal indica riesgo de cancelación | El goniómetro muestra la imagen estéreo y la relación de fase simultáneamente; una imagen muy abierta puede ser legítima o indicar inversión de polaridad | Interpretar el óvalo ancho siempre como imagen estéreo sin verificar si hay inversión de polaridad | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1B-07 | Fase | Correlatómetro | Lectura del correlatómetro | Mide el coeficiente de correlación entre los canales L y R. Escala de +1 a –1 | +1 = 0° (señales idénticas, máxima correlación) · 0 = 90° (sin correlación) · –1 = 180° (señales opuestas) | El promedio de la lectura importa más que los picos instantáneos. Una lectura de promedio por encima de ~45° indica riesgo de problemas al colapsar a mono | El correlator entra en zona roja alrededor de 90°; eso es una advertencia de umbral, no una declaración de catástrofe | Tomar la lectura instantánea del correlatómetro como referencia del estado general de la mezcla | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1B-08 | Comb filtering | Definición | Filtro peine por diferencia temporal | Cuando dos señales coherentes arriban con diferencia temporal, se producen sumas y cancelaciones alternadas a lo largo del espectro según la relación entre la diferencia de tiempo y los períodos de cada frecuencia. El patrón resultante en el analizador espectral tiene aspecto de "peine" | Frecuencia de primera cancelación: f₁ = 1 / (2 × Δt) donde Δt es la diferencia temporal en segundos. Las siguientes cancelaciones ocurren en múltiplos impares de f₁ | Identificar comb filtering por su firma espectral característica (cancelaciones periódicas equidistantes en frecuencia) o por la degradación del timbre cuando se escucha en mono | Entre 1 y ~20 ms el comb filtering produce coloración tímbrica identificable (robótico, metálico, parecido a flanger/chorus). Por encima de ese rango las señales empiezan a percibirse separadas (eco) | Confundir la coloración tímbrica del comb filtering con problemas de EQ y aplicar ecualización en lugar de alineación temporal | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1B-09 | Comb filtering | Condición de cancelación | Cancelación total vs parcial | La cancelación total solo ocurre cuando las amplitudes de las dos señales son idénticas. Si hay diferencia de nivel entre ambas señales, habrá reducción pero no cancelación absoluta | Cancelación total: A = B y desfasaje = 180° · Cancelación parcial: A ≠ B | Para que el comb filtering sea grave, las señales deben tener niveles similares. La regla 3:1 en microfonía aumenta la diferencia de nivel lo suficiente para minimizar el efecto | Dos micrófonos a más de 3× su distancia mutua respecto a la fuente generan >9,5 dB de diferencia de nivel, reduciendo el comb filtering a niveles mínimos | Creer que cualquier diferencia temporal entre micrófonos produce cancelación total | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1B-10 | Comb filtering | Diagnóstico | Detección en analizador espectral | El comb filtering se visualiza en el analizador como cancelaciones periódicas equidistantes. La frecuencia de la primera cancelación indica la diferencia temporal. Colapsando a mono se hace visible en la señal cuando en estéreo permanecía oculto | f_1ª cancelación = 1 / (2 × Δt) | Colapsar a mono para revelar comb filtering que en estéreo no es audible porque los canales no se suman | Una mezcla con overheads de batería puede sonar normal en estéreo pero mostrar severo comb filtering al colapsar a mono | No revisar en mono señales grabadas con múltiples micrófonos sobre la misma fuente | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE C — ANÁLISIS ESPECTRAL

| # | Tema | Subtema | Concepto técnico | Definición neutra | Fórmula / Relación | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|---|
| 1C-01 | Analizador | Escalas | Escala lineal vs logarítmica | Escala lineal: frecuencias distribuidas linealmente; mayor detalle en altas frecuencias, menor en graves. Escala logarítmica: frecuencias distribuidas por décadas; refleja mejor la percepción auditiva, con mayor detalle en graves | — | Usar escala logarítmica para análisis de balance tonal general (refleja mejor la percepción). Usar escala lineal para inspeccionar problemas de alta frecuencia con precisión | El analizador FFT logarítmico muestra lo que se parece más a lo que se escucha; el lineal muestra lo que físicamente está pasando en alta frecuencia | Analizar problemas de graves con escala lineal y perder detalle precisamente en la zona donde hay más energía | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1C-02 | Analizador | División por octava | Análisis en 1/3 de octava | El análisis por división de octava (1/1, 1/3, 1/12 de octava) muestra el balance espectral promediado por bandas perceptualmente relevantes, no la energía por Hz individual. Es más estable visualmente y más cercano a la percepción de balance tonal | — | Usar el análisis por 1/3 de octava para evaluar el balance global de una mezcla; usar FFT para detectar problemas específicos de frecuencia | 1/3 de octava muestra si la mezcla tiene tendencia cálida, neutral o brillante con un golpe de vista; la FFT detalla qué frecuencias exactas son problemáticas | Tomar el espectro FFT de una mezcla compleja como representación fiel de lo que se escucha | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1C-03 | Analizador | FFT | Compromiso FFT: resolución vs tiempo real | El tamaño de bloque FFT define la resolución espectral y el tiempo necesario para calcularla. Ambos parámetros están en relación inversa | Resolución espectral = SR / FFT (Hz/barra) · Duración del bloque = FFT / SR (segundos) · FFT alta → más resolución, menos tiempo real · FFT baja → menos resolución, más tiempo real | FFT de ~8192 puntos: equilibrio útil para análisis general de mezcla. Para detectar problemas de muy baja frecuencia, aumentar FFT. Para seguimiento dinámico rápido, reducir FFT | Una FFT baja produce anchos de banda de barra tan grandes que ocultan problemas reales; un "error de resolución de analizador" no es un problema del audio | Confundir anomalías de representación del analizador (error de resolución de FFT) con problemas reales en la señal | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1C-04 | Analizador | Tilt | Compensación de pendiente (Tilt) | Ajuste que aplica una pendiente al eje de amplitud del analizador para compensar la diferencia de energía percibida entre graves y agudos. Un tilt de ~3 dB/octava compensa la distribución natural del espectro musical hacia los graves | — | Activar el Tilt para comparar el balance espectral de una mezcla con referencias comerciales en la misma escala | Sin Tilt, una mezcla bien balanceada puede parecer sobredimensionada en graves por la distribución natural del espectro | Interpretar el analizador sin Tilt como representación fiel del balance percibido | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1C-05 | Analizador | Ventanas | Ventana Hanning (compromiso general) | La ventana Hanning reduce la fuga espectral alrededor de los picos, pero puede enmascarar componentes débiles muy próximos a una frecuencia dominante | — | Usar como ventana por defecto para la mayoría de los análisis de mezcla | Para trabajo general es suficiente; no es la mejor para detectar componentes de bajo nivel cerca de una frecuencia dominante | Mantener siempre la misma ventana sin considerar si el objetivo es análisis general o detección de artefactos de bajo nivel | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1C-06 | Analizador | Ventanas | Ventana Blackman-Harris / Alta resolución | Estas ventanas reducen aún más el enmascaramiento a niveles bajos cerca de frecuencias dominantes, a costa de una representación más ancha del pico principal. Permiten detectar distorsión de bajo nivel, batimentos y artefactos próximos a una frecuencia fuerte | — | Usar Blackman-Harris o High Resolution para investigar productos de distorsión, batimentos o componentes débiles muy cercanos a frecuencias fuertes | La V corta en el analizador (depresión estrecha junto a un pico) suele indicar señal espuria de bajo nivel; la ventana adecuada la hace visible | Usar High Resolution para análisis de mezcla general y leer como errática una imagen más ancha en los picos | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1C-07 | Analizador | Overlap / Average Time | Configuración de visualización | Overlap: fundido entre bloques de análisis consecutivos, suaviza la visualización sin modificar la resolución real. Average Time: tiempo durante el cual el analizador promedia o retiene la lectura; valores altos muestran la tendencia tonal; valores bajos muestran la señal instantánea | — | Combinar un Average Time suficiente para leer tendencia con un Overlap moderado para fluidez visual; usar Average Time corto solo cuando se quiera ver comportamiento dinámico rápido | El Field Display (relleno visual de las barras hacia abajo) no aporta información útil; desactivarlo reduce carga gráfica sin perder datos | Leer el Field Display como dato relevante sobre la estructura espectral | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 1C-08 | Analizador | Usos prácticos | Aplicaciones diagnósticas del analizador | El analizador espectral revela: problemas de ruido a muy baja frecuencia (infra), contenido armónico de instrumentos, sibilancias, enmascaramiento entre instrumentos, alias de plugins, balance tonal global | — | Insertar el analizador en el bus de salida para lectura global; en solo de cada canal para diagnóstico individual. Para detectar problemas subsónicos, extender el rango hasta –144 dB | Los monitores no reproducen contenido por debajo de su límite de extensión; el analizador puede detectar energía invisible para el oído y el sistema de monitoreo | Depender exclusivamente de los monitores para diagnosticar el espectro completo de la señal | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

## 3. CONTENIDO ATRIBUIBLE DEL EJE

| Bloque | Atribución requerida | Etiqueta recomendada |
|---|---|---|
| K-System (K-20 / K-14 / K-12) | Diseñado por Bob Katz. Autoría explícita del sistema y la calibración a 85 dBSPL en ponderación C | "Sistema K (Bob Katz)" — citar autor al introducir el sistema |
| Estándares LUFS / EBU R128 / ITU-R BS.1770 | Normativa pública (EBU, ITU); no requiere atribución al autor fuente | "Según EBU R128 / ITU-R BS.1770" |
| PDFs de Medidores de Nivel, Análisis Espectral, Fase y Comb Filtering, Suma Coherente y no Coherente | Autoría: Pablo Rabinovich. Si se cita cualquier formulación de esos documentos, requiere atribución. La doctrina técnica contenida en ellos (FFT, polaridad, fase, comb filter) es de dominio general y no requiere atribución cuando se reformula | "Según [Rabinovich, material de referencia]" solo si se cita la formulación |
| Tabla de resultados de suma coherente / no coherente (Apunte Suma Coherente) | Autoría: Pablo Rabinovich. La tabla en sí es una forma de presentación específica; los valores técnicos son de dominio general | Citar la tabla si se usa directamente; reformular si se presenta como doctrina propia |
| "V corta en el analizador" como indicador de señal espuria | Observación práctica descrita en clase como hallazgo de oficio del docente, documentado también en publicación de un exalumno | USAR CON ATRIBUCIÓN si se menciona como criterio diagnóstico específico |

---

## 4. BLOQUEOS DEL EJE

| Bloque bloqueado | Tipo de riesgo | Por qué no debe pasar |
|---|---|---|
| Anécdota del docente sobre Cerati y el jurado del Clarín (años 90) | EXPRESIÓN NO REUTILIZABLE | Historia personal identificable del autor fuente |
| Anécdota de Eagles / Wish You Were Here / Mozart como ejemplos en clase | EXPRESIÓN NO REUTILIZABLE | Ejemplos anclados a la secuencia de clase del autor fuente; identificables |
| Referencia a "Correlometer de Voxengo" como herramienta recomendada | EXPRESIÓN NO REUTILIZABLE | Recomendación específica de herramienta con nombre ligada al flujo del curso fuente; no es doctrina general |
| Formulaciones orales: "el enemigo público número uno del audio", "sonido robótico", "suena como cuando grabás con latencia" | EXPRESIÓN NO REUTILIZABLE | Frases y analogías del autor fuente; tono oral marcado |
| Orden de introducción de temas en el curso fuente: nivel → polaridad → fase → espectral (Módulos VII→IX→X→XI) | ESTRUCTURA NO REUTILIZABLE | Secuencia pedagógica del curso fuente reconocible |
| Referencia al libro del exalumno donde quedó documentada la observación de la "V corta" | EXPRESIÓN NO REUTILIZABLE | Relato situado en la biografía del autor fuente; identificable |
| Descripción del correlator como "parece un VU meter pero…" | EXPRESIÓN NO REUTILIZABLE | Formulación oral muy distintiva del docente fuente |

---

## 5. VACÍOS Y TENSIONES DEL EJE

| Tipo | Descripción | Implicación para redacción |
|---|---|---|
| **Vacío** | No hay cobertura explícita de lectura comparada con referencias comerciales como práctica sistemática. Las fuentes muestran referencias puntuales en clases de training (Clases 21–24), pero no un método estructurado para leer referencias en el contexto de Eje 1 | Al redactar: construir el criterio operativo de lectura comparada desde cero o desde fuentes externas de referencia profesional |
| **Vacío** | El osciloscopio se menciona como herramienta de lectura de fase junto al goniómetro y el correlatómetro, pero no tiene desarrollo técnico propio en las fuentes. Solo aparece como enumeración | Al redactar: o desarrollar el osciloscopio como instrumento de lectura con fuentes externas, o reducir su presencia a una mención en el contexto de las otras herramientas |
| **Tensión de límite** | El comb filtering se describe tanto como fenómeno diagnóstico (Eje 1) como problema que se corrige mediante alineación temporal (Eje 2). En las fuentes ambas cosas aparecen en las mismas sesiones | Al redactar: Eje 1 solo diagnostica el comb filtering y lo mide; el tratamiento (alineación, inversión de polaridad correctora) pertenece íntegramente a Eje 2 |
| **Tensión de límite** | El VU en plugins de modelado es tanto herramienta de lectura (Eje 1) como herramienta de control del gain staging por elemento (Eje 2). La línea entre "leer" y "calibrar para operar" puede confundirse | Al redactar: en Eje 1 el VU describe el nivel; en Eje 2 el VU se usa para ajustar el input de cada procesador a su punto de trabajo |
| **Tensión de límite** | La suma coherente y no coherente de señales cubre tanto el diagnóstico de polaridad/fase (Eje 1) como el fundamento de la ley de panorama (pre-Eje 5). Al redactar Eje 1 habrá que establecer hasta dónde llega la aplicación a lectura sin entrar en la lógica de paneo | Marcar el cruce explícitamente al alumno: la suma coherente en Eje 1 explica diagnóstico; la ley de panorama se retoma en Eje 5 |
| **Cruce activo con Eje 0** | Los instrumentos de Eje 1 operan sobre la cadena calibrada en Eje 0. Sin cadena calibrada (gain staging, referencia de nivel AES/EBU), las lecturas de VU y LUFS del Eje 1 carecen de contexto | Declarar explícitamente el cruce en la transición Eje 0 → Eje 1 al redactar |
| **Cruce activo con Eje 2** | El diagnóstico de comb filtering, polaridad invertida y problemas de fase activa directamente las correcciones del Eje 2. El alumno debe entender que el Eje 1 termina en el diagnóstico; la acción es del siguiente eje | Cierre explícito del Eje 1 apuntando al Eje 2 como destino del diagnóstico |

---

## 6. PAQUETE LIMPIO DEL EJE

### EJE 1 — LECTURA DE SEÑALES · Paquete limpio para proyecto generativo

---

**FUNCIÓN DEL EJE:** Primer paso del ciclo LDOV. Lee lo que hay antes de intervenir. Sin lectura previa toda operación es sobre supuestos. El Eje 1 solo diagnostica; no corrige.

---

#### BLOQUE A — MEDICIÓN DE NIVEL

**Doctrina reutilizable:**
- Peak (PPM): velocidad instantánea; detecta clipping y protege conversión. El retensor captura el máximo numérico exacto
- VU: integración ~300 ms; balística lenta deliberada; se aproxima al nivel percibido. No captura transitorios cortos
- Calibración VU estándar: 0 VU = +4 dBu (profesional) / –10 dBV (semipro). En digital: 0 VU = –20 dBFS (AES) o –18 dBFS (EBU)
- Calibración de plugins de modelado analógico: el plugin tiene un punto de trabajo óptimo; verificar qué estándar implementa antes de calibrar el nivel de entrada
- RMS: promedio cuadrático en una ventana temporal; indica el peso sostenido de la señal. La compensación AES-17 define cómo medir señales de prueba senoidales
- K-System (Bob Katz): tres escalas RMS calibradas a 85 dBSPL en ponderación C. K-20 (–20 dBFS): amplio rango dinámico. K-14 (–14 dBFS): pop/rock de alta fidelidad. K-12 (–12 dBFS): broadcast
- LUFS/LKFS: medición de sonoridad integrada ponderada por sensibilidad frecuencial del oído. Tres vistas: Momentary (400 ms), Short-Term (~1-3 s), Integrated (programa completo). True Peak: picos entre muestras en dBTP
- Suma coherente: depende de la relación de fase. 0° → +6 dB; 90° → +3 dB; 120° → ~0 dB; 180° → cancelación (si amplitudes iguales). Suma no coherente: siempre +3 dB máximo si niveles iguales

**Heurísticas reformulables:**
- Ningún medidor único es suficiente: Peak protege contra clipping; VU/RMS informa sobre nivel sostenido percibido; LUFS informa sobre el destino de entrega
- Una señal percusiva puede mostrar –2 dBVU mientras su peak llega a –6 dBFS: ambas lecturas son correctas y distintas
- Comparar lecturas RMS solo entre medidores con el mismo tiempo de integración

**Atribuciones:**
- K-System: Bob Katz
- LUFS / EBU R128: normativa EBU / ITU-R BS.1770

**Advertencias:**
- LÍMITE: el uso del VU para controlar el nivel de entrada de procesadores individuales pertenece a Eje 2. En Eje 1 el VU solo describe el nivel de la señal
- CRUCE → EJE 0: los valores de calibración AES/EBU ya deben conocerse de Eje 0-B

**Bloqueos:** secuencia pedagógica del temario fuente para este bloque; ejemplos personales del docente; formulaciones orales del autor fuente

---

#### BLOQUE B — DIAGNÓSTICO DE FASE Y POLARIDAD

**Doctrina reutilizable:**
- Polaridad: binaria. Invierte el signo de toda la señal por igual en todas las frecuencias. El botón "∅" habitualmente invierte polaridad, no fase
- Inversión de polaridad en mono: cancelación total si las señales son idénticas
- Inversión de polaridad en estéreo (entre L y R): pérdida de graves al colapsar a mono + imagen desestabilizada y percepción incómoda o extraña al oyente
- Fase: desplazamiento temporal expresado en grados. La misma diferencia temporal produce distintos grados según la frecuencia. 0° = inicio de ciclo; 90° = cuarto; 180° = medio ciclo
- Resultados de suma por ángulo de fase: 0° → +6 dB / 45° → +5,3 dB / 90° → +3 dB / 120° → ~0 dB / 180° → cancelación (si amplitudes iguales)
- Goniómetro: representa la relación de fase L/R. Línea vertical = mono/0°. Óvalo vertical = imagen estéreo saludable. Círculo ≈ 90°. Línea horizontal ≈ 180°/cancelación
- Correlatómetro: escala de +1 (0°) a –1 (180°). El promedio importa más que los picos instantáneos. El promedio debería sostenerse dentro de aproximadamente 45° para una mezcla con buena monocompatibilidad
- Comb filtering: patrón de cancelaciones y sumas alternadas producido por la suma de una señal con una copia retardada. Primera cancelación en f₁ = 1/(2×Δt); las demás en múltiplos impares. Visible en el analizador como cancelaciones periódicas equidistantes
- La cancelación total en comb filtering requiere amplitudes iguales. Si hay diferencia de nivel entre las señales, la cancelación es parcial
- Regla 3:1: distancia mínima entre dos micrófonos que captan la misma fuente = al menos 3× la distancia micrófono-fuente. Genera >9,5 dB de diferencia de nivel, reduciendo el comb filtering a niveles mínimos

**Heurísticas reformulables:**
- Diagnóstico de polaridad: colapsar a mono. Si desaparece casi todo, hay inversión de polaridad. Si desaparece solo una zona frecuencial, hay desfasaje
- Diagnóstico de comb filtering: buscar la firma de peine en el analizador; confirmar colapsando a mono
- El correlatómetro en 90° no es zona catastrófica: todavía hay +3 dB. El problema es que si el promedio está en 90°, los picos llevan a 120° y más
- Chequeo de monocompatibilidad: colapsar a mono y comparar con la mezcla estéreo. Si no cambia nada, la mezcla era básicamente mono
- Polaridad invertida entre L/R puede sonar "ancha" en estéreo y perder los graves en mono: diagnóstico doble necesario

**Atribuciones:**
- PDFs fuente: Rabinovich (si se cita la formulación directamente)
- Tabla de suma coherente/no coherente: Rabinovich (reformular al reutilizar)

**Advertencias:**
- LÍMITE: el Eje 1 diagnostica comb filtering, polaridad y desfasaje. La corrección (alineación temporal, inversión de polaridad correctora, rotor de fase) pertenece íntegramente a Eje 2
- CRUCE → EJE 5: la suma coherente explicada aquí como fundamento de diagnóstico de fase se retoma en Eje 5 para la ley de panorama
- VACÍO: el osciloscopio aparece mencionado pero sin desarrollo propio en las fuentes. Al redactar, desarrollar desde fuentes externas o reducir a mención contextual

---

#### BLOQUE C — ANÁLISIS ESPECTRAL

**Doctrina reutilizable:**
- Escala lineal: distribución lineal de frecuencias; detalla alta frecuencia; pierde resolución en graves
- Escala logarítmica: distribución por décadas; refleja mejor la percepción auditiva; mejor para análisis de balance tonal general
- Lo que el analizador FFT muestra plano no suena plano: el oído no percibe energía lineal, sino logarítmica por octava
- División por 1/3 de octava: estable, perceptualmente relevante, útil para balance global. FFT: preciso, útil para problemas específicos de frecuencia
- Compromiso FFT: resolución espectral = SR/FFT. Duración del bloque = FFT/SR. Mayor FFT → más resolución, menos tiempo real. ~8192 puntos: equilibrio para mezcla general
- Tilt: compensación de pendiente espectral aplicada al analizador para comparar material en la misma escala perceptual
- Ventana Hanning: compromiso general; puede enmascarar señales débiles junto a frecuencias dominantes
- Ventana Blackman-Harris / Alta resolución: detecta distorsión de bajo nivel y componentes débiles cerca de frecuencias fuertes; sacrifica precisión en el pico principal
- Overlap: suaviza la transición visual entre bloques; no mejora la resolución real
- Average Time: mayor valor → más estabilidad de lectura de tendencia; menor valor → más dinámico e instantáneo
- El Field Display (relleno visual de barras) no aporta información técnica útil; puede desactivarse

**Heurísticas reformulables:**
- Para análisis de balance tonal general: escala logarítmica + Tilt + 1/3 octava + Average Time moderado
- Para detectar problemas subsónicos o de alta frecuencia específicos: FFT alta + escala logarítmica para graves / lineal para agudos
- Para investigar distorsión de bajo nivel o artefactos: cambiar a ventana Blackman-Harris o High Resolution
- Una anomalía en el analizador puede ser un error de resolución de FFT, no un problema real del audio; verificar aumentando el tamaño de bloque

**Advertencias:**
- CRUCE → EJE 0: el análisis espectral requiere la cadena calibrada de Eje 0. Sin calibración, las lecturas no tienen contexto de referencia
- CRUCE → EJE 2: el analizador es la herramienta que confirma el diagnóstico de comb filtering y otros problemas de fase; la acción correctora es Eje 2
- VACÍO: lectura comparada con referencias comerciales como práctica sistemática no está cubierta en las fuentes con suficiente desarrollo operativo; construir desde cero o referenciar fuentes externas (p.ej., Ian Shepherd, Bob Katz)

---

*Paquete listo para ingesta en Proyecto Generativo. Siguiente eje cuando lo indiques.*