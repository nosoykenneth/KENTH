Tengo suficiente material. Produzco el paquete completo.

---

# EJE 0 — CAMPO DE DECISIÓN
## Extracción Forense KENTH Academy

---

## 1. COBERTURA DEL EJE

**Fuentes que lo alimentan directamente:**

| Fuente | Contenido relevante para Eje 0 |
|---|---|
| Clases 1–5 (Mezcla) | Posicionamiento de monitores, sala, auriculares, decibeles referenciados, gain staging intro |
| PDF: Posicionamiento de Monitores | Doctrina técnica de ubicación física de monitores |
| PDF: Apunte Decibel 2023 | Tipos de dB, fórmulas, pasaje dBu→dBFS, estándares AES/EBU |
| PDF: Estructura de Ganancia | Niveles de señal, gain staging conceptual |
| PDF: Vúmetros | Relación dBu / dBFS, estándares de calibración |
| PDF: Apunte Mastering (secciones de SR y bits) | Nyquist, aliasing, bits, coma fija/flotante |
| Material: Auriculares y amplificadores | Tipos, impedancias, factor de damping, crossfeed |
| Material: Sample Rates | Criterio de elección de SR, aliasing en plugins |
| Clase 25 (Master) | Pasaje sobre SR, bits, coma fija/flotante — contenido de Eje 0 dislocado al bloque de mastering |
| Temario fuente (temarioPablo.md) | Estructura de referencia de los mismos bloques en el curso original |

**Partes dislocadas desde otros bloques del curso fuente:**
- El temario fuente ubica "Medición de Nivel / K-System / VU / Gain Stage" como módulo VII, después de los decibeles. En la arquitectura KENTH eso se divide: el gain staging conceptual queda en Eje 0-B, los instrumentos de medición migran a Eje 1.
- Clase 25 contiene una explicación extensa de sample rate y bits pensada para mastering, pero el contenido técnico pertenece a Eje 0-B.
- El temario fuente incluye "Mixer" (Módulo VIII) como práctica de configuración de sesión en DAW — en KENTH ese segmento de routing básico pertenece al cierre de Eje 0-B.

---

## 2. MATRIZ NEUTRA DEL EJE

### CAPA 0-A — ENTORNO FÍSICO DE DECISIÓN

