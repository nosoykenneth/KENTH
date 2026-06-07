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
# Conocimiento UNIVERSAL compartido por TODOS los cursos (course_id vacío).
GLOBAL_DIR = os.path.join(OFFICIAL_DIR, "global")

# Convención multi-curso para etiquetar course_id por la RUTA del archivo:
#   - documentos/oficial/cursos/<id>/...  -> course_id = <id>
#   - documentos/oficial/global/...       -> course_id = ""  (universal)
#   - resto (legacy: ejes/, contenido_canonico/, course_runtime) -> curso base actual.
# Cuando crees un 2º curso, su contenido va bajo cursos/<id>/ y se etiqueta solo.
DEFAULT_COURSE_ID = os.getenv("KENTH_DEFAULT_COURSE_ID", "2")

READY_STATUS = "ready_for_indexing"
SAFE_SOURCE_ORIGIN = "course"
SAFE_EXTENSIONS = (".json", ".md", ".pdf")
# Imágenes que el profe puede subir como conocimiento (se indexa su descripción).
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")
# Recursos de lección: archivos que el profe sube por lección. Los de texto se
# indexan por contenido; los binarios (audio/plantillas) NO se embeben — se indexa
# su descripción y se sirven como descarga. Clasificados por extensión.
AUDIO_EXTENSIONS = (".wav", ".mp3", ".flac", ".ogg", ".aiff", ".aif", ".m4a")
TEMPLATE_EXTENSIONS = (".flp", ".als", ".ptx", ".logicx", ".cpr", ".rpp", ".band", ".aup3")
TEXT_DOC_EXTENSIONS = (".pdf", ".txt", ".md")
RESOURCE_EXTENSIONS = (
    IMAGE_EXTENSIONS + AUDIO_EXTENSIONS + TEMPLATE_EXTENSIONS + TEXT_DOC_EXTENSIONS + (".zip",)
)


def resource_media_type(ext: str) -> str:
    """Clasifica la extensión en un media_type para UI/tutor: image/audio/template/document/file."""
    e = (ext or "").lower()
    if not e.startswith("."):
        e = "." + e
    if e in IMAGE_EXTENSIONS:
        return "image"
    if e in AUDIO_EXTENSIONS:
        return "audio"
    if e in TEMPLATE_EXTENSIONS:
        return "template"
    if e in TEXT_DOC_EXTENSIONS:
        return "document"
    return "file"
# Archivos de ESTRUCTURA/estado (no son conocimiento): se inyectan desde la BD,
# no deben entrar al RAG. Se saltan en la ingesta para no contaminar la búsqueda.
STRUCTURE_SKIP_NAMES = ("00_manifest.json", "curso_manifest.json", "mapa_curricular.json")

ALLOWED_PUBLIC_DIRS = (
    EJES_DIR,
    CONTENT_CANONICO_DIR,
    COURSE_UPLOADS_DIR,
    GLOBAL_DIR,
    # COURSE_RUNTIME_DIR se quitó: son SEMILLAS de estructura (manifests,
    # res_*.json, lecciones), no conocimiento. El estado se inyecta desde la BD.
    # Los modulo_01..08 (estructura vieja) se archivaron a documentos/no_indexar/.
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
    # Estructura/estado: nunca al RAG (se inyecta desde BD).
    if filename in STRUCTURE_SKIP_NAMES:
        return False
    # Documentos subidos por el profesor (documentos/oficial/cursos/<course_id>/
    # y documentos/oficial/global/): se permite cualquier nombre con extension
    # segura o de imagen. La politica de copyright se aplica aparte.
    if _esta_dentro(filepath, COURSE_UPLOADS_DIR) or _esta_dentro(filepath, GLOBAL_DIR):
        return filename.endswith(SAFE_EXTENSIONS) or filename.endswith(IMAGE_EXTENSIONS)
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


def _as_bool(valor, default: bool = False) -> bool:
    """Coacciona a bool valores que pueden venir como bool, int o string
    (frontmatter md guarda 'True'/'False' como texto)."""
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, (int, float)):
        return bool(valor)
    if isinstance(valor, str):
        return valor.strip().lower() in ("1", "true", "yes", "si", "sí", "on")
    return default


def _default_resource_type_safe(media_type: str, doc_type: str = "") -> str:
    """Wrapper sin dependencia dura: uso pedagogico por defecto desde el formato."""
    try:
        from services.db_service import default_resource_type
        return default_resource_type(media_type, doc_type)
    except Exception:
        m = (media_type or "").lower()
        return {"template": "daw_template", "audio": "audio_practice",
                "image": "image_reference", "document": "theory",
                "file": "downloadable"}.get(m, "other")


