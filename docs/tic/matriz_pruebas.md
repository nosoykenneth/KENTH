# Matriz de pruebas — TIC KENTH

Pruebas por tipo, con estado, resultado, evidencia y comando reproducible.
Referencias: suite `tesis-rag/tests/`, validadores `tesis-rag/scripts/`, smoke
`scripts/smoke_produccion.sh`, y la auditoría E2E del servidor (`AUDITORIA_TIC_READYNESS.md`).

**Estado:** ✅ ejecutada · ⏳ pendiente.
Los comandos de backend se corren desde `tesis-rag/` (con el venv activo).

---

## 1. Pruebas funcionales / unitarias (pytest)

| ID | Qué prueba | Estado | Resultado | Evidencia | Comando |
|---|---|---|---|---|---|
| F-01 | Contrato de capabilities (normalización, accesores, WS no configurada). | ✅ | pass | `tests/test_moodle_permissions.py` | `pytest tests/test_moodle_permissions.py` |
| F-02 | Separación de roles en autoría (momentos vs bloques; guards). | ✅ | pass | `tests/test_authoring_role_separation.py` | `pytest tests/test_authoring_role_separation.py` |
| F-03 | Perfil pedagógico canónico (build/apply/fuse). | ✅ | pass | `tests/test_pedagogy_profile.py` | `pytest tests/test_pedagogy_profile.py` |
| F-04 | Asistente ai-prepare (schema, modelos, promoción). | ✅ | pass | `tests/test_ai_prepare.py` | `pytest tests/test_ai_prepare.py` |
| F-05 | Domain Pack Fase 0 (snapshot byte-idéntico). | ✅ | pass | `tests/test_domain_pack_phase0.py` | `pytest tests/test_domain_pack_phase0.py` |
| F-06 | Routing de dominio y orientación (decisión sobre la pregunta). | ✅ | pass | `tests/test_routing_domain_orientation.py` | `pytest tests/test_routing_domain_orientation.py` |
| F-07 | Fixes pedagógicos del tutor (delegación, perdido, dedup). | ✅ | pass | `tests/test_tutor_pedagogical_fixes.py` | `pytest tests/test_tutor_pedagogical_fixes.py` |
| F-08 | Lenguaje del profesor (idioma/tono). | ✅ | pass | `tests/test_professor_language.py` | `pytest tests/test_professor_language.py` |
| **F-09** | **/health, /moodle/me (B1), course_id tolerante (B3), seguridad no debilitada.** | ✅ | **12 pass** | `tests/test_operational_endpoints.py` | `pytest tests/test_operational_endpoints.py` |

## 2. Pruebas de integración

| ID | Qué prueba | Estado | Resultado | Evidencia | Comando |
|---|---|---|---|---|---|
| I-01 | Contrato de secciones Moodle (WS + BD). | ✅ | pass | `tests/test_moodle_section_contract.py` | `pytest tests/test_moodle_section_contract.py` |
| I-02 | RAG por secciones (metadata sin `axis_id`, scope). | ✅ | pass | `tests/test_rag_secciones.py` | `pytest tests/test_rag_secciones.py` |
| I-03 | Política de ingesta pública/segura. | ✅ | pass | `tests/test_ingest_public_policy.py`, `test_source_policy.py` | `pytest tests/test_source_policy.py` |
| I-04 | Contrato de sección (frontend). | ✅ | pass | `scripts/verify_moodle_section_contract.mjs` | `npm run test:moodle-section` |
| **I-SUITE** | **Suite completa backend.** | ✅ | **183 passed, 1 skipped** | `tesis-rag/tests/` | `python -m pytest tests/` |

## 3. Pruebas E2E (tutor por el gateway, con token real)

Ejecutadas en la auditoría del servidor (03-jul-2026) por SSH contra el gateway.

