# Plantillas de entrega

Dos plantillas: **informe de hallazgos** (cierre de una auditoría) y **plan de
implementación / entrega** (cuando se corrige algo). Úsalas tal cual; rellena con
datos reales (archivos, líneas, resultados del endpoint, salida de pytest). No
inventes números: si no ejecutaste algo, dilo.

---

## Plantilla A — Informe de hallazgos (auditoría)

```markdown
# Auditoría del tutor — <ámbito: p. ej. "tutor dentro de lección N">
Fecha: <YYYY-MM-DD> · Curso: <course_id> · Lección(es): <ids>

## 1. Resumen ejecutivo
<3-6 líneas: qué se auditó, el patrón estructural dominante, lo más grave.>

## 2. Flujo real trazado
<interfaz → payload → endpoint → contexto → políticas → routing → retrieval →
generación → validación → respuesta, con archivo:línea en cada salto y qué datos
están disponibles vs ausentes.>

## 3. Metadata inspeccionada
- Lección COMPLETA <id>: campos poblados / leídos / muertos.
- Lección INCOMPLETA <id>: campos poblados / leídos / muertos.

## 4. Contexto renderizado (literal)
<pega el bloque exacto que recibió el modelo en ≥1 caso; señala doble inyección o
mezcla de fuentes si la hay.>

## 5. Resultados del endpoint real
| Escenario | Ruta | Intent | evidence_level | blocked_by | ¿Correcto? |
|---|---|---|---|---|---|
| <con timestamp> | | | | | |
| <sin timestamp> | | | | | |
| <suggested_prompt> | | | | | |
| <tema delegado> | | | | | |
| <fuera de dominio> | | | | | |

## 6. Hallazgos por severidad
### Crítico
- **[C1] <título>** — Causa raíz: <archivo:función:línea> · Regla violada:
  <concepts.md §8 #n> · Síntoma observable: <…> · Fix mínimo propuesto: <…>
### Alto
- **[A1] …**
### Medio
- **[M1] …**
### Menor
- **[m1] …**

## 7. Arreglo arquitectónico recomendado
<el fix correcto y mínimo, normalmente "pasar la política pedagógica al punto de
decisión X" o "derivar el vocabulario del gate de `concepts`". Incluye stopgap
provisional si aplica, marcado como tal.>

## 8. Riesgos y próximos pasos
- ¿Requiere reindex (destructivo)? <sí/no>
- Deuda en otras capas: <…>
- Próximo paso recomendado: <…>
```

### Reglas de calidad del informe
- Cada hallazgo lleva **archivo:función:línea**, **regla violada** y **síntoma
  observable** (no "parece que").
- Severidad según la rúbrica de [audit-workflow.md](audit-workflow.md).
- Distingue lo verificado (con evidencia) de lo sospechado (a confirmar).

---

## Plantilla B — Plan de implementación / entrega

Úsala para **proponer** un cambio antes de codificar y, con los resultados
rellenados, como **resumen de entrega** después.

```markdown
# Plan de implementación — <hallazgo(s) que corrige: C1, A2, …>

## Objetivo
<qué propiedad del sistema se restablece, en términos de la regla de diseño.>

## Cambios propuestos
| # | Archivo:función | Qué cambia | Regla restaurada | Riesgo |
|---|---|---|---|---|
| 1 | | | | |

## Por qué este y no un parche
<por qué es el arreglo mínimo correcto y no una excepción puntual sobre el ejemplo
(FL Studio, etc.).>

## Observabilidad añadida
<blocked_by / retrieval_scope / applied_policies nuevos o ajustados.>

## Pruebas
| Caso (de testing.md) | Tipo (e2e/unit) | Falla sin fix | Pasa con fix |
|---|---|---|---|
| | | | |

## Regresión
- Comando: `cd tesis-rag && python -m pytest tests/ -q`
- Resultado REAL: <pegar resumen; incluir fallos si los hubo>
- Endpoint real (probe_tutor): <escenarios probados y resultado>

## Pendientes / riesgos
- ¿Reindex requerido? <sí/no — recordar que es destructivo y lo ejecuta el
  usuario>
- Stopgap vs definitivo: <…>
- Deuda restante: <…>

## Próximos pasos
- <…>
```

### Reglas de calidad de la entrega
- Reporta resultados **reales** de pruebas (incluye fallos; no afirmes "todo
  verde" sin la salida).
- Si algo quedó fuera de alcance o sin verificar, decláralo explícitamente.
- No marques como "hecho" lo que requiere un reindex que aún no se corrió.
