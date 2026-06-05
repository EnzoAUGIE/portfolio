from database.db import get_db

def get_skills() -> list:
    con = get_db()
    skills = [dict(r) for r in con.execute("SELECT * FROM skills").fetchall()]
    con.close()
    return skills

def create_skill(name: str, level: str):
    con = get_db()
    con.execute("INSERT INTO skills (name, level) VALUES (?, ?)", (name, level))
    con.commit()
    con.close()

def update_skill(skill_id: int, name: str, level: str):
    con = get_db()
    con.execute("UPDATE skills SET name=?, level=? WHERE id=?", (name, level, skill_id))
    con.commit()
    con.close()

def delete_skill(skill_id: int):
    con = get_db()
    con.execute("DELETE FROM skills WHERE id=?", (skill_id,))
    con.commit()
    con.close()