| # | Tema | Subtema | Concepto técnico | Definición neutra | Fórmula / Relación | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|---|
| 0A-01 | Posicionamiento de monitores | Distancia a paredes | Efecto de reflexión temprana en bajas frecuencias | Las ondas graves se comportan omnidireccionalmente; la cercanía a superficies produce acumulación de energía en bajas frecuencias | Pared lateral: +6 dB. Esquina (2 paredes): +12 dB. Rincón (3 paredes): +18 dB | Mantener distancia asimétrica entre monitor–pared trasera y monitor–pared lateral | Si la distancia a dos paredes es igual, se amplifica la resonancia modal de esa frecuencia | Apoyar los monitores sobre la pared esperando compensar los graves con EQ posterior | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0A-02 | Posicionamiento de monitores | Distancia a paredes | Cancelación por cuarto de longitud de onda | Al alejar el monitor de la pared, habrá siempre una distancia que coincida con λ/4 de alguna frecuencia, produciendo cancelación por reflexión en fase opuesta | λ = velocidad del sonido / frecuencia (343 m/s a temperatura ambiente) | No existe posición ideal libre de problemas; la decisión es elegir el compromiso menos dañino | Empotrar monitores elimina la variable de reflexión trasera; permite compensar la ganancia de bajas con EQ, que es más controlable | Mover monitores aleatoriamente creyendo que una nueva posición resolverá el problema | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0A-03 | Posicionamiento de monitores | Orientación y altura | Directividad de frecuencias altas | Las frecuencias agudas son más direccionales que las graves. Los tweeters pequeños reducen pero no eliminan la directividad | — | Tweeter a altura de oídos; monitor apuntando al punto de escucha en plano horizontal y vertical | Si el monitor apunta al frente y el oyente está al centro, los agudos llegan atenuados, lo que induce compensación errónea de EQ en el material | Orientar monitores al frente en sala rectangular sin verificar eje de tiro | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0A-04 | Posicionamiento de monitores | Orientación | Frecuencia de cruce en monitores verticales/horizontales | En monitores de dos vías, la orientación vertical u horizontal cambia la relación de fase entre woofer y tweeter en el eje horizontal. El fabricante especifica la orientación correcta | — | Respetar la orientación indicada por el fabricante; desviarse altera la respuesta en la zona de cruce | Si el manual especifica posición, hay razón física; ignorarlo deteriora la zona de cruce | Girar los monitores horizontalmente por razones estéticas sin verificar el manual | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0A-05 | Posicionamiento de monitores | Desacople mecánico | Transmisión de vibraciones por estructura | Las vibraciones del gabinete del monitor se transmiten a la superficie de apoyo y de vuelta al recinto. Eso colorea la escucha e introduce energía no deseada | — | Desacoplar físicamente los monitores de la superficie (aisladores, soportes, pads) | El desacople reduce retroalimentación estructural, especialmente audible en bajas frecuencias a alto volumen | Colocar monitores directamente sobre la mesa de trabajo sin ningún tipo de aislamiento | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0A-06 | Sala / acústica | Frecuencias modales | Resonancias de sala | Las dimensiones de la sala determinan las frecuencias que se refuerzan o cancelan por interferencia constructiva y destructiva entre superficies paralelas | Frecuencias modales aproximadas: f = n × (v / 2L), donde L = dimensión de la sala, n = número entero | Detectar modas con señal de barrido o ruido rosa + analizador; confirmar con medición en punto de escucha | Una sala con modos fuertes produce decisiones erróneas de EQ en graves; las correcciones se aplican a la sala, no al audio | Intentar compensar resonancias de sala cambiando la mezcla | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0A-07 | Sala / acústica | Tratamiento | Paneles vs resonadores | Los materiales absorbentes tienen coeficiente de absorción variable por frecuencia. Para problemas de exceso modal se usan resonadores (Helmholtz, membrana), no paneles de espuma. Los paneles tratan primeras reflexiones y tiempo de reverberación, no resonancias de sala | — | Seleccionar tratamiento según el tipo de problema; no aplicar el mismo material para todos los casos | Los difusores dispersan la energía; los absorbentes la eliminan; los resonadores controlan frecuencias específicas | Llenar toda la sala de espuma creyendo que "más absorción = menos problemas" | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0A-08 | Monitoreo | Campo de escucha | Campo cercano, medio y lejano | Campo cercano: el sonido directo predomina sobre la reflexión de sala. Campo medio: el sonido directo y la sala se equilibran. Campo lejano: la sala domina. La elección de campo afecta cuánto información de sala entra en la decisión | — | El campo cercano es el estándar en home studio y estudios medianos; a mayor volumen de sala, el campo lejano es útil para verificar | En campo cercano con monitores pequeños hay que gestionar la pérdida de información por debajo del límite de extensión del monitor | Usar monitores de campo lejano a corta distancia, confundiendo más volumen con más detalle | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0A-09 | Monitoreo | Ancho de banda | Respuesta en frecuencia de monitores | Cada monitor tiene un límite inferior de extensión en graves. Por debajo de esa frecuencia el monitor no reproduce información real. Las decisiones de mezcla en esa zona son ciegas | — | Conocer el límite inferior del monitor y complementar con auriculares de buena extensión en graves si no se dispone de subwoofer | Un monitor no reproduciría, por ejemplo, un pico en 12 Hz; necesitás un analizador espectral para detectarlo | Asumir que "si no se escucha, no existe" | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0A-10 | Auriculares | Tipos | Auriculares cerrados / abiertos / semiabiertos | Cerrados: alta aislación, útiles en grabación; colorean el grave por resonancias del casco. Abiertos: menor coloración de grave, mínima interacción interaural, mejor translación a monitores. Semiabiertos: intermedio | — | Para mezcla: preferir auriculares abiertos cuando sea posible | Los abiertos, aunque mínimamente, permiten una leve interacción interaural que los cerrados eliminan por completo | Mezclar con auriculares cerrados y esperar el mismo resultado que con monitores | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0A-11 | Auriculares | Impedancia | Relación de impedancia auricular / amplificador | La impedancia de salida del amplificador de auriculares afecta la respuesta en frecuencia y el factor de amortiguamiento (damping) del transductor | Relación óptima: impedancia del auricular ≈ 8× impedancia de salida del amplificador | Verificar las especificaciones del amplificador antes de elegir el auricular | Si la relación no se cumple, el transductor "flota" después de los transientes graves: imprecisión en el bajo | Conectar un auricular de 32 Ω a una interfaz con salida de ~40 Ω y asumir que funciona correctamente | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0A-12 | Auriculares | Imagen estéreo | Problema estructural de los auriculares | En auriculares, las señales L y R van directamente a cada oído sin cruce natural. Se pierde la interacción interaural (diferencias de nivel, tiempo y sombra acústica) que define la localización espacial en escucha con monitores | — | Las mezclas en auriculares no garantizan translación de la imagen estéreo a monitores; es necesario verificar en ambos sistemas | Las posiciones percibidas en auriculares y en monitores son distintas incluso con el mismo material | Considerar que "suena bien en auriculares" equivale a "suena bien en monitores" | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0A-13 | Auriculares | Crossfeed | Simulación de interacción interaural en auriculares | El crossfeed mezcla una fracción de la señal de un canal en el otro con retardo, simulando la llegada del sonido al oído contralateral. No replica completamente la escucha natural con monitores | — | Puede mejorar la translación de mezclas entre auriculares y monitores; evaluar por comparación en el caso concreto | Un crossfeed mal implementado puede comprometer la imagen estéreo percibida | Asumir que el crossfeed resuelve completamente el problema de la mezcla en auriculares | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0A-14 | Nivel de monitoreo | Curvas isofónicas | Percepción de nivel frecuencial dependiente del SPL | La sensibilidad del oído a las distintas frecuencias varía con el nivel de escucha (curvas Fletcher-Munson / ISO 226). A bajo volumen, graves y agudos extremos se perciben atenuados relativamente a los medios; a alto volumen, la curva se aplana | — | El nivel de monitoreo de referencia debe ser consistente y calibrado para tomar decisiones de balance espectral reproducibles | Escuchar a volumen alto hace que la mezcla parezca con graves y agudos correctos; al bajar el volumen esos mismos elementos pueden percibirse desbalanceados | Mezclar a distintos niveles sin establecer un nivel de referencia y sin interpretar los cambios perceptuales como artefactos del volumen | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0A-15 | Calibración | Ruido blanco y rosa | Ruido de calibración de analizadores | Ruido blanco: igual energía por Hz. Ruido rosa: igual energía por octava (–3 dB/octava respecto al blanco). El oído percibe el ruido rosa como plano en las tres décadas porque su distribución de energía por octava coincide con la percepción logarítmica | Ruido rosa = Ruido blanco filtrado con LPF de –3 dB/octava | Usar ruido rosa para calibración de salas y referencia comparativa de analizadores | En analizador FFT lineal, el ruido blanco parece plano; el oído lo percibe brillante. El ruido rosa parece plano al oído | Calibrar con ruido blanco y esperar una respuesta percibida plana | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### CAPA 0-B — CADENA DIGITAL DE DECISIÓN

