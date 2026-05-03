salida 1
Como diseñador instruccional y experto en ingeniería de audio, he redactado la siguiente guía canónica para el módulo "Filtros y ecualización", basada estrictamente en la doctrina técnica y pedagógica extraída de las fuentes proporcionadas.

***

### Guía Canónica: Módulo "Filtros y ecualización"

#### 1. Objetivo de aprendizaje
Capacitar al estudiante para aplicar filtros con criterio técnico (limpieza, protección y jerarquía espacial) y utilizar ecualizadores con fines quirúrgicos o musicales, comprendiendo los efectos colaterales que estos procesos generan en la fase acústica y en la dinámica de la señal.

#### 2. Conceptos clave
*   **Frecuencia de corte:** El punto exacto donde la señal ha sido atenuada en -3 dB, lo que equivale a la mitad de la potencia.
*   **Pendiente (Slope):** La intensidad de atenuación fuera de la banda pasante, medida en dB por octava o dB por década.
*   **Rotación de Fase:** Efecto colateral ineludible de los filtros estándar. Por cada polo (6 dB/octava), la fase rota 45º en la frecuencia de corte.
*   **Fase Lineal y Pre-ringing:** Filtros digitales que evitan la rotación de fase, pero introducen latencia y un artefacto antinatural llamado *pre-ringing* (un eco o anticipación antes del transitorio).
*   **Overshoot y Ringing:** Alteraciones de la transiente y resonancias parásitas generadas por el uso de pendientes hiperabruptas.
*   **Método "Robin Hood":** Regla de gestión de headroom que dicta atenuar frecuencias inútiles antes de aplicar ganancia en otras zonas.

#### 3. Diferencia entre filtro y ecualización
*   **Filtros:** Son dispositivos diseñados exclusivamente para atenuar el nivel de determinadas frecuencias a partir de un punto establecido (Frecuencia de Corte) o en bandas específicas. Sus tipologías principales son Pasa-Altos (HPF), Pasa-Bajos (LPF), Pasa-Banda (BPF) y Elimina Banda (Notch). Sirven principalmente para control, protección térmica y para hacer espacio en la mezcla.
*   **Ecualizadores:** Son dispositivos que modifican la respuesta en frecuencia de una señal, con la capacidad no solo de atenuar, sino también de **aplicar ganancia** (en diseños de circuitos activos). Utilizan tipologías como Campana (Peak/Bell) o Estante (Shelving).

#### 4. Q y ancho de banda
*   **Ancho de banda (BW):** Es la cantidad de frecuencias afectadas a los lados de la frecuencia central, medida en el punto donde la atenuación es de 3 dB.
*   **Factor Q (Factor de calidad):** Es una relación matemática que se obtiene dividiendo la frecuencia central sobre el ancho de banda ($Q = f_c / \Delta f$). El Q determina la selectividad o resonancia de la campana, y **no debe confundirse con la pendiente del filtro**.
*   **Comportamiento del Q:** Existen ecualizadores de *Q Constante* (el ancho de banda no varía con los cambios de ganancia) y de *Q Proporcional* (el factor Q aumenta y la campana se estrecha a medida que se aplica mayor ganancia).

#### 5. Ecualización correctiva vs tonal
El profesor divide el abordaje de la ecualización en dos enfoques claros:
*   **Ecualización Correctiva ("Tengo un problema"):** Busca domar resonancias o desbalances. Se realiza mediante ecualización sustractiva y campanas estrechas (Q alto) para extirpar el problema sin dañar las frecuencias adyacentes. Se prefieren EQs digitales transparentes y quirúrgicos.
*   **Ecualización Tonal/Estética ("Me gustaría que..."):** Busca aportar cuerpo, aire, presencia o color musical. Se apoya en ecualización aditiva, utilizando campanas muy anchas o curvas tipo Shelving. Aquí brillan las emulaciones de hardware analógico (Pultec, Neve, SSL, Harrison), las cuales aportan distorsión armónica y curvas musicales asimétricas.

