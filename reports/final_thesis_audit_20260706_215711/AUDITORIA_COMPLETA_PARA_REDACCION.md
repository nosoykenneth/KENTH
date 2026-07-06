# AUDITORÍA COMPLETA PARA REDACCIÓN DEL DOCUMENTO — TIC KENTH

> Generada al cierre funcional y documental (rama
> `feat/final-ux-guidance-and-thesis-audit`, 2026-07-06/07, servidor de
> producción). Todos los conteos fueron medidos en vivo; las rutas de código son
> verificables en el repositorio. Complementos: `docs/tic/*.md`,
> `docs/tic/diagramas.md`, reportes en `reports/`.

---

## 1. Resumen ejecutivo del sistema

**Problema que resuelve.** En cursos virtuales asincrónicos el estudiante no
tiene retroalimentación inmediata ni personalizada, y los chatbots genéricos
alucinan contenido que el docente nunca aprobó. TIC KENTH implementa un curso
virtual (piloto: mezcla y masterización de audio) cuyo tutor de IA responde
**solo con evidencia aprobada por el docente** (RAG teacher-driven), entiende el
contexto exacto del estudiante (lección/momento del video) y **adapta su
orientación al desempeño real** medido con evaluación formativa H5P.

**Qué se implementó.**
- Plataforma SOA: SPA React + gateway nginx + FastAPI/LangGraph + Moodle/MariaDB
  + ChromaDB + Ollama (modelos 100% locales) + observabilidad Loki/Grafana.
- Flujo docente completo: transcripción aprobada, "Preparar tutor con IA",
  recursos reales con flags indexar/visible, publicación incremental.
- Sección 0 completa (7 lecciones) con H5P InteractiveVideo (29 interacciones)
  y learning signals que producen orientación automática: conceptos débiles
  priorizados + minuto del video + recurso + micro-práctica, con guía
  persistente y recuperable en la UI.
- Tono y nivel de ayuda por lección con directivas operativas; chat general
  neutral separado del chat de lección.

**Qué se validó.** Suite backend 263 tests verdes (4 skipped); 3 contratos
frontend; batería de retrieval 21/21; smoke de producción; auditoría de Chroma
(241 chunks, sin cambios durante este cierre); pruebas manuales del flujo
estudiante.

**Alcance.** Un curso (id=2), una sección completa end-to-end, defensa con
video de 3 minutos. El mecanismo es multi-curso por diseño (Domain Pack), pero
solo el piloto está poblado.

## 2. Objetivo general sugerido

> Desarrollar una plataforma de curso virtual con un tutor pedagógico basado en
> IA generativa local y recuperación aumentada por evidencia (RAG) gobernada por
> el docente, que entregue orientación adaptativa verificable a partir de la
> evaluación formativa del estudiante, validada funcionalmente en un curso
> piloto de mezcla y masterización de audio.

## 3. Objetivos específicos sugeridos

1. Diseñar e implementar el curso virtual piloto sobre Moodle (estructura de
   secciones/lecciones, recursos y video-lecciones) integrado a una SPA propia.
2. Integrar un tutor de IA contextual (FastAPI + LangGraph + Ollama) con
   enrutamiento determinista, verificación post-generación y trazabilidad por
   interacción.
3. Implementar el flujo RAG teacher-driven: el docente alimenta, aprueba y
   publica el conocimiento del tutor desde la interfaz (transcripciones,
   recursos, contexto aprobado), sin manipular artefactos técnicos.
4. Incorporar evaluación formativa H5P (InteractiveVideo) en las lecciones del
   piloto y transformar sus resultados en señales de aprendizaje por concepto.
5. Desarrollar la orientación adaptativa del tutor a partir de las señales
   (recomendación de minuto, recurso y micro-práctica, priorizada por
   desempeño) con una experiencia de usuario recuperable y no punitiva.
6. Validar funcionalmente el sistema: pruebas automatizadas backend/frontend,
   batería de retrieval con métricas, smoke de producción y validación manual
   del flujo del estudiante.

## 4. Alcance real implementado

- **Curso 2** ("mezcla y masterización"), **Sección 0 — El sistema de decisión**
  completa: 7 lecciones (SEC2-R55…R61, identidad anclada al cmid).
