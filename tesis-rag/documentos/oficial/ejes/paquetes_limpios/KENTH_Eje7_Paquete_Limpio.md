Tengo suficiente material. Produzco el paquete completo.

---

# EJE 7 — TRADUCCIÓN Y ENTREGA
## Extracción Forense KENTH Academy

---

## 1. COBERTURA DEL EJE

**Fuentes que lo alimentan directamente:**

| Fuente | Contenido relevante para Eje 7 |
|---|---|
| Clases 25–28 (Master) | Flujo completo de mastering: tres etapas, preparación, trimming, medición, corrección técnica, compresión, limitación, imagen estéreo, MS en mastering, dithering, targets de streaming, coherencia de álbum |
| PDF: Apunte Mastering 2022 | Definición del mastering, tres etapas, procesos habituales, filtrado de subsónicas, corrección de resonancias, compresión en serie, balance L/R, imagen estéreo, mono maker, optimización para plataformas |
| PDF: Medidores de Nivel (sección LUFS) | LUFS como sistema de medición, LKFS/LUFS equivalencia, tipos de medición (momentary, short-term, integrated), true peak |
| PDF: Apunte Fundamento de Señales de Audio (sección resampleo) | Resampleo, sobremuestreo, aliasing en la cadena digital de entrega |
| Temario fuente (Módulo de Mastering) | Lista canónica del eje: preparación, medición, técnicas de procesamiento, MS, imagen estéreo, limitación, dithering, resampleo, targets de streaming, álbum |

**Partes dislocadas:**

El **nivel de entrega de la mezcla** (headroom, LUFS al recibir la mezcla para masterizar) aparece en las fuentes como introducción al módulo de mastering pero fue asignado al Eje 6 en la arquitectura KENTH. El Eje 7 arranca desde lo que el Eje 6 entregó.

La **subsección de álbum** (coherencia entre canciones, continuidad, concepto de disco) aparece distribuida entre Clases 20, 25 y el apunte de mastering. En KENTH es la subsección final del Eje 7.

El **dithering** tiene cobertura extensa en Clase 27 pero también aparece mencionado en contexto de bits y exportación en Clase 25 (bloque de audio digital). La doctrina técnica es la misma; el contexto específico de aplicación en la entrega del master es Eje 7.

---

## 2. MATRIZ NEUTRA DEL EJE

### BLOQUE A — DEFINICIÓN Y TRES ETAPAS DEL MASTERING

