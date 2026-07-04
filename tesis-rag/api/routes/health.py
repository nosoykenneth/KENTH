"""Endpoint de disponibilidad (readiness/liveness) del servicio de IA.

`GET /health`  (via gateway: `GET /api/ai/health`)

Revisa que FastAPI y sus dependencias criticas esten operativas:
FastAPI, BD Moodle/MariaDB, Moodle Web Services, Chroma (indice vectorial),
Ollama y los modelos de chat/embedding configurados.

Contrato de diseno:
- NO expone secretos (tokens, contrasenas, URLs con credenciales, rutas absolutas).
  Solo expone estados textuales, nombres de modelos (que ya son configuracion no
  secreta) y conteos agregados.
- NO requiere autenticacion: es un probe de disponibilidad; el rate-limit del
  gateway lo protege. Cada chequeo esta acotado en tiempo y aislado en try/except
  para que un fallo de dependencia nunca tumbe el propio endpoint.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Tuple

import httpx
from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool

from config import CHROMA_DIR, EMBED_MODEL, OLLAMA_BASE_URL, TEXT_MODEL
from services import db_service
from services.moodle_ws_client import MoodleWSClient

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])

_HTTP_TIMEOUT = 5.0
_WS_TIMEOUT = 5.0


def _check_moodle_db() -> str:
    """`ok` (MariaDB Moodle), `sqlite` (fallback dev) o `error`."""
    try:
        with db_service.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.fetchone()
            cur.close()
        return "ok" if db_service.using_moodle_db() else "sqlite"
    except Exception:  # pragma: no cover - depende del entorno
        logger.warning("health_moodle_db_error", exc_info=True)
        return "error"


def _check_chroma() -> Tuple[str, Optional[int]]:
    """`ok` + nº de chunks indexados, o `error`."""
    try:
        import chromadb

        client = chromadb.PersistentClient(path=CHROMA_DIR)
        total = 0
        for col in client.list_collections():
            total += col.count()
        return "ok", total
    except Exception:  # pragma: no cover
        logger.warning("health_chroma_error", exc_info=True)
        return "error", None


def _model_present(model: str, names: set) -> bool:
    if not model:
        return False
    if model in names:
        return True
    base = model.split(":")[0]
    return any(n == model or n.startswith(model + ":") or n.split(":")[0] == base for n in names)


def _check_ollama() -> Tuple[str, Dict[str, bool]]:
    """`ok`/`error` + presencia de los modelos chat/embedding configurados."""
    try:
        resp = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=_HTTP_TIMEOUT)
        resp.raise_for_status()
        names = {m.get("name") for m in resp.json().get("models", []) if isinstance(m, dict)}
        return "ok", {
            "chat": _model_present(TEXT_MODEL, names),
            "embedding": _model_present(EMBED_MODEL, names),
        }
    except Exception:  # pragma: no cover
        logger.warning("health_ollama_error", exc_info=True)
        return "error", {"chat": False, "embedding": False}


async def _check_moodle_ws() -> str:
    """`ok`, `unavailable` (sin configurar) o `error`."""
    client = MoodleWSClient(timeout=_WS_TIMEOUT)
    if not client.configured:
        return "unavailable"
    try:
        await client.call("core_webservice_get_site_info")
        return "ok"
    except Exception:  # pragma: no cover
        logger.warning("health_moodle_ws_error", exc_info=True)
        return "error"
    finally:
        await client.aclose()


@router.get("/health")
async def health() -> Dict[str, Any]:
    """Estado agregado de disponibilidad. Nunca lanza; nunca expone secretos."""
    moodle_db = await run_in_threadpool(_check_moodle_db)
    chroma, chroma_chunks = await run_in_threadpool(_check_chroma)
    ollama, models_present = await run_in_threadpool(_check_ollama)
    moodle_ws = await _check_moodle_ws()

    # Estado global. Criticos: BD, Chroma, Ollama. `moodle_ws`, el fallback SQLite y
    # modelos ausentes degradan (no rompen) la disponibilidad.
    critical = (moodle_db, chroma, ollama)
    if any(state == "error" for state in critical):
        status = "error"
    elif (
        moodle_db == "sqlite"
        or moodle_ws in ("error", "unavailable")
        or not all(models_present.values())
    ):
        status = "degraded"
    else:
        status = "ok"

    return {
        "status": status,
        "fastapi": "ok",
        "moodle_db": moodle_db,
        "moodle_ws": moodle_ws,
        "chroma": chroma,
        "ollama": ollama,
        "models": {
            "chat": TEXT_MODEL,
            "embedding": EMBED_MODEL,
        },
        "details": {
            "chroma_chunks": chroma_chunks,
            "ollama_models_present": models_present,
            "db_backend": "moodle" if moodle_db == "ok" else ("sqlite" if moodle_db == "sqlite" else "unknown"),
        },
    }
