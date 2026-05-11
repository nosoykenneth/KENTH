Now let me read the key PDFs for Module 1 content.Now let me check Class 3 briefly for Module 1 boundary.Ya tengo suficiente material de las fuentes primarias. Procedo con la extracción completa del Módulo 1.

---

# EXTRACCIÓN M01 — FUNDAMENTOS FÍSICOS, ACÚSTICA Y MEDICIÓN
**Fuentes procesadas:** Clase 1, Clase 2, Clase 3 (mezcla) + PDFs de referencia del corpus  
**Fecha de extracción:** 07-05-2026

---

## 1. MATRIZ NEUTRA DE CONOCIMIENTO

### BLOQUE 1.1 — Las tres variables fundamentales del audio

| Campo | Contenido |
|---|---|
| Concepto técnico | Nivel, fase y espectro como ejes de medición en audio |
| Definición neutra | Todo parámetro relevante en audio profesional puede reducirse a una de estas tres variables: amplitud (nivel), relación temporal entre señales (fase) y distribución de energía por frecuencia (espectro) |
| Fórmula / relación | No hay fórmula unificada; son categorías clasificatorias |
| Criterio operativo | Cualquier decisión técnica debe poder justificarse en al menos una de estas tres variables. Si no puede ubicarse en ninguna, el criterio es subjetivo |
| Error frecuente | Tratar la ecualización, el paneo o el compresor como herramientas sin vincularlos a la variable que operan |
| Heurística reformulable | Antes de intervenir en la señal, identificar cuál de las tres variables está siendo afectada |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.2 — Ciclo, período y frecuencia en el dominio temporal

| Campo | Contenido |
|---|---|
| Concepto técnico | Período y frecuencia como descriptores del dominio temporal de la onda |
| Definición neutra | El período (T) es el tiempo que tarda en completarse un ciclo. La frecuencia (F) es la cantidad de ciclos por segundo. Son recíprocos |
| Fórmula / relación | F = 1/T · T = 1/F · Unidad: Hz (ciclos/segundo) |
| Criterio operativo | Identificar un ciclo completo en el oscilograma y medir su duración para calcular la frecuencia correspondiente. La amplitud no afecta el cálculo |
| Error frecuente | Describir el período como "lo que dura una frecuencia" en lugar de "lo que dura un ciclo" |
| Heurística reformulable | Una onda es periódica si el período no varía. Si es periódica, tiene frecuencia. La frecuencia depende solo del período, no de la amplitud |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.3 — Ondas simples y ondas complejas

| Campo | Contenido |
|---|---|
| Concepto técnico | Clasificación de ondas según su composición espectral |
| Definición neutra | Una onda simple (senoidal) contiene una única frecuencia. Una onda compleja contiene múltiples frecuencias superpuestas |
| Fórmula / relación | Toda onda compleja es suma de senoidales (Fourier). Si las componentes mantienen relación de múltiplo entero → onda compleja periódica. Si no → onda compleja aperiódica |
| Criterio operativo | Las ondas complejas periódicas corresponden a fuentes de afinación tonal. Las aperiódicas corresponden a fuentes percusivas sin altura tonal definida |
| Error frecuente | Tratar la senoidal como representativa del audio real. En la práctica es el sonido más inusual en la naturaleza |
| Heurística reformulable | Si hay patrón que se repite, hay fundamental. Si no hay patrón repetido, no hay altura tonal |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.4 — Fundamental, parciales armónicos e inarmónicos

| Campo | Contenido |
|---|---|
| Concepto técnico | Estructura armónica de las ondas complejas periódicas |
| Definición neutra | La fundamental es la frecuencia más grave que determina el período de la onda. Los parciales armónicos son múltiplos enteros de la fundamental. Los parciales inarmónicos no mantienen esa relación |
| Fórmula / relación | Armónico n = n × fundamental. Armónicos pares: ×2, ×4, ×6… Armónicos impares: ×3, ×5, ×7… |
| Criterio operativo | La fundamental suele tener la mayor amplitud pero no necesariamente. La relación de amplitudes entre armónicos varía en el tiempo y construye el timbre |
| Error frecuente | Asumir que la fundamental siempre es el componente de mayor amplitud |
| Heurística reformulable | El timbre no depende de qué armónicos están presentes, sino de la relación de amplitudes entre ellos y de cómo varían esas amplitudes en el tiempo |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.5 — Distorsión armónica, color y modelado analógico

| Campo | Contenido |
|---|---|
| Concepto técnico | Distorsión armónica como mecanismo generador de color en equipos analógicos y plugins de modelado |
| Definición neutra | Un procesador digital transparente no altera la composición espectral de la señal. Un procesador analógico (o plugin que lo emule) agrega armónicos a la fundamental original. Eso constituye distorsión armónica |
| Fórmula / relación | Señal de salida = fundamental + serie de armónicos. Color = combinación específica de amplitudes relativas de esos armónicos |
| Criterio operativo | La distorsión armónica par suena más musical (el segundo armónico es la octava). La impar aporta presencia y ataque. Ambas combinadas pueden ser muy favorables. Hay un punto a partir del cual se vuelven indeseables |
| Error frecuente | Agregar distorsión hasta escucharla explícitamente. La regla: debe sentirse, no escucharse |
| Heurística reformulable | Si la distorsión es perceptible como efecto y no como densidad o cuerpo, el nivel está excedido |
| Sensibilidad autoral | Media (criterio de uso específico) |
| Acción | **REFORMULAR MÁS** |