- **35 recursos docentes reales** subidos por el flujo del profesor
  (123 chunks `resource_text` + 21 `resource_description`).
- **RAG**: 241 chunks en Chroma para el curso; canonical_md de Sección 0
  superseded (208→0); retrieval scope-aware (block>lesson>section>global>course).
- **H5P**: 7 InteractiveVideo, 29 interacciones calificables; 49 resultados
  xAPI reales al cierre.
- **Tutor**: chat por lección (contexto + señales + tono/nivel), chat general
  neutral, orientación automática recuperable, timeout con fallback.
- **Roles**: estudiante / profesor (editing) / revisor / admin de curso /
  técnico RAG, resueltos por capabilities Moodle vía WS.
- **Validaciones**: ver §13.

## 5. Limitaciones (declararlas tal cual en el documento)

1. Solo la Sección 0 está poblada end-to-end; el resto del curso usa el
   mecanismo pero no está cargado.
2. La defensa se sustenta con un video de 3 minutos (no hay piloto longitudinal
   con estudiantes reales dentro del alcance).
3. Los modelos locales (llama3.1:8b) tienen muletillas y menor fluidez que
   modelos comerciales; se mitiga con guidance determinística y verificación
   post-generación.
4. Las señales de aprendizaje dependen de que el estudiante responda el H5P;
   sin intento no hay personalización (by design, no inventa desempeño).
5. Los binarios pesados (FLP, audio, stems) se distribuyen aparte; solo su
   descripción pedagógica es buscable.
6. El plugin `local_tesisai` y `api_persistente` viven en el runtime de Moodle
   del servidor (respaldados, fuera de este repo git).
7. Deuda técnica menor: residuales del esquema `axis_id` (migración
   ejes→secciones diferida en BD).

## 6. Arquitectura (para el capítulo de diseño)

Ver `docs/tic/ARQUITECTURA_GENERAL.md` y `docs/tic/diagramas.md` §1–2, §9.
Resumen: SOA tras gateway nginx con dos prefijos contractuales (`/api/ai/*` →
FastAPI; `/api/lms/*` → Moodle). FastAPI aloja el agente LangGraph (supervisor
determinista → rag/web/guardia/saludo/perdido), el retrieval Chroma pre-filtrado
por curso, la verificación post-generación, el authoring docente y los learning
signals. Moodle es el LMS y dueño del esquema (`mdl_local_tesisai_*` vía plugin).
MariaDB es la única BD operacional. Ollama sirve chat/embeddings/visión local.
Dos modos (dev nativo / full-docker) con paridad por contrato. Flujos completos:
diagramas §3 (chat), §4 (ai-prepare), §7 (teacher-driven), §8 (señales).

## 7. Módulos implementados

| Módulo | Dónde | Estado |
|---|---|---|
| Gestión de curso (secciones/recursos/participantes) | SPA + Moodle Studio embebido | ✅ |
| Recursos por lección (subir/describir/flags indexar-visible) | SPA + `/authoring/lessons/*/resources` | ✅ |
| Tutor pedagógico por lección (contexto+señales+perfil) | `TutorAssistCard` + `/chat` | ✅ |
| RAG teacher-driven (aprobar→preparar→publicar) | `teacher_context.py`, `ai_prepare/` | ✅ |
| H5P InteractiveVideo (29 interacciones) | mod_hvp + `scripts/h5p/` | ✅ |
| Learning signals + guidance determinística | `learning_signals.py` + 4 endpoints | ✅ |
| Guía recuperable (badge/flecha/sonido/persistencia) | `guidanceStore.js` + `CourseContentView` | ✅ (este cierre) |
| Tono/nivel de ayuda operativos | `pedagogy_profile.py` + `context_service.py` | ✅ (este cierre) |
| Chat general del curso (neutral) | `TutorView`/`OllamaChat` + deflector en `chat.py` | ✅ (este cierre) |
| Roles y permisos por capabilities | WS `get_permissions` + guards FastAPI | ✅ |
| Pagos (PayPhone/PayPal) y onboarding | `api_persistente` | ✅ (fuera del foco de tesis) |
| Observabilidad (logs JSON→Loki→Grafana) | promtail/loki/grafana | ✅ |

## 8. Flujo pedagógico (para el marco metodológico-pedagógico)

