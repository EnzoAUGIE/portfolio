# Tier 2 — Logique métier
# Ce fichier gère les opérations sur les profils utilisateurs
from database.db import get_db


def get_profile(user_id: int) -> dict:
    con = get_db()
    row = con.execute("SELECT * FROM profile WHERE user_id=?", (user_id,)).fetchone()
    con.close()
    return dict(row) if row else {}


def update_profile(user_id: int, name: str, titre: str, bio: str, email: str):
    # Met à jour le profil d'un utilisateur
    # Le WHERE user_id=? garantit qu'on ne modifie que son propre profil
    con = get_db()
    con.execute(
        "UPDATE profile SET name=?, titre=?, bio=?, email=? WHERE user_id=?",
        (name, titre, bio, email, user_id),
    )
    con.commit()
    con.close()
