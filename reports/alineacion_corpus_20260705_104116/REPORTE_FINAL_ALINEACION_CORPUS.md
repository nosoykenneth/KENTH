# Reporte final de alineacion corpus RAG

## 1. Estado local
- Rama/estado inicial: `## main...origin/main`.
- HEAD local: `c9f496c1402fc0d6983c03b020816356f424ef2f`.
- origin/main: `c9f496c1402fc0d6983c03b020816356f424ef2f`.
- Local HEAD == origin/main: `True`.
- Cambios locales de corpus detectados: 24 archivos borrados bajo `tesis-rag/documentos`.

## 2. Estado servidor
- Servidor accesible en `/srv/kenneth/tic-kenth`.
- Compose correcto usado: `docker-compose.deploy.yml --env-file .env`.
- 9 contenedores `tic-*` arriba; `tic-mariadb` healthy.
- Health post-cleanup: `ok`; Chroma `ok`; Ollama `ok`; chunks `233`.
- Drift: el servidor no tiene worktree limpio; ver `SERVER_PRE_AUDIT.md` y `LOCAL_SERVER_DIFF.md`.

## 3. Fuente canonica confirmada
- Fuente canonica viva: `tesis-rag/documentos/`.
- `corpus/` raiz local no existe y no es fuente de ingesta.
- El codigo real (`ingest.py`) recorre `documentos/oficial/cursos`, `documentos/oficial/global` y `documentos/oficial/curso_<id>`; no recorre `corpus/` raiz.

## 4. Archivos eliminados detectados
- Local: 24 borrados pendientes.
- En Chroma pre-cleanup habia 7 fuentes eliminadas localmente con chunks activos.

## 5. Archivos que ya no estan en Chroma
- `documentos/oficial/curso_2/seccion_02_leer_la_senal/contenido_canonico.md`: 36 -> 0 chunks
- `documentos/oficial/curso_2/seccion_03_integridad_de_la_senal/contenido_canonico.md`: 50 -> 0 chunks
- `documentos/oficial/curso_2/seccion_04_identidad_espectral/contenido_canonico.md`: 50 -> 0 chunks
- `documentos/oficial/curso_2/seccion_05_energia_y_movimiento/contenido_canonico.md`: 61 -> 0 chunks
- `documentos/oficial/curso_2/seccion_06_dimension_espacial/contenido_canonico.md`: 52 -> 0 chunks
- `documentos/oficial/curso_2/seccion_07_integracion_global/contenido_canonico.md`: 51 -> 0 chunks
- `documentos/oficial/curso_2/seccion_08_traduccion_y_entrega/contenido_canonico.md`: 58 -> 0 chunks

## 6. Archivos nuevos indexados
- No se indexaron archivos nuevos en esta operacion. La correccion fue limpieza incremental de stale chunks.

## 7. Archivos excluidos correctamente
- Post-cleanup: evaluation_prompt=0, qa=0, operational_manifest=0, reports=0, root_corpus=0, excluded_paths=0.
- `visible_to_student=false`: 59 chunks internos presentes para contexto, no como fuente visible al estudiante; contrato frontend `test:chat-sources` PASS.

## 8. Estrategia usada
- Opcion B: incremental cleanup por `source_path`.
- Justificacion: 67 indexables presentes, 0 faltantes, 7 fuentes stale bien identificadas; rebuild global innecesario.

## 9. Backup creado
- Servidor: `reports/alineacion_corpus_20260705_104116/chroma_backup` (17M).
- Pre-state: `CHROMA_PRE_AUDIT.json`, `CHROMA_PRE_AUDIT.md`, `CHROMA_CLEANUP_RESULT.json`.

## 10. Estado Chroma antes/despues
- Antes: 591 chunks, 67 OK_INDEXED, 7 fuentes stale, 358 chunks stale.
- Despues: 233 chunks, 67 OK_INDEXED, 0 stale, 0 missing, 0 excluded indexed.

## 11. Validacion de metadata
- course_id: `{'2': 233}`.
- section_number: `{'1': 233}`.
- moodle_section_id: `{'2': 233}`.
- lesson_id: `{'SEC2-R55': 38, 'SEC2-R56': 37, 'SEC2-R57': 36, '<empty>': 13, 'SEC2-R58': 27, 'SEC2-R59': 27, 'SEC2-R60': 27, 'SEC2-R61': 28}`.
- Nota: la Seccion pedagogica 0 esta mapeada a Moodle `section_number=1` / `moodle_section_id=2`; no se cambio a la fuerza.

## 12. Pruebas de chat
- Bloqueadas parcialmente por falta de token estudiante utilizable. Ver `CHAT_VALIDATION.md`.
- Validacion indirecta de fuentes internas: `npm run test:chat-sources` PASS.

## 13. Tests ejecutados
- Backend pytest: 198 passed, 4 skipped.
- Frontend `test:moodle-section`: PASS.
- Frontend `test:chat-sources`: PASS.
- Frontend lint: PASS con 5 warnings.
- Frontend build: PASS con warning de chunk grande.
- Smoke produccion: 9 PASS, 0 FAIL; auth omitida.
- `validate_rag_index.py`: OK.

## 14. Riesgos pendientes
- No se puede decir `local/main/servidor alineados`: hay borrados locales sin commit y el servidor tiene worktree dirty con un conjunto distinto de borrados/untracked.
- Si alguien ejecuta un rebuild antes de normalizar filesystem/branch, el servidor podria reintroducir archivos que aun existan fisicamente en su working tree.
- Falta bateria de chat autenticada con token estudiante real.

## 15. Proximos pasos
- Revisar y aprobar la rama `chore/align-corpus-rag-index` con los borrados locales y reportes.
- Tras merge, hacer deploy/pull limpio en servidor y dejar el worktree sin drift.
- Ejecutar bateria de chat con token estudiante y anexar resultados.

## Veredicto
Chroma quedo alineado con el corpus canonico local aprobado. No declaro el DoD completo del encargo porque local/main/servidor aun tienen drift documental y falta validacion de chat autenticada.
