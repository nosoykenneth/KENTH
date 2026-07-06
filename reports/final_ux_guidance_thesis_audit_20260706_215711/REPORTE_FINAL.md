# REPORTE FINAL — Cierre funcional y documental (final_ux_guidance_thesis_audit)

- **Fecha**: 2026-07-06/07 (UTC)
- **Rama de trabajo**: `feat/final-ux-guidance-and-thesis-audit` → **PR #19 MERGEADO**
- **main desplegado**: `df4ef05` (merge de `812c5cb`)
- **Servidor**: `/srv/kenneth/tic-kenth` (bodyguard26), compose `docker-compose.deploy.yml`
- **Pre-state**: `PRE_STATE.md` (misma carpeta)

---

## 1. Cambios implementados

### FASE 1 — La guía del tutor ya no se pierde (recuperable)
- Nuevo módulo puro `frontend-tesis/src/shared/utils/guidanceStore.js`:
  persistencia del `pending_guidance` por **curso+lección** en localStorage con
  `{id, message, created_at, notified_at, seen_at}`; expiración 7 días; formato
  legado (solo id) tratado como visto.
- `CourseContentView.jsx`: `deliverGuidance` reescrito sobre el store
  (antes marcaba "entregado" ANTES de que el alumno viera el mensaje y solo
  guardaba el id → el mensaje moría con una recarga). Ahora: chat abierto =
  insertar+marcar visto; chat cerrado = badge/flecha + sonido solo la primera
  vez; recarga = badge restaurado sin sonido; `verGuiaDelTutor()` reinserta o
  enfoca desde el store aunque ya haya sido vista.
- `H5PStudentSignal.jsx`: el badge "Conviene reforzar · el tutor tiene una
  guía" ahora es **botón** con la acción explícita "Ver guía".
- `TutorAssistCard.jsx`: si la guía ya está en el historial, hace scroll hasta
  ella (nunca duplica; dedupe por `proactiveId`).

### FASE 2 — Orientación multi-concepto priorizada
- `learning_signals.get_lesson_signals`: `weak_concepts` ordenados por **menor
  acierto por concepto** (empate → orden pedagógico del video); expone
  score/max por concepto; `recommended_review` sigue ese orden (tope 3).
- `build_guidance_message`: 1 débil = concepto+minuto+recurso+micro-práctica;
  2 débiles = ambos numerados + orden recomendado (partial los conecta);
  3+ = "Prioridad 1/2/3" + ruta corta, sin saturar; ready = sin alerta (sólo
  sugerencia suave si hubo fallo puntual); needs = guiado sin reto avanzado.
- `render_signals_block`: inyecta las mismas prioridades al chat del tutor.
- Nunca menciona internos (xAPI/Chroma/JSON/chunks/backend) — testeado.

### FASE 3 — Tono / nivel de ayuda operativos
- Hallazgo: se inyectaba solo la palabra cruda ("practico") → efecto marginal.
- `pedagogy_profile.py`: `TONE_DIRECTIVES` / `HELP_DIRECTIVES` para TODAS las
  opciones reales de la UI (directo/paciente/exigente/socratico/practico;
  orientar/explicar/corregir/preguntar/ejemplo_guiado).
- `context_service.py`: inyecta "COMO APLICAR EL TONO/NIVEL DE AYUDA" + regla
  dura: el comportamiento nunca omite minuto/recurso ni altera la verdad.
- La guidance determinística cierra según `help_level` de la lección.
- Tabla completa: `FASE3_AUDITORIA_TONO_AYUDA.md` (misma carpeta).

### FASE 4 — Chat general neutral
- `chat.py`: guard determinista — pregunta personal de progreso
  (`is_personal_progress_question`, deliberadamente estrecho) **sin lección
  activa** → respuesta neutral fija (`personal_progress_no_lesson`), sin
  invocar al agente ni inventar señales. El chat de lección no cambia.

### FASE 5-6 — Documentación
- `docs/tic/diagramas.md`: +5 diagramas Mermaid (§7 teacher-driven RAG,
  §8 señales H5P, §9 contexto del tutor, §10 estados, §11 secuencia defensa).
- Nuevos: `ARQUITECTURA_GENERAL.md`, `TEACHER_DRIVEN_RAG.md`,
  `H5P_LEARNING_SIGNALS.md`, `TUTOR_ADAPTATIVO.md`, `FLUJO_DEFENSA_3_MIN.md`
  (guion 3 min + checklist grabación).
- **Auditoría integral para redacción** (20 secciones):
  `reports/final_thesis_audit_20260706_215711/AUDITORIA_COMPLETA_PARA_REDACCION.md`.

## 2. Pruebas

| Prueba | Resultado |
|---|---|
| Backend `pytest tests/` (contenedor aislado, CHROMA_DIR de prueba, add-host Ollama) | **263 passed, 4 skipped, 0 failed** |
| Nuevos: `tests/test_final_ux_guidance.py` | 21 tests (multi-concepto, prioridades, help_level, directivas, chat general, chat lección) |
| Frontend lint | 0 errores (4 warnings preexistentes) |
| `npm run build` | OK |
| Contratos: `test:moodle-section` / `test:chat-sources` / **`test:guidance` (nuevo)** | 3/3 OK |

