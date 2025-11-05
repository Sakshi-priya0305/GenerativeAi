from database import get_db
import bcrypt

def create_user(username, password):
    conn = get_db()
    cursor = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def authenticate(username, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row and bcrypt.checkpw(password.encode(), row[1]):
        return row[0]
    return None

