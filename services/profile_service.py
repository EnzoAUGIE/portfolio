from database.db import get_db

def get_profile(user_id: int) -> dict:
    con = get_db()
    row = con.execute("SELECT * FROM profile WHERE user_id=?", (user_id,)).fetchone()
    con.close()
    return dict(row) if row else {}

def update_profile(user_id: int, name: str, titre: str, bio: str, email: str):
    con = get_db()
    con.execute("UPDATE profile SET name=?, titre=?, bio=?, email=? WHERE user_id=?",
                (name, titre, bio, email, user_id))
    con.commit()
    con.close()
