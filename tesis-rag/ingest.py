import hashlib
import json
import os
import re

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


embeddings = OllamaEmbeddings(model="nomic-embed-text")

PDF_CHUNK_SIZE = 900
PDF_CHUNK_OVERLAP = 160
TRANSCRIPT_CHUNK_SIZE = 1200
TRANSCRIPT_CHUNK_OVERLAP = 120

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documentos")
OFFICIAL_DIR = os.path.join(DOCUMENTS_DIR, "oficial")
LOCATION_DIR = os.path.join(DOCUMENTS_DIR, "localizacion")
EXTERNAL_DIR = os.path.join(DOCUMENTS_DIR, "externo")
NO_INDEX_DIR = os.path.join(DOCUMENTS_DIR, "no_indexar")

READY_STATUS = "ready_for_indexing"
SAFE_SOURCE_ORIGIN = "course"
SAFE_EXTENSIONS = (".json", ".md", ".pdf")


def get_vector_store():
    return Chroma(persist_directory="./bd_vectorial", embedding_function=embeddings)


def _normalizar_path(filepath: str) -> str:
    return filepath.replace("\\", "/")


def _abs_path(path: str) -> str:
    return os.path.abspath(path)


def _esta_dentro(filepath: str, directory: str) -> bool:
    try:
        return os.path.commonpath([_abs_path(filepath), _abs_path(directory)]) == _abs_path(directory)
    except ValueError:
        return False


def _es_ruta_permitida(filepath: str) -> bool:
    return (
        _esta_dentro(filepath, OFFICIAL_DIR)
        or _esta_dentro(filepath, LOCATION_DIR)
    ) and not (
        _esta_dentro(filepath, EXTERNAL_DIR)
        or _esta_dentro(filepath, NO_INDEX_DIR)
    )