| # | Tema | Subtema | Concepto técnico | Definición neutra | Fórmula / Relación | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|---|
| 0B-01 | Sample rate | Nyquist | Frecuencia de Nyquist | La frecuencia máxima representable en un sistema digital es igual a la mitad de la frecuencia de muestreo. Para reconstruir una frecuencia, se requiere al menos una muestra por semiciclo | f_Nyquist = SR / 2 | El SR no aumenta la resolución temporal de amplitud: aumenta el límite de frecuencia reproducible y reduce el aliasing | La información de altura (tono) de una señal se reconstruye perfectamente con 2 muestras por ciclo: más muestras no añaden información sobre esa frecuencia | Subir el SR creyendo que se obtiene más detalle de la forma de onda (confusión SR con bits) | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0B-02 | Sample rate | Aliasing | Distorsión por aliasing | Cuando una frecuencia por encima de f_Nyquist llega al conversor, se refleja como una frecuencia inarmónica dentro de la banda útil. El aliasing no es ruidoso ni armónico: es distorsión inarmónica no filtrable a posteriori | f_alias = SR – f_señal (simplificado para 1er orden) | Usar filtro anti-aliasing (AAF) antes del ADC. En plugins, verificar si incorporan oversampling para evitar alias interno durante el procesamiento | Una señal grabada correctamente a 44,1 kHz no tiene más aliasing que una grabada a 96 kHz; el aliasing ocurre durante el procesamiento si el plugin no hace oversampling | Subir el SR del proyecto creyendo que eso corrige el aliasing de plugins grabados previamente | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0B-03 | Sample rate | Oversampling | Oversampling en la cadena | El oversampling procesa la señal internamente a una frecuencia mayor y luego la reduce. Permite a los plugins operar por encima de f_Nyquist durante el procesamiento, reduciendo el aliasing generado por operaciones no lineales | — | Activar oversampling en procesadores que lo ofrecen cuando la calidad del procesamiento importa más que el consumo de CPU | A mayor SR del proyecto, menor posibilidad de alias en plugins que no hacen oversampling, pero con costo de CPU lineal; el oversampling por plugin es la solución más eficiente | Usar 192 kHz de proyecto "para evitar alias" sin verificar si los plugins usados hacen oversampling propio | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0B-04 | Bits | Cuantización | Profundidad de bits y resolución de amplitud | Los bits determinan la cantidad de escalones de amplitud disponibles para almacenar cada muestra. Cada bit adicional duplica la cantidad de escalones y añade ~6 dB al rango dinámico | RD ≈ 6,02 × bits + 1,76 dB | Trabajar en 24 bits en sesión; 16 bits para distribución en CD; 32 bit float como formato interno de DAW para headroom ilimitado en procesamiento | La distancia entre escalones en 16 bits vs 24 bits es exponencial: la diferencia de resolución no es de un 50%, sino de 256 veces la cantidad de escalones | Confundir la profundidad de bits (resolución de amplitud) con el sample rate (resolución temporal/frecuencial) | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0B-05 | Bits | Coma fija vs flotante | Aritmética de coma fija y flotante | Coma fija: cada valor se almacena en una posición fija de la grilla de cuantización. Coma flotante: el valor se almacena con mantisa y exponente, permitiendo representar un rango dinámico mucho mayor sin clipping interno. La conversión A/D trabaja en coma fija; el procesamiento en DAW trabaja en coma flotante | — | En 32 bit float no hay clipping dentro del motor de la DAW aunque los medidores superen 0 dBFS. El clipping ocurre al momento de la conversión D/A o al exportar a 24/16 bits | El medidor interno de la DAW puede superar 0 dBFS sin distorsión real si el motor es float; confiar el control de nivel a los medidores de las salidas y conversión | Dejar clipping en los medidores de la DAW pensando que "en float no importa" cuando se va a exportar a 24 bits | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0B-06 | Decibeles | No referenciado | dB no referenciado | Expresa una relación entre dos valores; no indica nivel absoluto. Solo describe cuánto es más o menos que otra cantidad | dB = 10 × log₁₀(P₁/P₂) [potencia] / dB = 20 × log₁₀(V₁/V₂) [voltaje] | Uso: describir cambios relativos (ganancia, atenuación, pendiente de filtro) | El multiplicador es 10 para potencia y 20 para voltaje porque potencia es proporcional al cuadrado del voltaje | Aplicar la fórmula de potencia a voltajes o viceversa | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0B-07 | Decibeles | Referenciados | Tipos de dB referenciado | Un dB referenciado fija el 0 dB a un valor absoluto específico. La referencia define qué significa "0" en ese sistema | dBW: ref = 1 W · dBm: ref = 1 mW · dBu: ref = 0,775 V · dBV: ref = 1 V · dBFS: ref = nivel máximo codificable · dBSPL: ref = 20 μPa | Elegir la unidad correcta según el dominio (potencia, voltaje analógico, digital, acústico) | El dBu y el dBV tienen referencias diferentes; no son intercambiables sin conversión | Usar "dB" sin especificar referencia en contextos donde el nivel absoluto importa | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0B-08 | Decibeles | Duplicación de potencia | Principio de duplicación de potencia | Duplicar la potencia añade ~3 dB. Duplicar 10 veces la potencia añade ~10 dB. Duplicar la tensión (voltaje) añade ~6 dB | 10 × log₁₀(2) ≈ 3,01 dB · 20 × log₁₀(2) ≈ 6,02 dB | Base para estimar cambios perceptuales de nivel: +3 dB es cambio claramente audible; +10 dB se percibe como "el doble de fuerte" aproximadamente | No confundir potencia con voltaje: un amplificador que duplica el voltaje de salida cuadruplica la potencia entregada (+6 dB en tensión = +6 dB en potencia solo si la carga es constante) | Sumar 3 dB creyendo que duplica el voltaje, o sumar 6 dB creyendo que duplica la potencia indistintamente | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0B-09 | Decibeles | Pasaje analógico-digital | Relación dBu → dBFS | No existe una única relación entre dBu y dBFS: depende del valor máximo de entrada del conversor. La equivalencia es fija para un conversor específico | AES RP155: 0 dBFS = +24 dBu; nivel de referencia: +4 dBu = –20 dBFS = 0 VU · EBU R68: 0 dBFS = +18 dBu; nivel de referencia: 0 dBu = –18 dBFS | Usar el estándar aplicable al contexto (broadcast: EBU; producción musical general: AES) y configurar los plugins de modelado analógico al nivel de calibración correspondiente | En un plugin VU calibrado a AES, 0 VU corresponde a –20 dBFS; en uno calibrado a EBU, 0 VU = –18 dBFS. Usar el incorrecto desplaza el punto de trabajo | Asumir que 0 VU siempre equivale a –18 dBFS o que todos los plugins usan el mismo estándar | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0B-10 | Niveles de señal | Tipos de nivel | Niveles de señal en producción musical | La cadena de señal pasa por distintos rangos de tensión según la etapa: micrófono (mV, desde –60 dBu), instrumento (entre mic y línea), línea (+4 dBu profesional / –10 dBV semipro), y digital (referenciado a 0 dBFS) | +4 dBu = nivel de línea profesional ≈ 1,23 V rms · –10 dBV = nivel semiprofesional ≈ 0,316 V rms | Conectar señales al nivel de entrada correspondiente de cada dispositivo para evitar distorsión por exceso o ruido por nivel insuficiente | La diferencia entre +4 dBu y –10 dBV es de ~11,8 dB; conectar equipo pro a entrada –10 puede saturar; conectar semipro a entrada +4 puede quedar enterrado en el piso de ruido | Usar la entrada de micrófono para conectar línea, o línea para conectar instrumento pasivo | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 0B-11 | Gain staging | Concepto | Estructura de ganancia en la cadena | El gain staging es la práctica de gestionar el nivel de señal en cada etapa de la cadena de procesamiento para que: (a) todas las etapas operen en su rango óptimo, (b) se evite clipping no deseado, (c) se minimice el piso de ruido acumulado | — | Objetivo: mantener el nivel promedio de trabajo dentro del rango de confort de cada procesador; en DAW, conservar headroom suficiente antes de la mezcla final | Un buen gain staging en cada elemento facilita el control dinámico global en etapas posteriores; un gain staging deficiente hace que el mix "explote" antes de llegar al master | Dejar todos los faders al 0 dB sin gestionar las ganancias de entrada/salida de cada track y procesador | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

