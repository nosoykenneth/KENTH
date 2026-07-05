from __future__ import annotations

import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
local = json.loads((OUT / "LOCAL_CANONICAL_AUDIT.json").read_text(encoding="utf-8-sig"))
pre = json.loads((OUT / "CHROMA_PRE_AUDIT.json").read_text(encoding="utf-8-sig"))
post = json.loads((OUT / "CHROMA_POST_AUDIT.json").read_text(encoding="utf-8-sig"))
cleanup = json.loads((OUT / "CHROMA_CLEANUP_RESULT.json").read_text(encoding="utf-8-sig"))
health = json.loads((OUT / "health_post_cleanup.json").read_text(encoding="utf-8-sig"))
pre_status = Counter(r.get("status") for r in pre.get("diff_table", []))
post_status = Counter(r.get("status") for r in post.get("diff_table", []))

chat_md = [
    "# Validacion de chat",
    "",
    "## Estado",
    "Bloqueada parcialmente: no hubo `MOODLE_TOKEN` utilizable para ejecutar las 10 preguntas por gateway real como estudiante. El smoke autenticado quedo omitido por el propio script de produccion.",
    "",
    "## Validado sin token",
    "- `/api/ai/chat` sin token devuelve 401.",
    "- Smoke produccion sin auth: 9 PASS, 0 FAIL.",
    "- Health post-cleanup: `status=ok`, `chroma_chunks=233`.",
    "- Contrato frontend `test:chat-sources`: PASS; las fuentes con `visible_to_student=false` se ocultan al alumno.",
    "",
    "## Casos requeridos no ejecutados",
]
for case in [
    "Pregunta 0.1 conceptual",
    "Pregunta 0.1 procedural",
    "Pregunta 0.2 conceptual",
    "Pregunta 0.2 Fletcher-Munson / ISO 226",
    "Pregunta nivel seccion",
    "Pregunta sobre 0.3-0.7",
    "Pregunta fuera de dominio",
    "Pregunta ambigua",
    "Pregunta que use guia interna sin mostrarla como fuente",
    "Pregunta que antes recuperaba archivo borrado",
]:
    chat_md.append(f"- {case}: NO EJECUTADA por falta de token estudiante utilizable.")
chat_md += ["", "## Veredicto"]
chat_md.append("No se declara validacion pedagogica E2E completa. El indice esta tecnicamente limpio, pero falta correr bateria de chat autenticada con token de estudiante.")
(OUT / "CHAT_VALIDATION.md").write_text("\n".join(chat_md) + "\n", encoding="utf-8")

test_md = [
    "# Resultados de validacion tecnica",
    "",
    "## Backend",
    "- `python -B -m pytest tests --basetemp <dir>` dentro de `tesis-rag`: 198 passed, 4 skipped, 1 warning. Requirio ejecucion fuera del sandbox por permisos de temporales/cache en Windows.",
    "- `docker exec tic-fastapi python scripts/validate_rag_index.py`: OK, 233 chunks, 0 `axis_id`, 0 `scope=axis`, 0 duplicados por `source_hash`.",
    "",
    "## Frontend",
    "- `npm run test:moodle-section`: PASS.",
    "- `npm run test:chat-sources`: PASS.",
    "- `npm run lint`: PASS con 5 warnings existentes de `react-hooks/exhaustive-deps`.",
    "- `npm run build`: PASS; Vite advierte chunk JS > 500 kB.",
    "",
    "## Smoke servidor",
    "- `BASE_URL=http://localhost:8090 bash scripts/smoke_produccion.sh`: 9 PASS, 0 FAIL; pruebas autenticadas omitidas por falta de `MOODLE_TOKEN` utilizable.",
]
(OUT / "TEST_RESULTS.md").write_text("\n".join(test_md) + "\n", encoding="utf-8")

