# Contrato de metadata (campos = políticas ejecutables)

Cada campo de metadata pedagógica es una **política**, no texto decorativo. Para
cada uno, la auditoría debe responder tres preguntas:

1. **¿Dónde se LEE?** (archivo/función). Si no se lee en ningún lado de la lógica,
   es un campo *muerto* → hallazgo.
2. **¿Qué EFECTO produce?** ¿Solo entra al prompt, o además gobierna routing /
   gates / retrieval / verificación?
3. **¿Respeta la jerarquía?** ¿Puede una regla global anular su efecto cuando no
   debería?

Usa `scripts/scan_metadata_usage.py` para responder (1) en segundos y para
detectar campos muertos. Usa este archivo para saber qué *debería* hacer cada
campo.

## Cómo leer la tabla "efecto esperado"

- **Inyección** = debe aparecer en el prompt (contexto runtime, etiquetado).
- **Routing/Intención** = debe influir en la ruta/clasificación.
- **Autorización** = habilita una capacidad (puede vencer un gate de dominio).
- **Gate** = puede bloquear/condicionar.
- **Retrieval** = debe afectar el alcance o el ranking.
- **Forma** = afecta el formato/tono/estructura de la respuesta.
- **Verificación** = debe imponerse en la salida (post-generación).

## Catálogo

### `learning_goal` / `learning_goals`
- **Qué es:** objetivo(s)/criterios de la lección.
- **Efecto esperado:** Inyección + Routing/Intención (ayuda a decidir dominio) +
  Forma (la respuesta debe servir al objetivo).
- **Trampa real:** se inyecta como "Objetivo de la leccion" *y* como "Objetivo de
  aprendizaje" (doble). De-duplicar, no borrar.
- **Para el gate de dominio:** un objetivo del dominio mantiene la pregunta dentro
  del dominio aunque el título sea genérico.

### `expected_action`
- **Qué es:** qué debe hacer el alumno a continuación.
- **Efecto esperado:** Inyección + Forma (orienta el "siguiente paso" de la
  respuesta).
- **Trampa real:** también se inyecta dos veces. De-duplicar.

### `prerequisites`
- **Qué es:** lecciones previas necesarias.
- **Efecto esperado:** Inyección + Forma (si el alumno muestra lagunas, remitir a
  estas lecciones) + posible señal de progreso.
- **Verifica:** que se use para *remitir*, no para bloquear arbitrariamente.