## 3. CONTENIDO ATRIBUIBLE DEL EJE

| Bloque | Atribución requerida | Etiqueta recomendada |
|---|---|---|
| Estándares AES RP155 y EBU R68 | Documentos normativos públicos; citar como estándares (AES/EBU), no como contenido del autor fuente | "Según norma AES RP155 / EBU R68" |
| Curvas de igual sonoridad | Fletcher & Munson (1933) / ISO 226 actualizada; dominio público científico | "Curvas ISO 226 (Fletcher-Munson)" |
| Teorema de Nyquist-Shannon | Harry Nyquist / Claude Shannon; dominio público científico | "Teorema de Nyquist-Shannon" |
| Materiales pedagógicos (PDFs de posicionamiento, decibeles, gain stage) | Autoría: Pablo Rabinovich. Materiales usados con autorización; si se cita directamente cualquier formulación de esos documentos, requiere atribución | "Según [Rabinovich, material de referencia]" |
| Apunte de Análisis Espectral (ruido blanco/rosa) | Autoría: Pablo Rabinovich | Igual |

**Nota operativa:** toda la doctrina técnica de este eje (física, DSP, normas) es de dominio general y no requiere atribución al autor fuente. La atribución solo aplica si se cita directamente la formulación o los materiales de Rabinovich.

