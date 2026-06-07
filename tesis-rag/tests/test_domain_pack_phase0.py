"""Gate de regresion durable de la Fase 0 (extraccion al Domain Pack).

Reconstruye el snapshot determinista del comportamiento dependiente de dominio
(routing, prompts, verificacion, scoring de retrieval, prompts de nodo) y exige
que sea BYTE-IDENTICO al golden baseline capturado antes del refactor para
course_id=2. Si la extraccion (o un pack) cambia el comportamiento, este test
falla. No necesita Ollama ni Chroma.

Correr: python -m pytest tests/test_domain_pack_phase0.py -q
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASELINE = os.path.join(os.path.dirname(__file__), "phase0_baseline.json")


def _flatten(obj, prefix=""):
    flat = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            flat.update(_flatten(v, f"{prefix}.{k}" if prefix else str(k)))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            flat.update(_flatten(v, f"{prefix}[{i}]"))
    else:
        flat[prefix] = obj
    return flat


def test_phase0_snapshot_matches_baseline():
    from scripts.phase0_snapshot import build_snapshot

    assert os.path.exists(BASELINE), "Falta el golden baseline tests/phase0_baseline.json"
    with open(BASELINE, encoding="utf-8") as f:
        baseline = json.load(f)

    current = json.loads(json.dumps(build_snapshot(), ensure_ascii=False))  # normaliza tuplas->listas

    fb, fc = _flatten(baseline), _flatten(current)
    diffs = [k for k in set(fb) | set(fc) if fb.get(k) != fc.get(k)]
    assert not diffs, f"Comportamiento cambio en {len(diffs)} valores; ej: {diffs[:10]}"


def test_default_pack_loads():
    """El pack neutro (_default) carga: un curso sin pack degrada sin romper."""
    from services.domain import get_domain_pack

    pack = get_domain_pack("__curso_inexistente__")
    assert pack.unsupported_terms() == []
    assert pack.controlled_answers() == []
    assert pack.node_prompt("rag_system")  # no vacio


def test_course2_pack_is_source_of_truth():
    """Las constantes del agente provienen del pack de course 2 (no de literales)."""
    from services.domain import get_domain_pack
    from services.agent import routing

    pack = get_domain_pack("2")
    assert routing.COURSE_AXES == pack.course_axes()
    assert routing.SPECIFIC_UNSUPPORTED_TERMS == pack.unsupported_terms()
    assert len(routing.TECHNICAL_CONCEPT_PATTERNS) == len(pack.concept_patterns())


if __name__ == "__main__":
    # Runnable sin pytest (no esta en el venv): corre el gate y reporta.
    test_phase0_snapshot_matches_baseline()
    test_default_pack_loads()
    test_course2_pack_is_source_of_truth()
    print("PHASE 0 GATE: OK — comportamiento byte-identico al baseline para course 2.")
