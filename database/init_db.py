# Tier 3 — Données
# Ce fichier initialise la base de données au démarrage de l'application
# Il crée les tables si elles n'existent pas encore (CREATE TABLE IF NOT EXISTS)
from database.db import get_db


def init_db():
    con = get_db()
    cur = con.cursor()

    # Table des utilisateurs
    # Stocke les informations de connexion de chaque utilisateur
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Table des profils
    # Chaque utilisateur a un profil lié via user_id (clé étrangère)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            name TEXT,
            titre TEXT,
            bio TEXT,
            email TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Table des projets
    # Un utilisateur peut avoir plusieurs projets (relation 1 -> N)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT,
            description TEXT,
            link TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Table des compétences
    # idem que projets, un utilisateur peut avoir plusieurs compétences
    cur.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT,
            level TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Table des informations de contact
    # Chaque utilisateur a un seul contact lié via user_id (relation 1 -> 1)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contact (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            email TEXT,
            linkedin TEXT,
            github TEXT,
            localisation TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    con.commit()
    con.close()