1. **Diagnóstico**: el video interactivo H5P evalúa formativamente durante la
   lección (no al final): cada interacción mapea a un concepto.
2. **Presentación del material**: video + recursos reales de la lección
   (bitácoras, plantillas, referencias) curados por el docente.
3. **Evaluación formativa**: MC/TF/Summary dentro del video; resultado en
   Moodle (xAPI + gradebook).
4. **Retroalimentación inmediata**: guía determinística del tutor — conceptos
   débiles priorizados, minuto exacto, recurso y micro-práctica; no punitiva.
5. **Refuerzo**: el chat del tutor orienta con las mismas señales y la
   evidencia del curso, con el tono/nivel de ayuda definidos por el docente.
6. **Práctica**: micro-prácticas concretas (proyecto del DAW) y retos aplicados
   cuando el nivel es `ready`.

## 9. Evidencia de buenas prácticas (con su justificación)

- **Human-in-the-loop**: nada se indexa sin aprobación docente
  (`INDEX_TRANSCRIPT_ONLY_AFTER_APPROVAL`; borradores IA aislados hasta aceptar).
- **El profesor no manipula Markdown/YAML/Chroma**: 4 gestos de interfaz
  (aprobar, preparar, subir, publicar).
- **Trazabilidad**: cada chunk lleva course/section/lesson/source_type; cada
  respuesta persiste trace con chunks, scores, fuentes, modelo, latencia.
- **Separación evidencia (RAG) vs comportamiento (inyección)**: el perfil
  pedagógico jamás entra al índice; `requires_reindex=false` al aceptar.
- **Learning signals runtime**: datos del estudiante NUNCA en Chroma ni en la
  query vectorial (solo inyección Capa 3).
- **Evaluación de retrieval**: batería 21/21 con reporte reproducible.
- **Backups/rollback**: backups de Chroma y BD antes de operaciones sensibles;
  reportes pre/post en `reports/`.
- **Privacidad/control local**: modelos Ollama locales; sin datos a terceros.
- **No punitividad**: pauta explícita inyectada + tests que la protegen.

## 10. Detalle teacher-driven RAG (números finales)

- canonical_md Sección 0: **208 → 0** activos (superseded; semilla en disco).
- Recursos reales: **35** (resource_text **123 chunks**, resource_description
  **21 chunks**); transcripciones aprobadas por lección;
  `teacher_approved_context` 50 chunks.
- Chroma curso 2: **241 chunks** — R55=30, R56=34, R57=38, R58=32, R59=36,
  R60=32, R61=33, L1(test)=6. **Sin cambios durante este cierre** (auditado
  antes/después).
- Indexación incremental delete-then-add (`teacher_context:<lesson_id>`); nunca
  reindex global en operación.
- Pruebas: batería 21/21 (retrieval) + 6/6 (preguntas sobre recursos);
  0 fugas de material interno (filtro visible_to_student en backend y frontend).
- Detalle: `docs/tic/TEACHER_DRIVEN_RAG.md`,
  reportes `section0_teacher_driven_resources_*`, `section0_retrieval_validation_*`.

## 11. Detalle H5P

- 7 videos **InteractiveVideo** (mod_hvp ids 21–27, curso 2), inyectados vía
  `H5PCore::filterParameters` **preservando cmid** (sin reimportar .h5p).
- **29 interacciones** calificables: multiple choice, true/false, summary
  (R55=5, R56–R61=4 c/u), todas dentro de la duración del video (test de
  manifest).
- Resultados: `mdl_hvp_xapi_results` (padre compound + hijos por interacción) +
  gradebook. Al cierre: **49 filas xAPI**; resultados en 6/7 videos (L6=0).
- Manifest pedagógico único (`course_2_interactions.json`): concepto +
  enunciado + remediación (timestamp_seconds, recurso real, micro-práctica) —
  el mismo archivo generó las interacciones y las interpreta.
- Endpoints: §3 de `docs/tic/H5P_LEARNING_SIGNALS.md`.

## 12. Detalle tutor adaptativo (post-cierre)

- **Lee señales**: score %, nivel (needs<60 / partial 60–79 / ready≥80),
  conceptos débiles **ordenados por menor acierto** (empate → orden del video).
