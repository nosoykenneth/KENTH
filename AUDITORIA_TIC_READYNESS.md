# AUDITORÍA — Preparación para Trabajo de Integración Curricular (TIC)

**Proyecto:** TIC KENTH — Tutor IA local (RAG) para curso de *Mezcla y Masterización* en Moodle (ESPE)
**Referencia académica de madurez:** `T-ESPE-060286.pdf` (TIC "Prototipo de tutor virtual para entornos inmersivos 3D — Second Life"). Usado **solo** como vara de estructura y nivel de evidencia; no se copia tema ni implementación.
**Fecha de auditoría:** 2026-07-03
**Auditor:** revisión técnica sobre el **servidor desplegado real** (no repo local aislado).
**Naturaleza:** solo lectura / diagnóstico. **No** se hicieron cambios funcionales, merge, PR ni despliegues. No se ejecutaron operaciones destructivas (reindex/rebuild) ni escrituras reales de autoría.

> Todos los datos provienen de comandos ejecutados por SSH contra `kenneth@100.97.90.86:/srv/kenneth/tic-kenth` (host real `bodyguard26`, Ubuntu). Secretos (tokens, contraseñas, `KENTH_COURSE_ID_SECRET`, `MOODLE_WS_TOKEN`) se conocieron durante la auditoría pero **se redactan** en este documento.

---

## 1. Resumen ejecutivo

El sistema **desplegado está vivo, coherente y sin drift**: 9 contenedores arriba, commit `6b25712` (main, árbol limpio, == `origin/main`), y el código dentro del contenedor FastAPI es **byte-idéntico** al HEAD (sha256 verificado). El **tutor IA funciona end-to-end** por el gateway público con grounding real, guardrails de dominio, ruta de aclaración y trazabilidad persistida. La **seguridad por rol está bien enforced** (token Moodle obligatorio, bypass por `X-User-Id` cerrado, gates `require_rag_admin`/`require_course_admin`/`require_teacher` correctos; profesor sin edición bloqueado).

El sistema real es **más rico** que el TIC de referencia (RAG por secciones, roles por capabilities, editor docente/admin, transcripción automática, observabilidad Grafana/Loki).

Los **bloqueos para presentar como TIC** son de dos tipos:
1. **Cobertura del conocimiento (RAG):** el índice desplegado tiene **solo 24 chunks de 1 sola fuente** (transcripción de la lección `SEC2-R55`). Las otras 2 lecciones y 8 secciones no están indexadas → grounding materialmente incompleto para un piloto real.
2. **Paquete documental y evaluación académica:** faltan RF/RNF formales, diagramas (general, componentes, secuencia, ERD), casos de uso, tabla de endpoints, matriz de pruebas y, sobre todo, un **set de evaluación con métricas de precisión/grounding** (exigencia medible tipo OE4).

Defectos concretos hallados: `/moodle/me` responde **500** (bug de logging, causa raíz localizada), no existe endpoint `/health`, la suite `pytest` no está en la imagen de producción, y el **plugin Moodle `local_tesisai` + `api_persistente` + `tesis_role.php` están fuera del repo** (viven en `runtime/`, gitignored).

**Veredicto rápido:** Demo técnica **SÍ** · Piloto con estudiantes **PARCIAL** · Sustentación TIC **PARCIAL** · Producción institucional **NO**.

---

## 2. Alcance de la auditoría

| Incluido | Excluido / no verificable |
|---|---|
| Versión desplegada (git + contenedores + drift) | Recorrido de UI en navegador (SPA headless) |
| Arquitectura real (compose, nginx, volúmenes, env, Ollama) | Pruebas de carga/estrés y métricas cuantitativas de rendimiento |
| Moodle: curso, secciones, lecciones, recursos, H5P, roles, tokens | Restauración real de backups (solo se confirmó existencia) |
| RAG/Chroma: colección, chunks, metadata, validadores oficiales | Ejecución de `pytest` en servidor (no instalado en imagen prod) |
| Tutor IA E2E (6 casos) por el gateway con token real | Ejecución de rutas destructivas (reindex/rebuild) — evitadas por seguridad |
| Seguridad/roles (matriz de autorización, rechazos reales) | Escrituras reales de autoría (blocks/moments/pedagogy/ai-prepare) — evitadas |
| Persistencia de trazas (delta pre/post E2E) | Flujo profundo de logs en Loki/Grafana |

