# Mapa de arquitectura (wiring real del repo)

Dónde vive cada cosa **hoy** y cuál es el flujo verdadero. Esta es la parte de la
skill más acoplada al repositorio actual; trátala como **mapa que puede
desfasarse**. Antes de afirmar nada, **verifica con búsqueda** (Grep/Glob) porque
el proyecto se refactoriza (la migración ejes→secciones está en curso). Si algo
no coincide, gana el código, y conviene actualizar este archivo.

> Backend principal: `tesis-rag/`. Frontend: `frontend-tesis/`. Plugin Moodle:
> `C:\Moodle\server\moodle\local\tesisai` (esquema y Web Services). Lee también
> `CLAUDE.md` y `docs/arquitectura.md` para el contrato SOA.

## 1. Flujo real end-to-end (request del alumno)

```
React (frontend-tesis)
  → gateway /api/ai/chat            (Vite dev-proxy o nginx)
  → FastAPI POST /chat              tesis-rag/api/routes/chat.py
      · auth                        api/dependencies.py (get_current_user_id)
      · build_envelope(...)         services/context_service.py   ← hidrata Capas 2/3
      · render_context_block(...)   services/context_service.py   ← arma el bloque inyectable
      · super_agente.invoke(estado) services/agent_service.py → services/agent/graph.py
          · nodo_supervisor         services/agent/routing.py     ← ROUTING + gates (¡ojo!)
          · agente_rag / teoria     services/agent/retrieval.py   ← retrieval por curso/eje/sección
          · verificación post-gen   services/agent/verification.py
          · perdido/saludo/guardia/web según ruta
  → respuesta + trazas              services/db_service.py (mdl_local_tesisai_*)
```

Confirma el grafo y los nodos con:
`Grep "add_node|add_edge|add_conditional_edges" tesis-rag/services/agent/graph.py`.

## 2. Contrato de entrada (payload del `/chat`)

El modelo de request es `Consulta` en `tesis-rag/models/schemas.py`. **Importante
para auditorías:** no todos los campos que el contrato conceptual nombra
(`section_id`, `resource_id`, `timestamp`) son top-level. Hoy viajan **dentro de
`activity_context`**:

| Campo conceptual | Dónde llega realmente |
|---|---|
| `course_id` | top-level `consulta.course_id` (resuelto a numérico con `resolve_course_numeric`) |
| `lesson_id` | top-level `consulta.lesson_id` (también se inyecta en `activity_context.current_lesson_id`) |
| `section_id` | `activity_context.moodle_section_id` |
| `resource_id` | `activity_context.current_resource_id` |
| `timestamp` | `activity_context.current_timestamp` |
| pregunta | `consulta.pregunta` |
| historial | `consulta.historial` o dentro de `contexto_leccion` JSON |
| forzar internet | `consulta.usar_internet` |

Verifica el modelo exacto: `Read tesis-rag/models/schemas.py` (clase `Consulta`).

## 3. Modelos de contexto (Capas 2/3)

`tesis-rag/models/context.py` define las estructuras canónicas:
- `ActivityContext` — snapshot runtime (sección, lección, recurso, timestamp,
  página, `learning_goal`, `expected_action`, `interaction_mode`).
- `Lesson` — `learning_goals`, `prerequisites`, `delegated_to_tutor`,
  `attribution_constraints`, `notes` (interno, nunca se inyecta).
- `InteractionMode` (enum) — vocabulario compartido con el editor React
  (`LessonVideoEditor.jsx`); ambos listados deben ser idénticos.
- `StudentSessionState` + `BehavioralSignals` — Capa 3.
- `TutorContextEnvelope` — la unión que viaja al agente, con `active_lesson` y
  `active_block` resueltos por timestamp.

Este `TutorContextEnvelope` es el candidato natural a "contexto del alumno
canónico" de [concepts.md](concepts.md) §4.1. Audita si el **routing** realmente
lo consume (ver §5).

## 4. Dónde se LEE cada campo de metadata

Punto de partida (verifica con `scripts/scan_metadata_usage.py` y Grep):
- **Hidratación**: `services/context_service.py::hydrate_activity_context` puebla
  `learning_goal`, `expected_action`, `interaction_mode`, `current_section` desde
  el bloque/lección.
- **Inyección al prompt**: `services/context_service.py::render_context_block`
  renderiza `learning_goal(s)`, `prerequisites`, `delegated_to_tutor`,
  `proactive_message`, `suggested_prompts`, `attribution_constraints`,
  `tutor_focus`, `concepts`, `preguntas_probables`.
- **Carga desde persistencia**: `services/db_service.py` y
  `services/lesson_service.py` (DB Moodle → fallback JSON).
- **Autoría (escritura)**: `api/routes/authoring.py`.
- **Tipos**: `models/context.py`.

Lo que casi nunca lee la metadata (y debería, según la jerarquía):
`services/agent/routing.py` (ver §5).

## 5. El punto caliente: routing decide antes de hidratar la política

`tesis-rag/services/agent/routing.py::nodo_supervisor` opera **solo** sobre
`pregunta`, `contexto_leccion` (string), `imagen` y `ruta`. **No** recibe
`tutor_envelope`, `active_lesson`, `active_block`, ni la política derivada de
`delegated_to_tutor` / `concepts`. Como el supervisor corre antes que la
generación, todas sus compuertas están ciegas a las capas 3-4. Gates a revisar
con lupa (todos en `routing.py`, alimentados por el Domain Pack):

