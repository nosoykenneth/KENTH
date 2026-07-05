# Alineacion corpus RAG

Estado al 2026-07-05:

- `tesis-rag/documentos/` es la fuente canonica viva de ingesta.
- `corpus/` raiz no existe localmente y no es fuente de ingesta.
- Chroma fue limpiado incrementalmente por `source_path`: 591 -> 233 chunks.
- Se removieron 358 chunks stale de 7 archivos de secciones 02-08 eliminados localmente.
- Post-audit: 67 archivos canonicos indexables OK, 0 missing, 0 stale, 0 eval/QA/manifests operativos/reportes/corpus raiz, 0 `axis_id`/`scope=axis`.
- Backup servidor: `reports/alineacion_corpus_20260705_104116/chroma_backup`.
- Seccion pedagogica 0 se mantiene mapeada internamente a Moodle `section_number=1` / `moodle_section_id=2`.

Cierres adicionales:

- Servidor normalizado en `chore/align-corpus-rag-index`; worktree limpio salvo artefactos ignorados/server-only.
- Chat autenticado validado: 9/9 PASS con token real de estudiante, sin imprimir token.
- Health OK, smoke OK, `validate_rag_index.py` OK.

Pendiente:

- Revisar y mergear el PR `chore/align-corpus-rag-index` -> `main`.
- Tras merge, dejar el servidor nuevamente en `main` con pull/deploy limpio.

Reporte completo: `reports/alineacion_corpus_20260705_104116/REPORTE_FINAL_ALINEACION_CORPUS.md`.
