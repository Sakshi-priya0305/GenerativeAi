from database import get_db
from datetime import datetime

def save_note(user_id: int, content: str):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO notes (user_id, content, created_at) VALUES (%s, %s, %s)",
        (user_id, content, datetime.now())
    )
    conn.commit()
    conn.close()

def get_notes(user_id: int):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT content, created_at FROM notes WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows
