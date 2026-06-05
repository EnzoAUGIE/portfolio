# Tier 3 — Données
# Ce fichier gère la connexion à la base de données SQLite

import sqlite3

# Chemin vers le fichier de base de données
DB_PATH = "portfolio.db"


def get_db():
    # Ouvre une connexion à la base de données SQLite
    con = sqlite3.connect(DB_PATH)
    # Permet de récupérer les résultats sous forme de dictionnaire
    # au lieu de tuples, ex: row["name"] au lieu de row[0]
    con.row_factory = sqlite3.Row
    return con