| # | Tema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|
| 7A-01 | Definición | Mastering: finalidad y alcance | El mastering es la preparación de un programa fonográfico para su distribución. Es la última instancia para corregir desajustes de índole general; no está diseñado para corregir la mezcla, sino para retocar lo que quedó desajustado de forma global. Todo procesamiento en mastering afecta al conjunto, no a un elemento individual | — | El mastering no arregla mezclas: traduce lo que hay. Si el bajo de un instrumento específico está mal, es un problema de mezcla. Si los graves de la canción completa son excesivos, es un problema de mastering | Un problema de un elemento específico que se intenta corregir en mastering inevitablemente afecta a todos los demás elementos del programa | Asumir que el mastering puede "terminar" una mezcla que no estuvo bien procesada por elemento | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7A-02 | Etapas | Tres etapas del mastering | El mastering puede dividirse en tres etapas independientes: (1) Técnica: corregir problemas físicos y formales de la señal; (2) Comercial: llevar el material al nivel de sonoridad adecuado para el destino de distribución; (3) Artística: añadir carácter, color o modificaciones tímbricas y dinámicas deliberadas. La etapa artística puede estar o no, dependiendo del estado del material recibido | — | El orden importa: la técnica se resuelve antes de la comercial. No tiene sentido optimizar el nivel si la señal todavía tiene problemas de DC offset, resonancias o fase | Si la mezcla llega bien terminada, la etapa artística puede ser mínima o innecesaria. No forzar procesamiento artístico cuando el material no lo necesita | Aplicar procesamiento artístico antes de resolver la etapa técnica, contaminando la cadena con problemas que luego se amplifican | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE B — PREPARACIÓN Y REPARACIÓN DE SEÑAL

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|
| 7B-01 | Preparación | Trimming | Ajuste de ganancia de clip a la entrada de la cadena | Antes de entrar en la cadena de procesamiento, el nivel de la mezcla se ajusta con el clip gain (o trim) para que los procesadores de mastering operen en su rango óptimo. Si el material tiene picos cercanos a 0 dBFS o LUFS integrados muy altos, el trimming es una condición necesaria antes de cualquier procesamiento | Objetivo orientativo: ~–20 a –23 LUFSi a la entrada de la cadena | Verificar LUFS integrados del material antes de configurar el primer procesador; si los modelados analógicos esperan un nivel de calibración específico, este es el momento de alcanzarlo | Si la mezcla llega a –10 LUFSi ya comprimida, el masterizador tiene mucho menos espacio para operar; el problema está antes, en la mezcla | Comenzar el proceso de mastering sin medir y ajustar el nivel de entrada, dejando que los primeros procesadores operen fuera de su rango óptimo | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7B-02 | Preparación | DC offset | Corrección de desplazamiento por continua | El DC offset es una componente de corriente continua que desplaza toda la forma de onda fuera de su posición centrada de reposo. Consecuencias: clipping asimétrico (se llega antes al techo de un lado), carga térmica innecesaria en los parlantes, reacción desigual de procesadores dinámicos | Valor umbral práctico: si el porcentaje de offset medido con estadísticas del archivo es ≤0,0xx%, no intervenir. Si alcanza valores enteros o claramente significativos (~1%), corregir con HPF bajo (5–10 Hz) o herramienta específica de offset | El DC offset equivale a energía en 0 Hz o muy cerca; un HPF bien bajo elimina esa componente sin afectar el audio útil | Corregir el DC offset al final de la cadena de mastering; si está presente, debe resolverse en la etapa técnica antes de cualquier procesamiento | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7B-03 | Preparación | Asimetría de forma de onda | Corrección de asimetría | Una señal asimétrica está centrada (sin DC offset) pero sus picos tienden más hacia el semiciclo positivo o negativo. Causa: la relación de fase entre los componentes frecuenciales de la señal genera esa distribución asimétrica de picos. Consecuencia: al querer subir el volumen, se llega antes al techo del lado más cargado, reduciendo el headroom útil | Diagnóstico: estadísticas del archivo o visualización en osciloscopio. Corrección: filtro AllPass → rota la fase de una frecuencia y sus adyacentes sin modificar la amplitud de ninguna componente | La forma de onda de una señal depende de tres factores: cantidad de frecuencias, amplitud de cada una, y relación de fase entre ellas. La asimetría es un problema de relación de fase, no de amplitud | Confundir asimetría con DC offset y aplicar HPF cuando el problema requiere AllPass, o aplicar AllPass cuando el problema es offset | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7B-04 | Preparación | DC offset vs asimetría | Distinción entre ambos | DC offset: toda la señal está desplazada del eje de cero; no necesariamente asimétrica. Asimetría: la señal está centrada pero sus picos no son simétricos. Son fenómenos distintos con correcciones distintas | DC offset → HPF o herramienta de offset. Asimetría → filtro AllPass | Si una señal tiene ambos problemas, corregir primero el DC offset (HPF) y luego la asimetría (AllPass) | Aplicar AllPass para corregir DC offset: el AllPass no elimina la componente continua | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE C — MEDICIÓN Y CORRECCIÓN ESPECTRAL

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|
| 7C-01 | Medición | Nivel, fase, espectro | Análisis técnico previo | El diagnóstico en mastering sigue la misma lógica que en Eje 1: nivel, fase, espectro. La diferencia es que en mastering el análisis es global (el programa completo) y el objetivo es detectar problemas de índole general, no de elementos individuales | — | Analizar la señal completa antes de insertar cualquier procesador. Chequear: LUFS integrados y pico, correlación fase (goniómetro/correlatómetro), espectro (subsónicas, balance general, sibilancias residuales) | Si el análisis de fase muestra problemas en los graves por diferencia temporal entre canales, la corrección es temporal (AllPass o alineación) no colapsar a mono | Comenzar el procesamiento de mastering sin diagnóstico técnico previo, aplicando procesadores "por defecto" | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7C-02 | Corrección | Subsónicas | Filtrado HPF en mastering | La presencia de energía significativa por debajo del fundamento de la canción (típicamente por encima de ~42–50 Hz para bombo/bajo) es un problema de mastering: no aporta información musical y carga térmicamente las bobinas de los parlantes, especialmente los de consumo doméstico | HPF suave en mastering: corte gradual por debajo del fundamento de la canción. Criterio: si la curva espectral desciende de forma continua desde el fundamento hacia las subsónicas, no hay problema; si hay energía que sube o sostiene en la zona subsónica, intervenir | Un HPF subsónico en mastering no es obligatorio por defecto; es necesario solo si el análisis muestra energía problemática en esa zona | Aplicar HPF subsónico en todos los masters como práctica automática sin verificar si el material lo necesita | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7C-03 | Corrección | Resonancias | Corrección de resonancias en mastering | Las resonancias en mastering son problemas frecuenciales de carácter general: energía en exceso en una frecuencia que afecta a toda la canción (no a un instrumento específico). Corrección: EQ paramétrico con Q adecuado, o EQ dinámico si la resonancia es intermitente | — | Una resonancia del snare que aparece en Mid pero no en Side puede corregirse con EQ en modo MS, evitando afectar al Side innecesariamente | Corregir en mastering una resonancia que en realidad viene de un instrumento específico (p.ej., un tambor); ese problema debería haberse resuelto en la mezcla | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7C-04 | Corrección | Balance L/R | Corrección del desbalance entre canales | Si la mezcla tiene más energía en un canal que en el otro (el bombo, el bajo o el tambor se mezclaron fuera del centro), el oyente percibe que la mezcla "se apoya" en un lado. En mastering puede corregirse con herramientas de "mono maker" que pasan gradualmente a mono por debajo de una frecuencia específica | — | La corrección del balance en mastering es global; si el problema viene de un instrumento paneado incorrectamente, lo correcto es volver a la mezcla | Un desequilibrio en graves es más notorio que en agudos porque las bajas frecuencias son omnidireccionales y se esperan al centro | Confundir balance L/R (diferencia de nivel entre canales) con imagen estéreo (anchura y distribución del campo) | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE D — COMPRESIÓN Y SATURACIÓN EN MASTERING

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|
| 7D-01 | Compresión | En serie | Compresión escalonada en mastering | Diferentes objetivos de compresión requieren diferentes configuraciones. En mastering, es común escalar compresores en serie: primero un compresor musical (Vari-mu/valvular) para dar consistencia general y carácter, luego un compresor preciso (VCA) para controlar picos percusivos | Tip del apunte de mastering: mejores resultados con varios pasos pequeños que con grandes saltos en muy pocos pasos | Un compresor valvular trabajando sobre un material ya parcialmente nivelado puede aportar mucho más carácter con menos reducción de ganancia que si tiene que gestionar todo el rango dinámico solo | Intentar resolver compresión de carácter y control de picos con un solo compresor, comprometiendo siempre alguno de los dos objetivos | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7D-02 | Compresión | Paralela y ascendente | Compresión alternativa en mastering | La compresión paralela (mezclar señal comprimida muy agresivamente con la original) puede subir el nivel percibido reduciendo la diferencia entre pasajes fuertes y suaves. La compresión ascendente levanta los pasajes más bajos sin tocar los más fuertes. Ambas pueden combinarse con la compresión descendente para controlar la dinámica sin que la canción "se aplaste" perceptivamente | — | La compresión paralela con envolventes muy rápidas puede introducir aliasing y distorsión; con envolventes suaves el resultado es más transparente. El compresor ascendente es una alternativa más transparente | Comprimir en paralelo con envolventes muy rápidas esperando obtener densidad sin costo; el costo en este caso es aliasing y coloración no controlada | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7D-03 | Saturación | Distorsión armónica | Saturación en mastering | La saturación controlada en mastering puede añadir riqueza armónica y "pegar" la señal de forma sutil. Segundo armónico: percepción cálida. También puede aumentar la densidad percibida de los pasajes más suaves al añadir armónicos que el procesamiento dinámico no genera | — | La saturación de mastering se mide en décimas de dB de THD; si es audible como distorsión, hay demasiada. Su efecto real se percibe como "calor" o "presencia" más que como distorsión identificable | Comparar con bypass sin compensar el nivel; si la saturación sube el volumen aunque sea mínimamente, la comparación no es honesta | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE E — IMAGEN ESTÉREO Y MS EN MASTERING

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|
| 7E-01 | MS en mastering | Diferencia con MS en mezcla | MS en mastering opera sobre el programa completo | En mastering, el procesamiento Mid/Side opera sobre la suma final del programa: el Mid contiene todo lo que está al centro (graves, voz, bombo, kick), el Side contiene todo lo que está en los laterales. Modificar el Mid o el Side en mastering modifica el balance de todos los elementos que viven en esa zona del campo estéreo | — | Una resonancia del snare suele estar en Mid; aplicar corrección en Mid en mastering evita afectar el Side sin necesidad | El MS en mastering es quirúrgico pero global: cualquier corrección en el Mid toca todo el contenido central del programa simultáneamente. Si el problema es de un instrumento específico, debe resolverse en la mezcla | Usar el procesamiento MS en mastering para corregir problemas que corresponden a elementos individuales de la mezcla | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7E-02 | Imagen estéreo | Ajuste global | Control de anchura en mastering | En mastering es posible controlar la imagen estéreo del programa: (a) por bandas de frecuencia (imagen estéreo multibanda), (b) de forma global mediante el procesamiento MS. La práctica recomendada: mantener los graves más centrados (mono en frecuencias bajas) para aumentar el peso percibido y reducir problemas de reproducción en sistemas mono | — | Abrir la imagen a medida que aumenta la frecuencia y cerrarla en graves: da más peso y más estabilidad. Cerrar demasiado la imagen puede hacer que la mezcla suene sin espacialidad | Ampliar la imagen estéreo en mastering esperando compensar una mezcla plana; si la mezcla no tiene contenido lateral, no hay imagen real que ampliar | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE F — LIMITACIÓN, TRUE PEAK Y ETAPA COMERCIAL

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|
| 7F-01 | Limitador de mastering | Función | Limitador/maximizador: ganancia + limitación | Un limitador de mastering sube la ganancia de la señal y simultáneamente limita lo que supera el umbral. El threshold actúa como control de ganancia de entrada: bajar el threshold X dB sube la señal X dB pero limita lo que supera ese umbral. El Out Ceiling define el techo de salida | — | Primero definir el objetivo de LUFS integrados y estimar cuántos dB de ganancia se necesitan. Usar el threshold para aportar esa ganancia; usar el Out Ceiling para establecer el techo de pico | Si se empieza a aplicar limitación sin un objetivo de loudness definido, es fácil sobrepasar sin criterio o quedarse corto | Girar el threshold máximo sin definir cuánto se quiere subir, aplicando una cantidad indefinida de compresión/limitación | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7F-02 | Limitador de mastering | Comparación | Método delta de verificación | Para verificar si el limitador está introduciendo daño no perceptible a oído, se puede usar el método delta: invertir la polaridad de la señal limitada y sumarla con la señal original. El resultado debería ser casi silencio si el limitador no introdujo cambios sustanciales; si se escucha algo, eso es lo que el limitador modificó | Escuchar la diferencia (delta) al mismo nivel que la señal original para verificar si el daño introducido es relevante | Si el delta suena principalmente a transitores levemente recortados, el limitador está trabajando bien. Si el delta suena a distorsión generalizada, hay sobrecompresión | Aprobar el trabajo del limitador solo a oído sin comparar la señal original con la señal procesada en igualdad de nivel | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7F-03 | Limitador de mastering | Release y distorsión | Relación entre release del limitador y distorsión | Un release demasiado rápido en el limitador puede generar distorsión cuando la señal tiene componentes de baja frecuencia de período largo. El limitador está diseñado para picos breves; si el release es muy rápido, actúa sobre porciones de onda más grandes y produce distorsión armónica no deseada | — | Release más corto → más volumen posible, más distorsión. Release más largo → menos distorsión, menos volumen. Ajustar el balance según el objetivo del master y el contenido frecuencial del material | Si el limitador colorea y suena duro, antes de descartarlo verificar si el release automático puede pasarse a manual y alargarse | Mantener el release en automático en todos los casos sin considerar que para cierto material (graves sostenidos, cuerdas, pads) un release más largo puede ser necesario | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7F-04 | True Peak | Definición | True Peak y picos entre muestras | El True Peak (dBTP) mide los picos de reconstrucción analógica que ocurren entre muestras, que no son visibles en una lectura peak de datos convencional pero pueden producir clipping durante la conversión D/A o la codificación del archivo | True Peak recomendado para streaming: entre –1 dBTP y –0,3 dBTP según la plataforma | El true peak de –1 dBTP es una convención ampliamente adoptada; protege contra el overshooting que ocurre durante la codificación a formatos comprimidos (MP3, AAC) | No medir el True Peak y usar solo el Peak convencional, asumiendo que si el peak es –0,1 dBFS no habrá saturación en la conversión o la codificación | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7F-05 | True Peak | Overshoot en codificación | Peligro del archivo codificado | Al codificar el archivo WAV/AIFF a MP3 o AAC, el proceso de codificación puede producir overshooting: picos que superan 0 dBFS aunque el archivo de 24 bits estuviera por debajo. El True Peak en el archivo de 24 bits no garantiza que el archivo codificado no sature | — | Analizar el archivo codificado con un medidor de True Peak después del proceso de codificación para verificar que el overshoot de la codificación no haya generado clipping | Una canción entregada con –1 dBTP en 24 bits puede terminar con picos de +0,3 dBTP o más en el MP3 o AAC resultante | Asumir que controlar el True Peak en el archivo de entrega es suficiente sin verificar el archivo codificado resultante | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE G — TARGETS DE PLATAFORMAS Y OPTIMIZACIÓN

