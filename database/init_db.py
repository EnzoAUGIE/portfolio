from database.db import get_db

def init_db():
    con = get_db()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY,
            name TEXT,
            titre TEXT,
            bio TEXT,
            email TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            link TEXT,
            is_featured INTEGER DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            level TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contact (
            id INTEGER PRIMARY KEY,
            email TEXT,
            linkedin TEXT,
            github TEXT,
            localisation TEXT
        )
    """)

    cur.execute("SELECT COUNT(*) FROM profile")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO profile (id, name, titre, bio, email)
            VALUES (1, 'Enzo Augie', 'Etudiant ingénieur à l EPF, majeure Data/IA',
                    'Actuellement en 4ème année à l EPF...', 'enzo.augie@epfedu.fr')
        """)

    cur.execute("SELECT COUNT(*) FROM projects")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO projects (title, description, link, is_featured)
            VALUES ('Portfolio Website', 'Personal website built with FastAPI',
                    'https://example.com', 1)
        """)

    cur.execute("SELECT COUNT(*) FROM skills")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO skills (name, level) VALUES ('Python', 'intermediate')")

    cur.execute("SELECT COUNT(*) FROM contact")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO contact (id, email, linkedin, github, localisation)
            VALUES (1, 'enzo.augie@epfedu.fr', 'https://fr.linkedin.com/in/enzo-augie',
                    'https://github.com/EnzoAUGIE', 'Paris, France')
        """)

    con.commit()
    con.close()
