# Tier 2 — Logique métier
# Ce fichier gère toute la logique d'authentification :
# création de compte, connexion, sessions et déconnexion
import hashlib
import secrets
from fastapi import Request
from database.db import get_db

# Dictionnaire en mémoire qui stocke les sessions actives
# Format : { token: user_id }
sessions: dict[str, int] = {}


def hash_password(password: str) -> str:
    # Transforme le mot de passe en hash SHA-256
    # Le mot de passe n'est jamais stocké en clair en base de données
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username: str, password: str) -> bool:
    # Crée un nouveau compte utilisateur
    # Retourne True si la création a réussi, False si le nom est déjà pris
    con = get_db()
    try:
        hashed = hash_password(password)
        cur = con.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed)
        )
        user_id = cur.lastrowid
        con.execute(
            "INSERT INTO profile (user_id, name) VALUES (?, ?)", (user_id, username)
        )
        con.execute("INSERT INTO contact (user_id, email) VALUES (?, ?)", (user_id, ""))
        con.commit()
        return True
    except Exception:
        return False
    finally:
        con.close()


def login_user(username: str, password: str) -> str | None:
    # Vérifie les identifiants et crée une session si correct
    # Retourne le token de session ou None si identifiants incorrects
    con = get_db()
    hashed = hash_password(password)
    row = con.execute(
        "SELECT id FROM users WHERE username=? AND password=?", (username, hashed)
    ).fetchone()
    con.close()
    if row:
        token = secrets.token_hex(32)
        sessions[token] = row["id"]
        return token
    return None


def logout_user(token: str):
    sessions.pop(token, None)


def get_current_user_id(request: Request) -> int | None:
    # Récupère l'identifiant de l'utilisateur connecté depuis le cookie
    # Retourne None si l'utilisateur n'est pas connecté
    token = request.cookies.get("session_token")
    return sessions.get(token)


def get_all_users() -> list:
    # Retourne la liste de tous les utilisateurs pour la page d'accueil
    con = get_db()
    users = [dict(r) for r in con.execute("SELECT id, username FROM users").fetchall()]
    con.close()
    return users
