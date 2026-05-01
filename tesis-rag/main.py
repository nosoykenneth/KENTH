from fastapi import FastAPI
from api.routes import chat, documents, chat_sessions
from services.db_service import init_db

# Inicializar base de datos
init_db()

app = FastAPI(
    title="KENTH AI - RAG System",
    description="Sistema de RAG para Mezcla y Masterización",
    version="1.0.0"
)

# Incluir las rutas
app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(chat_sessions.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