---

## 4. BLOQUEOS DEL EJE

| Bloque bloqueado | Tipo de riesgo | Por qué no debe pasar |
|---|---|---|
| Anécdota sobre experiencia personal del docente con Sonarworks (HD 650 vs DT 990) | EXPRESIÓN NO REUTILIZABLE | Anécdota personal identificable; opinión subjetiva de experiencia de usuario |
| Formulación "enchufarle un Rivotril a la mezcla" y similares | EXPRESIÓN NO REUTILIZABLE | Frase distintiva del autor; tono oral muy marcado |
| Secuencia pedagógica del temario fuente (Módulos I→VII en orden) | ESTRUCTURA NO REUTILIZABLE | El orden Acústica → Control Room → Altavoces → Monitoreo → Digital → Decibeles → Medición es la secuencia reconocible del curso fuente |
| Ejemplos personales del docente (nombre del artista de los 90, anécdota Clarín/Cerati) | EXPRESIÓN NO REUTILIZABLE | Historias personales del autor; identificables y no transferibles |
| Formulaciones orales muy específicas: "muy complicado", "carísimo", "topetinas", "barullar" | EXPRESIÓN NO REUTILIZABLE | Vocabulario oral marcado del autor; reproduce tono de clase |
| Descripción del mecanismo de damping con la metáfora de la cuerda que flota | EXPRESIÓN NO REUTILIZABLE | Analogía memorable del autor; aunque el concepto es reutilizable, esta forma no lo es |
| Referencia al artículo de Neumann como fuente mencionada en clase | EXPRESIÓN NO REUTILIZABLE | Referencia situada en el contexto de clase de otro curso; no aplicable directamente |