#### 6. Errores comunes
*   **Confusión visual de la frecuencia de corte:** Creer que el filtro comienza a actuar visualmente donde la línea empieza a curvarse en la pantalla, ignorando que el corte real está en los -3 dB.
*   **Confundir Q con Pendiente:** Usar el parámetro Q en plugins creyendo que se está alterando la pendiente (dB/oct) del filtro.
*   **Abuso de pendientes abruptas:** Utilizar filtros de 48 dB/octava de manera rutinaria, lo que destroza la fase acústica y genera *overshoot* y *ringing* antinatural.
*   **Uso ciego de Fase Lineal:** Insertar plugins de fase lineal asumiendo que "suenan más puros", sin notar que acumulan retardo y *pre-ringing* destructivo en instrumentos percusivos.
*   **La mentira de las perillas:** Confiar en los números de un EQ de modelado analógico sin escuchar (ej. marcar 1000 Hz cuando el equipo realmente está afectando los 600 Hz).
*   **Cirugía infinita:** Intentar arreglar una mala toma, mala acústica o mala elección de sonido mediante parches excesivos de ecualización en la mezcla.

#### 7. Criterio pedagógico para responder a estudiantes
*   **Sobre decisiones estéticas:** Obligar al estudiante a ecualizar el carácter final del instrumento siempre en contexto con la mezcla, prohibiendo la toma de decisiones tímbricas con el botón *Solo* activado.
*   **Sobre el exceso de graves/agudos:** Si el alumno satura el Mix Bus por abusar de la EQ aditiva, el tutor debe exigirle aplicar el "Método Robin Hood" para proteger la estructura de ganancia.
*   **Sobre la desalineación de capas (Layering):** Si el alumno reporta que al filtrar bombos o bajos superpuestos el sonido "pierde cuerpo", el tutor debe indicarle que analice la suma con un osciloscopio para evidenciar la rotación de fase destructiva generada por los filtros.
*   **Sobre la filosofía de trabajo:** Promover un análisis socrático. Antes de permitir que el estudiante inserte un ecualizador, preguntarle: *¿Estás resolviendo un problema o estás buscando un color?*. Remarcar siempre que "las consolas mienten" visualmente y que las decisiones definitivas deben tomarse con el oído. *(Nota: La creación de un flujo automatizado de tutoría sobre estos criterios específicos requiere validación según las capacidades técnicas del entorno Moodle implementado).*

salida 2
Como diseñador instruccional, analista curricular y experto en ingeniería de audio, he estructurado una base de conocimientos ("Knowledge Base") con 12 preguntas frecuentes (FAQs) exclusivas del módulo "Filtros y ecualización". 

Esta matriz está diseñada específicamente para calibrar las respuestas de un tutor de Inteligencia Artificial en la plataforma Moodle, asegurando que sus explicaciones sean exactas, breves y alineadas al enfoque pedagógico del profesor, sin incurrir en alucinaciones o consejos genéricos de internet.

---

### Banco de Preguntas Frecuentes (FAQs) para Tutor IA

**1. Frecuencia de corte y visualización**
*   **Pregunta:** ¿Dónde empieza realmente a actuar o cortar un filtro?
*   **Respuesta canónica breve:** El filtro comienza a atenuar antes de la frecuencia de corte. La frecuencia de corte no es el punto donde la curva visualmente empieza a caer, sino el punto exacto donde la señal ya ha sido atenuada en -3 dB (la mitad de su potencia).
*   **Tema:** Lectura de filtros y analizadores.
*   **Qué NO debería decir un tutor de IA:** No debe decirle al alumno que el filtro "elimina por completo" todo lo que está más allá de la frecuencia, ni afirmar que el corte inicia matemáticamente en el número que marca la pantalla.

