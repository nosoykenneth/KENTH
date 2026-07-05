# Chroma post-audit

## Resultado
- Health post-cleanup: `ok`.
- Chroma chunks en health: `233`.
- Coleccion: `langchain`.
- Total chunks: 233.
- Fuentes unicas: 71.
- Cleanup delta: 591 -> 233 (358 chunks removidos).

## Distribucion
- Por course_id: `{'2': 233}`
- Por section_number: `{'1': 233}`
- Por moodle_section_id: `{'2': 233}`
- Por lesson_id: `{'SEC2-R55': 38, 'SEC2-R56': 37, 'SEC2-R57': 36, '<empty>': 13, 'SEC2-R58': 27, 'SEC2-R59': 27, 'SEC2-R60': 27, 'SEC2-R61': 28}`
- Por source_type: `{'transcript': 24, 'resource_file': 1, 'canonical_md': 208}`
- Por corpus_version: `{'<empty>': 233}`

## Gates post-index
- allowed_for_indexing_false: 0
- axis_id: 0
- canonical_source_not_expected: 0
- deleted_local_paths: 0
- evaluation_prompt: 0
- excluded_paths: 0
- external_resources_suggested: 0
- operational_manifest: 0
- pending_or_hold: 0
- qa: 0
- report: 0
- resource_manifest_chunks: 0
- root_corpus: 0
- scope_axis: 0
- visible_to_student_false: 59

## Estados corpus vs Chroma
- OK_INDEXED: 67

## Fuentes removidas
- `documentos/oficial/curso_2/seccion_02_leer_la_senal/contenido_canonico.md`: 36 -> 0 chunks
- `documentos/oficial/curso_2/seccion_03_integridad_de_la_senal/contenido_canonico.md`: 50 -> 0 chunks
- `documentos/oficial/curso_2/seccion_04_identidad_espectral/contenido_canonico.md`: 50 -> 0 chunks
- `documentos/oficial/curso_2/seccion_05_energia_y_movimiento/contenido_canonico.md`: 61 -> 0 chunks
- `documentos/oficial/curso_2/seccion_06_dimension_espacial/contenido_canonico.md`: 52 -> 0 chunks
- `documentos/oficial/curso_2/seccion_07_integracion_global/contenido_canonico.md`: 51 -> 0 chunks
- `documentos/oficial/curso_2/seccion_08_traduccion_y_entrega/contenido_canonico.md`: 58 -> 0 chunks

## Conclusion
El indice Chroma queda alineado con el conjunto canonico local aprobado: no hay stale chunks, faltantes, excluidos indexados ni metadatos legacy `axis_id`/`scope=axis`.
