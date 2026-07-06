#!/usr/bin/env python3
"""Convierte el manifest pedagógico (course_2_interactions.json) en un
'build spec' de H5P: por cada actividad InteractiveVideo (hvp_content_id) genera
el array `interactions` con params VÁLIDOS de H5P.MultiChoice / H5P.TrueFalse /
H5P.Summary. El applier PHP (apply_h5p_interactions.php) sólo inyecta este array
en `interactiveVideo.assets.interactions` vía mod_hvp core (re-filtra + recalcula
dependencias). NO se toca el bloque de video ni el resto de params.

subContentId es DETERMINISTA (uuid5 del interaction_id) → re-ejecutar es idempotente.

Uso:
  python scripts/h5p/build_h5p_interactions.py \
      --manifest data/learning_signals/course_2_interactions.json \
      --out /tmp/h5p_build_course2.json
"""
from __future__ import annotations
import argparse
import json
import uuid
from pathlib import Path

# Namespace estable para derivar subContentIds deterministas.
_NS = uuid.UUID("5f9d3a2e-0000-4000-8000-000000000002")

# Versiones EXACTAS instaladas en el Moodle (mdl_hvp_libraries).
LIB_MULTICHOICE = "H5P.MultiChoice 1.16"
LIB_TRUEFALSE = "H5P.TrueFalse 1.8"
LIB_SUMMARY = "H5P.Summary 1.10"


def _uuid(seed: str) -> str:
    return str(uuid.uuid5(_NS, seed))


def _p(text: str) -> str:
    return f"<p>{text}</p>"


def _mc_params(it: dict) -> tuple[str, dict, dict]:
    answers = []
    for opt in it["options"]:
        answers.append({
            "text": f"<div>{opt['text']}</div>",
            "correct": bool(opt["correct"]),
            "tipsAndFeedback": {
                "tip": "",
                "chosenFeedback": f"<div>{opt.get('feedback', '')}</div>",
                "notChosenFeedback": "",
            },
        })
    params = {
        "question": _p(it["question"]),
        "answers": answers,
        "behaviour": {
            "enableRetry": True,
            "enableSolutionsButton": False,
            "enableCheckButton": True,
            "type": "auto",
            "singlePoint": True,
            "randomAnswers": True,
            "showSolutionsRequiresInput": True,
            "confirmCheckDialog": False,
            "confirmRetryDialog": False,
            "autoCheck": False,
            "passPercentage": 100,
            "showScorePoints": True,
        },
        "overallFeedback": [
            {"from": 0, "to": 99, "feedback": it.get("feedback_incorrect", "")},
            {"from": 100, "to": 100, "feedback": it.get("feedback_correct", "")},
        ],
    }
    meta = {
        "contentType": "Multiple Choice", "license": "U",
        "title": it["interaction_id"], "authors": [], "changes": [],
        "extraTitle": it["interaction_id"],
    }
    return LIB_MULTICHOICE, params, meta


def _tf_params(it: dict) -> tuple[str, dict, dict]:
    params = {
        "question": _p(it["question"]),
        "correct": "true" if it["correct"] else "false",
        "behaviour": {
            "enableRetry": True,
            "enableSolutionsButton": False,
            "enableCheckButton": True,
            "confirmCheckDialog": False,
            "confirmRetryDialog": False,
            "autoCheck": False,
        },
    }
    meta = {
        "contentType": "True/False Question", "license": "U",
        "title": it["interaction_id"], "authors": [], "changes": [],
        "extraTitle": it["interaction_id"],
    }
    return LIB_TRUEFALSE, params, meta


def _summary_params(it: dict) -> tuple[str, dict, dict]:
    # H5P.Summary: en cada grupo, el statement en índice 0 es el CORRECTO (se
    # baraja en pantalla). Ponemos el correcto primero.
    correct = [s["text"] for s in it["summaries"] if s["correct"]]
    wrong = [s["text"] for s in it["summaries"] if not s["correct"]]
    statements = correct[:1] + wrong
    params = {
        "intro": _p(it["question"]),
        "summaries": [{
            "subContentId": _uuid(it["interaction_id"] + ":grp"),
            "summary": statements,
            "tip": "",
        }],
        "overallFeedback": [{"from": 0, "to": 100}],
        "solvedLabel": "Progreso:",
        "scoreLabel": "Respuestas incorrectas:",
        "resultLabel": "Tu resultado",
        "labelCorrect": "Correcta.",
        "labelIncorrect": "Incorrecto. Inténtalo otra vez.",
        "alternativeIncorrectLabel": "Incorrecto",
        "labelCorrectAnswers": "Respuestas correctas.",
        "tipButtonLabel": "Mostrar pista",
        "scoreBarLabel": "Has conseguido :num de un total de :total puntos",
        "progressText": "Progreso :num de :total",
    }
    meta = {
        "contentType": "Summary", "license": "U",
        "title": it["interaction_id"], "authors": [], "changes": [],
        "extraTitle": it["interaction_id"],
    }
    return LIB_SUMMARY, params, meta


_BUILDERS = {
    "multiple_choice": _mc_params,
    "true_false": _tf_params,
    "summary": _summary_params,
}


def build_interaction(it: dict, duration: int) -> dict:
    builder = _BUILDERS.get(it["type"])
    if builder is None:
        raise ValueError(f"Tipo no soportado: {it['type']} ({it['interaction_id']})")
    library, params, meta = builder(it)
    at = int(it["at"])
    # El marcador es visible en la línea de tiempo unos segundos; el video se
    # pausa en `from` si pause=true (interacción formativa, no bloqueante).
    to = min(at + 12, max(at + 1, duration - 1))
    return {
        "x": 44.813,
        "y": 31.135,
        "width": 10,
        "height": 10,
        "duration": {"from": at, "to": to},
        "libraryTitle": meta["contentType"],
        "action": {
            "library": library,
            "params": params,
            "subContentId": _uuid(it["interaction_id"]),
            "metadata": meta,
        },
        "pause": bool(it.get("pause", True)),
        "displayType": "poster",
        "buttonOnMobile": False,
        "adaptivity": {
            "correct": {"allowOptOut": False, "message": ""},
            "incorrect": {"allowOptOut": False, "message": ""},
            "requireCompletion": False,
        },
        "label": "",
        "visuals": {"backgroundColor": "rgba(255,255,255,0.9)", "boxShadow": True},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    build = {"course_id": manifest["course_id"], "activities": []}
    for lesson in manifest["lessons"]:
        dur = int(lesson["duration_seconds"])
        interactions = [build_interaction(it, dur) for it in lesson["interactions"]]
        build["activities"].append({
            "lesson_id": lesson["lesson_id"],
            "cmid": lesson["cmid"],
            "hvp_content_id": lesson["hvp_content_id"],
            "interactions": interactions,
            "expected_max_score": sum(int(i.get("max_score", 1)) for i in lesson["interactions"] if i.get("graded", True)),
        })
    Path(args.out).write_text(json.dumps(build, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(len(a["interactions"]) for a in build["activities"])
    print(f"OK build: {len(build['activities'])} activities, {total} interactions -> {args.out}")
    for a in build["activities"]:
        libs = sorted({i["action"]["library"] for i in a["interactions"]})
        print(f"  {a['lesson_id']} hvp={a['hvp_content_id']} n={len(a['interactions'])} max={a['expected_max_score']} libs={libs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
