import logging
import sys
import time
import uuid
import warnings

from langchain_core._api.deprecation import LangChainPendingDeprecationWarning
from fastapi import FastAPI, Request

warnings.filterwarnings(
    "ignore",
    message=r"The default value of `allowed_objects` will change in a future version\..*",
    category=LangChainPendingDeprecationWarning,
)

# Configuracion temprana de logging JSON (antes de importar modulos que loguean en su carga).
try:
    from pythonjsonlogger import jsonlogger

    _handler = logging.StreamHandler(sys.stdout)
    _formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={"asctime": "time", "levelname": "level", "name": "logger"},
    )
    _handler.setFormatter(_formatter)
    _root = logging.getLogger()
    _root.handlers = [_handler]
    _root.setLevel(logging.INFO)
    # Uvicorn ya configura sus loggers; los apuntamos al mismo handler para mantener formato JSON.
    for _name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        _logger = logging.getLogger(_name)
        _logger.handlers = [_handler]
        _logger.propagate = False
except ImportError:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

from api.routes import chat, documents, chat_sessions, axes, moodle, authoring, course_documents
from services.db_service import init_db

# Inicializar base de datos
init_db()

app = FastAPI(
    title="KENTH AI - RAG System",
    description="Sistema de RAG para Mezcla y Masterización",
    version="1.0.0",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Emite un log JSON por cada request con request_id, latencia y user_id."""
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    start = time.perf_counter()
    user_id = request.headers.get("x-user-id", "")
    try:
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000.0
        logging.getLogger("tesis_rag.request").info(
            "request_handled",
            extra={
                "request_id": request_id,
                "path": request.url.path,
                "method": request.method,
                "status": response.status_code,
                "duration_ms": round(duration_ms, 2),
                "user_id": user_id,
            },
        )
        response.headers["X-Request-ID"] = request_id
        return response
    except Exception as exc:
        duration_ms = (time.perf_counter() - start) * 1000.0
        logging.getLogger("tesis_rag.request").exception(
            "request_failed",
            extra={
                "request_id": request_id,
                "path": request.url.path,
                "method": request.method,
                "duration_ms": round(duration_ms, 2),
                "user_id": user_id,
                "error": str(exc),
            },
        )
        raise


# Incluir las rutas
app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(chat_sessions.router)
app.include_router(axes.router)
app.include_router(moodle.router)
app.include_router(authoring.router)
app.include_router(course_documents.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
