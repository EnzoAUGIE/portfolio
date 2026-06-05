from database.db import get_db

def get_contact(user_id: int) -> dict:
    con = get_db()
    row = con.execute("SELECT * FROM contact WHERE user_id=?", (user_id,)).fetchone()
    con.close()
    return dict(row) if row else {}

def update_contact(user_id: int, email: str, linkedin: str = None, github: str = None, localisation: str = None):
    con = get_db()
    con.execute("UPDATE contact SET email=?, linkedin=?, github=?, localisation=? WHERE user_id=?",
                (email, linkedin, github, localisation, user_id))
    con.commit()
    con.close()