| # | Tema | Subtema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|
| 7G-01 | Targets | Normalización en plataformas | Cómo actúa la normalización de loudness | Las plataformas de streaming miden el LUFS integrado del material y ajustan el volumen de reproducción para igualarlo a su target. Si el material está por encima del target, la plataforma baja el volumen de reproducción (no comprime ni procesa el audio; solo ajusta la ganancia de reproducción). Si está por debajo, puede subirlo (no todas las plataformas) o reproducirlo como está | — | La normalización de la plataforma no afecta la calidad del audio ni comprime la señal; solo ajusta el volumen de reproducción. No es dithering ni conversión adicional | La normalización no penaliza la dinámica del material; un master con PLR alto reproducido a –14 LUFS sigue sonando dinámico | Creer que masterizar fuerte "gana" en competitividad porque las plataformas no normalizan o se puede desactivar; las plataformas con normalización activada por defecto reproducen todos los materiales a su target independientemente de cómo llegaron | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7G-02 | Targets | Valores actuales | Targets de LUFS por plataforma | Referencia de targets de LUFS integrados por plataforma (sujetos a cambio; verificar en la documentación oficial de cada plataforma) | Spotify: –14 LUFSi · Apple Music: –16 LUFSi · YouTube: –14 LUFSi · Tidal: –14 LUFSi · Broadcast (EBU R128): –23 LUFSi | Para distribución en streaming, un master entre –10 y –14 LUFSi permite competitividad en la mayoría de los géneros sin sacrificar dinámica | Un master a –7 LUFSi en Spotify se escuchará al mismo volumen que uno a –14 LUFSi porque la plataforma baja el más fuerte al target; la diferencia es que el de –7 tiene menos dinámica | Masterizar al valor exacto del target de la plataforma como objetivo universal cuando el género puede requerir un valor distinto | HEURÍSTICA OPERATIVA REFORMULABLE | REFORMULAR MÁS |
| 7G-03 | Targets | Criterio por género | El LUFS objetivo depende del género | El nivel de loudness en el master depende del género y del contexto de escucha. No existe un único target "correcto": la música electrónica, el trap y el reggaetón tienden a targets más altos (–8 a –10 LUFSi); la música acústica, el jazz y la música orquestal se benefician de targets más dinámicos (–16 a –18 LUFSi) | — | Llevar un material a –10 LUFSi no implica necesariamente sacrificar dinámica; depende de cuánta compresión se aplica para lograrlo. Con el procesamiento correcto puede llegar a –10 con PLR de 10–12 | Fijar el target de LUFS sin considerar el género ni el rango dinámico intencional del material | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE H — DITHERING Y ENTREGA DIGITAL

