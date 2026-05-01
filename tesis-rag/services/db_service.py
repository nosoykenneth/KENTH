import sqlite3
import os
import uuid
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
