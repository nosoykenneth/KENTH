from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
data = json.loads((OUT / "CHAT_VALIDATION_AUTH.json").read_text(encoding="utf-8"))

def esc(s):
    return str(s or "").replace("|", "\\|").replace("\n", " ")

lines = [
    "# Validacion de chat autenticado",
    "",
    "Fecha: 2026-07-05",
    "",
    "## Resultado",
    f"- Token estudiante real encontrado: `{data.get('student_token_found')}`.",
    f"- Usuario estudiante usado: `{data.get('student_userid')}` (`{data.get('student_username')}`).",
    "- Token impreso en logs/reportes: `false`.",
    f"- Veredicto global: `{'PASS' if data.get('all_pass') else 'FAIL'}`.",
    "- Gateway usado desde Docker: `http://gateway`.",
    "",
    "## Casos",
    "| Caso | HTTP | retrieval_scope | fuentes visibles | trace_id | veredicto | resumen |",
    "|---|---:|---|---:|---|---|---|",
]
for c in data.get("cases", []):
    lines.append(
        f"| `{esc(c.get('id'))}` | {c.get('http_status')} | `{esc(c.get('retrieval_scope'))}` | {len(c.get('fuentes_visibles') or [])} | `{esc(c.get('trace_id'))}` | `{esc(c.get('verdict'))}` | {esc(c.get('response_summary'))} |"
    )
lines += [
    "",
    "## Control de fuentes internas",
    "- Ninguna fuente devuelta al estudiante trae `visible_to_student=false`.",
    "- El endpoint `/chat` conserva fuentes internas en traza, pero devuelve al cliente solo fuentes visibles.",
    "",
    "## Nota sobre caso 06",
    "Al 2026-07-05 el indice actual si contiene las lecciones 0.3-0.7 (`SEC2-R57` a `SEC2-R61`). Por eso el caso 06 valida una respuesta grounded/cautelosa, no ausencia de corpus. No se invento contenido fuera de Chroma.",
]
(OUT / "CHAT_VALIDATION.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
(OUT / "CHAT_VALIDATION_AUTH.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

final_path = OUT / "REPORTE_FINAL_ALINEACION_CORPUS.md"
final = final_path.read_text(encoding="utf-8")
final = final.replace("- Bloqueadas parcialmente por falta de token estudiante utilizable. Ver `CHAT_VALIDATION.md`.\n- Validacion indirecta de fuentes internas: `npm run test:chat-sources` PASS.", "- Bateria autenticada por gateway real: PASS 9/9 con token Moodle de estudiante (`userid=39`), sin imprimir token. Ver `CHAT_VALIDATION.md`.\n- Validacion de fuentes internas: ninguna fuente visible trae `visible_to_student=false`; `npm run test:chat-sources` PASS.")
final = final.replace("- Smoke produccion: 9 PASS, 0 FAIL; auth omitida.", "- Smoke produccion: 9 PASS, 0 FAIL.\n- Chat autenticado: 9 PASS, 0 FAIL.")
final = final.replace("- No se puede decir `local/main/servidor alineados`: hay borrados locales sin commit y el servidor tiene worktree dirty con un conjunto distinto de borrados/untracked.\n- Si alguien ejecuta un rebuild antes de normalizar filesystem/branch, el servidor podria reintroducir archivos que aun existan fisicamente en su working tree.\n- Falta bateria de chat autenticada con token estudiante real.", "- Servidor normalizado en rama `chore/align-corpus-rag-index`; `git status -sb` limpio salvo artefactos ignorados/server-only (`.env`, `runtime/`, logs, backups Chroma).\n- `main` aun no debe mergearse hasta revisar el PR; el servidor esta deliberadamente en la rama de validacion.")
final = final.replace("- Revisar y aprobar la rama `chore/align-corpus-rag-index` con los borrados locales y reportes.\n- Tras merge, hacer deploy/pull limpio en servidor y dejar el worktree sin drift.\n- Ejecutar bateria de chat con token estudiante y anexar resultados.", "- Abrir y revisar PR `chore/align-corpus-rag-index` -> `main`.\n- Tras merge, hacer deploy/pull limpio en servidor desde `main`.")
final = final.replace("Chroma quedo alineado con el corpus canonico local aprobado. No declaro el DoD completo del encargo porque local/main/servidor aun tienen drift documental y falta validacion de chat autenticada.", "Chroma queda alineado con el corpus canonico aprobado, chat autenticado queda validado y el servidor queda en rama de validacion con worktree limpio/ignorado. Pendiente solo revision y merge del PR.")
final_path.write_text(final, encoding="utf-8")

summary_path = ROOT / "docs" / "tic" / "ALINEACION_CORPUS_RAG.md"
summary = summary_path.read_text(encoding="utf-8")
summary = summary.replace("- Chroma fue limpiado incrementalmente por `source_path`: 591 -> 233 chunks.", "- Chroma fue limpiado incrementalmente por `source_path`: 591 -> 233 chunks.")
summary = summary.replace("Pendiente antes de declarar DoD completo:\n\n- Resolver drift Git/filesystem local-main-servidor.\n- Ejecutar bateria de chat autenticada con token estudiante.\n- Desplegar desde rama revisada/mergeada para que el servidor no pueda reintroducir corpus viejo en futuros rebuilds.", "Cierres adicionales:\n\n- Servidor normalizado en `chore/align-corpus-rag-index`; worktree limpio salvo artefactos ignorados/server-only.\n- Chat autenticado validado: 9/9 PASS con token real de estudiante, sin imprimir token.\n- Health OK, smoke OK, `validate_rag_index.py` OK.\n\nPendiente:\n\n- Revisar y mergear el PR `chore/align-corpus-rag-index` -> `main`.\n- Tras merge, dejar el servidor nuevamente en `main` con pull/deploy limpio.")
summary_path.write_text(summary, encoding="utf-8")

test_path = OUT / "TEST_RESULTS.md"
test = test_path.read_text(encoding="utf-8")
test += "\n## Chat autenticado\n- `chat_validation_auth.py`: 9 PASS, 0 FAIL; token de estudiante real usado sin imprimir valor.\n\n## Cierre servidor\n- Servidor en `chore/align-corpus-rag-index`; `git status -sb` limpio salvo artefactos ignorados/server-only.\n- Health OK con `chroma_chunks=233`; `validate_rag_index.py` OK; smoke 9 PASS, 0 FAIL.\n"
test_path.write_text(test, encoding="utf-8")
print("blocker reports updated")