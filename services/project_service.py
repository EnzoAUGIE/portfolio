from database.db import get_db

def get_projects(user_id: int) -> list:
    con = get_db()
    projects = [dict(r) for r in con.execute("SELECT * FROM projects WHERE user_id=?", (user_id,)).fetchall()]
    con.close()
    return projects

def create_project(user_id: int, title: str, description: str, link: str = None):
    if link and not link.startswith(("http://", "https://")):
        link = "https://" + link
    con = get_db()
    con.execute("INSERT INTO projects (user_id, title, description, link) VALUES (?, ?, ?, ?)",
                (user_id, title, description, link))
    con.commit()
    con.close()

def update_project(project_id: int, user_id: int, title: str, description: str, link: str = None):
    if link and not link.startswith(("http://", "https://")):
        link = "https://" + link
    con = get_db()
    con.execute("UPDATE projects SET title=?, description=?, link=? WHERE id=? AND user_id=?",
                (title, description, link, project_id, user_id))
    con.commit()
    con.close()

def delete_project(project_id: int, user_id: int):
    con = get_db()
    con.execute("DELETE FROM projects WHERE id=? AND user_id=?", (project_id, user_id))
    con.commit()
    con.close()
