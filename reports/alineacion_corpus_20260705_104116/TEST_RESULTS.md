# Resultados de validacion tecnica

## Backend
- `python -B -m pytest tests --basetemp <dir>` dentro de `tesis-rag`: 198 passed, 4 skipped, 1 warning. Requirio ejecucion fuera del sandbox por permisos de temporales/cache en Windows.
- `docker exec tic-fastapi python scripts/validate_rag_index.py`: OK, 233 chunks, 0 `axis_id`, 0 `scope=axis`, 0 duplicados por `source_hash`.

## Frontend
- `npm run test:moodle-section`: PASS.
- `npm run test:chat-sources`: PASS.
- `npm run lint`: PASS con 5 warnings existentes de `react-hooks/exhaustive-deps`.
- `npm run build`: PASS; Vite advierte chunk JS > 500 kB.

## Smoke servidor
- `BASE_URL=http://localhost:8090 bash scripts/smoke_produccion.sh`: 9 PASS, 0 FAIL; pruebas autenticadas omitidas por falta de `MOODLE_TOKEN` utilizable.

## Chat autenticado
- `chat_validation_auth.py`: 9 PASS, 0 FAIL; token de estudiante real usado sin imprimir valor.

## Cierre servidor
- Servidor en `chore/align-corpus-rag-index`; `git status -sb` limpio salvo artefactos ignorados/server-only.
- Health OK con `chroma_chunks=233`; `validate_rag_index.py` OK; smoke 9 PASS, 0 FAIL.