---

### BLOQUE 1.6 — Aliasing y distorsión por intermodulación

| Campo | Contenido |
|---|---|
| Concepto técnico | Dos tipos de distorsión inarmónica relevantes en contexto digital y analógico |
| Definición neutra | El aliasing es una distorsión inarmónica característica del dominio digital, sin equivalente analógico. La intermodulación ocurre cuando la saturación excesiva genera frecuencias sin relación entera con la fundamental |
| Fórmula / relación | Ninguna operativa para contexto de mezcla. Son fenómenos cualitativos identificables por análisis espectral |
| Criterio operativo | Un plugin que produce aliasing no emula comportamiento analógico con fidelidad, independientemente de su calidad sonora subjetiva. La intermodulación produce sonido áspero, chillón y fatigante |
| Error frecuente | Confundir distorsión armónica agradable con intermodulación |
| Heurística reformulable | Si la señal saturada suena agresiva y fatigante, el origen probable es intermodulación, no distorsión armónica |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.7 — Frecuencia vs. tono: dimensión objetiva y subjetiva

| Campo | Contenido |
|---|---|
| Concepto técnico | Distinción entre frecuencia (magnitud física) y tono (percepción subjetiva) |
| Definición neutra | Frecuencia: magnitud objetiva medible en Hz. Tono: respuesta perceptual del oyente a esa frecuencia. La correspondencia no es biunívoca ni universal |
| Fórmula / relación | No hay relación lineal. La percepción tonal varía según amplitud, oyente y momento de escucha |
| Criterio operativo | Por debajo de 100 Hz: aumentar amplitud → percepción de tono más grave (en la mayoría). Por encima de 5000 Hz: aumentar amplitud → percepción de tono más agudo (en todos). Entre 1000–5000 Hz: zona de transición con efecto mínimo |
| Error frecuente | Usar frecuencia y tono como sinónimos. Asumir que todos los oyentes perciben igual |
| Heurística reformulable | No se escucha lo mismo a distinto nivel de monitoreo. La percepción tonal cambia con la amplitud |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.8 — Curvas isofónicas y percepción de nivel

| Campo | Contenido |
|---|---|
| Concepto técnico | Curvas de igual sonoridad (Fletcher-Munson / ISO 226) |
| Definición neutra | Las curvas isofónicas describen cómo la sensibilidad del oído varía con la frecuencia según el nivel de presión sonora. A niveles bajos la sensibilidad en graves y agudos es menor. A niveles altos las curvas se "enderezan" y la respuesta se percibe más uniforme |
| Fórmula / relación | No operativa en este contexto. Las curvas son gráficas de referencia |
| Criterio operativo | Subir el volumen de monitoreo hace que la mezcla "suene mejor" sin que haya mejorado. Esta sensación es artefacto perceptual, no mejora técnica. El nivel de referencia estable es obligatorio para decisiones técnicas confiables |
| Error frecuente | Confundir la mejora perceptual al subir el volumen con una mejora real de la mezcla. Compensar a volumen muy bajo exagerando graves y agudos |
| Heurística reformulable | Si una mezcla suena mejor solo al subir el volumen, el problema puede estar en el monitoreo, no en la mezcla |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.9 — Volumen de monitoreo: referencia, fatiga y criterios de protección

| Campo | Contenido |
|---|---|
| Concepto técnico | Nivel de monitoreo como variable controlable que afecta la calidad de decisión técnica |
| Definición neutra | El volumen de monitoreo es independiente del nivel de señal interno. Un nivel de referencia estable es condición técnica necesaria para mezcla consistente |
| Fórmula / relación | Medición estricta: SPL (dB) con ponderación C, medición lenta. Referencia práctica: nivel donde aún es posible mantener una conversación |
| Criterio operativo | Mezclar a nivel de referencia estable. Chequear fuerte y bajo como verificación adicional, nunca como base de decisión. No mezclar cambiando continuamente el volumen de monitoreo |
| Error frecuente | 1. Mezclar fuerte: produce fatiga, enmascaramiento, distorsión del sistema y del oído. 2. Mezclar bajo: produce compensaciones incorrectas en graves y agudos |
| Heurística reformulable | Un nivel por encima del que permite mantener conversación es un nivel de monitoreo problemático para trabajo de larga duración |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.10 — Fatiga auditiva y daño a células ciliadas

| Campo | Contenido |
|---|---|
| Concepto técnico | Consecuencias fisiológicas del monitoreo a alto nivel |
| Definición neutra | Las células ciliadas de la cóclea son el receptor fisiológico de la señal sonora. No se regeneran. La exposición prolongada a alto nivel produce pérdida progresiva e irreversible, con mayor impacto en altas frecuencias |
| Fórmula / relación | No operativa aquí. Variable relevante: tiempo de exposición × nivel de presión sonora |
| Criterio operativo | La pérdida de sensibilidad en agudos durante la sesión es señal de fatiga activa. Continuar mezclando bajo fatiga auditiva produce decisiones incorrectas de ecualización (sobrestimación de agudos) |
| Error frecuente | Usar auriculares con ruido ambiente elevado (transporte público) sin cancelación: el nivel efectivo es mucho mayor del percibido subjetivamente |
| Heurística reformulable | El nivel útil para mezcla es el más bajo que permita tomar decisiones técnicas precisas, no el más "cómodo" o "envolvente" |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.11 — Dominio espacial de la frecuencia y longitud de onda