**2. Parámetros: Pendiente vs. Factor Q**
*   **Pregunta:** ¿Es lo mismo el factor Q que la pendiente de un filtro?
*   **Respuesta canónica breve:** No. La pendiente (Slope) define cuán rápida o abrupta es la atenuación de las frecuencias fuera de la banda pasante (se mide en dB por octava o por década). El factor Q determina la selectividad o resonancia de la curva, y se obtiene dividiendo la frecuencia central sobre el ancho de banda.
*   **Tema:** Parámetros del ecualizador.
*   **Qué NO debería decir un tutor de IA:** No debe sugerir que mover el control "Q" en un ecualizador cambia directamente los dB/octava de la pendiente del filtro de corte, ya que son atributos acústicos distintos.

**3. Riesgos de la atenuación extrema**
*   **Pregunta:** ¿Qué problemas genera usar siempre filtros con pendientes muy abruptas, como 48 dB/octava?
*   **Respuesta canónica breve:** Las pendientes hiperabruptas son menos musicales, no existen así en la naturaleza e introducen mayor rotación de fase. Además, pueden generar picos artificiales de nivel (*overshoot*) y oscilaciones o resonancias parásitas (*ringing*) posteriores a la transiente.
*   **Tema:** Efectos colaterales de los filtros.
*   **Qué NO debería decir un tutor de IA:** No debe recomendar el uso de pendientes extremas (como 24 o 48 dB/octava) "para limpiar mejor o con más precisión" a menos que haya un problema técnico severo que lo justifique.

**4. Filtros de Fase Lineal**
*   **Pregunta:** ¿Conviene usar siempre filtros de fase lineal para no dañar la señal?
*   **Respuesta canónica breve:** No. Si bien los filtros de fase lineal evitan la rotación de fase, introducen latencia y generan un artefacto antinatural llamado *pre-ringing*, que es una anticipación o eco de energía que aparece *antes* del golpe real, arruinando ataques en instrumentos percusivos.
*   **Tema:** Tipologías de filtros digitales.
*   **Qué NO debería decir un tutor de IA:** No debe calificar a la fase lineal como "el ecualizador perfecto" o sugerir su uso rutinario en todo el Mix Bus, omitiendo el daño temporal (*pre-ringing*).

**5. El mito del Shelving**
*   **Pregunta:** ¿Si uso un ecualizador tipo *shelving* evito la rotación de fase que hacen los filtros LPF o HPF?
*   **Respuesta canónica breve:** No, eso es falso. Un ecualizador *shelving* convencional también rota la fase. Lo único que lo diferencia de un filtro de corte es la forma de su curva de transferencia (ya que eleva o atenúa una zona plana sin caer a cero), pero no evita el fenómeno temporal de fase.
*   **Tema:** Curvas Shelving y Fase.
*   **Qué NO debería decir un tutor de IA:** No debe validar la idea de que el *shelving* es la "solución mágica temporal" frente al uso de filtros para mantener las fases intactas.

**6. Criterios Filosóficos: Quirúrgico vs. Musical**
*   **Pregunta:** ¿Cuándo debo usar un ecualizador transparente digital y cuándo uno de modelado analógico?
*   **Respuesta canónica breve:** Se usa un ecualizador transparente/quirúrgico (como un Pro-Q) bajo la premisa "tengo un problema", empleando EQ sustractiva con campanas estrechas para corregir resonancias. Se usa uno de modelado analógico bajo la premisa "me gustaría que...", empleando EQ aditiva y curvas anchas para dar color, cuerpo y armónicos musicales.
*   **Tema:** Criterios estéticos de mezcla.
*   **Qué NO debería decir un tutor de IA:** No debe sugerir usar ecualizadores analógicos (como un Neve o un SSL) para realizar cortes quirúrgicos muy estrechos (Notch), ya que no es la filosofía de su diseño de circuito.

**7. Modelado Analógico y Asimetrías**
*   **Pregunta:** ¿Qué sucede si subo (boost) y bajo (attenuation) simultáneamente la misma frecuencia grave en un ecualizador Pultec?
*   **Respuesta canónica breve:** Como el Pultec es un ecualizador asimétrico (sus curvas para subir y para bajar no son idénticas), no se anulan entre sí. En su lugar, se genera la famosa "curva Pultec", que realza la frecuencia grave deseada mientras limpia (atenúa) una zona adyacente más arriba, logrando engrosar y dar claridad al mismo tiempo.
*   **Tema:** Emulación de Hardware (Pultec EQP-1A).
*   **Qué NO debería decir un tutor de IA:** No debe decirle al alumno que hacer ambas cosas a la vez resultará en la "cancelación" de la frecuencia (física de ganancia unitaria), ignorando el diseño de circuito asimétrico de esta herramienta legendaria.