### `delegated_to_tutor`  ⭐ (causa #1 de bugs)
- **Qué es:** temas que el profesor encarga **explícitamente** al tutor, aunque no
  estén literales en la evidencia RAG (p. ej. "traduce los pasos a otra
  herramienta", "explica el atajo equivalente en X").
- **Efecto esperado:** **Autorización** (vence el gate de dominio y el gate de
  términos no soportados) + Inyección + Retrieval (no exigir evidencia para el
  tema delegado) + Forma (responder **distinguiendo** adaptación operativa del
  tutor vs contenido oficial del curso).
- **Trampa real:** el supervisor bloquea por `unsupported_terms` /
  `domain_hint_terms` **antes** de mirar `delegated_to_tutor`. Resultado: rechaza
  lo que el profe delegó. Fix: la delegación debe consultarse en el gate.
- **Límite:** no autoriza temas fuera de lo delegado ni viola
  `attribution_constraints` o reglas de seguridad.

### `attribution_constraints`  ⭐ (cumplimiento observable)
- **Qué es:** reglas obligatorias de comportamiento/atribución para esta lección
  (p. ej. "no des una receta universal", "atribuye al criterio del autor", "no
  prometas resultados").
- **Efecto esperado:** **se impone PRE y POST generación**. Pre = entra como
  norma en el prompt. Post = la verificación valida que la salida las cumple.
- **Trampa real:** llegan al prompt pero no hay verificación que las imponga en la
  salida → cumplimiento no observable. Conviértelas en aserciones de test.

### `proactive_message`
- **Qué es:** mensaje que el tutor puede ofrecer proactivamente en la lección.
- **Efecto esperado:** Inyección (runtime) + Forma. **No** es evidencia
  documental: el modelo no debe citarlo como contenido del curso.

### `suggested_prompts`  ⭐ (se vuelven pruebas)
- **Qué es:** preguntas que el profesor sugiere que el alumno haga.
- **Efecto esperado:** Inyección + (implícito) **deben ser respondibles**: si el
  profe la sugirió, el tutor **no** puede rechazarla por fuera-de-dominio o pedir
  aclaración trivial.
- **Acción de la skill:** cada `suggested_prompt` se convierte automáticamente en
  un caso de prueba que debe pasar (ver [testing.md](testing.md)).

### `lesson_blocks` (+ campos de bloque)
- **Qué es:** segmentación del recurso (típicamente video) en bloques con tiempos.
- **Efecto esperado:** Retrieval/Contexto — con `timestamp` se resuelve el bloque
  activo y se prioriza. Cada bloque puede traer `tutor_focus`, `concepts`,
  `probable_questions`, `interaction_mode`, `summary`.
- **Trampa real:** sin timestamp no debe romperse ni fabricar un bloque.

### `tutor_focus` (de bloque)
- **Qué es:** en qué debe centrarse el tutor en el bloque activo.
- **Efecto esperado:** Forma + prioridad de respuesta cuando hay bloque activo.

### `probable_questions` / `preguntas_probables` (de bloque)
- **Qué es:** preguntas que el alumno probablemente hará aquí.
- **Efecto esperado:** Routing/Intención + clasificación de dominio (ayudan a
  reconocer que una pregunta pertenece al curso). Son **pistas runtime**, no
  evidencia: no se citan como contenido.

### `concepts` (de lección/bloque)
- **Qué es:** conceptos en juego.
- **Efecto esperado:** **Clasificación de dominio/intención** (un concepto del
  curso mantiene la pregunta dentro del dominio) + Retrieval (anclar la búsqueda)
  + señal contra falsos "fuera de dominio".
- **Objetivo de diseño:** el vocabulario del gate de dominio debería derivarse de
  `concepts` (propiedad del profesor), no de una lista paralela mantenida a mano.

### `interaction_mode`
- **Qué es:** modo del tutor (teoría/práctica/troubleshooting/revisión/…).
  Enum compartido con el editor React; ambos listados deben ser idénticos.
- **Efecto esperado:** Forma (tono/estructura) + posible Routing.
- **Trampa real:** un valor que no existe en el enum es error de datos; debe
  reportarse fuerte, nunca conservar el modo previo en silencio.

---

## Checklist de metadata (para cada lección auditada)

Marca por campo. "Leído" = aparece en la lógica, no solo en el modelo de datos.

- [ ] **Inventario:** ¿qué campos están poblados en esta lección? (completa vs
      incompleta — audita al menos una de cada una).
- [ ] `learning_goal(s)` — leído, inyectado **una sola vez**, e influye en dominio.
- [ ] `expected_action` — leído, inyectado una sola vez, orienta siguiente paso.
- [ ] `prerequisites` — leído; usado para remitir, no para bloquear.
- [ ] `delegated_to_tutor` — leído **en el gate de dominio/términos**, no solo en
      el prompt; autoriza el tema; la respuesta lo marca como adaptación operativa.
- [ ] `attribution_constraints` — impuestas **pre y post** generación; verificables.
- [ ] `proactive_message` — inyectado como runtime; no citable como evidencia.
- [ ] `suggested_prompts` — respondibles (no rechazados); convertidos en pruebas.
- [ ] `lesson_blocks` — con timestamp resuelven bloque; sin timestamp no rompen.
- [ ] `tutor_focus` — prioriza respuesta cuando hay bloque activo.
- [ ] `probable_questions` — ayudan a clasificar dominio; no se citan como evidencia.
- [ ] `concepts` — gobiernan clasificación de dominio y anclan retrieval.
- [ ] `interaction_mode` — afecta forma; valor inválido se reporta, no se silencia.
- [ ] **Campos muertos:** ningún campo poblado queda sin lectura en la lógica.
- [ ] **Jerarquía:** ninguna regla global anula un campo de lección sin razón de
      seguridad/integridad.
- [ ] **Separación de fuentes:** lo runtime (proactive/probable/foco) no se
      presenta como evidencia documental.