def _leer_json_seguro(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _leer_frontmatter_md(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read(4000)
    except Exception:
        return {}

    if not text.startswith("---"):
        return {}

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}

    metadata = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata


def _sidecar_metadata_pdf(filepath: str):
    base, _ = os.path.splitext(filepath)
    for sidecar in (f"{base}.json", f"{base}.metadata.json"):
        data = _leer_json_seguro(sidecar)
        if isinstance(data, dict):
            return data
    return {}


def obtener_metadata_documental(filepath: str):
    filepath_lower = filepath.lower()
    if filepath_lower.endswith(".json"):
        data = _leer_json_seguro(filepath)
        return data if isinstance(data, dict) else {}
    if filepath_lower.endswith(".md"):
        return _leer_frontmatter_md(filepath)
    if filepath_lower.endswith(".pdf"):
        return _sidecar_metadata_pdf(filepath)
    return {}


def es_documento_aprobado_para_indexar(filepath: str, explicar: bool = False):
    razones = []

    if not os.path.exists(filepath):
        razones.append("archivo no existe")
    if not filepath.lower().endswith(SAFE_EXTENSIONS):
        razones.append("extension no soportada por ingesta segura")
    if not _es_ruta_permitida(filepath):
        razones.append("ruta fuera de documentos/oficial o documentos/localizacion")

    metadata = obtener_metadata_documental(filepath)
    status = metadata.get("status", "")
    source_origin = metadata.get("source_origin", "")

    if status != READY_STATUS:
        razones.append(f"status='{status or 'missing'}' distinto de '{READY_STATUS}'")
    if source_origin != SAFE_SOURCE_ORIGIN:
        razones.append(f"source_origin='{source_origin or 'missing'}' distinto de '{SAFE_SOURCE_ORIGIN}'")

    aprobado = not razones
    if explicar:
        return aprobado, razones, metadata
    return aprobado


def get_safe_document_candidates():
    archivos = []
    for root_dir in (OFFICIAL_DIR, LOCATION_DIR):
        if not os.path.exists(root_dir):
            continue
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [
                d for d in dirs
                if not _esta_dentro(os.path.join(root, d), EXTERNAL_DIR)
                and not _esta_dentro(os.path.join(root, d), NO_INDEX_DIR)
            ]
            for filename in files:
                if filename.lower().endswith(SAFE_EXTENSIONS):
                    archivos.append(os.path.join(root, filename))
    return archivos


def get_approved_documents():
    return [
        filepath
        for filepath in get_safe_document_candidates()
        if es_documento_aprobado_para_indexar(filepath)
    ]


def _valor_metadata(valor, fallback=""):
    if valor is None:
        return fallback
    if isinstance(valor, (str, int, float, bool)):
        return valor
    return str(valor)


def _stem(filename: str) -> str:
    return os.path.splitext(filename)[0]


def _inferir_modulo_desde_nombre(filename: str):
    match = re.search(r"m[oó]dulo\s*(\d+)", filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return ""


def _inferir_course(filepath: str) -> str:
    parts = _normalizar_path(filepath).split("/")
    if "documentos" in parts:
        idx = parts.index("documentos")
        if idx > 0 and parts[idx - 1] not in (".", "tesis-rag"):
            return parts[idx - 1]
    return "curso mezcla y masterizacion"


def _crear_chunk_id(filepath: str, chunk_index: int, prefix: str = "", page="") -> str:
    raw = f"{_normalizar_path(filepath)}|{prefix}|{page}|{chunk_index}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()[:16]


def _metadata_base(filepath: str, doc_type: str, chunk_index: int, chunk_id: str):
    filename = os.path.basename(filepath)
    doc_meta = obtener_metadata_documental(filepath)
    return {
        "source": _normalizar_path(filepath),
        "filename": filename,
        "doc_type": doc_meta.get("doc_type", doc_type),
        "source_origin": doc_meta.get("source_origin", ""),
        "status": doc_meta.get("status", ""),
        "course": doc_meta.get("course_id", "") or _inferir_course(filepath),
        "course_id": doc_meta.get("course_id", ""),
        "module_id": doc_meta.get("module_id", ""),
        "module_title": doc_meta.get("module_title", ""),
        "version": doc_meta.get("version", ""),
        "chunk_index": chunk_index,
        "chunk_id": chunk_id,
    }


def _metadata_pdf(filepath: str, page, chunk_index: int):
    filename = os.path.basename(filepath)
    module = _inferir_modulo_desde_nombre(filename)
    chunk_id = _crear_chunk_id(filepath, chunk_index, "pdf", page)
    metadata = _metadata_base(filepath, "pdf", chunk_index, chunk_id)
    metadata.update({
        "module": module,
        "modulo": module,
        "submodule": "",
        "submodulo": "",
        "lesson_title": _stem(filename),
        "topic": _stem(filename),
        "tema": _stem(filename),
        "learning_objective": "",
        "resource_title": _stem(filename),
        "resource_type": "pdf",
        "url": "",
        "url_video": "",
        "start_time": "",
        "end_time": "",
        "page": page,
    })
    return metadata


def _parse_time(value):
    if value in ("", None):
        return ""
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value).strip()
    if text.isdigit():
        return int(text)
    parts = text.split(":")
    if all(part.isdigit() for part in parts):
        total = 0
        for part in parts:
            total = total * 60 + int(part)
        return total
    return text


def _url_con_tiempo(url: str, start_time):
    if not url or start_time in ("", None):
        return url or ""
    if "time=" in url or "t=" in url:
        return url
    separator = "&" if "?" in url else "?"
    return f"{url}{separator}time={start_time}"


def _extraer_tiempo_desde_url(url: str):
    if not url:
        return ""
    match = re.search(r"(?:[?&](?:time|t)=)(\d+)", url)
    if match:
        return int(match.group(1))
    return ""


def _extraer_items_json(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in (
            "segments", "segmentos", "items", "terms", "resources",
            "errors", "activities", "locations", "transcript", "transcripcion"
        ):
            value = data.get(key)
            if isinstance(value, list):
                return value
        return [data]
    return []


def _contenido_item_json(item: dict):
    contenido = (
        item.get("contenido", "")
        or item.get("content", "")
        or item.get("texto", "")
        or item.get("text", "")
    )
    if contenido:
        return contenido

    preferred_keys = [
        "question", "canonical_answer", "short_answer",
        "term", "definition", "common_confusion",
        "resource_title", "summary", "review_purpose",
        "title", "description", "tutor_response_rule",
        "objective", "student_task",
        "topic", "learning_objective", "notes",
    ]
    lines = []
    for key in preferred_keys:
        value = item.get(key)
        if value not in ("", None, [], {}):
            lines.append(f"{key}: {value}")

    if lines:
        return "\n".join(lines)

    return json.dumps(item, ensure_ascii=False)


def _metadata_transcripcion(filepath: str, item: dict, chunk_index: int, parent_meta: dict = None):
    parent_meta = parent_meta or {}
    filename = os.path.basename(filepath)
    item_id = item.get("id", "") or item.get("chunk_id", "") or f"segment_{chunk_index}"
    start_time = _parse_time(item.get("start_time", item.get("inicio", item.get("start", ""))))
    end_time = _parse_time(item.get("end_time", item.get("fin", item.get("end", ""))))
    url = item.get("url", "") or item.get("url_video", "")
    if start_time == "":
        start_time = _extraer_tiempo_desde_url(url)
    url = _url_con_tiempo(url, start_time)
    titulo = (
        item.get("lesson_title", "")
        or item.get("titulo", "")
        or parent_meta.get("module_title", "")
        or _stem(filename)
    )
    tema = item.get("topic", "") or item.get("tema", "") or titulo
    recurso = (
        item.get("resource_title", "")
        or item.get("recurso_recomendado", "")
        or item.get("recurso", "")
    )
    module = item.get("module", item.get("modulo", "")) or parent_meta.get("module_id", "")
    submodule = item.get("submodule", item.get("submodulo", ""))
    chunk_id = item.get("chunk_id", "") or _crear_chunk_id(filepath, chunk_index, item_id, start_time)

    metadata = _metadata_base(filepath, parent_meta.get("doc_type", "video_transcript"), chunk_index, chunk_id)
    metadata.update({
        "id": _valor_metadata(item_id),
        "module": _valor_metadata(module),
        "modulo": _valor_metadata(module),
        "submodule": _valor_metadata(submodule),
        "submodulo": _valor_metadata(submodule),
        "lesson_title": _valor_metadata(titulo),
        "topic": _valor_metadata(tema),
        "tema": _valor_metadata(tema),
        "learning_objective": _valor_metadata(
            item.get("learning_objective", "")
            or item.get("objetivo_aprendizaje", "")
            or parent_meta.get("learning_objective", "")
        ),
        "resource_title": _valor_metadata(recurso),
        "resource_type": _valor_metadata(
            item.get("resource_type", "")
            or item.get("tipo_recurso", "")
            or parent_meta.get("doc_type", "json")
        ),
        "recurso_recomendado": _valor_metadata(recurso),
        "recurso": _valor_metadata(recurso),
        "url": _valor_metadata(url),
        "url_video": _valor_metadata(url),
        "start_time": _valor_metadata(start_time),
        "end_time": _valor_metadata(end_time),
        "page": "",
    })
    return metadata


def _texto_chunk(page_content: str, metadata: dict) -> str:
    partes = [
        f"Tipo de documento: {metadata.get('doc_type', '')}",
        f"Modulo: {metadata.get('module', '')}",
        f"Submodulo: {metadata.get('submodule', '')}",
        f"Clase: {metadata.get('lesson_title', '')}",
        f"Tema: {metadata.get('topic', '')}",
        f"Objetivo: {metadata.get('learning_objective', '')}",
        f"Recurso: {metadata.get('resource_title', '')}",
        f"Tiempo: {metadata.get('start_time', '')}-{metadata.get('end_time', '')}",
        "Contenido:",
        page_content,
    ]
    return "\n".join(str(parte) for parte in partes if parte not in ("", None))


def _crear_chunks_pdf(filepath: str):
    loader = PyPDFLoader(filepath)
    documentos = loader.load()

    if not documentos:
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=PDF_CHUNK_SIZE,
        chunk_overlap=PDF_CHUNK_OVERLAP,
    )
    chunks = []
    chunk_index = 0

    for doc in documentos:
        page_raw = doc.metadata.get("page", "")
        page = page_raw + 1 if isinstance(page_raw, int) else page_raw
        for text in text_splitter.split_text(doc.page_content or ""):
            metadata = _metadata_pdf(filepath, page, chunk_index)
            chunks.append(Document(page_content=_texto_chunk(text, metadata), metadata=metadata))
            chunk_index += 1

    return chunks


def _crear_chunks_json(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    parent_meta = data if isinstance(data, dict) else {}
    items = _extraer_items_json(data)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=TRANSCRIPT_CHUNK_SIZE,
        chunk_overlap=TRANSCRIPT_CHUNK_OVERLAP,
    )
    chunks = []

    for item in items:
        if not isinstance(item, dict):
            continue
        contenido = _contenido_item_json(item)
        if not contenido:
            continue

        for chunk_str in text_splitter.split_text(contenido):
            chunk_index = len(chunks)
            metadata = _metadata_transcripcion(filepath, item, chunk_index, parent_meta)
            chunks.append(Document(page_content=_texto_chunk(chunk_str, metadata), metadata=metadata))

    return chunks


def _crear_chunks_markdown(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    metadata_doc = _leer_frontmatter_md(filepath)
    content = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            content = parts[2].strip()

    if not content:
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=TRANSCRIPT_CHUNK_SIZE,
        chunk_overlap=TRANSCRIPT_CHUNK_OVERLAP,
    )

    chunks = []
    for chunk_str in text_splitter.split_text(content):
        chunk_index = len(chunks)
        chunk_id = _crear_chunk_id(filepath, chunk_index, "md")
        metadata = _metadata_base(filepath, metadata_doc.get("doc_type", "markdown"), chunk_index, chunk_id)
        metadata.update({
            "module": metadata_doc.get("module_id", ""),
            "modulo": metadata_doc.get("module_id", ""),
            "submodule": "",
            "submodulo": "",
            "lesson_title": metadata_doc.get("module_title", "") or _stem(os.path.basename(filepath)),
            "topic": metadata_doc.get("module_title", "") or _stem(os.path.basename(filepath)),
            "tema": metadata_doc.get("module_title", "") or _stem(os.path.basename(filepath)),
            "learning_objective": "",
            "resource_title": _stem(os.path.basename(filepath)),
            "resource_type": metadata_doc.get("resource_type", "markdown"),
            "url": "",
            "url_video": "",
            "start_time": "",
            "end_time": "",
            "page": "",
        })
        chunks.append(Document(page_content=_texto_chunk(chunk_str, metadata), metadata=metadata))

    return chunks


def add_single_document(filepath: str):
    """
    Lee un PDF o JSON, lo procesa y lo anade a Chroma de forma incremental,
    borrando primero los chunks previos del mismo source para evitar duplicados.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El archivo {filepath} no existe.")

    aprobado, razones, _ = es_documento_aprobado_para_indexar(filepath, explicar=True)
    if not aprobado:
        return {
            "success": False,
            "skipped": True,
            "message": f"Documento omitido por politica de ingesta segura: {os.path.basename(filepath)}",
            "reasons": razones,
        }

    print(f"Leyendo el documento: {filepath}...")

    filename = os.path.basename(filepath)
    filepath_lower = filepath.lower()

    if filepath_lower.endswith(".pdf"):
        chunks = _crear_chunks_pdf(filepath)
        if not chunks:
            return {"success": False, "message": "El documento esta vacio o no se pudo leer."}
    elif filepath_lower.endswith(".json"):
        chunks = _crear_chunks_json(filepath)
        if not chunks:
            return {"success": False, "message": "El JSON no contiene texto valido."}
    elif filepath_lower.endswith(".md"):
        chunks = _crear_chunks_markdown(filepath)
        if not chunks:
            return {"success": False, "message": "El Markdown no contiene texto valido."}
    else:
        return {"success": False, "message": "Formato de archivo no soportado."}

    remove_single_document(filepath)

    print("Anadiendo a ChromaDB...")
    db = get_vector_store()
    db.add_documents(chunks)

    return {
        "success": True,
        "message": f"Documento '{filename}' vectorizado correctamente.",
        "chunks": len(chunks),
    }


def remove_single_document(filepath: str):
    """
    Elimina los fragmentos de un documento especifico de ChromaDB por su source.
    """
    db = get_vector_store()
    collection = db._collection

    try:
        collection.delete(where={"source": filepath})
        collection.delete(where={"source": _normalizar_path(filepath)})
        collection.delete(where={"source": filepath.replace("/", "\\")})
        collection.delete(where={"source": filepath.replace("\\", "/")})
    except Exception as e:
        print(f"Nota al borrar documento (puede no existir previamente): {e}")

    filename = os.path.basename(filepath)
    return {"success": True, "message": f"Documento '{filename}' eliminado de la IA."}


def get_indexed_documents():
    """
    Consulta ChromaDB para obtener una lista unica de documentos indexados.
    """
    try:
        db = get_vector_store()
        collection = db._collection
        result = collection.get(include=["metadatas"])

        indexed_files = set()
        if result and "metadatas" in result and result["metadatas"]:
            for meta in result["metadatas"]:
                if meta and "source" in meta:
                    indexed_files.add(os.path.basename(meta["source"]))

        return list(indexed_files)
    except Exception as e:
        print(f"Error consultando documentos indexados: {e}")
        return []


def process_all_documents():
    """
    Sincroniza solo documentos oficiales/localizacion explicitamente aprobados.
    """
    archivos = get_approved_documents()

    processed = 0
    skipped = 0
    for filepath in archivos:
        result = add_single_document(filepath)
        if result.get("success"):
            processed += 1
        else:
            skipped += 1

    return {
        "success": True,
        "message": "Documentos oficiales aprobados sincronizados.",
        "processed": processed,
        "skipped": skipped,
        "candidates": len(get_safe_document_candidates()),
    }


def rebuild_all_documents():
    """
    Elimina TODA la base vectorial de Chroma y re-indexa todos los documentos
    desde cero. Usar cuando se modifico ingest.py, chunking o metadatos y se
    quiere que los documentos ya indexados tomen la nueva logica.
    """
    import chromadb

    persist_dir = "./bd_vectorial"

    # Paso 1: Borrar la coleccion de Chroma usando su API nativa
    # (No podemos borrar la carpeta en Windows porque los archivos estan bloqueados
    # por el proceso de FastAPI que mantiene la conexion abierta)
    try:
        print("[REBUILD] Conectando a ChromaDB para resetear la coleccion...")
        client = chromadb.PersistentClient(path=persist_dir)
        collections = client.list_collections()
        for col in collections:
            print(f"[REBUILD] Eliminando coleccion: {col.name}")
            client.delete_collection(col.name)
        print("[REBUILD] Todas las colecciones eliminadas.")
    except Exception as e:
        print(f"[REBUILD] Error al resetear colecciones (puede ser primera vez): {e}")

    # Paso 2: Re-procesar todos los documentos (esto recrea la coleccion)
    print("[REBUILD] Re-indexando todos los documentos desde cero...")
    result = process_all_documents()
    print(f"[REBUILD] Completado. {result['processed']} documentos procesados.")
    return {
        "success": True,
        "message": f"Rebuild completo. {result['processed']} documentos re-indexados desde cero.",
        "processed": result["processed"],
    }
