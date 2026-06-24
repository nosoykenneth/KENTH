# Pruebas mínimas obligatorias y criterios de aceptación

Toda auditoría que detecte un defecto y toda corrección deben dejar pruebas
**repetibles**. Lo ideal es que sean **end-to-end** (contra `/chat`), porque los
defectos viven en la interacción routing→retrieval→verificación, no en funciones
aisladas. Donde un e2e sea caro, un test de integración del nodo correspondiente
es aceptable, pero al menos los casos de "delegación", "perdido", "timestamp" y
"herencia" deben ejercitarse end-to-end.

## Cómo se ejecutan
- Suite mantenida: `cd tesis-rag && python -m pytest tests/ -q`.
- E2e contra el endpoint real: `scripts/probe_tutor.py` (manual/exploratorio) o un
  test pytest que haga POST a `/chat` con el backend levantado. Lee URL/token de
  entorno; nunca hardcodees credenciales.
- Reusa la metadata real: los `suggested_prompts` y `delegated_to_tutor` de cada
  lección **se convierten automáticamente** en casos (ver §"Generación
  automática").

## Los 18 casos obligatorios

Cada caso indica el **escenario** y la **aserción observable** (qué mirar en la
respuesta o en los campos de diagnóstico).

1. **Pregunta conceptual central de la lección** → responde anclado a la lección;
   `evidence_level` alto/parcial; no bloquea.
2. **Cada `suggested_prompt`** → no se rechaza, no cae a "ambigua"/"fuera de
   dominio"; produce respuesta útil. (Uno por prompt.)
3. **Cada `delegated_to_tutor`** → responde dentro del límite delegado **aunque no
   haya evidencia RAG**, marcándolo como adaptación operativa del tutor; no
   bloquea por dominio/términos.
4. **Cada `attribution_constraint`** → la restricción se cumple de forma
   observable en la salida (p. ej. ausencia de "receta universal" si está
   prohibida).
5. **Pregunta con bloque + timestamp** → resuelve `active_block`; la respuesta
   prioriza el bloque; `runtime_context.active_block_id` poblado.
6. **Misma pregunta sin timestamp** → sigue funcionando a nivel de lección; no
   inventa bloque; `active_block` vacío pero `active_lesson` presente.
7. **Pregunta sobre contenido futuro** → no "promete"/inventa ejes/temas que no
   corresponden; previene el preview de "eje futuro".
8. **Solicitud de receta universal** → la rechaza/relativiza según las
   restricciones; no entrega receta absoluta.
9. **Pregunta fuera del dominio** → bloquea con `blocked_by` explicando el porqué;
   no responde contenido ajeno.
10. **Lección con metadata completa** → todos los campos poblados influyen
    (objetivo orienta, restricciones se imponen, delegación habilita).
11. **Lección sin metadata** → funciona de forma degradada y **honesta**; no
    inventa objetivo/criterios; declara lo que no sabe.
12. **Lección sin transcripción** → no inventa contenido de video; si no hay
    material propio, declara insuficiencia.
13. **Retrieval que intenta traer otra lección** → no hereda; la respuesta no se
    arma con material de otra lección; `retrieval_scope` correcto.
14. **Pregunta normal que NO debe ser "perdido"** → una consulta conceptual que
    contiene "no entiendo X" se clasifica como consulta normal, no
    `estudiante_perdido`.
15. **Respuesta que no debe truncarse** → respuesta larga completa, sin corte a
    media frase.
16. **Tutor general vs tutor de lección** → sin `lesson_id` activo, modo general
    (orienta, no inventa bloque); con `lesson_id`, modo lección (ancla en la
    lección). Comportamientos distintos y correctos.
17. **Término específico ausente del RAG pero delegado** → (caso afinado de #3)
    p. ej. una traducción a otra herramienta marcada en `delegated_to_tutor`: se
    responde aunque el término no aparezca en la evidencia.
18. **Título genérico, conceptos del dominio** → una lección con título no
    descriptivo cuyos `concepts` son del dominio: la pregunta se trata dentro del
    dominio, no se bloquea.

## Generación automática desde metadata
Para no mantener los casos a mano, deriva 2/3/4 (y 17) directamente de la
metadata real de cada lección:
- por cada `suggested_prompt` → un caso tipo #2;
- por cada `delegated_to_tutor` → un caso tipo #3/#17;
- por cada `attribution_constraint` → un caso tipo #4 con su aserción de
  cumplimiento.
Un pequeño data-driven test (parametrize de pytest) que lea las lecciones y
expanda estos casos mantiene la cobertura alineada con lo que el profesor edita.

## Criterios de aceptación (la barra de "correcto")
El sistema pasa cuando, de forma repetible:
- los `suggested_prompts` del profesor no son rechazados (#2);
- los temas delegados se responden dentro de sus límites (#3, #17);
- las restricciones se cumplen de forma observable (#4);
- el tutor distingue adaptación general de evidencia del curso (#3, generación);
- el retrieval prioriza la lección activa (#1, #13);
- una lección vacía no se describe usando otra (#11, #12, #13);
- el timestamp mejora pero no es requisito (#5, #6);
- las preguntas normales no se marcan como "perdido" (#14);
- las compuertas explican por qué bloquearon (#9, `blocked_by`);
- la lógica central no depende del dominio de mezcla (revisión de código + #18);
- existen pruebas end-to-end repetibles (toda la suite).

## Notas de fiabilidad
- Si una aserción depende de la redacción libre del LLM, hazla **robusta**:
  verifica señales estructurales (ruta/intent/evidence_level/blocked_by, presencia/
  ausencia de un marcador) en vez de coincidencia exacta de texto.
- Si el modelo local introduce variabilidad, corre el caso varias veces y exige la
  propiedad (p. ej. "nunca clasifica como perdido"), no una salida idéntica.