---

## 5. VACÍOS Y TENSIONES DEL EJE

| Tipo | Descripción | Implicación para redacción |
|---|---|---|
| **Vacío** | El Eje 0-A no cubre explícitamente detección práctica de modas con herramientas específicas (p.ej., Room EQ Wizard); las fuentes mencionan el problema pero no un protocolo de medición paso a paso | Habrá que construir ese contenido operativo o remitir a fuentes externas de acústica |
| **Vacío** | El Eje 0-A no incluye contenido sobre tratamiento de primeras reflexiones con criterio operativo claro (el "método del espejo" aparece mencionado en transcripciones pero no desarrollado técnicamente) | Necesita desarrollo propio o fuente externa |
| **Tensión de límite** | El temario fuente incluye análisis espectral (Módulo XI) como herramienta de calibración; en KENTH el análisis espectral es Eje 1. El Eje 0 solo debe introducir ruido rosa como señal de calibración, no profundizar en configuración de analizadores | Al redactar: introducir ruido rosa como herramienta; redirigir el uso del analizador a Eje 1 |
| **Tensión de límite** | El gain staging conceptual está en Eje 0-B pero el gain staging por elemento está en Eje 2. La frontera puede ser difusa al redactar | Eje 0-B: solo el principio y la lógica de cadena. Eje 2: la aplicación por track/procesador |
| **Tensión de límite** | Las medidas de nivel (VU, RMS, Peak, K-System) están en el temario fuente junto a los decibeles. En KENTH los instrumentos de medición son Eje 1. En Eje 0 solo entra el dB como unidad conceptual y el estándar de calibración (AES/EBU) | Al redactar Eje 0: hablar de dB y calibración de referencia, no de medidores de nivel ni de K-System |
| **Cruce activo con Eje 1** | Los instrumentos de lectura (analizadores, medidores) se introducen en Eje 1 pero operan sobre la cadena calibrada en Eje 0. Habrá que declarar explícitamente ese cruce al alumno | Advertencia pedagógica a incluir en la transición Eje 0 → Eje 1 |
| **Riesgo de profundidad variable** | Las fuentes dedican más tiempo y detalle a algunos subtemas (p.ej., bits y sample rate se desarrollan extensamente en transcripciones) que a otros (p.ej., configuración inicial de DAW es casi inexistente en las fuentes). El balance de profundidad del eje deberá construirse editorialmente | Al redactar: no replicar las proporciones del curso fuente; definir la profundidad de cada subtema según los objetivos de KENTH |

