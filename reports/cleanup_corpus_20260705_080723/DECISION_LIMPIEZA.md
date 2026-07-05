# Decisión de limpieza de corpus (FASE 2-3)

Fecha: 2026-07-05 · Autor: arquitecto técnico (auditoría controlada) · Estado: **PENDIENTE DE CONFIRMACIÓN DEL DUEÑO**

## Hallazgo que invierte la premisa del encargo

El encargo asumía: «`tesis-rag/documentos` = corpus viejo/conflictivo a borrar; `corpus/` = nuevo/correcto». **La realidad, verificada contra el código y los docs, es la inversa:**

- **`tesis-rag/documentos/` es la fuente canónica VIVA que lee el pipeline** (`ingest.py`, reindex, tests). Contiene el corpus canónico por sección (`oficial/curso_2/seccion_01..08/contenido_canonico.md`, migrado de los ejes) que **el tutor usa hoy** para las secciones 1-8. Borrarlo rompería el RAG.
- **`corpus/` (raíz) es una fuente de AUTORÍA** de la Sección 0 (7 lecciones × 10 archivos). **Ningún código la lee.** Su frontmatter es "humano" (sin `moodle_section_id`/`scope`/`source`), por lo que **no es ingest-ready**: requiere un transform a "árbol server-ready" (documentado en `PLAN_INGESTA_CORPUS.md` pasos 6-7) que corrió sólo en el servidor con un driver `ingest_seccion0.py` **no versionado aquí**.

Ambas carpetas están **trackeadas en git** (corpus/ = 80 archivos; documentos = 95). No hay carpetas untracked salvo dos artefactos sueltos en la raíz.

## Duplicación real detectada

La Sección 0 ("El sistema de decisión") existe en dos representaciones:
1. `documentos/oficial/curso_2/seccion_01_el_sistema_de_decision/contenido_canonico.md` — versión vieja, 1 archivo, migrada de Eje 0 (`section_number=1`, `moodle_section_id=2`). **Es lo único que ancla la Sección 0 en el índice local.**
2. `corpus/seccion_00_sistema_decision/**` — versión nueva y detallada, 7 lecciones. **Fuente de autoría, no indexada localmente.**

En el **servidor** conviven ambas (el reporte de ingesta copió 22 archivos de la nº2 a `documentos/.../seccion_00_sistema_decision/` en el host-repo del server; esa carpeta **no está en el repo local**). El servidor no se toca en esta operación.

## Fuente canónica ELEGIDA

**`tesis-rag/documentos/` es y sigue siendo la fuente canónica de ingesta** (alineada con el código real). `corpus/` se mantiene como **fuente de autoría** explícita y documentada (no como segunda fuente de ingesta).

## Artefactos claramente eliminables (sin riesgo, en cualquier estrategia)
| Archivo | Estado | Motivo |
|---|---|---|
| `corpus_seccion_00.zip` (raíz, 127 KB) | untracked | binario pesado, empaquetado redundante de `corpus/` (hay backup externo) |
| `00_QA_CORPUS_SECCION_0.md` (raíz) | untracked | duplicado suelto (difiere de la copia en `corpus/…/00_QA_CORPUS_SECCION_0.md`); QA no indexable, no debe vivir en la raíz |

## Estrategias posibles (decisión del dueño)

### Opción A — Documentar roles + limpiar strays (RECOMENDADA, no destructiva)
- Mantener `documentos/` intacto (canónico de ingesta) y `corpus/` intacto (autoría).
- Borrar los 2 artefactos sueltos de la raíz.
- Añadir `corpus/README.md` y nota en `PLAN_INGESTA_CORPUS.md` fijando: «`corpus/` = autoría; `documentos/oficial/curso_*` = ingest-ready canónico; promoción vía árbol server-ready».
- **Sin** tocar el índice, sin migración riesgosa. Elimina la confusión por documentación + strays.
- Riesgo: nulo. Validable localmente (tests).

### Opción B — Consolidar la Sección 0 dentro de `documentos/`
- Reproducir el transform "server-ready" de `corpus/` → `documentos/oficial/curso_2/seccion_00_sistema_decision/` (inyectar `moodle_section_id=2`, `scope`, `source`, aplicar correcciones de flags, **retener** las 55 no-aprobadas).
- Borrar la raíz `corpus/`.
- **Riesgo alto:** el driver de transform no está versionado; **no se puede validar localmente** sin reindex (prohibido en este encargo). Un error contamina el RAG (prompts de evaluación/QA indexables) — justo lo que la DoD prohíbe. Además crearía relación con el drift del servidor.

## Recomendación
**Opción A.** Deja una sola fuente canónica de *ingesta* (`documentos/`), documenta `corpus/` como autoría (sin ambigüedad de "dos fuentes activas"), y no arriesga el índice ni el tutor. La Opción B debería hacerse siguiendo el procedimiento completo de `PLAN_INGESTA_CORPUS.md` (con reindex y validación de chat), no como parte de una limpieza de archivos.
