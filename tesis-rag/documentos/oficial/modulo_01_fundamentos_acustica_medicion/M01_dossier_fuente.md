---
course_id: mezcla_masterizacion_kenth
module_id: M01
module_order: 1
module_title: Fundamentos fisicos, acustica y medicion
module_slug: fundamentos-fisicos-acustica-medicion
doc_type: source_dossier
source_origin: author_compiled_from_transcripts
filename: M01_dossier_fuente.md
version: 0.1
status: draft_source_compilation
curation_source: extraccion_exhaustiva_notebooklm_desde_clases_definitivas
ready_for_indexing: false
---

# M01 — Dossier fuente exhaustivo
## Fundamentos fisicos, acustica y medicion

> Este documento NO es guia canonica.
> NO es FAQ.
> NO es glosario final.
> Es una fuente intermedia exhaustiva, reorganizada por modulo, construida a partir de clases definitivas corregidas.
> Su objetivo es preservar detalle, matices, ejemplos, advertencias y trazabilidad antes de condensar doctrina para el RAG.

---

## 1. Alcance del dossier

Este dossier reúne contenido perteneciente al Módulo 1 aunque haya aparecido:
- en clases introductorias,
- en clases que formalmente abren otros módulos,
- en preguntas de estudiantes,
- o como aclaraciones laterales del profesor.

La prioridad aquí es **no perder información**.  
La función de este documento es dejar reunido el material fuente del módulo antes de abstraerlo en:
- `M01_guia_canonica.md`
- `M01_faq.json`
- `M01_glosario.json`

---

## 2. Núcleo conceptual del módulo

### 2.1 Dominio temporal de la señal
- El oscilograma representa tiempo en el eje horizontal y amplitud en el eje vertical.
- Un ciclo es el recorrido completo de la onda.
- El período es el tiempo que tarda un ciclo en completarse.
- Corrección explícita del profesor: no es correcto decir “el período es lo que dura una frecuencia”; lo correcto es “lo que dura un ciclo de esa frecuencia”.
- La frecuencia depende del período:
  - `F = 1 / T`
  - `T = 1 / F`
- Si el período no varía, la onda es periódica y tiene frecuencia definida.

### 2.2 Ondas simples y complejas
- Una onda simple es una senoidal: una sola frecuencia.
- Una onda compleja es la suma de múltiples senoidales.
- Si la suma conserva patrón repetitivo, sigue siendo periódica.
- La frecuencia que “lleva el período” en una onda compleja periódica es la fundamental.
- Los componentes múltiplos enteros de la fundamental son parciales armónicos.
- Si no hay relación de múltiplo entero, se trata de parciales inarmónicos y la onda es aperiódica.

### 2.3 Distorsión armónica vs intermodulación
- Saturación moderada: puede introducir distorsión armónica útil o musical.
- Saturación excesiva: aparece distorsión por intermodulación, áspera, chillona y fatigante.
- Esto surge como respuesta a una pregunta de estudiante y no debe perderse.

### 2.4 Frecuencia vs tono
- La frecuencia es un hecho físico, medible y objetivo.
- El tono es una percepción subjetiva.
- Analogía del profesor:
  - frecuencia = temperatura
  - tono = sensación térmica
- No deben tratarse como sinónimos.

### 2.5 Variación de la percepción tonal con la amplitud
- Una misma frecuencia no siempre se percibe igual si cambia la amplitud.
- Por debajo de 1000 Hz, al aumentar nivel, suele percibirse un tono más bajo.
- Entre 1000 y 5000 Hz, el efecto se atenúa o desaparece.
- Por encima de 5000 Hz, al aumentar nivel, puede percibirse más agudo.

### 2.6 Curvas isofónicas
- El oído no es lineal.
- Al subir el volumen, parecen aparecer más graves y agudos.
- Esto genera autoengaño en mezcla o mastering si no se compara a mismo nivel.
- Esta idea reaparece también en clases posteriores, no solo en la parte inicial del curso.

