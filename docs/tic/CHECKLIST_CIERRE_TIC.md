# CHECKLIST DE CIERRE TIC — rama `fix/tic-readiness-operational-docs`

Reporte final del cierre operativo + documental. Referencia: `AUDITORIA_TIC_READYNESS.md`
(commit auditado `6b25712`). **No** se tocó el corpus/materia definitiva ni se reindexó;
**no** se hizo merge a `main` ni se abrió PR (a la espera de revisión).

**Fecha:** 2026-07-04 · **Rama:** `fix/tic-readiness-operational-docs`

---

## 1. Qué quedó corregido

| Bug (auditoría §11) | Estado | Corrección |
|---|---|---|
| **B1** `/moodle/me` → 500 (KeyError de logging) | ✅ **Cerrado** | `moodle_ws_client.py`: clave `message` en `extra` renombrada a `ws_message`/`ws_function`. `/moodle/me` ahora responde **200** con `user_id`+`profile`(whitelist)+`capabilities` y degrada de forma controlada si el WS falla (nunca 500/502). |
| **B2** sin `/health` | ✅ **Cerrado** | Nuevo `GET /api/ai/health` con estado de FastAPI/BD/WS/Chroma/Ollama y modelos; sin secretos. En el servidor → `status: ok`. |
| **B3** `/sections/lessons/all` → 422 opaco | ✅ **Cerrado** | `require_course_view` acepta el curso por `X-Course-Id` o `?course_id`; **400** claro si falta; la capability se valida siempre sobre el curso resuelto (no debilita seguridad). Aplicado también a `/list`, `/links`, `/{section}/lessons`. |
| **B4** plugin/api_persistente fuera del repo | ✅ **Cerrado** | Versionados en `moodle/` **sin secretos** (auditados y redactados). |

## 2. Qué documentos se crearon

**Reproducibilidad / despliegue**
- `moodle/README.md`, `moodle/local_tesisai/**` (plugin completo), `moodle/api_persistente/**` (fuente PHP + `.env.example` + `.htaccess` + README).
- `docs/deploy/DEPLOY_PRODUCCION.md`.
- `scripts/smoke_produccion.sh`.

**Paquete académico TIC (`docs/tic/`)**
- `requisitos.md` · `casos_de_uso.md` · `diagramas.md` (Mermaid) · `endpoints.md` ·
  `matriz_pruebas.md` · `evaluacion_tutor.md` (plantilla) · `encuesta_likert.md` ·
  `rubrica_validacion.md` · `seguridad.md` · **este** `CHECKLIST_CIERRE_TIC.md`.
- `AUDITORIA_TIC_READYNESS.md` versionado en la raíz.

## 3. Qué bugs se cerraron

B1 ✅ · B2 ✅ · B3 ✅ · B4 ✅. (B5 pytest-en-imagen, B6 asset, B7 corpus escaso, B8
tabla `axes` residual: **no** abordados — ver pendientes.)

## 4. Qué pruebas pasaron

| Suite | Resultado |
|---|---|
| Backend `pytest tests/` | **182 passed, 1 skipped** (exit 0) |
| Nuevos `tests/test_operational_endpoints.py` | **12 passed** (B1 logging, /health forma+sin-secretos, /moodle/me resiliente, course_id no salta capability, token obligatorio) |
| `npm run lint` | 0 errores (5 warnings pre-existentes, no de esta rama) |
| `npm run test:moodle-section` | OK |
| `npm run build` | OK (bundle generado) |
| Smoke en servidor `scripts/smoke_produccion.sh` | **11 PASS, 0 FAIL** |
| `/api/ai/health` (servidor) | `status: ok` (BD/WS/Chroma/Ollama/modelos ✔) |
| `/api/ai/moodle/me` con token (servidor) | **200** (antes 500) |
| Seguridad sin token (chat/rebuild/authoring) | 401/403 ✔ |

## 5. Commits y alineación

| Dónde | Commit | Rama |
|---|---|---|
| **Local** | `e4ac8f6` (← `8e905ed` ← `6b25712`) | `fix/tic-readiness-operational-docs` |
| **origin** | `e4ac8f6` | `fix/tic-readiness-operational-docs` |
| **Servidor** (`/srv/kenneth/tic-kenth`) | `e4ac8f6` | `fix/tic-readiness-operational-docs` |

> Local == origin == servidor, todos en la rama. `main` **no** modificada.
> ⚠️ El servidor en vivo quedó ejecutando **la rama** (por la validación de Fase 6),
> no `main`. Decisión pendiente del autor: mantenerla o revertir a `main` hasta el
> merge.

## 6. Estado de contenedores (servidor)

9 contenedores arriba: `tic-fastapi` (rebuild), `tic-frontend` (rebuild), `tic-gateway`,
`tic-moodle`, `tic-moodle-cron`, `tic-mariadb` (healthy), `tic-grafana`, `tic-loki`,
`tic-promtail`. Gateway no recreado (no cambió `nginx.full.conf`).

## 7. Pendiente por el corpus definitivo (fuera de esta rama)

- **Reindexar el corpus completo** del curso (hoy 24 chunks / 1 lección → B7). Bloquea:
  cobertura RAG de todas las lecciones/secciones y el fallback inter-sección.
- **Ejecutar el set de evaluación** (`evaluacion_tutor.md`) con respuestas/fuentes
  definitivas y reportar precisión/grounding/no-alucinación.
- Prueba R-03 (cobertura por sección) queda pendiente hasta el reindex.

## 8. Pendiente para piloto / evaluación

- Recorrido en navegador (student/profesor/admin) — FE-04 manual.
- Aplicar `encuesta_likert.md` (≥10 estudiantes, ≥1–2 docentes) y `rubrica_validacion.md`.
- Pruebas de carga / p95 (RNF-06) y hardening (HTTPS/dominio).
- Restauración de backups **probada** y fresca (ver `DEPLOY_PRODUCCION.md` §8).
- **Hallazgo residual (no bloqueante):** `/moodle/me` devuelve `moodle_ws: "error"` y
  `profile: null` porque el WS `core_user_get_users_by_field` lanza excepción con el
  token de servicio (probable falta de `moodle/user:viewdetails` o de la función en el
  servicio `api_tesis`). El endpoint ya es resiliente (200 + capabilities). Para que
  muestre el perfil, habilitar/permisar esa función WS en Moodle.
- Limpieza opcional: B5 (pytest en imagen), B6 (asset `logo_recortado.svg`), B8 (tabla
  `axes` residual), ramas remotas obsoletas.

---

## 9. Definition of Done (esta rama)

- [x] `/moodle/me` ya **no** responde 500 (200 con capabilities, verificado en servidor).
- [x] Existe `/api/ai/health` (200, `status: ok` en servidor).
- [x] Despliegue documentado (`DEPLOY_PRODUCCION.md`).
- [x] Plugin Moodle fuera del repo **versionado/documentado** (`moodle/`, sin secretos).
- [x] `docs/tic/` mínimos creados (9 + checklist).
- [x] Sin secretos en el diff (escaneo previo al commit, limpio).
- [x] Tests/lint/build en verde.
- [x] Servidor alineado con la rama (`e4ac8f6`), smoke 11/11.
- [ ] Merge a `main` / PR — **a la espera de revisión del autor** (por diseño).
