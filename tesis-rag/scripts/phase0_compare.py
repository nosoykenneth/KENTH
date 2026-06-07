"""Fase 0 — Compara dos snapshots deterministas (baseline vs after).

Gate de regresion: la extraccion al Domain Pack es behavior-preserving si y solo
si el snapshot DESPUES es byte-identico al baseline para course_id=2.

Uso: python scripts/phase0_compare.py <baseline.json> <after.json>
"""

import json
import sys


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


def main():
    if len(sys.argv) < 3:
        print("Uso: python scripts/phase0_compare.py <baseline.json> <after.json>")
        sys.exit(2)
    base = json.load(open(sys.argv[1], encoding="utf-8"))
    after = json.load(open(sys.argv[2], encoding="utf-8"))

    fb = _flatten(base)
    fa = _flatten(after)

    keys = sorted(set(fb) | set(fa))
    diffs = []
    for k in keys:
        if k not in fb:
            diffs.append(("ADDED", k, None, fa[k]))
        elif k not in fa:
            diffs.append(("REMOVED", k, fb[k], None))
        elif fb[k] != fa[k]:
            diffs.append(("CHANGED", k, fb[k], fa[k]))

    if not diffs:
        print(f"GATE OK — snapshots IDENTICOS ({len(fb)} valores comparados).")
        sys.exit(0)

    print(f"GATE FALLO — {len(diffs)} diferencias (de {len(keys)} valores):\n")
    for kind, k, old, new in diffs[:60]:
        print(f"[{kind}] {k}")
        if kind == "CHANGED":
            print(f"    baseline: {old!r}")
            print(f"    after   : {new!r}")
        elif kind == "ADDED":
            print(f"    after   : {new!r}")
        else:
            print(f"    baseline: {old!r}")
    if len(diffs) > 60:
        print(f"\n... y {len(diffs) - 60} mas.")
    sys.exit(1)


if __name__ == "__main__":
    main()
