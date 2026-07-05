# Reporte de ingesta — Sección 0 lecciones 0.3–0.7 (completar la sección)

- **Fecha (local):** 2026-07-05 · **Servidor:** bodyguard26 (`100.97.90.86`) · commit `8042271`
- **Curso:** Mezcla y Masterización `course_id=2` · **Sección:** `moodle_section_id=2` / `section_number=1` / "SECCIÓN 0: El sistema de decisión"
- **Backup:** `/srv/kenneth/tic-kenth/reports/ingesta_seccion0_lessons_20260705_145139/` (chroma_backup 14M + pre_index_state.json + server_commit.txt)

## Contexto
La ingesta de julio dejó indexadas solo las lecciones 0.1 y 0.2 + nivel-sección (22 archivos → 72 chunks canónicos); las 0.3–0.7 quedaron **retenidas** porque sus lecciones no existían en la plataforma. Ahora el profesor creó las 7 lecciones (H5P) en Moodle → se completa la sección.

## Mapeo verificado (fuente: nombres reales H5P `mdl_hvp`, secuencia sección `55..61`)
La tabla `mdl_local_tesisai_lessons.title` estaba **desactualizada** (R57="Volumen y Gain", R59="Nativos"); NO se usó. Mapeo autoritativo por cmid:

| Corpus | Lección real (H5P) | lesson_id (cmid) |
|---|---|---|
| 0.3 Monitores y auriculares | L3 Monitores y auriculares | SEC2-R57 |
| 0.4 Anatomía/ruteo | L4 Anatomía universal del mixer: ruteo | SEC2-R58 |
| 0.5 Gain Staging | L5 Gain Staging | SEC2-R59 |
| 0.6 Nativos vs emulaciones | L6 Nativos vs emulaciones | SEC2-R60 |
| 0.7 Checklist | L7 Checklist de sesión lista | SEC2-R61 |

## Operación
1. Manifest actualizado con el mapeo; re-promoción local (`scripts/promote_seccion_corpus.py`) → 0.3–0.7 pasan a `allowed_for_indexing:true`, `scope:lesson`, `lesson_id` resuelto. Gate local: **67 indexables, 0 fugas**.
2. Sincronizados **45 archivos indexables** (9 × 5 lecciones; sin prompts de evaluación) → host repo + `docker cp` al contenedor (acotado; NO se tocaron 0.1/0.2/sección).
3. Backup de Chroma + pre_index_state (97 chunks).
4. Dry-run gate en contenedor: **45/45 aprobados, 0 rechazados**.
5. Ingesta acotada `add_single_document` × 45 → **136 chunks nuevos, 0 fallos**.

## Resultado (post-index)
| Métrica | Pre | Post |
|---|---:|---:|
| Chroma total | 97 | **233** |
| canonical_md | 72 | **208** |
| transcript | 24 | 24 |
| resource_file | 1 | 1 |

- **canonical_md por lección:** R55=30, R56=29, **R57=27, R58=27, R59=27, R60=27, R61=28** (las 7 lecciones con corpus).
- **Fugas eval/QA/manifest/recursos: 0.** 59 chunks `visible_to_student=false` (guías internas; el frontend los filtra de las fuentes del alumno).
- Health post-index: `status:ok`, `chroma_chunks=233`.

## Pruebas de chat (token estudiante userid=37, gateway :8090)
| Pregunta | Lección | Fuentes | trace | Veredicto |
|---|---|---|---|---|
| ¿Qué es el gain staging…? | 0.5 / SEC2-R59 | 4 | `ac407c29…` | ✅ grounded (definición + headroom) |
| ¿Cómo trabajo con monitores no ideales? | 0.3 / SEC2-R57 | 20 | `c845ea59…` | ✅ grounded (momentos + FAQ: "conocer tu sistema") |

## Durabilidad y rollback
- **Índice durable:** Chroma es bind-mount `runtime/chroma` → persiste entre recreaciones.
- **Rollback fino:** `remove_single_document(source_path)` de los 45 nuevos, o restaurar `chroma_backup`.
- **Pendiente durabilidad de archivos:** los 45 .md están en el contenedor (docker cp) y en el host repo (untracked), pero NO horneados en la imagen (`8042271`). Un rebuild los baked-in (evita perderlos si se recrea el contenedor / se hace un reindex full).

## Follow-ups (no incluidos en esta ingesta)
1. **Rebuild imagen fastapi** para hornear los 45 archivos (durabilidad ante recreate/reindex).
2. **Reconciliar servidor con el repo limpio:** el server sigue en `8042271` (sin el merge de limpieza) y conserva `seccion_01_el_sistema_de_decision/` (vieja Sección 0, NO indexada) → un reindex full la duplicaría. Empujar `main` + `git pull` en el server + quitar seccion_01.
3. **Bug de sync del plugin:** `mdl_local_tesisai_lessons.title` desactualizado para R57/R59 (no afecta al RAG; sí a la UI/contexto si usa ese título).
