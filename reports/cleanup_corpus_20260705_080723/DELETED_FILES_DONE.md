# Borrado / migración ejecutados (FASE 4-5) — DONE

Fecha: 2026-07-05 · Rama: `chore/corpus-canonical-cleanup` (sin merge)

## Migrado (autoría → canónico ingest-ready)
- **80 archivos** `corpus/seccion_00_sistema_decision/**` → `tesis-rag/documentos/oficial/curso_2/seccion_00_sistema_decision/**`
  vía `tesis-rag/scripts/promote_seccion_corpus.py --commit` (frontmatter de sistema; cuerpos verbatim).
- Resultado del gate real `es_documento_aprobado_para_indexar`: **22 indexables / 58 excluidos-retenidos**, 0 falsos positivos/negativos.
  - 18 lección (0.1→SEC2-R55, 0.2→SEC2-R56) + 4 sección = 22 indexables.
  - 10 EXCLUDE (7×prompt_evaluacion, QA, manifest_indexacion, recursos_externos) → `allowed_for_indexing:false`.
  - 45 HOLD (lecciones 0.3–0.7) → `allowed_for_indexing:false` + `retention_status:pending_lesson_mapping`.
  - 3 companions (PLAN.md, MANIFEST.json, MANIFEST.csv) gateados.

## Borrado
| Ruta | Método | Nº |
|---|---|---|
| `corpus/` (raíz, autoría) | `git rm -r` | 80 archivos |
| `tesis-rag/documentos/oficial/curso_2/seccion_01_el_sistema_de_decision/contenido_canonico.md` (vieja Sección 0, migrada de Eje 0; superseded) | `git rm` | 1 archivo |
| `corpus_seccion_00.zip` (raíz, binario) | `rm` (untracked) | 1 |
| `00_QA_CORPUS_SECCION_0.md` (raíz, stray) | `rm` (untracked) | 1 |
| **Total staged (git rm)** | | **81** |

## Referencias actualizadas
- `tesis-rag/documentos/oficial/curso_2/_seccion_map.json`: entrada Eje 0 marcada `dest_status: superseded_and_removed` + `superseded_by`.
- `docs/tic/PLAN_INGESTA_CORPUS.md`: paso 7 documenta el driver versionado `scripts/promote_seccion_corpus.py`; deuda `allowed_flag is False` marcada **RESUELTA**.
- `reports/INGESTA_SECCION_0_REPORTE.md` y `docs/tic/INGESTA_SECCION_0_REPORTE.md`: línea de "Corpus" apunta al árbol canónico consolidado.

## Intacto (verificado)
- `documentos/oficial/curso_2/seccion_02..08/` (canónico secciones 2-8).
- `documentos/no_indexar/**`, `oficial/{guiones,global,TEMARIO,curso_manifest.json}`.
- `domain_packs/2.json` y `tests/phase0_baseline.json` (taxonomía id `seccion_01_el_sistema_de_decision` = **label** acoplado al gate phase0, NO ruta de archivo; retrieval enlaza por `section_number=1`/`moodle_section_id=2`).
- Servidor, Chroma, MariaDB, runtime/, .env, backups: **no tocados**.
