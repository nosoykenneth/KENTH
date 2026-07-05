---
course_title: "Mezcla y Masterización"
section_number: 0
section_title: "El sistema de decisión"
lesson_number: ""
lesson_title: ""
source_type: "qa_report"
recommended_scope: "section"
visible_to_student: false
allowed_for_indexing: false
status: "excluded_operational"
---

# QA del corpus — Sección 0

Control de calidad del corpus generado para la Sección 0 "El sistema de decisión". Documento operativo (no indexable, no visible al estudiante).

## Archivos creados

### Nivel sección (6)
00_seccion_overview.md · 00_glosario_seccion.md · 00_mapa_conceptual_seccion.md · 00_atribuciones_seccion.md · 00_manifest_indexacion_seccion.md · 00_recursos_externos_sugeridos.md

### Lecciones (7 × 10 = 70)
Cada carpeta de lección (0.1 a 0.7) contiene: 01_contenido_canonico.md, 02_guia_tutor_ia.md, 03_momentos_clase.md, 04_glosario.md, 05_preguntas_frecuentes.md, 06_actividad_practica.md, 07_rubrica_actividad.md, 08_recursos_manifest.md, 09_atribuciones.md, 10_prompt_evaluacion.md.

### QA (1)
00_QA_CORPUS_SECCION_0.md (este archivo).

## Conteo de archivos
- Archivos Markdown de contenido: 76 (6 de sección + 70 de lección).
- Con este QA: 77 archivos Markdown en total.
- Carpetas de lección: 7.

## Verificaciones de requisitos cumplidas
- Contenido canónico: entre 908 y 1126 palabras por lección (rango objetivo 900–1400). Cumple.
- Glosario por lección: 12–13 términos (mínimo 12). Cumple.
- Preguntas frecuentes: 16 por lección (mínimo 15). Cumple.
- Momentos de clase: 7–8 por lección (rango 5–8). Cumple.
- Glosario de sección: 15 términos transversales. Cumple.
- Frontmatter YAML presente en los 77 archivos, con los campos exigidos.

## Observación menor (para revisión de autor)
- Guía del tutor (02): 528–619 palabras por lección, algo por debajo del rango sugerido (700–1100). El contenido cubre los 11 apartados exigidos (rol, reforzar, responder, evitar, profundidad, temas complementarios, límites, ejemplos buenos, ejemplos malos, reglas de lenguaje, cuándo pedir precisión). Se optó por concisión sin relleno; si se desea, el autor puede ampliar ejemplos para acercarse al rango. No es un placeholder ni contenido faltante.

## Qué SE DEBE indexar (allowed_for_indexing: true)
- Todos los 01_contenido_canonico, 02_guia_tutor_ia, 03_momentos_clase, 04_glosario, 05_preguntas_frecuentes, 06_actividad_practica, 07_rubrica_actividad, 08_recursos_manifest y 09_atribuciones de las 7 lecciones.
- De sección: overview, glosario, mapa conceptual, atribuciones de sección y recursos externos sugeridos.

## Qué NO se debe indexar (allowed_for_indexing: false)
- Los 7 archivos 10_prompt_evaluacion.md (contienen respuestas esperadas; evitar contaminación de la evaluación).
- 00_manifest_indexacion_seccion.md (solo operativo del pipeline).
- 00_QA_CORPUS_SECCION_0.md (este archivo, operativo).

## Visibilidad al estudiante
- Visibles (visible_to_student: true): contenidos canónicos, glosarios, FAQ, actividades, rúbricas, recursos_manifest, overview, glosario de sección, mapa conceptual, recursos externos, y las atribuciones de 0.2 y 0.6 (didácticas).
- No visibles (false): todas las guías del tutor (02), los prompts de evaluación (10), las atribuciones no didácticas (0.1, 0.3, 0.4, 0.5, 0.7), atribuciones de sección, manifest de indexación y este QA.

## Riesgos de copyright detectados y su manejo
- 0.2 (curvas de igual sonoridad): riesgo medio. Se describe el fenómeno con redacción propia y se atribuye a Fletcher-Munson e ISO 226 sin reproducir tablas ni gráficos propietarios. Correcto.
- 0.6 (emulaciones y marcas): riesgo medio. Se habla por función y categoría; las marcas se tratan como referencia descriptiva; no se recomiendan compras ni se reproduce material de fabricantes. Correcto.
- Resto de lecciones: riesgo bajo; conceptos de dominio general redactados de forma propia.
- Referencias musicales y multipistas: propiedad de sus dueños. No se incluye ningún binario en el corpus; solo descripciones textuales y sugerencias de recursos externos con licencia clara.

## Atribuciones críticas
- Atribución obligatoria y correctamente incluida en 0.2: Fletcher-Munson (1933) e ISO 226 para las curvas de igual sonoridad.
- Nota de marcas en 0.6: tratar nombres de fabricantes/equipos como marcas registradas de sus dueños; solo referencia descriptiva.
- Reglas transversales en 00_atribuciones_seccion.md.

## Recursos no textuales que faltan generar (no son placeholders de texto; dependen de producción física)
- Imágenes/diagramas: ciclo de decisión (0.1), esquema de igual sonoridad propio (0.2), colocación de monitores y efecto de sala (0.3), flujo de señal y serie/paralelo (0.4), gain staging por etapas (0.5), matriz de decisión y "misma función distinto cómo" (0.6), checklist de seis bloques y sesión ordenada (0.7).
- Proyectos DAW: sesiones base y de práctica por lección, y una plantilla de sesión modelo (0.7).
- Audio: multipistas/stems de práctica (a obtener de librerías con licencia; no incluidas).
- Plantillas de texto: bitácora de decisiones (0.1), matriz de decisión (0.6), checklist imprimible (0.7).
Cada recurso no textual ya cuenta con su descripción textual indexable en el 08_recursos_manifest correspondiente.

## Recomendaciones para el siguiente paso
1. Producir los diagramas e imágenes listados y vincularlos a sus descripciones indexables.
2. Preparar los proyectos DAW base y la plantilla de sesión; verificar rutas y niveles.
3. Conseguir multipistas de práctica con licencia adecuada (ver 00_recursos_externos_sugeridos.md).
4. Revisión editorial humana de las 7 guías del tutor si se desea acercarlas al rango de palabras sugerido.
5. Confirmar en el pipeline que los 10_prompt_evaluacion y los archivos operativos quedan excluidos del índice de recuperación.
6. Cambiar el campo status de "draft_generated" a un estado aprobado tras la revisión.
