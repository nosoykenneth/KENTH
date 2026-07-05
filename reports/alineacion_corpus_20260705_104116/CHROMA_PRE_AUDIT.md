# Chroma pre-audit

- Chroma dir: `/app/bd_vectorial`
- Coleccion: `langchain`
- Total chunks: 591
- Fuentes unicas: 78

## Distribucion
- Por course_id: `{'2': 591}`
- Por section_number: `{'1': 233, '2': 36, '3': 50, '4': 50, '5': 61, '6': 52, '7': 51, '8': 58}`
- Por moodle_section_id: `{'2': 233, '3': 36, '4': 50, '5': 50, '20': 61, '19': 52, '18': 51, '17': 58}`
- Por lesson_id: `{'SEC2-R55': 38, 'SEC2-R56': 37, 'SEC2-R57': 36, '<empty>': 371, 'SEC2-R58': 27, 'SEC2-R59': 27, 'SEC2-R60': 27, 'SEC2-R61': 28}`
- Por source_type: `{'transcript': 24, 'resource_file': 1, 'canonical_md': 566}`
- Por corpus_version: `{'<empty>': 591}`

## Controles de basura/stale
- allowed_for_indexing_false: 0
- axis_id: 0
- canonical_source_not_expected: 358
- deleted_local_paths: 358
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
- STALE_IN_CHROMA: 7

## Stale chunks detectados
- `documentos/oficial/curso_2/seccion_02_leer_la_senal/contenido_canonico.md` -> 36 chunks
- `documentos/oficial/curso_2/seccion_03_integridad_de_la_senal/contenido_canonico.md` -> 50 chunks
- `documentos/oficial/curso_2/seccion_04_identidad_espectral/contenido_canonico.md` -> 50 chunks
- `documentos/oficial/curso_2/seccion_05_energia_y_movimiento/contenido_canonico.md` -> 61 chunks
- `documentos/oficial/curso_2/seccion_06_dimension_espacial/contenido_canonico.md` -> 52 chunks
- `documentos/oficial/curso_2/seccion_07_integracion_global/contenido_canonico.md` -> 51 chunks
- `documentos/oficial/curso_2/seccion_08_traduccion_y_entrega/contenido_canonico.md` -> 58 chunks

## Faltantes aprobados
- 0

## Excluidos indexados
- 0
