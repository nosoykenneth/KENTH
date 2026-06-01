He revisado el Anexo 5, los Lineamientos UDED-LNM-2026-V9 y tu nota conceptual aprobada. No encuentro en el directorio los archivos KENTH_Eje*_Contenido_Canonico.md, estructura_congelada_lecciones_kenth.md, los guiones v2 ni la auditoría forense — los marcaré como evidencia a inyectar después.

1. Diagnóstico
A. Qué debe conservarse de la nota conceptual

Tema literal, objetivo general y los cinco objetivos específicos (el quinto — conclusiones/recomendaciones — es estructural, no de contenido).
Enfoque metodológico mixto, diseño cuasi-experimental, alcance correlacional/explicativo.
PRISMA 2020 como método de revisión.
Productos acreditables (documento, curso Moodle, sistema IA, código + guías, reporte de evaluación).
Decisión arquitectónica: Ollama local (justificación de privacidad/gobernanza ya argumentada con UNESCO 2023 y Marín & Tur 2023).
B. Qué puede cambiarse respecto al índice tentativo de la nota conceptual
El índice tentativo de la nota conceptual (9 capítulos) infla y duplica. Cambios recomendados:

Fusionar “Análisis y Diseño de la Solución” + “Desarrollo e Implementación” + “Evaluación y Resultados” + “Discusión” en un único Capítulo IV (lo exige Anexo 5, que solo permite un capítulo de análisis y discusión).
Eliminar “Marco Teórico” como capítulo separado; absorberlo dentro del Capítulo II junto al Estado del Arte.
Mover requerimientos (técnicos, pedagógicos, funcionales) al Capítulo IV como fase de diseño, no al marco teórico.
C. Qué exige el Anexo 5 sí o sí

Portada, certificado de análisis de similitud, certificación del director, responsabilidad de autoría, autorización de publicación, dedicatoria/agradecimiento (opcionales), índices (contenido/tablas/figuras), Resumen + palabras clave, Abstract + keywords.
Capítulos I–V con la nomenclatura exacta del anexo: Introducción / Estado del arte–Marco teórico–Marco conceptual / Metodología (con Enfoque, Tipo y diseño, Población y muestra, Técnica e instrumento, Validación y confiabilidad, Consideraciones éticas) / Análisis y discusión de los resultados / Conclusiones y Recomendaciones.
Referencias + Apéndices.
Mínimo 60, máximo 120 páginas.
Máximo 3 niveles de índice.
D. Qué capítulos conviene fusionar

Estado del arte + Marco teórico + Marco conceptual → un solo Capítulo II con tres apartados internos (el anexo los exige por nombre, pero pueden vivir como secciones, no como capítulos separados).
Diseño + Implementación + Resultados → Capítulo IV unificado, con secuencia: requerimientos → arquitectura → implementación Moodle → integración Ollama/RAG → piloto → resultados → discusión.
Conclusiones + Recomendaciones → Capítulo V, alineado uno-a-uno con objetivos específicos.
E. Riesgos metodológicos o autorales a cuidar

Riesgo de mutar a manual de mezcla/masterización — el contenido del curso es insumo, no objeto de evaluación académica. El TIC evalúa la integración Moodle+IA, no la teoría de audio.
Contaminación autoral — la auditoría forense menciona riesgos con Rabinovich. Cualquier analogía, secuencia pedagógica o fraseo distintivo que provenga de fuentes señaladas debe reescribirse o atribuirse explícitamente.
Sobre-prometer evaluación — la nota conceptual habla de pre-test/post-test y muestreo por conveniencia. No inventes tamaño muestral ni resultados; deja placeholders hasta tener datos.
Diseño cuasi-experimental sin grupo control — declara explícitamente las amenazas a la validez interna (Fabrigar et al., 2024) en lugar de ocultarlas.
Confusión de capas — separar siempre: contenido pedagógico del curso ≠ plataforma Moodle ≠ tutor IA/RAG ≠ infraestructura Ollama ≠ instrumentos de evaluación. Conviene una figura de arquitectura en capas en el Capítulo IV.
IA generativa sin supervisión declarada — Anexo 17 institucional exige cumplimiento ético; documenta criterios de validación de prompts y supervisión docente (Wu et al., 2025; UNESCO 2023).
Métricas de IA mal definidas — “precisión de respuestas” necesita rúbrica operacional (coherencia, exactitud técnica, alineación pedagógica), no solo accuracy.
2. Índice recomendado
Elementos preliminares
Portada (Anexo 5 plantilla)
Certificado de similitud (herramienta autorizada)
Certificación del director
Responsabilidad de autoría
Autorización de publicación
Dedicatoria (opcional)
Agradecimiento (opcional)
Índice de contenidos, de tablas, de figuras
Resumen (200–350 palabras) + palabras clave (5)
Abstract + keywords (5)
Capítulo I — Introducción
1.1 Planteamiento del problema
1.2 Formulación del problema / pregunta de investigación
1.3 Objetivos
1.3.1 Objetivo general
1.3.2 Objetivos específicos
1.4 Justificación
1.5 Alcance y delimitación
Propósito: situar el problema (escalabilidad del feedback formativo + brecha de IA aplicada a mezcla/masterización en LMS), declarar objetivos sin alteración respecto a la nota conceptual, delimitar lo que NO cubre el trabajo.
Evidencia: nota conceptual aprobada (resolución ESPE-RES-ITIN-2026-006).
Extensión: 6–9 páginas.
Riesgo de inflado: repetir antecedentes en cada subsección. Mitigación: el problema se justifica una sola vez; el resto remite a Cap. II.

