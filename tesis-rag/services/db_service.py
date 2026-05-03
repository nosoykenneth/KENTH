import sqlite3
import os
import uuid
import json
from datetime import datetime

DB_PATH = "./bd_chat/chats.db"

def get_connection():
    os.makedirs("./bd_chat", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Tabla de Chats (Sesiones)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Tabla de Mensajes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            chat_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES chats (id) ON DELETE CASCADE
        )
    """)
    # AUDIT FIX #5: Tabla de trazas RAG por mensaje del asistente.
    # Persiste ruta, evidence_level y fuentes para auditar calidad del retrieval.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS message_traces (
            id TEXT PRIMARY KEY,
            message_id TEXT NOT NULL,
            ruta TEXT,
            evidence_level TEXT,
            fuentes_json TEXT,
            trace_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (message_id) REFERENCES messages (id) ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interaction_traces (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            trace_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("PRAGMA table_info(message_traces)")
    trace_columns = [row["name"] for row in cursor.fetchall()]
    if "trace_json" not in trace_columns:
        cursor.execute("ALTER TABLE message_traces ADD COLUMN trace_json TEXT")
    conn.commit()
    conn.close()

def create_chat(user_id: str, title: str = "Nuevo Chat") -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    chat_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO chats (id, user_id, title, created_at) VALUES (?, ?, ?, ?)",
        (chat_id, user_id, title, created_at)
    )
    conn.commit()
    conn.close()
    return {"id": chat_id, "user_id": user_id, "title": title, "created_at": created_at}

def get_user_chats(user_id: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chats WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def delete_chat(chat_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
    cursor.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

def add_message(chat_id: str, role: str, content: str, image: str = None) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    msg_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO messages (id, chat_id, role, content, image, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (msg_id, chat_id, role, content, image, created_at)
    )
    conn.commit()
    conn.close()
    return {"id": msg_id, "chat_id": chat_id, "role": role, "content": content, "image": image, "created_at": created_at}

def get_chat_messages(chat_id: str) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE chat_id = ? ORDER BY created_at ASC", (chat_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def save_trace(
    message_id: str,
    ruta: str = "",
    evidence_level: str = "",
    fuentes: list = None,
    trace_data: dict = None,
    trace_id: str = None
):
    """Persiste la traza RAG asociada a un mensaje del asistente."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(message_traces)")
        trace_columns = [row["name"] for row in cursor.fetchall()]
        if "trace_json" not in trace_columns:
            cursor.execute("ALTER TABLE message_traces ADD COLUMN trace_json TEXT")
        trace_id = trace_id or str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        fuentes_json = json.dumps(fuentes or [], ensure_ascii=False)
        trace_json = json.dumps(trace_data or {}, ensure_ascii=False)
        cursor.execute(
            """
            INSERT INTO message_traces
            (id, message_id, ruta, evidence_level, fuentes_json, trace_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (trace_id, message_id, ruta, evidence_level, fuentes_json, trace_json, created_at)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[TRACE] Error guardando traza: {e}")


def save_interaction_trace(trace_id: str, session_id: str = "", trace_data: dict = None):
    """Guarda una traza evaluable por interaccion, incluso si no hay chat persistido."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interaction_traces (
                id TEXT PRIMARY KEY,
                session_id TEXT,
                trace_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        created_at = datetime.now().isoformat()
        cursor.execute(
            "INSERT OR REPLACE INTO interaction_traces (id, session_id, trace_json, created_at) VALUES (?, ?, ?, ?)",
            (trace_id, session_id, json.dumps(trace_data or {}, ensure_ascii=False), created_at)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[TRACE] Error guardando traza de interaccion: {e}")
