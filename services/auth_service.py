import secrets
from fastapi import Request

sessions: dict[str, bool] = {}

def is_admin(request: Request) -> bool:
    token = request.cookies.get("session_token")
    return token in sessions

def create_session() -> str:
    token = secrets.token_hex(32)
    sessions[token] = True
    return token

def delete_session(token: str):
    if token in sessions:
        del sessions[token]
