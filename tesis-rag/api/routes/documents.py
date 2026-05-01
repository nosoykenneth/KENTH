from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import os
import shutil
from typing import List, Optional
from pydantic import BaseModel

# Importamos la lógica de ingesta granular
from ingest import add_single_document, remove_single_document, get_indexed_documents, process_all_documents

router = APIRouter(prefix="/documents", tags=["Documents"])

DOCUMENTS_DIR = "./documentos"

# Asegurar que el directorio de documentos exista al iniciar
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

# Estado en memoria para archivos que se están procesando
# Formato: {"filename": "processing" | "error: detalle"}
processing_status = {}

class DocumentInfo(BaseModel):
    filename: str
    size_bytes: int
    is_indexed: bool
    status: str  # 'indexed', 'unindexed', 'processing', 'failed'
    error_msg: Optional[str] = None

@router.get("/", response_model=List[DocumentInfo])
def list_documents():
    """Obtiene la lista de documentos PDF y su estado de indexación"""
    try:
        indexed_files = get_indexed_documents()
        files = []
        for filename in os.listdir(DOCUMENTS_DIR):
            if filename.endswith(".pdf"):
                filepath = os.path.join(DOCUMENTS_DIR, filename)
                size = os.path.getsize(filepath)
                is_indexed = filename in indexed_files
                
                # Determinar el estado
                status = "indexed" if is_indexed else "unindexed"
                error_msg = None
                
                if filename in processing_status:
                    if processing_status[filename] == "processing":
                        status = "processing"
                    else:
                        status = "failed"
                        error_msg = processing_status[filename]
                
                files.append(DocumentInfo(
                    filename=filename, 
                    size_bytes=size, 
                    is_indexed=is_indexed,
                    status=status,
                    error_msg=error_msg
                ))
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_add_single_document(filepath: str, filename: str):
    processing_status[filename] = "processing"
    try:
        add_single_document(filepath)
        # Si tiene éxito, lo quitamos del estado (el listado lo verá como is_indexed)
        if filename in processing_status:
            del processing_status[filename]
    except Exception as e:
        print(f"Error procesando {filename}: {e}")
        processing_status[filename] = f"Error: {str(e)}"

@router.post("/upload")
def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Sube un nuevo documento PDF e inicia su vectorización individual en segundo plano"""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    
    filepath = os.path.join(DOCUMENTS_DIR, file.filename)
    try:
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Añadir a la base vectorial inmediatamente en background
        background_tasks.add_task(run_add_single_document, filepath, file.filename)
        
        return {"success": True, "message": f"Archivo '{file.filename}' subido y procesando para la IA."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando archivo: {str(e)}")

@router.delete("/{filename}")
def delete_document(background_tasks: BackgroundTasks, filename: str):
    """Elimina un documento PDF de la carpeta y lo borra de la memoria de la IA"""
    filepath = os.path.join(DOCUMENTS_DIR, filename)
    if os.path.exists(filepath) and filename.endswith(".pdf"):
        try:
            os.remove(filepath)
            # Borrar de la base vectorial en background
            background_tasks.add_task(remove_single_document, filename)
            return {"success": True, "message": f"Archivo '{filename}' eliminado."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error eliminando archivo: {str(e)}")
    raise HTTPException(status_code=404, detail="Archivo no encontrado")

def run_process_all_documents():
    # Marcar todos los no indexados como procesando
    try:
        indexed_files = get_indexed_documents()
        archivos = [f for f in os.listdir(DOCUMENTS_DIR) if f.endswith(".pdf")]
        for archivo in archivos:
            if archivo not in indexed_files:
                processing_status[archivo] = "processing"
                
        # Procesar
        process_all_documents()
        
        # Limpiar
        for archivo in archivos:
            if archivo in processing_status and processing_status[archivo] == "processing":
                del processing_status[archivo]
                
    except Exception as e:
        print(f"Error en process_all: {e}")

@router.post("/index")
def index_documents(background_tasks: BackgroundTasks):
    """
    Sincroniza toda la carpeta en segundo plano, añadiendo solo los documentos necesarios.
    """
    try:
        background_tasks.add_task(run_process_all_documents)
        return {"success": True, "message": "Proceso de sincronización general iniciado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