| Campo | Contenido |
|---|---|
| Concepto técnico | Relación entre frecuencia, velocidad del sonido y longitud de onda |
| Definición neutra | Una onda sonora tiene una extensión física (longitud de onda) determinada por la relación entre velocidad de propagación y frecuencia. Cuando esa extensión coincide con dimensiones físicas del espacio, se producen interferencias |
| Fórmula / relación | λ = v / f (λ: longitud de onda en metros; v: velocidad del sonido ≈ 343 m/s; f: frecuencia en Hz) |
| Criterio operativo | Ejemplo: distancia entre paredes de 3,43 m → modo de sala prominente en 100 Hz. El rango audible ocupa longitudes de onda de ~17 m (20 Hz) a ~17 mm (20 kHz) |
| Error frecuente | Tratar la frecuencia como fenómeno solo temporal, ignorando sus consecuencias espaciales en el entorno de monitoreo |
| Heurística reformulable | Las dimensiones físicas de la sala siempre coinciden con la longitud de onda de alguna frecuencia. No hay posición neutra |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.12 — Modos de sala, resonancias y tratamiento acústico

| Campo | Contenido |
|---|---|
| Concepto técnico | Modos de sala como consecuencia de interferencias en el dominio espacial |
| Definición neutra | Cuando las dimensiones de una habitación son múltiplos o fracciones de la longitud de onda de una frecuencia, se forman patrones estacionarios (modos). Hay zonas de refuerzo y zonas de cancelación para esa frecuencia |
| Fórmula / relación | F_modo = n × (v / 2L) donde n es el número de modo y L la dimensión relevante |
| Criterio operativo | Los paneles absorbentes actúan sobre reflexiones, no sobre modos. Para frecuencias infladas por modos se requieren resonadores (Helmholtz u otros), no absorción genérica. La solución ideal de muchos problemas de sala requiere intervención especializada |
| Error frecuente | Llenar una sala de paneles absorbentes creyendo que eso resuelve problemas de resonancia de bajas frecuencias |
| Heurística reformulable | Absorción controla reflexiones. Resonadores controlan modos. Son herramientas distintas para problemas distintos |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.13 — Posicionamiento de monitores y consecuencias acústicas

| Campo | Contenido |
|---|---|
| Concepto técnico | Variables de colocación física del monitor y su impacto en la respuesta en frecuencia |
| Definición neutra | La distancia monitor-pared determina qué frecuencias se refuerzan o cancelan por reflexión. No existe posición libre de interferencias |
| Fórmula / relación | Cancelación: distancia = λ/4 de una frecuencia. Refuerzo: distancia = λ/2. Empotrado en pared → elimina interferencias pero suma energía en bajas (compensable por EQ) |
| Criterio operativo | Tweeter a la altura de los oídos. Monitores apuntando al oyente. Orientación (vertical/horizontal) según especificación del fabricante. Desacoplamiento firme de la superficie de apoyo |
| Error frecuente | 1. Monitores apuntando al frente con el oyente al centro → pérdida de agudos percibida → compensación incorrecta de EQ. 2. Desacoplador excesivamente blando → debilitamiento de graves. 3. Ignorar la orientación de fábrica → problema de fase en la frecuencia de cruce |
| Heurística reformulable | Cualquier compensación de EQ que intente corregir un problema de colocación física está aplicando el parche en el lugar equivocado |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.14 — Localización binaural: ITD, ILD y sombra acústica

| Campo | Contenido |
|---|---|
| Concepto técnico | Mecanismos de localización auditiva en el plano horizontal |
| Definición neutra | El sistema auditivo determina el ángulo de incidencia de una fuente sonora a partir de cuatro diferencias entre ambos oídos: tiempo de arribo (ITD), nivel/amplitud (ILD), fase y timbre (sombra acústica de la cabeza) |
| Fórmula / relación | ITD máxima (90°): ≈ 0,5 ms (cabeza ~17 cm). Sombra acústica: afecta frecuencias cuya λ < tamaño de la cabeza (aprox. > 1 kHz). λ rango audible: ~17 m a ~17 mm |
| Criterio operativo | Las cuatro claves binaurales (ITD, ILD, fase, timbre) son los fundamentos físicos sobre los que opera el paneo, la ambiencia y la localización en mezcla |
| Error frecuente | Confundir "no llega a un oído" con cancelación. Los oídos están separados; la cancelación total nunca ocurre binaralmente para una señal en campo abierto |
| Heurística reformulable | El paneo y la ambiencia son operaciones sobre los cuatro parámetros binaurales. Entenderlos permite operar con criterio en lugar de solo por escucha |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.15 — Monitores vs. auriculares: diferencias fundamentales