Capítulo II — Estado del arte y fundamentos
2.1 Estado del arte (revisión sistemática PRISMA 2020)
2.1.1 Protocolo de búsqueda y criterios de inclusión/exclusión
2.1.2 Diagrama de flujo PRISMA y matriz de estudios seleccionados
2.1.3 Hallazgos por eje (LMS y Moodle / IA aplicada a audio / IA generativa y feedback / tutoría inteligente con LLMs)
2.1.4 Brechas identificadas
2.2 Marco teórico
2.2.1 Diseño instruccional y evaluación formativa en entornos virtuales
2.2.2 Fundamentos de procesamiento digital de audio en mezcla y masterización
2.2.3 LLMs locales, RAG y arquitecturas de tutoría inteligente
2.3 Marco conceptual
2.3.1 Glosario operacional (LMS, RAG, prompt acotado, retroalimentación formativa, etc.)
Propósito: consolidar el sustento académico que ata el problema con la propuesta. PRISMA cumple OE1; marco teórico anclaje conceptual.
Evidencia: salida del proceso PRISMA (bases: Scopus, IEEE Xplore, ACM, ScienceDirect); referencias ya citadas en nota conceptual.
Extensión: 14–18 páginas.
Riesgo de inflado: convertir 2.2.2 en tratado de audio. Mitigación: limitar a conceptos que un evaluador necesita para entender los criterios técnicos del curso y del tutor.

Capítulo III — Metodología
3.1 Enfoque de la investigación (mixto, predominio cuantitativo)
3.2 Tipo y diseño de investigación (aplicada, cuasi-experimental, alcance correlacional/explicativo)
3.3 Población y muestra (estudiantes Carrera de Software ESPE; muestreo por conveniencia)
3.4 Técnicas e instrumentos
3.4.1 Encuesta Likert de satisfacción y utilidad
3.4.2 Rúbricas de desempeño práctico
3.4.3 Pre-test / post-test de conocimientos
3.4.4 Métricas de calidad del tutor IA (coherencia, precisión técnica, alineación pedagógica)
3.4.5 Trazas del LMS
3.5 Validación y confiabilidad del instrumento
3.6 Consideraciones éticas (consentimiento informado, manejo de datos, IA local, UNESCO 2023)
Propósito: demostrar rigor metodológico exigido por el Anexo 5 (todos los subapartados están listados en el Capítulo III obligatorio).
Evidencia: PRISMA-S checklist, plantillas de cuestionarios, rúbricas, plan de pilotaje.
Extensión: 8–12 páginas.
Riesgo de inflado: describir cada ítem del cuestionario. Mitigación: descripción agregada; instrumento completo va al Apéndice.

Capítulo IV — Desarrollo, implementación y resultados
4.1 Análisis de requerimientos
4.1.1 Requerimientos funcionales
4.1.2 Requerimientos no funcionales
4.1.3 Requerimientos pedagógicos
4.2 Diseño de la solución
4.2.1 Arquitectura general (capas: contenido / Moodle / orquestador IA / Ollama / RAG)
4.2.2 Diseño instruccional del curso (ejes 0–7, estructura congelada)
4.2.3 Diseño del tutor contextual y estrategia RAG
4.3 Implementación
4.3.1 Configuración del curso en Moodle (secciones, actividades, evaluaciones)
4.3.2 Integración del backend con Ollama
4.3.3 Ingesta y vectorización de contenidos canónicos
4.3.4 Diseño y validación de prompts
4.4 Pruebas y validación del sistema
4.5 Piloto con estudiantes
4.6 Resultados
4.6.1 Resultados cuantitativos (pre/post, Likert, trazas)
4.6.2 Resultados cualitativos (percepción, comentarios)
4.6.3 Métricas de desempeño del tutor IA
4.7 Discusión de los resultados
Propósito: ejecutar OE2, OE3 y OE4 en una sola narrativa coherente requerimientos → diseño → implementación → evaluación → discusión.
Evidencia: archivos KENTH canónicos Eje0–Eje7, estructura_congelada_lecciones_kenth.md, guiones v2, código del repo tesis-rag y bd_vectorial, logs de pruebas, datos del piloto.
Extensión: 25–35 páginas (es el capítulo más denso).
Riesgo de inflado: convertir 4.2.2 en réplica del contenido del curso. Mitigación: describir la estructura y los criterios de diseño, no el contenido completo (este va al Apéndice como enlace al curso desplegado).

