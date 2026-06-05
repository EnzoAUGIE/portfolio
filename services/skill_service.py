from database.db import get_db

def get_skills(user_id: int) -> list:
    con = get_db()
    skills = [dict(r) for r in con.execute("SELECT * FROM skills WHERE user_id=?", (user_id,)).fetchall()]
    con.close()
    return skills

def create_skill(user_id: int, name: str, level: str):
    con = get_db()
    con.execute("INSERT INTO skills (user_id, name, level) VALUES (?, ?, ?)", (user_id, name, level))
    con.commit()
    con.close()

def update_skill(skill_id: int, user_id: int, name: str, level: str):
    con = get_db()
    con.execute("UPDATE skills SET name=?, level=? WHERE id=? AND user_id=?",
                (name, level, skill_id, user_id))
    con.commit()
    con.close()

def delete_skill(skill_id: int, user_id: int):
    con = get_db()
    con.execute("DELETE FROM skills WHERE id=? AND user_id=?", (skill_id, user_id))
    con.commit()
    con.close()
