import glob
import hashlib
import json
import os
import re
import unicodedata
from datetime import datetime, timezone

import pdfplumber

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
COURSE_RUNTIME_DIR = os.path.join(BASE_DIR, "course_runtime")
LOCATION_DIR = os.path.join(DOCUMENTS_DIR, "localizacion")
EXTERNAL_DIR = os.path.join(DOCUMENTS_DIR, "externo")
NO_INDEX_DIR = os.path.join(DOCUMENTS_DIR, "no_indexar")
# Documentos de conocimiento subidos por el profesor, organizados por curso:
# documentos/oficial/cursos/<course_id>/<doc>. Indexables si pasan la politica.
COURSE_UPLOADS_DIR = os.path.join(OFFICIAL_DIR, "cursos")
# Conocimiento UNIVERSAL compartido por TODOS los cursos (course_id vacío).
GLOBAL_DIR = os.path.join(OFFICIAL_DIR, "global")

# Corpus canónico organizado por SECCIÓN (arquitectura nueva, post-migración ejes):
#   documentos/oficial/curso_<id>/seccion_<NN>_<slug>/contenido_canonico.md
# Cada archivo lleva frontmatter con su moodle_section_id real. La taxonomía por
# "eje" quedó deprecada: el conocimiento se ancla a la sección Moodle, no al eje.
def _canonical_course_dirs():
    return tuple(
        p for p in glob.glob(os.path.join(OFFICIAL_DIR, "curso_*"))
        if os.path.isdir(p)
    )


CANONICAL_COURSE_DIRS = _canonical_course_dirs()

# Convención multi-curso para etiquetar course_id por la RUTA del archivo:
#   - documentos/oficial/curso_<id>/...   -> course_id = <id>  (corpus canónico por sección)
#   - documentos/oficial/cursos/<id>/...  -> course_id = <id>  (subidas del profesor)
#   - documentos/oficial/global/...       -> course_id = ""    (universal)
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
STRUCTURE_SKIP_NAMES = (
    "00_manifest.json", "curso_manifest.json", "mapa_curricular.json",
    "_seccion_map.json",  # log de decisión de la migración ejes->secciones, no es contenido
)

# Carpetas públicas indexables. El corpus canónico ahora vive bajo
# documentos/oficial/curso_<id>/ (por sección); ejes/ quedó deprecado y se purga.
ALLOWED_PUBLIC_DIRS = (
    COURSE_UPLOADS_DIR,
    GLOBAL_DIR,
) + CANONICAL_COURSE_DIRS
# COURSE_RUNTIME_DIR se quitó: son SEMILLAS de estructura (manifests, res_*.json,
# lecciones), no conocimiento. El estado se inyecta desde la BD.

