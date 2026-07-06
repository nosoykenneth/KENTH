# Auditoria H5P realtime guidance

Fecha: 2026-07-06 11:06
Servidor: /srv/kenneth/tic-kenth
Rama base auditada: main
Rama de trabajo: feat/h5p-realtime-guidance
Curso/seccion: course_id=2, moodle_section_id=2

## Frontend

- CourseContentView.jsx resuelve la leccion activa con resolveLessonForResource y mantiene tutorAbierto/tutorMontado para el panel lateral.
- H5PStudentSignal.jsx solo consulta GET /learning-signals/lesson/{lesson_id}/me al montar. No hay refresh, polling ni evento H5P conectado, por eso el estado no cambia hasta cerrar/reabrir.
- TutorAssistCard.jsx acepta proactiveMessage, pero es estatico y no deduplica por attempt_id/signal_hash.
- MoodleRenderer.jsx embebe el H5P en iframe moodle_view_iframe y solo escucha kenth:resource_meta para quitar spinner.
- useResourceTimestamp.js documenta que xAPI no se retransmite al padre por defecto. Se debe escuchar postMessage si aparece y usar polling temporal como respaldo.
- aiService.js no tiene AbortController/timeout para /chat.

## Backend

- GET /api/ai/learning-signals/lesson/{id}/me devuelve senales del estudiante autenticado.
- POST /api/ai/learning-signals/sync/lesson/{id} exige require_teacher, incompatible con sincronizacion iniciada por estudiante al terminar H5P.
- services/learning_signals.py separa explicitamente learning_signals de RAG/Chroma; solo se inyectan como runtime context en chat.
- No existe endpoint guidance listo para UI.
- api/routes/chat.py genera trace_id, pero no envuelve super_agente.invoke con fallback robusto.

## Estrategia

- Escuchar mensajes H5P/xAPI si el wrapper los emite: kenth:h5p_completed, kenth:h5p_submitted, kenth:h5p_answered y statement/xAPI.
- Como respaldo, al detectar interaccion o meta H5P iniciar polling cada 3 segundos hasta 30 segundos.
- El polling hace POST sync + GET guidance/me, sin recargar pagina ni cerrar modal.
- Guidance deterministico desde learning_signals, sin modelo y sin Chroma.
- Deduplicar en frontend con attempt_id o signal_hash en localStorage.