def _scope_chunk(course_id: str, axis_id: str, lesson_id: str, is_global: bool, declared: str = "") -> str:
    """Scope del chunk para Chroma. Usa el declarado en metadata si es valido;
    si no, lo deriva con la misma regla que la BD (single source: db_service)."""
    declared = (declared or "").strip().lower()
    if declared in ("global", "course", "axis", "lesson"):
        return declared
    try:
        from services.db_service import derive_scope
        return derive_scope(course_id, axis_id, lesson_id, is_global)
    except Exception:
        if is_global or (not course_id and not axis_id and not lesson_id):
            return "global"
        if lesson_id:
            return "lesson"
        if axis_id:
            return "axis"
        return "course"


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


def _inferir_course_id(filepath: str) -> str:
    """Deriva el course_id por la RUTA (convención multi-curso). Ver constantes.

    - cursos/<id>/...  -> <id>
    - global/...       -> "" (universal, lo ven todos los cursos)
    - resto (legacy de Mezcla) -> DEFAULT_COURSE_ID
    """
    norm = _normalizar_path(filepath)
    if "/oficial/global/" in norm or norm.endswith("/oficial/global"):
        return ""
    m = re.search(r"/cursos/([^/]+)/", norm)
    if m:
        return m.group(1)
    return DEFAULT_COURSE_ID


def _crear_chunk_id(filepath: str, chunk_index: int, prefix: str = "", page="") -> str:
    raw = f"{_normalizar_path(filepath)}|{prefix}|{page}|{chunk_index}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()[:16]


def _metadata_base(filepath: str, doc_type: str, chunk_index: int, chunk_id: str):
    filename = os.path.basename(filepath)
    doc_meta = obtener_metadata_documental(filepath)
    axis = _metadata_axis(doc_meta, filepath)
    layer = _metadata_layer(doc_meta, filename)

    course_id = doc_meta.get("course_id") or _inferir_course_id(filepath)
    lesson_id = doc_meta.get("lesson_id", "") or ""
    axis_id = doc_meta.get("axis_id", axis) or ""
    # Fase 1: la visibilidad y el alcance viajan al chunk para que el retrieval
    # y el servido de media puedan filtrar sin volver a la BD.
    is_global = _as_bool(doc_meta.get("is_global"), course_id == "")
    visible_to_student = _as_bool(doc_meta.get("visible_to_student"), True)
    allowed_for_indexing = _as_bool(doc_meta.get("allowed_for_indexing"), True)
    scope = _scope_chunk(course_id, axis_id, lesson_id, is_global, doc_meta.get("scope", ""))
    # Fase 2: media_type (formato) + resource_type (uso pedagogico) viajan al chunk.
    media_type = doc_meta.get("media_type") or resource_media_type(os.path.splitext(filepath)[1])
    resource_type = (doc_meta.get("resource_type") or "").strip().lower()
    if not resource_type:
        try:
            from services.db_service import default_resource_type
            resource_type = default_resource_type(media_type, doc_meta.get("doc_type", doc_type))
        except Exception:
            resource_type = "other"

    return {
        "source": _normalizar_path(filepath),
        "filename": filename,
        "doc_type": doc_meta.get("doc_type", doc_type),
        "source_origin": doc_meta.get("source_origin", ""),
        "status": doc_meta.get("status", ""),
        "course": doc_meta.get("course_id", "") or _inferir_course_id(filepath) or _inferir_course(filepath),
        "course_id": course_id,
        "module_id": doc_meta.get("module_id", ""),
        "lesson_id": lesson_id,
        "axis_id": axis_id,
        "axis_number": doc_meta.get("axis_number", ""),
        "axis_title": doc_meta.get("axis_title", ""),
        "axis": axis,
        "eje": axis,
        "layer": layer,
        "capa": layer,
        "module_title": doc_meta.get("module_title", ""),
        "version": doc_meta.get("version", ""),
        "scope": scope,
        "is_global": is_global,
        "visible_to_student": visible_to_student,
        "allowed_for_indexing": allowed_for_indexing,
        "media_type": media_type,
        "resource_type": resource_type,
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


def _crear_chunks_txt(filepath: str):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().strip()
    if not content:
        return []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=TRANSCRIPT_CHUNK_SIZE, chunk_overlap=TRANSCRIPT_CHUNK_OVERLAP,
    )
    chunks = []
    for chunk_str in splitter.split_text(content):
        i = len(chunks)
        cid = _crear_chunk_id(filepath, i, "txt")
        metadata = _metadata_base(filepath, "texto", i, cid)
        chunks.append(Document(page_content=_texto_chunk(chunk_str, metadata), metadata=metadata))
    return chunks