| # | Tema | Subtema | Concepto técnico | Definición neutra | Fórmula / Relación | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|---|---|---|
| 7H-01 | Dithering | Definición | Dither: qué es y para qué sirve | Al exportar desde 32 bit float (motor de la DAW) o 24 bits a 16 bits, hay una reducción de la resolución de amplitud. El dithering añade ruido de muy bajo nivel (por debajo del piso de cuantización) antes de la conversión, lo que reduce la distorsión de cuantización que resultaría del truncamiento directo | Truncamiento: redondear al escalón más cercano → distorsión de cuantización no lineal. Dithering: añadir ruido aleatorio de bajo nivel → la distorsión de cuantización se convierte en ruido lineal, menos perceptible | Aplicar dither siempre que se realice una conversión de profundidad de bits hacia abajo (24→16, 32→24, 32→16). No aplicar dither si se exporta a la misma profundidad | El dither solo se aplica una vez, en la conversión final. Si el archivo de 16 bits resultante se vuelve a abrir y procesar, no se aplica dither otra vez hasta la próxima exportación definitiva | Exportar a 16 bits sin dithering para "mantener la señal limpia", generando en realidad distorsión de cuantización que es más perceptible que el ruido del dither | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7H-02 | Dithering | Noise shaping | Noise shaping: optimización del ruido de dither | El noise shaping es un proceso que redistribuye el ruido del dithering hacia las frecuencias donde el oído es menos sensible (alta frecuencia), reduciendo la percepción del ruido en las zonas de mayor sensibilidad auditiva (medios). El ruido total del sistema no disminuye; se mueve a zonas menos perceptibles | — | Usar noise shaping cuando se quiere minimizar la audibilidad del dither. Tipos 1 y 2 son las configuraciones más comunes; el tipo más agresivo mueve más ruido hacia la alta frecuencia pero puede aumentar el nivel de ruido en esas zonas | El noise shaping puede traer compensaciones: mueve el ruido a frecuencias menos audibles pero si se aplica de forma excesiva puede aumentar el nivel de ruido en el extremo alto | Aplicar noise shaping agresivo sin considerar que puede introducir ruido audible en alta frecuencia | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7H-03 | Dithering | Cuándo aplicar | Condiciones de aplicación del dither | El dither se aplica exclusivamente cuando se reduce la profundidad de bits. No se aplica si se exporta a la misma profundidad; no se aplica en múltiples etapas del proceso; se aplica una sola vez, en la conversión final hacia el formato de entrega | — | Para entrega a streaming (usualmente 24 bits, aunque las plataformas comprimen internamente): no aplicar dither si se exporta a 24 bits. Para entrega en CD (16 bits): aplicar dither en la conversión 24→16. Para archivos de trabajo intermedios: no aplicar dither | Si el master de trabajo está en 32 bit float y se exporta para guardar en 24 bits como backup, no es necesario dither; si ese archivo de 24 bits va después a 16 bits para CD, el dither va ahí | Aplicar dither en cada exportación "por si acaso" sin considerar si hay reducción real de profundidad de bits | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7H-04 | Resampleo | Definición | Resampleo: cambio de frecuencia de muestreo | El resampleo es el proceso de cambiar la frecuencia de muestreo de una señal digital. El resampleo introduce artifacts si no se realiza correctamente; los mejores convertidores aplican interpolación de alta calidad. En el DAW, el resampleo puede introducir aliasing si el SRC (Sample Rate Conversion) del DAW no es de alta calidad | — | Para entregar a plataformas de streaming que aceptan 44,1 kHz o 48 kHz, si el proyecto está a 96 kHz hay que resamplear. Usar el SRC de mayor calidad disponible o una aplicación externa especializada | El resampleo dentro del DAW no siempre produce resultados de la misma calidad que un SRC externo especializado; comparar los resultados antes de elegir el método | Asumir que todos los algoritmos de resampleo producen resultados idénticos en calidad | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

