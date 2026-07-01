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

# Moodle Web Services (sincronizacion FastAPI -> Moodle).
# El token se emite en Moodle: Site administration -> Server -> Manage tokens.
MOODLE_WS_BASE = os.getenv("MOODLE_WS_BASE", "http://moodle:8080/webservice/rest/server.php")
MOODLE_WS_TOKEN = os.getenv("MOODLE_WS_TOKEN", "")