| Campo | Contenido |
|---|---|
| Concepto técnico | Diferencia de campo de escucha entre monitoreo por altavoces y por auriculares |
| Definición neutra | Con monitores, ambos oídos escuchan ambos altavoces con diferencias naturales de tiempo, amplitud y fase. Con auriculares, cada oído recibe solo su canal sin interacción cruzada. Esto elimina la interacción interaural natural |
| Fórmula / relación | No aplica fórmula directa |
| Criterio operativo | La imagen estéreo se construye de modo diferente en ambos sistemas. Una mezcla revisada solo en auriculares puede presentar problemas no detectados de localización y fase cuando se reproduce en altavoces |
| Error frecuente | Asumir que una mezcla que funciona bien en auriculares funcionará igual en monitores, o viceversa |
| Heurística reformulable | Auriculares y monitores no son equivalentes: son entornos de referencia complementarios, no sustituibles |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.16 — Medidores de nivel: VU, PPM, RMS, LU/LUFS

| Campo | Contenido |
|---|---|
| Concepto técnico | Tipología de medidores de nivel y su relación con la percepción |
| Definición neutra | Existen cuatro familias de medición de nivel: VU (promedio, refleja percepción de sonoridad), PPM (pico, tiempo de integración rápido), RMS (promedio cuadrático) y LU/LUFS (loudness ponderado por percepción) |
| Fórmula / relación | 1 LU = 1 dB. LUFS = LU referenciado a escala de audio digital. VU 0 ≠ –18 dBFS en señal compleja real (solo en senoidal de prueba) |
| Criterio operativo | Cada medidor informa una variable distinta. Usar el medidor correcto para la decisión correcta. No existe un único medidor universal |
| Error frecuente | Asumir que 0 VU = –18 dBFS en condiciones reales de programa. Esa equivalencia solo es válida para señal senoidal pura |
| Heurística reformulable | El medidor VU informa promedio. El PPM informa pico. El LU informa sonoridad percibida. Ninguno reemplaza a los otros |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.17 — Analizador de espectro: uso técnico vs. uso perceptual

| Campo | Contenido |
|---|---|
| Concepto técnico | Dos modos de calibración y uso de un analizador de espectro (FFT) |
| Definición neutra | Un analizador puede configurarse para mostrar lo que el oído percibe (calibración perceptual, respuesta con pendiente ascendente hacia agudos) o para mostrar la energía real de la señal (calibración técnica, respuesta plana para señal plana) |
| Fórmula / relación | Ruido blanco real: distribución plana de energía. Ruido blanco percibido: energía percibida mayor en agudos. La discrepancia es función de las curvas isofónicas |
| Criterio operativo | La calibración del analizador debe corresponder al tipo de análisis requerido. Para diagnóstico técnico (detección de energía subsónica, verificación de filtros, análisis de fase) → calibración plana. Para referencia de escucha → calibración perceptual |
| Error frecuente | Dejar el analizador en configuración perceptual por defecto y hacer análisis técnico sobre esa visualización |
| Heurística reformulable | El analizador se calibra según el objetivo del análisis, no se fija una vez y se olvida |
| Sensibilidad autoral | Media |
| Acción | **REFORMULAR MÁS** |

---

### BLOQUE 1.18 — Decibel: unidad, variantes y referencias

| Campo | Contenido |
|---|---|
| Concepto técnico | Sistema de decibeles y variantes referenciadas en audio |
| Definición neutra | El decibel es una relación logarítmica entre dos valores de potencia o voltaje. Cada variante con sufijo especifica la referencia |
| Fórmula / relación | dB = 10 × log(P2/P1) para potencia; dB = 20 × log(V2/V1) para voltaje. Referencias: dBu (0,775 V), dBV (1 V), dBFS (fullscale digital), dBm (1 mW), dBW (1 W) |
| Criterio operativo | dBu es la referencia estándar para audio profesional analógico y calibración de estructura de ganancia. dBFS es la referencia del dominio digital. No son comparables sin conversión de referencia |
| Error frecuente | Usar "decibeles" sin especificar referencia. Confundir dBu y dBV |
| Heurística reformulable | Un decibel sin referencia es una relación sin contexto. La referencia define qué se está midiendo |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

### BLOQUE 1.19 — Filtros: consecuencias no solicitadas

| Campo | Contenido |
|---|---|
| Concepto técnico | Efectos secundarios inevitables de los filtros sobre fase y nivel |
| Definición neutra | Todo filtro, al modificar el espectro de la señal, produce simultáneamente rotaciones de fase, demoras en el tiempo y potencialmente incrementos de nivel en la zona de corte |
| Fórmula / relación | Ejemplo observado: filtro de 24 dB/oct a 20 Hz → incremento de nivel de salida de –20 a –14,6 dB (pico). RMS no cambia aunque el pico suba. La pendiente de atenuación y el orden del filtro determinan la rotación de fase |
| Criterio operativo | Un filtro siempre produce lo que se le pidió más algo que no se le pidió. Eso adicional puede ser inerte o puede generar cancelaciones de fase con otras señales |
| Error frecuente | Asumir que un filtro solo atenúa frecuencias. Ignorar que puede subir el nivel de salida en la zona de transición |
| Heurística reformulable | El filtro hace lo pedido y algo más. Ese "algo más" siempre debe ser verificado |
| Sensibilidad autoral | Baja |
| Acción | **REUTILIZAR** |