### 2.7 Acústica fisiológica como base del audio
- Los controles de audio están diseñados a partir de cómo trabaja el oído.
- Esto incluye faders, paneo, ecualización y lectura espectral.
- El módulo no debe tratar la fisiología auditiva como adorno teórico: es base de comprensión.

---

## 3. Acústica física y sala

### 3.1 Dominio espacial de la frecuencia
- La onda sonora es una variación de presión que se propaga.
- Se usa como referencia de cálculo:
  - velocidad del sonido ≈ 343 m/s
- Si una dimensión de la sala coincide con la longitud de onda de una frecuencia o sus múltiplos, aparecen modos de sala.

### 3.2 Modos de sala
- No basta analizar un solo eje.
- Deben considerarse:
  - ancho
  - largo
  - alto
  - trayectorias complejas
- Ejemplo técnico conservable:
  - 3,43 m corresponden al ciclo completo de 100 Hz

### 3.3 Paneles acústicos vs resonadores
- Error común: intentar arreglar graves inflados con espuma o paneles absorbentes.
- Los graves inflados se controlan con resonadores.
- Las cancelaciones severas a veces ni siquiera se resuelven así y exigen cambios arquitectónicos.

### 3.4 Difusión
- Analogía de la cuchara bajo el chorro de agua.
- La difusión reparte energía, no la absorbe.
- Solución doméstica aceptable: biblioteca llena de libros detrás de la posición de escucha.

---

## 4. Monitoreo y sistemas de escucha

### 4.1 Monitores y pared
- Muy cerca de la pared: aumento en graves.
- Al alejar el monitor, eventualmente aparece cancelación por recorrido hacia atrás y rebote.
- No existe ubicación físicamente perfecta.
- Ideal teórico: monitores empotrados, poco viable en la práctica.

### 4.2 Tweeters y direccionalidad
- Los agudos son muy direccionales.
- Los tweeters deben estar a la altura del oído y apuntar directamente al oyente.
- Error típico:
  - mal posicionamiento físico
  - luego compensado erróneamente con ecualización

### 4.3 Orientación vertical/horizontal del gabinete
- Si un monitor fue pensado para uso vertical, acostarlo puede generar problemas serios en la zona de crossover.
- El problema aparece especialmente cuando el oyente se desplaza lateralmente.

### 4.4 Desacople
- Dos monitores sobre la misma mesa pueden transmitirse vibración por estructura sólida.
- Eso afecta especialmente señales fantasma centradas.
- Solución práctica:
  - desacople con material firme
  - evitar material demasiado blando que permita pivoteo

### 4.5 Auriculares vs monitores
- En monitores hay interacción interaural natural.
- En auriculares paneados duros no existe esa sombra acústica real.
- Esto simplifica artificialmente el campo estéreo y puede engañar en planos y balances.

### 4.6 Auriculares abiertos vs cerrados
- Cerrados:
  - más resonancias internas
  - más coloración en graves
- Abiertos:
  - menos resonancias
  - mejor referencia para mezcla
- Recomendación del docente: abiertos para mezclar.

### 4.7 Impedancia y factor de damping
- Regla operativa:
  - la impedancia del auricular debería ser aprox. 8 veces mayor que la de salida del amplificador
- Si no:
  - cambia respuesta en frecuencia
  - baja el damping
  - el transductor “queda flotando”
  - se ensucia el grave

### 4.8 Respuesta plana: matiz importante
- El monitor absolutamente plano no existe.
- Lo importante no es la fantasía de planitud perfecta, sino la capacidad del sistema profesional de soportar señal cruda sin distorsionar de forma burda.

### 4.9 Corrección por EQ del sistema
- Sí puede usarse corrección tipo Sonarworks.
- Pero no es magia:
  - introduce costos en fase o pre-ringing
  - el beneficio puede superar el costo en home studio
- Debe quedar como contenido útil pero con formulación prudente.

