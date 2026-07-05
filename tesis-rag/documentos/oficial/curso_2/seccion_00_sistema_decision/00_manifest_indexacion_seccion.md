---
course_id: "2"
moodle_section_id: "2"
section_id: "2"
section_number: "1"
section_slug: "el_sistema_de_decision"
section_title: "SECCIÓN 0: El sistema de decisión"
lesson_id: ""
lesson_number: ""
lesson_title: ""
source_type: "resource_manifest"
scope: "section"
source: "canonical_md"
content_type: "markdown"
visible_to_student: false
allowed_for_indexing: false
status: "excluded_operational"
source_origin: "course"
corpus_version: "seccion_0_v1"
ingestion_batch_id: "seccion0_20260704"
original_relative_path: "00_manifest_indexacion_seccion.md"
---

# Manifiesto de indexación — Sección 0

Tabla operativa para el pipeline RAG. Define, por tipo de archivo, si se indexa, si es visible al estudiante, su scope recomendado, su capa (layer) y el motivo. La capa distingue material de estudiante (canónico/actividad), material del tutor (guía/prompt) y material operativo (manifiestos).

| Archivo | Indexar sí/no | Visible estudiante sí/no | Scope recomendado | Layer | Motivo |
|---|---|---|---|---|---|
| 00_seccion_overview.md | Sí | Sí | section | student | Contexto general útil para respuestas de encuadre |
| 00_glosario_seccion.md | Sí | Sí | section | student | Definiciones transversales consultables |
| 00_mapa_conceptual_seccion.md | Sí | Sí | section | student | Relaciones entre lecciones |
| 00_atribuciones_seccion.md | Sí | No | section | tutor | Reglas para no responder mal; no didáctico para alumno |
| 00_manifest_indexacion_seccion.md | No | No | section | ops | Solo operativo del pipeline |
| 00_recursos_externos_sugeridos.md | Sí | Sí | section | student | Recursos legales consultables |
| 01_contenido_canonico.md (cada lección) | Sí | Sí | lesson | student | Núcleo didáctico |
| 02_guia_tutor_ia.md (cada lección) | Sí | No | lesson | tutor | Guía interna del tutor |
| 03_momentos_clase.md (cada lección) | Sí | No | block | tutor | Estructura temporal para el tutor |
| 04_glosario.md (cada lección) | Sí | Sí | lesson | student | Vocabulario de la lección |
| 05_preguntas_frecuentes.md (cada lección) | Sí | Sí | lesson | student | Respuestas frecuentes |
| 06_actividad_practica.md (cada lección) | Sí | Sí | lesson | student | Instrucciones de práctica |
| 07_rubrica_actividad.md (cada lección) | Sí | Sí | lesson | student | Criterios de evaluación visibles |
| 08_recursos_manifest.md (cada lección) | Sí | Sí | lesson | student | Recursos y sus descripciones indexables |
| 09_atribuciones.md (cada lección) | Sí | Según lección | lesson | tutor | Reglas de atribución |
| 10_prompt_evaluacion.md (cada lección) | No | No | lesson | eval | Contiene respuestas esperadas; no debe contaminar RAG |

## Reglas de resolución de conflictos
Si un archivo aparece en varios scopes, prevalece el más específico disponible para la consulta (block > lesson > section). El material `eval` nunca entra al índice de recuperación general. El material `tutor` se indexa pero se marca para uso del sistema, no para cita directa al estudiante.