### BLOQUE I — MASTERING DE ÁLBUM

| # | Tema | Concepto técnico | Definición neutra | Criterio operativo | Heurística útil | Error frecuente | Categoría | Acción |
|---|---|---|---|---|---|---|---|
| 7I-01 | Álbum vs single | Diferencia de contexto | Para un single no hay horizonte; la optimización es maximizar esa canción sin restricciones externas. Para un álbum, todas las canciones deben convivir en equilibrio, con una identidad recognizable como conjunto, aunque cada una conserve su carácter individual | — | La diferencia entre mastering de single y álbum no es técnica sino de criterio: en álbum cada decisión debe evaluarse también en relación con el conjunto | Una canción que suena perfecta sola puede sonar desproporcionada dentro del álbum; el contexto del álbum cambia la evaluación de cada canción | Aplicar el mismo criterio de single a cada canción del álbum sin comparar la coherencia del conjunto | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |
| 7I-02 | Coherencia | "Bajo un mismo techo" | En un álbum, todas las canciones deben "sonar al mismo disco" aunque difieran en carácter, densidad o intensidad. El concepto de "mismo techo" no significa mismo volumen ni mismo timbre; significa identidad recognizable como producción coherente | — | Comparar constantemente con las demás canciones del álbum durante el proceso de cada canción; tomar decisiones en relación con el conjunto | Una canción puede necesitar más bajo por su carácter; esa decisión es válida si no rompe la coherencia con el resto del álbum | Masterizar cada canción del álbum en sesiones separadas sin referencias cruzadas entre ellas | HEURÍSTICA OPERATIVA REFORMULABLE | REFORMULAR MÁS |
| 7I-03 | Nivelación | Nivelación de sonoridad del álbum | Nivelar las canciones del álbum no significa que todas tengan el mismo LUFS integrado; significa que la experiencia de escucha del álbum completo sea fluida y que los cambios de sonoridad entre canciones sean intencionales, no accidentales | — | Ajustar los niveles entre canciones con el criterio musical del álbum: puede ser válido que una balada sea más suave que un tema de hard rock dentro del mismo álbum, siempre que sea una decisión deliberada | Si las mezclas del álbum llegaron bien calibradas (Eje 6), la nivelación en mastering puede ser mínima; si llegaron muy disparejas, el trimming de entrada es más importante | Igualar todos los LUFS integrados del álbum a un único valor de referencia sin considerar que algunas canciones por su naturaleza y género deben ser más dinámicas que otras | DOCTRINA GENERAL REUTILIZABLE | REUTILIZAR |

