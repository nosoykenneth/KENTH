# 1. Lecciones piloto seleccionadas

1. **E2-L01 — HPF y LPF: cuándo filtrar de verdad**
   Elegida porque prueba muy bien si el tutor puede responder sobre **decisión operativa básica**, distinguir **solo vs mezcla**, y explicar **por qué se filtra** sin caer en recetas. Además deja muy claro el patrón “práctica primero, teoría en el punto de decisión”. 

2. **E2-L02 — Notch, AllPass y fase lineal: cada problema con su herramienta**
   Elegida porque fuerza al tutor a diferenciar **tipos de problema**: resonancia, fase y preservación de suma. Sirve para probar si el tutor corrige malas elecciones de herramienta y si sabe entrar en modo **troubleshooting**. 

3. **E3-L03 — EQ correctivo vs EQ estético**
   Elegida porque prueba una de las fronteras pedagógicas más valiosas del sistema: distinguir **quitar problema** de **construir carácter**. Es ideal para ver si el tutor entiende intención, no solo parámetros.

4. **E3-L06 — API, Neve, SSL y Pultec como decisiones tonales, no como fetiches**
   Elegida porque habilita preguntas comparativas muy útiles para demo: **qué usar y por qué**, sin reducirlo a marcas. Es perfecta para probar respuestas del tutor sobre **comparación entre herramientas** y elección por objetivo tonal.

5. **E4-L01 — Threshold, ratio y knee sin mirar solo numeritos**
   Elegida porque permite probar ayuda en **teoría aplicada**, lectura de **GR**, corrección de criterio y explicación de compresión desde resultado auditivo. Muy buena para validar asistencia contextual durante una demostración práctica. 

6. **E4-L06 — Paralela, serie y sidechain: tres montajes, tres usos**
   Elegida porque es la más fuerte para probar tutor sobre **ruteo**, **criterio operativo**, convivencia entre elementos y decisiones de montaje. También da preguntas muy naturales del alumno en video real.

Estas seis cubren variedad real de prueba: decisión técnica puntual, teoría aplicada, error frecuente, criterio operativo, comparación de herramientas y ayuda contextual por bloque. Además respetan la estructura congelada de lecciones ya definida para Ejes 2, 3 y 4. 

# 2. Paquete piloto por lección

## E2-L01

* **código:** E2-L01
* **título:** HPF y LPF: cuándo filtrar de verdad
* **eje:** Eje 2 — Integridad de la señal
* **objetivo:** enseñar a filtrar con criterio real, separando limpieza legítima de cortes arbitrarios
* **tipo de valor para la prueba:** criterio operativo + explicación práctica contextual
* **rol dentro del proceso:** primera operación real del eje; limpia antes de moldear carácter 
* **learning goal:** distinguir cuándo un filtro elimina basura, cuándo delimita registro y cuándo hace ceder espacio en mezcla
* **expected action:** aplicar HPF o LPF inicial con punto de corte y pendiente razonados, verificando solo y mezcla

### bloques del video

1. **Apertura** — problema visible en analizador; duda real sobre si esa energía pertenece al instrumento
2. **Planteamiento del problema** — diferencia entre cortar por costumbre y filtrar con criterio
3. **Demostración práctica** — lectura en solo, barrido del HPF, escucha de lo que desaparece
4. **Demostración práctica en contexto** — mezcla completa, conflicto con bajo/piano
5. **Teoría aplicada** — tres preguntas que justifican el filtrado
6. **Criterio de decisión** — cuándo conservar, cuándo ceder espacio
7. **Errores frecuentes** — falsas reglas sobre HPF/LPF
8. **Cierre**

### timestamps funcionales propuestos

* **00:00–00:35** apertura
* **00:35–01:20** planteamiento del problema
* **01:20–03:20** demostración práctica en solo
* **03:20–04:50** demostración práctica en mezcla
* **04:50–06:00** teoría aplicada
* **06:00–06:50** criterio de decisión
* **06:50–07:40** errores frecuentes
* **07:40–08:00** cierre