final = [
    "# Reporte final de alineacion corpus RAG",
    "",
    "## 1. Estado local",
    f"- Rama/estado inicial: `{local['git']['branch_status'].splitlines()[0]}`.",
    f"- HEAD local: `{local['git']['head']}`.",
    f"- origin/main: `{local['git']['origin_main']}`.",
    f"- Local HEAD == origin/main: `{local['git']['head'] == local['git']['origin_main']}`.",
    f"- Cambios locales de corpus detectados: {local['counts']['deleted_documentos']} archivos borrados bajo `tesis-rag/documentos`.",
    "",
    "## 2. Estado servidor",
    "- Servidor accesible en `/srv/kenneth/tic-kenth`.",
    "- Compose correcto usado: `docker-compose.deploy.yml --env-file .env`.",
    "- 9 contenedores `tic-*` arriba; `tic-mariadb` healthy.",
    f"- Health post-cleanup: `{health.get('status')}`; Chroma `{health.get('chroma')}`; Ollama `{health.get('ollama')}`; chunks `{health.get('details', {}).get('chroma_chunks')}`.",
    "- Drift: el servidor no tiene worktree limpio; ver `SERVER_PRE_AUDIT.md` y `LOCAL_SERVER_DIFF.md`.",
    "",
    "## 3. Fuente canonica confirmada",
    "- Fuente canonica viva: `tesis-rag/documentos/`.",
    "- `corpus/` raiz local no existe y no es fuente de ingesta.",
    "- El codigo real (`ingest.py`) recorre `documentos/oficial/cursos`, `documentos/oficial/global` y `documentos/oficial/curso_<id>`; no recorre `corpus/` raiz.",
    "",
    "## 4. Archivos eliminados detectados",
    f"- Local: {local['counts']['deleted_documentos']} borrados pendientes.",
    "- En Chroma pre-cleanup habia 7 fuentes eliminadas localmente con chunks activos.",
    "",
    "## 5. Archivos que ya no estan en Chroma",
]
for item in cleanup.get("details", []):
    final.append(f"- `{item['source_path']}`: {item['source_path_chunks_before']} -> {item['source_path_chunks_after']} chunks")