---

## 3. CONTENIDO ATRIBUIBLE DEL EJE

| Bloque | Atribución requerida | Etiqueta recomendada |
|---|---|---|
| PDF: Apunte Mastering 2022 | Autoría: Pablo Rabinovich. La clasificación en tres etapas (técnica, estética, comercial), el flujo de procesos habituales, los criterios de filtrado y compresión son del apunte. La doctrina técnica subyacente es de dominio general del campo | Reformular; citar si se usa la formulación directamente |
| Método delta para verificar el limitador | Técnica bien conocida en el campo de mastering (no es exclusiva del autor fuente); presentada en clase con su implementación específica (inversión de polaridad + suma) | Doctrina general del campo; no requiere atribución al docente fuente; es una técnica estándar |
| "Bajo un mismo techo" como criterio de coherencia de álbum | Formulación del autor fuente en el apunte de mastering. El concepto es de dominio general del campo; la formulación específica es del apunte | Reformular; el concepto es reutilizable sin atribución |
| Referencia al libro "El arte y la ciencia del mastering" de Bob Katz | Libro de Bob Katz; referencia bibliográfica independiente del autor fuente | Citar como fuente externa si se recomienda |

---

## 4. BLOQUEOS DEL EJE

| Bloque bloqueado | Tipo de riesgo | Por qué no debe pasar |
|---|---|---|
| Clase de mastering presentada como "lo que muestra es cómo lo hago yo" | EXPRESIÓN NO REUTILIZABLE | El docente fuente marca explícitamente su práctica personal; identificable |
| Anécdota de Sound Forge en 1995 y el "renderizado por separado" | EXPRESIÓN NO REUTILIZABLE | Historia personal del docente fuente con fecha y contexto específico |
| "Esto es recontra fino el mastering" | EXPRESIÓN NO REUTILIZABLE | Formulación oral muy marcada del docente fuente |
| Comentario sobre T-Racks: "vi cosas que me llamaron la atención" | EXPRESIÓN NO REUTILIZABLE | Opinión personal del docente fuente; identificable con su estilo de clase |
| Secuencia pedagógica del temario fuente para el módulo de mastering: técnica → comercial → artística en ese orden específico como "dogma" | ESTRUCTURA NO REUTILIZABLE | La secuencia es la del autor fuente; la lógica subyacente (etapas diferenciadas) es reformulable |
| "El mastering es un proceso recontrafino" | EXPRESIÓN NO REUTILIZABLE | Formulación oral del docente fuente |
| "No hago videos de TikTok, hago capacitación técnica" | EXPRESIÓN NO REUTILIZABLE | Frase de contexto autobiográfico del docente fuente |
| Recomendaciones específicas de plugins como "prefiero otros limitadores aunque use este para enseñar" | EXPRESIÓN NO REUTILIZABLE | Opinión personal del docente fuente sobre herramientas específicas |

---

## 5. VACÍOS Y TENSIONES DEL EJE

| Tipo | Descripción | Implicación para redacción |
|---|---|---|
| **Vacío** | La **reparación de audio** (limpieza de clics, ruidos puntuales) aparece en la arquitectura KENTH como parte de la subsección de preparación de Eje 7, pero no tiene desarrollo técnico propio en las fuentes del módulo de mastering. La Clase 28 muestra RX para DC offset y asimetrías, pero no para eliminación de ruidos puntuales | Al redactar: construir el criterio básico de limpieza de ruidos puntuales desde doctrina general o reducir a una mención operativa |
| **Vacío relativo** | Los **clippers en mastering** (relación con el limitador final, cuándo usar uno u otro) están en la lista de la arquitectura KENTH y brevemente mencionados en las clases de mastering, pero sin el mismo desarrollo que los limitadores | Al redactar: la doctrina de clippers (del Eje 4) aplica aquí en contexto de mastering; ampliar con criterio de contexto pero sin desarrollar nuevamente la mecánica |
| **Vacío relativo** | El **resampleo dentro del DAW** como problema tiene cobertura en el apunte de mastering pero poca profundidad práctica en las transcripciones. Los criterios de SRC de calidad son mencionados pero no desarrollados | Al redactar: la doctrina técnica de resampleo está disponible (apunte mastering, Clase 25); la comparación entre métodos de SRC necesita fuentes externas |
| **Tensión de límite** | La distinción entre **etapa artística** y **etapa estética** del mastering en las fuentes presenta una ligera inconsistencia: el apunte las llama Técnica / Estética / Comercial; las clases las llaman Técnica / Comercial / Artística. Son dos formulaciones distintas del mismo concepto | Al redactar: usar una sola terminología y ser consistente. La lógica subyacente (hay una etapa de corrección técnica, una de optimización de nivel, y una optativa de carácter) es la misma en ambas versiones |
| **Tensión de límite** | Los **targets de LUFS** de las plataformas pueden haber cambiado desde la fecha de las fuentes. La arquitectura KENTH indica verificar en documentación oficial de cada plataforma | Al redactar: siempre incluir nota de que los valores deben verificarse en las fuentes oficiales de cada plataforma; no presentarlos como definitivos |
| **Tensión de cruce con Eje 0** | El **dithering** y la **entrega de bits** cruzan con el Eje 0-B (bits, coma fija/flotante, headroom digital). En Eje 0 se introdujo el concepto; en Eje 7 se aplica al contexto de la entrega final del master | Al redactar: en Eje 7, el dithering se presenta como aplicación final de los conceptos ya conocidos de Eje 0; no repetir la doctrina técnica básica de bits sino referenciar el cruce |
| **Cruce activo con Eje 5** | El MS en mastering (Eje 7) usa exactamente la misma mecánica de codificación/decodificación que el MS en mezcla (Eje 5). La diferencia es el escenario de uso y el alcance de la intervención | Al redactar: declarar el cruce explícitamente; la mecánica M/S ya se conoce de Eje 5; Eje 7 desarrolla las aplicaciones específicas en el contexto del programa completo entregado |