---

## 6. PAQUETE LIMPIO DEL EJE

### EJE 0 — CAMPO DE DECISIÓN · Paquete limpio para proyecto generativo

---

**FUNCIÓN DEL EJE:** Condición de posibilidad. Establece que toda decisión de mezcla depende de que el sistema de monitoreo sea confiable y la cadena digital no tenga pérdidas estructurales invisibles.

---

#### BLOQUE A — ENTORNO FÍSICO

**Doctrina reutilizable:**
- Proximidad a paredes añade energía en bajas frecuencias: pared (+6 dB), esquina (+12 dB), rincón (+18 dB)
- Alejarse de las paredes introduce cancelaciones por reflexiones en λ/4 de ciertas frecuencias
- No existe posición sin compromiso; la tarea es elegir el compromiso menos dañino
- Los agudos son más direccionales que los graves; el eje de tiro del monitor debe apuntar al punto de escucha
- La orientación de un monitor de dos vías afecta la frecuencia de cruce; seguir especificación del fabricante
- El desacople mecánico reduce coloración por transmisión estructural
- Las resonancias de sala son un problema de la sala, no del audio; no corregir con EQ del material
- Paneles absorben; resonadores controlan frecuencias específicas; difusores dispersan. No son intercambiables
- El campo cercano minimiza la influencia de la sala en la escucha
- Por debajo del límite de extensión del monitor, las decisiones de mezcla son ciegas
- El ruido rosa tiene igual energía por octava; el oído lo percibe plano; es el estándar de calibración

**Heurísticas reformulables:**
- Si no se puede posicionar el monitor idealmente, verificar la mezcla en múltiples sistemas
- Mayor ancho de banda del monitor = menos zonas ciegas; en donde el monitor no llega, usar auriculares de referencia con extensión en graves
- Auriculares abiertos para mezcla: menor coloración de grave, mínima interacción interaural natural
- Verificar la relación de impedancia auricular/amplificador antes de confiar en la escucha grave
- El nivel de monitoreo de referencia debe ser consistente; las curvas isofónicas hacen que el balance espectral cambie con el volumen

**Atribuciones:**
- Curvas de igual sonoridad: ISO 226 (Fletcher-Munson)

**Advertencias:**
- LÍMITE: física pura y psicoacústica teórica entran solo si resuelven una decisión de monitoreo o de cadena. No desarrollar movimiento oscilatorio como objeto independiente
- CRUCE → EJE 1: la configuración y uso del analizador espectral y de los medidores de nivel pertenecen a Eje 1; en Eje 0 el ruido rosa solo introduce el concepto de señal de calibración

