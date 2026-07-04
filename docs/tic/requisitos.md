# Requisitos del sistema — TIC KENTH

Requisitos funcionales (RF) y no funcionales (RNF) del tutor IA contextual para el
curso de *Mezcla y Masterización* (ESPE). Cada ficha incluye prioridad, descripción,
criterio de aceptación y evidencia actual (verificada en la auditoría del servidor
desplegado, `AUDITORIA_TIC_READYNESS.md`, commit `6b25712`).

**Prioridad:** `Alta` = imprescindible para el piloto · `Media` = esperado ·
`Baja` = deseable.
**Estado evidencia:** ✅ verificado · ⚠️ parcial · ⛔ pendiente.

---

## 1. Requisitos funcionales (RF)

| ID | Requisito | Prio | Criterio de aceptación | Evidencia |
|---|---|---|---|---|
| **RF-01** | **Curso en Moodle**: el sistema opera sobre un curso Moodle real (id canónico numérico). | Alta | Existe el curso, con secciones y matrículas; el `course_id` se resuelve/valida (firmado HMAC). | ✅ curso id=2, 9 secciones, roles poblados |
| **RF-02** | **Lecciones/secciones**: estructura de lecciones anclada al `cmid` de Moodle, agrupada por sección. | Alta | CRUD de lecciones (autoría) y lectura por estudiante; reordenar no intercambia metadata. | ✅ 3 lecciones (SEC2-R55/56/57), 14 bloques |
| **RF-03** | **Tutor IA (chat)**: el estudiante conversa con un tutor por lección. | Alta | `POST /chat` con token → respuesta en español, con traza; sin token → 401. | ✅ E2E 6/6, `/chat` 200 grounded |
| **RF-04** | **RAG contextual**: la respuesta se fundamenta en el corpus recuperado, filtrado por curso/sección/lección. | Alta | La respuesta expone `retrieval_scope`/`fuentes`; sin evidencia responde “fuera de contexto”, no inventa. | ✅ scope-aware; ⚠️ corpus escaso (24 chunks/1 lección) |
| **RF-05** | **Retroalimentación contextual**: el tutor usa el contexto de actividad (lección/sección/bloque activo) inyectado, sin contaminar la búsqueda. | Media | El contexto (Capa 2) se inyecta en el prompt pero **no** en la query de retrieval. | ✅ `context_service` (inject vs index) |
| **RF-06** | **Roles/permisos**: estudiante, profesor (editor), profesor sin edición, gestor, técnico RAG. | Alta | Cada acción exige la capability correcta (WS `get_permissions`), con fallback por rol. | ✅ matriz de roles verificada |
| **RF-07** | **Recursos por lección**: subir/enlazar recursos con flags `allowed_for_indexing` y `visible_to_student`. | Media | Recurso indexado-pero-no-visible: el tutor usa el texto pero no muestra el archivo. | ✅ 25 recursos; flags aplicados |
| **RF-08** | **Transcripción**: transcripción automática (Whisper) del vídeo H5P + edición manual por segmentos. | Media | `POST …/transcript/auto` genera segmentos; `PUT …/transcript` los corrige. | ✅ 144 `transcript_segments` |
| **RF-09** | **Preparar tutor con IA**: asistente que genera un borrador pedagógico (momentos con tiempos/tipo, bienvenida, preguntas sugeridas) desde la transcripción. | Media | `POST …/ai-prepare` produce borrador aislado en `metadata.ai_prepare`; `…/accept` lo promueve. NO reindexa. | ✅ probado en server (35 s draft / 263 s max) |
| **RF-10** | **Trazabilidad**: cada interacción del tutor se persiste (traza + logs). | Alta | `interaction_traces` +1 por request; log JSON por request. | ✅ traza +6 tras E2E |
| **RF-11** | **Bloqueo fuera de dominio**: preguntas ajenas al dominio se rechazan sin alucinar. | Alta | Pregunta fuera de dominio → `out_of_domain`, ruta `bloqueo`; sin fuga de internos. | ✅ E2E C3 |
| RF-12 | **Sesiones de chat**: historial de conversación por usuario recuperable. | Media | `chat-sessions` CRUD por token; un usuario no ve sesiones de otro. | ✅ endpoints + guard por token |
| RF-13 | **Salud del servicio**: endpoint de disponibilidad de la app y sus dependencias. | Media | `GET /api/ai/health` → 200 con estado de BD/WS/Chroma/Ollama/modelos, sin secretos. | ✅ añadido en esta rama (B2) |
| RF-14 | **Perfil del usuario**: identidad + capabilities del usuario autenticado. | Baja | `GET /api/ai/moodle/me` → 200 con `user_id`/`profile`/`capabilities`; error controlado si WS falla. | ✅ corregido en esta rama (B1) |

