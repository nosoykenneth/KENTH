# Rúbrica de validación del tutor — TIC KENTH

Rúbrica analítica para que un evaluador experto (docente/tutor de tesis) valore la
calidad de las respuestas del tutor. Complementa las métricas automáticas de
`evaluacion_tutor.md` con un juicio pedagógico.

**Escala por criterio:** 0 = deficiente · 1 = insuficiente · 2 = aceptable ·
3 = bueno · 4 = excelente. Se aplica **por respuesta** (o por muestra de respuestas).

---

## Criterios

### 1. Precisión técnica
| Nivel | Descriptor |
|---|---|
| 4 | Técnicamente correcta y completa; terminología de mezcla/masterización exacta. |
| 3 | Correcta con omisiones menores. |
| 2 | Correcta en lo esencial pero con imprecisiones. |
| 1 | Errores técnicos que confundirían al estudiante. |
| 0 | Incorrecta o engañosa. |

### 2. Alineación con la lección
| Nivel | Descriptor |
|---|---|
| 4 | Totalmente pertinente a la lección/sección/momento activo. |
| 3 | Pertinente, con leve desvío de foco. |
| 2 | Relacionada pero genérica (no usa el contexto de actividad). |
| 1 | Poco relacionada con la lección. |
| 0 | Ajena a la lección o responde otra cosa. |

### 3. Evidencia / grounding
| Nivel | Descriptor |
|---|---|
| 4 | Claramente fundamentada en el corpus; `fuentes`/`retrieval_scope` coherentes. |
| 3 | Fundamentada, con atribución algo débil. |
| 2 | Plausible pero con grounding pobre. |
| 1 | Sin evidencia clara; “de memoria”. |
| 0 | Cita/fuente inventada. |

### 4. Claridad
| Nivel | Descriptor |
|---|---|
| 4 | Clara, bien estructurada, en español, al nivel del estudiante. |
| 3 | Clara con algún exceso de tecnicismo. |
| 2 | Comprensible con esfuerzo. |
| 1 | Confusa o desordenada. |
| 0 | Incomprensible. |

### 5. Pedagogía
| Nivel | Descriptor |
|---|---|
| 4 | Guía el aprendizaje (no solo responde): ejemplifica, conecta, invita a seguir. |
| 3 | Buena orientación pedagógica. |
| 2 | Responde sin acompañar. |
| 1 | Respuesta seca o desincentivadora. |
| 0 | Inapropiada pedagógicamente. |

### 6. Control de alucinación
| Nivel | Descriptor |
|---|---|
| 4 | Reconoce límites; rehúsa cuando no hay evidencia; no inventa. |
| 3 | Prudente, con matices honestos. |
| 2 | Alguna afirmación no respaldada, sin consecuencia grave. |
| 1 | Afirmaciones no respaldadas relevantes. |
| 0 | Alucinación clara (contenido/cita/lugar inventado). |

### 7. Utilidad
| Nivel | Descriptor |
|---|---|
| 4 | Resuelve la necesidad del estudiante y aporta valor añadido. |
| 3 | Resuelve la necesidad. |
| 2 | Ayuda parcialmente. |
| 1 | Poco útil. |
| 0 | No útil. |

---

## Hoja de puntuación (por respuesta)

| trace_id | Precisión | Alineación | Grounding | Claridad | Pedagogía | Anti-alucinación | Utilidad | Total /28 |
|---|---|---|---|---|---|---|---|---|
| `<trace_id>` | — | — | — | — | — | — | — | — |

**Interpretación del total (28 máx):**
- 24–28 — Excelente (listo para piloto/producción del dominio evaluado).
- 18–23 — Bueno (aceptable con mejoras puntuales).
- 12–17 — Insuficiente (requiere ajuste de corpus/prompt/verificación).
- < 12 — Deficiente (no apto).

> **Peso crítico:** cualquier respuesta con **Anti-alucinación = 0** o
> **Grounding = 0** se marca como *fallo grave* aunque el total sea alto: el tutor no
> debe inventar. Reportar estos casos por separado.

---

## Procedimiento

1. Muestra representativa (≥ 20 respuestas) de distintas lecciones y tipos.
2. Dos evaluadores independientes puntúan; medir concordancia (p. ej. κ de Cohen).
3. Promediar por criterio y por lección.
4. Cruzar con métricas objetivas (`evaluacion_tutor.md`) y percepción (`encuesta_likert.md`).
5. Redactar conclusiones ligadas a los objetivos específicos de la tesis.