- **Recomienda**: por concepto débil → minuto + recurso + micro-práctica; con
  2 débiles cubre ambos y da orden de repaso; con 3+ prioriza máximo 3
  ("Prioridad 1/2/3" + ruta corta); ready → reto aplicado, sin alerta.
- **Chat abierto**: la guía se inserta al historial; **cerrado**: badge
  "Conviene reforzar · el tutor tiene una guía" + flecha con contador + sonido
  (una vez por intento).
- **Dedupe**: por `attempt_id`/`signal_hash` (nuevo intento = nueva guía).
- **Recuperable**: persistida por curso+lección en localStorage (`guidanceStore`)
  con notified_at/seen_at; sobrevive recargas; expira a 7 días; clic en el
  badge → abre chat y reinserta/enfoca sin duplicar; no cruza lecciones.
- **Respeta al docente**: cierre del mensaje según nivel de ayuda; el chat
  aplica directivas operativas de tono/nivel (sin alterar la verdad ni omitir
  minuto/recurso).

## 13. Validaciones realizadas (evidencia para Resultados)

| Validación | Resultado |
|---|---|
| Backend `pytest tests/` (contenedor aislado, Chroma de prueba) | **263 passed, 4 skipped, 0 failed** |
| Nuevos tests del cierre (`test_final_ux_guidance.py`) | 21 tests: multi-concepto, prioridades, tono/nivel, chat general |
| Frontend `npm run lint` | 0 errores (4 warnings preexistentes) |
| Contratos frontend (`test:moodle-section`, `test:chat-sources`, `test:guidance`) | 3/3 OK |
| `npm run build` | OK |
| Batería retrieval Sección 0 | 21/21 + 6/6 recursos |
| Health producción `/api/ai/health` | ok (fastapi/moodle_db/moodle_ws/chroma/ollama) |
| Smoke producción (`smoke_produccion.sh`) | OK (ver REPORTE_FINAL del cierre) |
| Auditoría Chroma antes/después del cierre | 241 = 241 (sin cambios) |
| H5P render-ready | 7/7 videos con interacciones activas |
| Pruebas manuales de navegador | flujo badge→guía, multi-concepto, chat general (ver §Validación del REPORTE_FINAL) |

## 14. Riesgos y mitigaciones

| Riesgo | Mitigación implementada |
|---|---|
| Contaminación de Chroma por tests | tests corren con `CHROMA_DIR` aislado; fixtures limpian; auditoría de conteos pre/post |
| Reindex global destructivo | prohibido en operación; indexación incremental por lección; backups `bd_vectorial_backup_*` |
| Rate-limit del gateway en cargas | drivers con `--sleep`; límites por zona en nginx |
| Pérdida de uploads | volumen persistente para recursos |
| Rotura de H5P al editar | inyección vía filterParameters preservando cmid; backup de BD antes de tocar H5P |
| Chat colgado por modelo lento | timeout en el cliente + fallback con reintento; location nginx dedicada con timeout 600s para authoring |
| Alucinación del tutor | RAG con evidencia + verificación post-generación + guidance determinística |
| Rollback | despliegue por imagen; `git reset --hard origin/main` + rebuild; reportes con pre-state |

## 15. Material para el capítulo de Metodología

- **Tipo**: proyecto tecnológico aplicado (desarrollo e integración de
  software) con validación funcional; enfoque cuantitativo-descriptivo en las
  métricas de validación (tests PASS/FAIL, precisión de retrieval, conteos).
- **Fases ejecutadas** (trazables por PRs/reportes): (1) plataforma y
  arquitectura SOA; (2) tutor RAG + Domain Pack + verificación; (3) authoring
  docente (perfil canónico, ai-prepare, momentos); (4) corpus por secciones y
  migración ejes→secciones; (5) teacher-driven RAG Sección 0 (supersesión
  canónica); (6) H5P + learning signals + tutor adaptativo; (7) cierre UX +
  chat general + tono/nivel; (8) documentación y auditoría final.
- **Herramientas**: React 19/Vite/Tailwind, FastAPI, LangGraph, ChromaDB,
  Ollama (llama3.1:8b, nomic-embed-text, qwen3:14b), Moodle 5 + mod_hvp,
  MariaDB, Docker Compose, nginx, Loki/Grafana, Whisper, pytest/eslint/node.
