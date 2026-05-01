from fastapi import FastAPI
from api.routes import chat, documents

app = FastAPI(
    title="KENTH AI - RAG System",
    description="Sistema de RAG para Mezcla y Masterización",
    version="1.0.0"
)

# Incluir las rutas
app.include_router(chat.router)
app.include_router(documents.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
