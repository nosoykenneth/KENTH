# Plan de borrado / movimiento (FASE 4-5) — Estrategia B (consolidar Sección 0)

Fecha: 2026-07-05 · Rama: `chore/corpus-canonical-cleanup` · Backup externo confirmado por el dueño.

## Se MIGRA (transform authoring → system frontmatter)
`corpus/seccion_00_sistema_decision/**` (77 MD + 3 operativos) → `tesis-rag/documentos/oficial/curso_2/seccion_00_sistema_decision/**`
- Vía script versionado `tesis-rag/scripts/promote_seccion_corpus.py`, que lee `INGEST_MANIFEST_SECCION_0.json` (spec autoritativa) y emite frontmatter de sistema (`course_id, moodle_section_id, section_id, section_number=1, section_slug, scope, source, source_origin, lesson_id`).
- Política de flags aplicada por `action` del manifest:
  - `INDEX_lesson` (0.1→SEC2-R55, 0.2→SEC2-R56): `allowed_for_indexing:true`, `scope:lesson`.
  - `INDEX_section` (overview, glosario, mapa, atribuciones sección): `allowed_for_indexing:true`, `scope:section`.
  - `EXCLUDE_never_index` (7×prompt_evaluacion, QA, manifest_indexacion, recursos_externos): `allowed_for_indexing:false`.
  - `HOLD_pending_lesson_mapping` (lecciones 0.3–0.7, 45 archivos): `allowed_for_indexing:false` + `retention_status:pending_lesson_mapping` (retenidas hasta que exista la lección real; reversible re-corriendo el script cuando el manifest tenga `lesson_id_real`).

## Se BORRA
| Ruta | git | Motivo |
|---|---|---|
| `corpus/` (raíz, 80 archivos tracked) | tracked | queda vacío tras migrar; ya no es fuente activa (evita "dos fuentes activas") |
| `corpus_seccion_00.zip` (raíz) | untracked | binario pesado redundante (hay backup externo) |
| `00_QA_CORPUS_SECCION_0.md` (raíz) | untracked | duplicado suelto de QA en la raíz |
| `tesis-rag/documentos/oficial/curso_2/seccion_01_el_sistema_de_decision/contenido_canonico.md` | tracked | **versión vieja de la Sección 0** (1 archivo, migrado de Eje 0); superseded por la nueva Sección 0 detallada. Ambos anclan `moodle_section_id=2` → evita dos versiones activas |

## NO se toca
- `documentos/oficial/curso_2/seccion_02..08/` (canónico vivo de secciones 2-8).
- `documentos/no_indexar/**`, `documentos/oficial/{guiones,global,TEMARIO,curso_manifest.json}` (material fuente no indexado; no es corpus viejo conflictivo).
- Servidor, Chroma, MariaDB, runtime/, .env, backups.

## Consecuencia conocida (documentada)
Tras la consolidación, la cobertura INDEXABLE de la Sección 0 (en un futuro reindex) = lecciones 0.1 + 0.2 + nivel-sección. Las 0.3–0.7 quedan retenidas (igual que en el servidor). Reactivación = crear las lecciones, completar `lesson_id_real` en el manifest y re-correr el script (flip a indexable) + ingesta acotada. **No se valida con reindex local (prohibido); se valida con el gate `es_documento_aprobado_para_indexar` (FASE 7).**
