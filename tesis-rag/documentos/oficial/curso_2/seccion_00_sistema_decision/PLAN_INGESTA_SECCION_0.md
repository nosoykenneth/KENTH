---
course_id: "2"
moodle_section_id: "2"
section_number: "1"
section_title: "SECCIÓN 0: El sistema de decisión"
source_type: "operational_plan"
scope: "section"
visible_to_student: false
allowed_for_indexing: false
status: "excluded_operational"
source_origin: "course"
---

# Plan de ingesta — Sección 0 "El sistema de decisión"

> Documento operativo. `allowed_for_indexing: false`, `visible_to_student: false`.
> Acompaña a `INGEST_MANIFEST_SECCION_0.csv` / `.json`. Resultado ejecutado: ver `../../reports/INGESTA_SECCION_0_REPORTE.md`.

## 1. Resumen de auditoría
77 MD (7 sección + 7×10 lección). 0 vacíos, YAML válido, UTF-8, sin secretos, sin enlaces http(s). Ver reporte para detalle.

## 2. Correcciones aplicadas (metadata/flags; contenido intacto)
- QA: `source_type → qa_report`, `status → excluded_operational`.
- Recursos externos: `allowed_for_indexing → false`, `status → needs_human_approval`.
- Prompts de evaluación (×7): `false/false`, `status → excluded_evaluation`.
- Manifest de indexación: `false/false`, `status → excluded_operational`.
- Guías del tutor (×7) y demás indexados-no-visibles (20 archivos): `internal_context: true`.
- Indexables aprobados: `status → approved_for_ingestion`. Total: 99 cambios.

## 3. Clasificación (67 indexables / 10 excluidos lado-corpus → 22 indexados este batch)
- **Indexados ahora (22):** 4 nivel-sección + 0.1(01–09) + 0.2(01–09). Ver `INGEST_MANIFEST_SECCION_0.csv` col `action=INDEX_*`.
- **Retenidos (45):** lecciones 0.3–0.7 (`action=HOLD_pending_lesson_mapping`).
- **Excluidos (10):** eval prompts, QA, manifest, recursos externos (`action=EXCLUDE_never_index`).

## 4. Mapping archivo → destino / lección real
- Sección 0 (corpus) = `course_id=2`, `moodle_section_id=2`, `section_number=1`, slug `el_sistema_de_decision`.
- 0.1 → `lesson_id=SEC2-R55` · 0.2 → `lesson_id=SEC2-R56` (matches fuertes/exactos).
- 0.3, 0.4, 0.5, 0.6, 0.7 → sin lección real → **retenidas**. SEC2-R57 "Volumen y Gain" → sin mapear (débil).
- Nivel-sección → sin `lesson_id`, `scope=section`.

## 5. Flags por archivo
Fuente de verdad: frontmatter corregido + `INGEST_MANIFEST_SECCION_0.*`. Reglas: los `visible_to_student=false` van con `internal_context=true`; el tutor los usa como conocimiento pero NO deben exponerse como fuente citada.

## 6. Endpoint / script
`ingest.add_single_document(<archivo>)` **acotado por archivo** (incremental, delete-then-add por `source_path`), vía `docker exec tic-fastapi python /app/ingest_seccion0.py [--commit]`. Dry-run obligatorio antes del commit. **Prohibido** `/documents/rebuild` (global/destructivo) para esta operación.

## 7. Plan de backup (ejecutado)
`cp -r runtime/chroma` → `reports/ingesta_seccion_0_<ts>/chroma_backup` + `pre_index_state.json`. No se tocan tablas de BD.

## 8. Plan de ingesta (ejecutado)
1. Generar árbol server-ready con frontmatter de sistema (course_id/moodle_section_id/section_number/lesson_id/scope + provenance). 2. Copiar a host-repo `documentos/oficial/curso_2/seccion_00_sistema_decision/`. 3. `docker cp` al contenedor vivo. 4. Dry-run política. 5. `--commit`.

## 9. Plan de reindex
No aplica rebuild global. La consolidación durable se logró con `docker compose build fastapi && up -d fastapi` (hornea archivos; Chroma persiste en volumen).

## 10. Validadores
- Chroma: `total`, `by_source`, `by_scope`, `by_lesson_id`; EVAL/QA/oper indexados=0; otras secciones=0; retenidas=0; seccion_00 únicos=22.
- Health `status:ok`, `chroma_chunks` esperado 97.

## 11. Preguntas de prueba (chat, token estudiante)
2×0.1, 2×0.2, 1 fuera-de-dominio, 1 ambigua, 1 guía-interna. (0.5 no aplica: retenida.) Ver tabla de resultados en el reporte.

## 12. Rollback
Fino: `remove_single_document` de los 22 `source_path`. Completo: restaurar `chroma_backup`. Filesystem: borrar `seccion_00_sistema_decision/` + rebuild.

## 13. Evidencia para tesis
`reports/ingesta_seccion_0_<ts>/` (backup, pre/post state, commands.log, ingest_commit.log, chat_tests_result.json) + este plan + manifiestos + `INGESTA_SECCION_0_REPORTE.md`.