---

## 3. Versión desplegada auditada (reporte obligatorio)

| Ítem | Valor | Evidencia |
|---|---|---|
| **Commit server** | `6b25712c382e6ddf9e3adc18f7ba9333d5be0125` — *Merge PR #8 fix/ai-moments-timeline-coverage* (2026-07-02 21:19 -0500) | `git rev-parse HEAD` |
| **Branch server** | `main` | `git branch --show-current` |
| **Dirty state** | **NO** (árbol limpio) | `git status --porcelain` vacío |
| **Sync con origin** | `## main...origin/main` (sin ahead/behind) | `git status -sb` |
| **Remoto** | `git@github-kenneth:nosoykenneth/KENTH.git` | `git remote -v` |
| **Drift imagen↔código** | **Ninguno** — `service.py`/`prompts.py` sha256 idénticos repo vs contenedor; `diff` vacío | `sha256sum` + `docker exec` |
| **Local (snapshot sesión)** | `6b25712`, main, limpio → == server | contexto git de sesión |

**Contenedores activos y salud:**

| Servicio | Imagen | Estado | Puertos | Salud |
|---|---|---|---|---|
| tic-gateway | nginx:alpine | Up 19h | `0.0.0.0:8090→80` | `/`→200, `/api/lms/`→200 |
| tic-fastapi | tic-kenth/fastapi:latest | Up 22h | 8000/tcp | 50 rutas OK; `/chat` operativo |
| tic-frontend | tic-kenth/frontend:latest | Up 28h | (build compartido) | index + assets 200 |
| tic-moodle | tic-kenth/moodle:5.0-real | Up 28h | `8091→8080` | curso/WS OK |
| tic-mariadb | mariadb:11.4 | Up 4d | 3306/tcp | **healthy** |
| tic-moodle-cron | tic-kenth/moodle:5.0-real | Up 4d | — | cron 60s |
| tic-grafana | grafana/grafana:10.4.0 | Up 4d | `127.0.0.1:3000` | up |
| tic-loki | grafana/loki:2.9.0 | Up 4d | 3100 | up |
| tic-promtail | grafana/promtail:2.9.0 | Up 4d | — | up |

**Riesgos de desalineación:**
- 🟢 `main`: local == server == origin/main; sin drift imagen↔código.
- 🟡 3 ramas remotas obsoletas no traídas al server (`feat/ai-timed-moments-professor-timeline`, `feat/editor-recursos-ia-flow`, `fix/step3-action-bar-fullwidth`) — ya mergeadas; limpieza pendiente.
- 🔴 **`local_tesisai` (plugin Moodle) + `proyecto_curso/api_persistente` + `tesis_role.php` NO están en el repo `tic-kenth`** (solo un mirror SQL `tesis-rag/migrations/moodle/001_local_tesisai_operational.sql` y un doc de patch). Viven en `runtime/moodle/` (gitignored, solo servidor) → riesgo de reproducibilidad y de fuente de verdad.
- 🟢 Secretos **no** versionados (`.env`, `runtime/`, `_migration/` en `.gitignore`).

---

## 4. Arquitectura actual

### 4.1 Diagrama textual (SOA tras API Gateway)

