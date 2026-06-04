from typing import Annotated
import os
import sqlite3

from fastapi import FastAPI, Request, Form, status, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import secrets

load_dotenv()

app = FastAPI()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
sessions: dict[str, bool] = {}

# ── Base de données ──────────────────────────────────────────────

DB_PATH = "portfolio.db"


def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


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

    # Données initiales si la table profile est vide
    cur.execute("SELECT COUNT(*) FROM profile")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO profile (id, name, titre, bio, email)
            VALUES (1, 'Enzo Augie', 'Etudiant ingénieur à l EPF, majeure Data/IA',
                    'Actuellement en 4ème année à l EPF...', 'enzo.augie@epfedu.fr')
        """)

    # Données initiales si la table projects est vide
    cur.execute("SELECT COUNT(*) FROM projects")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO projects (title, description, link, is_featured)
            VALUES ('Portfolio Website', 'Personal website built with FastAPI',
                    'https://example.com', 1)
        """)

    # Données initiales si la table skills est vide
    cur.execute("SELECT COUNT(*) FROM skills")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO skills (name, level) VALUES ('Python', 'intermediate')"
        )

    # Données initiales si la table contact est vide
    cur.execute("SELECT COUNT(*) FROM contact")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO contact (id, email, linkedin, github, localisation)
            VALUES (1, 'enzo.augie@epfedu.fr', 'https://fr.linkedin.com/in/enzo-augie',
                    'https://github.com/EnzoAUGIE', 'Paris, France')
        """)

    con.commit()
    con.close()


init_db()

# ── Auth ─────────────────────────────────────────────────────────


def is_admin(request: Request) -> bool:
    token = request.cookies.get("session_token")
    return token in sessions


# ── Login / Logout ────────────────────────────────────────────────

templates = Jinja2Templates(directory="templates")


@app.get("/login", response_class=HTMLResponse)
def show_login(request: Request, error: int = 0):
    return templates.TemplateResponse(
        request=request, name="login.html", context={"error": error}
    )


@app.post("/login")
def do_login(response: Response, password: Annotated[str, Form()]):
    if password != ADMIN_PASSWORD:
        return RedirectResponse("/login?error=1", status_code=303)
    token = secrets.token_hex(32)
    sessions[token] = True
    redirect = RedirectResponse("/admin", status_code=303)
    redirect.set_cookie(key="session_token", value=token, httponly=True, max_age=3600)
    return redirect


@app.get("/logout")
def logout(request: Request):
    token = request.cookies.get("session_token")
    if token in sessions:
        del sessions[token]
    redirect = RedirectResponse("/", status_code=303)
    redirect.delete_cookie("session_token")
    return redirect


# ── Routes principales ────────────────────────────────────────────


@app.get("/", response_class=HTMLResponse)
def show_portfolio(request: Request):
    con = get_db()
    profile = dict(con.execute("SELECT * FROM profile WHERE id=1").fetchone())
    projects = [dict(r) for r in con.execute("SELECT * FROM projects").fetchall()]
    skills = [dict(r) for r in con.execute("SELECT * FROM skills").fetchall()]
    contact = dict(con.execute("SELECT * FROM contact WHERE id=1").fetchone())
    con.close()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "profile": profile,
            "projects": projects,
            "skills": skills,
            "contact": contact,
            "admin": is_admin(request),
        },
    )


@app.get("/admin", response_class=HTMLResponse)
def show_admin(request: Request):
    if not is_admin(request):
        return RedirectResponse("/login", status_code=303)
    con = get_db()
    profile = dict(con.execute("SELECT * FROM profile WHERE id=1").fetchone())
    projects = [dict(r) for r in con.execute("SELECT * FROM projects").fetchall()]
    skills = [dict(r) for r in con.execute("SELECT * FROM skills").fetchall()]
    contact = dict(con.execute("SELECT * FROM contact WHERE id=1").fetchone())
    con.close()
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "profile": profile,
            "projects": projects,
            "skills": skills,
            "contact": contact,
        },
    )


# ── Profile ───────────────────────────────────────────────────────


@app.post("/profile")
def update_profile(
    request: Request,
    name: Annotated[str, Form()],
    titre: Annotated[str, Form()],
    bio: Annotated[str, Form()],
    email: Annotated[str, Form()],
):
    if not is_admin(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not admin"
        )
    con = get_db()
    con.execute(
        "UPDATE profile SET name=?, titre=?, bio=?, email=? WHERE id=1",
        (name, titre, bio, email),
    )
    con.commit()
    con.close()
    return RedirectResponse("/admin", status_code=303)


# ── Contact ───────────────────────────────────────────────────────


@app.post("/contact")
def update_contact(
    request: Request,
    email: Annotated[str, Form()],
    linkedin: Annotated[str, Form()] = None,
    github: Annotated[str, Form()] = None,
    localisation: Annotated[str, Form()] = None,
):
    if not is_admin(request):
        raise HTTPException(status_code=401, detail="Not admin")
    con = get_db()
    con.execute(
        "UPDATE contact SET email=?, linkedin=?, github=?, localisation=? WHERE id=1",
        (email, linkedin, github, localisation),
    )
    con.commit()
    con.close()
    return RedirectResponse("/admin", status_code=303)


# ── Projects ──────────────────────────────────────────────────────


@app.post("/projects")
def create_project(
    request: Request,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    link: Annotated[str, Form()] = None,
):
    if not is_admin(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not admin"
        )
    con = get_db()
    con.execute(
        "INSERT INTO projects (title, description, link) VALUES (?, ?, ?)",
        (title, description, link),
    )
    con.commit()
    con.close()
    return RedirectResponse("/admin", status_code=303)


@app.post("/projects/{project_id}/delete")
def delete_project_form(request: Request, project_id: int):
    if not is_admin(request):
        raise HTTPException(status_code=401, detail="Not admin")
    con = get_db()
    con.execute("DELETE FROM projects WHERE id=?", (project_id,))
    con.commit()
    con.close()
    return RedirectResponse("/admin", status_code=303)


@app.post("/projects/{project_id}/edit")
def edit_project_form(
    request: Request,
    project_id: int,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    link: Annotated[str, Form()] = None,
):
    if not is_admin(request):
        raise HTTPException(status_code=401, detail="Not admin")
    con = get_db()
    con.execute(
        "UPDATE projects SET title=?, description=?, link=? WHERE id=?",
        (title, description, link, project_id),
    )
    con.commit()
    con.close()
    return RedirectResponse("/admin", status_code=303)


# ── Skills ────────────────────────────────────────────────────────


@app.post("/skills")
def create_skill(
    request: Request, name: Annotated[str, Form()], level: Annotated[str, Form()]
):
    if not is_admin(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not admin"
        )
    con = get_db()
    con.execute("INSERT INTO skills (name, level) VALUES (?, ?)", (name, level))
    con.commit()
    con.close()
    return RedirectResponse("/admin", status_code=303)


@app.post("/skills/{skill_id}/delete")
def delete_skill_form(request: Request, skill_id: int):
    if not is_admin(request):
        raise HTTPException(status_code=401, detail="Not admin")
    con = get_db()
    con.execute("DELETE FROM skills WHERE id=?", (skill_id,))
    con.commit()
    con.close()
    return RedirectResponse("/admin", status_code=303)


@app.post("/skills/{skill_id}/edit")
def edit_skill_form(
    request: Request,
    skill_id: int,
    name: Annotated[str, Form()],
    level: Annotated[str, Form()],
):
    if not is_admin(request):
        raise HTTPException(status_code=401, detail="Not admin")
    con = get_db()
    con.execute("UPDATE skills SET name=?, level=? WHERE id=?", (name, level, skill_id))
    con.commit()
    con.close()
    return RedirectResponse("/admin", status_code=303)