def _crear_chunks_imagen(filepath: str):
    """La imagen NO se embebe: se indexa su DESCRIPCIÓN (del profe + caption IA),
    guardada en un sidecar <archivo>.json. La imagen se referencia en metadata
    (media_type='image', media_path) para que el tutor pueda mostrarla."""
    sidecar = os.path.splitext(filepath)[0] + ".json"
    meta_doc = _leer_json_seguro(sidecar) or {}
    title = meta_doc.get("title") or _stem(os.path.basename(filepath))
    desc = (meta_doc.get("description") or "").strip()
    concepts = meta_doc.get("concepts") or []
    if isinstance(concepts, str):
        concepts = [c.strip() for c in concepts.split(",") if c.strip()]
    if not desc:
        return []  # sin descripción no hay nada indexable
    partes = [title, "", f"Imagen (captura/diagrama): {desc}"]
    if concepts:
        partes.append("Conceptos: " + ", ".join(concepts))
    content = "\n".join(partes)
    cid = _crear_chunk_id(filepath, 0, "img")
    metadata = _metadata_base(filepath, "image_description", 0, cid)
    rel = os.path.relpath(filepath, BASE_DIR).replace("\\", "/")
    metadata.update({"media_type": "image", "media_path": rel, "title": title})
    return [Document(page_content=_texto_chunk(content, metadata), metadata=metadata)]


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
    elif filepath_lower.endswith(".txt"):
        chunks = _crear_chunks_txt(filepath)
        if not chunks:
            return {"success": False, "message": "El TXT esta vacio."}
    elif filepath_lower.endswith(IMAGE_EXTENSIONS):
        chunks = _crear_chunks_imagen(filepath)
        if not chunks:
            return {"success": False, "message": "La imagen necesita una descripcion para indexarse."}
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
    """Reindexa de forma SEGURA todo el conocimiento de un curso (Fase 1).

    Borra los chunks con metadata course_id=<curso> y los reconstruye COMPLETOS:
      1. Documentos/PDF/MD/TXT (contenido) e imágenes (descripción) desde archivos.
      2. Descripciones de recursos binarios (audio/plantilla/file) desde la BD.
      3. Transcripciones de cada lección desde local_tesisai_transcript_segments.
    Antes solo re-añadía SAFE_EXTENSIONS, perdiendo transcripciones, imágenes y
    recursos no-documento. Los recursos GLOBAL (course_id="") NO se tocan.
    """
    course = str(course_id or "").strip()
    if not course:
        return {"success": False, "message": "course_id requerido", "processed": 0, "skipped": 0}

    from services import db_service  # import perezoso: evita ciclos al cargar ingest.

    db = get_vector_store()
    try:
        db._collection.delete(where={"course_id": course})
    except Exception as e:
        print(f"Nota al borrar chunks del curso {course}: {e}")

    processed = 0
    skipped = 0
    reasons = {}
    transcripts_indexed = 0
    resources_indexed = 0
    chunks_por_doc: dict = {}

    # 1) Archivos con contenido indexable (incluye imágenes por descripción).
    indexables = SAFE_EXTENSIONS + IMAGE_EXTENSIONS
    root = course_upload_dir(course)
    candidates = []
    if os.path.exists(root):
        for current_root, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d.lower() not in EXCLUDED_DIR_NAMES]
            for filename in files:
                filepath = os.path.join(current_root, filename)
                if filepath.lower().endswith(indexables) and not _es_sidecar_metadata(filepath):
                    candidates.append(os.path.abspath(filepath))

    for filepath in sorted(candidates):
        doc_id = os.path.splitext(os.path.basename(filepath))[0]
        result = add_single_document(filepath)
        if result.get("success"):
            processed += 1
            chunks_por_doc[doc_id] = ("indexed", result.get("chunks", 0))
        else:
            skipped += 1
            reasons[_rel_path(filepath)] = result.get("reasons") or [result.get("message", "no aprobado")]
            # Si el archivo estaba marcado indexable pero la política lo rechazó,
            # lo dejamos como 'failed' (no como 'indexed' silencioso).
            chunks_por_doc[doc_id] = ("failed", 0)

    # 2) Recursos binarios (audio/plantilla/file): se reindexa su DESCRIPCIÓN.
    try:
        docs = db_service.list_documents(course_id=course)
    except Exception as e:
        docs = []
        print(f"[reindex] no se pudieron leer documentos del curso {course}: {e}")

    for doc in docs:
        media_type = (doc.get("media_type") or (doc.get("metadata") or {}).get("media_type") or "")
        if media_type not in ("audio", "template", "file"):
            continue
        doc_id = doc.get("doc_id")
        if not doc.get("allowed_for_indexing"):
            chunks_por_doc[doc_id] = ("pending", 0)
            continue
        meta = doc.get("metadata") or {}
        description = (meta.get("description") or doc.get("notes") or "").strip()
        if not description:
            # Indexable pero sin descripción suficiente: error claro, no se indexa.
            chunks_por_doc[doc_id] = ("failed", 0)
            reasons[f"resource:{doc_id}"] = ["recurso binario sin descripción para indexar"]
            continue
        r = index_resource_description(
            course_id=course, lesson_id=doc.get("lesson_id", ""), doc_id=doc_id,
            title=doc.get("title", ""), description=description, concepts=meta.get("concepts") or [],
            axis_id=doc.get("axis_id", ""), media_type=media_type,
            media_path=doc.get("relpath", ""), doc_type=doc.get("doc_type", ""),
            visible_to_student=doc.get("visible_to_student", False),
            allowed_for_indexing=True, scope=doc.get("scope", ""), is_global=doc.get("is_global", False),
            resource_type=doc.get("resource_type", ""),
        )
        if r.get("success"):
            resources_indexed += 1
            chunks_por_doc[doc_id] = ("indexed", r.get("chunks", 0))
        else:
            chunks_por_doc[doc_id] = ("failed", 0)

    # 3) Transcripciones por lección (DB-driven, sin archivo).
    try:
        lessons = db_service.list_lessons(course_id=course)
    except Exception as e:
        lessons = []
        print(f"[reindex] no se pudieron leer lecciones del curso {course}: {e}")

    for lesson in lessons:
        lid = lesson.get("lesson_id")
        if not lid:
            continue
        segments = db_service.list_transcript(lid)
        if not segments:
            continue
        tr = index_lesson_transcript(course, lid, segments, axis_id=lesson.get("axis_id", ""))
        if tr.get("success") and tr.get("chunks"):
            transcripts_indexed += 1

    # 4) Persistir index_status/chunk_count por documento.
    for doc_id, (estado, n) in chunks_por_doc.items():
        try:
            db_service.update_document_index_state(doc_id, course, index_status=estado, chunk_count=n)
        except Exception as e:
            print(f"[reindex] no se pudo actualizar index_status de {doc_id}: {e}")

    return {
        "success": True,
        "message": f"Reindex seguro completado para curso {course}.",
        "course_id": course,
        "processed": processed,
        "skipped": skipped,
        "candidates": len(candidates),
        "resources_indexed": resources_indexed,
        "transcripts_indexed": transcripts_indexed,
        "reasons": reasons,
    }


