# Validacion de chat

## Estado
Bloqueada parcialmente: no hubo `MOODLE_TOKEN` utilizable para ejecutar las 10 preguntas por gateway real como estudiante. El smoke autenticado quedo omitido por el propio script de produccion.

## Validado sin token
- `/api/ai/chat` sin token devuelve 401.
- Smoke produccion sin auth: 9 PASS, 0 FAIL.
- Health post-cleanup: `status=ok`, `chroma_chunks=233`.
- Contrato frontend `test:chat-sources`: PASS; las fuentes con `visible_to_student=false` se ocultan al alumno.

## Casos requeridos no ejecutados
- Pregunta 0.1 conceptual: NO EJECUTADA por falta de token estudiante utilizable.
- Pregunta 0.1 procedural: NO EJECUTADA por falta de token estudiante utilizable.
- Pregunta 0.2 conceptual: NO EJECUTADA por falta de token estudiante utilizable.
- Pregunta 0.2 Fletcher-Munson / ISO 226: NO EJECUTADA por falta de token estudiante utilizable.
- Pregunta nivel seccion: NO EJECUTADA por falta de token estudiante utilizable.
- Pregunta sobre 0.3-0.7: NO EJECUTADA por falta de token estudiante utilizable.
- Pregunta fuera de dominio: NO EJECUTADA por falta de token estudiante utilizable.
- Pregunta ambigua: NO EJECUTADA por falta de token estudiante utilizable.
- Pregunta que use guia interna sin mostrarla como fuente: NO EJECUTADA por falta de token estudiante utilizable.
- Pregunta que antes recuperaba archivo borrado: NO EJECUTADA por falta de token estudiante utilizable.

## Veredicto
No se declara validacion pedagogica E2E completa. El indice esta tecnicamente limpio, pero falta correr bateria de chat autenticada con token de estudiante.
