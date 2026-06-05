import sqlite3

DB_PATH = "portfolio.db"

def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con