Capítulo V — Conclusiones y recomendaciones
5.1 Conclusiones (una por objetivo específico)
5.2 Recomendaciones
5.3 Trabajos futuros
Propósito: cierre alineado uno-a-uno con OE1–OE4 (OE5 se cumple al redactar este capítulo).
Evidencia: todo lo anterior.
Extensión: 4–6 páginas.
Riesgo de inflado: reescribir resultados. Mitigación: cada conclusión = 1 párrafo afirmativo con cifra/hallazgo y limitación.

Referencias (norma IEEE — área técnica)
Apéndices
A. Protocolo PRISMA y matriz de estudios
B. Instrumentos validados (encuestas, rúbricas, pre/post-test)
C. Documento de requerimientos
D. Diagramas de arquitectura
E. Guía de instalación y uso del sistema
F. Capturas y enlace al curso desplegado
G. Prompts del tutor IA y criterios de validación
H. Datos brutos del piloto (anonimizados)
Total estimado: 70–90 páginas (dentro del rango 60–120).

3. Tabla de alineación objetivos ↔ capítulos ↔ evidencias
Objetivo específico	Capítulo donde se cumple	Evidencia esperada	Resultado/Documento	Indicador de cumplimiento
OE1 — Revisión sistemática PRISMA	Cap. II §2.1	Protocolo PRISMA, búsqueda en Scopus/IEEE/ACM/ScienceDirect, cribado, matriz final	Diagrama PRISMA + matriz de estudios (Apéndice A)	N° de estudios incluidos justificado; flujo PRISMA completo; síntesis por ejes temáticos
OE2 — Requerimientos técnicos, pedagógicos, funcionales	Cap. IV §4.1 + §4.2.1	Documento de requerimientos validado por tutor	Documento de requerimientos (Apéndice C)	RF/RNF/RP numerados, trazables a objetivos, validados por director
OE3 — Implementación curso Moodle + componentes IA Ollama	Cap. IV §4.2.2, §4.2.3, §4.3	Curso desplegado, código del backend, ingesta RAG, prompts validados	Curso funcional + repositorio de código + guías de instalación (Apéndice E)	Curso operativo accesible; tutor IA respondiendo con contexto; criterios de validación de prompts documentados
OE4 — Evaluación de efectividad y precisión IA	Cap. III + Cap. IV §4.4–§4.7	Resultados pre/post, Likert, rúbricas, métricas IA	Reporte de evaluación + datos crudos (Apéndice H)	Estadísticos descriptivos/inferenciales reportados; métricas IA con rúbrica operacional; análisis de áreas de mejora
OE5 — Conclusiones, recomendaciones, trabajos futuros	Cap. V	Síntesis del resto del documento	Capítulo V completo	Una conclusión por OE; recomendaciones accionables; agenda de trabajo futuro
4. Prompt reutilizable largo

Actúa como redactor académico del Trabajo de Integración Curricular en la ESPE 
para el proyecto "Integración de herramientas de inteligencia artificial para el 
diseño e implementación de un curso virtual interactivo de mezcla y masterización 
utilizando Moodle y Ollama".

VARIABLES DE ESTA TAREA
- Capítulo: [CAPÍTULO]
- Sección/subsección a redactar: [SECCIÓN]
- Objetivo específico vinculado: [OBJETIVO_ESPECÍFICO_RELACIONADO]
- Archivos fuente que debes leer antes de escribir: [ARCHIVOS_A_USAR]
- Extensión aproximada: [EXTENSIÓN_APROXIMADA] páginas / palabras
- Norma de citación: [ESTILO_DE_CITACIÓN] (IEEE por defecto)
- Estado actual del proyecto: [ESTADO_ACTUAL_DEL_PROYECTO]
- Contenido prohibido en esta sección: [QUÉ_NO_DEBE_INCLUIR]

