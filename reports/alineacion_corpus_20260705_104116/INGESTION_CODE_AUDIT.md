# Auditoria del codigo de ingesta

Fecha local: 2026-07-05

## Resultado ejecutivo

- Fuente real de ingesta: `tesis-rag/documentos`, via `DOCUMENTS_DIR` en `tesis-rag/ingest.py`.
- Carpetas publicas recorridas: `documentos/oficial/cursos`, `documentos/oficial/global` y `documentos/oficial/curso_<id>` detectadas al importar el modulo.
- `corpus/` raiz no aparece como fuente activa de ingesta. Si existe, queda fuera del walk y debe tratarse como autoria/residuo.
- Gate oficial usado para decidir indexacion: `es_documento_aprobado_para_indexar(filepath, explicar=True)`.
- Metodo incremental seguro existente: `add_single_document(filepath)`, que ejecuta `remove_single_document(filepath)` antes de anadir chunks nuevos.
- Eliminacion fina existente: `remove_single_document(filepath)` borra por metadata `source_path` y por `source` legado.
- Rebuild global existente: `rebuild_all_documents()` borra la coleccion completa. Es destructivo y no se debe usar como primera opcion.
- Reindex por curso existente: `reindex_course_documents(course_id)` reindexa conocimiento DB-driven del curso, pero no purga el corpus canonico `canonical_md`; no sirve por si solo para limpiar stale chunks de archivos Markdown canonicos eliminados.

## Evidencia de rutas

- `tesis-rag/ingest.py:25-30`: define `DOCUMENTS_DIR`, `OFFICIAL_DIR`, `EXTERNAL_DIR` y `NO_INDEX_DIR` bajo `tesis-rag/documentos`.
- `tesis-rag/ingest.py:93-99`: `ALLOWED_PUBLIC_DIRS` incluye uploads de curso, global y carpetas canonicas `curso_<id>`; no incluye `corpus/` raiz.
- `tesis-rag/ingest.py:239-245`: `_es_ruta_permitida()` rechaza rutas fuera de carpetas publicas, `externo`, `no_indexar` y directorios excluidos.
- `tesis-rag/ingest.py:363-386`: `get_safe_document_candidates()` recorre solo `ALLOWED_PUBLIC_DIRS` y luego aplica el gate oficial.

## Politica de gate

- `tesis-rag/ingest.py:317-360`: `es_documento_aprobado_para_indexar()` valida existencia, extension, ruta permitida, patrones prohibidos, nombre seguro, metadata y flags.
- La auditoria local no implemento una politica alternativa para aprobar archivos: ejecuto esta funcion real y uso su salida como fuente de verdad.
- Resultado local actual: 67 `gate_ok` y 31 `gate_reject` bajo `tesis-rag/documentos`.

## Comportamiento de escritura en Chroma

- `tesis-rag/ingest.py:1104-1160`: `add_single_document()` procesa un archivo y antes de insertar llama a `remove_single_document(filepath)`.
- `tesis-rag/ingest.py:1164-1183`: `remove_single_document()` borra por variantes de `source_path` y `source`, incluyendo compatibilidad con indice viejo.
- Esto permite correccion incremental por archivo cuando el diff sea pequeno y los `source_path` sean confiables.

## Riesgos detectados

- `rebuild_all_documents()` (`tesis-rag/ingest.py:1564+`) borra toda la coleccion Chroma. Solo corresponde si el diff demuestra que la limpieza incremental no es confiable, con backup previo y autorizacion para el alcance.
- `reindex_course_documents(course_id)` (`tesis-rag/ingest.py:1191+`) no limpia `canonical_md` del curso; por diseno conserva el corpus canonico y solo reindexa documentos/recursos/transcripciones DB-driven. No debe venderse como solucion para stale chunks de Markdown borrados.
- Los `08_recursos_manifest.md` de leccion tienen `source_type=resource_manifest`, `allowed_for_indexing=true` y son descripciones pedagogicas visibles al estudiante. No son manifiestos operativos como `00_manifest_indexacion_seccion.md`.

## Scripts y documentacion relacionada

- `tesis-rag/scripts/reindex_rag_clean.py`: wrapper destructivo que ejecuta `rebuild_all_documents()` y luego DB-driven; valida con `validate_rag_index.py`.
- `tesis-rag/scripts/validate_rag_index.py`: valida Chroma sin Ollama; detecta `axis_id`, `scope=axis`, chunks seccionales sin seccion, chunks sin curso y duplicados por `source_hash` entre rutas.
- `docs/tic/PLAN_INGESTA_CORPUS.md`: documenta el flujo seguro: auditar, corregir flags, respaldar Chroma, ingestar acotado y validar.
- `reports/INGESTA_SECCION_0_REPORTE.md` y `reports/INGESTA_SECCION_0_LECCIONES_0307_REPORTE.md`: evidencian que la Seccion 0 se indexo con `add_single_document()` acotado, no con rebuild global.

## Conclusion de FASE 2

El codigo real coincide con la fuente canonica declarada: `tesis-rag/documentos/` es la raiz viva de ingesta y `corpus/` raiz no se usa. Para stale chunks de archivos eliminados, la estrategia preferente sera incremental por `source_path` si el pre-audit de Chroma encuentra residuos. Un rebuild global queda descartado salvo autorizacion explicita.