### preguntas probables del alumno por bloque

* **Apertura:** “¿Cómo sé si eso de abajo es basura o cuerpo real?”
* **Solo:** “¿El HPF siempre se mueve desde abajo?” / “¿Hasta qué punto puedo subirlo?”
* **Mezcla:** “Si en solo suena mejor sin corte, ¿por qué en mezcla sí conviene?”
* **Teoría aplicada:** “¿Filtrar es EQ correctivo o es otra cosa?”
* **Errores frecuentes:** “¿Entonces no todas las pistas llevan HPF?”

### modo del tutor por bloque

* **00:00–01:20:** práctica + navegación de recurso
* **01:20–04:50:** práctica + troubleshooting
* **04:50–06:50:** teoría + criterio operativo
* **06:50–08:00:** corrección de criterio

### interaction_mode dominante por bloque

* apertura: `navegación de recurso`
* problema: `criterio operativo`
* solo: `práctica`
* mezcla: `práctica`
* teoría: `teoría`
* decisión: `criterio operativo`
* errores: `troubleshooting`

### preguntas_probables

* “¿Qué diferencia hay entre limpiar y adelgazar?”
* “¿Corto en solo o en mezcla?”
* “¿Pendiente fuerte siempre es mejor?”
* “¿El LPF también puede usarse por perspectiva?”

---

## E2-L02

* **código:** E2-L02
* **título:** Notch, AllPass y fase lineal: cada problema con su herramienta
* **eje:** Eje 2 — Integridad de la señal
* **objetivo:** distinguir cuándo conviene Notch, AllPass o fase lineal
* **tipo de valor para la prueba:** troubleshooting + corrección de herramienta equivocada
* **rol dentro del proceso:** evita operar mal un diagnóstico correcto; profundiza preparación técnica antes del tono 
* **learning goal:** clasificar correctamente si el problema es de amplitud localizada, relación de fase o preservación de suma
* **expected action:** seleccionar herramienta correcta según el tipo de fallo y verificar su efecto de forma pertinente

### bloques del video

1. **Apertura** — “diagnosticar bien y operar mal”
2. **Caso 1:** resonancia puntual → Notch
3. **Caso 2:** problema entre señales → AllPass
4. **Caso 3:** preservar fase → fase lineal
5. **Teoría aplicada**
6. **Criterio de decisión**
7. **Errores frecuentes**
8. **Cierre**

### timestamps funcionales propuestos

* **00:00–00:40** apertura
* **00:40–02:30** caso Notch
* **02:30–04:20** caso AllPass
* **04:20–05:50** fase lineal
* **05:50–06:50** teoría aplicada
* **06:50–07:40** criterio de decisión
* **07:40–08:30** errores frecuentes
* **08:30–08:50** cierre

### preguntas probables del alumno por bloque

* **Caso Notch:** “¿Cómo sé si la resonancia es lo bastante estrecha para notch?”
* **Caso AllPass:** “¿Por qué no lo escucho claro en solo?”
* **Fase lineal:** “¿Cuándo vale la pena aceptar latencia y pre-ringing?”
* **Criterio:** “¿Esto no se arreglaba mejor con alineación temporal?”
* **Errores:** “¿Fase lineal es la opción pro?”

### modo del tutor por bloque

* **00:00–00:40:** navegación de recurso
* **00:40–05:50:** troubleshooting
* **05:50–07:40:** teoría + criterio operativo
* **07:40–08:50:** corrección de criterio

### interaction_mode dominante por bloque

* apertura: `navegación de recurso`
* notch: `troubleshooting`
* allpass: `troubleshooting`
* fase lineal: `criterio operativo`
* teoría: `teoría`
* decisión: `criterio operativo`
* errores: `troubleshooting`

### preguntas_probables

* “¿Qué hago si al sumar se siente raro pero no veo pico espectral?”
* “¿AllPass corrige cualquier problema de fase?”
* “¿Notch muy estrecho puede empeorar el sonido?”
* “¿Cuándo conviene volver al filtro estándar?”

---

## E3-L03