**Bloqueos:**
- Secuencia pedagógica del temario fuente: no replicar el orden Acústica → Altavoces → Monitoreo
- Anécdotas y ejemplos personales del autor fuente: bloqueados
- Formulaciones orales del autor fuente: bloqueadas

---

#### BLOQUE B — CADENA DIGITAL

**Doctrina reutilizable:**
- SR define el límite frecuencial reproducible (f_Nyquist = SR/2); no mejora la resolución de amplitud
- El alias es distorsión inarmónica: ocurre si se intenta procesar frecuencias superiores a f_Nyquist
- El alias no desaparece al subir el SR del proyecto si ya está grabado; solo se previene durante la grabación o el procesamiento
- El oversampling reduce el alias generado por operaciones no lineales en plugins durante el procesamiento
- Los bits determinan la cantidad de escalones de amplitud (escalones = 2ⁿ); cada bit adicional ≈ +6 dB de rango dinámico
- 16 bits = 65.536 escalones (~96 dB). 24 bits = 16.777.216 escalones (~144 dB)
- Coma fija: valor en posición fija de la grilla (conversores A/D y D/A). Coma flotante: mantisa + exponente (motor interno de DAW); no genera clipping interno en el procesamiento
- El dB no referenciado expresa una relación (factor 10 para potencia, factor 20 para voltaje)
- El dB referenciado fija el 0 dB a un valor absoluto. Tipos: dBW, dBm, dBu, dBV, dBFS, dBSPL
- Duplicar la potencia: +3 dB. Duplicar el voltaje: +6 dB
- La relación dBu↔dBFS depende del conversor; no es universal
- AES RP155: +4 dBu = –20 dBFS = 0 VU
- EBU R68: 0 dBu = –18 dBFS
- Niveles de señal en producción: micrófono (~–60 dBu), instrumento (intermedio), línea profesional (+4 dBu / ~1,23 V rms), línea semiprofesional (–10 dBV / ~0,316 V rms)
- El gain staging gestiona el nivel en cada etapa de la cadena para operar en el rango óptimo de cada dispositivo o procesador

**Heurísticas reformulables:**
- Grabar en 24 bits; procesar en 32 bit float; exportar al formato del destino
- El SR más alto no mejora la señal ya grabada; mejora el alias durante el procesamiento si los plugins no tienen oversampling propio
- Activar oversampling en procesadores no lineales (saturadores, compresores de modelado) cuando la CPU lo permita
- En modelado analógico con plugins, verificar qué estándar de calibración aplica el plugin (AES vs EBU) antes de calibrar
- El headroom en la sesión no es un lujo: es el espacio donde el procesamiento opera sin degradarse

**Atribuciones:**
- Teorema de Nyquist-Shannon: Harry Nyquist / Claude Shannon (dominio público)
- Estándares de calibración: AES RP155 / EBU R68 (documentos normativos)

**Advertencias:**
- LÍMITE: los medidores de nivel (VU, RMS, Peak, K-System) se introducen en Eje 1, no aquí. En Eje 0 solo entra el concepto de dB y el punto de calibración AES/EBU
- CRUCE → EJE 2: el gain staging por elemento (ajuste de ganancia de entrada/salida de cada procesador en la cadena de cada track) es Eje 2, no Eje 0. Eje 0 solo introduce el principio y la lógica de cadena
- VACÍO A CUBRIR: tratamiento de primeras reflexiones y protocolo práctico de detección de modas no están cubiertos con suficiente desarrollo operativo en las fuentes; habrá que construir o referenciar fuentes externas

**Bloqueos:**
- Orden de explicación del temario fuente para este bloque: bloqueado
- Ejemplos, anécdotas y formulaciones orales del autor fuente: bloqueados

---

*Paquete listo para ingesta en Proyecto Generativo. Siguiente eje cuando lo indiques.*