- **Pruebas**: unitarias e integración backend (263), contratos frontend (3),
  batería de retrieval con criterios de aceptación, smoke E2E, validación
  manual guiada.

## 16. Material para el capítulo de Resultados

- **Tablas de conteos**: §10 (Chroma/source_type/lección), §11 (H5P/xAPI),
  §13 (validaciones). PRE_STATE con los valores exactos en
  `reports/final_ux_guidance_thesis_audit_20260706_215711/PRE_STATE.md`.
- **Ejemplo de interacción real** (salida literal de `build_guidance_message`
  con el manifest de producción, lección SEC2-R55, 2 conceptos fallados):

  > Revisé tus respuestas del video interactivo. Conviene reforzar estos puntos:
  >
  > 1. formular un diagnóstico útil (elemento, momento y cualidad)
  >    Vuelve al minuto 2:30 del video. Usa el recurso “Bitácora de decisiones
  >    de mezcla”. Practica: Diagnostica una voz áspera nombrando elemento,
  >    momento y cualidad, y anótalo en la bitácora.
  > 2. verificar con A/B a volumen igualado
  >    Vuelve al minuto 4:50 del video. Usa el recurso “Apuntes del profesor —
  >    Mezclar es decidir: el ciclo de trabajo”. Practica: Haz un bypass
  >    igualando volumen y decide si el cambio realmente ayuda.
  >
  > Estos dos puntos se conectan en la práctica: primero revisa formular un
  > diagnóstico útil (elemento, momento y cualidad), luego aplica verificar con
  > A/B a volumen igualado en el proyecto de práctica.
  > ¿Quieres que repasemos el primer punto juntos?

- **Evidencia de mejora del flujo** (antes → después del cierre):
  guía perdible al recargar → persistida y recuperable; 1 concepto → hasta 3
  priorizados; tono/nivel decorativos → directivas operativas verificadas por
  test; chat general podía derivar a rutas genéricas ante "qué debo reforzar" →
  respuesta determinística honesta.
- **PASS/FAIL**: suite completa y contratos en §13.

## 17. Material para Conclusiones

- Se demostró que un tutor RAG **gobernado por el docente** puede dar
  retroalimentación personalizada inmediata **sin indexar datos del alumno** y
  sin depender de servicios externos (modelos locales).
- La Sección 0 demuestra el ciclo completo y repetible: autoría docente →
  conocimiento indexado → evaluación formativa → señales → orientación
  adaptativa verificable.
- **Escalamiento**: poblar el resto de secciones es operación de contenido
  (mismo flujo docente), no de código; multi-curso = nuevo Domain Pack +
  manifest de interacciones.
- **Trabajo futuro**: vista longitudinal por estudiante, evaluación con
  estudiantes reales (piloto controlado), afinamiento de modelos locales,
  completar la limpieza de esquema (axis_id), panel docente de señales
  agregadas por sección.

## 18. Guion técnico para el video de 3 minutos

Ver `docs/tic/FLUJO_DEFENSA_3_MIN.md` §1 (tabla con tiempos, acciones exactas y
narración sugerida). Cubre: login → estructura del curso → secciones → lección
de Sección 0 → video H5P → recursos → evaluación → orientación automática del
tutor (badge→guía) → pregunta con fuentes → cierre.

## 19. Checklist para grabar el video

Ver `docs/tic/FLUJO_DEFENSA_3_MIN.md` §2: preparación (usuario demo sin
intentos, health ok, ensayo para calentar Ollama, chat cerrado, audio on),
qué mostrar (badge con "Ver guía", ≥2 conceptos numerados, minuto+recurso,
fuentes), qué NO mostrar (admin técnico, logs, tokens), y plan B ante fallas.

## 20. Estado final del sistema

*(Se completa en el REPORTE_FINAL del cierre tras merge+deploy; valores al
momento de esta auditoría:)*

- Servidor: `/srv/kenneth/tic-kenth`, contenedores 9/9 up, health ok.
- Chroma: 241 chunks (sin cambios en este cierre).
- Rama de trabajo con el cierre funcional + documental; pendiente inmediato:
  PR → merge a `main` → deploy → smoke → REPORTE_FINAL (FASE 8).
- Pendientes reales post-cierre: los de §5 (alcance) — ninguno bloquea la
  redacción ni la defensa.
