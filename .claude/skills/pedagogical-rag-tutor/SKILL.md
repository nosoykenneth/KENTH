---
name: pedagogical-rag-tutor
description: >-
  Auditar, diseñar, implementar, corregir y testear la capa de IA de un curso
  virtual cuando el tutor NO debe comportarse como un chatbot RAG genérico sino
  como un tutor pedagógico contextual gobernado por la estructura del curso, la
  metadata de cada lección, el bloque activo del recurso, la evidencia recuperada
  y el progreso del alumno. Úsala SIEMPRE que el trabajo toque el agente
  LangGraph / RAG, el routing o clasificación de intención, las compuertas
  (gates) de dominio/seguridad, el retrieval por lección/eje/sección, los
  prompts del tutor, la verificación post-generación, los servicios de contexto
  (Capas 2/3), o el contrato de metadata pedagógica (learning_goal,
  delegated_to_tutor, attribution_constraints, suggested_prompts,
  proactive_message, tutor_focus, probable_questions, concepts, interaction_mode,
  lesson_blocks). Dispara también ante síntomas como: "el tutor rechaza una
  pregunta que el profe delegó", "marca preguntas normales como estudiante
  perdido", "una lección vacía responde con el contenido de otra", "el gate de
  dominio depende del título", "el tutor inventa contexto de video", "el timestamp
  rompe el tutor", "diferencia entre tutor general y tutor dentro de lección", o
  cualquier auditoría/fix/test end-to-end del tutor de IA del proyecto
  (Moodle + React + FastAPI/LangGraph). Es una skill de proceso: produce
  hallazgos por severidad con causa raíz, planes de fix arquitectónico y pruebas
  repetibles, no respuestas sueltas.
---

# Pedagogical RAG Tutor

Skill de ingeniería para la **capa de inteligencia artificial** de un curso
virtual cuyo tutor está gobernado por datos pedagógicos, no por reglas cableadas.
El sistema de referencia es el proyecto de tesis **TIC KENTH** (Moodle +
frontend React + backend FastAPI/LangGraph con RAG), pero la lógica central de
la skill es **agnóstica al curso**: las particularidades de dominio deben venir
de configuración (Domain Pack) y metadata, nunca del código del agente.

> Trata el sistema como un **tutor pedagógico contextual**, no como un
> "RAG + LLM". El comportamiento correcto emerge de cómo la metadata gobierna
> el flujo, no solo de qué texto entra al prompt.

## Cuándo usar esta skill

Actívala cuando el usuario quiera **analizar, diseñar, implementar, corregir o
probar** cualquier parte del tutor de IA. Señales típicas (úsalas como ejemplos,
no como lista cerrada):

- "audita el tutor dentro de una lección" / "revisa el flujo del agente".
- "el tutor rechaza una pregunta que el profesor delegó al tutor" (p. ej. una
  traducción de un término a otra herramienta marcada en `delegated_to_tutor`).
- "marca como estudiante perdido preguntas normales".
- "una lección sin metadata responde usando la transcripción de otra".
- "la compuerta de dominio bloquea según el título de la lección".
- "el tutor inventa un bloque/timestamp que no existe" o "sin timestamp deja de
  funcionar".
- "diferencia entre el tutor general del curso y el tutor dentro de una lección".
- "objetivo y acción esperada se inyectan duplicados".
- "haz que `suggested_prompts` no sean rechazados" / "convierte los prompts
  sugeridos en pruebas".
- cualquier pedido de **observabilidad / trazabilidad** del agente (por qué
  eligió una ruta, qué políticas aplicó, qué bloqueó la respuesta).

No la uses para tareas ajenas al tutor de IA (UI pura sin lógica de tutor,
pagos, infra de Moodle no relacionada, etc.).

## Principio arquitectónico central (la regla que todo lo demás sirve)

**La metadata pedagógica es política ejecutable, no decoración del prompt.** Debe
gobernar, en este orden de influencia: (1) enrutamiento, (2) clasificación de
intención, (3) autorizaciones del tutor, (4) bloqueos, (5) recuperación de
evidencia, (6) forma de respuesta, (7) validación final.

La **jerarquía de contexto** (de mayor a menor autoridad) es:

1. Reglas generales del sistema (seguridad, integridad académica).
2. Configuración del curso (Domain Pack).
3. Metadata de la **lección activa**.
4. Metadata del **bloque activo**.
5. Evidencia **RAG** recuperada.
6. Conocimiento general **autorizado**.
7. Historial y **progreso** del alumno.

Corolario que origina la mayoría de los bugs reales: **una regla global no debe
bloquear una capacidad que la lección delegó explícitamente al tutor**, salvo que
exista una prohibición superior de seguridad o integridad académica. Si una
compuerta decide *antes* de hidratar el contexto pedagógico (lección, bloque,
`concepts`, `delegated_to_tutor`), es casi siempre un defecto arquitectónico, no
un detalle de tuning.

## Los dos modos del tutor (no los confundas nunca)

- **A. Tutor general del curso** — dentro del curso pero **fuera de una
  lección**. Orienta, navega, explica conceptos generales y considera el
  progreso. **No** debe inventar contexto de video/bloque activo.
- **B. Tutor dentro de una lección** — recibe `course_id`, sección, `lesson_id`,
  recurso, metadata de la lección y, opcionalmente, `timestamp`. Responde
  **primero desde la lección activa**. Con `timestamp` resuelve el bloque
  activo; **sin** `timestamp` debe seguir funcionando a nivel de lección.