* **código:** E3-L03
* **título:** EQ correctivo vs EQ estético
* **eje:** Eje 3 — Identidad espectral
* **objetivo:** separar quitar problemas de construir carácter; enseñar barrido para localizar antes de cortar
* **tipo de valor para la prueba:** teoría aplicada + criterio de intención
* **rol dentro del proceso:** organiza toda la lógica del EQ antes de seguir construyendo identidad tonal
* **learning goal:** identificar intención antes de tocar una banda de EQ
* **expected action:** clasificar la intervención como correctiva o estética y cambiar método de escucha según esa intención

### bloques del video

1. **Apertura** — un bajo con resonancia y además necesidad de carácter
2. **Planteamiento del problema** — dos tareas distintas mezcladas
3. **Demostración práctica correctiva** — barrido, localización, corte
4. **Demostración práctica estética** — construcción tonal en contexto
5. **Teoría aplicada**
6. **Criterio de decisión**
7. **Errores frecuentes**
8. **Cierre**

### timestamps funcionales propuestos

* **00:00–00:35** apertura
* **00:35–01:20** planteamiento del problema
* **01:20–03:10** EQ correctivo
* **03:10–04:50** EQ estético
* **04:50–05:50** teoría aplicada
* **05:50–06:40** criterio de decisión
* **06:40–07:30** errores frecuentes
* **07:30–07:50** cierre

### preguntas probables del alumno por bloque

* **Inicio:** “¿Cómo sé si estoy corrigiendo o coloreando?”
* **Correctivo:** “¿El barrido siempre se hace con boost y Q alto?”
* **Estético:** “¿Por qué esto ya no se decide en solo?”
* **Teoría:** “¿Toda sustracción es correctiva?”
* **Errores:** “¿Un canal puede sonar peor en solo y mejor en mezcla?”

### modo del tutor por bloque

* **00:00–01:20:** navegación de recurso + criterio operativo
* **01:20–04:50:** práctica
* **04:50–06:40:** teoría + criterio operativo
* **06:40–07:50:** corrección de criterio

### interaction_mode dominante por bloque

* apertura: `navegación de recurso`
* problema: `criterio operativo`
* correctivo: `práctica`
* estético: `práctica`
* teoría: `teoría`
* decisión: `criterio operativo`
* errores: `corrección de criterio`

### preguntas_probables

* “¿Esto lo escucho en solo o en contexto?”
* “¿Qué pasa si corto algo que en solo se oye bien?”
* “¿Todo boost es estético?”
* “¿Toda sustracción es correctiva?”

---

## E3-L06

* **código:** E3-L06
* **título:** API, Neve, SSL y Pultec como decisiones tonales, no como fetiches
* **eje:** Eje 3 — Identidad espectral
* **objetivo:** asociar familias de modelado a objetivos tonales concretos
* **tipo de valor para la prueba:** comparación entre herramientas
* **rol dentro del proceso:** aterriza el modelado analógico a decisiones útiles y no a prestigio de marca
* **learning goal:** elegir familia de EQ modelado a partir del objetivo tonal
* **expected action:** comparar familias y escoger una por función, no por fama

### bloques del video

1. **Apertura** — varios modelados en pantalla
2. **API: frontalidad y presencia**
3. **Neve: cuerpo y brillo amable**
4. **SSL: lógica de canal y flujo**
5. **Pultec: peso con limpieza relativa**
6. **Teoría aplicada**
7. **Criterio de decisión**
8. **Errores frecuentes y cierre**

### timestamps funcionales propuestos

* **00:00–00:35** apertura
* **00:35–01:40** API
* **01:40–02:45** Neve
* **02:45–03:45** SSL
* **03:45–05:00** Pultec
* **05:00–05:50** teoría aplicada
* **05:50–06:50** criterio de decisión
* **06:50–07:30** errores + cierre

### preguntas probables del alumno por bloque

* **API:** “¿Esto me sirve para sacar algo al frente?”
* **Neve:** “¿Cómo consigo brillo sin dureza?”
* **SSL:** “¿Cuándo me conviene por flujo más que por color?”
* **Pultec:** “¿Cómo puede boost y attenuate a la vez tener sentido?”
* **Criterio:** “¿Hay una familia correcta por instrumento?”

