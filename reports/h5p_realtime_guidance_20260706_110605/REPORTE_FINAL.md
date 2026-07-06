# Reporte final - H5P realtime guidance

Fecha: 2026-07-06
Rama: feat/h5p-realtime-guidance
Servidor: /srv/kenneth/tic-kenth
Curso/seccion validada: course_id=2, moodle_section_id=2

## Auditoria

Ver AUDIT.md en este mismo directorio. Hallazgos principales:

- La UI de alumno solo consultaba learning_signals al montar H5PStudentSignal.
- sync/lesson/{lesson_id} estaba cerrado a profesor, por eso el alumno no podia recalcular al terminar H5P.
- El chat ya aceptaba un mensaje proactivo inicial, pero no uno nuevo por attempt_id.
- El wrapper H5P no garantiza xAPI al padre; se usa postMessage si existe y polling corto como respaldo.

## Estrategia H5P

- Listener de mensajes kenth:h5p_completed, kenth:h5p_submitted, kenth:h5p_answered, kenth:resource_time, xAPI/statement.
- Fallback: polling temporal cada 3 segundos por maximo 30 segundos.
- Cada ciclo llama POST /api/ai/learning-signals/sync/lesson/{lesson_id} y POST /api/ai/learning-signals/lesson/{lesson_id}/guidance.
- Se detiene al encontrar status=available o al vencer el limite.

## Cambios backend

- learning_signals.py ahora incluye ttempt_id, updated_at y signal_hash.
- Nuevo guidance_for() deterministico: no llama al modelo, no usa Chroma y no toca prompts globales.
- Nuevo sync_lesson_for_user() para recalculo idempotente por estudiante autenticado.
- learning_signals.py mantiene la separacion: learning_signals son runtime context, no evidencia RAG.
- learning_signals.py conserva sync_lesson() agregado para profesor.
- learning_signals.py tiene tests nuevos para partial/not_attempted/ready/sync idempotente.
- pi/routes/learning_signals.py agrega POST /lesson/{lesson_id}/guidance y cambia sync a 
equire_course_view.
- chat.py captura excepciones del agente, loguea 	race_id y devuelve fallback visible.

## Cambios frontend

- CourseContentView.jsx coordina polling H5P, sync de senales, guidance proactivo, badge/flecha y sonido corto.
- H5PStudentSignal.jsx acepta senal externa y refresh sin cerrar/reabrir.
- TutorAssistCard.jsx inserta guidance nueva por ID estable sin duplicar historial.
- MoodleRenderer.jsx notifica actividad H5P al contenedor cuando llegan mensajes del wrapper/iframe.
- iService.js agrega timeout de 45s con AbortController para liberar input del chat.
- 
agService.js agrega getLessonSignalGuidance().

## Comportamiento chat abierto/cerrado

- Chat abierto: la guidance entra como mensaje assistant y hace scroll por el comportamiento existente del chat.
- Chat cerrado: aparece badge 1, tooltip/flecha Abre el tutor para ver que reforzar, y sonido corto si el navegador permite audio y hubo interaccion previa.
- Al abrir tutor: se mueve la guidance pendiente al chat y se limpia el badge.
- Deduplicacion: localStorage por kenth:h5p-guidance:{course_id}:{lesson_id} con ttempt_id o signal_hash.

## Pruebas

- `python3 -m py_compile tesis-rag/services/learning_signals.py tesis-rag/api/routes/learning_signals.py tesis-rag/api/routes/chat.py`: OK.
- `pytest tests/test_learning_signals.py -q` en contenedor FastAPI efimero: 19 passed.
- `pytest tests/ -q` en contenedor FastAPI efimero aislado: detecto fallo ambiental por Ollama no accesible.
- `pytest tests/ -q` con `docker compose run` y `AI_PREP_MODEL=qwen2.5:14b-instruct`: OK completo. Sin ese override, el `.env` del servidor usa `qwen3:14b` y falla una expectativa historica de `test_ai_prepare.py`.
- `npm run lint` en contenedor Node efimero: OK con 4 warnings heredados de exhaustive-deps.
- `npm run test:moodle-section`: OK.
- `npm run test:chat-sources`: OK.
- `npm run build`: OK.
- `docker compose -f docker-compose.deploy.yml --env-file .env build fastapi frontend`: OK.

## Riesgos

- Si el wrapper Moodle no emite ningun evento despues de que el estudiante interactua, solo se garantiza polling inicial/onLoad/meta. El fallback mejora con cualquier kenth:resource_time o evento xAPI futuro.
- El sonido depende de permisos del navegador y de interaccion previa del usuario.
- pytest tests/ completo requiere que AI_PREP_MODEL coincida con el valor esperado por la suite historica o que el test se actualice al modelo configurado en servidor.

## Rollback

- Git: revertir el commit de esta rama.
- Servidor: git checkout main && git reset --hard origin/main && docker compose -f docker-compose.deploy.yml --env-file .env up -d --build fastapi frontend gateway.