```
                       Navegador (SPA React)
                               │  (mismo origen)
                               ▼
                  ┌──────────────────────────┐
                  │  tic-gateway (nginx)      │  :8090→80
                  │  rate-limit por Authorization / IP
                  └───────┬───────────┬──────┘
        /api/ai/* │       │ /api/lms/ /moodle/ /moodle_api/
        (timeout 300s chat│ (assets, sin rate-limit)
         600s authoring)  │
                          ▼                      ▼
          ┌──────────────────────┐      ┌──────────────────────┐
          │ tic-fastapi (LangGraph)│    │ tic-moodle (PHP 5.0)  │ :8091
          │  supervisor→ rag/web/  │◄───┤  local_tesisai + WS   │
          │  guardia/saludo/perdido│ WS │  api_persistente      │
          └───┬───────────┬────────┘    └──────────┬───────────┘
      Chroma  │           │ Ollama (host)          │ SQL
   /app/bd_vectorial      │ host.docker.internal   ▼
   (bind runtime/chroma)  │ :11434 (NATIVO, GPU)   tic-mariadb :3306
                          │                        (bind runtime/mariadb)
                    llama3.1:8b (chat)             + tic-moodle-cron
                    nomic-embed-text (embed)
                    qwen3:14b (ai-prepare)
                    qwen3-vl:4b (visión)
                    deepseek-r1:32b (quality=max)

   Observabilidad: nginx JSON logs → promtail → loki → grafana (127.0.0.1:3000)
```

### 4.2 Tabla de componentes

| Componente | Tecnología | Responsabilidad | Puerto | Dependencia | Estado | Evidencia |
|---|---|---|---|---|---|---|
| Gateway | nginx:alpine | Entrada pública única, ruteo `/api/ai`→FastAPI, `/api/lms`→Moodle, rate-limit, timeouts | 8090→80 | fastapi, moodle, frontend_build | ✅ | `nginx.full.conf`, `/`→200 |
| Frontend | React (Vite build) | SPA (estudiante + editor docente/admin) | (build en volumen) | — | ✅ sirviendo | `index.html`+`/assets/*.js`→200 |
| FastAPI/IA | Python 3.11, LangGraph | Tutor RAG, autoría, proxy Moodle, contexto | 8000 | Ollama, MariaDB, Moodle WS, Chroma | ✅ 50 rutas | openapi 50 paths |
| Moodle | PHP 5.0-real + plugin `local_tesisai` | LMS, curso, H5P, WS, roles/capabilities | 8091→8080 | MariaDB | ✅ | curso 2 + WS 200 |
| MariaDB | mariadb:11.4 | Persistencia operativa (Moodle + `mdl_local_tesisai_*`) | 3306 | — | ✅ healthy | `docker ps` healthy |
| moodle-cron | mismo img Moodle | Cron Moodle (H5P, tareas) cada 60s | — | Moodle | ✅ | compose |
| Chroma | chromadb (persistente) | Índice vectorial RAG | archivo | FastAPI | ⚠️ escaso (24 chunks) | `chroma.sqlite3`, validadores |
| Ollama | nativo host (GPU) | Modelos LLM/embeddings/visión | 11434 | — | ✅ 13 modelos | `/api/tags` |
| Observabilidad | Loki/Promtail/Grafana | Logs centralizados | 3000 (local) | — | ✅ up | `docker ps` |

**Persistencia real (bind-mounts en `./runtime/`):** `runtime/mariadb` (DB), `runtime/moodle` (webroot Moodle **incl. plugin**), `runtime/moodledata` (media, ro para FastAPI), `runtime/chroma` (índice), `runtime/fastapi-chat` (SQLite dev), `runtime/whisper-cache` (modelo Whisper). Volúmenes nombrados: `frontend_build`, `loki_data`, `grafana_data`.

**Backups (existen):** `/srv/kenneth/backups/` → `moodle-db-20260629.sql.gz` (2.2MB), `moodledata-20260629.tar` (702MB), `rag-migration-20260630/`, `tesis_role.php.bak.*`, `backup.log` (act. 2026-07-03). `tic-kenth-backups/pre-align-20260629/`. ⚠️ Snapshot DB/moodledata es del **29-jun** (no fresco); restauración **no probada**.

### 4.3 Comparación con arquitectura defendible para tesis

| Criterio | Estado | Nota |
|---|---|---|
| Separación de responsabilidades | ✅ Fuerte | SOA por gateway; el front solo llama 2 prefijos |
| Modularidad | ✅ | Servicios independientes, dominio en Domain Pack |
| Persistencia | ✅ | Moodle-first (`mdl_local_tesisai_*`) + Chroma; binds versionables |
| Recuperación semántica | ⚠️ | Motor correcto (scope-aware, sin `axis_id`), **corpus escaso** |
| Seguridad | ✅ | Token obligatorio, gates por capability, secretos fuera de repo |
| Trazabilidad | ✅ | `interaction_traces` por request (verificado +6) + logs JSON→Loki |
| Despliegue reproducible | ⚠️ | `docker compose` reproducible, pero plugin Moodle/api_persistente **fuera del repo** |