final += [
    "",
    "## 6. Archivos nuevos indexados",
    "- No se indexaron archivos nuevos en esta operacion. La correccion fue limpieza incremental de stale chunks.",
    "",
    "## 7. Archivos excluidos correctamente",
    f"- Post-cleanup: evaluation_prompt={post['violation_counts']['evaluation_prompt']}, qa={post['violation_counts']['qa']}, operational_manifest={post['violation_counts']['operational_manifest']}, reports={post['violation_counts']['report']}, root_corpus={post['violation_counts']['root_corpus']}, excluded_paths={post['violation_counts']['excluded_paths']}.",
    "- `visible_to_student=false`: 59 chunks internos presentes para contexto, no como fuente visible al estudiante; contrato frontend `test:chat-sources` PASS.",
    "",
    "## 8. Estrategia usada",
    "- Opcion B: incremental cleanup por `source_path`.",
    "- Justificacion: 67 indexables presentes, 0 faltantes, 7 fuentes stale bien identificadas; rebuild global innecesario.",
    "",
    "## 9. Backup creado",
    "- Servidor: `reports/alineacion_corpus_20260705_104116/chroma_backup` (17M).",
    "- Pre-state: `CHROMA_PRE_AUDIT.json`, `CHROMA_PRE_AUDIT.md`, `CHROMA_CLEANUP_RESULT.json`.",
    "",
    "## 10. Estado Chroma antes/despues",
    f"- Antes: {pre.get('total_chunks')} chunks, {pre_status.get('OK_INDEXED', 0)} OK_INDEXED, {pre_status.get('STALE_IN_CHROMA', 0)} fuentes stale, {pre['violation_counts']['deleted_local_paths']} chunks stale.",
    f"- Despues: {post.get('total_chunks')} chunks, {post_status.get('OK_INDEXED', 0)} OK_INDEXED, 0 stale, 0 missing, 0 excluded indexed.",
    "",
    "## 11. Validacion de metadata",
    f"- course_id: `{post['counts']['by_course_id']}`.",
    f"- section_number: `{post['counts']['by_section_number']}`.",
    f"- moodle_section_id: `{post['counts']['by_moodle_section_id']}`.",
    f"- lesson_id: `{post['counts']['by_lesson_id']}`.",
    "- Nota: la Seccion pedagogica 0 esta mapeada a Moodle `section_number=1` / `moodle_section_id=2`; no se cambio a la fuerza.",
    "",
    "## 12. Pruebas de chat",
    "- Bloqueadas parcialmente por falta de token estudiante utilizable. Ver `CHAT_VALIDATION.md`.",
    "- Validacion indirecta de fuentes internas: `npm run test:chat-sources` PASS.",
    "",
    "## 13. Tests ejecutados",
    "- Backend pytest: 198 passed, 4 skipped.",
    "- Frontend `test:moodle-section`: PASS.",
    "- Frontend `test:chat-sources`: PASS.",
    "- Frontend lint: PASS con 5 warnings.",
    "- Frontend build: PASS con warning de chunk grande.",
    "- Smoke produccion: 9 PASS, 0 FAIL; auth omitida.",
    "- `validate_rag_index.py`: OK.",
    "",
    "## 14. Riesgos pendientes",
    "- No se puede decir `local/main/servidor alineados`: hay borrados locales sin commit y el servidor tiene worktree dirty con un conjunto distinto de borrados/untracked.",
    "- Si alguien ejecuta un rebuild antes de normalizar filesystem/branch, el servidor podria reintroducir archivos que aun existan fisicamente en su working tree.",
    "- Falta bateria de chat autenticada con token estudiante real.",
    "",
    "## 15. Proximos pasos",
    "- Revisar y aprobar la rama `chore/align-corpus-rag-index` con los borrados locales y reportes.",
    "- Tras merge, hacer deploy/pull limpio en servidor y dejar el worktree sin drift.",
    "- Ejecutar bateria de chat con token estudiante y anexar resultados.",
    "",
    "## Veredicto",
    "Chroma quedo alineado con el corpus canonico local aprobado. No declaro el DoD completo del encargo porque local/main/servidor aun tienen drift documental y falta validacion de chat autenticada.",
]
(OUT / "REPORTE_FINAL_ALINEACION_CORPUS.md").write_text("\n".join(final) + "\n", encoding="utf-8")

summary = [
    "# Alineacion corpus RAG",
    "",
    "Estado al 2026-07-05:",
    "",
    "- `tesis-rag/documentos/` es la fuente canonica viva de ingesta.",
    "- `corpus/` raiz no existe localmente y no es fuente de ingesta.",
    "- Chroma fue limpiado incrementalmente por `source_path`: 591 -> 233 chunks.",
    "- Se removieron 358 chunks stale de 7 archivos de secciones 02-08 eliminados localmente.",
    "- Post-audit: 67 archivos canonicos indexables OK, 0 missing, 0 stale, 0 eval/QA/manifests operativos/reportes/corpus raiz, 0 `axis_id`/`scope=axis`.",
    "- Backup servidor: `reports/alineacion_corpus_20260705_104116/chroma_backup`.",
    "- Seccion pedagogica 0 se mantiene mapeada internamente a Moodle `section_number=1` / `moodle_section_id=2`.",
    "",
    "Pendiente antes de declarar DoD completo:",
    "",
    "- Resolver drift Git/filesystem local-main-servidor.",
    "- Ejecutar bateria de chat autenticada con token estudiante.",
    "- Desplegar desde rama revisada/mergeada para que el servidor no pueda reintroducir corpus viejo en futuros rebuilds.",
    "",
    "Reporte completo: `reports/alineacion_corpus_20260705_104116/REPORTE_FINAL_ALINEACION_CORPUS.md`.",
]
(ROOT / "docs" / "tic" / "ALINEACION_CORPUS_RAG.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
print("final reports generated")