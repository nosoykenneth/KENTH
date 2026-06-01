import hashlib
import json
import os
import re

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import EMBED_MODEL, CHROMA_DIR


embeddings = OllamaEmbeddings(model=EMBED_MODEL)

PDF_CHUNK_SIZE = 900
PDF_CHUNK_OVERLAP = 160
TRANSCRIPT_CHUNK_SIZE = 1200
TRANSCRIPT_CHUNK_OVERLAP = 120
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documentos")
OFFICIAL_DIR = os.path.join(DOCUMENTS_DIR, "oficial")
EJES_DIR = os.path.join(OFFICIAL_DIR, "ejes")
CONTENT_CANONICO_DIR = os.path.join(EJES_DIR, "contenido_canonico")
COURSE_RUNTIME_DIR = os.path.join(BASE_DIR, "course_runtime")
LOCATION_DIR = os.path.join(DOCUMENTS_DIR, "localizacion")
EXTERNAL_DIR = os.path.join(DOCUMENTS_DIR, "externo")
NO_INDEX_DIR = os.path.join(DOCUMENTS_DIR, "no_indexar")
# Documentos de conocimiento subidos por el profesor, organizados por curso:
# documentos/oficial/cursos/<course_id>/<doc>. Indexables si pasan la politica.
COURSE_UPLOADS_DIR = os.path.join(OFFICIAL_DIR, "cursos")

READY_STATUS = "ready_for_indexing"
SAFE_SOURCE_ORIGIN = "course"
SAFE_EXTENSIONS = (".json", ".md", ".pdf")

ALLOWED_PUBLIC_DIRS = (
    EJES_DIR,
    CONTENT_CANONICO_DIR,
    COURSE_RUNTIME_DIR,
    COURSE_UPLOADS_DIR,
    os.path.join(OFFICIAL_DIR, "modulo_01_fundamentos_acustica_medicion"),
    os.path.join(OFFICIAL_DIR, "modulo_02_estructura_ganancia_flujo_senal"),
    os.path.join(OFFICIAL_DIR, "modulo_03_polaridad_fase_monocompatibilidad"),
    os.path.join(OFFICIAL_DIR, "modulo_04_filtros_ecualizacion"),
    os.path.join(OFFICIAL_DIR, "modulo_05_procesadores_dinamicos"),
    os.path.join(OFFICIAL_DIR, "modulo_06_espacialidad_profundidad_ambiencia"),
    os.path.join(OFFICIAL_DIR, "modulo_07_practica_integradora_mezcla"),
    os.path.join(OFFICIAL_DIR, "modulo_08_masterizacion_optimizacion_comercial"),
)

EXCLUDED_DIR_NAMES = {
    "paquetes_limpios",
    "no_indexar",
    "externo",
    "transcripciones_crudas",
    "transcripciones_corregidas",
    "backups",
    "backup",
    "logs",
    "debug",
    "tmp",
    "temp",
    "__pycache__",
}

ALLOWED_FILE_PATTERNS = (
    r"^01_contenido_canonico\.md$",
    r"^kenth_eje\d+_contenido_canonico\.md$",
    r"^03_glosario\.json$",
    r"^04_heuristicas\.json$",
    r"^05_errores_frecuentes\.json$",
    r"^06_faq\.json$",
    r"^07_recursos\.json$",
    r"^m\d{2}_guia_canonica\.md$",
    r"^m\d{2}_glosario\.json$",
    r"^m\d{2}_faq\.json$",
    r"^m\d{2}_recursos\.json$",
    r"^m\d{2}_actividades\.json$",
    r"^m\d{2}_errores_comunes\.json$",
    r"^manifest\.json$",
    r"^[a-z0-9_-]+\.json$",
)

PROHIBITED_FILE_PATTERNS = (
    r"(^|[/\\])paquetes_limpios([/\\]|$)",
    r"02_paquete_limpio\.md$",
    r".*_paquete_limpio\.md$",
    r".*paquete_limpio.*",
    r".*paquete.*limpio.*",
    r"auditoria_forense_autoria_rabinovich\.md$",
    r".*dossier_fuente.*",
    r".*fuente_protegida.*",
    r".*pdf.*fuente.*",
    r".*transcripci[oó]n.*cruda.*",
    r".*transcripci[oó]n.*corregida.*",
    r".*backup.*",
    r".*\.bak.*",
    r".*log.*",
    r".*debug.*",
    r".*tmp.*",
    r".*temp.*",
)

PROHIBITED_CONTENT_MARKERS = (
    "02_paquete_limpio.md",
    "paquete_limpio",
    "paquetes_limpios",
    "auditoria_forense_autoria_rabinovich",
    "transcripcion cruda",
    "transcripcion corregida",
    "pdf fuente protegido",
    "dossier_fuente",
)


