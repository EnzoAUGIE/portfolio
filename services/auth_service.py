import hashlib
import secrets
from fastapi import Request
from database.db import get_db

sessions: dict[str, int] = {}

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, password: str) -> bool:
    con = get_db()
    try:
        hashed = hash_password(password)
        cur = con.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        user_id = cur.lastrowid
        con.execute("INSERT INTO profile (user_id, name) VALUES (?, ?)", (user_id, username))
        con.execute("INSERT INTO contact (user_id, email) VALUES (?, ?)", (user_id, ""))
        con.commit()
        return True
    except Exception:
        return False
    finally:
        con.close()

def login_user(username: str, password: str) -> str | None:
    con = get_db()
    hashed = hash_password(password)
    row = con.execute("SELECT id FROM users WHERE username=? AND password=?", (username, hashed)).fetchone()
    con.close()
    if row:
        token = secrets.token_hex(32)
        sessions[token] = row["id"]
        return token
    return None

def logout_user(token: str):
    sessions.pop(token, None)

def get_current_user_id(request: Request) -> int | None:
    token = request.cookies.get("session_token")
    return sessions.get(token)

def get_all_users() -> list:
    con = get_db()
    users = [dict(r) for r in con.execute("SELECT id, username FROM users").fetchall()]
    con.close()
    return users
