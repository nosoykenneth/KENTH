# Validación post-limpieza (FASE 7-8)

Fecha: 2026-07-05 · Rama: `chore/corpus-canonical-cleanup`

## Invariantes de corpus (FASE 7)
| # | Chequeo | Esperado | Resultado |
|---|---|---|---|
| V1 | `axis_id` / `scope=axis` / `eje_id` en corpus activo indexable (`documentos/oficial/curso_2`) | 0 | **0 ✅** |
| V2 | Carpeta `seccion_01_el_sistema_de_decision/` (vieja Sección 0) | ausente | **ausente ✅** (quedan seccion_00 + seccion_02..08) |
| V3 | Archivos `.md` anclando `moodle_section_id:"2"` fuera de `seccion_00_sistema_decision` | 0 | **0 ✅** (no hay dos versiones activas de Sección 0) |
| V4 | `corpus/` (raíz) + `corpus_seccion_00.zip` + `00_QA_CORPUS_SECCION_0.md` (raíz) | ausentes | **ausentes ✅** |
| V5 | Fuente canónica de ingesta única = `tesis-rag/documentos/` | sí | **sí ✅** (ningún código lee otra ruta) |

## Gate real de ingesta sobre `seccion_00_sistema_decision` (FASE 7)
`ingest.es_documento_aprobado_para_indexar` sobre los 80 archivos promovidos:
- **Indexables: 22** (18 lección [0.1→SEC2-R55, 0.2→SEC2-R56] + 4 sección). Coincide exactamente con la ingesta del servidor.
- **Excluidos/retenidos: 58** (10 EXCLUDE + 45 HOLD + 3 companions).
- **Falsos positivos (indexa lo prohibido): 0** · **Falsos negativos (no indexa lo aprobado): 0**.
- EVAL/QA/manifest/recursos_externos aprobados: **0** · Lecciones HOLD 0.3–0.7 aprobadas: **0**.
- Cuerpos markdown byte-idénticos a la fuente: **77/77** (sólo se reescribió frontmatter).

## Tests locales (FASE 8) — sin reindex, sin servidor
| Suite | Resultado |
|---|---|
| `pytest tests/` (backend) | **~202 passed, 1 skipped, 0 failed** |
| `test_domain_pack_phase0` (gate byte-idéntico) | **passed** (no se rompió la baseline; taxonomía intacta) |
| `test_ingest_public_policy`, `test_source_policy`, `test_ingest_flag_normalization`, `test_rag_secciones` | **passed** |
| `npm run lint` | **0 errores** (5 warnings preexistentes de exhaustive-deps) |
| `test:moodle-section` / `test:chat-sources` / `test:professor-view` | **OK / OK / OK** |
| `npm run build` | **✓ built** |

## No validado localmente (por diseño)
- **Reindex Chroma**: prohibido en este encargo. El efecto real en el índice se validará en el flujo de `PLAN_INGESTA_CORPUS.md` (add_single_document acotado + pruebas de chat). El gate determinista de arriba es la garantía local de que *qué* se indexaría es correcto.
- **Servidor**: no tocado. Existe drift esperado (el server ya tenía `seccion_00_sistema_decision` con 22 archivos; ahora el repo local también, más las 0.3–0.7 retenidas).