**8. Q Constante vs. Q Proporcional**
*   **Pregunta:** ¿Por qué en algunos ecualizadores, como los API, la campana se hace más puntiaguda si le doy más volumen?
*   **Respuesta canónica breve:** Porque utilizan un diseño de circuito de "Q Proporcional". En estos ecualizadores, el factor Q aumenta y el ancho de banda se estrecha automáticamente a medida que se aplica mayor ganancia, a diferencia de los ecualizadores de "Q Constante", donde la campana mantiene el mismo ancho siempre.
*   **Tema:** Comportamiento del factor de calidad (Q).
*   **Qué NO debería decir un tutor de IA:** No debe afirmar que esto es un "error del plugin" o sugerirle al alumno que desactive esa función, ya que es el comportamiento electrónico deseado por el fabricante.

**9. Ecualización en Capas (Layering)**
*   **Pregunta:** ¿Por qué cuando superpongo dos bombos (layers) y le filtro los graves a uno de ellos, el sonido pierde pegada en lugar de aclararse?
*   **Respuesta canónica breve:** Porque los filtros rotan la fase de la señal. Al aplicar un filtro, desalineas la fase temporal de la capa respecto a la otra; lo que originalmente iba a sumar constructivamente, ahora genera una cancelación destructiva en el grave útil. Hay que revisar siempre la suma con un osciloscopio.
*   **Tema:** Rotación de Fase e Interacciones.
*   **Qué NO debería decir un tutor de IA:** No debe proponer "ecualizar más fuerte los graves" para compensar la pérdida, ignorando que el problema es puramente temporal/espacial por rotación.

**10. La confianza en las interfaces analógicas (GUI)**
*   **Pregunta:** ¿Si el potenciómetro de mi plugin analógico marca 1000 Hz, puedo estar seguro de que estoy ecualizando exactamente ahí?
*   **Respuesta canónica breve:** No. Las serigrafías de los ecualizadores de modelado analógico no suelen coincidir matemáticamente con la acción real debido al diseño y las tolerancias de los circuitos clásicos. Una perilla marcada en 1000 Hz podría estar afectando su curva alrededor de los 600 Hz o 900 Hz.
*   **Tema:** Comportamiento del modelado analógico.
*   **Qué NO debería decir un tutor de IA:** Nunca debe pedirle al estudiante que digite valores exactos a ciegas confiando en el panel analógico; siempre debe obligar al alumno a usar su oído para validar el corte.

**11. Ecualización Dinámica vs. Estática**
*   **Pregunta:** ¿Cuándo debo utilizar un ecualizador dinámico en la mezcla?
*   **Respuesta canónica breve:** Cuando el problema de frecuencias (ej. un choque entre bajo y bombo, o una sibilancia vocal) es intermitente u ocasional. Si utilizas un ecualizador estático, atenuarías permanentemente esa zona, destruyendo el timbre del instrumento durante los momentos donde el problema no existe.
*   **Tema:** Ecualización Dinámica.
*   **Qué NO debería decir un tutor de IA:** No debe confundir la ecualización dinámica con un compresor multibanda. Debe recordar que el EQ dinámico actúa mediante campanas y es más quirúrgico para resolver conflictos localizados.