def get_vector_store():
    return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)


def _normalizar_path(filepath: str) -> str:
    return filepath.replace("\\", "/")


def _rel_path(filepath: str) -> str:
    try:
        return _normalizar_path(os.path.relpath(filepath, BASE_DIR))
    except ValueError:
        return _normalizar_path(filepath)


def _abs_path(path: str) -> str:
    return os.path.abspath(path)


def _esta_dentro(filepath: str, directory: str) -> bool:
    try:
        return os.path.commonpath([_abs_path(filepath), _abs_path(directory)]) == _abs_path(directory)
    except ValueError:
        return False


def _tiene_directorio_excluido(filepath: str) -> bool:
    parts = [part.lower() for part in _normalizar_path(filepath).split("/")]
    return any(part in EXCLUDED_DIR_NAMES for part in parts)


def _coincide_patron(patterns, text: str) -> bool:
    normalized = _normalizar_path(text).lower()
    return any(re.search(pattern, normalized, re.IGNORECASE) for pattern in patterns)


def _nombre_permitido(filepath: str) -> bool:
    filename = os.path.basename(filepath).lower()
    if _esta_dentro(filepath, COURSE_RUNTIME_DIR):
        return filename.endswith(".json")
    # Documentos subidos por el profesor (documentos/oficial/cursos/<course_id>/):
    # se permite cualquier nombre con extension segura. La politica de copyright
    # (patrones y marcadores prohibidos) se sigue aplicando aparte.
    if _esta_dentro(filepath, COURSE_UPLOADS_DIR):
        return filename.endswith(SAFE_EXTENSIONS)
    return _coincide_patron(ALLOWED_FILE_PATTERNS, filename)


def _contenido_contiene_marcador_prohibido(filepath: str) -> bool:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read(12000).lower()
    except Exception:
        return False
    return any(marker.lower() in text for marker in PROHIBITED_CONTENT_MARKERS)


def _log_ingest_decision(action: str, filepath: str, reasons=None, chunks=None):
    detail = f" chunks={chunks}" if chunks is not None else ""
    suffix = f" :: {'; '.join(reasons)}" if reasons else ""
    print(f"[INGEST][{action}] {_rel_path(filepath)}{detail}{suffix}")