### modo del tutor por bloque

* **00:00–05:00:** criterio operativo + comparación de herramientas
* **05:00–06:50:** teoría + criterio operativo
* **06:50–07:30:** corrección de criterio

### interaction_mode dominante por bloque

* apertura: `navegación de recurso`
* API/Neve/SSL/Pultec: `criterio operativo`
* teoría: `teoría`
* decisión: `criterio operativo`
* cierre: `corrección de criterio`

### preguntas_probables

* “¿Cuál me conviene para presencia?”
* “¿Cuál para densidad sin agresividad?”
* “¿SSL es solo por color o por canal completo?”
* “¿Pultec es realmente útil o solo famoso?”

---

## E4-L01

* **código:** E4-L01
* **título:** Threshold, ratio y knee sin mirar solo numeritos
* **eje:** Eje 4 — Energía y movimiento
* **objetivo:** entender la curva de transferencia desde el resultado auditivo y el GR
* **tipo de valor para la prueba:** teoría aplicada + ayuda operativa en dinámica
* **rol dentro del proceso:** entrada real al eje de compresión; fija vocabulario y lectura de acción del compresor 
* **learning goal:** comprender cuándo entra el compresor, cuánto contiene y cómo entra esa compresión
* **expected action:** ajustar threshold, ratio y knee con intención y comparar con bypass compensado

### bloques del video

1. **Apertura** — voz con saltos de nivel
2. **Makeup en cero**
3. **Threshold** — punto de entrada
4. **Ratio** — intensidad de contención
5. **Knee** — tipo de transición
6. **Teoría aplicada**
7. **Criterio de decisión**
8. **Errores frecuentes**
9. **Cierre**

### timestamps funcionales propuestos

* **00:00–00:40** apertura
* **00:40–01:10** makeup en cero
* **01:10–02:50** threshold
* **02:50–04:00** ratio
* **04:00–05:00** knee
* **05:00–06:00** teoría aplicada
* **06:00–06:50** criterio de decisión
* **06:50–07:40** errores frecuentes
* **07:40–08:00** cierre

### preguntas probables del alumno por bloque

* **Threshold:** “¿Bajo hasta que siempre comprima?”
* **Ratio:** “¿Más ratio siempre es más control?”
* **Knee:** “¿Soft knee es siempre más musical?”
* **Teoría:** “¿Por qué no me guío solo por el número del panel?”
* **Decisión:** “¿Cómo sé si ya me pasé?”

### modo del tutor por bloque

* **00:00–05:00:** práctica + criterio operativo
* **05:00–06:50:** teoría
* **06:50–08:00:** corrección de criterio

### interaction_mode dominante por bloque

* apertura: `navegación de recurso`
* makeup: `criterio operativo`
* threshold: `práctica`
* ratio: `práctica`
* knee: `práctica`
* teoría: `teoría`
* decisión: `criterio operativo`
* errores: `corrección de criterio`

### preguntas_probables

* “¿Qué miro: número o GR?”
* “¿Cómo comparo sin engañarme por volumen?”
* “¿Cuándo quiero knee duro?”
* “¿Threshold bajo significa mejor control?”

---

## E4-L06

* **código:** E4-L06
* **título:** Paralela, serie y sidechain: tres montajes, tres usos
* **eje:** Eje 4 — Energía y movimiento
* **objetivo:** entender tres montajes de compresión y cuándo usar cada uno
* **tipo de valor para la prueba:** criterio operativo + ruteo + convivencia entre elementos
* **rol dentro del proceso:** pasa de parámetros a arquitectura de uso; muy fuerte para prueba contextual de tutor
* **learning goal:** distinguir densidad, reparto de tareas y cesión de espacio entre señales
* **expected action:** elegir entre compresión paralela, en serie o sidechain según el problema real

### bloques del video