**12. "Método Robin Hood" en Ecualización**
*   **Pregunta:** Si una mezcla ya tiene demasiado nivel, ¿cómo aplico el Método Robin Hood con el ecualizador?
*   **Respuesta canónica breve:** Consiste en un criterio sustractivo de protección de *headroom*: "robarle energía a lo que molesta antes de darle ganancia a lo que falta". Se basa en atenuar frecuencias conflictivas en lugar de realzar las deseadas, logrando abrir espacio en la mezcla sin saturar la etapa de salida.
*   **Tema:** Metodologías de gestión de Headroom.
*   **Qué NO debería decir un tutor de IA:** No debe alucinar que el "Método Robin Hood" es un plugin, un tipo de filtro físico real o un parámetro del compresor. Es un concepto y un enfoque pedagógico de ecualización sustractiva. *(Basado en las transcripciones y desarrollo curricular general).*

salida 3
Como diseñador instruccional y experto en ingeniería de audio, he sistematizado el contenido del módulo "Filtros y ecualización" basándome exclusivamente en los materiales y transcripciones provistos. 

A continuación, presento un glosario curricular de 18 términos clave, estructurado para despejar las dudas más habituales de los estudiantes en un entorno universitario.

***

### Glosario del Módulo: Filtros y Ecualización

**1. Frecuencia de corte (Fc)**
*   **Definición breve:** Es el punto exacto donde un filtro consigue una atenuación de 3 dB, equivalente a la mitad de su potencia acústica respecto de la banda pasante.
*   **Etiquetas:** Filtros, Parámetros de medición.
*   **Suele confundirse con:** El punto visual donde la curva gráfica recién empieza a caer en la pantalla del plugin; en realidad, el filtro empieza a atenuar antes de llegar a la frecuencia de corte nominal.

**2. Pendiente (Slope)**
*   **Definición breve:** Es la intensidad con la que un filtro atenúa las frecuencias que quedan fuera de la banda pasante, midiéndose comúnmente en decibeles por octava o por década.
*   **Etiquetas:** Filtros, Parámetros.
*   **Suele confundirse con:** El factor "Q" o resonancia del filtro, dado que en algunos plugins básicos el control Q se usa erróneamente para intentar cambiar la dureza de la caída.

**3. Factor de Calidad (Q)**
*   **Definición breve:** Es la relación matemática entre la frecuencia central y su ancho de banda ($Q = fc / BW$), determinando así cuán estrecha, selectiva o resonante será la campana de ecualización o el corte del filtro.
*   **Etiquetas:** Ecualizadores, Parámetros.
*   **Suele confundirse con:** La pendiente (Slope); el Q controla la resonancia en el punto de corte, no cuán rápido caen las frecuencias subsiguientes.

**4. Ancho de banda (Bandwidth / BW)**
*   **Definición breve:** Es la cantidad de frecuencias afectadas a los lados de la frecuencia central en una curva de campana, determinándose en los puntos donde la atenuación o realce llega a los 3 dB.
*   **Etiquetas:** Ecualizadores, Parámetros.

**5. Filtro Pasa Altos (HPF / Low Cut)**
*   **Definición breve:** Dispositivo o algoritmo que deja pasar las frecuencias altas y atenúa gradualmente las frecuencias ubicadas por debajo de su frecuencia de corte.
*   **Etiquetas:** Filtros, Limpieza, Control de Headroom.

**6. Filtro Pasa Bajos (LPF / High Cut)**
*   **Definición breve:** Dispositivo que atenúa gradualmente las frecuencias ubicadas por encima de la frecuencia de corte seleccionada, dejando pasar las frecuencias más graves.
*   **Etiquetas:** Filtros, Control espectral.

**7. Filtro Notch (Ranura o Muesca)**
*   **Definición breve:** Filtro diseñado para eliminar casi por completo un sector extremadamente estrecho de frecuencias, utilizado frecuentemente para extirpar resonancias molestas o acoples.
*   **Etiquetas:** Filtros, Corrección Quirúrgica.

**8. Filtro Butterworth**
*   **Definición breve:** Tipología de filtro clásico que mantiene una respuesta muy estable y pareja a lo largo de toda su banda pasante antes de llegar a la frecuencia de corte.
*   **Etiquetas:** Tipologías de filtros, Modelado.
*   **Suele confundirse con:** No debe confundirse con la totalidad de los filtros existentes; el profesor advierte que es solo un modelo (aunque el más común en DAWs) y que otros diseños reaccionan diferente.

