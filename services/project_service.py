from database.db import get_db

def get_projects() -> list:
    con = get_db()
    projects = [dict(r) for r in con.execute("SELECT * FROM projects").fetchall()]
    con.close()
    return projects

def create_project(title: str, description: str, link: str = None):
    con = get_db()
    con.execute("INSERT INTO projects (title, description, link) VALUES (?, ?, ?)",
                (title, description, link))
    con.commit()
    con.close()

def update_project(project_id: int, title: str, description: str, link: str = None):
    con = get_db()
    con.execute("UPDATE projects SET title=?, description=?, link=? WHERE id=?",
                (title, description, link, project_id))
    con.commit()
    con.close()

def delete_project(project_id: int):
    con = get_db()
    con.execute("DELETE FROM projects WHERE id=?", (project_id,))
    con.commit()
    con.close()
