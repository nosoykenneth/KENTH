# Reporte de ingesta — Corpus Sección 0 "El sistema de decisión"

- **Fecha (local):** 2026-07-04 · **Servidor (UTC):** 2026-07-05T03:3x
- **Commit local:** `1df18e3` · **Commit servidor:** `1df18e3` (rama `main`, sin drift antes de la operación)
- **Corpus (autoría, consolidado 2026-07-05):** originalmente `corpus\seccion_00_sistema_decision` (raíz); **consolidado** al árbol canónico `tesis-rag/documentos/oficial/curso_2/seccion_00_sistema_decision` con frontmatter de sistema (ver `reports/cleanup_corpus_20260705_080723`). La carpeta `corpus/` de la raíz fue eliminada.
- **Curso:** Mezcla y Masterización · `course_id=2`
- **Sección destino real:** `moodle_section_id=2` · **`section_number=1`** · `section_title="SECCIÓN 0: El sistema de decisión"` · slug `el_sistema_de_decision`
- **Batch:** `seccion0_20260704` · **corpus_version:** `seccion_0_v1`
- **Evidencia servidor:** `/srv/kenneth/tic-kenth/reports/ingesta_seccion_0_20260705_033332/`

## Veredicto

- ✅ **LISTO para revisión docente** de las lecciones **0.1** y **0.2** y del **nivel-sección** (overview, glosario, mapa conceptual, atribuciones): indexadas, con grounding verificado por chat.
- ⚠️ **PARCIAL para evaluación RAG de la sección completa:** solo **2 de 7** lecciones del corpus tienen lección real en el sistema. Las lecciones **0.3, 0.4, 0.5, 0.6, 0.7** quedaron **retenidas** (`pending_lesson_mapping`), NO indexadas.
- ❌ **NO listo como "Sección 0 completa"** hasta que se creen en el sistema las lecciones faltantes (o se autorice indexarlas a scope sección).

Se cumplió la Definition of Done para el alcance autorizado (opción **Estricto: solo mapeadas**).

## Auditoría del corpus (FASE 1–2)

- **77 archivos Markdown** auditados (7 nivel-sección + 7 lecciones × 10). 0 vacíos, 0 YAML inválido, UTF-8 correcto, sin secretos/tokens, sin URLs http(s) (los "recursos externos" solo referencian sitios oficiales, sin enlaces inventados). Los "placeholders/TODO" detectados eran la palabra española *todo/toda*, no marcadores.
- **99 correcciones de frontmatter/flags** (contenido académico intacto):
  - `00_QA_CORPUS_SECCION_0.md`: `source_type resource_manifest → qa_report`; `status → excluded_operational` (vis/idx `false`).
  - `00_recursos_externos_sugeridos.md`: `allowed_for_indexing true → false`; `status → needs_human_approval` (visible al alumno se mantiene; no hay enlaces dudosos).
  - `10_prompt_evaluacion.md` (×7): `false/false`, `status → excluded_evaluation`.
  - `00_manifest_indexacion_seccion.md`: `false/false`, `status → excluded_operational`.
  - `02_guia_tutor_ia.md` (×7): `internal_context: true` (vis `false`, idx `true`).
  - `internal_context: true` añadido a **20** archivos indexados-pero-no-visibles (guías del tutor, momentos, atribuciones internas).
  - Resto de indexables: `status → approved_for_ingestion`.
- Resultado: **67 indexables / 10 excluidos** (lado-corpus); todos los invariantes de gate pasan.
- Respaldo del corpus pre-corrección: `scratchpad/corpus_backup_pre_fase2/` (77 archivos).

## Mapeo lección corpus → sistema (FASE 6)