**9. Fase Lineal (Filtros de)**
*   **Definición breve:** Son filtros del dominio digital diseñados para operar sin generar la rotación de fase tradicional que sí causan los filtros estándar.
*   **Etiquetas:** Filtros digitales, Artefactos, Fase.
*   **Suele confundirse con:** La "solución perfecta" de ecualización. Se cree que por no dañar la fase son siempre inofensivos, ignorando que introducen latencia severa y artefactos antinaturales en los ataques.

**10. Pre-ringing**
*   **Definición breve:** Artefacto o "eco" antinatural que aparece como una anticipación de energía justo antes del transitorio real de un sonido, generado exclusivamente por el uso de filtros o ecualizadores de Fase Lineal.
*   **Etiquetas:** Artefactos digitales, Problemas de ecualización.

**11. Overshoot**
*   **Definición breve:** Picos de nivel artificiales generados en el dominio temporal cerca de la frecuencia de corte cuando se aplican filtros con pendientes exageradamente abruptas (ej. 48 dB/octava).
*   **Etiquetas:** Artefactos, Filtros agresivos.

**12. Ringing**
*   **Definición breve:** Oscilaciones o resonancias parásitas que ocurren inmediatamente después de un impacto o transitorio a causa de utilizar pendientes de filtrado hiperabruptas.
*   **Etiquetas:** Artefactos, Alteración temporal.

**13. Ecualizador Shelving (Estante)**
*   **Definición breve:** Filtro que divide el espectro en dos partes, aplicando una ganancia o atenuación constante a todas las frecuencias desde su punto de corte hacia el extremo, aplanándose gradualmente sin regresar a cero.
*   **Etiquetas:** Ecualizadores, Modelado Tonal.
*   **Suele confundirse con:** Existe un gran mito de que el ecualizador Shelving evita la rotación de fase típica de los filtros High/Low Pass; en realidad, los shelving también alteran la fase.

**14. Ecualizador Peak (Campana)**
*   **Definición breve:** Diseño de filtro que basa su funcionamiento en centrar su máxima actividad de realce o recorte en una frecuencia central (Fc), decayendo progresivamente hacia los costados de acuerdo a su factor Q.
*   **Etiquetas:** Ecualizadores, Topologías.

**15. Q Proporcional**
*   **Definición breve:** Topología presente en ecualizadores analógicos (como los API) donde el ancho de banda se vuelve cada vez más estrecho (el Q se hace más agudo) a medida que se aumenta la ganancia de la campana.
*   **Etiquetas:** Ecualizadores, Hardware clásico.
*   **Suele confundirse con:** Suele generar sorpresa al intentar trasladar el mismo ajuste numérico a un ecualizador digital, ya que el comportamiento de la curva cambia dinámicamente según el nivel de volumen aplicado.

**16. Ecualización Asimétrica**
*   **Definición breve:** Se refiere a ecualizadores (como el legendario Pultec EQP-1A) cuyas curvas para aplicar realces (Boost) y atenuaciones (Cut) no tienen la misma forma ni el mismo recorrido espectral.
*   **Etiquetas:** Emulación Analógica, Color musical.
*   **Suele confundirse con:** La idea de que subir y bajar la misma frecuencia simultáneamente anula el sonido. En equipos asimétricos, hacerlo genera un ensanchamiento grave combinado con una limpieza adyacente (la "curva Pultec").

**17. Ecualización Dinámica**
*   **Definición breve:** Proceso que aplica atenuación o realce en una campana selectiva de frecuencias solo cuando la señal sobrepasa un nivel de umbral (threshold) configurado, ideal para problemas intermitentes.
*   **Etiquetas:** Procesadores Dinámicos, Ecualización avanzada.
*   **Suele confundirse con:** El compresor multibanda. Sin embargo, la EQ dinámica opera con campanas y anchos de banda ("Range") sin alterar la fase global con crossovers físicos, siendo más quirúrgica y focalizada.

