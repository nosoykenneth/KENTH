from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
import os
import shutil
from typing import List, Optional
from pydantic import BaseModel

from ingest import (
    add_single_document,
    remove_single_document,
    get_indexed_documents,
    process_all_documents,
    rebuild_all_documents,
    get_safe_document_candidates,
    es_documento_aprobado_para_indexar,
)

router = APIRouter(prefix="/documents", tags=["Documents"])

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documentos")
OFFICIAL_DIR = os.path.join(DOCUMENTS_DIR, "oficial")
LOCATION_DIR = os.path.join(DOCUMENTS_DIR, "localizacion")
NO_INDEX_UPLOADS_DIR = os.path.join(DOCUMENTS_DIR, "no_indexar", "uploads")

os.makedirs(OFFICIAL_DIR, exist_ok=True)
os.makedirs(LOCATION_DIR, exist_ok=True)
os.makedirs(NO_INDEX_UPLOADS_DIR, exist_ok=True)


def get_all_filepaths():
    return get_safe_document_candidates()


# Estado en memoria para archivos que se estan procesando
# Formato: {"filename": "processing" | "error: detalle"}
processing_status = {}


class DocumentInfo(BaseModel):
    filename: str
    size_bytes: int
    is_indexed: bool
    status: str  # indexed | ready | blocked | processing | failed
    error_msg: Optional[str] = None


@router.get("/", response_model=List[DocumentInfo])
def list_documents():
    """Lista candidatos de ingesta segura y su estado."""
    try:
        indexed_files = get_indexed_documents()
        files = []
        for filepath in get_all_filepaths():
            filename = os.path.basename(filepath)
            size = os.path.getsize(filepath)
            is_indexed = filename in indexed_files

            approved, reasons, _ = es_documento_aprobado_para_indexar(filepath, explicar=True)
            status = "indexed" if is_indexed else ("ready" if approved else "blocked")
            error_msg = None if approved else "; ".join(reasons)

            if filename in processing_status:
                if processing_status[filename] == "processing":
                    status = "processing"
                    error_msg = None
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
        result = add_single_document(filepath)
        if not result.get("success"):
            processing_status[filename] = result.get("message", "Documento omitido por politica segura")
            return
        if filename in processing_status:
            del processing_status[filename]
    except Exception as e:
        print(f"Error procesando {filename}: {e}")
        processing_status[filename] = f"Error: {str(e)}"


@router.post("/upload")
def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Sube archivos a no_indexar/uploads. No se indexan automaticamente.
    Para indexar, mover a documentos/oficial o documentos/localizacion y
    marcar status=ready_for_indexing + source_origin=course.
    """
    if not file.filename.endswith((".pdf", ".json", ".md")):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF, JSON y Markdown")

    filepath = os.path.join(NO_INDEX_UPLOADS_DIR, file.filename)

    try:
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "success": True,
            "message": (
                f"Archivo '{file.filename}' subido a no_indexar/uploads. "
                "No fue indexado automaticamente."
            )
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando archivo: {str(e)}")


@router.delete("/{filename}")
def delete_document(background_tasks: BackgroundTasks, filename: str):
    """Elimina un candidato seguro o upload no_indexar y borra su memoria vectorial si existia."""
    filepath = None
    for candidate in get_all_filepaths():
        if os.path.basename(candidate) == filename:
            filepath = candidate
            break

    if filepath is None:
        upload_candidate = os.path.join(NO_INDEX_UPLOADS_DIR, filename)
        if os.path.exists(upload_candidate):
            filepath = upload_candidate

    if filepath and os.path.exists(filepath):
        try:
            os.remove(filepath)
            background_tasks.add_task(remove_single_document, filepath)
            return {"success": True, "message": f"Archivo '{filename}' eliminado."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error eliminando archivo: {str(e)}")

    raise HTTPException(status_code=404, detail="Archivo no encontrado")


def run_process_all_documents():
    try:
        indexed_files = get_indexed_documents()
        archivos = get_all_filepaths()
        for filepath in archivos:
            filename = os.path.basename(filepath)
            if es_documento_aprobado_para_indexar(filepath) and filename not in indexed_files:
                processing_status[filename] = "processing"

        process_all_documents()

        for filename in list(processing_status.keys()):
            if processing_status[filename] == "processing":
                del processing_status[filename]
    except Exception as e:
        print(f"Error en process_all: {e}")


def run_rebuild_all_documents():
    """Borra la BD vectorial y re-indexa solo documentos aprobados por politica segura."""
    try:
        processing_status.clear()

        for filepath in get_all_filepaths():
            filename = os.path.basename(filepath)
            if es_documento_aprobado_para_indexar(filepath):
                processing_status[filename] = "processing"

        rebuild_all_documents()

        for filename in list(processing_status.keys()):
            if processing_status[filename] == "processing":
                del processing_status[filename]
    except Exception as e:
        print(f"Error en rebuild_all: {e}")
        for key in list(processing_status.keys()):
            if processing_status[key] == "processing":
                processing_status[key] = f"Error: {str(e)}"


@router.post("/index")
def index_documents(background_tasks: BackgroundTasks):
    """Sincroniza en segundo plano solo documentos oficiales aprobados."""
    try:
        background_tasks.add_task(run_process_all_documents)
        return {"success": True, "message": "Proceso de ingesta segura iniciado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rebuild")
def rebuild_documents(background_tasks: BackgroundTasks):
    """Rebuild completo, limitado a documentos aprobados por politica segura."""
    try:
        background_tasks.add_task(run_rebuild_all_documents)
        return {
            "success": True,
            "message": "Rebuild seguro iniciado. Solo se re-indexaran documentos ready_for_indexing/source_origin=course."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
