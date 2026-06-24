# Workflow de auditoría

Procedimiento obligatorio cuando se pide analizar/auditar el tutor (o cuando un
fix requiere entender primero). El objetivo no es "leer código y opinar": es
**trazar el flujo real, observar el contexto que recibe el modelo, probar el
endpoint y producir hallazgos accionables con causa raíz**. No modifiques código
en esta fase; primero propones, el usuario aprueba.

## Principios
- **Verifica, no asumas.** El [mapa de arquitectura](architecture-map.md) puede
  estar desfasado. Confirma cada afirmación con Grep/Read sobre el código actual.
- **Sigue los datos, no el prompt.** El bug suele estar en *quién decide antes de
  hidratar*, no en el texto del prompt.
- **Una lección completa y una incompleta.** Casi todos los defectos (herencia
  silenciosa, campos muertos, gates) solo se ven contrastando ambas.
- **Reproduce en el endpoint real.** Tests unitarios sobre funciones aisladas no
  capturan el flujo de routing→retrieval→verificación.

## Las 14 fases

### Fase 1 — Instrucciones del repo
Lee `CLAUDE.md`, `docs/arquitectura.md` y notas relevantes. Anota el contrato SOA,
los dos prefijos (`/api/ai`, `/api/lms`) y las gotchas (reindex destructivo,
`.pyc` trackeados, identidad de lección por `cmid`, migración ejes→secciones).

### Fase 2 — Localizar las piezas
Ubica frontend, backend, servicios de contexto, routing, retrieval, prompts,
modelos de datos y tests. Usa Glob/Grep; no confíes en rutas de memoria. Salida:
una lista de archivos:función con su rol en el flujo.

### Fase 3 — Trazar el flujo completo
Reconstruye, con números de línea reales:
`interfaz → payload → endpoint → resolución de contexto → políticas → routing →
retrieval → generación → validación → respuesta`.
Para cada salto anota **qué datos están disponibles** y **cuáles no**. El hallazgo
estructural más común aparece aquí: una decisión que se toma cuando aún no está
hidratado el contexto pedagógico.

### Fase 4 — Cazar hardcodes y gates tempranos
Busca:
- decisiones tomadas **antes** de hidratar lección/bloque/política;
- compuertas que dependen de keywords/títulos en vez de `concepts`/delegación;
- vocabulario de dominio cableado en la lógica (nombres de curso, DAWs, listas
  paralelas a `concepts`);
- LLM pequeño decidiendo gates críticos solo.
Comandos útiles: Grep de los nombres de gate (`_es_estudiante_perdido`,
`_parece_consulta_del_dominio_curso`, `unsupported_terms`, `domain_hint_terms`),
y `scripts/scan_metadata_usage.py` para campos muertos.

### Fase 5 — Inspeccionar metadata real
Toma **una lección completa** y **una incompleta** (sin metadata o sin
transcripción). Muestra sus campos reales (DB o JSON). Contrasta contra el
[contrato de metadata](metadata-contract.md): ¿qué campos están poblados, cuáles
se leen, cuáles quedan muertos?

### Fase 6 — Renderizar el contexto exacto
Obtén el **texto literal** que recibe el modelo para un turno (el bloque de
`render_context_block` + lo que arma el nodo de generación). Dos vías:
- ejecutar/loggear `build_envelope` + `render_context_block` para una entrada de
  ejemplo (hay scripts en `tesis-rag/scratch/inspect_context.py` y similares —
  verifica), o
- añadir un log temporal del prompt final (revertir luego).
Verifica con tus ojos: ¿hay doble inyección? ¿se mezcla runtime con evidencia?
¿faltan campos que sí están en la metadata?

### Fase 7 — Probar el endpoint real
Usa `scripts/probe_tutor.py` (o curl) contra `/chat`. Construye payloads para los
escenarios de [testing.md](testing.md): con/sin timestamp, lección completa/
incompleta, suggested_prompt, tema delegado, pregunta fuera de dominio, etc.
Captura los campos de diagnóstico (`ruta`/`selected_route`, `intent`,
`evidence_level`, `warnings`, `runtime_context`, `source_policy`). Levanta el
backend si hace falta (`cd tesis-rag && python main.py`).

### Fase 8 — Clasificar por severidad
Asigna a cada hallazgo: **crítico / alto / medio / menor** (ver rúbrica abajo).

### Fase 9 — Causa raíz
Para cada hallazgo: archivo, función, línea, y **por qué** ocurre en términos de
la jerarquía/regla violada (cita la regla de [concepts.md](concepts.md) §8). No
te quedes en el síntoma.

### Fase 10 — Proponer el arreglo arquitectónico mínimo
Primero el fix *correcto y mínimo* (normalmente: pasar la política pedagógica al
punto de decisión, o derivar el vocabulario del gate de `concepts`), no un parche
puntual sobre el ejemplo. Si hay un stopgap barato, ofrécelo como alternativa
explícitamente marcada como provisional.

### Fase 11 — (Solo si lo piden) Implementar
Pasa a [implementation-workflow.md](implementation-workflow.md). Si no lo piden,
detente en la propuesta.

### Fase 12 — Pruebas
Crea/actualiza las pruebas afectadas (ver [testing.md](testing.md)). Toda
corrección lleva su prueba de regresión.

### Fase 13 — Regresiones
Corre la suite (`cd tesis-rag && python -m pytest tests/ -q`) y las pruebas e2e
nuevas. Reporta el resultado real (incluye fallos).

### Fase 14 — Entrega
Resume con la [plantilla de informe](templates.md): hallazgos por severidad,
causa raíz, fixes propuestos/aplicados, riesgos pendientes y próximos pasos.

## Rúbrica de severidad

- **Crítico** — produce respuestas incorrectas o inseguras de forma sistemática, o
  rompe la integridad académica. Ej.: una lección vacía responde con el contenido
  de otra; el tutor rechaza sistemáticamente lo que el profe delegó; una
  restricción de atribución no se cumple.
- **Alto** — degrada la calidad pedagógica de forma frecuente o rompe un modo.
  Ej.: preguntas normales clasificadas como "perdido"; gate de dominio que
  depende del título; sin timestamp el tutor se degrada.
- **Medio** — defecto real pero acotado o con workaround. Ej.: doble inyección de
  objetivo/acción; falta `blocked_by`/`retrieval_scope` en trazas.
- **Menor** — higiene/observabilidad/legibilidad sin impacto directo en
  respuestas. Ej.: campo muerto sin consecuencia, log ruidoso.

## Salida obligatoria de la auditoría
- Mapa del flujo real (con archivos:líneas).
- Inventario de metadata (lección completa vs incompleta).
- Contexto renderizado literal (al menos un caso).
- Resultados del endpoint real para los escenarios clave.
- Tabla de hallazgos por severidad con causa raíz.
- Propuesta de fix mínimo arquitectónico (y stopgap si aplica).
- Usa la [plantilla de informe de hallazgos](templates.md).
