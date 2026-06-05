from database.db import get_db

def get_profile() -> dict:
    con = get_db()
    profile = dict(con.execute("SELECT * FROM profile WHERE id=1").fetchone())
    con.close()
    return profile

def update_profile(name: str, titre: str, bio: str, email: str):
    con = get_db()
    con.execute("UPDATE profile SET name=?, titre=?, bio=?, email=? WHERE id=1",
                (name, titre, bio, email))
    con.commit()
    con.close()