---

## 5. Estado por componente (síntesis)

- **Gateway:** ✅ operativo, rutas y rate-limit correctos. Falta: nada crítico.
- **Frontend:** ✅ servido. Pendiente: verificación en navegador; posible asset roto `/src/assets/logo_recortado.svg` (ruta dev).
- **FastAPI/IA:** ✅ 50 rutas; tutor E2E OK. Bugs: `/moodle/me` 500; sin `/health`.
- **Moodle:** ✅ curso 2 + 9 secciones + 3 H5P + roles + WS. Riesgo: plugin fuera de repo.
- **MariaDB:** ✅ healthy, datos poblados.
- **Chroma/RAG:** ⚠️ limpio pero 24 chunks / 1 fuente.
- **Ollama:** ✅ todos los modelos del `.env` presentes.
- **Observabilidad:** ✅ up (flujo de logs no auditado en profundidad).

---

## 6. Matriz comparativa contra el PDF de referencia

| Criterio del PDF | Exigencia académica | En este proyecto | Estado | Evidencia |
|---|---|---|---|---|
| Objetivo general / OE | Medibles, encadenados | Existen como sistema; falta redacción formal | ⚠️ Parcial | — |
| Requisitos funcionales | Fichas RF (in/out/prioridad) | Implementados (chat/RAG/roles/editor/transcripción/trazas); no documentados | ❌ Doc ausente | 50 rutas |
| Requisitos no funcionales | Tabla RNF | Seguridad/observabilidad verificadas; doc ausente | ⚠️ Parcial | matriz §8 |
| Arquitectura | Distribuida + justificación | SOA gateway verificada en runtime | ✅ Impl / ❌ diagrama | §4 |
| Componentes | Responsabilidad + mecanismos | 9 servicios activos | ✅ Impl / ❌ diagrama | `docker ps` |
| Diagramas (gral/comp/**secuencia**/ERD) | 4 vistas | Textual en §4; formales ausentes | ❌ | — |
| Casos de uso | CU con flujos alternos | No documentados | ❌ | — |
| Modelo de datos (ERD) | ERD + tabla entidades | 13 tablas `mdl_local_tesisai_*` reales | ⚠️ esquema sí / ERD no | §7 |
| Endpoints | Inventario tabular | 50 rutas reales | ✅ datos / ❌ tabla doc | openapi |
| Desarrollo/Sprints | Metodología + hitos | Reconstruible de PRs #4–#8 | ⚠️ Parcial | git log |
| Pruebas funcionales/integración/**E2E** | Matriz con resultados | Ejecutadas en esta auditoría (E2E + seguridad) | ⚠️ hechas / ❌ doc formal | §9,§10 |
| Criterios de aceptación | Explícitos | Aplicados aquí ad-hoc; no formalizados | ⚠️ | §10 |
| Conclusiones/Futuros | Ligados a objetivos | Pendiente redacción | ❌ | — |

---

## 7. Matriz de funcionalidades (Moodle + curso)

| Funcionalidad | Estado | Evidencia | Riesgo | Pendiente |
|---|---|---|---|---|
| Moodle carga | ✅ | `/api/lms/`→200; WS POST 200 | — | — |
| Curso existe | ✅ | `mdl_course` id=2 "Mezcla y Masterización", visible | — | — |
| Secciones | ✅ | 9 secciones en curso 2 | — | — |
| Lecciones | ✅ | 3: `SEC2-R55/56/57` (ancladas a `cmid`) | — | — |
| Bloques | ✅ | 14 en `lesson_blocks` | — | — |
| Prompts | ✅ | 14 en `lesson_prompts` | — | — |
| Recursos | ✅ | 25 en `course_resources` | — | — |
| H5P/video | ✅ | 3 módulos `hvp` en curso 2; auto-enlazados a lecciones | — | — |
| Transcripción | ✅ | 144 `transcript_segments`; tutor cita transcripción | — | — |
| Trazas | ✅ | `interaction_traces` 847→853 tras E2E | — | — |
| Roles/capabilities | ✅ | editingteacher/teacher/manager/student en curso 2; gates OK | — | — |
| Estudiante accede al tutor | ✅ | E2E con token `estudiante`→200 grounded | — | — |
| Profesor → panel docente | ✅ (backend) | `require_teacher` autoriza editingteacher (moments 404 lección ficticia) | UI no verificada en navegador | Smoke UI |
| Admin → editor avanzado | ✅ (backend) | gates admin OK | UI no verificada | Smoke UI |
| Diagnóstico técnico/siteadmin | ⚠️ | No hay `/health` ni panel de diagnóstico de app | — | Añadir `/health` |
| Estudiante NO edita | ✅ | estudiante→403 en blocks/moments/ai-prepare/rebuild | — | — |
| `documents` (tabla) | ⚠️ | 0 filas (índice se nutre de transcripción) | — | Confirmar diseño |

---

## 8. Matriz de roles / permisos (verificada en runtime)

| Endpoint | Método | No-token | Estudiante | Teacher (no edit) | EditingTeacher | Manager/RAG-admin | Guard (código) |
|---|---|---|---|---|---|---|---|
| `/api/ai/chat` | POST | **401** | 200 | 200 | 200 | 200 | token Moodle obligatorio |
| `/api/ai/chat` + `X-User-Id` sin token | POST | **401** | — | — | — | — | bypass cerrado ✅ |
| `/moodle/me` | GET | 401 | **500** | 500 | 500 | 500 | bug (ver §11) |
| `/sections/lessons/all` | GET | **401** | 422* | — | 422* | — | `require_course_view` (*falta course_id firmado) |
| `/documents/rebuild` | POST | **401** | **403** | **403** | (no probado) | `require_rag_admin` | destructivo — positivo no ejecutado |
| `/authoring/documents/reindex` | POST | (código) | — | — | — | `require_course_admin` | "profesor editor NO reindexa" |
| `/authoring/.../blocks` | PUT | **401** | **403** | **403** | 404** | — | `require_teacher` (**404=autorizado, lección ficticia) |
| `/authoring/.../moments` | PUT | — | **403** | — | 404** | — | `require_teacher` |
| `/authoring/.../ai-prepare` | POST | **401** | **403** | — | (no ejecutado) | — | `require_teacher` |

**Conclusión seguridad:** enforcement por rol correcto en todos los casos probados; sin bypass. Único hallazgo abierto es funcional (`/moodle/me` 500), no de autorización.

---

## 9. Matriz RAG / Tutor (verificada)

| Ítem | Resultado | Evidencia |
|---|---|---|
| FastAPI responde | ✅ | 50 rutas; `/chat` 200 |
| Ollama responde | ✅ | `/api/tags` 13 modelos |
| Modelo chat | `llama3.1:8b` (`KENTH_TEXT_MODEL`) | env |
| Modelo embeddings | `nomic-embed-text` (`KENTH_EMBED_MODEL`) | env |
| Chroma existe / colección | ✅ `langchain` | `PersistentClient` |
| **Chunks totales** | **24** | `col.count()`, `verify_rag_index_clean` |
| **Fuentes únicas** | **1** (transcripción `SEC2-R55`) | validadores |
| Chunks por sección | Sección 1 (SECCIÓN 0): 24; resto: **0** | metadata |
| Chunks globales (`is_global`) | 0 en muestra | metadata |
| Ausencia de `axis_id` / `scope=axis` | ✅ 0 | metadata (código migrado) |
| Metadata course/section/lesson/block | ✅ presente | `course_id`,`section_id`,`lesson_id`,`block_id`,`moodle_section_id`,`section_number` |
| `retrieval_scope` / `retrieval_fallback` | ✅ expuestos (`lesson`/`false`) | respuesta `/chat` |
| Validador oficial índice | ✅ "Índice coherente" | `validate_rag_index.py` |
| Guardrail fuera de dominio | ✅ `out_of_domain:semantic`, `ruta:bloqueo` | E2E C3 |
| Respuesta dentro de lección | ✅ grounded, `evidence:alto`, 4 fuentes | E2E probe/C5 |
| Trazas guardadas | ✅ (`interaction_traces` +6) | delta DB |

**E2E ejecutados (usuario `estudiante`, curso 2, gateway):**

| # | Pregunta | course/section/lesson | scope | fallback | evidencia | respuesta | traza | veredicto |
|---|---|---|---|---|---|---|---|---|
| P | sistema de decisión | 2 / — / R55 | lesson | no | alto | 5 pasos, grounded | sí | ✅ |
| C2 | sidechain (otra sección) | 2 / — / R55 | lesson | no | alto | rehúsa "fuera del contexto" | sí | ✅ no alucina (fallback no ejercitable: 1 sola lección) |
| C3 | derivada/integral (fuera dominio) | 2 / — / R55 | — | no | bajo | bloqueo out_of_domain | sí | ✅ |
| C4 | "y eso cómo se hace?" (ambigua) | 2 / — / — | — | no | bajo | pide precisión | sí | ✅ |
| C5 | transcripción específica | 2 / — / R55 | lesson | no | alto | "escuchar con las manos quietas" | sí | ✅ |
| C6 | volumen vs ganancia (R57, no indexada) | 2 / — / R57 | lesson | no | alto | responde plausible | sí | ⚠️ grounding probable vía metadata inyectada (R57 sin chunks) — revisar |

> **Nota crítica:** El motor RAG (routing, scope-affinity, verificación post-generación, guardrails, trazas) está **maduro y bien construido**. El límite es de **datos**: el índice cubre 1 lección. El fallback inter-sección no puede demostrarse porque no hay otra fuente indexada.

`pytest`: **no ejecutable en el contenedor de producción** ("No module named pytest"). La suite existe en el repo (`tesis-rag/tests/`) y requiere entorno de desarrollo. `scripts/validate_rag_index.py` y `verify_rag_index_clean.py` sí corren y pasan.

---

## 10. Matriz académica TIC (clasificación)

| Requisito académico | Clasificación | Nota |
|---|---|---|
| RF curso Moodle | Parcial | implementado; sin RF formal |
| RF tutor IA | Parcial | implementado + E2E; sin RF formal |
| RF retroalimentación personalizada | Parcial | contextual por lección; personalización por progreso limitada |
| RF roles | Parcial | implementado+verificado; sin RF formal |
| RF recursos | Parcial | 25 recursos; sin RF formal |
| RF transcripción | Parcial | funcional (144 segs); sin RF formal |
| RF trazabilidad | Parcial | verificado; sin RF formal |
| RF evaluación | **Ausente** | sin set de evaluación/rúbrica |
| RNF seguridad | Parcial | verificado; sin doc |
| RNF mantenibilidad | Parcial | SOA modular; sin doc |
| RNF disponibilidad | Parcial | sin `/health`; observabilidad sí |
| RNF privacidad | Parcial | secretos fuera de repo; sin doc |
| RNF rendimiento | **Ausente** | sin pruebas de carga (tiempos anecdóticos: chat 0.2–6.8s) |
| RNF despliegue local | Completo | `docker compose` + Ollama nativo reproducible |
| Diagrama general | Ausente (formal) | textual en §4 |
| Diagrama componentes | Ausente (formal) | textual en §4 |
| Flujo estudiante→tutor→RAG→respuesta | Parcial | demostrado E2E; sin diagrama secuencia |
| ERD | Parcial | 13 tablas reales; sin diagrama |
| Endpoints | Parcial | 50 rutas; sin tabla doc |
| Sprints/decisiones | Parcial | git history |
| Integración Moodle/Ollama/RAG/roles/editor | Completo (impl) | verificado runtime |
| Matriz de pruebas | Parcial | esta auditoría |
| Casos E2E | Parcial | ejecutados aquí |
| Pruebas de seguridad/roles | Parcial | ejecutadas aquí |
| Pruebas RAG | Parcial | validadores + E2E |
| Pruebas usabilidad/estudiantes | **Ausente** | — |
| Métricas de precisión de respuestas | **Ausente** | crítico para OE medible |
| Encuesta Likert | **Ausente** | — |
| Rúbrica de aprendizaje | **Ausente** | — |

---

## 11. Defectos / bugs verificados

| ID | Severidad | Descripción | Evidencia | Impacto |
|---|---|---|---|---|
| B1 | 🟠 Media | `/moodle/me` → **500**. La WS a Moodle devuelve 200, pero `services/moodle_ws_client.py:100` llama `logger.error(...)` con clave `message` que colisiona con `LogRecord` → `KeyError: "Attempt to overwrite 'message'"`. Un error WS manejable se vuelve 500 no controlado. | `docker logs tic-fastapi` (traceback) | Frontend no obtiene perfil; **no** afecta autorización (gates independientes) |
| B2 | 🟡 Baja-Media | No existe endpoint `/health` en FastAPI (404). | openapi (50 rutas, sin health) | Falta RNF disponibilidad / CU salud (que el PDF sí exige) |
| B3 | 🟡 Baja | `/sections/lessons/all` → **422** con token (espera `X-Course-Id` firmado). | matriz §8 | Contrato poco tolerante; posible fricción de integración |
| B4 | 🔴 Alta (reproducibilidad) | Plugin `local_tesisai` + `api_persistente` + `tesis_role.php` fuera del repo `tic-kenth` (viven en `runtime/`, gitignored). | `git ls-files` | Fuente de verdad no versionada; difícil reconstruir |
| B5 | ⚪ Info | `pytest` ausente en imagen prod → suite no ejecutable en contenedor. | `python -m pytest`→"No module named pytest" | Tests solo en dev |
| B6 | ⚪ Info | Posible asset roto `/src/assets/logo_recortado.svg` (ruta dev en build). | `curl /` | Cosmético |
| B7 | 🟡 Media (contenido) | Índice RAG con 24 chunks / 1 lección; 2 lecciones y 8 secciones sin indexar. | validadores | Grounding incompleto para piloto |
| B8 | ⚪ Info | Tabla `mdl_local_tesisai_axes` con 8 filas (residual de migración eje→sección). | count DB | Deuda técnica esquema (Capa 4 diferida) |

---

## 12. Veredicto de preparación (4 niveles)

### 12.1 Demo técnica — **SÍ**
- **Evidencia:** 9 servicios up; tutor E2E grounded (HTTP 200, 0.2–6.8s); guardrails y aclaración OK; seguridad por rol enforced; trazas persistidas.
- **Bloqueos:** ninguno crítico.
- **Acciones mínimas:** (opcional) arreglar `/moodle/me` para que la UI muestre el perfil.

### 12.2 Piloto con estudiantes — **PARCIAL**
- **Evidencia:** flujo estudiante real funciona; curso/roles/H5P poblados.
- **Bloqueos:** B7 (RAG cubre 1 lección → las otras responderán "fuera de contexto"); B1 (`/moodle/me` 500 puede degradar UI); sin métricas para medir el piloto.
- **Acciones mínimas:** reindexar el corpus completo del curso (3 lecciones / secciones con contenido); fix B1; smoke test por lección; instrumentar recolección de resultados.

### 12.3 Sustentación como TIC — **PARCIAL**
- **Evidencia:** arquitectura e implementación defendibles y superiores al TIC de referencia; seguridad y trazabilidad demostrables.
- **Bloqueos:** paquete documental (RF/RNF/CU/ERD/diagramas/tabla endpoints/matriz de pruebas) + **set de evaluación con métricas de precisión/grounding** (exigencia medible); versionar el plugin (B4).
- **Acciones mínimas:** ver Plan §13 (bloqueantes).

### 12.4 Producción institucional — **NO**
- **Bloqueos:** cobertura RAG; sin `/health`; sin pruebas de carga/hardening; backups no restaurados-verificados y no frescos; sin HTTPS/dominio; gestión de secretos formal; plugin fuera de repo.

### 12.5 Porcentajes aproximados (justificados por evidencia)

| Dimensión | % | Base |
|---|---|---|
| Arquitectura | **90%** | SOA verificada, sin drift, observabilidad |
| Implementación | **85%** | 50 rutas, tutor+editor+transcripción funcionando |
| Seguridad | **80%** | gates correctos; falta hardening/HTTPS y fix B1 |
| UX | **60%** | backend enforce OK; sin verificación navegador; B1/B6 |
| RAG/Tutor | **65%** | motor maduro; corpus escaso (B7) |
| Documentación | **20%** | casi todo el paquete TIC pendiente |
| Pruebas | **40%** | E2E+seguridad hechas hoy; falta formalización, usabilidad, carga |
| Evaluación académica | **10%** | sin set de evaluación/métricas/Likert/rúbrica |
| Despliegue | **90%** | compose reproducible; falta versionar plugin |

---

## 13. Plan mínimo de cierre

> Prioriza **cerrar evidencia**, no añadir features. Tiempos estimados orientativos.

### Bloqueantes (para sustentar el TIC)
| Acción | Prioridad | Evidencia necesaria | Tiempo | Responsable |
|---|---|---|---|---|
| Reindexar corpus completo del curso 2 (3 lecciones + secciones con contenido) | Bloqueante | `validate_rag_index` con N>>24 chunks y cobertura por sección | 0.5–1 día | Dev + Profe (contenido) |
| Definir y ejecutar **set de evaluación** (batería de preguntas con respuesta esperada) + métricas de precisión/grounding | Bloqueante | Tabla de resultados (aciertos, grounding, no-alucinación) | 2–3 días | Dev + Tutor tesis |
| Producir paquete documental: RF/RNF, diagramas (general, componentes, **secuencia**, ERD), casos de uso, tabla de endpoints, matriz de pruebas | Bloqueante | Capítulos III–V del documento | 3–5 días | Autor |

### Importantes
| Acción | Prioridad | Evidencia | Tiempo | Responsable |
|---|---|---|---|---|
| Fix B1 `/moodle/me` (logging KeyError + capacidad WS) | Importante | `/moodle/me`→200 con perfil por rol | 0.5 día | Dev |
| Añadir `/health` a FastAPI (RNF disponibilidad) | Importante | `/api/ai/health`→200 | 0.25 día | Dev |
| Versionar plugin `local_tesisai` + `api_persistente` + `tesis_role.php` | Importante | archivos en git | 0.5 día | Dev |
| Pruebas de roles/usabilidad con estudiantes + encuesta Likert | Importante | resultados + encuestas | 2–3 días | Autor |

### Deseables
| Acción | Prioridad | Evidencia | Tiempo | Responsable |
|---|---|---|---|---|
| Resolver B3 `/sections/lessons/all` 422 (contrato course_id) | Deseable | 200 con token | 0.5 día | Dev |
| Limpiar tabla `axes` residual (B8) y ramas remotas obsoletas | Deseable | count 0 / ramas borradas | 0.25 día | Dev |
| Revisar asset B6 `logo_recortado.svg` | Deseable | asset 200 | 0.1 día | Dev |

### Post-tesis
| Acción | Evidencia | 
|---|---|
| HTTPS + dominio (moodle.DOMINIO / subdominio SPA) | cert + wwwroot coherente |
| Pruebas de carga/escalabilidad y hardening | métricas p95, límites |
| Test de restauración de backups (frescura diaria) | restore verificado |
| Multi-curso | segundo curso indexado |

---

## 14. Definition of Done — checklist de esta auditoría

- [x] Auditado el **servidor real** (no repo local aislado) — SSH a `bodyguard26`.
- [x] Identificado **commit desplegado** (`6b25712`, main, limpio, sin drift).
- [x] Comparado contra el **PDF** de referencia (§6, §10).
- [x] Probado **frontend** (200 + assets), **backend** (50 rutas, E2E), **RAG** (validadores + 6 casos E2E).
- [x] Revisada **seguridad** (matriz de roles, bypass cerrado, gates).
- [x] Generado **veredicto** de presentación (4 niveles + %).
- [x] Creado **`AUDITORIA_TIC_READYNESS.md`**.

> Auditoría de solo lectura. No se realizaron cambios funcionales, merges, PRs ni despliegues.