---

## 5. Medición espectral

### 5.1 Analizador de espectro
- Herramienta central del módulo.
- Se presenta como “la cinta métrica del audio”.
- Permite ver cosas que el oído no detecta bien:
  - subsónicas
  - acumulaciones
  - distorsiones
  - patrones energéticos

### 5.2 Ruido blanco y ruido rosa
- Ruido blanco:
  - misma energía por frecuencia
  - físicamente plano
  - perceptualmente brilloso
- Ruido rosa:
  - caída aprox. de 3 dB por octava
  - perceptualmente más equilibrado

### 5.3 Calibración del analizador
- Los analizadores pueden venir configurados para “parecer perceptualmente correctos”.
- Para uso técnico:
  - el slope / tilt debe ir a cero
- Esto es una idea fuerte del módulo y no debe perderse.

### 5.4 FFT y compromiso resolución-tiempo
- FFT alta:
  - mejor resolución espectral
  - peor inmediatez temporal
- FFT baja:
  - más rapidez visual
  - menos precisión frecuencial
- Valor citado como equilibrio útil:
  - 8192 puntos
- Esto debe preservarse como referencia técnica, no como dogma universal.

### 5.5 Overlap y Average Time
- Overlap suaviza visualmente la transición entre bloques.
- Average Time estabiliza la curva y muestra tendencia tonal real.

### 5.6 Ventanas
- Hanning:
  - compromiso general
  - más fuga espectral
- Blackman-Harris:
  - mejor lectura de señales débiles cercanas
- High Resolution:
  - menos “bonita” arriba
  - mejor para distorsión o actividad débil de fondo

### 5.7 La “V corta” en graves
- Hallazgo visual de oficio.
- Sirve para diferenciar:
  - señal útil
  - contenido espurio/subsónico
- Debe conservarse como criterio empírico útil, no como ley exacta.

### 5.8 Advertencia en agudos
- Si el analizador calibrado plano muestra pendiente ascendente fuerte en agudos extremos:
  - hay riesgo físico para tweeters
- Esto es una advertencia importante del profesor y no debe borrarse.

---

## 6. Medición de nivel y decibeles referenciados

### 6.1 Decibel referenciado
- No todo dB es simplemente relativo.
- Hay casos donde el cero está anclado a una referencia fija.

### 6.2 Potencia vs voltaje
- En potencia:
  - doble = +3 dB
- En voltaje:
  - doble = +6 dB
- Esto se repite como fundamento importante.

### 6.3 Fórmulas
- Potencia:
  - `10 · log10(dato/referencia)`
- Voltaje:
  - `20 · log10(dato/referencia)`

### 6.4 Referencias
- dBW = 1 W
- dBm = 1 mW
- dBV = 1 V
- dBu = 0,775 V

### 6.5 Niveles operativos
- Profesional:
  - +4 dBu
- Doméstico / semiprofesional:
  - -10 dBV

### 6.6 Switch +4 / -10
- No es decorativo.
- Sirve para adaptar correctamente niveles operativos entre equipos.
- Mala adaptación:
  - satura
  - o deja señal demasiado baja y ruidosa

### 6.7 dBFS
- 0 dBFS = máximo codificable digitalmente
- No hay señal “por encima” de eso en la salida real
- Si el master marca +3 dB:
  - no significa que el sistema entregue +3 reales
  - significa que ya recortó y perdió 3 dB de información

### 6.8 Ponderaciones A, B, C
- A:
  - volumen bajo
  - recorte fuerte de extremos
- B:
  - intermedio
- C:
  - alto volumen
  - respuesta más plana

### 6.9 LUFS y ponderación K
- LUFS no es una ponderación.
- Usa la ponderación K.
- Si exageras agudos:
  - sube la lectura LUFS
  - plataformas normalizan más agresivamente

### 6.10 Spotify no comprime dinámicamente para normalizar
- Normaliza por ganancia.
- La compresión que aplica es de datos, no de dinámica musical.
- Este matiz debe quedar sí o sí.