Nota: `test_ai_prepare` falla solo si se corre con la env de producción
`AI_PREP_MODEL` (pisa el default esperado) o sin `--add-host` para Ollama —
ambos son artefactos del entorno de ejecución, no del código (verificado
también contra main previo `aba2ab8`).

## 3. Commit / merge / deploy

- Commit: `812c5cb` (20 archivos, +1976/−79) → push → **PR #19** → merge a
  `main` (`df4ef05`).
- Deploy: `git reset --hard origin/main` + `build fastapi frontend` +
  `up -d fastapi frontend gateway`. El gateway necesitó `restart` para
  refrescar la IP del upstream de fastapi (gotcha conocido; 502 transitorio
  ~40 s durante la ventana de deploy).

## 4. Health y smoke (post-deploy)

- `GET /api/ai/health` → `status: ok` (fastapi/moodle_db/moodle_ws/chroma/
  ollama ok, `chroma_chunks: 241`).
- `smoke_produccion.sh` con token: **11 PASS, 0 FAIL** (incluye `/moodle/me`
  y `/chat` autenticados).

## 5. Validación funcional en vivo (producción, estudiante real id=40)

1. **Guidance multi-concepto** (SEC2-R55, 2 fallos reales de 5): POST
   `/learning-signals/lesson/SEC2-R55/guidance` → `should_notify=true`,
   `level=partial`, mensaje con los **2 conceptos numerados**, cada uno con
   minuto (2:30 / 4:50), recurso real y micro-práctica + orden recomendado +
   cierre `orientar`. ✔
2. **Chat general** "¿Qué debo reforzar?" sin lesson_id →
   `intent=personal_progress_no_lesson`, `answer_type=deterministic_orientation`,
   sin señales inventadas, respuesta neutral que pide abrir una lección. ✔
3. **Chat de lección** (SEC2-R55, pregunta de desempeño) →
   `has_learning_signals=true`; el tutor cubrió ambos conceptos débiles
   anclado a la transcripción. ✔ (una corrida previa con pregunta más escueta
   devolvió el fallback "sin evidencia" — no-determinismo del modelo 8b; la vía
   principal para esa necesidad es la guía determinística, que es estable).
4. **Diferencia real tono/nivel**: A/B en vivo con SEC2-R56 temporalmente en
   `socratico/preguntar` (config respaldada y **restaurada** a
   `practico/orientar`, verificado en las 7 lecciones): práctico produjo pasos
   accionables numerados; socrático produjo razonamiento conceptual con
   recomendación operativa. Diferencia observable; el estilo socrático del
   modelo 8b es parcial (limitación conocida del modelo local; la inyección de
   directivas está garantizada por tests unitarios del render). ✔ con reserva
5. **Bundle servido**: los assets del gateway contienen la nueva UI
   ("Ver guía del tutor"). ✔
6. **Persistencia/dedupe/no-duplicados**: garantizados por contrato
   (`verify_guidance_recovery_contract.mjs`, 9 escenarios incluidos recarga,
   expiración, legado, cruce de lecciones) — la verificación visual en
   navegador (sonido/animación) queda listada para la prueba manual del autor.

## 6. Chroma — sin cambios (obligatorio)

| | PRE | POST |
|---|---|---|
| Colecciones | langchain | langchain |
| Total chunks | 241 | **241** |
| source_type None | 191 | **191** |
| teacher_approved_context | 50 | **50** |

(Único evento: una sonda inicial creó por error la colección vacía
`documentos_curso` (0 docs) y fue eliminada de inmediato — documentado en
PRE_STATE. Los tests corrieron con `CHROMA_DIR` aislado.)

## 7. Estado final

- Servidor en **main limpio** (`df4ef05`), 9/9 contenedores up, health ok,
  smoke 11/11.
- Sin tocar: H5P (0 cambios en mod_hvp/manifest), teacher-driven RAG (0 cambios
  de ingest), modelos (mismos), prompts globales (solo inyección aditiva por
  lección), Chroma (241=241).
- Untracked preexistentes bajo `reports/` (contienen backups .tar.gz/.sql.gz de
  cierres anteriores): se dejan fuera de git a propósito, como estaban.

## 8. Pendientes reales

1. Verificación visual en navegador del sonido/animación del badge (la lógica
   está cubierta por contratos; falta solo la comprobación sensorial).
2. Poblar Secciones 1..N con el mismo flujo docente (contenido, no código).
3. Estilo socrático del modelo 8b es parcial — mejorable con un modelo mayor
   o few-shots en el pack (post-piloto).
4. Deuda técnica ya conocida: residual `axis_id` en esquema; plugin
   `local_tesisai`/`api_persistente` fuera del repo (respaldados en runtime).
5. Lección 6 (content 26) sin intentos de estudiantes al cierre (dato, no bug).