def _es_ruta_permitida(filepath: str) -> bool:
    return any(_esta_dentro(filepath, directory) for directory in ALLOWED_PUBLIC_DIRS) and not (
        _esta_dentro(filepath, EXTERNAL_DIR)
        or _esta_dentro(filepath, NO_INDEX_DIR)
        or _tiene_directorio_excluido(filepath)
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


def _es_sidecar_metadata(filepath: str) -> bool:
    lower = filepath.lower()
    if lower.endswith(".metadata.json"):
        return True
    if lower.endswith(".json") and os.path.exists(os.path.splitext(filepath)[0] + ".pdf"):
        return True
    return False


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


def course_upload_dir(course_id: str) -> str:
    """Carpeta de subidas de conocimiento del profesor para un curso (la crea si falta)."""
    safe = re.sub(r"[^0-9A-Za-z_-]", "_", str(course_id or "default"))
    path = os.path.join(COURSE_UPLOADS_DIR, safe)
    os.makedirs(path, exist_ok=True)
    return path


def es_documento_aprobado_para_indexar(filepath: str, explicar: bool = False):
    razones = []

    if not os.path.exists(filepath):
        razones.append("archivo no existe")
    if not filepath.lower().endswith(SAFE_EXTENSIONS):
        razones.append("extension no soportada por ingesta segura")
    if not _es_ruta_permitida(filepath):
        razones.append("ruta fuera de carpetas publicas permitidas o dentro de carpeta excluida")

    relpath = _rel_path(filepath)
    filename_lower = os.path.basename(filepath).lower()
    if _coincide_patron(PROHIBITED_FILE_PATTERNS, relpath):
        razones.append("coincide con patron prohibido de ingesta")
    if not _nombre_permitido(filepath):
        razones.append("nombre de archivo fuera de patrones publicos aprobados")
    if _contenido_contiene_marcador_prohibido(filepath):
        razones.append("contiene referencia a paquete limpio, fuente protegida o material interno")

    metadata = obtener_metadata_documental(filepath)
    status = metadata.get("status", "")
    source_origin = metadata.get("source_origin", "")
    is_course_runtime = _esta_dentro(filepath, COURSE_RUNTIME_DIR)
    is_legacy_canonical = _esta_dentro(filepath, CONTENT_CANONICO_DIR) and filename_lower.endswith("_contenido_canonico.md")

    if not (is_course_runtime or is_legacy_canonical) and status != READY_STATUS:
        razones.append(f"status='{status or 'missing'}' distinto de '{READY_STATUS}'")
    if not (is_course_runtime or is_legacy_canonical) and source_origin != SAFE_SOURCE_ORIGIN:
        razones.append(f"source_origin='{source_origin or 'missing'}' distinto de '{SAFE_SOURCE_ORIGIN}'")

    nested_metadata = metadata.get("metadata", {}) if isinstance(metadata, dict) else {}
    allowed_flag = metadata.get("allowed_for_indexing", nested_metadata.get("allowed_for_indexing", None))
    if allowed_flag is False:
        razones.append("allowed_for_indexing=false")

    aprobado = not razones
    if explicar:
        return aprobado, razones, metadata
    return aprobado


def get_safe_document_candidates():
    archivos = set()
    for root_dir in ALLOWED_PUBLIC_DIRS:
        if not os.path.exists(root_dir):
            continue
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [
                d for d in dirs
                if d.lower() not in EXCLUDED_DIR_NAMES
                and not _esta_dentro(os.path.join(root, d), EXTERNAL_DIR)
                and not _esta_dentro(os.path.join(root, d), NO_INDEX_DIR)
            ]
            for filename in files:
                filepath = os.path.join(root, filename)
                if filepath.lower().endswith(SAFE_EXTENSIONS) and not _es_sidecar_metadata(filepath):
                    archivos.add(os.path.abspath(filepath))
    return sorted(archivos)


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
    # Soporte para Eje 0-7 y Modulo 1-8
    match_eje = re.search(r"eje\s*(\d+)", filename, re.IGNORECASE)
    if match_eje:
        return int(match_eje.group(1))
    match_mod = re.search(r"m[oó]dulo\s*(\d+)", filename, re.IGNORECASE)
    if match_mod:
        return int(match_mod.group(1))
    return ""


def _inferir_eje_desde_path(filepath: str):
    path = _normalizar_path(filepath).lower()
    match = re.search(r"eje[_\s-]*(\d+)", path)
    if match:
        return f"Eje {int(match.group(1))}"
    return ""


def _normalizar_eje(valor):
    if valor in ("", None):
        return ""
    if isinstance(valor, (int, float)):
        return f"Eje {int(valor)}"
    text = str(valor).strip()
    match = re.search(r"(\d+)", text)
    if match and ("eje" in text.lower() or text.isdigit()):
        return f"Eje {int(match.group(1))}"
    return text


def _metadata_axis(doc_meta: dict, filepath: str):
    axis = (
        doc_meta.get("axis")
        or doc_meta.get("eje")
        or doc_meta.get("axis_id")
        or doc_meta.get("module_id")
        or doc_meta.get("axis_number")
        or _inferir_eje_desde_path(filepath)
        or _inferir_modulo_desde_nombre(os.path.basename(filepath))
    )
    return _normalizar_eje(axis)


def _inferir_layer_desde_nombre(filename: str):
    fn = filename.lower()
    if "canonico" in fn or "guia_canonica" in fn:
        return "canonico"
    if "paquete_limpio" in fn or "limpio" in fn:
        return "limpio"
    return "general"


def _metadata_layer(doc_meta: dict, filename: str):
    return (
        doc_meta.get("layer")
        or doc_meta.get("capa")
        or doc_meta.get("doc_layer")
        or _inferir_layer_desde_nombre(filename)
    )


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
    axis = _metadata_axis(doc_meta, filepath)
    layer = _metadata_layer(doc_meta, filename)
    
    return {
        "source": _normalizar_path(filepath),
        "filename": filename,
        "doc_type": doc_meta.get("doc_type", doc_type),
        "source_origin": doc_meta.get("source_origin", ""),
        "status": doc_meta.get("status", ""),
        "course": doc_meta.get("course_id", "") or _inferir_course(filepath),
        "course_id": doc_meta.get("course_id", ""),
        "module_id": doc_meta.get("module_id", ""),
        "axis_id": doc_meta.get("axis_id", axis),
        "axis_number": doc_meta.get("axis_number", ""),
        "axis_title": doc_meta.get("axis_title", ""),
        "axis": axis,
        "eje": axis,
        "layer": layer,
        "capa": layer,
        "module_title": doc_meta.get("module_title", ""),
        "version": doc_meta.get("version", ""),
        "chunk_index": chunk_index,
        "chunk_id": chunk_id,
    }


def _metadata_pdf(filepath: str, page, chunk_index: int):
    filename = os.path.basename(filepath)
    doc_meta = obtener_metadata_documental(filepath)
    axis = _metadata_axis(doc_meta, filepath)
    layer = _metadata_layer(doc_meta, filename)
    chunk_id = _crear_chunk_id(filepath, chunk_index, "pdf", page)
    metadata = _metadata_base(filepath, "pdf", chunk_index, chunk_id)
    metadata.update({
        "module": axis,
        "modulo": axis,
        "axis": axis,
        "eje": axis,
        "layer": layer,
        "capa": layer,
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
    axis = _normalizar_eje(
        item.get("axis")
        or item.get("eje")
        or item.get("axis_id")
        or item.get("module")
        or item.get("modulo")
        or parent_meta.get("axis_id")
        or parent_meta.get("module_id")
        or parent_meta.get("axis_number")
        or _inferir_eje_desde_path(filepath)
    )
    submodule = item.get("submodule", item.get("submodulo", ""))
    layer = (
        item.get("layer")
        or item.get("capa")
        or item.get("doc_layer")
        or parent_meta.get("doc_layer")
        or _inferir_layer_desde_nombre(filename)
    )
    chunk_id = item.get("chunk_id", "") or _crear_chunk_id(filepath, chunk_index, item_id, start_time)

    metadata = _metadata_base(filepath, parent_meta.get("doc_type", "video_transcript"), chunk_index, chunk_id)
    metadata.update({
        "id": _valor_metadata(item_id),
        "module": _valor_metadata(axis),
        "modulo": _valor_metadata(axis),
        "axis": _valor_metadata(axis),
        "eje": _valor_metadata(axis),
        "layer": _valor_metadata(layer),
        "capa": _valor_metadata(layer),
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
        f"Eje: {metadata.get('axis', '')}",
        f"Capa: {metadata.get('layer', '')}",
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

    # REGLA: No romper filas de tablas markdown
    class TableAwareSplitter(RecursiveCharacterTextSplitter):
        def split_text(self, text: str):
            # Si el texto parece contener tablas, usamos un separador que respete lineas
            if "|" in text:
                lines = text.split("\n")
                chunks = []
                current_chunk = []
                current_size = 0
                for line in lines:
                    line_len = len(line) + 1
                    if current_size + line_len > self._chunk_size and current_chunk:
                        chunks.append("\n".join(current_chunk))
                        current_chunk = []
                        current_size = 0
                    current_chunk.append(line)
                    current_size += line_len
                if current_chunk:
                    chunks.append("\n".join(current_chunk))
                return chunks
            return super().split_text(text)

    text_splitter = TableAwareSplitter(
        chunk_size=TRANSCRIPT_CHUNK_SIZE,
        chunk_overlap=TRANSCRIPT_CHUNK_OVERLAP,
    )

    chunks = []
    for chunk_str in text_splitter.split_text(content):
        chunk_index = len(chunks)
        chunk_id = _crear_chunk_id(filepath, chunk_index, "md")
        metadata = _metadata_base(filepath, metadata_doc.get("doc_type", "markdown"), chunk_index, chunk_id)
        axis = _metadata_axis(metadata_doc, filepath)
        layer = _metadata_layer(metadata_doc, os.path.basename(filepath))
        
        metadata.update({
            "module": axis,
            "modulo": axis,
            "axis": axis,
            "eje": axis,
            "layer": layer,
            "capa": layer,
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
        _log_ingest_decision("SKIP", filepath, razones)
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
    _log_ingest_decision("INDEX", filepath, chunks=len(chunks))

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


def reindex_course_documents(course_id: str):
    """Reindexa solo los documentos subidos por profesor para un curso.

    Borra de Chroma los chunks con metadata course_id=<curso> y vuelve a cargar
    los archivos aprobados dentro de documentos/oficial/cursos/<course_id>/.
    """
    course = str(course_id or "").strip()
    if not course:
        return {"success": False, "message": "course_id requerido", "processed": 0, "skipped": 0}

    db = get_vector_store()
    try:
        db._collection.delete(where={"course_id": course})
    except Exception as e:
        print(f"Nota al borrar chunks del curso {course}: {e}")

    root = course_upload_dir(course)
    candidates = []
    if os.path.exists(root):
        for current_root, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d.lower() not in EXCLUDED_DIR_NAMES]
            for filename in files:
                filepath = os.path.join(current_root, filename)
                if filepath.lower().endswith(SAFE_EXTENSIONS) and not _es_sidecar_metadata(filepath):
                    candidates.append(os.path.abspath(filepath))

    processed = 0
    skipped = 0
    reasons = {}
    for filepath in sorted(candidates):
        result = add_single_document(filepath)
        if result.get("success"):
            processed += 1
        else:
            skipped += 1
            reasons[_rel_path(filepath)] = result.get("reasons") or [result.get("message", "no aprobado")]

    return {
        "success": True,
        "message": f"Reindex scoped completado para curso {course}.",
        "course_id": course,
        "processed": processed,
        "skipped": skipped,
        "candidates": len(candidates),
        "reasons": reasons,
    }


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
    archivos = get_safe_document_candidates()

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

    persist_dir = CHROMA_DIR

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