**18. Método Robin Hood**
*   **Definición breve:** Estrategia metodológica explicada por el profesor para la gestión de ecualización que se basa en la premisa de "robarle energía a lo inútil antes de darle ganancia a lo útil", privilegiando ecualización sustractiva para proteger el margen de volumen general de la mezcla.
*   **Etiquetas:** Metodología, Headroom, Buenas Prácticas.

salida 4
Como diseñador instruccional, he mapeado exhaustivamente los materiales de estudio vinculados al módulo "Filtros y ecualización". A continuación, presento el catálogo de recursos disponibles para estructurar el aprendizaje de los estudiantes.

### Mapa de Recursos: Módulo "Filtros y ecualización"

**1. Apunte Filtros 2022 V1.pdf**
*   **Título del recurso:** Apunte Filtros 2022 V1.pdf
*   **Tipo de recurso:** Apunte teórico (Documento PDF).
*   **Tema:** Comportamiento físico y matemático de los filtros, frecuencias de corte, pendientes, tipologías (Butterworth, Chebyshev, Cauer, Bessel), factor Q y conceptos avanzados como rotación de fase y *pre-ringing*.
*   **Clase o lección asociada:** Se introduce y desarrolla en las Clases 11 y 12.
*   **Página o minuto:** Sin página exacta especificada en el documento.
*   **Para qué sirve revisar ese recurso:** Sirve para sentar las bases teóricas duras. Permite que el alumno comprenda que la frecuencia de corte es un punto acústico (-3 dB) y no un punto visual, y enseña las diferencias y efectos destructivos (como *overshoot* y *ringing*) que cada modelo de filtro puede generar en la señal temporal.

**2. Apunte Ecualizadores 2020 V1.pdf**
*   **Título del recurso:** Apunte Ecualizadores 2020 V1.pdf
*   **Tipo de recurso:** Apunte teórico (Documento PDF).
*   **Tema:** Topologías de ecualizadores (Peak/Campana, Shelving), clasificación técnica (Gráficos, Paramétricos, Semiparamétricos), anchos de banda, factor Q (constante vs. proporcional), y criterios de ecualización aditiva y sustractiva.
*   **Clase o lección asociada:** Base teórica para las Clases 13 y 14.
*   **Página o minuto:** Sin página exacta especificada en el documento.
*   **Para qué sirve revisar ese recurso:** Brinda el sustento para diferenciar los comportamientos analógicos de la curva (ej. por qué el factor Q en algunos ecualizadores analógicos se estrecha al dar volumen) y asienta la justificación pedagógica de privilegiar la ecualización sustractiva para proteger la ganancia general.

**3. Clase 11 - Mezcla.md**
*   **Título del recurso:** Clase 11 - Mezcla.md
*   **Tipo de recurso:** Transcripción de clase teórica (Texto Markdown).
*   **Tema:** Desmitificación de filtros (diferencia entre Pendiente y Q), lectura visual del analizador espectral (la "V corta"), el mito temporal de los curvas shelving, filtros de fase lineal, *ringing* y *pre-ringing* aplicados al *layering* (capas) de baterías.
*   **Clase o lección asociada:** Clase 11.
*   **Página o minuto:** Sin minuto exacto de grabación.
*   **Para qué sirve revisar ese recurso:** Es fundamental para desmontar errores comunes de internet. Sirve para que el estudiante comprenda por qué usar ciegamente pendientes de 48 dB/oct o filtros de Fase Lineal puede destrozar el ataque y la alineación temporal de bombos y bajos.

**4. Clase 12 - Mezcla.md**
*   **Título del recurso:** Clase 12 - Mezcla.md
*   **Tipo de recurso:** Transcripción de clase práctica (Texto Markdown).
*   **Tema:** Implementación del filtrado en una mezcla real. Desarrollo de "Los tres motivos para usar un filtro" (protección térmica, limpieza fuera de registro y jerarquía espacial en mezcla). Técnica del "Filtro invertido".
*   **Clase o lección asociada:** Clase 12.
*   **Página o minuto:** Sin minuto exacto de grabación.
*   **Para qué sirve revisar ese recurso:** Sirve para pasar de la teoría a la práctica en el DAW. Enseña el criterio para ejecutar filtrado prudente sobre instrumentos críticos (no arruinar los *rooms* o *hi-hats* por exceso de limpieza) y el protocolo de filtrado en contexto en lugar de usar el botón de *Solo*.