def index_lesson_transcript(course_id, lesson_id, segments, axis_id="", resource_id=""):
    """Indexa (RAG) la transcripción de una lección como conocimiento canónico.

    Agrupa los segmentos en chunks (~700 chars) conservando el tiempo de inicio/fin
    para que el tutor pueda citar el minuto. Patrón delete-then-add por lección:
    borra los chunks previos con source="transcription:<lesson_id>" y re-inserta.
    Pensado para llamarse al guardar/auto-transcribir (datos en BD, sin archivo).
    """
    course = str(course_id or "").strip()
    lid = str(lesson_id or "").strip()
    if not lid:
        return {"success": False, "chunks": 0, "message": "lesson_id requerido"}

    source_tag = f"transcription:{lid}"
    store = get_vector_store()

    # 1) Borrar chunks previos de esta transcripción.
    try:
        store._collection.delete(where={"source": source_tag})
    except Exception as e:  # pragma: no cover
        print(f"Nota al borrar transcript chunks de {lid}: {e}")

    # 2) Agrupar segmentos en chunks.
    CHUNK_CHARS = 700
    chunks = []  # {text, start, end}
    cur_text, cur_start, cur_end = "", None, None
    for s in (segments or []):
        text = (s.get("text") or "").strip()
        if not text:
            continue
        st = float(s.get("start_time") or 0)
        en = float(s.get("end_time") or st)
        if cur_start is None:
            cur_start = st
        cur_end = en
        cur_text = (cur_text + " " + text).strip()
        if len(cur_text) >= CHUNK_CHARS:
            chunks.append({"text": cur_text, "start": cur_start, "end": cur_end})
            cur_text, cur_start, cur_end = "", None, None
    if cur_text:
        chunks.append({"text": cur_text, "start": cur_start or 0.0, "end": cur_end or 0.0})

    if not chunks:
        return {"success": True, "chunks": 0, "message": "transcripción vacía (solo se limpió el índice)"}

    texts, metadatas, ids = [], [], []
    for i, ch in enumerate(chunks):
        texts.append(ch["text"])
        metadatas.append({
            "course_id": course,
            "axis_id": str(axis_id or ""),
            "lesson_id": lid,
            "resource_id": str(resource_id or ""),
            "start_time": float(ch["start"] or 0),
            "end_time": float(ch["end"] or 0),
            "doc_layer": "canonico",
            "doc_type": "video_transcript",
            "source": source_tag,
            "title": lid,
            # La transcripcion es conocimiento del curso (scope lección): el tutor
            # la usa y la puede citar; no es un archivo descargable.
            "scope": _scope_chunk(course, str(axis_id or ""), lid, False, "lesson" if lid else ""),
            "is_global": False,
            "visible_to_student": True,
            "allowed_for_indexing": True,
            "resource_type": "transcription",
        })
        ids.append(f"{source_tag}:{i}")

    store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
    try:
        store.persist()
    except Exception:
        pass  # chromadb reciente persiste solo

    return {"success": True, "chunks": len(chunks), "course_id": course, "lesson_id": lid}