---

## 2. LISTA DE BLOQUEOS

### EXPRESIONES Y FRASES DISTINTIVAS — BLOQUEAR

| Elemento | Tipo | Motivo | Acción |
|---|---|---|---|
| "Eso no es una estructura de ganancia" | Frase característica | Fórmula oral del docente, muy reconocible como suya | BLOQUEAR |
| "Los filtros hacen lo que se les pide pero siempre hacen otra cosa que no se les pidió" | Expresión conceptual | Formulación memorable y estructurada del docente | REFORMULAR |
| "Tiene que sentirse y no escucharse" | Frase axiomática | Expresión muy atribuible al corpus del docente | REFORMULAR |
| "Bombas de tiempo subsónicas" | Metáfora | Creación retórica personal | BLOQUEAR |
| "Por lejísimos" (como superlativo) | Muletilla oral | Marca de tono | BLOQUEAR |
| "Reloco" (como énfasis de sorpresa) | Muletilla oral | Marca de registro informal | BLOQUEAR |
| "De la A a la Z" | Expresión coloquial | Registro oral | BLOQUEAR |
| "Malas noticias" refiriéndose al dominio espacial | Tono oral | Expresión personal hacia el contenido propio | BLOQUEAR |
| "El más completo en formato plugin por lejísimos" referido a SPAN | Recomendación atribuible | Opinión personal del docente sobre herramienta específica | REFORMULAR |
| "Me pareció excelente y terminé adoptándola" | Historia personal | Anécdota sobre Pat Brown | BLOQUEAR |
| Referencia al Aural Exciter con anécdota del manual | Historia docente | Ejemplo personal específico | BLOQUEAR |

---

### ANALOGÍAS DEL DOCENTE — BLOQUEAR O REFORMULAR

| Analogía | Origen | Acción |
|---|---|---|
| Carpintería y la pata corta de la mesa | Creación docente original | BLOQUEAR |
| Temperatura vs. sensación térmica (para frecuencia vs. tono) | Analogía construida | REFORMULAR (la idea es reutilizable, no la formulación) |
| Agua con la mano a la mitad para explicar propagación de onda | Creación docente | REFORMULAR |
| Cuchara bajo el chorro de agua para explicar difusión | Creación docente | BLOQUEAR |
| Palabra incompleta que el cerebro reconstruye (para ambiencia) | Creación docente | BLOQUEAR (muy característica) |
| Cognición como completador de información faltante en sala virtual | Analogía docente | REFORMULAR |

---

### SECUENCIAS PEDAGÓGICAS RECONOCIBLES — BLOQUEAR

| Secuencia | Descripción | Acción |
|---|---|---|
| Concepto → visualización → fórmula | Método explícito del docente ("primero el concepto, la fórmula después") | No conservar el orden ni mencionarlo como método |
| Pregunta encadenada antes de cada herramienta | Estructura de apertura de tema: "Para explicar X tengo que explicar Y, pero antes tengo que entender Z" | BLOQUEAR la secuencia; reutilizar solo el contenido |
| Demostración de ruido blanco para introducir calibración de analizador | Secuencia pedagógica muy específica del docente | BLOQUEAR la secuencia; reutilizar el concepto subyacente |
| Filtro con ruido blanco a -20 dB para mostrar incremento de salida | Ejercicio demostrativo con setup específico | BLOQUEAR como ejercicio; reutilizar la consecuencia técnica |

---

### NOMBRES DE MÉTODO CON SENSIBILIDAD MEDIA-ALTA

| Elemento | Riesgo | Acción |
|---|---|---|
| "Método de abordaje de la compresión" (triángulo) | Metodología nombrada y atribuida públicamente (AES/CAPER) | **ATRIBUIR o BLOQUEAR para M01. Revisar en M05** |
| "Técnica de armado de mixer" | Herramienta de trabajo personal del docente | REFORMULAR sin mencionar como técnica del docente |
| Calibración de analizador como práctica técnica específica | Probablemente desarrollada y sistematizada por el docente | REFORMULAR MÁS |

---

### HERRAMIENTAS CON RECOMENDACIÓN DEMASIADO ASOCIADA AL DOCENTE

| Herramienta | Nivel de asociación | Acción |
|---|---|---|
| SPAN como "el mejor analizador por lejísimos" | Alta | Mencionar como herramienta disponible sin superlativo atribuible |
| Youlean Loudness Meter como referencia de loudness | Media | Reutilizable como mención neutra |
| Waves PAZ/PAZ Meters | Media | Reutilizable como herramienta entre otras |
| ListenTo / AudioMovers | Alta (plataforma de clase del docente) | No reutilizar en contexto pedagógico alternativo |
| Topetinas de ferretería como desacoplador | Alta (consejo muy personal y específico) | BLOQUEAR la referencia concreta; reutilizar el criterio de desacoplamiento firme |
| Plugin "Ambient" del instituto | Altísima | BLOQUEAR (ligado directamente a la institución del docente) |
| Pat Brown como referencia metodológica | Alta | BLOQUEAR nombre; el principio es genérico |

