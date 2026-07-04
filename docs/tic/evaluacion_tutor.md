# Plantilla de evaluación del tutor — TIC KENTH

Instrumento para medir **precisión**, **grounding** y **no-alucinación** del tutor
(exigencia medible tipo OE4). **No** se llena aún con el corpus definitivo: aquí van
la metodología, los criterios y ejemplos genéricos con placeholders. Se completa
tras reindexar el corpus completo del curso.

> Regla de oro: la evaluación se ejecuta **por el gateway** con un token de
> estudiante real, sobre el índice desplegado, y cada respuesta se puntúa contra la
> fuente esperada. La respuesta del tutor expone `retrieval_scope`, `fuentes` y
> `trace_id` — úsalos como evidencia.

---

## 1. Batería de preguntas (plantilla)

Diseñar 20–40 ítems cubriendo: (a) conceptos por lección/sección, (b) preguntas
literales de la transcripción, (c) preguntas fuera de dominio (control negativo),
(d) preguntas ambiguas (deben pedir precisión), (e) preguntas de una lección **no**
cubierta por el corpus (deben rehusar, no inventar).

| ID | Pregunta | Tipo | Lección/Sección | Respuesta esperada (resumen) | Fuente esperada |
|---|---|---|---|---|---|
| Q-01 | `<pregunta conceptual>` | conceptual | SEC?-R?? | `<idea clave esperada>` | `<transcripción/recurso: segmento/pág.>` |
| Q-02 | `<cita literal de la transcripción>` | literal | SEC?-R?? | `<frase esperada>` | `transcript_segments[<n>]` |
| Q-03 | `¿cuál es la derivada de x²?` | fuera-de-dominio | — | **rechazo** cortés (out_of_domain) | ninguna |
| Q-04 | `¿y eso cómo se hace?` (sin antecedente) | ambigua | — | **pide precisión** | — |
| Q-05 | `<pregunta de lección sin corpus>` | cobertura | SEC?-R?? | “fuera del contexto de la lección” | ninguna (no inventar) |
| … | … | … | … | … | … |

Tipos de control obligatorios: al menos **3** fuera-de-dominio (Q-03) y **3** de
cobertura no indexada (Q-05) para medir la tasa de alucinación.

---

## 2. Criterios de calificación

### 2.1 Precisión (¿la respuesta es correcta?)
| Nivel | Definición |
|---|---|
| 2 — Correcta | Coincide con la respuesta esperada; sin errores técnicos. |
| 1 — Parcial | Correcta a medias u omite parte clave. |
| 0 — Incorrecta | Contradice la fuente o comete error técnico. |
| N/A | Ítem de control (fuera de dominio / ambigua) — se evalúa con 2.4. |

### 2.2 Grounding (¿está fundamentada en la fuente esperada?)
| Nivel | Definición |
|---|---|
| 2 — Fundamentada | Cita/usa la fuente esperada (aparece en `fuentes`); `retrieval_scope` coherente. |
| 1 — Débil | Responde bien pero con fuente distinta o `scope` inesperado. |
| 0 — Sin fundamento | No hay fuente pertinente; responde “de memoria”. |

### 2.3 No-alucinación (control negativo)
| Nivel | Definición |
|---|---|
| 2 — Correcto rechazo | Fuera de dominio → rechaza; sin corpus → “fuera del contexto”. |
| 0 — Alucinación | Inventa contenido/cita/lugar cuando no hay evidencia. |

### 2.4 Comportamiento esperado en ítems de control
- Fuera de dominio (Q-03) → `blocked_by=out_of_domain`.
- Ambigua (Q-04) → solicita precisión (no responde a ciegas).
- Cobertura no indexada (Q-05) → rehúsa sin inventar.

---

## 3. Métricas agregadas (a reportar)

| Métrica | Fórmula | Objetivo sugerido |
|---|---|---|
| Precisión media | Σ precisión / (ítems no-control × 2) | ≥ 0.80 |
| Tasa de grounding | ítems con grounding ≥ 1 / ítems no-control | ≥ 0.85 |
| **Tasa de alucinación** | alucinaciones / ítems de control | **= 0.00** (objetivo duro) |
| Tasa de rechazo correcto | rechazos correctos / ítems de control | ≥ 0.95 |
| Cobertura | lecciones con ≥1 ítem grounded / lecciones totales | 100% tras reindex |

---

## 4. Formato de resultados (una fila por ítem)

Guardar como CSV/JSONL en `tesis-rag/evaluation/reports/` (gitignored).

```jsonl
{"id":"Q-01","pregunta":"…","tipo":"conceptual","leccion":"SEC2-R55",
 "respuesta_tutor":"…","fuente_esperada":"transcript_segments[12]",
 "fuentes_devueltas":["…"],"retrieval_scope":"lesson","trace_id":"…",
 "precision":2,"grounding":2,"no_alucinacion":2,"nota":""}
```

Tabla resumen por lección:

| Lección | Ítems | Precisión media | Grounding | Alucinaciones | Veredicto |
|---|---|---|---|---|---|
| SEC?-R?? | — | — | — | — | — |

---

## 5. Procedimiento de ejecución

1. Reindexar el corpus completo del curso y validar cobertura (`validate_rag_index.py`).
2. Cargar la batería (sección 1) con respuestas/fuentes esperadas definitivas.
3. Ejecutar cada ítem por `POST /api/ai/chat` (token de estudiante, `course_id`, `lesson_id`).
4. Registrar `respuesta`, `fuentes`, `retrieval_scope`, `trace_id`.
5. Puntuar con los criterios (sección 2) — idealmente doble evaluador.
6. Agregar métricas (sección 3) y redactar el veredicto por lección.

> Este archivo es una **plantilla**: no contiene el corpus ni las respuestas
> definitivas. El script de apoyo `tesis-rag/evaluation/run_rag_eval.py` puede
> automatizar la ejecución una vez definida la batería.