---

## 6. PAQUETE LIMPIO DEL EJE

### EJE 7 — TRADUCCIÓN Y ENTREGA · Paquete limpio para proyecto generativo

---

**FUNCIÓN DEL EJE:** El mastering es la última instancia de corrección y la etapa de preparación del programa para su distribución. No arregla mezclas: traduce lo que hay al formato en que debe existir. Es el ciclo LDOV a escala del proceso completo.

---

#### BLOQUE A — DEFINICIÓN Y ETAPAS

**Doctrina reutilizable:**
- El mastering prepara un programa fonográfico para su distribución. Es global: cualquier procesamiento afecta a todos los elementos del programa simultáneamente
- El mastering no está diseñado para corregir mezclas; está diseñado para retocar desajustes de índole general. Si el problema viene de un elemento específico, debió resolverse en la mezcla
- Diferencia entre nivel general y elemento específico: si el bajo de un instrumento suena mal → mezcla; si los graves de la canción son excesivos → mastering
- Tres etapas (la artística puede estar o no): Técnica (corregir problemas formales de la señal) → Comercial (llevar al nivel de sonoridad del destino) → Artística optativa (carácter, color, cambios deliberados)
- La etapa técnica siempre precede a la comercial

**Advertencias:**
- CRUCE → EJE 6: el nivel de entrega de la mezcla y el headroom al entregar para mastering son Eje 6. El Eje 7 arranca desde lo que Eje 6 entregó

---

#### BLOQUE B — PREPARACIÓN Y REPARACIÓN

**Doctrina reutilizable:**
- Trimming: ajustar el clip gain de la mezcla antes de la cadena de mastering para que los procesadores operen en su rango óptimo (~–20 a –23 LUFSi de entrada si se usan modelados analógicos)
- DC offset: desplazamiento de toda la forma de onda fuera del cero. Corrección: HPF muy bajo (5–10 Hz) o herramienta específica de offset. No intervenir si el valor es despreciable (≤0,0xx%)
- Asimetría de forma de onda: señal centrada pero con picos desiguales entre semiciclos. Corrección: filtro AllPass (rota la fase entre componentes frecuenciales sin modificar amplitudes). Consecuencia de no corregirla: se llega antes al techo del lado más cargado, reduciendo el headroom útil
- DC offset ≠ asimetría: son fenómenos distintos con correcciones distintas. Orden: corregir DC offset primero (HPF), asimetría después (AllPass)
- Verificar siempre el resultado de la corrección antes de asumir que fue útil; una corrección técnica puede introducir problemas si no se monitorea el resultado

**Advertencias:**
- CRUCE → EJE 0 y 1: DC offset y AllPass son conceptos introducidos en Eje 0 y usados como diagnóstico en Eje 1; en Eje 7 se aplican como corrección previa a la cadena de mastering
- VACÍO: reparación de ruidos puntuales tiene cobertura mínima en las fuentes; construir desde fuentes externas o reducir a criterio básico

---

#### BLOQUE C — MEDICIÓN Y CORRECCIÓN

**Doctrina reutilizable:**
- Analizar nivel, fase y espectro antes de insertar cualquier procesador
- HPF subsónico: no es obligatorio por defecto; solo si el análisis muestra energía problemática por debajo del fundamento de la canción
- Resonancias en mastering: afectan al conjunto del programa. Corrección: EQ paramétrico (resonancias estáticas) o EQ dinámico (resonancias intermitentes). EQ en modo MS permite correcciones selectivas por zona de campo estéreo
- Balance L/R: si la mezcla está más cargada en un canal, herramientas de mono maker pasan gradualmente a mono por debajo de una frecuencia para reequilibrar los graves

**Advertencias:**
- CRUCE → EJE 1: el diagnóstico de mastering usa los mismos instrumentos de lectura de Eje 1 (analizador, goniómetro, correlatómetro, medidor de nivel)

---

#### BLOQUE D — COMPRESIÓN Y SATURACIÓN

**Doctrina reutilizable:**
- Varios pasos pequeños dan mejores resultados que grandes saltos en pocos pasos
- Compresión en serie: primero compresor musical (valvular) para consistencia → segundo compresor preciso (VCA) para picos
- Compresión paralela: en mastering, sube el nivel de los pasajes más suaves mezclando con el original sin aplastarlo. Costo: posible aliasing y distorsión con envolventes rápidas
- Compresión ascendente: levanta los pasajes más bajos sin tocar los más fuertes; alternativa más transparente a la compresión paralela agresiva
- Saturación en mastering: riqueza armónica y densidad percibida. Si se escucha como distorsión, hay demasiada. Comparar siempre en igualdad de nivel

