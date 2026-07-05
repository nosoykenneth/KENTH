import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEXT_MODEL = os.getenv("KENTH_TEXT_MODEL", "llama3.2:3b")
VISION_MODEL = os.getenv("KENTH_VISION_MODEL", "qwen3-vl:4b-instruct")
EMBED_MODEL = os.getenv("KENTH_EMBED_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# ==========================================
# Selección de modelos por TAREA para el asistente "Preparar tutor con IA".
# Todo configurable por entorno; nada hardcodeado en el agente. Lo consume
# services/ai_prepare/models.py::get_model_for(task). NO re-cablea el chat/visión/
# embeddings en vivo (esos siguen usando KENTH_*): esta capa es aditiva.
# Reglas del diseño: qwen2.5:14b-instruct genera el JSON pedagógico; la revisión
# quality=max usa un modelo más fuerte SOLO si está configurado; deepseek-r1:70b
# NUNCA es el default (hay que ponerlo explícito en AI_PREP_REVIEW_MODEL).
# Los embeddings NO se tocan en esta rama (evita forzar reindex): nomic-embed-text.
# ==========================================
AI_PREP_MODEL = os.getenv("AI_PREP_MODEL", "qwen2.5:14b-instruct")
AI_PREP_REVIEW_MODEL = os.getenv("AI_PREP_REVIEW_MODEL", "deepseek-r1:32b")
AI_PREP_LONG_CONTEXT_MODEL = os.getenv("AI_PREP_LONG_CONTEXT_MODEL", "command-r:latest")
AI_VISION_MODEL = os.getenv("AI_VISION_MODEL", VISION_MODEL)
AI_CHAT_MODEL = os.getenv("AI_CHAT_MODEL", "llama3.1:8b")
AI_EMBEDDING_MODEL = os.getenv("AI_EMBEDDING_MODEL", EMBED_MODEL)

# Parámetros de ejecución del asistente IA (timeout/retry/contexto). El chat en
# vivo NO define ninguno hoy; aquí sí, porque un modelo 14B/32B sobre una
# transcripción larga puede colgarse sin límite.
AI_PREP_TIMEOUT = float(os.getenv("AI_PREP_TIMEOUT", "300"))
AI_PREP_NUM_CTX = int(os.getenv("AI_PREP_NUM_CTX", "16384"))
AI_PREP_MAX_RETRIES = int(os.getenv("AI_PREP_MAX_RETRIES", "1"))
# Umbral (caracteres) sobre el que la transcripción se resume jerárquicamente con
# el modelo de contexto largo antes de generar el borrador.
AI_PREP_LONG_CONTEXT_THRESHOLD = int(os.getenv("AI_PREP_LONG_CONTEXT_THRESHOLD", "18000"))
# Tope duro de caracteres de transcripción que se procesan (seguridad/coste).
AI_PREP_TRANSCRIPT_CHAR_LIMIT = int(os.getenv("AI_PREP_TRANSCRIPT_CHAR_LIMIT", "60000"))
_CHROMA_DIR = os.getenv("CHROMA_DIR", "./bd_vectorial")
CHROMA_DIR = _CHROMA_DIR if os.path.isabs(_CHROMA_DIR) else os.path.join(BASE_DIR, _CHROMA_DIR)


def _as_flag(value: str, default: bool) -> bool:
    v = str(value if value is not None else "").strip().lower()
    if v in ("1", "true", "yes", "on", "si", "sí"):
        return True
    if v in ("0", "false", "no", "off"):
        return False
    return default


# ==========================================
# FLUJO DOCENTE (teacher-driven RAG). Fase 3.
# La transcripción CRUDA de Whisper NO es evidencia final hasta que el profesor la
# apruebe/edite. Con el flag activo (default seguro para PRODUCCIÓN) el job de
# Whisper deja la transcripción en estado `generated_pending_review` y NO la indexa;
# se indexa recién cuando el profesor la aprueba/edita (PUT transcript) o la importa.
# En test/dev se puede poner en false para indexar de inmediato (compat histórica).
# ==========================================
INDEX_TRANSCRIPT_ONLY_AFTER_APPROVAL = _as_flag(
    os.getenv("INDEX_TRANSCRIPT_ONLY_AFTER_APPROVAL"), True
)

# Estados de transcripción (contrato único del backend, evita strings mágicos).
TRANSCRIPT_STATUS_PENDING = "generated_pending_review"  # Whisper crudo, sin revisar
TRANSCRIPT_STATUS_APPROVED = "approved"                 # aprobada explícitamente
TRANSCRIPT_STATUS_EDITED = "edited"                     # corregida por el profesor
# Estados que cuentan como "aprobada" -> sí se indexa como evidencia.
TRANSCRIPT_APPROVED_STATES = (TRANSCRIPT_STATUS_APPROVED, TRANSCRIPT_STATUS_EDITED)


def transcript_is_approved(status: str) -> bool:
    """True si un estado de transcripción cuenta como aprobado (indexable)."""
    return str(status or "").strip().lower() in TRANSCRIPT_APPROVED_STATES

# Moodle Web Services (sincronizacion FastAPI -> Moodle).
# El token se emite en Moodle: Site administration -> Server -> Manage tokens.
MOODLE_WS_BASE = os.getenv("MOODLE_WS_BASE", "http://moodle:8080/webservice/rest/server.php")
MOODLE_WS_TOKEN = os.getenv("MOODLE_WS_TOKEN", "")