1. **Apertura** — un solo compresor no siempre resuelve elegantemente
2. **Compresión paralela**
3. **Compresión en serie**
4. **Sidechain**
5. **Filtrado del sidechain**
6. **Teoría aplicada**
7. **Criterio de decisión**
8. **Errores frecuentes**
9. **Cierre**

### timestamps funcionales propuestos

* **00:00–00:35** apertura
* **00:35–02:00** compresión paralela
* **02:00–03:20** compresión en serie
* **03:20–04:40** sidechain
* **04:40–05:20** filtrado del sidechain
* **05:20–06:20** teoría aplicada
* **06:20–07:10** criterio de decisión
* **07:10–08:00** errores frecuentes
* **08:00–08:20** cierre

### preguntas probables del alumno por bloque

* **Paralela:** “¿Cómo agrego densidad sin matar transientes?”
* **Serie:** “¿Por qué dos compresores y no uno?”
* **Sidechain:** “¿Esto es para arreglar balance o para efecto?”
* **Filtrado:** “¿Por qué filtrar la ruta de detección y no el audio?”
* **Errores:** “¿Sidechain es obligatorio entre bombo y bajo?”

### modo del tutor por bloque

* **00:00–05:20:** práctica + criterio operativo + troubleshooting
* **05:20–07:10:** teoría + criterio operativo
* **07:10–08:20:** corrección de criterio

### interaction_mode dominante por bloque

* apertura: `navegación de recurso`
* paralela: `práctica`
* serie: `criterio operativo`
* sidechain: `práctica`
* filtro SC: `troubleshooting`
* teoría: `teoría`
* decisión: `criterio operativo`
* errores: `corrección de criterio`

### preguntas_probables

* “¿Cuándo paralelo y cuándo serie?”
* “¿Sidechain resuelve mala mezcla?”
* “¿Cómo lo hago sutil y no evidente?”
* “¿Por qué el detector escucha otra cosa?”

# 3. Orden recomendado de producción

1. **E2-L01**
   Es el arranque más simple y demostrable. Permite probar rápido timestamps, contexto por bloque y respuestas del tutor a una decisión concreta.

2. **E4-L01**
   Después conviene una lección donde el tutor tenga que explicar teoría aplicada mientras el alumno mira un plugin en pantalla.

3. **E3-L03**
   Luego una lección de criterio. Aquí validas si el tutor entiende intención pedagógica y no solo operación técnica.

4. **E2-L02**
   Después una lección de troubleshooting. Sirve para ver si el tutor corrige bien elecciones equivocadas.

5. **E4-L06**
   Luego una lección de ruteo y convivencia entre elementos. Muy útil para prueba más rica del asistente.

6. **E3-L06**
   Déjala después porque sirve muy bien como demo comparativa y de valor percibido, pero depende menos del contexto minuto a minuto que las anteriores.

# 4. Qué validaría cada lección dentro del asistente

* **E2-L01**
  Valida **contexto por bloque/timestamp**, ayuda operativa básica y corrección de falsas reglas sobre filtrado.

* **E2-L02**
  Valida **troubleshooting** real: identificar si el problema es resonancia, fase o suma crítica, y no recomendar la herramienta equivocada. 

* **E3-L03**
  Valida **explicación conceptual** y **corrección de criterio**: si el tutor distingue intención correctiva vs estética y cambia su ayuda según eso.

* **E3-L06**
  Valida **comparación entre herramientas** y razonamiento por objetivo tonal, no por receta ni por marca.

* **E4-L01**
  Valida **teoría aplicada en tiempo real**, lectura de GR y ayuda para no interpretar mal los controles del compresor. 

* **E4-L06**
  Valida **ayuda operativa**, **criterio de montaje**, preguntas sobre sidechain y decisiones de convivencia entre elementos dentro de una mezcla.

En conjunto, este lote ya sirve como paquete piloto funcional: cubre lectura del contexto de video, cambio de modo de ayuda por bloque, explicación práctica, teoría aplicada, troubleshooting, comparación de herramientas y corrección de criterio sin reescribir los guiones ni cambiar la arquitectura del curso.
