# Evaluación del tutor IA (OE4 — precisión medible)

Esta carpeta contiene el **conjunto de evaluación** del tutor y un **runner** que
calcula métricas defendibles para la tesis (Objetivo Específico 4: retroalimentación
con precisión *medible* y verificable).

## Archivos

| Archivo | Qué es |
|---|---|
| `tutor_eval_set.jsonl` | 36 casos etiquetados (12 categorías × 3). Un caso por línea (JSONL). |
| `run_tutor_eval.py` | Ejecuta los casos contra el tutor y calcula métricas. |
| `results/example_results.json` | Salida de referencia en **modo mock** (determinista, reproducible en cualquier máquina). |
| `results/example_results_real.json` | Salida de una corrida **real** contra el agente + Ollama (evidencia en vivo). |
| `results/<modo>_<timestamp>.json` | Cada corrida deja su propio JSON (ignorado por git). |

## Qué se evalúa

Cada caso declara el **comportamiento esperado** del tutor:

- `respond` — debe responder (dentro de su dominio).
- `reject` — debe **bloquear** (pregunta fuera de alcance).
- `ask_more_context` — debe **pedir aclaración** (pregunta ambigua).

Y banderas de calidad: `requires_sources`, `should_reject_out_of_scope`,
`must_not_claim_audio_analysis`, `weight` (severidad 1–3) y `evaluation_criteria`.

### Categorías (12)

`concepto_mezcla`, `concepto_masterizacion`, `flujo_senal`, `compresion`,
`ecualizacion`, `ganancia_headroom`, `fuera_de_dominio`, `ambigua`,
`sin_evidencia_suficiente`, `supuesto_analisis_audio`, `pedagogica_guia`,
`contenido_del_curso`.

### Métricas que calcula

| Métrica | Significado | Modo |
|---|---|---|
| `behavior_accuracy` | % de casos donde el comportamiento observado == esperado | mock + real |
| `behavior_accuracy_weighted` | igual, ponderada por severidad (`weight`) | mock + real |
| `correct_rejection_rate` | % de fuera-de-dominio correctamente rechazados | mock + real |
| `out_of_scope_blocked_rate` | % de casos `should_reject_out_of_scope` bloqueados | mock + real |
| `ask_more_context_accuracy` | % de ambiguas que piden aclaración | mock + real |
| `non_hallucination_rate` | % de respuestas sin nombres de DAW/plugin inventados | **real** |
| `source_usage_rate` | % de casos `requires_sources` que devuelven fuentes | **real** |
| `audio_claim_avoidance_rate` | % de casos de audio sin fingir escucha/análisis | **real** |
| `avg_latency_ms` | latencia media por respuesta | **real** |

## Cómo correr

Desde `tesis-rag/` (con el venv activado o usando su Python):

```bash
# MODO MOCK (por defecto) — sin Ollama ni Chroma.
# Usa el ROUTING DETERMINISTA REAL del agente (nodo_supervisor) para validar las
# compuertas (responder/rechazar/pedir contexto). Reproducible en cualquier máquina.
python evaluation/run_tutor_eval.py

# MODO REAL — agente completo (super_agente.invoke), igual que /chat.
# Requiere Ollama corriendo; las fuentes requieren el índice Chroma del corpus.
python evaluation/run_tutor_eval.py --mode real --course-id 2

# Guardar una copia con nombre fijo (p. ej. para la defensa):
python evaluation/run_tutor_eval.py --mode real --out evaluation/results/defensa.json
```

El runner imprime un resumen y guarda el JSON completo (con resultado por caso) en
`results/`.

## Cómo leer los modos

- **Mock**: valida la capa más crítica para la defensa (las *compuertas* de
  dominio/ambigüedad) **sin depender del entorno**. Es determinista: el mismo
  resultado en cualquier máquina. No genera texto, por eso las métricas de
  contenido salen `n/a`.
- **Real**: invoca el modelo local y el RAG. Mide además no-alucinación, uso de
  fuentes, no-afirmación de análisis de audio y latencia. Sus números dependen del
  modelo y del corpus indexado (regenerar tras un reindex).

## Notas honestas

- `source_usage_rate` en modo real depende de que el índice Chroma del corpus esté
  construido (`python scripts/reindex_rag_clean.py`). Sin corpus indexado será bajo
  aunque el tutor responda correctamente.
- Las heurísticas de no-alucinación / no-audio son **deterministas y conservadoras**
  (listas de marcadores), no un juez LLM: priorizan ser explicables y reproducibles
  para la defensa por encima de cobertura semántica total.