| Lección corpus | lesson_id real | Título en sistema | Confianza | Acción |
|---|---|---|---|---|
| 0.1 Mezclar es decidir | **SEC2-R55** | "1 — Mezclar es decidir: el ciclo de trabajo" | Fuerte (exacto) | Indexada (lesson) |
| 0.2 Tu oído miente | **SEC2-R56** | "Lección 2 — Tu oído miente…" | Fuerte (exacto) | Indexada (lesson) |
| 0.5 Gain Staging | — (SEC2-R57?) | "3 — Volumen y Gain" | Débil/ambiguo | **No mapeada** (decisión del operador) |
| 0.3 Monitores | — | *(no existe)* | — | Retenida `pending_lesson_mapping` |
| 0.4 Ruteo | — | *(no existe)* | — | Retenida `pending_lesson_mapping` |
| 0.6 Nativos vs emul. | — | *(no existe)* | — | Retenida `pending_lesson_mapping` |
| 0.7 Checklist | — | *(no existe)* | — | Retenida `pending_lesson_mapping` |

- El curso 2 tiene **solo 3 lecciones** registradas, todas bajo `moodle_section_id=2`: SEC2-R55, SEC2-R56, SEC2-R57.
- **SEC2-R57 "Volumen y Gain"** quedó sin contenido de corpus (match débil con 0.5; por posición sería 0.3) → marcado `needs_human_confirmation`. No se inventó `lesson_id`.

## Archivos indexados (FASE 8) — 22 archivos → 72 chunks

- **Nivel sección (4, scope=section, sin lesson_id):** `00_seccion_overview.md`, `00_glosario_seccion.md`, `00_mapa_conceptual_seccion.md`, `00_atribuciones_seccion.md` (esta última `visible_to_student=false`, `internal_context=true`).
- **Lección 0.1 → SEC2-R55 (9, scope=lesson):** `01_contenido_canonico`, `02_guia_tutor_ia` (interno), `03_momentos_clase` (interno), `04_glosario`, `05_preguntas_frecuentes`, `06_actividad_practica`, `07_rubrica_actividad`, `08_recursos_manifest`, `09_atribuciones` (interno).
- **Lección 0.2 → SEC2-R56 (9, scope=lesson):** ídem 01–09.
- Método: `add_single_document()` **acotado por archivo** (incremental, delete-then-add por `source_path`), ejecutado vía `docker exec` con el driver `ingest_seccion0.py` (dry-run + `--commit`). **No** se usó `/documents/rebuild` global (habría reindexado también las secciones 1–8) ni ningún borrado destructivo.

### Archivos NO enviados al índice
- **Excluidos (10):** 7×`10_prompt_evaluacion.md`, `00_QA_CORPUS_SECCION_0.md`, `00_manifest_indexacion_seccion.md`, `00_recursos_externos_sugeridos.md`. **No** se colocaron en el árbol de ingesta del servidor (defensa en profundidad).
- **Retenidos (45):** todas las lecciones 0.3–0.7 (`pending_lesson_mapping`). Presentes solo en el corpus fuente local, **fuera** de `documentos/oficial/curso_2/`.

## Estado del índice (FASE 5/7/10)

| Métrica | Pre-index | Post-index |
|---|---:|---:|
| Total chunks | **25** | **97** |
| `canonical_md` | 0 | 72 |
| `transcript` | 24 | 24 |
| `resource_file` | 1 | 1 |
| SEC2-R55 (lección 0.1) | 8 | 38 |
| SEC2-R56 (lección 0.2) | 7 | 37 |
| SEC2-R57 | 9 | 9 (intacto) |
| scope=section | 0 | 13 |

### Validadores de gate (post-index) — todos ✅
- EVAL/QA/operativos indexados: **0**.
- Canónicos de **otras** secciones (1–8) indexados por esta operación: **0**.
- Lecciones retenidas 0.3–0.7 indexadas: **0**.
- Archivos `seccion_00` únicos en el índice: **22**.
- Todos los chunks nuevos con `course_id=2`, `moodle_section_id=2`, `section_number=1`.

## Pruebas de chat con token estudiante (FASE 10)

Token del usuario `userid=37` (rol student, servicio `api_tesis`). Gateway `http://localhost:8090/api/ai/chat`.