def index_resource_description(course_id, lesson_id, doc_id, title, description,
                               concepts=None, axis_id="", media_type="file",
                               media_path="", doc_type="", visible_to_student=True,
                               allowed_for_indexing=True, scope="", is_global=False,
                               resource_type=""):
    """Indexa (RAG) la DESCRIPCIÓN de un recurso cuyo binario no es texto
    (.flp/.als/.wav/.mp3, o una imagen). El archivo NO se embebe: lo buscable es su
    descripción + conceptos, con un puntero (media_path/media_type) para que el tutor
    lo pueda mostrar/enlazar. Patrón delete-then-add por recurso (source="resource:<doc_id>")."""
    desc = (description or "").strip()
    did = str(doc_id or "").strip()
    if not did or not desc:
        return {"success": False, "chunks": 0, "message": "doc_id y descripción requeridos"}

    if isinstance(concepts, str):
        concepts = [c.strip() for c in concepts.split(",") if c.strip()]
    concepts = concepts or []

    source_tag = f"resource:{did}"
    store = get_vector_store()
    try:
        store._collection.delete(where={"source": source_tag})
    except Exception as e:  # pragma: no cover
        print(f"Nota al borrar resource chunks de {did}: {e}")

    etiqueta = {
        "image": "Imagen (captura/diagrama)",
        "audio": "Archivo de audio de ejemplo",
        "template": "Plantilla de proyecto (DAW)",
    }.get(media_type, "Recurso de la lección")
    partes = [title or did, "", f"{etiqueta}: {desc}"]
    if concepts:
        partes.append("Conceptos: " + ", ".join(concepts))
    texto = "\n".join(partes)

    metadata = {
        "course_id": str(course_id or ""),
        "axis_id": str(axis_id or ""),
        "lesson_id": str(lesson_id or ""),
        "doc_layer": "canonico",
        "doc_type": doc_type or media_type or "resource",
        "source": source_tag,
        "title": title or did,
        "media_type": media_type or "file",
        "media_path": (media_path or "").replace("\\", "/"),
        # Fase 1: visibilidad + alcance viajan al chunk.
        "scope": _scope_chunk(str(course_id or ""), str(axis_id or ""), str(lesson_id or ""),
                              _as_bool(is_global, False), scope),
        "is_global": _as_bool(is_global, False),
        "visible_to_student": _as_bool(visible_to_student, True),
        "allowed_for_indexing": _as_bool(allowed_for_indexing, True),
        # Fase 2: uso pedagogico.
        "resource_type": (resource_type or "").strip().lower() or _default_resource_type_safe(media_type),
    }

    store.add_texts(texts=[texto], metadatas=[metadata], ids=[f"{source_tag}:0"])
    try:
        store.persist()
    except Exception:
        pass
    return {"success": True, "chunks": 1, "doc_id": did}


def delete_resource_index(doc_id):
    """Borra del índice los chunks de descripción de un recurso (al borrar el recurso)."""
    did = str(doc_id or "").strip()
    if not did:
        return
    try:
        get_vector_store()._collection.delete(where={"source": f"resource:{did}"})
    except Exception as e:  # pragma: no cover
        print(f"Nota al borrar resource index {did}: {e}")


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
