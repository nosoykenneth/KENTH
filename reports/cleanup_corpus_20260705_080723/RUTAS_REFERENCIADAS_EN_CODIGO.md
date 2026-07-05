# Rutas de corpus referenciadas en el código (FASE 1 — auditoría)

Fecha: 2026-07-05 · Rama base: `main` (`8042271`)

## Pregunta clave: ¿qué carpeta lee el pipeline real?

**Respuesta: `tesis-rag/documentos/`. La carpeta raíz `corpus/` NO la lee ningún código.**

### Evidencia en `tesis-rag/ingest.py`
| Línea | Constante | Valor | Significado |
|---|---|---|---|
| 24-25 | `BASE_DIR` / `DOCUMENTS_DIR` | `tesis-rag/` / `tesis-rag/documentos` | raíz del corpus que el código recorre |
| 26 | `OFFICIAL_DIR` | `documentos/oficial` | subárbol oficial |
| 41-48 | `CANONICAL_COURSE_DIRS` | `glob(documentos/oficial/curso_*)` | **corpus canónico por sección** |
| 95-98 | `ALLOWED_PUBLIC_DIRS` | `oficial/cursos` + `oficial/global` + `curso_*` | **únicas carpetas indexables** |
| 102-116 | `EXCLUDED_DIR_NAMES` | `ejes, no_indexar, externo, backups, ...` | se saltan siempre |

`get_safe_document_candidates()` (363-379) sólo recorre `ALLOWED_PUBLIC_DIRS`. **`corpus/` (raíz del repo) queda completamente fuera del walk.**

### Convención de `course_id` por ruta (`_inferir_course_id`, 576-594)
- `documentos/oficial/curso_<id>/...` → `course_id = <id>` (corpus canónico por sección)
- `documentos/oficial/cursos/<id>/...` → subidas del profesor
- `documentos/oficial/global/...` → `""` (universal)

## Dónde aparece cada ruta

| Ruta | Código Python | Docs / reportes | Rol real |
|---|---|---|---|
| `tesis-rag/documentos/oficial/curso_<id>/…` | `ingest.py`, `reindex_rag_clean.py`, `test_ingest_public_policy.py`, `test_source_policy.py`, `test_rag_secciones.py` | `PLAN_INGESTA_CORPUS.md:12`, `arquitectura.md`, `CLAUDE.md` | **CANÓNICO indexable** (fuente de verdad del RAG) |
| `documentos/no_indexar/**` | `ingest.py` (excluido), `course_documents.py:319` (destino de borrado durable) | — | material fuente NO indexado (dossiers, guías gestor) |
| `documentos/oficial/{guiones,ejes}` | `ingest.py` (ejes en EXCLUDED; guiones fuera de ALLOWED) | `migrate_corpus_ejes_to_secciones.py` | guiones/ejes viejos, **no indexados** |
| `corpus/` (raíz) | **NINGUNO** | `PLAN_INGESTA_CORPUS.md` (paso 6-7, como *fuente de autoría*), `INGESTA_SECCION_0_REPORTE.md:5` | **fuente de AUTORÍA** de la Sección 0 (no ingest-ready) |

## Diferencia de esquema de frontmatter (por qué `corpus/` NO es ingest-ready)

`corpus/…/01_contenido_canonico.md` (autoría, humano):
```yaml
course_title, section_number: 0, section_title, lesson_number, lesson_title,
source_type, recommended_scope, visible_to_student, allowed_for_indexing, status
```
**Falta** `course_id`, `moodle_section_id`, `section_id`, `scope`, `source`, `section_slug`.

`documentos/oficial/curso_2/seccion_01_…/contenido_canonico.md` (ingest-ready, sistema):
```yaml
course_id: "2", moodle_section_id: "2", section_id: "2", section_number: "1",
section_slug, section_title, resource_type, content_type, layer, scope: "section",
source: "canonical_md", source_origin: "course", status: "ready_for_indexing",
visible_to_student, allowed_for_indexing, version, legacy_axis
```

`PLAN_INGESTA_CORPUS.md` (pasos 6-7) documenta que el corpus de autoría se transforma a un **"árbol server-ready" con frontmatter de sistema** (inyectando `moodle_section_id`, `scope`, etc.) mediante un driver `ingest_seccionN.py` **antes** de colocarse en `documentos/oficial/curso_2/`. Ese driver corrió en el servidor y **no está versionado en este repo**.

## `axis_id` / `scope=axis` en corpus activo
- `corpus/`: **0 ocurrencias** (limpio).
- `documentos/oficial/**` (indexable): **0 ocurrencias**.
- Únicas ocurrencias de `axis_id`: `documentos/no_indexar/desde_gestor/*` (datos de prueba del gestor, **carpeta excluida de la ingesta**). No contaminan el RAG.