---

## 3. MAPA DE COBERTURA

### TEMAS CUBIERTOS EN M01

| Tema | Subtemas cubiertos | Profundidad |
|---|---|---|
| Señales de audio | Ciclo, período, frecuencia (F=1/T), onda simple, onda compleja, periodicidad, fundamental, parciales armónicos e inarmónicos | Alta |
| Distorsión armónica | Pares vs. impares, timbre, color, intermodulación, aliasing | Media-alta |
| Percepción auditiva básica | Frecuencia vs. tono, amplitud y tono, curvas isofónicas, enmascaramiento, fatiga auditiva, células ciliadas | Alta |
| Dominio espacial | Velocidad del sonido, longitud de onda, modos de sala, resonancias | Media |
| Tratamiento acústico | Paneles absorbentes, resonadores, difusores, primeras reflexiones | Media |
| Posicionamiento de monitores | Distancia a pared, empotrado, orientación, tweeter, crossover, desacoplamiento | Alta |
| Localización binaural | ITD, ILD, sombra acústica, fase binaural, auriculares vs. monitores | Alta |
| Medidores de nivel | VU, PPM, RMS, LU, LUFS | Media (intro) |
| Analizador de espectro | FFT, calibración técnica vs. perceptual, ruido blanco | Media |
| Decibeles | Variantes referenciadas (dBu, dBV, dBFS, dBm, dBW), principio logarítmico | Intro |
| Filtros | Butterworth, consecuencias de fase y nivel, cancelación de fase | Intro |

---

### SUBTEMAS PRESENTES EN M01 PERO DESARROLLADOS EN OTRO MÓDULO

| Subtema | Módulo correcto |
|---|---|
| Estructura de ganancia completa | M02 |
| Polaridad vs. fase (diferencia conceptual) | M03 |
| Fase: definición, rotación, grados | M03 |
| Correlador de fase, goniómetro, osciloscopio | M03 |
| Tipos de ecualizadores (paramétrico, shelving, etc.) | M04 |
| Análisis de ecualizadores de consola (SSL, Neve, API) | M04 |
| Compresores y procesadores dinámicos | M05 |
| Método del triángulo de compresión | M05 |
| Ambiencia, sala virtual, reverb, delay | M06 |
| Mastering | M08 |

---

### CRUCES CON OTROS MÓDULOS

| Contenido de M01 | Se vincula con |
|---|---|
| Distorsión armónica y modelado analógico | M02 (calibración), M04 (EQ analógico), M05 (compresión analógica) |
| Curvas isofónicas y percepción de nivel | M05 (compresión y sonoridad), M08 (mastering y LUFS) |
| Longitud de onda y dominio espacial | M03 (fase por distancia), M06 (ambiencia) |
| Localización binaural (ITD/ILD) | M06 (paneo, ambiencia) |
| Filtros: consecuencias de fase | M03, M04 |
| Medidores VU, RMS, LUFS | M02, M08 |

---

### VACÍOS DETECTADOS EN M01

| Vacío | Nota |
|---|---|
| Principio de duplicación de potencia (+3 dB / ×2) | Mencionado como tema a ver, no desarrollado en C1–C3 |
| Fórmulas completas del decibel | Solo intro; no se desarrollan en las clases disponibles |
| Ruido rosa | Mencionado brevemente; no hay desarrollo |
| HRTF (función de transferencia relacionada con la cabeza) | Referida implícitamente en sombra acústica pero no nombrada |
| Sample rate y bit depth | Referido en Samplerates.txt (material complementario); no integrado en clases M01 |
| Decibel de potencia vs. voltaje | Solo mencionado; pendiente de desarrollo en apuntes del corpus |

---

### CONTENIDO DISLOCADO (presente en M01, pertenece a otro módulo)

| Contenido encontrado en C1–C3 | Módulo al que pertenece |
|---|---|
| Descripción detallada de compresores por tecnología (óptico, FET, VCA, etc.) | M05 |
| Descripción de tipos de ecualizadores y EQ de consolas | M04 |
| Descripción de ambiencia y parámetros de sala virtual | M06 |
| Descripción del training de mezcla y módulo de mastering | M07, M08 |

---

## 4. INFORME DE RIESGO

### 4.1 RIESGO EXPRESIVO

| Nivel | Descripción |
|---|---|
| **MEDIO-ALTO** | Las clases 1–3 contienen numerosas frases características, muletillas y formulaciones que, aunque se producen en contexto oral, son suficientemente reconocibles como para constituir huella expresiva. Especial atención a las frases-axioma ("se siente y no se escucha", "hace lo pedido y algo más"), que son breves, memorables y difíciles de reutilizar sin paráfrasis sustancial |

**Acciones requeridas:** Reformulación total de cualquier frase-axioma. Prohibición de conservar el tono oral. Prohibición de conservar el orden de presentación de los temas.

---

### 4.2 RIESGO ESTRUCTURAL