- `_parece_consulta_del_dominio_curso(...)` → ruta `bloqueo` si la pregunta/
  contexto no contiene `DOMAIN_HINT_TERMS`. **Riesgo:** un título genérico o una
  pregunta sin término de dominio cae a fuera-de-dominio aunque la lección la
  delegue. (Clase de bug "gate de dominio depende del título/keyword".)
- `SPECIFIC_UNSUPPORTED_TERMS = _PACK.unsupported_terms()` → puede rechazar
  términos (p. ej. otra herramienta/DAW) aun cuando `delegated_to_tutor` los
  cubra. (Clase de bug "rechaza lo delegado".)
- `_es_estudiante_perdido(...)` → frases hardcodeadas ("no entiendo", "me
  perdí"...). **Riesgo:** "no entiendo cómo funciona X concepto del curso" se
  marca `estudiante_perdido`. (Clase de bug "preguntas normales → perdido".)
- El prompt del clasificador LLM hardcodea "curso de mezcla y masterizacion".
  (Clase de bug "dominio cableado en el agente".)
- `_inferir_modulo_categoria(...)` tiene una escalera `if` Eje 0..7 acoplada al
  curso (aunque sembrada desde `COURSE_AXES` del pack).

El arreglo arquitectónico canónico (no implementar sin pedido): **pasar la
política pedagógica al supervisor** y hacer que los gates la consulten —
delegación y conceptos *anulan* el bloqueo de dominio; "perdido" exige señal real
no cubierta por un concepto del curso.

## 6. El otro punto caliente: doble inyección y herencia

En `render_context_block` (`context_service.py`):
- `learning_goal` se inyecta como "Objetivo de la leccion" (desde `lesson_data`)
  y otra vez como "Objetivo de aprendizaje" (desde `ctx`). Igual con
  `expected_action` ("Accion esperada de la leccion" vs "Accion esperada").
  (Clase de bug "objetivo/acción duplicados".) Verifica antes de tocar: pueden
  provenir de fuentes distintas y querer de-duplicación, no borrado.
- Herencia silenciosa: si una lección sin metadata/transcripción cae al retrieval
  general y trae chunks de **otra** lección, el tutor la describe con material
  ajeno. El scoping vive en `services/agent/retrieval.py` (pre-filtro Chroma por
  curso; alcance por eje/sección/lección). Audita que el retrieval priorice y, si
  no hay material propio, **declare insuficiencia** en vez de heredar.

## 7. Bloque activo y timestamp

`context_service.py::build_envelope` →
`lesson_service.resolve_lesson_block(lesson_id, timestamp)` resuelve
`active_lesson`/`active_block`. Con timestamp, `render_context_block` antepone un
bloque "BLOQUE ACTIVO DEL VIDEO". **Verifica el comportamiento sin timestamp:**
`resolve_lesson_block(lesson_id, None)` debe seguir devolviendo la lección (nivel
de lección) sin fabricar un bloque. La prueba 5/6 de [testing.md](testing.md)
cubre exactamente esto.

## 8. Diagnóstico / trazas que YA existen (y los que faltan)

El endpoint (`chat.py`) ya devuelve y persiste:
`ruta` (≈ `selected_route`), `intent`, `answer_type`, `course_module`,
`evaluation_category`, `requires_course_evidence`, `evidence_level`, `warnings`,
`runtime_context` (incluye `active_lesson_id`, `active_block_id`),
`source_policy` (`A_INDEXED_RAG` / `B_RUNTIME_CONTEXT` / `C_SYSTEM_RULES`),
`retrieved_chunks` + `scores`, `fuentes`.

Mapeo a los nombres canónicos de [concepts.md](concepts.md) §7 y **gaps**:

| Canónico | Estado actual |
|---|---|
| `selected_route` | existe como `ruta` |
| `intent` | existe |
| `active_lesson` / `active_block` | existen en `runtime_context` (ids) |
| `applied_policies` | parcial: `source_policy` cubre fuentes, **falta** qué políticas de metadata se aplicaron (delegación, restricciones) |
| `retrieval_scope` | **falta** explícito (curso/eje/sección/lección) |
| `evidence_level` | existe |
| `warnings` | existe |
| `blocked_by` | **falta** una razón explícita por la que un gate bloqueó/recortó |

Añadir `retrieval_scope`, `applied_policies` (metadata) y `blocked_by` es un fix
de observabilidad barato y habilita casi todas las pruebas de
[testing.md](testing.md).

## 9. Domain Pack (dominio como datos)

`tesis-rag/domain_packs/<course_id>.json` (piloto: `2.json`; `_default.json` es el
fallback neutro), cargado por `services/domain/domain_pack.py`. Contiene persona,
prompts de nodo, taxonomía de ejes, léxico de conceptos, listas allow/deny, FAQ.
**Toda** particularidad de dominio debe extenderse aquí, no en el agente. El gate
de routing consume `unsupported_terms`, `domain_hint_terms`,
`technical_word_list`, `concept_patterns`, `strong_axis_terms`, etc. del pack;
parte del vocabulario del gate duplica los `concepts` que define el profesor — un
objetivo de diseño es derivarlo de la metadata, no mantener dos listas.

## 10. Comandos útiles de verificación

```bash
# Estructura del agente
ls tesis-rag/services/agent/
# Dónde se lee un campo
#   (preferir Grep tool; ejemplo conceptual)
#   grep -rn "delegated_to_tutor" tesis-rag/
# Suite mantenida
cd tesis-rag && python -m pytest tests/ -q
# Probar el endpoint real (ver script de la skill)
python <skill>/scripts/probe_tutor.py --help
```