---

## 7. Ejemplos técnicos que no deben perderse

- cálculo de frecuencia desde período
- suma 100 Hz + 200 Hz vs 100 Hz + 373 Hz
- habitación de 3,43 m para 100 Hz
- comparación 2 W / 4 W y 2 V / 4 V
- FFT alta vs baja
- analogía de carpintería
- temperatura vs sensación térmica
- cuchara bajo chorro de agua
- “analizador = cinta métrica del audio” :contentReference[oaicite:3]{index=3}

---

## 8. Preguntas de estudiantes que sí aportan contenido

Estas no deben desaparecer al redactar:

- si saturar mucho termina generando distorsión fea
- si la fundamental siempre es la de mayor amplitud
- si hay cancelación de fase entre los dos oídos
- para qué sirven A, B y C
- cómo se aplica la regla de impedancia 8:1
- dudas sobre reproducción grave en celular y reconstrucción de fundamental ausente :contentReference[oaicite:4]{index=4} :contentReference[oaicite:5]{index=5}

---

## 9. Advertencias y matices fuertes

- no usar frecuencia y tono como sinónimos
- no creer que subir volumen “mejora” objetivamente la mezcla
- no arreglar sala llenándola de espuma
- no compensar con EQ un mal posicionamiento del monitor
- no confiar en el analizador si no está calibrado para uso técnico
- no asumir que 0 VU = -18 dBFS aplica siempre a señal musical compleja
- no decir que Spotify comprime la dinámica para normalizar
- no vender Sonarworks o aplanamiento por EQ como solución perfecta :contentReference[oaicite:6]{index=6} :contentReference[oaicite:7]{index=7} :contentReference[oaicite:8]{index=8}

---

## 10. Contenido dislocado que sí pertenece a M01

Este punto es clave para no perder información por culpa del orden de clases.

### Reubicar dentro de M01 aunque aparezca después
- calibración técnica del analizador y slope en cero
- FFT, block size, overlap, average time
- ventanas del analizador
- fundamental ausente
- curvas isofónicas reapareciendo en dinámica/mastering
- sibilancia explicada desde ruido rosa
- aclaraciones posteriores sobre auriculares abiertos/cerrados
- matices posteriores sobre VU, ondas complejas y calibración :contentReference[oaicite:9]{index=9} :contentReference[oaicite:10]{index=10}

---

## 11. Mapa de cobertura

### Muy fuerte
- física del sonido
- frecuencia / período / longitud de onda
- psicoacústica básica
- monitoreo
- acústica de sala
- analizador de espectro
- decibeles referenciados
- niveles operativos

### Fuerte pero con formulación prudente
- Sonarworks / corrección por EQ
- V corta en graves
- uso concreto de FFT = 8192
- recomendaciones de modelos concretos de auriculares

### No perder al redactar
- analogías del profesor
- preguntas útiles de estudiantes
- advertencias operativas
- contenido dislocado de clases posteriores
- distinción entre realidad física y percepción

---

## 12. Trazabilidad principal por clases

- **Clase 1:** introducción a medición, analizadores, ruido blanco, base fisiológica del oído
- **Clase 2:** período, frecuencia, ondas simples/complejas, armónicos, inarmónicos, tono, sala, difusión
- **Clase 3:** monitoreo, posicionamiento, desacople, auriculares, impedancia, sistemas de escucha
- **Clase 4:** decibeles referenciados, potencia, voltaje, dBu, dBV, dBFS
- **Clase 5:** ponderaciones, LUFS, K-weighting, normalización en streaming
- **Clase 9:** fundamental ausente y reconstrucción psicoacústica
- **Clase 10:** calibración del analizador, slope, FFT, average time
- **Clase 11:** ventanas, V corta, advertencias espectrales
- **Clase 14 / 15 / 27:** repeticiones y matices que refuerzan contenido de M01