| Nivel | Descripción |
|---|---|
| **MEDIO** | La secuencia didáctica del docente (pregunta encadenada → herramienta → concepto previo → herramienta) es sistemática y reconocible. Si se reutiliza ese patrón de presentación en el mismo orden, el material puede identificarse estructuralmente aunque las frases estén reformuladas |

**Acciones requeridas:** Reorganizar el contenido por categoría técnica, no por la secuencia en que fue presentado. No conservar el patrón "para explicar X hay que entender Y antes".

---

### 4.3 RIESGO METODOLÓGICO

| Nivel | Descripción |
|---|---|
| **ALTO en un punto específico** | El "método de abordaje de la compresión" (triángulo) tiene riesgo alto: ha sido presentado en foros académicos (AES/CAPER según las fuentes) y tiene nombre propio. Si se reutiliza sin atribución o con reformulación leve, hay riesgo de apropiación indebida de metodología con autoría trazable |
| **BAJO para el resto del M01** | Los conceptos de señales, acústica fisiológica, longitud de onda, etc., son doctrina técnica establecida de dominio público |

**Acciones requeridas:** El método del triángulo debe marcarse ATRIBUIR o BLOQUEAR en M05. En M01 no aparece desarrollado: solo mencionado como anticipo.

---

### 4.4 RIESGO DE NOMENCLATURA

| Nivel | Descripción |
|---|---|
| **BAJO-MEDIO** | La mayoría de la terminología es estándar del sector. Los términos con mayor riesgo son: "retensor" (para lo que en inglés es peak hold o retención de pico): es un término del docente o de uso local no universal; y "sala virtual" como denominación del sistema de ambiencia artificial |

**Acciones requeridas:** Verificar si "retensor" es terminología estándar en el sector hispanohablante o si es un uso propio del docente. Si es propio, sustituir por "retención de pico" o "peak hold". Verificar "sala virtual" vs. terminología AES estándar.

---

## 5. PAQUETE LIMPIO PARA PROYECTO B

### DOCTRINA TÉCNICA REUTILIZABLE

**Señales y frecuencia**
- Una onda es periódica si su período es constante. Si es periódica, tiene frecuencia definida. F = 1/T
- Las ondas complejas periódicas están compuestas por una fundamental y múltiplos enteros (armónicos)
- La fundamental suele ser la frecuencia de mayor amplitud, pero no necesariamente
- Las amplitudes relativas entre armónicos no son estáticas: varían en el tiempo y determinan el timbre
- Los armónicos pares suenan más musicales (el segundo es la octava). Los impares suman presencia y ataque
- Un procesador analógico o de modelado agrega armónicos a la señal. Un procesador digital transparente no lo hace
- El aliasing es una distorsión inarmónica característica del digital. La intermodulación surge de saturación excesiva y produce sonido áspero y fatigante

**Percepción auditiva**
- Frecuencia y tono no son lo mismo: la frecuencia es objetiva y medible; el tono es la respuesta perceptual subjetiva
- La percepción tonal varía con la amplitud: por debajo de 100 Hz, mayor amplitud → sensación de tono más grave. Por encima de 5 kHz, mayor amplitud → sensación de tono más agudo
- Las curvas isofónicas describen la variación de sensibilidad auditiva con la frecuencia y el nivel. A niveles bajos el oído pierde respuesta en extremos del espectro
- El enmascaramiento aumenta con el nivel: frecuencias próximas se enmascaran más cuando la señal es más fuerte
- Las células ciliadas de la cóclea no se regeneran. La exposición prolongada a alto nivel produce pérdida irreversible con mayor impacto en agudos

**Monitoreo**
- El volumen de monitoreo es independiente del nivel interno de señal. Debe mantenerse estable durante la toma de decisiones técnicas
- Mezclar a nivel cambiante produce decisiones de balance inconsistentes
- El nivel de referencia práctico: el más bajo que permita tomar decisiones técnicas precisas (por encima del umbral de conversación como límite superior)
- Chequear fuerte o muy bajo sirve como verificación adicional, nunca como base de decisión

**Dominio espacial**
- λ = v/f (v ≈ 343 m/s). El rango audible abarca desde ~17 m (20 Hz) hasta ~17 mm (20 kHz)
- Las dimensiones físicas de cualquier sala coinciden con la longitud de onda de alguna frecuencia. No existe posición neutra
- Cuando monitor-pared = λ/4 de una frecuencia → cancelación. Cuando = λ/2 → refuerzo
- Monitor empotrado en pared: elimina interferencias por reflexión trasera (el incremento de bajas es compensable por EQ)
- La absorción actúa sobre reflexiones. Los resonadores actúan sobre modos estacionarios. No son intercambiables

**Localización binaural**
- El sistema auditivo determina la dirección de una fuente a partir de: ITD (diferencia de tiempo), ILD (diferencia de nivel), diferencia de fase e ILD espectral (sombra acústica de la cabeza)
- ITD máxima (fuente a 90°): ≈ 0,5 ms
- Las frecuencias cuya λ < tamaño de la cabeza son las más afectadas por la sombra acústica (aprox. por encima de 1 kHz)
- Con monitores ambos oídos reciben ambos canales con diferencias naturales. Con auriculares cada oído recibe solo su canal: no hay interacción interaural

