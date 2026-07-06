# PRE_STATE — final_ux_guidance_thesis_audit — 2026-07-06 21:57 UTC

## Git
- Rama: main
- HEAD: aba2ab890d9079fec45a612cb31df63ee8dc1d15 (feat: add realtime H5P tutor guidance)
- origin/main: idéntico (sin drift)
- Working tree: limpio (solo reports/ untracked)

## Contenedores
9 up: tic-fastapi, tic-frontend, tic-gateway, tic-grafana, tic-loki, tic-mariadb(healthy), tic-moodle, tic-moodle-cron, tic-promtail

## Health
/api/ai/health → status ok, fastapi/moodle_db/moodle_ws/chroma/ollama ok, chroma_chunks=241, chat=llama3.1:8b, embedding=nomic-embed-text

## Chroma (colección langchain, path /app/bd_vectorial)
- Total: 241 chunks
- by_source_type: None=191, teacher_approved_context=50
- course 2 by lesson: L1=6, SEC2-R55=30, SEC2-R56=34, SEC2-R57=38, SEC2-R58=32, SEC2-R59=36, SEC2-R60=32, SEC2-R61=33
- NOTA: sonda inicial creó colección vacía "documentos_curso" (0 docs); eliminada de inmediato → estado exacto restaurado.

## H5P
- 7 videos mod_hvp (ids 21-27) curso 2
- mdl_hvp_xapi_results: 49 filas
- Por video: L1=13, L2=10, L3=5, L4=5, L5=10, L6=0, L7=6

## Manifest learning_signals (data/learning_signals/course_2_interactions.json)
- 29 interacciones: R55=5, R56..R61=4 c/u
- levels: needs_reinforcement, partial, ready

## Endpoints learning-signals (api/routes/learning_signals.py)
- GET /learning-signals/lesson/{lesson_id}/me
- GET /learning-signals/lesson/{lesson_id}/summary
- POST /learning-signals/sync/lesson/{lesson_id}
- POST /learning-signals/lesson/{lesson_id}/guidance (realtime, commit aba2ab8)

## Config tono/nivel ayuda (mdl_local_tesisai_lessons.metadata_json $.pedagogy)
Las 7 lecciones SEC2-R55..R61: tutor_tone=practico, help_level=orientar
(campos gestionados por services/pedagogy_profile.py: tutor_tone <-> metadata.pedagogy.tutor_tone, help_level <-> metadata.pedagogy.help_level)

## Rutas relevantes
- Backend: tesis-rag/services/learning_signals.py, tesis-rag/api/routes/learning_signals.py, tesis-rag/api/routes/chat.py, tesis-rag/services/pedagogy_profile.py, tesis-rag/services/context_service.py
- Frontend: frontend-tesis/src/shared/components/ai/H5PStudentSignal.jsx, H5PSignalsPanel.jsx, TutorPedagogyView.jsx, frontend-tesis/src/modules/academy/CourseContentView.jsx, frontend-tesis/src/shared/services/ragService.js