| # | Tipo | Pregunta | scope / intent | Fuentes | trace_id | Veredicto |
|---|---|---|---|---|---|---|
| T1 | 0.1 | 5 pasos del ciclo | lesson / aclaracion_concepto | 18 (canónico nuevo) | `742959fc…` | ✅ grounded |
| T2 | 0.1 | "mezclar es decidir" | lesson | 18 | `acff86c5…` | ✅ grounded |
| T3 | 0.2 | oído se engaña / fatiga | lesson | 22 | `745625ad…` | ✅ grounded |
| T4 | 0.2 | volumen de escucha | lesson (+section) | 23 | `7cf7e584…` | ✅ grounded |
| T5 | fuera de dominio | micrófono para grabar | out_of_domain / `blocked_by=out_of_domain:semantic` | 0 | `929abf79…` | ✅ rechazo correcto |
| T6 | ambigua | ¿cuántos plugins? | lesson (intervención mínima) | 20 | `60c7c0c6…` | ✅ grounded |
| T7 | guía interna | ¿está bien mi decisión? | lesson; usa verificación **sin** exponer guía; `vis_false=0` en fuentes | 17 | `ac91ce42…` | ✅ correcto |
| Smoke | post-recreate | gain staging (1 frase) | lesson | 25 | `2c7417d3…` | ✅ grounded |

- La lección **0.5 NO se probó** por diseño (retenida, no indexada). Sustituida por la batería anterior.

## Backup y rollback (FASE 7 / DoD)

- **Backup Chroma:** `reports/ingesta_seccion_0_20260705_033332/chroma_backup/` (14M) + `pre_index_state.json` (25 chunks, 4 fuentes) + `commands.log` + `server_commit.txt`.
- **No se modificaron tablas de BD** (`mdl_local_tesisai_*`): la ingesta es solo filesystem → Chroma. Rollback totalmente reversible.
- **Rollback disponible:**
  1. Fino: borrar del índice los 22 `source_path` bajo `documentos/oficial/curso_2/seccion_00_sistema_decision/` (`remove_single_document`), o borrar por `where source_path startswith`.
  2. Completo: restaurar `runtime/chroma` desde `chroma_backup` (volver a 25 chunks).
  3. Filesystem: eliminar `tesis-rag/documentos/oficial/curso_2/seccion_00_sistema_decision/` y rebuild de la imagen.

## Durabilidad (FASE 9)

- Archivos copiados al **host-repo** (`tesis-rag/documentos/oficial/curso_2/seccion_00_sistema_decision/`, 22) y **horneados** en la imagen `tic-kenth/fastapi:latest` (rebuild + recreate). Health post-recreate `status:ok`, `chroma_chunks=97` (Chroma persiste en volumen). Sin drift imagen↔índice.

## Problemas / hallazgos

1. **Numeración 0 vs 1:** el corpus rotula "Sección 0", pero en Moodle esa sección es `section_number=1` / `moodle_section_id=2` (Moodle reserva la 0 para el área general). Los chunks se etiquetaron con la identidad del sistema (`1`/`2`) para que el retrieval haga match; el rótulo humano "SECCIÓN 0" se conserva en `section_title`.
2. **5 de 7 lecciones no existen** en el sistema → retenidas. Requiere crear las lecciones o autorizar scope-sección.
3. **SEC2-R57 "Volumen y Gain"** sin contrapartida clara → sin mapear.
4. **Bug menor de la política de ingesta** (`ingest.py`): `allowed_flag is False` no atrapa el string `"false"` del frontmatter markdown (solo el bool de JSON). Mitigado NO colocando archivos excluidos en el árbol de ingesta. **Recomendación:** normalizar con `_as_bool(...) is False`.
5. **Frontend — fuga potencial:** el array `fuentes` de `/chat` incluye chunks `visible_to_student=false` (guías internas usadas como conocimiento). La respuesta no los cita, pero el frontend debería filtrar `fuentes` por `visible_to_student` para el alumno (igual que ya filtra imágenes/recursos). Recomendación, no bloqueante.

## Próximos pasos sugeridos

- Crear en el sistema las lecciones 0.3, 0.4, 0.6, 0.7 (y aclarar SEC2-R57 ↔ 0.5); luego re-ejecutar la ingesta acotada para esas lecciones (el corpus y los manifiestos ya están listos).
- Aplicar el fix del gate `allowed_for_indexing` y el filtro de `fuentes` en el frontend.