**Medición y análisis**
- VU: promedio. PPM: pico. RMS: promedio cuadrático. LU: 1 LU = 1 dB. LUFS: LU referenciado a escala digital
- La equivalencia 0 VU = –18 dBFS solo es válida para señal senoidal pura, no para programa complejo
- El analizador de espectro debe calibrarse según el objetivo del análisis: configuración perceptual para referencia de escucha; configuración técnica (plana) para diagnóstico
- El ruido blanco tiene la misma energía en cada frecuencia pero no se escucha plano: la percepción exagera los agudos
- Todo filtro produce modificaciones de fase y puede producir incrementos de nivel no esperados en la zona de transición

---

### HEURÍSTICAS REFORMULABLES

1. Toda intervención sobre la señal afecta al menos una de estas tres variables: nivel, fase, espectro
2. La distorsión es favorable en su punto justo y perjudicial cuando se hace audible como efecto
3. Cualquier EQ que compensa un problema de colocación física del monitor está aplicando el parche en el lugar equivocado
4. Un analizador de espectro tiene dos modos de uso: confirmar lo que se escucha o revelar lo que no se escucha
5. La absorción acústica y los resonadores resuelven problemas distintos y no son intercambiables
6. La sensación de que "suena mejor al subir el volumen" puede ser artefacto de las curvas isofónicas, no una mejora real
7. Todo filtro hace lo que se le pide y algo adicional que no se le pidió: ese efecto adicional debe ser verificado
8. Mezclar a nivel inestable produce decisiones inconsistentes aunque el resultado momentáneo suene bien

---

### FÓRMULAS

| Fórmula | Variables | Uso operativo |
|---|---|---|
| F = 1/T | F en Hz, T en segundos | Calcular frecuencia a partir de período |
| T = 1/F | T en segundos, F en Hz | Calcular período a partir de frecuencia |
| λ = v/f | λ en metros, v ≈ 343 m/s, f en Hz | Calcular longitud de onda en aire |
| F_modo = n × (v / 2L) | n: número de modo, L: dimensión de sala | Estimar modos de sala por dimensión |
| dB = 10 × log(P2/P1) | P: potencia | Relación logarítmica de potencia |
| dB = 20 × log(V2/V1) | V: voltaje | Relación logarítmica de tensión |
| 1 LU = 1 dB | — | Conversión LU/dB |

---

### CRITERIOS DE DECISIÓN

| Situación | Criterio |
|---|---|
| Usar absorción vs. resonadores | Absorción para reflexiones y RT60. Resonadores para modos y resonancias específicas |
| Calibrar analizador | Plano para análisis técnico. Perceptual para referencia de escucha |
| Nivel de monitoreo | Estable durante trabajo. Variación solo para verificación puntual |
| Orientación de monitores | Según fabricante. Tweeter a la altura de oídos. Apuntando al oyente |
| Desacoplamiento de monitores | Firme, no blando. El material blando debilita graves |
| Verificar emulación analógica de plugin | Análisis espectral objetivo: presencia de armónicos esperados, ausencia de aliasing |
| Evaluar distorsión | Favorable: se siente como densidad o cuerpo. Desfavorable: se escucha como efecto o produce aspereza |

---

### ADVERTENCIAS

- **[ADV-01]** La equivalencia 0 VU = –18 dBFS se aplica exclusivamente a señal senoidal de prueba. En señal compleja de programa real la relación cambia
- **[ADV-02]** No existe posición de monitor libre de interferencias por longitud de onda en una sala convencional
- **[ADV-03]** Los filtros producen rotaciones de fase, demoras y pueden incrementar nivel en la zona de transición. Esos efectos secundarios deben verificarse caso a caso
- **[ADV-04]** La pérdida de células ciliadas es irreversible. El nivel de monitoreo no es solo una decisión de comodidad sino de salud auditiva a largo plazo
- **[ADV-05]** Una mezcla evaluada solo en auriculares puede presentar problemas no detectados al reproducirse en altavoces

---

### BLOQUEOS CONFIRMADOS PARA PROYECTO B

| ID | Elemento | Motivo |
|---|---|---|
| BLQ-01 | Analogía de la carpintería | Creación narrativa propia del docente |
| BLQ-02 | "Bombas de tiempo subsónicas" | Metáfora retórica personal |
| BLQ-03 | Anécdota del Aural Exciter | Historia personal |
| BLQ-04 | Referencia a Pat Brown como mentor | Historia personal |
| BLQ-05 | Plugin "Ambient" del instituto | Ligado directamente a la institución del docente |
| BLQ-06 | Cuchara bajo el chorro de agua (difusión) | Analogía personal |
| BLQ-07 | Topetinas de ferretería como desacoplador | Consejo específico y muy reconocible |
| BLQ-08 | ListenTo / AudioMovers como plataforma de clase | Plataforma de uso específico del docente |
| BLQ-09 | Secuencia pedagógica "pregunta encadenada → herramienta" | Estructura de presentación del docente |
| BLQ-10 | "Método del triángulo" de compresión | Metodología con autoría trazable (AES/CAPER) — revisar en M05 |

---

*Paquete generado para uso en Proyecto B. No contiene dossier final ni guía redactada. No conserva orden de clase ni tono oral.*