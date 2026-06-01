import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from ingest import rebuild_all_documents


def main() -> int:
    print("[REINDEX] Iniciando rebuild limpio de ChromaDB con politica publica.")
    result = rebuild_all_documents()
    print(f"[REINDEX] Resultado: {result}")

    verify_script = os.path.join(BASE_DIR, "scripts", "verify_rag_index_clean.py")
    completed = subprocess.run([sys.executable, verify_script], cwd=BASE_DIR)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
