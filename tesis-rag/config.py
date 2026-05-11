import os

TEXT_MODEL = os.getenv("KENTH_TEXT_MODEL", "llama3.2:3b")
VISION_MODEL = os.getenv("KENTH_VISION_MODEL", "qwen3-vl:4b-instruct")
EMBED_MODEL = os.getenv("KENTH_EMBED_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./bd_vectorial")