---

#### BLOQUE E — MS E IMAGEN ESTÉREO EN MASTERING

**Doctrina reutilizable:**
- El procesamiento MS en mastering opera sobre el programa completo: Mid = contenido central (voz, graves, bombo); Side = contenido lateral. Modificar el Mid modifica todos los elementos del centro simultáneamente
- Imagen estéreo por bandas: mantener los graves más centrados (mono) aumenta el peso percibido y la estabilidad. Abrir a medida que sube la frecuencia
- Una resonancia alojada en Mid (p.ej., del snare) puede corregirse en el canal Mid sin afectar el Side

**Advertencias:**
- LÍMITE Eje 5 / Eje 7: la mecánica M/S ya se conoce de Eje 5. En Eje 7 el MS opera sobre el programa completo entregado, no sobre elementos individuales de la mezcla

---

#### BLOQUE F — LIMITACIÓN Y TRUE PEAK

**Doctrina reutilizable:**
- El limitador de mastering sube la ganancia (threshold como control de entrada) y limita lo que supera ese umbral. Out Ceiling define el techo de salida
- Regla de comparación: siempre comparar la señal limitada con la original en igualdad de nivel percibido. Linkear threshold y Out Ceiling de forma que se compensen al aplicar la ganancia
- Método delta: invertir la polaridad de la señal limitada y sumarla con la original; el resultado es lo que el limitador modificó. Escuchar a bajo nivel para evaluar el daño introducido
- Release del limitador: más corto → más volumen, más distorsión posible. Más largo → menos distorsión, menos volumen. Para material con componentes graves sostenidos, un release más largo puede ser necesario
- True Peak (dBTP): mide picos de reconstrucción entre muestras. Objetivo general: –1 dBTP para proteger contra overshooting en la codificación
- El archivo codificado (MP3/AAC) puede generar overshooting adicional: verificar el True Peak del archivo codificado, no solo del WAV de entrega

---

#### BLOQUE G — TARGETS Y OPTIMIZACIÓN

**Doctrina reutilizable:**
- La normalización de loudness de las plataformas ajusta el volumen de reproducción (ganancia), no comprime ni procesa el audio
- Spotify: –14 LUFSi · Apple Music: –16 LUFSi · YouTube: –14 LUFSi · Broadcast EBU R128: –23 LUFSi *(verificar en documentación oficial de cada plataforma; estos valores pueden actualizarse)*
- El target de LUFS del master depende del género y del PLR intencional del material
- Un material a –10 LUFSi puede ser perfectamente competitivo y dinámico si el PLR es adecuado (10–12 LU o más)

**Advertencias:**
- Los valores de targets de plataformas pueden cambiar; siempre verificar en la documentación oficial antes de publicar

---

#### BLOQUE H — DITHERING Y ENTREGA DIGITAL

**Doctrina reutilizable:**
- El dithering añade ruido de bajo nivel antes de la conversión de bits para convertir la distorsión de cuantización en ruido lineal menos perceptible
- Aplicar dither solo en conversiones hacia abajo (24→16, 32→16); no aplicar si se exporta a la misma profundidad
- El dither se aplica una sola vez, en la conversión final al formato de entrega definitivo
- Noise shaping: redistribuye el ruido del dither hacia frecuencias de menor sensibilidad auditiva. El ruido total no disminuye; se mueve a zonas menos perceptibles. Puede haber compensaciones si se aplica de forma agresiva
- Resampleo: cambio de SR puede introducir aliasing si el SRC no es de alta calidad; usar el mejor algoritmo disponible o aplicación externa especializada

**Atribuciones:**
- Apunte Mastering 2022: Rabinovich (reformular; doctrina técnica de dominio general)

**Advertencias:**
- CRUCE → EJE 0-B: la doctrina técnica de bits, coma fija/flotante y headroom digital ya se conoce de Eje 0; en Eje 7 se aplica al contexto de la entrega definitiva del master

---

#### BLOQUE I — MASTERING DE ÁLBUM

**Doctrina reutilizable:**
- Para un single: la optimización no tiene restricciones externas. Para un álbum: cada canción debe convivir con el resto; la identidad del conjunto define los límites de cada decisión individual
- Coherencia de álbum: todas las canciones deben pertenecer perceptualmente a la misma producción aunque difieran en carácter y densidad. El contexto del álbum cambia la evaluación de cada canción
- Nivelación de álbum: no significa LUFS iguales; significa que los cambios de sonoridad entre canciones sean intencionales. Si las mezclas llegaron bien calibradas, la nivelación en mastering puede ser mínima
- Referencia cruzada permanente durante el proceso: comparar constantemente con las canciones ya masterizadas del álbum para tomar decisiones en relación con el conjunto

**Advertencias:**
- CRUCE → EJE 6: la coherencia de álbum durante la mezcla (importar referencias de canciones anteriores) fue cubierta en Eje 6. En Eje 7 la coherencia se verifica y ajusta en el programa final entregado

---

*Paquete de Eje 7 listo para ingesta en Proyecto Generativo.*

*TODOS LOS EJES (0–7) HAN SIDO PROCESADOS. El proyecto de extracción forense KENTH Academy está completo.*