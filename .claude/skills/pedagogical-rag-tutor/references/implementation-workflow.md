# Workflow de implementación

Aplica solo cuando el usuario **pide implementar** un cambio (no en auditoría).
El objetivo es el **arreglo arquitectónico mínimo correcto** que respeta la
jerarquía de contexto y mantiene el sistema agnóstico al curso, con pruebas que
prueben que el problema ya no ocurre y que nada se rompió.

## Antes de tocar código
1. **Confirma el alcance** con el usuario: qué hallazgo(s) se corrigen ahora.
2. **Recupera el estado del repo con cuidado.** Este proyecto tiene `.pyc`
   trackeados: `git stash`/`pop` se atasca con los `__pycache__`. Para comparar
   con HEAD usa `git show`/`git worktree`, no stash. (Gotcha de `CLAUDE.md`.)
3. **Relee la causa raíz** del [informe](templates.md) y la regla de
   [concepts.md](concepts.md) §8 que se viola.

## Principios de implementación
- **Mínimo y correcto, no mínimo y parche.** Si el bug es "el gate decide antes de
  hidratar", el fix es **pasar la política al gate** o mover la decisión después
  de hidratar — no añadir una excepción para el término del ejemplo (FL Studio,
  etc.). Un parche por término reaparece con el siguiente curso/lección.
- **Dominio en datos.** Si necesitas vocabulario nuevo, ponlo en el Domain Pack /
  metadata, nunca en el agente. Idealmente **deriva** el vocabulario del gate de
  los `concepts`/`delegated_to_tutor` ya definidos por el profesor, para no
  mantener dos listas.
- **Representación canónica.** Si el fix toca lógica que existe duplicada entre el
  tutor general y el de lección, unifícala en la representación canónica
  (`StudentContext` / `PedagogicalPolicy`, ver [concepts.md](concepts.md) §4) en
  vez de arreglar las dos copias.
- **Respeta la jerarquía al codificar el gate:** orden de precedencia
  seguridad/integridad → delegación de lección → dominio general. Un bloqueo de
  dominio se **anula** si `delegated_to_tutor`/`concepts` cubren el tema, pero
  **nunca** se anula una regla de seguridad.
- **Declara, no heredes.** Si una lección no tiene material propio suficiente, el
  cambio debe hacer que el tutor declare insuficiencia, no que tome chunks de otra
  lección. Ajusta el **scope del retrieval**, no solo el prompt.
- **Observabilidad como parte del fix.** Si tocas un gate, emite `blocked_by` con
  la razón. Si tocas retrieval, emite `retrieval_scope`. Si aplicas una política
  de metadata, refléjala en `applied_policies`. Un fix sin traza es difícil de
  testear y de defender en la tesis.
- **Pre y post.** Las restricciones (`attribution_constraints`) se imponen al
  construir el prompt **y** se verifican en la salida.

## Pasos
1. **Localiza el punto de cambio exacto** (archivo:función). Prefiere el punto más
   alto en la jerarquía donde el arreglo es correcto (p. ej. inyectar la política
   en el estado del grafo antes del supervisor, en vez de parchear cada gate).
2. **Implementa el cambio** siguiendo el estilo del código vecino (idioma español
   en strings de usuario y dominio, igual densidad de comentarios, mismos
   patrones). No reescribas de más.
3. **Añade/actualiza la observabilidad** asociada.
4. **Escribe la prueba que falla sin el fix y pasa con él** (ver
   [testing.md](testing.md)). Si el fix nació de un `suggested_prompt` o un tema
   `delegated_to_tutor`, la prueba se deriva directamente de esa metadata.
5. **Corre la prueba nueva** y confirma que pasa.
6. **Corre la regresión completa:** `cd tesis-rag && python -m pytest tests/ -q`.
   Si hay guards de política de corpus/ingest, respétalos (ver gotchas).
7. **Prueba el endpoint real** con `scripts/probe_tutor.py` para el escenario
   corregido y un par de escenarios vecinos (para descartar regresión de
   comportamiento que el unit test no capture).
8. **¿Requiere reindex?** Si tocaste mapeo eje→sección o lógica de ingest, el
   cambio **no surte efecto hasta reindexar** y el reindex es **destructivo**
   (`reindex_rag_clean.py` borra y reconstruye ChromaDB). No lo ejecutes por tu
   cuenta: avísalo como paso pendiente y deja que el usuario decida.

## Entrega
Resume con la [plantilla de plan/entrega](templates.md):
- Qué cambió (archivos:función) y por qué (regla restaurada).
- Pruebas nuevas/actualizadas y resultado de la regresión (real, con fallos si los
  hubo).
- Observabilidad añadida.
- Riesgos pendientes (¿requiere reindex? ¿stopgap vs fix definitivo? ¿deuda en
  otra capa?).
- Próximos pasos recomendados.

## Anti-patrones a rechazar (aunque "funcionen" en el ejemplo)
- Añadir el término del ejemplo a una allow-list a mano. (Reaparece.)
- Resolver un gate de dominio metiendo otra keyword del título.
- Bajar el umbral de evidencia globalmente para que "pase" una lección. (Rompe
  otras.)
- Hacer que el tutor de lección invente bloque/timestamp para uniformar con el
  caso con timestamp.
- Duplicar la lógica corregida en el tutor general y en el de lección.