REGLAS OBLIGATORIAS
1. Antes de redactar, lee los archivos listados en [ARCHIVOS_A_USAR]. Si alguno 
   no existe en el directorio, detente y pide el archivo en vez de inventar.
2. Redacta en tono académico claro, en español, voz impersonal o tercera persona, 
   sin marketing.
3. No inventes resultados, métricas, tamaños muestrales ni hallazgos que no 
   consten en los archivos provistos. Donde falte evidencia, escribe 
   "[EVIDENCIA PENDIENTE: descripción concreta de lo que falta]".
4. Cita únicamente fuentes que aparezcan en la nota conceptual aprobada, en los 
   archivos provistos, o que yo te entregue en esta tarea. No fabriques 
   referencias.
5. Mantén alineación estricta con el objetivo específico [OBJETIVO_ESPECÍFICO_RELACIONADO]. 
   Si un párrafo no contribuye a ese objetivo, elimínalo.
6. No copies frases textuales de fuentes marcadas como riesgo autoral (auditoría 
   forense). Si una idea proviene de Rabinovich u otra fuente señalada, 
   reformúlala con atribución explícita o reemplázala por fuente alternativa.
7. Propón tablas o figuras solo si aportan información que el texto plano no 
   transmite con la misma claridad. Numéralas según convención ESPE 
   (Tabla N, Figura N) e incluye nota al pie con la fuente.
8. Distingue siempre las capas del sistema: contenido pedagógico ≠ Moodle ≠ 
   componente IA/Ollama ≠ tutor contextual/RAG ≠ instrumentos de evaluación.
9. No conviertas la sección en manual de mezcla/masterización. El foco es la 
   integración IA + LMS + diseño instruccional + evaluación.
10. Cierra la sección con una transición de 2–3 líneas que conecte con la 
    siguiente sección del índice aprobado.
11. Respeta máximo tres niveles de jerarquía (X / X.Y / X.Y.Z).
12. No uses emojis. No uses lenguaje promocional ("revolucionario", 
    "innovador", "potente").

ENTREGA ESPERADA
- Texto listo para pegar en Word con jerarquía clara.
- Lista de referencias usadas en esta sección (solo las citadas).
- Lista de "[EVIDENCIA PENDIENTE: ...]" al final, si aplica.
- Sugerencia de tablas/figuras con su título propuesto.
5. Prompt corto de continuidad

Redacta [SECCIÓN] del índice aprobado del TIC. 
Objetivo específico vinculado: [OEX]. 
Archivos a usar: [LISTA]. 
Extensión: [N páginas]. 
Aplica todas las reglas del prompt reutilizable largo ya acordado: 
sin inventar resultados, sin citar fuentes no provistas, sin copiar de 
fuentes con riesgo autoral, separando capas del sistema, con cierre 
de transición a la siguiente sección.
6. Archivos que debes tener siempre disponibles
Indispensables para que cualquier redacción salga correcta:

Anexo 5 - Plantilla TIC (lo tengo ya).
UDED-LNM-2026-V9-002 Lineamientos UIC (lo tengo ya).
Nota conceptual aprobada (la tengo ya).
Anexo 13 — Guía metodológica del repositorio ESPE (no la tengo: pídela a biblioteca).
Anexo 17 — Lista de cotejo de entrega del TIC (no la tengo: la usaremos antes de cerrar).
KENTH_Eje0_Contenido_Canonico.md a KENTH_Eje7_Contenido_Canonico.md (no están en el repo visible).
estructura_congelada_lecciones_kenth.md (no está en el repo visible).
Eje2_Guiones_KENTH_v2.md, Eje3_Guiones_KENTH_v2.md, Eje4_Guiones_KENTH_v2.md (no están en el repo visible).
auditoria_forense_autoria_rabinovich.md (no está en el repo visible — crítica para evitar contaminación).
Carpeta de código del backend RAG (tesis-rag/) y base vectorial (bd_vectorial/) — sí existen en el repo, ya las localicé.
Datos del piloto cuando los tengas: respuestas Likert, pre/post-test, rúbricas, trazas Moodle. Sin esto, el Capítulo IV §4.5–§4.7 queda con placeholders.
Protocolo PRISMA-S completado por ti antes de redactar §2.1.
Instrumentos validados (encuestas, rúbricas) firmados por el director.
Documento de consentimiento informado para el piloto.
Para arrancar la redacción del Capítulo I ya tengo lo suficiente. El Capítulo II requiere que ejecutes PRISMA primero (no se puede redactar de memoria). El Capítulo IV requiere los archivos KENTH y los guiones — súbelos al repo o pásamelos cuando vayamos a esa fase.