La lógica común (contexto del alumno, política pedagógica) debe vivir en una
**representación canónica compartida**, no duplicarse entre A y B. Ver
[concepts.md](references/concepts.md).

## Cómo navegar esta skill (lee el archivo que toca, cuando toca)

| Necesitas… | Lee |
|---|---|
| Entender jerarquía, modos, representaciones canónicas y reglas de diseño | [references/concepts.md](references/concepts.md) |
| Saber **dónde** vive cada cosa en el repo real y el flujo verdadero | [references/architecture-map.md](references/architecture-map.md) |
| Tratar cada campo de metadata como política y verificar dónde se lee | [references/metadata-contract.md](references/metadata-contract.md) |
| Ejecutar una **auditoría** completa por fases | [references/audit-workflow.md](references/audit-workflow.md) |
| **Implementar** un fix de forma segura y mínima | [references/implementation-workflow.md](references/implementation-workflow.md) |
| Revisar routing / retrieval / generación con checklist | [references/checklists.md](references/checklists.md) |
| Generar/mantener las pruebas mínimas obligatorias | [references/testing.md](references/testing.md) |
| Entregar el informe de hallazgos o el plan de implementación | [references/templates.md](references/templates.md) |

Scripts reutilizables (sin secretos, configurables por curso):

- `scripts/scan_metadata_usage.py` — mapea dónde se **lee** cada campo de
  metadata en el backend y marca campos "muertos" (declarados pero nunca
  consumidos por la lógica). Soporta el requisito "comprobar dónde se lee cada
  campo y qué efecto tiene".
- `scripts/probe_tutor.py` — golpea el endpoint real del tutor con un payload
  (curso/sección/lección/recurso/timestamp/mensaje) e imprime la respuesta y los
  campos de diagnóstico. Toma URL y token de variables de entorno; no embebe
  credenciales.

Ejecuta `python scripts/scan_metadata_usage.py --help` y
`python scripts/probe_tutor.py --help` para ver opciones.

## Flujo de trabajo de un vistazo

La skill tiene dos modos de operación; casi siempre se hace auditoría primero y
luego implementación.

1. **Auditoría** (por defecto al invocar sin un fix concreto): traza el flujo
   real end-to-end, inspecciona metadata real (una lección completa y una
   incompleta), renderiza el contexto exacto que recibe el modelo, prueba el
   endpoint real, clasifica hallazgos por severidad con causa raíz, y propone el
   arreglo arquitectónico mínimo. **No** modifica código todavía. Detalle en
   [audit-workflow.md](references/audit-workflow.md).
2. **Implementación** (solo cuando el usuario lo pide): aplica el fix mínimo
   correcto, crea/actualiza pruebas, corre regresiones y entrega resumen de
   cambios, riesgos y próximos pasos. Detalle en
   [implementation-workflow.md](references/implementation-workflow.md).

## Reglas de oro (resumen; el detalle vive en concepts.md)

- **No re-cablees dominio en el agente.** Nada de nombres de cursos ("mezcla"),
  DAWs concretos, o términos de dominio en la lógica central. Extiende el Domain
  Pack / la metadata.
- **No decidas antes de hidratar.** Compuertas críticas (dominio, bloqueo,
  "perdido") no deben resolverse solo sobre la pregunta cruda y un string de
  contexto; deben poder consultar lección, bloque, `concepts` y
  `delegated_to_tutor`.
- **Ausencia de evidencia ≠ fuera de dominio.** Antes de bloquear, revisa
  `delegated_to_tutor`, `suggested_prompts`, `probable_questions`, `concepts`,
  `learning_goal`, `title` y el contexto de sección.
- **No herencia silenciosa.** Una lección sin metadata/sin evidencia no debe
  responder con el contenido de otra; el tutor debe **declarar insuficiencia de
  contexto** cuando corresponda.
- **Determinismo para gates críticos.** No dejes que un LLM pequeño decida solo
  compuertas que pueden resolverse con reglas deterministas.
- **Separa las cuatro fuentes.** Contexto runtime, evidencia documental, reglas
  del sistema y conocimiento general son distintos; nunca presentes metadata
  runtime como si fuera evidencia documental.
- **Timestamp mejora, no condiciona.** El bloque activo enriquece; su ausencia no
  debe degradar el nivel de lección.
- **Observabilidad siempre.** Mantén trazables `selected_route`, `intent`,
  `active_lesson`, `active_block`, `applied_policies`, `retrieval_scope`,
  `evidence_level`, `warnings`, `blocked_by`. Las compuertas deben explicar
  **por qué** bloquearon.
- **Implementa solo cuando te lo pidan.** En auditoría, primero propones; el
  usuario aprueba; luego cambias código.

## Criterios de aceptación (cuándo el sistema está "bien")

- Los `suggested_prompts` del profesor no son rechazados.
- Los temas `delegated_to_tutor` se responden dentro de sus límites, distinguiendo
  adaptación operativa del tutor de evidencia del curso.
- Las `attribution_constraints` se cumplen de forma observable (antes y después de
  generar).
- El retrieval prioriza la lección activa; una lección vacía no se describe con
  otra.
- El `timestamp` mejora el contexto pero no es requisito para funcionar.
- Las preguntas normales no se clasifican arbitrariamente como estudiante perdido.
- Las compuertas explican por qué bloquearon (`blocked_by`).
- La lógica central no depende del dominio de mezcla.
- Existen pruebas end-to-end repetibles (ver [testing.md](references/testing.md)).
