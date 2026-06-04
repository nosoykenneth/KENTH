"""
Persistencia operativa del tutor.

Regla arquitectonica:
- La base relacional principal es la BD de Moodle.
- Las tablas propias viven como extension del plugin local_tesisai
  (`mdl_local_tesisai_*`, respetando el prefijo real de Moodle).
- SQLite queda solo como fallback local/desarrollo si Moodle no esta disponible.

No se almacena corpus editorial aqui: contenido canonico, paquete limpio,
guiones y PDFs siguen siendo fuentes/indice RAG.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import uuid
import base64
import hashlib
import hmac
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from models.context import Lesson, Resource, ResourceType

try:
    import pymysql
    from pymysql.cursors import DictCursor
except Exception:  # pragma: no cover - se evalua segun entorno local.
    pymysql = None
    DictCursor = None


ROOT = Path(__file__).resolve().parents[1]
SQLITE_DB = Path(os.getenv("SQLITE_DB_PATH", ROOT / "bd_chat" / "chats.db"))
DEFAULT_MOODLE_CONFIG = Path(os.getenv("MOODLE_CONFIG_PATH", r"C:\Moodle\server\moodle\config.php"))

_INITIALIZED = False
_BACKEND: Optional[str] = None
_MOODLE_CFG: Optional[Dict[str, Any]] = None
_KENTH_SECRET: Optional[str] = None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _log(kind: str, **fields: Any) -> None:
    body = " ".join(f"{key}={value}" for key, value in fields.items() if value is not None)
    print(f"[DB {kind}] {body}")


def _source() -> str:
    return "moodle_db" if using_moodle_db() else "fallback_sqlite"


def _log_read(logical_table: str, rows: int, **fields: Any) -> None:
    _log("READ", source=_source(), table=table_name(logical_table), rows=rows, **fields)


def _log_write(logical_table: str, **fields: Any) -> None:
    _log("WRITE", source=_source(), table=table_name(logical_table), **fields)


def _log_fallback(source: str, entity: str, reason: str, **fields: Any) -> None:
    _log("FALLBACK", source=source, entity=entity, reason=reason, **fields)


def _log_error(message: str, **fields: Any) -> None:
    _log("ERROR", message=message, **fields)


def _load_kenth_secret() -> str:
    global _KENTH_SECRET
    if _KENTH_SECRET is not None:
        return _KENTH_SECRET
    secret = os.getenv("KENTH_COURSE_ID_SECRET", "")
    lib_path = DEFAULT_MOODLE_CONFIG.parent / "proyecto_curso" / "api_persistente" / "tesis_lib.php"
    if not secret and lib_path.exists():
        text = lib_path.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"\$KENTH_SECRET\s*=\s*\"([^\"]+)\"", text)
        if m:
            secret = m.group(1)
    _KENTH_SECRET = secret
    return secret


def _sign_course_id(course_id: str) -> Optional[str]:
    secret = _load_kenth_secret()
    if not secret or not course_id:
        return None
    digest = hmac.new(secret.encode("utf-8"), str(course_id).encode("utf-8"), hashlib.sha256).hexdigest()
    signature = digest[:12]
    return base64.b64encode(f"{course_id}.{signature}".encode("utf-8")).decode("ascii")


def _decode_signed_course_id(value: str) -> Optional[str]:
    if not value:
        return None
    try:
        decoded = base64.b64decode(value).decode("utf-8")
    except Exception:
        return None
    parts = decoded.split(".")
    if len(parts) != 2:
        return None
    course_id, signature = parts
    expected = _sign_course_id(course_id)
    if expected == value:
        return course_id
    return None


def _course_id_variants(course_id: Optional[str]) -> List[str]:
    if not course_id:
        return []
    variants = [str(course_id)]
    decoded = _decode_signed_course_id(str(course_id))
    if decoded and decoded not in variants:
        variants.append(decoded)
    signed = _sign_course_id(str(course_id)) if str(course_id).isdigit() else None
    if signed and signed not in variants:
        variants.append(signed)
    if decoded:
        signed_decoded = _sign_course_id(decoded)
        if signed_decoded and signed_decoded not in variants:
            variants.append(signed_decoded)
    return variants


def _load_moodle_config() -> Dict[str, Any]:
    """Lee config.php de Moodle sin ejecutar PHP."""
    global _MOODLE_CFG
    if _MOODLE_CFG is not None:
        return _MOODLE_CFG

    cfg: Dict[str, Any] = {}
    if DEFAULT_MOODLE_CONFIG.exists():
        text = DEFAULT_MOODLE_CONFIG.read_text(encoding="utf-8", errors="ignore")
        for key in ("dbtype", "dbhost", "dbname", "dbuser", "dbpass", "prefix", "dataroot"):
            m = re.search(rf"\$CFG->{key}\s*=\s*'([^']*)'", text)
            if m:
                cfg[key] = m.group(1)
        port = re.search(r"'dbport'\s*=>\s*(\d+)", text)
        if port:
            cfg["dbport"] = int(port.group(1))

    cfg["dbtype"] = os.getenv("MOODLE_DBTYPE", cfg.get("dbtype", "mariadb"))
    cfg["dbhost"] = os.getenv("MOODLE_DBHOST", cfg.get("dbhost", "localhost"))
    cfg["dbport"] = int(os.getenv("MOODLE_DBPORT", cfg.get("dbport", 3306)))
    cfg["dbname"] = os.getenv("MOODLE_DBNAME", cfg.get("dbname", "moodle"))
    cfg["dbuser"] = os.getenv("MOODLE_DBUSER", cfg.get("dbuser", "root"))
    cfg["dbpass"] = os.getenv("MOODLE_DBPASS", cfg.get("dbpass", ""))
    cfg["prefix"] = os.getenv("MOODLE_DB_PREFIX", cfg.get("prefix", "mdl_"))
    # En config.php (single-quoted) los backslashes de Windows van escapados
    # (C:\\moodledata). Des-escapar para obtener una ruta de filesystem valida.
    dataroot = os.getenv("MOODLE_DATAROOT", cfg.get("dataroot", ""))
    cfg["dataroot"] = dataroot.replace("\\\\", "\\").replace("\\'", "'")
    _MOODLE_CFG = cfg
    return cfg


def using_moodle_db() -> bool:
    return _BACKEND == "moodle"


def table_name(logical: str) -> str:
    prefix = _load_moodle_config().get("prefix", "mdl_") if using_moodle_db() else ""
    return f"{prefix}local_tesisai_{logical}"


def _moodle_core_table(name: str) -> str:
    """Tabla core de Moodle (ej. files, context) con el prefijo real."""
    prefix = _load_moodle_config().get("prefix", "mdl_")
    return f"{prefix}{name}"


def _json_dump(value: Any) -> str:
    if value is None:
        value = {}
    return json.dumps(value, ensure_ascii=False)


def _json_load(value: Any, default: Any = None) -> Any:
    if value is None or value == "":
        return [] if default is None else default
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except Exception:
        return [] if default is None else default


def _bool(value: bool) -> int:
    return 1 if value else 0


@contextmanager
def get_connection():
    """Conexion a Moodle/MariaDB o fallback SQLite."""
    global _BACKEND
    cfg = _load_moodle_config()
    force_sqlite = os.getenv("TESISAI_FORCE_SQLITE", "").lower() in {"1", "true", "yes"}
    allow_sqlite_fallback = (
        force_sqlite
        or os.getenv("TESISAI_ALLOW_SQLITE_FALLBACK", "").lower() in {"1", "true", "yes"}
    )
    # En Docker no existe el config.php fisico de Windows; basta con que las
    # variables de entorno definan host/db/user. La existencia del archivo
    # sigue siendo un fallback valido para entornos locales.
    moodle_cfg_available = (
        DEFAULT_MOODLE_CONFIG.exists()
        or bool(os.getenv("MOODLE_DBHOST") and os.getenv("MOODLE_DBNAME"))
    )
    can_use_moodle = (
        not force_sqlite
        and cfg.get("dbtype") in {"mariadb", "mysqli", "mysql"}
        and pymysql is not None
        and moodle_cfg_available
    )

    if can_use_moodle:
        _BACKEND = "moodle"
        try:
            conn = pymysql.connect(
                host=cfg["dbhost"],
                port=int(cfg["dbport"]),
                user=cfg["dbuser"],
                password=cfg["dbpass"],
                database=cfg["dbname"],
                charset="utf8mb4",
                cursorclass=DictCursor,
                autocommit=False,
            )
        except Exception as exc:
            _log_error("moodle_connection_failed", host=cfg["dbhost"], port=cfg["dbport"], db=cfg["dbname"], error=exc)
            raise
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
        return

    _BACKEND = "sqlite"
    reason = "forced" if force_sqlite else ("pymysql_missing" if pymysql is None else "moodle_config_missing")
    if not allow_sqlite_fallback:
        _log_error(
            "moodle_db_unavailable_sqlite_fallback_blocked",
            reason=reason,
            path=SQLITE_DB,
            hint="set TESISAI_ALLOW_SQLITE_FALLBACK=1 only for local dev",
        )
        raise RuntimeError(f"Moodle DB unavailable ({reason}); SQLite fallback is blocked by default.")
    _log_fallback("sqlite", "connection", reason, path=SQLITE_DB)
    SQLITE_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(SQLITE_DB)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _q() -> str:
    return "%s" if using_moodle_db() else "?"


def _row_to_dict(row: Any) -> Optional[Dict[str, Any]]:
    if row is None:
        return None
    return dict(row)


def _fetchone(conn, sql: str, params: Iterable[Any] = ()):
    cur = conn.cursor()
    cur.execute(sql, tuple(params))
    row = cur.fetchone()
    cur.close()
    return _row_to_dict(row)


def _fetchall(conn, sql: str, params: Iterable[Any] = ()) -> List[Dict[str, Any]]:
    cur = conn.cursor()
    cur.execute(sql, tuple(params))
    rows = cur.fetchall()
    cur.close()
    return [dict(r) for r in rows]


def _execute(conn, sql: str, params: Iterable[Any] = ()) -> None:
    cur = conn.cursor()
    cur.execute(sql, tuple(params))
    cur.close()


def init_db() -> None:
    global _INITIALIZED
    if _INITIALIZED:
        return

    with get_connection() as conn:
        if using_moodle_db():
            _init_mysql(conn)
        else:
            _init_sqlite(conn)
    _log("INIT", source=_source(), prefix=_load_moodle_config().get("prefix", ""))
    _INITIALIZED = True


def _init_mysql(conn) -> None:
    lessons = table_name("lessons")
    blocks = table_name("lesson_blocks")
    resources = table_name("course_resources")
    links = table_name("resource_lesson_links")
    prompts = table_name("lesson_prompts")
    sessions = table_name("tutor_sessions")
    messages = table_name("tutor_messages")
    traces = table_name("message_traces")
    interactions = table_name("interaction_traces")
    contexts = table_name("session_context")
    axes = table_name("axes")
    documents = table_name("documents")
    transcripts = table_name("transcript_segments")

    statements = [
        f"""
        CREATE TABLE IF NOT EXISTS {lessons} (
            lesson_id VARCHAR(64) PRIMARY KEY,
            course_id VARCHAR(64) NOT NULL DEFAULT '',
            axis_id VARCHAR(32) NOT NULL DEFAULT '',
            title VARCHAR(255) NOT NULL DEFAULT '',
            lesson_order INT NOT NULL DEFAULT 0,
            learning_goal TEXT NULL,
            expected_action TEXT NULL,
            source_script_file VARCHAR(512) NOT NULL DEFAULT '',
            is_pilot TINYINT(1) NOT NULL DEFAULT 0,
            learning_goals_json LONGTEXT NULL,
            expected_actions_json LONGTEXT NULL,
            resources_json LONGTEXT NULL,
            prerequisites_json LONGTEXT NULL,
            notes LONGTEXT NULL,
            metadata_json LONGTEXT NULL,
            timecreated BIGINT NOT NULL,
            timemodified BIGINT NOT NULL,
            KEY idx_axis (axis_id),
            KEY idx_course (course_id),
            KEY idx_pilot (is_pilot)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        f"""
        CREATE TABLE IF NOT EXISTS {blocks} (
            block_id VARCHAR(96) PRIMARY KEY,
            lesson_id VARCHAR(64) NOT NULL,
            block_order INT NOT NULL DEFAULT 0,
            start_time DOUBLE NULL,
            end_time DOUBLE NULL,
            block_title VARCHAR(255) NOT NULL DEFAULT '',
            summary LONGTEXT NULL,
            interaction_mode VARCHAR(64) NOT NULL DEFAULT '',
            tutor_focus LONGTEXT NULL,
            concepts_json LONGTEXT NULL,
            preguntas_probables_json LONGTEXT NULL,
            metadata_json LONGTEXT NULL,
            timecreated BIGINT NOT NULL,
            timemodified BIGINT NOT NULL,
            UNIQUE KEY uq_lesson_order (lesson_id, block_order),
            KEY idx_lesson_time (lesson_id, start_time, end_time)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        f"""
        CREATE TABLE IF NOT EXISTS {resources} (
            resource_id VARCHAR(96) PRIMARY KEY,
            course_id VARCHAR(64) NOT NULL DEFAULT '',
            axis_id VARCHAR(32) NOT NULL DEFAULT '',
            lesson_id VARCHAR(64) NOT NULL DEFAULT '',
            resource_type VARCHAR(64) NOT NULL DEFAULT 'lesson_note',
            resource_subtype VARCHAR(64) NOT NULL DEFAULT '',
            title VARCHAR(255) NOT NULL DEFAULT '',
            source_uri VARCHAR(512) NOT NULL DEFAULT '',
            duration_seconds INT NULL,
            page_count INT NULL,
            language VARCHAR(16) NOT NULL DEFAULT 'es',
            tags_json LONGTEXT NULL,
            metadata_json LONGTEXT NULL,
            timecreated BIGINT NOT NULL,
            timemodified BIGINT NOT NULL,
            KEY idx_resource_lesson (lesson_id),
            KEY idx_resource_course (course_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        f"""
        CREATE TABLE IF NOT EXISTS {links} (
            resource_id VARCHAR(96) PRIMARY KEY,
            course_id VARCHAR(64) NOT NULL DEFAULT '',
            lesson_id VARCHAR(64) NOT NULL,
            axis_id VARCHAR(32) NOT NULL DEFAULT '',
            resource_type VARCHAR(64) NOT NULL DEFAULT '',
            resource_subtype VARCHAR(64) NOT NULL DEFAULT '',
            timecreated BIGINT NOT NULL,
            timemodified BIGINT NOT NULL,
            KEY idx_link_course (course_id),
            KEY idx_link_lesson (lesson_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        f"""
        CREATE TABLE IF NOT EXISTS {prompts} (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            lesson_id VARCHAR(64) NOT NULL,
            prompt_type VARCHAR(32) NOT NULL,
            prompt_order INT NOT NULL DEFAULT 0,
            prompt_text LONGTEXT NOT NULL,
            timecreated BIGINT NOT NULL,
            timemodified BIGINT NOT NULL,
            UNIQUE KEY uq_prompt (lesson_id, prompt_type, prompt_order),
            KEY idx_prompt_lesson (lesson_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        f"""
        CREATE TABLE IF NOT EXISTS {sessions} (
            session_id VARCHAR(128) PRIMARY KEY,
            user_id VARCHAR(64) NOT NULL DEFAULT '',
            course_id VARCHAR(64) NOT NULL DEFAULT '',
            lesson_id VARCHAR(64) NOT NULL DEFAULT '',
            title VARCHAR(255) NOT NULL DEFAULT 'Nuevo chat',
            timecreated BIGINT NOT NULL,
            timemodified BIGINT NOT NULL,
            KEY idx_session_user (user_id),
            KEY idx_session_user_time (user_id, timemodified)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        f"""
        CREATE TABLE IF NOT EXISTS {messages} (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            session_id VARCHAR(128) NOT NULL,
            user_id VARCHAR(64) NOT NULL DEFAULT '',
            role VARCHAR(32) NOT NULL,
            content LONGTEXT NOT NULL,
            timecreated BIGINT NOT NULL,
            KEY idx_msg_session (session_id, id),
            KEY idx_msg_user (user_id, timecreated)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        f"""
        CREATE TABLE IF NOT EXISTS {traces} (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            session_id VARCHAR(128) NOT NULL,
            message_id BIGINT NULL,
            trace_json LONGTEXT NOT NULL,
            timecreated BIGINT NOT NULL,
            KEY idx_trace_session (session_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        f"""
        CREATE TABLE IF NOT EXISTS {interactions} (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            session_id VARCHAR(128) NOT NULL,
            question LONGTEXT NOT NULL,
            answer LONGTEXT NOT NULL,
            context_json LONGTEXT NULL,
            sources_json LONGTEXT NULL,
            timecreated BIGINT NOT NULL,
            KEY idx_interaction_session (session_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        f"""
        CREATE TABLE IF NOT EXISTS {contexts} (
            session_id VARCHAR(128) PRIMARY KEY,
            student_id VARCHAR(64) NOT NULL DEFAULT '',
            active_context_json LONGTEXT NULL,
            state_json LONGTEXT NULL,
            timemodified BIGINT NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        f"""
        CREATE TABLE IF NOT EXISTS {axes} (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            course_id VARCHAR(64) NOT NULL DEFAULT '',
            axis_id VARCHAR(32) NOT NULL DEFAULT '',
            axis_number INT NOT NULL DEFAULT 0,
            axis_slug VARCHAR(128) NOT NULL DEFAULT '',
            title VARCHAR(255) NOT NULL DEFAULT '',
            pedagogical_role LONGTEXT NULL,
            doc_root VARCHAR(512) NOT NULL DEFAULT '',
            status VARCHAR(64) NOT NULL DEFAULT '',
            axis_order INT NOT NULL DEFAULT 0,
            metadata_json LONGTEXT NULL,
            timecreated BIGINT NOT NULL,
            timemodified BIGINT NOT NULL,
            UNIQUE KEY uq_axis (course_id, axis_id),
            KEY idx_axis_course (course_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        f"""
        CREATE TABLE IF NOT EXISTS {documents} (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            doc_id VARCHAR(96) NOT NULL,
            course_id VARCHAR(64) NOT NULL DEFAULT '',
            axis_id VARCHAR(32) NOT NULL DEFAULT '',
            title VARCHAR(255) NOT NULL DEFAULT '',
            doc_layer VARCHAR(32) NOT NULL DEFAULT 'canonico',
            doc_type VARCHAR(64) NOT NULL DEFAULT '',
            filename VARCHAR(255) NOT NULL DEFAULT '',
            relpath VARCHAR(512) NOT NULL DEFAULT '',
            attribution_required TINYINT(1) NOT NULL DEFAULT 0,
            allowed_for_indexing TINYINT(1) NOT NULL DEFAULT 1,
            ownership VARCHAR(128) NOT NULL DEFAULT '',
            source_uri VARCHAR(512) NOT NULL DEFAULT '',
            status VARCHAR(32) NOT NULL DEFAULT 'active',
            uploaded_by VARCHAR(64) NOT NULL DEFAULT '',
            notes LONGTEXT NULL,
            metadata_json LONGTEXT NULL,
            timecreated BIGINT NOT NULL,
            timemodified BIGINT NOT NULL,
            UNIQUE KEY uq_document (course_id, doc_id),
            KEY idx_doc_course (course_id),
            KEY idx_doc_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        f"""
        CREATE TABLE IF NOT EXISTS {transcripts} (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            lesson_id VARCHAR(64) NOT NULL,
            seq INT NOT NULL DEFAULT 0,
            start_time DOUBLE NULL,
            end_time DOUBLE NULL,
            text LONGTEXT NULL,
            speaker VARCHAR(64) NOT NULL DEFAULT '',
            timecreated BIGINT NOT NULL,
            timemodified BIGINT NOT NULL,
            UNIQUE KEY uq_transcript_seq (lesson_id, seq),
            KEY idx_transcript_lesson (lesson_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
    ]
    for statement in statements:
        _execute(conn, statement)


def _init_sqlite(conn) -> None:
    names = {
        "lessons": table_name("lessons"),
        "blocks": table_name("lesson_blocks"),
        "resources": table_name("course_resources"),
        "links": table_name("resource_lesson_links"),
        "prompts": table_name("lesson_prompts"),
        "sessions": table_name("tutor_sessions"),
        "messages": table_name("tutor_messages"),
        "traces": table_name("message_traces"),
        "interactions": table_name("interaction_traces"),
        "contexts": table_name("session_context"),
        "axes": table_name("axes"),
        "documents": table_name("documents"),
        "transcripts": table_name("transcript_segments"),
    }
    _execute(conn, f"""CREATE TABLE IF NOT EXISTS {names['lessons']} (
        lesson_id TEXT PRIMARY KEY, course_id TEXT DEFAULT '', axis_id TEXT DEFAULT '',
        title TEXT DEFAULT '', lesson_order INTEGER DEFAULT 0, learning_goal TEXT,
        expected_action TEXT, source_script_file TEXT DEFAULT '', is_pilot INTEGER DEFAULT 0,
        learning_goals_json TEXT, expected_actions_json TEXT, resources_json TEXT,
        prerequisites_json TEXT, notes TEXT, metadata_json TEXT,
        timecreated INTEGER, timemodified INTEGER)""")
    _execute(conn, f"""CREATE TABLE IF NOT EXISTS {names['blocks']} (
        block_id TEXT PRIMARY KEY, lesson_id TEXT, block_order INTEGER DEFAULT 0,
        start_time REAL, end_time REAL, block_title TEXT DEFAULT '', summary TEXT,
        interaction_mode TEXT DEFAULT '', tutor_focus TEXT, concepts_json TEXT,
        preguntas_probables_json TEXT, metadata_json TEXT, timecreated INTEGER, timemodified INTEGER)""")
    _execute(conn, f"""CREATE TABLE IF NOT EXISTS {names['resources']} (
        resource_id TEXT PRIMARY KEY, course_id TEXT DEFAULT '', axis_id TEXT DEFAULT '',
        lesson_id TEXT DEFAULT '', resource_type TEXT DEFAULT 'lesson_note', resource_subtype TEXT DEFAULT '',
        title TEXT DEFAULT '', source_uri TEXT DEFAULT '', duration_seconds INTEGER,
        page_count INTEGER, language TEXT DEFAULT 'es', tags_json TEXT, metadata_json TEXT,
        timecreated INTEGER, timemodified INTEGER)""")
    _execute(conn, f"""CREATE TABLE IF NOT EXISTS {names['links']} (
        resource_id TEXT PRIMARY KEY, course_id TEXT DEFAULT '', lesson_id TEXT,
        axis_id TEXT DEFAULT '', resource_type TEXT DEFAULT '', resource_subtype TEXT DEFAULT '',
        timecreated INTEGER, timemodified INTEGER)""")
    _execute(conn, f"""CREATE TABLE IF NOT EXISTS {names['prompts']} (
        id INTEGER PRIMARY KEY AUTOINCREMENT, lesson_id TEXT, prompt_type TEXT,
        prompt_order INTEGER DEFAULT 0, prompt_text TEXT, timecreated INTEGER, timemodified INTEGER,
        UNIQUE(lesson_id, prompt_type, prompt_order))""")
    _execute(conn, f"""CREATE TABLE IF NOT EXISTS {names['sessions']} (
        session_id TEXT PRIMARY KEY, user_id TEXT DEFAULT '', course_id TEXT DEFAULT '',
        lesson_id TEXT DEFAULT '', title TEXT DEFAULT 'Nuevo chat',
        timecreated INTEGER, timemodified INTEGER)""")
    _execute(conn, f"CREATE INDEX IF NOT EXISTS idx_sessions_user_time ON {names['sessions']} (user_id, timemodified)")
    _execute(conn, f"""CREATE TABLE IF NOT EXISTS {names['messages']} (
        id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT, user_id TEXT DEFAULT '', role TEXT, content TEXT, timecreated INTEGER)""")
    _execute(conn, f"CREATE INDEX IF NOT EXISTS idx_messages_user ON {names['messages']} (user_id, timecreated)")
    _execute(conn, f"""CREATE TABLE IF NOT EXISTS {names['traces']} (
        id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT, message_id INTEGER, trace_json TEXT, timecreated INTEGER)""")
    _execute(conn, f"""CREATE TABLE IF NOT EXISTS {names['interactions']} (
        id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT, question TEXT, answer TEXT,
        context_json TEXT, sources_json TEXT, timecreated INTEGER)""")
    _execute(conn, f"""CREATE TABLE IF NOT EXISTS {names['contexts']} (
        session_id TEXT PRIMARY KEY, student_id TEXT DEFAULT '', active_context_json TEXT,
        state_json TEXT, timemodified INTEGER)""")
    _execute(conn, f"""CREATE TABLE IF NOT EXISTS {names['axes']} (
        id INTEGER PRIMARY KEY AUTOINCREMENT, course_id TEXT DEFAULT '', axis_id TEXT DEFAULT '',
        axis_number INTEGER DEFAULT 0, axis_slug TEXT DEFAULT '', title TEXT DEFAULT '',
        pedagogical_role TEXT, doc_root TEXT DEFAULT '', status TEXT DEFAULT '',
        axis_order INTEGER DEFAULT 0, metadata_json TEXT, timecreated INTEGER, timemodified INTEGER,
        UNIQUE(course_id, axis_id))""")
    _execute(conn, f"""CREATE TABLE IF NOT EXISTS {names['documents']} (
        id INTEGER PRIMARY KEY AUTOINCREMENT, doc_id TEXT, course_id TEXT DEFAULT '',
        axis_id TEXT DEFAULT '', title TEXT DEFAULT '', doc_layer TEXT DEFAULT 'canonico',
        doc_type TEXT DEFAULT '', filename TEXT DEFAULT '', relpath TEXT DEFAULT '',
        attribution_required INTEGER DEFAULT 0, allowed_for_indexing INTEGER DEFAULT 1,
        ownership TEXT DEFAULT '', source_uri TEXT DEFAULT '', status TEXT DEFAULT 'active',
        uploaded_by TEXT DEFAULT '', notes TEXT, metadata_json TEXT,
        timecreated INTEGER, timemodified INTEGER, UNIQUE(course_id, doc_id))""")
    _execute(conn, f"""CREATE TABLE IF NOT EXISTS {names['transcripts']} (
        id INTEGER PRIMARY KEY AUTOINCREMENT, lesson_id TEXT, seq INTEGER DEFAULT 0,
        start_time REAL, end_time REAL, text TEXT, speaker TEXT DEFAULT '',
        timecreated INTEGER, timemodified INTEGER, UNIQUE(lesson_id, seq))""")


def _ts() -> int:
    return int(datetime.now(timezone.utc).timestamp())


# ==========================================
# EJES (axes) - estructura del curso en BD
# ==========================================

def _normalize_axis(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "course_id": row.get("course_id", "") or "",
        "axis_id": row.get("axis_id", "") or "",
        "axis_number": row.get("axis_number", 0) or 0,
        "axis_slug": row.get("axis_slug", "") or "",
        "axis_title": row.get("title", "") or "",
        "title": row.get("title", "") or "",
        "pedagogical_role": row.get("pedagogical_role", "") or "",
        "doc_root": row.get("doc_root", "") or "",
        "status": row.get("status", "") or "",
        "axis_order": row.get("axis_order", 0) or 0,
        "metadata": _json_load(row.get("metadata_json"), {}),
    }


def upsert_axis(
    *,
    axis_id: str,
    course_id: str = "",
    axis_number: int = 0,
    axis_slug: str = "",
    title: str = "",
    pedagogical_role: str = "",
    doc_root: str = "",
    status: str = "",
    axis_order: int = 0,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    init_db()
    t = _ts()
    name = table_name("axes")
    with get_connection() as conn:
        if using_moodle_db():
            sql = f"""INSERT INTO {name}
                (course_id, axis_id, axis_number, axis_slug, title, pedagogical_role, doc_root,
                 status, axis_order, metadata_json, timecreated, timemodified)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE axis_number=VALUES(axis_number), axis_slug=VALUES(axis_slug),
                title=VALUES(title), pedagogical_role=VALUES(pedagogical_role), doc_root=VALUES(doc_root),
                status=VALUES(status), axis_order=VALUES(axis_order), metadata_json=VALUES(metadata_json),
                timemodified=VALUES(timemodified)"""
        else:
            sql = f"""INSERT INTO {name}
                (course_id, axis_id, axis_number, axis_slug, title, pedagogical_role, doc_root,
                 status, axis_order, metadata_json, timecreated, timemodified)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(course_id, axis_id) DO UPDATE SET axis_number=excluded.axis_number,
                axis_slug=excluded.axis_slug, title=excluded.title,
                pedagogical_role=excluded.pedagogical_role, doc_root=excluded.doc_root,
                status=excluded.status, axis_order=excluded.axis_order,
                metadata_json=excluded.metadata_json, timemodified=excluded.timemodified"""
        _execute(conn, sql, (
            course_id, axis_id, int(axis_number or 0), axis_slug, title, pedagogical_role,
            doc_root, status, int(axis_order or 0), _json_dump(metadata or {}), t, t,
        ))
    _log_write("axes", id=axis_id, course_id=course_id)


def list_axes(course_id: Optional[str] = None) -> List[Dict[str, Any]]:
    init_db()
    sql = f"SELECT * FROM {table_name('axes')}"
    params: List[Any] = []
    if course_id:
        variants = _course_id_variants(course_id)
        placeholders = ",".join([_q()] * len(variants))
        sql += f" WHERE course_id IN ({placeholders})"
        params.extend(variants)
    sql += " ORDER BY axis_order, axis_number, axis_id"
    with get_connection() as conn:
        rows = _fetchall(conn, sql, params)
    _log_read("axes", len(rows), filter=f"course_id:{course_id}" if course_id else "all")
    return [_normalize_axis(row) for row in rows]


def get_axis(axis_id: str, course_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    init_db()
    sql = f"SELECT * FROM {table_name('axes')} WHERE axis_id={_q()}"
    params: List[Any] = [axis_id]
    if course_id:
        variants = _course_id_variants(course_id)
        placeholders = ",".join([_q()] * len(variants))
        sql += f" AND course_id IN ({placeholders})"
        params.extend(variants)
    with get_connection() as conn:
        row = _fetchone(conn, sql, params)
    _log_read("axes", 1 if row else 0, filter=f"axis_id:{axis_id}")
    return _normalize_axis(row) if row else None


def delete_axis(axis_id: str, course_id: Optional[str] = None) -> bool:
    init_db()
    sql = f"DELETE FROM {table_name('axes')} WHERE axis_id={_q()}"
    params: List[Any] = [axis_id]
    if course_id:
        sql += f" AND course_id={_q()}"
        params.append(str(course_id))
    with get_connection() as conn:
        existing = _fetchone(conn, f"SELECT axis_id FROM {table_name('axes')} WHERE axis_id={_q()}", (axis_id,))
        _execute(conn, sql, params)
    _log_write("axes", id=axis_id, deleted=True)
    return bool(existing)


# ==========================================
# DELETES de lecciones / bloques / prompts / recursos
# ==========================================

def delete_lesson(lesson_id: str) -> bool:
    """Borra una lección y, en cascada lógica, sus bloques y prompts."""
    init_db()
    with get_connection() as conn:
        existing = _fetchone(conn, f"SELECT lesson_id FROM {table_name('lessons')} WHERE lesson_id={_q()}", (lesson_id,))
        _execute(conn, f"DELETE FROM {table_name('lessons')} WHERE lesson_id={_q()}", (lesson_id,))
        _execute(conn, f"DELETE FROM {table_name('lesson_blocks')} WHERE lesson_id={_q()}", (lesson_id,))
        _execute(conn, f"DELETE FROM {table_name('lesson_prompts')} WHERE lesson_id={_q()}", (lesson_id,))
    _log_write("lessons", id=lesson_id, deleted=True)
    return bool(existing)


def delete_lesson_block(block_id: str) -> bool:
    init_db()
    with get_connection() as conn:
        existing = _fetchone(conn, f"SELECT block_id FROM {table_name('lesson_blocks')} WHERE block_id={_q()}", (block_id,))
        _execute(conn, f"DELETE FROM {table_name('lesson_blocks')} WHERE block_id={_q()}", (block_id,))
    _log_write("lesson_blocks", id=block_id, deleted=True)
    return bool(existing)


# ==========================================
# TRANSCRIPCION (segmentos por leccion)
# ==========================================

def list_transcript(lesson_id: str) -> List[Dict[str, Any]]:
    """Segmentos de transcripcion de una leccion, ordenados por seq."""
    init_db()
    with get_connection() as conn:
        rows = _fetchall(
            conn,
            f"SELECT seq, start_time, end_time, text, speaker FROM {table_name('transcript_segments')} "
            f"WHERE lesson_id={_q()} ORDER BY seq, start_time",
            (lesson_id,),
        )
    _log_read("transcript_segments", len(rows), filter=f"lesson_id:{lesson_id}")
    return [
        {
            "seq": r.get("seq", 0),
            "start_time": r.get("start_time"),
            "end_time": r.get("end_time"),
            "text": r.get("text", "") or "",
            "speaker": r.get("speaker", "") or "",
        }
        for r in rows
    ]


def replace_transcript(lesson_id: str, segments: List[Dict[str, Any]]) -> int:
    """Reemplaza el set completo de segmentos de transcripcion (borra y re-inserta).

    El orden del array define `seq`.
    """
    init_db()
    t = _ts()
    name = table_name("transcript_segments")
    with get_connection() as conn:
        _execute(conn, f"DELETE FROM {name} WHERE lesson_id={_q()}", (lesson_id,))
        for idx, seg in enumerate(segments or []):
            cols = "(lesson_id, seq, start_time, end_time, text, speaker, timecreated, timemodified)"
            placeholders = "(%s,%s,%s,%s,%s,%s,%s,%s)" if using_moodle_db() else "(?,?,?,?,?,?,?,?)"
            _execute(
                conn,
                f"INSERT INTO {name} {cols} VALUES {placeholders}",
                (
                    lesson_id,
                    int(seg.get("seq", idx)),
                    seg.get("start_time"),
                    seg.get("end_time"),
                    seg.get("text", "") or "",
                    seg.get("speaker", "") or "",
                    t,
                    t,
                ),
            )
    _log_write("transcript_segments", lesson_id=lesson_id, replaced=len(segments or []))
    return len(segments or [])


# ==========================================
# LOCALIZACION DEL VIDEO H5P EN EL FILESTORE DE MOODLE
# ==========================================

def _moodledata_filepath(contenthash: str) -> Optional[Path]:
    """Ruta fisica de un archivo de Moodle por contenthash (filedir SHA-1)."""
    if not contenthash or len(contenthash) < 4:
        return None
    dataroot = _load_moodle_config().get("dataroot", "")
    if not dataroot:
        return None
    return Path(dataroot) / "filedir" / contenthash[0:2] / contenthash[2:4] / contenthash


def find_hvp_video_path(cmid: int) -> Optional[Dict[str, Any]]:
    """Localiza el archivo de video subido dentro de un modulo H5P (hvp/h5pactivity).

    Busca en `files` cualquier archivo con mimetype video/* atado al contexto del
    course module (contextlevel=70, instanceid=cmid) y devuelve el mas grande. Solo
    funciona contra la BD de Moodle (no SQLite). Devuelve None si no hay video local
    (p. ej. H5P que referencia un video externo por URL).
    """
    init_db()
    if not using_moodle_db():
        _log_error("find_hvp_video_path requires moodle_db", cmid=cmid)
        return None
    files = _moodle_core_table("files")
    context = _moodle_core_table("context")
    sql = (
        f"SELECT f.contenthash, f.filename, f.filesize, f.mimetype "
        f"FROM {files} f JOIN {context} ctx ON ctx.id = f.contextid "
        f"WHERE ctx.contextlevel = 70 AND ctx.instanceid = %s "
        f"AND f.mimetype LIKE 'video/%%' AND f.filesize > 0 "
        f"ORDER BY f.filesize DESC LIMIT 1"
    )
    with get_connection() as conn:
        row = _fetchone(conn, sql, (int(cmid),))
    if not row:
        _log_read("moodle_files", 0, filter=f"cmid:{cmid}", kind="hvp_video")
        return None
    path = _moodledata_filepath(row.get("contenthash", ""))
    if not path or not path.exists():
        _log_error("hvp_video_file_missing_on_disk", cmid=cmid, contenthash=row.get("contenthash"), path=str(path))
        return None
    return {
        "path": str(path),
        "filename": row.get("filename", ""),
        "mimetype": row.get("mimetype", ""),
        "filesize": row.get("filesize", 0),
        "contenthash": row.get("contenthash", ""),
    }


def replace_lesson_blocks(lesson_id: str, blocks: List[Dict[str, Any]]) -> int:
    """Reemplaza el set completo de bloques de una lección (borra y re-inserta).

    Cada bloque es un dict con las claves de upsert_lesson_block. El orden del
    array define block_order.
    """
    init_db()
    with get_connection() as conn:
        _execute(conn, f"DELETE FROM {table_name('lesson_blocks')} WHERE lesson_id={_q()}", (lesson_id,))
    for idx, block in enumerate(blocks or []):
        upsert_lesson_block(
            block_id=block.get("block_id") or f"{lesson_id}-B{idx + 1}",
            lesson_id=lesson_id,
            block_order=block.get("block_order", idx),
            start_time=block.get("start_time"),
            end_time=block.get("end_time"),
            block_title=block.get("block_title", ""),
            summary=block.get("summary", ""),
            interaction_mode=block.get("interaction_mode", ""),
            tutor_focus=block.get("tutor_focus", ""),
            concepts=block.get("concepts", []),
            preguntas_probables=block.get("preguntas_probables", []),
            metadata=block.get("metadata", {}),
        )
    _log_write("lesson_blocks", lesson_id=lesson_id, replaced=len(blocks or []))
    return len(blocks or [])


def delete_lesson_prompts(lesson_id: str, prompt_type: Optional[str] = None) -> None:
    """Borra prompts de una lección (todos o de un tipo: proactive|suggested)."""
    init_db()
    sql = f"DELETE FROM {table_name('lesson_prompts')} WHERE lesson_id={_q()}"
    params: List[Any] = [lesson_id]
    if prompt_type:
        sql += f" AND prompt_type={_q()}"
        params.append(prompt_type)
    with get_connection() as conn:
        _execute(conn, sql, params)
    _log_write("lesson_prompts", lesson_id=lesson_id, prompt_type=prompt_type or "all", deleted=True)


def set_lesson_prompts(
    lesson_id: str,
    *,
    proactive_message: str = "",
    suggested_prompts: Optional[List[str]] = None,
) -> None:
    """Reemplaza por completo los prompts de una lección."""
    delete_lesson_prompts(lesson_id)
    if proactive_message:
        upsert_lesson_prompt(lesson_id, "proactive", proactive_message, 0)
    for order, text in enumerate(suggested_prompts or []):
        if text:
            upsert_lesson_prompt(lesson_id, "suggested", text, order)


def delete_resource(resource_id: str) -> bool:
    init_db()
    with get_connection() as conn:
        existing = _fetchone(conn, f"SELECT resource_id FROM {table_name('course_resources')} WHERE resource_id={_q()}", (resource_id,))
        _execute(conn, f"DELETE FROM {table_name('course_resources')} WHERE resource_id={_q()}", (resource_id,))
    _log_write("course_resources", id=resource_id, deleted=True)
    return bool(existing)


# ==========================================
# DOCUMENTOS RAG (registro por curso)
# ==========================================

def _normalize_document(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "doc_id": row.get("doc_id", "") or "",
        "course_id": row.get("course_id", "") or "",
        "axis_id": row.get("axis_id", "") or "",
        "title": row.get("title", "") or "",
        "doc_layer": row.get("doc_layer", "canonico") or "canonico",
        "doc_type": row.get("doc_type", "") or "",
        "filename": row.get("filename", "") or "",
        "relpath": row.get("relpath", "") or "",
        "attribution_required": bool(row.get("attribution_required")),
        "allowed_for_indexing": bool(row.get("allowed_for_indexing")),
        "ownership": row.get("ownership", "") or "",
        "source_uri": row.get("source_uri", "") or "",
        "status": row.get("status", "active") or "active",
        "uploaded_by": row.get("uploaded_by", "") or "",
        "notes": row.get("notes", "") or "",
        "metadata": _json_load(row.get("metadata_json"), {}),
        "timemodified": row.get("timemodified"),
    }


def upsert_document(
    *,
    doc_id: str,
    course_id: str = "",
    axis_id: str = "",
    title: str = "",
    doc_layer: str = "canonico",
    doc_type: str = "",
    filename: str = "",
    relpath: str = "",
    attribution_required: bool = False,
    allowed_for_indexing: bool = True,
    ownership: str = "",
    source_uri: str = "",
    status: str = "active",
    uploaded_by: str = "",
    notes: str = "",
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    init_db()
    t = _ts()
    name = table_name("documents")
    with get_connection() as conn:
        if using_moodle_db():
            sql = f"""INSERT INTO {name}
                (doc_id, course_id, axis_id, title, doc_layer, doc_type, filename, relpath,
                 attribution_required, allowed_for_indexing, ownership, source_uri, status,
                 uploaded_by, notes, metadata_json, timecreated, timemodified)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE axis_id=VALUES(axis_id), title=VALUES(title),
                doc_layer=VALUES(doc_layer), doc_type=VALUES(doc_type), filename=VALUES(filename),
                relpath=VALUES(relpath), attribution_required=VALUES(attribution_required),
                allowed_for_indexing=VALUES(allowed_for_indexing), ownership=VALUES(ownership),
                source_uri=VALUES(source_uri), status=VALUES(status), uploaded_by=VALUES(uploaded_by),
                notes=VALUES(notes), metadata_json=VALUES(metadata_json), timemodified=VALUES(timemodified)"""
        else:
            sql = f"""INSERT INTO {name}
                (doc_id, course_id, axis_id, title, doc_layer, doc_type, filename, relpath,
                 attribution_required, allowed_for_indexing, ownership, source_uri, status,
                 uploaded_by, notes, metadata_json, timecreated, timemodified)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(course_id, doc_id) DO UPDATE SET axis_id=excluded.axis_id,
                title=excluded.title, doc_layer=excluded.doc_layer, doc_type=excluded.doc_type,
                filename=excluded.filename, relpath=excluded.relpath,
                attribution_required=excluded.attribution_required,
                allowed_for_indexing=excluded.allowed_for_indexing, ownership=excluded.ownership,
                source_uri=excluded.source_uri, status=excluded.status, uploaded_by=excluded.uploaded_by,
                notes=excluded.notes, metadata_json=excluded.metadata_json, timemodified=excluded.timemodified"""
        _execute(conn, sql, (
            doc_id, course_id, axis_id, title, doc_layer, doc_type, filename, relpath,
            _bool(attribution_required), _bool(allowed_for_indexing), ownership, source_uri,
            status, uploaded_by, notes, _json_dump(metadata or {}), t, t,
        ))
    _log_write("documents", id=doc_id, course_id=course_id, status=status)


def list_documents(course_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
    init_db()
    sql = f"SELECT * FROM {table_name('documents')}"
    clauses: List[str] = []
    params: List[Any] = []
    if course_id:
        variants = _course_id_variants(course_id)
        placeholders = ",".join([_q()] * len(variants))
        clauses.append(f"course_id IN ({placeholders})")
        params.extend(variants)
    if status:
        clauses.append(f"status={_q()}")
        params.append(status)
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY axis_id, doc_id"
    with get_connection() as conn:
        rows = _fetchall(conn, sql, params)
    _log_read("documents", len(rows), filter=f"course_id:{course_id}")
    return [_normalize_document(row) for row in rows]


def get_document(doc_id: str, course_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    init_db()
    sql = f"SELECT * FROM {table_name('documents')} WHERE doc_id={_q()}"
    params: List[Any] = [doc_id]
    if course_id:
        sql += f" AND course_id={_q()}"
        params.append(str(course_id))
    with get_connection() as conn:
        row = _fetchone(conn, sql, params)
    return _normalize_document(row) if row else None


def delete_document(doc_id: str, course_id: Optional[str] = None) -> bool:
    init_db()
    sql = f"DELETE FROM {table_name('documents')} WHERE doc_id={_q()}"
    params: List[Any] = [doc_id]
    if course_id:
        sql += f" AND course_id={_q()}"
        params.append(str(course_id))
    with get_connection() as conn:
        existing = _fetchone(conn, f"SELECT doc_id FROM {table_name('documents')} WHERE doc_id={_q()}", (doc_id,))
        _execute(conn, sql, params)
    _log_write("documents", id=doc_id, deleted=True)
    return bool(existing)


# ==========================================
# ROLES MOODLE (autorizacion del profesor)
# ==========================================

def _moodle_table(core_name: str) -> str:
    """Nombre real de una tabla CORE de Moodle (con prefijo), p.ej. 'course' -> 'mdl_course'."""
    prefix = _load_moodle_config().get("prefix", "mdl_") if using_moodle_db() else ""
    return f"{prefix}{core_name}"


def resolve_course_numeric(course_id: str) -> Optional[str]:
    """Devuelve el id numérico del curso Moodle a partir de un course_id que puede
    venir como id numérico ('2'), como id firmado (kenth) o como variante."""
    if not course_id:
        return None
    raw = str(course_id)
    if raw.isdigit():
        return raw
    decoded = _decode_signed_course_id(raw)
    if decoded and decoded.isdigit():
        return decoded
    for variant in _course_id_variants(raw):
        if variant.isdigit():
            return variant
    return None


_TEACHER_ROLE_SHORTNAMES = {"editingteacher", "teacher", "manager", "coursecreator"}


def is_site_admin(user_id: str) -> bool:
    if not using_moodle_db() or not user_id:
        return False
    with get_connection() as conn:
        row = _fetchone(conn, f"SELECT value FROM {_moodle_table('config')} WHERE name='siteadmins'", ())
    if not row:
        return False
    admins = {a.strip() for a in str(row.get("value", "")).split(",") if a.strip()}
    return str(user_id) in admins


def is_course_teacher(user_id: str, course_id: str) -> bool:
    """True si el usuario puede gestionar el curso (rol docente/manager o site admin).

    Reusa la verdad de Moodle: roles asignados en el contexto del curso. En
    fallback SQLite (dev) devuelve True para no bloquear desarrollo local.
    """
    if not using_moodle_db():
        return True
    if not user_id:
        return False
    if is_site_admin(user_id):
        return True
    numeric = resolve_course_numeric(course_id)
    if not numeric:
        return False
    with get_connection() as conn:
        ctx = _fetchone(
            conn,
            f"SELECT id FROM {_moodle_table('context')} WHERE contextlevel=50 AND instanceid={_q()}",
            (numeric,),
        )
        if not ctx:
            return False
        rows = _fetchall(
            conn,
            f"""SELECT r.shortname FROM {_moodle_table('role_assignments')} ra
                JOIN {_moodle_table('role')} r ON r.id = ra.roleid
                WHERE ra.contextid={_q()} AND ra.userid={_q()}""",
            (ctx["id"], user_id),
        )
    shortnames = {str(r.get("shortname", "")).lower() for r in rows}
    return bool(shortnames & _TEACHER_ROLE_SHORTNAMES)


def upsert_lesson(
    *,
    lesson_id: str,
    course_id: str = "",
    axis_id: str = "",
    title: str = "",
    order: int = 0,
    learning_goal: str = "",
    expected_action: str = "",
    source_script_file: str = "",
    is_pilot: bool = False,
    learning_goals: Optional[List[str]] = None,
    expected_actions: Optional[List[str]] = None,
    resources: Optional[List[str]] = None,
    prerequisites: Optional[List[str]] = None,
    notes: str = "",
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    init_db()
    t = _ts()
    with get_connection() as conn:
        name = table_name("lessons")
        if using_moodle_db():
            sql = f"""INSERT INTO {name}
                (lesson_id, course_id, axis_id, title, lesson_order, learning_goal, expected_action,
                 source_script_file, is_pilot, learning_goals_json, expected_actions_json,
                 resources_json, prerequisites_json, notes, metadata_json, timecreated, timemodified)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE course_id=VALUES(course_id), axis_id=VALUES(axis_id),
                title=VALUES(title), lesson_order=VALUES(lesson_order), learning_goal=VALUES(learning_goal),
                expected_action=VALUES(expected_action), source_script_file=VALUES(source_script_file),
                is_pilot=VALUES(is_pilot), learning_goals_json=VALUES(learning_goals_json),
                expected_actions_json=VALUES(expected_actions_json), resources_json=VALUES(resources_json),
                prerequisites_json=VALUES(prerequisites_json), notes=VALUES(notes),
                metadata_json=VALUES(metadata_json), timemodified=VALUES(timemodified)"""
        else:
            sql = f"""INSERT OR REPLACE INTO {name}
                (lesson_id, course_id, axis_id, title, lesson_order, learning_goal, expected_action,
                 source_script_file, is_pilot, learning_goals_json, expected_actions_json,
                 resources_json, prerequisites_json, notes, metadata_json, timecreated, timemodified)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        _execute(conn, sql, (
            lesson_id, course_id, axis_id, title, int(order or 0), learning_goal, expected_action,
            source_script_file, _bool(is_pilot), _json_dump(learning_goals or []),
            _json_dump(expected_actions or []), _json_dump(resources or []),
            _json_dump(prerequisites or []), notes, _json_dump(metadata or {}),
            t, t,
        ))
    _log_write("lessons", id=lesson_id, course_id=course_id, is_pilot=_bool(is_pilot))


def _normalize_lesson(row: Dict[str, Any]) -> Dict[str, Any]:
    prompts = list_lesson_prompts(row["lesson_id"])
    return {
        "lesson_id": row["lesson_id"],
        "course_id": row.get("course_id", ""),
        "axis_id": row.get("axis_id", ""),
        "lesson_title": row.get("title", ""),
        "title": row.get("title", ""),
        "order": row.get("lesson_order", 0),
        "learning_goal": row.get("learning_goal", "") or "",
        "expected_action": row.get("expected_action", "") or "",
        "source_script_file": row.get("source_script_file", "") or "",
        "is_pilot": bool(row.get("is_pilot")),
        "learning_goals": _json_load(row.get("learning_goals_json"), []),
        "expected_actions": _json_load(row.get("expected_actions_json"), []),
        "resources": _json_load(row.get("resources_json"), []),
        "prerequisites": _json_load(row.get("prerequisites_json"), []),
        "notes": row.get("notes", "") or "",
        "metadata": _json_load(row.get("metadata_json"), {}),
        "proactive_message": prompts.get("proactive_message", ""),
        "suggested_prompts": prompts.get("suggested_prompts", []),
    }


def get_lesson(lesson_id: str, course_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    init_db()
    sql = f"SELECT * FROM {table_name('lessons')} WHERE lesson_id={_q()}"
    params: List[Any] = [lesson_id]
    if course_id:
        variants = _course_id_variants(course_id)
        placeholders = ",".join([_q()] * len(variants))
        sql += f" AND course_id IN ({placeholders})"
        params.extend(variants)
    with get_connection() as conn:
        row = _fetchone(conn, sql, params)
    _log_read("lessons", 1 if row else 0, filter=f"lesson_id:{lesson_id} course:{course_id}")
    return _normalize_lesson(row) if row else None


def list_lessons(
    is_pilot: Optional[bool] = None,
    axis_id: Optional[str] = None,
    course_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    init_db()
    sql = f"SELECT * FROM {table_name('lessons')}"
    clauses: List[str] = []
    params: List[Any] = []
    if is_pilot is not None:
        clauses.append(f"is_pilot={_q()}")
        params.append(_bool(is_pilot))
    if axis_id:
        clauses.append(f"axis_id={_q()}")
        params.append(axis_id)
    if course_id:
        variants = _course_id_variants(course_id)
        placeholders = ",".join([_q()] * len(variants))
        clauses.append(f"course_id IN ({placeholders})")
        params.extend(variants)
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY axis_id, lesson_order, lesson_id"
    with get_connection() as conn:
        rows = _fetchall(conn, sql, params)
    _log_read("lessons", len(rows), filter=f"is_pilot:{is_pilot} axis:{axis_id} course:{course_id}")
    return [_normalize_lesson(row) for row in rows]


def upsert_lesson_block(
    *,
    block_id: str,
    lesson_id: str,
    block_order: int = 0,
    start_time: Optional[float] = None,
    end_time: Optional[float] = None,
    block_title: str = "",
    summary: str = "",
    interaction_mode: str = "",
    tutor_focus: str = "",
    concepts: Optional[List[str]] = None,
    preguntas_probables: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    init_db()
    t = _ts()
    name = table_name("lesson_blocks")
    with get_connection() as conn:
        if using_moodle_db():
            sql = f"""INSERT INTO {name}
                (block_id, lesson_id, block_order, start_time, end_time, block_title, summary,
                 interaction_mode, tutor_focus, concepts_json, preguntas_probables_json,
                 metadata_json, timecreated, timemodified)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE lesson_id=VALUES(lesson_id), block_order=VALUES(block_order),
                start_time=VALUES(start_time), end_time=VALUES(end_time), block_title=VALUES(block_title),
                summary=VALUES(summary), interaction_mode=VALUES(interaction_mode),
                tutor_focus=VALUES(tutor_focus), concepts_json=VALUES(concepts_json),
                preguntas_probables_json=VALUES(preguntas_probables_json),
                metadata_json=VALUES(metadata_json), timemodified=VALUES(timemodified)"""
        else:
            sql = f"""INSERT OR REPLACE INTO {name}
                (block_id, lesson_id, block_order, start_time, end_time, block_title, summary,
                 interaction_mode, tutor_focus, concepts_json, preguntas_probables_json,
                 metadata_json, timecreated, timemodified)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        _execute(conn, sql, (
            block_id, lesson_id, int(block_order or 0), start_time, end_time, block_title,
            summary, interaction_mode, tutor_focus, _json_dump(concepts or []),
            _json_dump(preguntas_probables or []), _json_dump(metadata or {}), t, t,
        ))
    _log_write("lesson_blocks", id=block_id, lesson_id=lesson_id)


def _normalize_block(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "block_id": row.get("block_id", ""),
        "lesson_id": row.get("lesson_id", ""),
        "block_order": row.get("block_order", 0),
        "start_time": row.get("start_time"),
        "end_time": row.get("end_time"),
        "block_title": row.get("block_title", ""),
        "summary": row.get("summary", "") or "",
        "interaction_mode": row.get("interaction_mode", "") or "",
        "tutor_focus": row.get("tutor_focus", "") or "",
        "concepts": _json_load(row.get("concepts_json"), []),
        "preguntas_probables": _json_load(row.get("preguntas_probables_json"), []),
        "metadata": _json_load(row.get("metadata_json"), {}),
    }


def list_lesson_blocks(lesson_id: str) -> List[Dict[str, Any]]:
    init_db()
    with get_connection() as conn:
        rows = _fetchall(
            conn,
            f"SELECT * FROM {table_name('lesson_blocks')} WHERE lesson_id={_q()} ORDER BY block_order, start_time",
            (lesson_id,),
        )
    _log_read("lesson_blocks", len(rows), filter=f"lesson_id:{lesson_id}")
    return [_normalize_block(row) for row in rows]


def find_lesson_block_at_timestamp(lesson_id: str, timestamp: Optional[float]) -> Optional[Dict[str, Any]]:
    if timestamp is None:
        return None
    for block in list_lesson_blocks(lesson_id):
        start = block.get("start_time")
        end = block.get("end_time")
        if start is not None and end is not None and float(start) <= float(timestamp) < float(end):
            return block
    return None


def upsert_lesson_prompt(lesson_id: str, prompt_type: str, prompt_text: str, prompt_order: int = 0) -> None:
    init_db()
    t = _ts()
    name = table_name("lesson_prompts")
    with get_connection() as conn:
        if using_moodle_db():
            sql = f"""INSERT INTO {name}
                (lesson_id, prompt_type, prompt_order, prompt_text, timecreated, timemodified)
                VALUES (%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE prompt_text=VALUES(prompt_text), timemodified=VALUES(timemodified)"""
        else:
            sql = f"""INSERT OR REPLACE INTO {name}
                (lesson_id, prompt_type, prompt_order, prompt_text, timecreated, timemodified)
                VALUES (?,?,?,?,?,?)"""
        _execute(conn, sql, (lesson_id, prompt_type, int(prompt_order), prompt_text, t, t))
    _log_write("lesson_prompts", lesson_id=lesson_id, prompt_type=prompt_type, prompt_order=prompt_order)


def list_lesson_prompts(lesson_id: str) -> Dict[str, Any]:
    init_db()
    with get_connection() as conn:
        rows = _fetchall(
            conn,
            f"SELECT prompt_type, prompt_order, prompt_text FROM {table_name('lesson_prompts')} "
            f"WHERE lesson_id={_q()} ORDER BY prompt_type, prompt_order",
            (lesson_id,),
        )
    _log_read("lesson_prompts", len(rows), filter=f"lesson_id:{lesson_id}")
    proactive = ""
    suggested: List[str] = []
    for row in rows:
        if row["prompt_type"] == "proactive":
            proactive = row["prompt_text"]
        elif row["prompt_type"] == "suggested":
            suggested.append(row["prompt_text"])
    return {"proactive_message": proactive, "suggested_prompts": suggested}


def upsert_resource(
    *,
    resource_id: str,
    course_id: str = "",
    axis_id: str = "",
    lesson_id: str = "",
    resource_type: str = "lesson_note",
    resource_subtype: str = "",
    title: str = "",
    source_uri: str = "",
    duration_seconds: Optional[int] = None,
    page_count: Optional[int] = None,
    language: str = "es",
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    init_db()
    t = _ts()
    name = table_name("course_resources")
    with get_connection() as conn:
        if using_moodle_db():
            sql = f"""INSERT INTO {name}
                (resource_id, course_id, axis_id, lesson_id, resource_type, resource_subtype,
                 title, source_uri, duration_seconds, page_count, language, tags_json,
                 metadata_json, timecreated, timemodified)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE course_id=VALUES(course_id), axis_id=VALUES(axis_id),
                lesson_id=VALUES(lesson_id), resource_type=VALUES(resource_type),
                resource_subtype=VALUES(resource_subtype), title=VALUES(title),
                source_uri=VALUES(source_uri), duration_seconds=VALUES(duration_seconds),
                page_count=VALUES(page_count), language=VALUES(language), tags_json=VALUES(tags_json),
                metadata_json=VALUES(metadata_json), timemodified=VALUES(timemodified)"""
        else:
            sql = f"""INSERT OR REPLACE INTO {name}
                (resource_id, course_id, axis_id, lesson_id, resource_type, resource_subtype,
                 title, source_uri, duration_seconds, page_count, language, tags_json,
                 metadata_json, timecreated, timemodified)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        _execute(conn, sql, (
            resource_id, course_id, axis_id, lesson_id, resource_type or "lesson_note",
            resource_subtype, title, source_uri, duration_seconds, page_count, language,
            _json_dump(tags or []), _json_dump(metadata or {}), t, t,
        ))
    _log_write("course_resources", id=resource_id, course_id=course_id, lesson_id=lesson_id)


def get_resource(resource_id: str) -> Optional[Resource]:
    init_db()
    with get_connection() as conn:
        row = _fetchone(conn, f"SELECT * FROM {table_name('course_resources')} WHERE resource_id={_q()}", (resource_id,))
    _log_read("course_resources", 1 if row else 0, filter=f"resource_id:{resource_id}")
    if not row:
        return None
    rtype = row.get("resource_type") or "lesson_note"
    if rtype not in {item.value for item in ResourceType}:
        rtype = "lesson_note"
    return Resource(
        resource_id=row["resource_id"],
        type=ResourceType(rtype),
        title=row.get("title", "") or "",
        axis_id=row.get("axis_id", "") or "",
        lesson_id=row.get("lesson_id", "") or "",
        source_uri=row.get("source_uri", "") or "",
        duration_seconds=row.get("duration_seconds"),
        page_count=row.get("page_count"),
        language=row.get("language", "es") or "es",
        tags=_json_load(row.get("tags_json"), []),
        metadata=_json_load(row.get("metadata_json"), {}),
    )


def upsert_resource_link(
    *,
    resource_id: str,
    lesson_id: str,
    course_id: str = "",
    axis_id: str = "",
    resource_type: str = "",
    resource_subtype: str = "",
) -> Dict[str, Any]:
    init_db()
    t = _ts()
    name = table_name("resource_lesson_links")
    with get_connection() as conn:
        if using_moodle_db():
            sql = f"""INSERT INTO {name}
                (resource_id, course_id, lesson_id, axis_id, resource_type, resource_subtype, timecreated, timemodified)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE course_id=VALUES(course_id), lesson_id=VALUES(lesson_id),
                axis_id=VALUES(axis_id), resource_type=VALUES(resource_type),
                resource_subtype=VALUES(resource_subtype), timemodified=VALUES(timemodified)"""
        else:
            sql = f"""INSERT OR REPLACE INTO {name}
                (resource_id, course_id, lesson_id, axis_id, resource_type, resource_subtype, timecreated, timemodified)
                VALUES (?,?,?,?,?,?,?,?)"""
        _execute(conn, sql, (resource_id, course_id, lesson_id, axis_id, resource_type, resource_subtype, t, t))
    _log_write("resource_lesson_links", id=resource_id, course_id=course_id, lesson_id=lesson_id)
    return get_resource_link(resource_id) or {
        "resource_id": resource_id,
        "course_id": course_id,
        "lesson_id": lesson_id,
        "axis_id": axis_id,
        "resource_type": resource_type,
        "resource_subtype": resource_subtype,
    }


def get_resource_link(resource_id: str) -> Optional[Dict[str, Any]]:
    init_db()
    with get_connection() as conn:
        row = _fetchone(conn, f"SELECT * FROM {table_name('resource_lesson_links')} WHERE resource_id={_q()}", (resource_id,))
    _log_read("resource_lesson_links", 1 if row else 0, filter=f"resource_id:{resource_id}")
    return row


def list_resource_links(course_id: Optional[str] = None) -> List[Dict[str, Any]]:
    init_db()
    sql = f"SELECT * FROM {table_name('resource_lesson_links')}"
    params: List[Any] = []
    if course_id:
        variants = _course_id_variants(course_id)
        placeholders = ",".join([_q()] * len(variants))
        sql += f" WHERE course_id IN ({placeholders})"
        params.extend(variants)
    sql += " ORDER BY course_id, resource_id"
    with get_connection() as conn:
        rows = _fetchall(conn, sql, params)
    _log_read(
        "resource_lesson_links",
        len(rows),
        filter=f"course_id:{course_id}" if course_id else "all",
        variants="|".join(_course_id_variants(course_id)) if course_id else "",
    )
    return rows


def delete_resource_link(resource_id: str) -> bool:
    init_db()
    with get_connection() as conn:
        existing = _fetchone(conn, f"SELECT resource_id FROM {table_name('resource_lesson_links')} WHERE resource_id={_q()}", (resource_id,))
        _execute(conn, f"DELETE FROM {table_name('resource_lesson_links')} WHERE resource_id={_q()}", (resource_id,))
    return bool(existing)


def _normalize_chat(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": row.get("session_id"),
        "session_id": row.get("session_id"),
        "user_id": row.get("user_id", ""),
        "title": row.get("title", "Nuevo chat"),
        "created_at": row.get("timecreated"),
        "updated_at": row.get("timemodified"),
    }


def create_chat(
    user_id: str = "",
    title: str = "Nuevo chat",
    session_id: Optional[str] = None,
    course_id: str = "",
    lesson_id: str = "",
) -> Dict[str, Any]:
    init_db()
    sid = session_id or str(uuid.uuid4())
    t = _ts()
    _log("CHAT_CREATE", auth_user=user_id, session_id=sid, title=title,
         source="moodle_db" if using_moodle_db() else "sqlite")
    try:
        with get_connection() as conn:
            if using_moodle_db():
                sql = f"""INSERT INTO {table_name('tutor_sessions')}
                    (session_id, user_id, course_id, lesson_id, title, timecreated, timemodified)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE title=VALUES(title), timemodified=VALUES(timemodified)"""
            else:
                sql = f"""INSERT OR REPLACE INTO {table_name('tutor_sessions')}
                    (session_id, user_id, course_id, lesson_id, title, timecreated, timemodified) VALUES (?,?,?,?,?,?,?)"""
            _execute(conn, sql, (sid, user_id, course_id, lesson_id, title, t, t))
        _log("CHAT_CREATE", result="ok", inserted_session_id=sid)
    except Exception as e:
        _log("CHAT_CREATE", result="ERROR", error=str(e), session_id=sid)
        raise
    return {"id": sid, "session_id": sid, "user_id": user_id, "title": title, "created_at": t, "updated_at": t}


def ensure_chat_exists(session_id: Optional[str] = None, user_id: str = "", title: str = "Nuevo chat", chat_id: Optional[str] = None) -> None:
    init_db()
    session_id = session_id or chat_id or ""
    if not session_id:
        return
    with get_connection() as conn:
        row = _fetchone(conn, f"SELECT session_id FROM {table_name('tutor_sessions')} WHERE session_id={_q()}", (session_id,))
    if not row:
        create_chat(user_id=user_id, title=title, session_id=session_id)
    else:
        _log_read("tutor_sessions", 1, filter=f"session_id:{session_id}", purpose="ensure_chat_exists")


def get_user_chats(user_id: str, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """Lista sesiones del usuario. user_id es OBLIGATORIO — nunca devuelve todo."""
    if not user_id:
        return []
    init_db()
    sql = f"SELECT * FROM {table_name('tutor_sessions')} WHERE user_id={_q()} ORDER BY timemodified DESC LIMIT {int(limit)} OFFSET {int(offset)}"
    with get_connection() as conn:
        rows = _fetchall(conn, sql, (user_id,))
    _log_read("tutor_sessions", len(rows), filter=f"user_id:{user_id}", limit=limit, offset=offset)
    return [_normalize_chat(row) for row in rows]


def delete_chat(session_id: str) -> bool:
    init_db()
    with get_connection() as conn:
        existing = _fetchone(conn, f"SELECT session_id FROM {table_name('tutor_sessions')} WHERE session_id={_q()}", (session_id,))
        for logical in ("tutor_messages", "message_traces", "interaction_traces", "session_context"):
            _execute(conn, f"DELETE FROM {table_name(logical)} WHERE session_id={_q()}", (session_id,))
        _execute(conn, f"DELETE FROM {table_name('tutor_sessions')} WHERE session_id={_q()}", (session_id,))
    _log_write("tutor_sessions", action="delete", id=session_id, existed=bool(existing))
    return bool(existing)


def add_message(session_id: str, role: str, content: str, image: Optional[str] = None, user_id: str = "") -> Dict[str, Any]:
    init_db()
    ensure_chat_exists(session_id)
    t = _ts()
    # Si no viene user_id explícito, lo resolvemos desde la sesión.
    if not user_id:
        with get_connection() as conn:
            row = _fetchone(conn, f"SELECT user_id FROM {table_name('tutor_sessions')} WHERE session_id={_q()}", (session_id,))
        user_id = (row or {}).get("user_id", "") or ""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO {table_name('tutor_messages')} (session_id, user_id, role, content, timecreated) VALUES ({_q()},{_q()},{_q()},{_q()},{_q()})",
            (session_id, user_id, role, content, t),
        )
        message_id = cur.lastrowid
        cur.close()
        _execute(conn, f"UPDATE {table_name('tutor_sessions')} SET timemodified={_q()} WHERE session_id={_q()}", (t, session_id))
    _log_write("tutor_messages", id=int(message_id or 0), session_id=session_id, role=role, user_id=user_id)
    return {
        "id": int(message_id or 0),
        "session_id": session_id,
        "role": role,
        "content": content,
        "image": image,
        "timecreated": t,
    }


def get_chat_messages(session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    init_db()
    with get_connection() as conn:
        rows = _fetchall(
            conn,
            f"SELECT id, session_id, role, content, timecreated FROM {table_name('tutor_messages')} "
            f"WHERE session_id={_q()} ORDER BY id DESC LIMIT {int(limit)}",
            (session_id,),
        )
    _log_read("tutor_messages", len(rows), filter=f"session_id:{session_id}", limit=limit)
    return list(reversed(rows))


def verify_session_ownership(session_id: str, user_id: str) -> bool:
    """Devuelve True si session_id pertenece a user_id.

    Consulta directa e indexada. Usada por todos los endpoints que
    acceden a sesiones/mensajes para garantizar aislamiento.
    """
    if not session_id or not user_id:
        return False
    init_db()
    with get_connection() as conn:
        row = _fetchone(
            conn,
            f"SELECT user_id FROM {table_name('tutor_sessions')} WHERE session_id={_q()}",
            (session_id,),
        )
    if not row:
        return False
    return row.get("user_id", "") == user_id


def get_user_id_from_token(token: str) -> Optional[str]:
    """Valida un token de Moodle y devuelve el userid.

    Validaciones (replica la lógica de Moodle lib/externallib.php):
      1. El token debe existir en mdl_external_tokens.
      2. validuntil: 0 = sin expiración, >0 = UNIX ts límite.
         Si está expirado, se rechaza.
      3. El external service vinculado debe estar enabled=1.

    Si no estamos usando Moodle DB, devuelve None.
    """
    if not token or not using_moodle_db():
        return None

    init_db()
    with get_connection() as conn:
        prefix = _MOODLE_CFG.get("prefix", "mdl_")
        try:
            row = _fetchone(
                conn,
                f"""SELECT t.userid, t.validuntil, s.enabled
                    FROM {prefix}external_tokens t
                    JOIN {prefix}external_services s
                      ON t.externalserviceid = s.id
                    WHERE t.token={_q()}""",
                (token,),
            )
            if not row or not row.get("userid"):
                _log("AUTH", result="token_not_found")
                return None

            # Servicio deshabilitado por admin
            if not row.get("enabled"):
                _log("AUTH", result="service_disabled", userid=row["userid"])
                return None

            # Expiración: 0 = nunca expira, >0 = timestamp límite
            valid_until = int(row.get("validuntil") or 0)
            if valid_until > 0:
                import time
                if time.time() > valid_until:
                    _log("AUTH", result="token_expired", userid=row["userid"],
                         expired_at=valid_until)
                    return None

            _log("AUTH", result="ok", userid=row["userid"])
            return str(row["userid"])
        except Exception as e:
            _log_error(f"Error validating token: {e}")

    return None


def save_trace(
    session_id: str = "",
    message_id: Optional[Any] = None,
    trace: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> None:
    init_db()
    trace_data = trace or kwargs.get("trace_data") or {}
    if not trace_data:
        trace_data = {
            "trace_id": kwargs.get("trace_id", ""),
            "ruta": kwargs.get("ruta", ""),
            "evidence_level": kwargs.get("evidence_level", ""),
            "fuentes": kwargs.get("fuentes", []),
        }
    session_id = session_id or trace_data.get("session_id") or kwargs.get("trace_id") or ""
    try:
        normalized_message_id = int(message_id) if message_id is not None and str(message_id).isdigit() else None
    except Exception:
        normalized_message_id = None
    with get_connection() as conn:
        _execute(
            conn,
            f"INSERT INTO {table_name('message_traces')} (session_id, message_id, trace_json, timecreated) "
            f"VALUES ({_q()},{_q()},{_q()},{_q()})",
            (session_id, normalized_message_id, _json_dump(trace_data), _ts()),
        )
    _log_write("message_traces", session_id=session_id, message_id=normalized_message_id)


def save_interaction_trace(
    session_id: str = "",
    question: str = "",
    answer: str = "",
    context: Optional[Dict[str, Any]] = None,
    sources: Optional[List[Dict[str, Any]]] = None,
    trace_id: str = "",
    trace_data: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> None:
    init_db()
    trace = trace_data or kwargs.get("trace") or {}
    session_id = session_id or trace.get("session_id") or trace_id or ""
    question = question or trace.get("pregunta", "") or trace.get("question", "")
    answer = answer or trace.get("respuesta", "") or trace.get("answer", "")
    context = context if context is not None else trace
    sources = sources if sources is not None else trace.get("fuentes_finales", trace.get("sources", []))
    with get_connection() as conn:
        _execute(
            conn,
            f"INSERT INTO {table_name('interaction_traces')} "
            f"(session_id, question, answer, context_json, sources_json, timecreated) "
            f"VALUES ({_q()},{_q()},{_q()},{_q()},{_q()},{_q()})",
            (session_id, question, answer, _json_dump(context or {}), _json_dump(sources or []), _ts()),
        )
    _log_write("interaction_traces", session_id=session_id, trace_id=trace_id)


def upsert_session_context(
    session_id: str,
    student_id: str = "",
    active_context: Optional[Dict[str, Any]] = None,
    state: Optional[Dict[str, Any]] = None,
    last_resource_id: str = "",
    last_concept: str = "",
    last_difficulty: str = "",
    recent_concepts: Optional[List[str]] = None,
    signals: Optional[Dict[str, Any]] = None,
    has_image: bool = False,
) -> None:
    init_db()
    name = table_name("session_context")
    t = _ts()
    state_payload = state or {
        "last_resource_id": last_resource_id,
        "last_concept": last_concept,
        "last_difficulty": last_difficulty,
        "recent_concepts": recent_concepts or [],
        "signals": signals or {},
        "has_image": bool(has_image),
    }
    with get_connection() as conn:
        if using_moodle_db():
            sql = f"""INSERT INTO {name}
                (session_id, student_id, active_context_json, state_json, timemodified)
                VALUES (%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE student_id=VALUES(student_id),
                active_context_json=VALUES(active_context_json), state_json=VALUES(state_json),
                timemodified=VALUES(timemodified)"""
        else:
            sql = f"""INSERT OR REPLACE INTO {name}
                (session_id, student_id, active_context_json, state_json, timemodified)
                VALUES (?,?,?,?,?)"""
        _execute(conn, sql, (session_id, student_id, _json_dump(active_context or {}), _json_dump(state_payload), t))
    _log_write("session_context", id=session_id, student_id=student_id)


def get_session_context(session_id: str) -> Optional[Dict[str, Any]]:
    init_db()
    with get_connection() as conn:
        row = _fetchone(conn, f"SELECT * FROM {table_name('session_context')} WHERE session_id={_q()}", (session_id,))
    _log_read("session_context", 1 if row else 0, filter=f"session_id:{session_id}")
    if not row:
        return None
    return {
        "session_id": row["session_id"],
        "student_id": row.get("student_id", ""),
        "active_context": _json_load(row.get("active_context_json"), {}),
        "state": _json_load(row.get("state_json"), {}),
        "updated_at": row.get("timemodified"),
    }
