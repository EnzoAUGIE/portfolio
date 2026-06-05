from database.db import get_db

def get_contact() -> dict:
    con = get_db()
    contact = dict(con.execute("SELECT * FROM contact WHERE id=1").fetchone())
    con.close()
    return contact

def update_contact(email: str, linkedin: str = None, github: str = None, localisation: str = None):
    con = get_db()
    con.execute("UPDATE contact SET email=?, linkedin=?, github=?, localisation=? WHERE id=1",
                (email, linkedin, github, localisation))
    con.commit()
    con.close()