---

## 2. Requisitos no funcionales (RNF)

| ID | Requisito | Prio | Criterio de aceptación | Evidencia |
|---|---|---|---|---|
| **RNF-01 Seguridad** | Autenticación por token Moodle obligatoria; autorización por capabilities. | Alta | Sin token → 401; sin capability → 403; bypass `X-User-Id` cerrado en prod. | ✅ verificado (§8 auditoría) |
| **RNF-02 Disponibilidad** | El sistema expone su estado y se recupera de reinicios (restart policies). | Media | `/health` responde; contenedores `restart: unless-stopped`. | ✅ `/health` + compose |
| **RNF-03 Mantenibilidad** | Código modular por servicios; dominio en datos (Domain Pack), no cableado. | Media | Cambiar el dominio no requiere tocar el agente; pruebas automatizadas. | ✅ `domain_packs/<id>.json`; suite pytest |
| **RNF-04 Modularidad / SOA** | Arquitectura tras API Gateway; el front sólo llama 2 prefijos. | Alta | Servicios independientes; paridad dev/prod garantizada por el gateway. | ✅ SOA verificada |
| **RNF-05 Privacidad** | Secretos fuera del repo; datos sensibles (pagos, logs) no versionados. | Alta | `.env`, logs y transacciones en `.gitignore`; secretos redactados al versionar Moodle. | ✅ auditado (Fase 2.4) |
| **RNF-06 Rendimiento** | Latencia de chat aceptable para uso interactivo. | Media | Tiempos de chat p50 razonables (anecdótico 0.2–6.8 s). | ⚠️ sin prueba de carga formal |
| **RNF-07 Despliegue local** | Reproducible con `docker compose` + Ollama nativo. | Alta | `up -d --build` levanta todo el stack; documentado. | ✅ `DEPLOY_PRODUCCION.md` |
| **RNF-08 Observabilidad** | Logs centralizados y consultables. | Media | Logs JSON → Promtail → Loki → Grafana. | ✅ stack de logging up |
| RNF-09 Reproducibilidad | Componentes fuera del webroot versionados sin secretos. | Alta | `local_tesisai`, `api_persistente`, `tesis_role.php` en `moodle/`. | ✅ esta rama (B4) |
| RNF-10 Trazabilidad técnica | Cada request identificable (request_id) y auditable. | Media | `X-Request-ID` propagado; traza por interacción. | ✅ middleware + traces |

---

## 3. Requisitos pendientes por corpus/evaluación (fuera de esta rama)

| ID | Requisito | Bloqueado por |
|---|---|---|
| RF-EVAL | **Set de evaluación** con métricas de precisión/grounding/no-alucinación. | Corpus definitivo indexado + batería validada (ver `evaluacion_tutor.md`) |
| RF-COBERTURA | Cobertura RAG de **todas** las lecciones/secciones del curso. | Reindexación del corpus completo (destructiva; diferida) |
| RNF-CARGA | Pruebas de carga/estrés y p95. | Entorno de pruebas + instrumentación |
| RNF-HTTPS | HTTPS + dominio institucional. | Infra post-tesis |