**5. Clase 13 - Mezcla.md**
*   **Título del recurso:** Clase 13 - Mezcla.md
*   **Tipo de recurso:** Transcripción de clase teórica-práctica (Texto Markdown).
*   **Tema:** Ecualizadores estáticos. Concepto de curvas simétricas vs. asimétricas. Filosofía "Tengo un problema" (EQ quirúrgico) vs "Me gustaría que..." (EQ musical). Crítica a la ecualización destructiva excesiva.
*   **Clase o lección asociada:** Clase 13.
*   **Página o minuto:** Sin minuto exacto de grabación.
*   **Para qué sirve revisar ese recurso:** Modifica el marco mental del estudiante, llevándolo de "reparador de audio" a ingeniero de mezcla. Demuestra que el foco siempre debe estar en la captura original y en la interpretación del músico, no en intentar arreglar grabaciones mediocres con "cirugías infinitas".

**6. Clase 14 - Mezcla.md**
*   **Título del recurso:** Clase 14 - Mezcla.md
*   **Tipo de recurso:** Transcripción de clase práctica (Texto Markdown).
*   **Tema:** Modelado Analógico. Análisis del ruteo interno de ecualización en consolas SSL (modelos E y G). Uso del ecualizador pasivo Pultec (EQP-1A y MQ-5) y demostración visual de las imprecisiones de los potenciómetros analógicos.
*   **Clase o lección asociada:** Clase 14.
*   **Página o minuto:** Sin minuto exacto de grabación.
*   **Para qué sirve revisar ese recurso:** Para que el estudiante domine las emulaciones "vintage" más estándar de la industria. Permite aplicar técnicas como la codiciada "Curva Pultec" (realzar y atenuar frecuencias graves simultáneamente en un sistema asimétrico) y enseña a cambiar el ruteo de los EQs (botón Split).

**7. Listado de plugins gratuitos para análisis de señales, y otros extras.txt**
*   **Título del recurso:** Listado de plugins gratuitos para análisis de señales, y otros extras.txt
*   **Tipo de recurso:** Archivo de texto (Listado de herramientas de software).
*   **Tema:** Repositorio de enlaces para descarga de software gratuito de ecualización estática y dinámica, así como emulaciones de *hardware* clásico (ej. *TDR Nova*, *TDR VOS SlickEQ*, *Warmy EP1A*).
*   **Clase o lección asociada:** Material transversal aplicable a los módulos de Filtros y Ecualización.
*   **Página o minuto:** Sin página exacta.
*   **Para qué sirve revisar ese recurso:** Como recurso de infraestructura. Permite que el alumno sin presupuesto pueda armar una estación de trabajo virtual completa (con EQs musicales, emuladores de Pultec y EQs dinámicos de altísima calidad) para replicar y practicar la doctrina del profesor.

**8. Leer.pdf**
*   **Título del recurso:** Leer.pdf
*   **Tipo de recurso:** Documento de texto (Guía de plantillas del profesor).
*   **Tema:** Inventario de plugins que componen la plantilla predeterminada de Pro Tools del instructor (incluyendo EQs como *Fabfilter Pro-Q 4*, *UAD SSL 4000 E*, y *UAD Pultec EQP-1A*).
*   **Clase o lección asociada:** Aplicable a los "Trainings" (Prácticas Integradoras a partir de la Clase 21).
*   **Página o minuto:** Sin página exacta.
*   **Para qué sirve revisar ese recurso:** Sirve como modelo de "cinturón de herramientas". El alumno puede observar el ecosistema real de *plugins* de modificación espectral que utiliza un profesional en su ruteo predeterminado.