| ID | Escenario | Estado | Resultado | Evidencia |
|---|---|---|---|---|
| E-01 | Pregunta en lección (sistema de decisión). | ✅ | grounded, evidencia alta | AUDITORIA §9 (P) |
| E-02 | Pregunta de otra sección (no indexada). | ✅ | rehúsa “fuera del contexto”, no alucina | §9 (C2) |
| E-03 | Pregunta fuera de dominio (cálculo). | ✅ | bloqueo `out_of_domain` | §9 (C3) |
| E-04 | Pregunta ambigua. | ✅ | pide precisión | §9 (C4) |
| E-05 | Cita literal de transcripción. | ✅ | responde con la cita | §9 (C5) |
| E-06 | Lección sin chunks (grounding por metadata). | ⚠️ | plausible; revisar tras reindex | §9 (C6) |

## 4. Pruebas de seguridad / roles

Verificadas en runtime (auditoría §8) y fijadas por unit tests (F-01/F-02/F-09).

| ID | Escenario | Esperado | Estado | Evidencia |
|---|---|---|---|---|
| S-01 | `/chat` sin token. | 401 | ✅ | §8 |
| S-02 | `/chat` con `X-User-Id` sin token (bypass). | 401 (cerrado) | ✅ | §8 |
| S-03 | `/documents/rebuild` como estudiante/profesor. | 403 | ✅ | §8 |
| S-04 | `/authoring/.../blocks` como estudiante/profesor sin edición. | 403 | ✅ | §8 |
| S-05 | Profesor sin edición intenta editar. | 403 | ✅ | F-02, §8 |
| S-06 | `/moodle/me` no filtra campos no whitelisted del perfil. | sólo lista blanca | ✅ | F-09 |
| S-07 | `/health` no expone secretos (token/DBpass). | ausentes en el body | ✅ | F-09 |
| S-08 | course_id por query no salta la capability. | 403 sin acceso | ✅ | F-09 |

## 5. Pruebas de RAG / índice

| ID | Qué prueba | Estado | Resultado | Comando |
|---|---|---|---|---|
| R-01 | Coherencia del índice (sin `axis_id`, sin `scope=axis`). | ✅ | “Índice coherente” | `python scripts/validate_rag_index.py` |
| R-02 | Índice limpio (fuentes/chunks). | ✅ | 24 chunks / 1 fuente (escaso) | `python scripts/verify_rag_index_clean.py` |
| R-03 | Cobertura por sección/lección. | ⏳ | pendiente reindex del corpus | (tras reindexar) |

## 6. Pruebas de disponibilidad

| ID | Qué prueba | Estado | Resultado | Comando |
|---|---|---|---|---|
| A-01 | `/api/ai/health` responde con estado. | ✅ | 200 + `status` | `curl -s $BASE/api/ai/health` |
| A-02 | Smoke de disponibilidad completo. | ✅ | 0 FAIL (esperado) | `bash scripts/smoke_produccion.sh` |
| A-03 | Contenedores del stack arriba. | ✅ | 9 up | `docker compose -f docker-compose.deploy.yml ps` |

## 7. Pruebas de frontend

| ID | Qué prueba | Estado | Resultado | Comando |
|---|---|---|---|---|
| FE-01 | Lint del frontend. | ✅ | sin errores | `npm run lint` |
| FE-02 | Build de producción. | ✅ | bundle generado | `npm run build` |
| FE-03 | Contrato de sección Moodle. | ✅ | pass | `npm run test:moodle-section` |
| FE-04 | Recorrido en navegador (student/profesor/admin). | ⏳ | pendiente (SPA headless en auditoría) | manual |

---

## Cómo reproducir todo

```bash
# Backend
cd tesis-rag && .venv/Scripts/python -m pytest tests/ -q

# Frontend
cd frontend-tesis && npm run lint && npm run test:moodle-section && npm run build

# Disponibilidad (servidor)
BASE_URL=http://localhost:8090 bash scripts/smoke_produccion.sh
curl -s http://localhost:8090/api/ai/health

# Índice RAG (lectura)
docker exec tic-fastapi python scripts/validate_rag_index.py
```