EXCLUDED_DIR_NAMES = {
    "ejes",            # taxonomía vieja por eje: deprecada, no se indexa
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
    r"^contenido_canonico\.md$",
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
    if (
        _esta_dentro(filepath, COURSE_UPLOADS_DIR)
        or _esta_dentro(filepath, GLOBAL_DIR)
        or _en_curso_canonico(filepath)
    ):
        return filename.endswith(SAFE_EXTENSIONS) or filename.endswith(IMAGE_EXTENSIONS)
    return _coincide_patron(ALLOWED_FILE_PATTERNS, filename)


def _en_curso_canonico(filepath: str) -> bool:
    """¿El archivo vive bajo documentos/oficial/curso_<id>/ (corpus por sección)?"""
    return any(_esta_dentro(filepath, d) for d in CANONICAL_COURSE_DIRS)


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
    # El corpus canónico por sección lleva su propio frontmatter (status/origin);
    # exento del requisito sólo de forma defensiva.
    is_canonical_course = _en_curso_canonico(filepath) and filename_lower.endswith(".md")

    if not (is_course_runtime or is_canonical_course) and status != READY_STATUS:
        razones.append(f"status='{status or 'missing'}' distinto de '{READY_STATUS}'")
    if not (is_course_runtime or is_canonical_course) and source_origin != SAFE_SOURCE_ORIGIN:
        razones.append(f"source_origin='{source_origin or 'missing'}' distinto de '{SAFE_SOURCE_ORIGIN}'")

    nested_metadata = metadata.get("metadata", {}) if isinstance(metadata, dict) else {}
    allowed_flag = metadata.get("allowed_for_indexing", nested_metadata.get("allowed_for_indexing", None))
    # El frontmatter markdown entrega el flag como STRING ('false'), no como bool;
    # comparar con `is False` dejaba pasar prompts de evaluación / QA / manifiestos.
    # Se rechaza solo cuando el flag está PRESENTE y es falsy (según _as_bool robusto).
    if allowed_flag is not None and not _as_bool(allowed_flag, default=True):
        razones.append(f"allowed_for_indexing={allowed_flag!r} (interpretado como false)")

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


_TRUTHY_STRINGS = ("1", "true", "yes", "si", "sí", "on", "t", "y")
_FALSY_STRINGS = ("0", "false", "no", "off", "f", "n", "null", "none", "nil", "")


def _as_bool(valor, default: bool = False) -> bool:
    """Coacciona a bool cualquier flag que venga como bool, int/float, string o None.

    Robusto e inequívoco:
      - bool  -> tal cual
      - None  -> default
      - int/float -> bool(valor)  (1/0)
      - str: 'true'/'false', '1'/'0', 'yes'/'no', 'on'/'off', 'null' (case-insensitive)
        Un string desconocido cae al default (no adivina).

    CRÍTICO: el frontmatter markdown (parser _leer_frontmatter_md) guarda TODO como
    texto, así que `allowed_for_indexing: false` llega como el string 'false'. Por eso
    NUNCA se debe comparar el flag crudo con `is False`/`== False`: hay que pasarlo por
    esta función. Ver es_documento_aprobado_para_indexar."""
    if isinstance(valor, bool):
        return valor
    if valor is None:
        return default
    if isinstance(valor, (int, float)):
        return bool(valor)
    if isinstance(valor, str):
        s = valor.strip().lower()
        if s in _TRUTHY_STRINGS:
            return True
        if s in _FALSY_STRINGS:
            return False
        return default
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


def _scope_chunk(
    course_id: str,
    lesson_id: str,
    is_global: bool,
    declared: str = "",
    moodle_section_id: str = "",
    block_id: str = "",
) -> str:
    """Scope pedagógico del chunk para Chroma. Jerarquía:
    block > lesson > section > course > global. El scope 'axis' quedó eliminado:
    el conocimiento se ancla a la sección Moodle, nunca al eje."""
    declared = (declared or "").strip().lower()
    if declared in ("global", "course", "section", "lesson", "block"):
        return declared
    try:
        from services.db_service import derive_scope
        return derive_scope(course_id, lesson_id, is_global, moodle_section_id, block_id)
    except Exception:
        if is_global or (not course_id and not lesson_id and not moodle_section_id and not block_id):
            return "global"
        if block_id:
            return "block"
        if lesson_id:
            return "lesson"
        if moodle_section_id:
            return "section"
        return "course"


_SECTIONS_CACHE = {}


def _course_sections_ordered(course_id: str):
    """Secciones del curso en orden Moodle (cacheadas por proceso de ingest)."""
    cid = str(course_id or "").strip()
    if not cid:
        return []
    if _SECTIONS_CACHE.get(cid):
        return _SECTIONS_CACHE[cid]
    try:
        from services import section_service
        sections = section_service._list_sections_from_db(cid)
    except Exception as exc:
        print(f"[ingest] no se pudieron leer secciones del curso {cid}: {exc}")
        sections = []
    # Solo cacheamos resultados NO vacíos: un vacío puede deberse a que la BD aún
    # no estaba inicializada (using_moodle_db False antes de init_db); reintentar.
    if sections:
        _SECTIONS_CACHE[cid] = sections
    return sections


def _slugify(text: str) -> str:
    """Slug estable y ASCII desde un título Moodle (sin acentos, kebab/snake)."""
    text = str(text or "").strip()
    # quitar prefijo "SECCIÓN N:" / "Tema N:" si lo hubiera
    text = re.sub(r"^\s*(secci[oó]n|tema)\s*\d+\s*[:.\-]\s*", "", text, flags=re.IGNORECASE)
    norm = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    norm = re.sub(r"[^a-zA-Z0-9]+", "_", norm).strip("_").lower()
    return norm


def _section_meta_for_id(course_id: str, moodle_section_id: str) -> dict:
    """Resuelve {section_number, section_title, section_slug} desde Moodle para un
    moodle_section_id. Devuelve {} si no se puede resolver (sin DB / sección ausente)."""
    sid = str(moodle_section_id or "").strip()
    if not sid:
        return {}
    for sec in _course_sections_ordered(course_id):
        if str(sec.get("moodle_section_id") or "") == sid:
            title = sec.get("section_name") or sec.get("current_section_name") or ""
            return {
                "section_number": sec.get("section_number"),
                "section_title": title,
                "section_slug": _slugify(title),
            }
    return {}


_FILE_HASH_CACHE = {}


def _file_source_hash(filepath: str) -> str:
    """md5 del contenido del archivo fuente (estable, para detectar duplicados/cambios)."""
    key = os.path.abspath(filepath)
    if key in _FILE_HASH_CACHE:
        return _FILE_HASH_CACHE[key]
    try:
        with open(filepath, "rb") as f:
            digest = hashlib.md5(f.read()).hexdigest()
    except Exception:
        digest = ""
    _FILE_HASH_CACHE[key] = digest
    return digest


def _stem(filename: str) -> str:
    return os.path.splitext(filename)[0]


def _inferir_layer_desde_nombre(filename: str):
    fn = filename.lower()
    if "transcrip" in fn:
        return "transcript"
    if "canonico" in fn or "guia_canonica" in fn or "contenido" in fn:
        return "canonical"
    if "rubric" in fn or "rubrica" in fn:
        return "rubric"
    return "resource"


def _metadata_layer(doc_meta: dict, filename: str):
    raw = (
        doc_meta.get("layer")
        or doc_meta.get("capa")
        or doc_meta.get("doc_layer")
        or _inferir_layer_desde_nombre(filename)
    )
    # Normaliza vocabulario viejo (canonico/limpio/general) al nuevo.
    alias = {"canonico": "canonical", "limpio": "resource", "general": "resource"}
    return alias.get(str(raw).strip().lower(), str(raw).strip().lower())


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
    # Corpus canónico por sección: documentos/oficial/curso_<id>/...
    m = re.search(r"/oficial/curso_([^/]+)/", norm)
    if m:
        return m.group(1)
    # Subidas del profesor: documentos/oficial/cursos/<id>/...
    m = re.search(r"/cursos/([^/]+)/", norm)
    if m:
        return m.group(1)
    return DEFAULT_COURSE_ID


def _crear_chunk_id(filepath: str, chunk_index: int, prefix: str = "", page="") -> str:
    raw = f"{_normalizar_path(filepath)}|{prefix}|{page}|{chunk_index}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()[:16]


def _metadata_base(filepath: str, doc_type: str, chunk_index: int, chunk_id: str):
    """Metadata canónica de un chunk. Estándar SECCIÓN/LECCIÓN/BLOQUE.

    Regla dura: ningún chunk seccional puede quedar sin moodle_section_id; sólo el
    conocimiento realmente universal (course_id vacío) puede ser scope 'global'.
    El eje quedó eliminado como fuente: se conserva `legacy_axis` SÓLO si el
    frontmatter lo trae, como traza de migración (nunca gobierna nada).
    """
    filename = os.path.basename(filepath)
    doc_meta = obtener_metadata_documental(filepath)
    layer = _metadata_layer(doc_meta, filename)

    course_id = str(doc_meta.get("course_id") or _inferir_course_id(filepath) or "").strip()
    lesson_id = str(doc_meta.get("lesson_id", "") or "").strip()
    block_id = str(doc_meta.get("block_id", "") or "").strip()
    moodle_section_id = str(
        doc_meta.get("moodle_section_id", "") or doc_meta.get("section_id", "") or ""
    ).strip()

    # Resolver título/número/slug de sección desde el frontmatter o, si falta,
    # desde Moodle (single source of truth de la estructura).
    sec_meta = _section_meta_for_id(course_id, moodle_section_id) if moodle_section_id else {}
    section_number = str(doc_meta.get("section_number") or sec_meta.get("section_number") or "")
    section_title = str(doc_meta.get("section_title") or sec_meta.get("section_title") or "")
    section_slug = str(doc_meta.get("section_slug") or sec_meta.get("section_slug") or "")

    is_global = _as_bool(doc_meta.get("is_global"), course_id == "")
    visible_to_student = _as_bool(doc_meta.get("visible_to_student"), True)
    allowed_for_indexing = _as_bool(doc_meta.get("allowed_for_indexing"), True)
    scope = _scope_chunk(course_id, lesson_id, is_global, doc_meta.get("scope", ""), moodle_section_id, block_id)

    media_type = doc_meta.get("media_type") or resource_media_type(os.path.splitext(filepath)[1])
    content_type = str(doc_meta.get("content_type") or os.path.splitext(filename)[1].lstrip(".").lower() or media_type)
    resource_type = (doc_meta.get("resource_type") or "").strip().lower()
    if not resource_type:
        try:
            from services.db_service import default_resource_type
            resource_type = default_resource_type(media_type, doc_meta.get("doc_type", doc_type))
        except Exception:
            resource_type = "other"

    source_kind = str(doc_meta.get("source") or "").strip().lower()
    if source_kind not in ("moodle", "canonical_md", "resource_file", "transcript"):
        source_kind = "canonical_md" if filename.lower().endswith(".md") else "resource_file"

    meta = {
        # --- identidad pedagógica (sección/lección/bloque) ---
        "course_id": course_id,
        "moodle_section_id": moodle_section_id,
        "section_id": moodle_section_id,
        "section_number": section_number,
        "section_title": section_title,
        "section_slug": section_slug,
        "lesson_id": lesson_id,
        "lesson_title": str(doc_meta.get("lesson_title", "") or ""),
        "block_id": block_id,
        "block_title": str(doc_meta.get("block_title", "") or ""),
        "resource_id": str(doc_meta.get("resource_id", "") or ""),
        # --- clasificación ---
        "resource_type": resource_type,
        "content_type": content_type,
        "layer": layer,
        "scope": scope,
        # --- procedencia / versionado ---
        "source": source_kind,
        "source_path": _normalizar_path(os.path.relpath(filepath, BASE_DIR)),
        "source_hash": _file_source_hash(filepath),
        "version": str(doc_meta.get("version", "") or ""),
        "index_status": "indexed",
        # --- flags operativos (filtrado/servido) ---
        "is_global": is_global,
        "visible_to_student": visible_to_student,
        "allowed_for_indexing": allowed_for_indexing,
        "media_type": media_type,
        "doc_type": doc_meta.get("doc_type", doc_type),
        "filename": filename,
        "chunk_index": chunk_index,
        "chunk_id": chunk_id,
    }
    # Traza de migración (no funcional). Nunca se usa para routing/retrieval.
    legacy_axis = str(doc_meta.get("legacy_axis", "") or "").strip()
    if legacy_axis:
        meta["legacy_axis"] = legacy_axis
    return meta


def _metadata_pdf(filepath: str, page, chunk_index: int):
    filename = os.path.basename(filepath)
    doc_meta = obtener_metadata_documental(filepath)
    chunk_id = _crear_chunk_id(filepath, chunk_index, "pdf", page)
    metadata = _metadata_base(filepath, "pdf", chunk_index, chunk_id)
    metadata.update({
        "lesson_title": metadata.get("lesson_title") or _stem(filename),
        "content_type": "pdf",
        "page": page,
        "start_time": "",
        "end_time": "",
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
    chunk_id = item.get("chunk_id", "") or _crear_chunk_id(filepath, chunk_index, item_id, start_time)

    metadata = _metadata_base(filepath, parent_meta.get("doc_type", "video_transcript"), chunk_index, chunk_id)
    metadata.update({
        "id": _valor_metadata(item_id),
        "lesson_title": _valor_metadata(titulo) or metadata.get("lesson_title", ""),
        "learning_objective": _valor_metadata(
            item.get("learning_objective", "")
            or item.get("objetivo_aprendizaje", "")
            or parent_meta.get("learning_objective", "")
        ),
        "url": _valor_metadata(url),
        "url_video": _valor_metadata(url),
        "start_time": _valor_metadata(start_time),
        "end_time": _valor_metadata(end_time),
        "page": "",
    })
    rt = (
        item.get("resource_type", "")
        or item.get("tipo_recurso", "")
    )
    if rt:
        metadata["resource_type"] = _valor_metadata(rt)
    return metadata


def _texto_chunk(page_content: str, metadata: dict) -> str:
    """Texto que se VECTORIZA. Estandar RAG: la metadata-maquina (doc_type, layer,
    filename, etc.) vive en el dict de metadata (Chroma la guarda aparte para
    filtrar/scope), NO embebida en el texto. Aqui solo va un prefijo de CONTEXTO
    corto y con sentido (seccion/leccion) + el contenido limpio. Esto evita ruido
    repetido en cada chunk y mejora la discriminacion semantica."""
    section = str(metadata.get("section_title") or "").strip()
    lesson = str(metadata.get("lesson_title") or metadata.get("lesson_id") or "").strip()
    ctx = list(dict.fromkeys([v for v in (section, lesson) if v]))  # dedup, preserva orden
    prefix = f"[{' · '.join(ctx)}]\n" if ctx else ""
    return f"{prefix}{(page_content or '').strip()}".strip()


_PDF_PAGE_ARTIFACT = re.compile(r"^\s*(p[áa]gina|page)\s*\d+\s*$", re.IGNORECASE)
# Token de numeracion al final de una linea (footer tipo "Banner ... Página 1"):
# se quita ANTES de detectar repetidos, asi el banner queda identico entre paginas.
_PDF_PAGE_TOKEN = re.compile(r"\s*(p[áa]gina|page)\s*\d+\s*$", re.IGNORECASE)


def _norm_pdf_line(s: str) -> str:
    return _PDF_PAGE_TOKEN.sub("", (s or "").strip()).strip()


def _tabla_a_markdown(rows) -> str:
    """Convierte una tabla (lista de filas) a markdown, preservando la relacion
    encabezado<->celda. Limpia None, saltos de linea internos y filas vacias."""
    limpias = []
    for r in rows or []:
        celdas = [(c or "").strip().replace("\n", " ") for c in r]
        if any(celdas):
            limpias.append(celdas)
    if not limpias:
        return ""
    ncol = max(len(r) for r in limpias)
    limpias = [r + [""] * (ncol - len(r)) for r in limpias]
    header = limpias[0]
    out = ["| " + " | ".join(header) + " |",
           "| " + " | ".join("---" for _ in header) + " |"]
    for r in limpias[1:]:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def _lineas_repetidas(textos_pagina) -> set:
    """Detecta headers/footers: lineas cortas que se repiten en (casi) todas las
    paginas. Estas son banner/titulo corrido/numeracion, no contenido."""
    from collections import Counter
    cont = Counter()
    for t in textos_pagina:
        for ln in {_norm_pdf_line(l) for l in (t or "").splitlines() if l.strip()}:
            if ln:
                cont[ln] += 1
    n = len(textos_pagina)
    umbral = 2 if n <= 2 else (n // 2 + 1)
    return {ln for ln, c in cont.items() if c >= umbral and len(ln) < 120}


def _crear_chunks_pdf_pypdf(filepath: str):
    """Fallback: extraccion lineal con PyPDFLoader (comportamiento previo)."""
    loader = PyPDFLoader(filepath)
    documentos = loader.load()
    if not documentos:
        return []
    splitter = RecursiveCharacterTextSplitter(chunk_size=PDF_CHUNK_SIZE, chunk_overlap=PDF_CHUNK_OVERLAP)
    chunks, chunk_index = [], 0
    for doc in documentos:
        page_raw = doc.metadata.get("page", "")
        page = page_raw + 1 if isinstance(page_raw, int) else page_raw
        for text in splitter.split_text(doc.page_content or ""):
            metadata = _metadata_pdf(filepath, page, chunk_index)
            chunks.append(Document(page_content=_texto_chunk(text, metadata), metadata=metadata))
            chunk_index += 1
    return chunks


def _crear_chunks_pdf(filepath: str):
    """Extraccion limpia con pdfplumber: texto narrativo FUERA de las tablas +
    tablas renderizadas como markdown (preserva encabezado<->celda) + strip de
    headers/footers/numeracion de pagina. Si pdfplumber falla, cae a PyPDFLoader."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=PDF_CHUNK_SIZE, chunk_overlap=PDF_CHUNK_OVERLAP)
    chunks, chunk_index = [], 0
    try:
        with pdfplumber.open(filepath) as pdf:
            paginas = pdf.pages
            crudos = [(p.extract_text() or "") for p in paginas]
            repetidas = _lineas_repetidas(crudos)
            for i, page in enumerate(paginas):
                page_no = i + 1
                tablas = page.find_tables() or []
                bboxes = [t.bbox for t in tablas]

                def _fuera_de_tabla(obj, _bboxes=bboxes):
                    cx = (obj.get("x0", 0) + obj.get("x1", 0)) / 2
                    cy = (obj.get("top", 0) + obj.get("bottom", 0)) / 2
                    for (x0, top, x1, bottom) in _bboxes:
                        if x0 <= cx <= x1 and top <= cy <= bottom:
                            return False
                    return True

                if bboxes:
                    try:
                        narrativa = page.filter(_fuera_de_tabla).extract_text() or ""
                    except Exception:
                        narrativa = crudos[i]
                else:
                    narrativa = crudos[i]

                lineas = []
                for ln in narrativa.splitlines():
                    s = ln.strip()
                    if not s or _PDF_PAGE_ARTIFACT.match(s):
                        continue
                    s = _norm_pdf_line(s)  # quita "Página N" del footer "Banner ... Página 1"
                    if not s or s in repetidas:
                        continue
                    lineas.append(s)
                narrativa_limpia = "\n".join(lineas)

                partes_tabla = []
                for t in tablas:
                    try:
                        md = _tabla_a_markdown(t.extract())
                    except Exception:
                        md = ""
                    if md:
                        partes_tabla.append(md)

                page_content = narrativa_limpia
                if partes_tabla:
                    page_content = (page_content + "\n\n" + "\n\n".join(partes_tabla)).strip()
                if not page_content.strip():
                    continue

                for text in splitter.split_text(page_content):
                    metadata = _metadata_pdf(filepath, page_no, chunk_index)
                    chunks.append(Document(page_content=_texto_chunk(text, metadata), metadata=metadata))
                    chunk_index += 1
    except Exception as e:
        print(f"[PDF] pdfplumber fallo en {filepath}: {e}. Fallback a PyPDFLoader.")
        return _crear_chunks_pdf_pypdf(filepath)

    return chunks if chunks else _crear_chunks_pdf_pypdf(filepath)


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
        metadata.update({
            "lesson_title": metadata_doc.get("lesson_title", "")
                or metadata.get("lesson_title")
                or metadata.get("section_title")
                or _stem(os.path.basename(filepath)),
            "url": "",
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

    # Fase 4: política de fuente activa. En modo teacher_flow, el markdown canónico
    # de la sección gobernada es SEMILLA (no evidencia): no se (re)indexa, aunque el
    # archivo siga en disco. Esto hace la supersesión (Fase 5) DURABLE ante un rebuild.
    if filepath.lower().endswith(".md") and _en_curso_canonico(filepath):
        _dm = obtener_metadata_documental(filepath)
        if str(_dm.get("source") or "").strip().lower() == "canonical_md":
            from config import canonical_md_is_active_source
            _c = _dm.get("course_id") or _inferir_course_id(filepath)
            _s = _dm.get("moodle_section_id") or _dm.get("section_id") or ""
            if not canonical_md_is_active_source(_c, _s):
                _log_ingest_decision("SKIP", filepath, ["canonical_md inactivo (modo teacher_flow) para esta seccion"])
                return {
                    "success": False,
                    "skipped": True,
                    "message": "canonical_md inactivo en modo teacher_flow para esta seccion (semilla, no evidencia).",
                    "reasons": ["source_mode=teacher_flow"],
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
    Elimina los fragmentos de un documento especifico de ChromaDB por su ruta.
    La ruta vive en `source_path` (relativa a tesis-rag/). Se intentan varias
    formas por compatibilidad con índices viejos que guardaban la ruta en `source`.
    """
    db = get_vector_store()
    collection = db._collection

    relpath = _normalizar_path(os.path.relpath(filepath, BASE_DIR)) if os.path.isabs(filepath) else _normalizar_path(filepath)
    variantes = {
        relpath,
        _normalizar_path(filepath),
        filepath.replace("/", "\\"),
        filepath.replace("\\", "/"),
    }
    try:
        for v in variantes:
            collection.delete(where={"source_path": v})
            collection.delete(where={"source": v})  # compat índice viejo
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
    # Limpieza ACOTADA: borra solo el conocimiento DB-driven del curso
    # (transcripciones y descripciones de recursos), que se re-agrega abajo.
    # NO toca el corpus canónico por sección (source='canonical_md'), que lo
    # gestiona rebuild_all_documents / add_single_document por archivo. Antes se
    # borraba TODO el curso aquí y eso aniquilaba el corpus canónico tras un rebuild.
    for src in ("transcript", "resource_file"):
        try:
            db._collection.delete(where={"$and": [{"course_id": course}, {"source": src}]})
        except Exception as e:
            print(f"Nota al borrar chunks DB-driven ({src}) del curso {course}: {e}")

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
            moodle_section_id=doc.get("moodle_section_id", ""),
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
        tr = index_lesson_transcript(
            course,
            lid,
            segments,
            axis_id="",
            moodle_section_id=lesson.get("moodle_section_id", ""),
            lesson_title=(lesson.get("title") or lesson.get("lesson_title") or ""),
        )
        if tr.get("success") and tr.get("chunks"):
            transcripts_indexed += 1

        # Flujo docente: reindexa también el contexto aprobado de la lección (si el
        # perfil pedagógico tiene contenido aprobado). delete-then-add por lección.
        try:
            from services import teacher_context
            doc = teacher_context.build_teacher_approved_context_document(lid, course)
            if doc and doc.get("has_content"):
                index_teacher_approved_context(
                    course, lid, doc["chunks"],
                    lesson_title=doc["metadata"].get("lesson_title", ""),
                    moodle_section_id=lesson.get("moodle_section_id", ""),
                    updated_at=doc["metadata"].get("updated_at", ""),
                    source_hash=doc["metadata"].get("source_hash", ""),
                )
            else:
                delete_teacher_approved_context(lid)
        except Exception as e:
            print(f"[reindex] teacher_context de {lid} no reindexado: {e}")

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


def index_lesson_transcript(course_id, lesson_id, segments, axis_id="", resource_id="",
                            moodle_section_id="", lesson_title=""):
    """Indexa (RAG) la transcripción de una lección como conocimiento canónico.

    Agrupa los segmentos en chunks (~700 chars) conservando el tiempo de inicio/fin
    para que el tutor pueda citar el minuto. Patrón delete-then-add por lección:
    borra los chunks previos con source="transcription:<lesson_id>" y re-inserta.
    Pensado para llamarse al guardar/auto-transcribir (datos en BD, sin archivo).

    `lesson_title` (humano) se usa como etiqueta de fuente; si viene vacío se cae al
    lesson_id (evita mostrar IDs técnicos tipo SEC2-R59 cuando hay título real).
    """
    course = str(course_id or "").strip()
    lid = str(lesson_id or "").strip()
    if not lid:
        return {"success": False, "chunks": 0, "message": "lesson_id requerido"}

    source_tag = f"transcription:{lid}"
    store = get_vector_store()
    sec_id = str(moodle_section_id or "").strip()
    sec_meta = _section_meta_for_id(course, sec_id) if sec_id else {}
    human_title = str(lesson_title or "").strip() or lid

    # 1) Borrar chunks previos de esta transcripción.
    try:
        store._collection.delete(where={"source_path": source_tag})
        store._collection.delete(where={"source": source_tag})  # compat con índice viejo
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
            "moodle_section_id": sec_id,
            "section_id": sec_id,
            "section_number": str(sec_meta.get("section_number") or ""),
            "section_title": str(sec_meta.get("section_title") or ""),
            "section_slug": str(sec_meta.get("section_slug") or ""),
            "lesson_id": lid,
            "lesson_title": human_title,
            "title": human_title,
            "block_id": "",
            "block_title": "",
            "resource_id": str(resource_id or ""),
            "start_time": float(ch["start"] or 0),
            "end_time": float(ch["end"] or 0),
            "layer": "transcript",
            "doc_type": "video_transcript",
            "content_type": "transcript",
            "source": "transcript",
            "source_path": source_tag,
            "source_hash": hashlib.md5(f"{source_tag}:{i}".encode("utf-8")).hexdigest(),
            "version": "",
            "index_status": "indexed",
            "chunk_index": i,
            "chunk_id": f"{source_tag}:{i}",
            # La transcripcion es conocimiento del curso (scope lección): el tutor
            # la usa y la puede citar; no es un archivo descargable.
            "scope": _scope_chunk(course, lid, False, "lesson" if lid else "", sec_id, ""),
            "is_global": False,
            "visible_to_student": True,
            "allowed_for_indexing": True,
            "resource_type": "transcript",
        })
        ids.append(f"{source_tag}:{i}")

    store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
    try:
        store.persist()
    except Exception:
        pass  # chromadb reciente persiste solo

    return {"success": True, "chunks": len(chunks), "course_id": course, "lesson_id": lid}


def index_teacher_approved_context(course_id, lesson_id, chunks, *, lesson_title="",
                                   moodle_section_id="", updated_at="", source_hash="",
                                   axis_id=""):
    """Indexa (RAG) el CONTEXTO APROBADO de la lección: la fuente textual derivada del
    editor docente (perfil pedagógico aceptado). Flujo docente, Fase 5/6.

    A diferencia de la transcripción (fiel al video), esto materializa lo que el
    PROFESOR aprobó como conocimiento indexable: objetivo, resumen, conceptos,
    errores comunes, preguntas probables, momentos y recursos aprobados. NO incluye
    comportamiento del tutor (tono/nivel/reglas privadas/must_not_do): eso se INYECTA,
    no se INDEXA. Patrón delete-then-add por lección: borra
    source_path="teacher_context:<lesson_id>" y re-inserta un chunk por sección.

    `chunks` es una lista de strings (una por sección del documento); cada uno se
    indexa como un fragmento autocontenido (ya viene prefijado con el título humano).
    """
    course = str(course_id or "").strip()
    lid = str(lesson_id or "").strip()
    if not lid:
        return {"success": False, "chunks": 0, "message": "lesson_id requerido"}

    source_tag = f"teacher_context:{lid}"
    store = get_vector_store()
    sec_id = str(moodle_section_id or "").strip()
    sec_meta = _section_meta_for_id(course, sec_id) if sec_id else {}
    human_title = str(lesson_title or "").strip() or lid
    updated = str(updated_at or "").strip() or datetime.now(timezone.utc).isoformat()
    base_hash = str(source_hash or "").strip()

    # 1) Borrar chunks previos de este contexto (delete-then-add por lección).
    try:
        store._collection.delete(where={"source_path": source_tag})
        store._collection.delete(where={"$and": [{"source": "authoring_profile"}, {"lesson_id": lid}]})
    except Exception as e:  # pragma: no cover
        print(f"Nota al borrar teacher_context chunks de {lid}: {e}")

    limpio = [str(c).strip() for c in (chunks or []) if str(c or "").strip()]
    if not limpio:
        return {"success": True, "chunks": 0, "message": "contexto vacío (solo se limpió el índice)"}

    scope_val = _scope_chunk(course, lid, False, "lesson", sec_id, "")
    texts, metadatas, ids = [], [], []
    for i, ch in enumerate(limpio):
        texts.append(ch)
        metadatas.append({
            "course_id": course,
            "moodle_section_id": sec_id,
            "section_id": sec_id,
            "section_number": str(sec_meta.get("section_number") or ""),
            "section_title": str(sec_meta.get("section_title") or ""),
            "section_slug": str(sec_meta.get("section_slug") or ""),
            "lesson_id": lid,
            "lesson_title": human_title,
            "title": human_title,
            "block_id": "",
            "block_title": "",
            "resource_id": "",
            "layer": "teacher_context",
            "doc_type": "teacher_approved_context",
            "content_type": "teacher_context",
            # Contrato del flujo docente.
            "source": "authoring_profile",
            "source_type": "teacher_approved_context",
            "source_path": source_tag,
            "source_hash": (base_hash or hashlib.md5(f"{source_tag}:{i}".encode("utf-8")).hexdigest()),
            "generated_from": "ai_prepare_acceptance",
            "status": "teacher_approved",
            "internal_context": False,
            "corpus_version": "teacher_flow_v1",
            "updated_at": updated,
            "version": "",
            "index_status": "indexed",
            "chunk_index": i,
            "chunk_id": f"{source_tag}:{i}",
            "scope": scope_val,
            "is_global": False,
            "visible_to_student": True,
            "allowed_for_indexing": True,
            "resource_type": "teacher_context",
        })
        ids.append(f"{source_tag}:{i}")

    store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
    try:
        store.persist()
    except Exception:
        pass  # chromadb reciente persiste solo

    return {"success": True, "chunks": len(limpio), "course_id": course, "lesson_id": lid,
            "source_path": source_tag}


def delete_teacher_approved_context(lesson_id):
    """Borra del índice los chunks de contexto aprobado de una lección."""
    lid = str(lesson_id or "").strip()
    if not lid:
        return {"success": False, "deleted": True}
    try:
        coll = get_vector_store()._collection
        coll.delete(where={"source_path": f"teacher_context:{lid}"})
        coll.delete(where={"$and": [{"source": "authoring_profile"}, {"lesson_id": lid}]})
    except Exception as e:  # pragma: no cover
        print(f"Nota al borrar teacher_context index {lid}: {e}")
    return {"success": True, "lesson_id": lid}


def index_resource_description(course_id, lesson_id, doc_id, title, description,
                               concepts=None, axis_id="", media_type="file",
                               moodle_section_id="",
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
    sec_id = str(moodle_section_id or "").strip()
    sec_meta = _section_meta_for_id(str(course_id or ""), sec_id) if sec_id else {}
    try:
        store._collection.delete(where={"source_path": source_tag})
        store._collection.delete(where={"source": source_tag})  # compat con índice viejo
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
        "moodle_section_id": sec_id,
        "section_id": sec_id,
        "section_number": str(sec_meta.get("section_number") or ""),
        "section_title": str(sec_meta.get("section_title") or ""),
        "section_slug": str(sec_meta.get("section_slug") or ""),
        "lesson_id": str(lesson_id or ""),
        "lesson_title": "",
        "block_id": "",
        "block_title": "",
        "resource_id": did,
        "layer": "resource",
        "doc_type": doc_type or media_type or "resource",
        "content_type": media_type or "file",
        "source": "resource_file",
        "source_path": source_tag,
        "source_hash": hashlib.md5(source_tag.encode("utf-8")).hexdigest(),
        "version": "",
        "index_status": "indexed",
        "title": title or did,
        "media_type": media_type or "file",
        "media_path": (media_path or "").replace("\\", "/"),
        "scope": _scope_chunk(str(course_id or ""), str(lesson_id or ""),
                              _as_bool(is_global, False), scope, sec_id, ""),
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
        coll = get_vector_store()._collection
        coll.delete(where={"source_path": f"resource:{did}"})
        coll.delete(where={"source": f"resource:{did}"})  # compat índice viejo
    except Exception as e:  # pragma: no cover
        print(f"Nota al borrar resource index {did}: {e}")


def count_section_canonical(course_id: str, moodle_section_id: str) -> int:
    """Cuántos chunks canonical_md hay indexados para una (curso, sección)."""
    c, s = str(course_id or ""), str(moodle_section_id or "")
    try:
        coll = get_vector_store()._collection
        r = coll.get(where={"$and": [
            {"course_id": c}, {"moodle_section_id": s}, {"source": "canonical_md"},
        ]})
        return len(r.get("ids") or [])
    except Exception as e:  # pragma: no cover
        print(f"[supersede] no se pudo contar canonical_md de {c}/{s}: {e}")
        return -1


def supersede_section_canonical(course_id: str, moodle_section_id: str) -> dict:
    """Fase 5: retira del ÍNDICE los chunks canonical_md de una sección (superseded
    por el flujo docente). NO borra los archivos .md del repo (siguen como semilla).
    Devuelve conteos antes/después para auditar. Delete acotado por metadata exacta:
    course_id + moodle_section_id + source='canonical_md' (no toca transcript,
    teacher_context, resource_file ni otras secciones)."""
    c, s = str(course_id or ""), str(moodle_section_id or "")
    if not c or not s:
        return {"success": False, "message": "course_id y moodle_section_id requeridos"}
    before = count_section_canonical(c, s)
    try:
        coll = get_vector_store()._collection
        coll.delete(where={"$and": [
            {"course_id": c}, {"moodle_section_id": s}, {"source": "canonical_md"},
        ]})
        try:
            get_vector_store().persist()
        except Exception:
            pass
    except Exception as e:
        return {"success": False, "message": f"error borrando canonical_md: {e}", "before": before}
    after = count_section_canonical(c, s)
    removed = (before - after) if (before >= 0 and after >= 0) else None
    return {"success": True, "course_id": c, "moodle_section_id": s,
            "before": before, "after": after, "removed": removed,
            "reason": "superseded_by_teacher_flow"}


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
