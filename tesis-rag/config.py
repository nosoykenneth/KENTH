import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEXT_MODEL = os.getenv("KENTH_TEXT_MODEL", "llama3.2:3b")
VISION_MODEL = os.getenv("KENTH_VISION_MODEL", "qwen3-vl:4b-instruct")
EMBED_MODEL = os.getenv("KENTH_EMBED_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
_CHROMA_DIR = os.getenv("CHROMA_DIR", "./bd_vectorial")
CHROMA_DIR = _CHROMA_DIR if os.path.isabs(_CHROMA_DIR) else os.path.join(BASE_DIR, _CHROMA_DIR)

# Moodle Web Services (sincronizacion FastAPI -> Moodle).
# El token se emite en Moodle: Site administration -> Server -> Manage tokens.
MOODLE_WS_BASE = os.getenv("MOODLE_WS_BASE", "http://moodle:8080/webservice/rest/server.php")
MOODLE_WS_TOKEN = os.getenv("MOODLE_WS_TOKEN", "")
