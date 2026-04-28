from typing import Annotated

from fastapi import FastAPI, Request, Form, status, HTTPException, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import secrets
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Mot de passe admin
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Stockage des sessions actives : { token: True }
sessions: dict[str, bool] = {}


def is_admin(request: Request) -> bool:
    """Vérifie si la requête contient un cookie de session valide."""
    token = request.cookies.get("session_token")
    return token in sessions


# Models


class Project(BaseModel):
    title: str
    description: str
    link: str | None = None
    is_featured: bool = False


class Skill(BaseModel):
    name: str
    level: str


class Contact(BaseModel):
    email: str
    linkedin: str | None = None
    github: str


# Data

profile = {
    "name": "Enzo Augie",
    "titre": "Etudiant ingénieur à l'EPF, majeure Data/IA",
    "bio": "Actuellement en 4ème année à l'EPF...",
}

projects: list[dict] = [
    {
        "title": "Portfolio Website",
        "description": "Personal website built with FastAPI",
        "link": "https://example.com",
        "is_featured": True,
    }
]

skills: list[dict] = [
    {"name": "Python", "level": "intermediate"},
]

contact = Contact(
    email="enzo.augie@epfedu.fr",
    linkedin="https://fr.linkedin.com/?mcid=7189711573932810240&src=go-pa&trk=sem-ga_campid.21228777300_asid.161774284317_crid.698137525090_kw.linkedin_d.c_tid.kwd-148086543_n.g_mt.e_geo.9055317&cid=&gclsrc=aw.ds&gad_source=1&gad_campaignid=21228777300&gbraid=0AAAAAojDCNSiTsBQw4PMlkU11qgO3evDy&gclid=CjwKCAjwtcHPBhADEiwAWo3sJm_W4LuUMxK4eZbT6uPwIfaeq-nZnBf0MuUrBc-Ey5LHZv6ds3yluxoCiPAQAvD_BwE",
    github="https://github.com/EnzoAUGIE",
)

templates = Jinja2Templates(directory="templates")


# Login / Logout


@app.get("/login", response_class=HTMLResponse)
def show_login(request: Request, error: int = 0):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": error},
    )


@app.post("/login")
def do_login(
    response: Response,
    password: Annotated[str, Form()],
):
    if password != ADMIN_PASSWORD:
        return RedirectResponse("/login?error=1", status_code=303)

    # Crée un token de session aléatoire et sécurisé
    token = secrets.token_hex(32)
    sessions[token] = True

    redirect = RedirectResponse("/admin", status_code=303)
    redirect.set_cookie(
        key="session_token",
        value=token,
        httponly=True,  # Inaccessible depuis JavaScript
        max_age=3600,  # Expire après 1 heure
    )
    return redirect


@app.get("/logout")
def logout(request: Request):
    token = request.cookies.get("session_token")
    if token in sessions:
        del sessions[token]

    redirect = RedirectResponse("/", status_code=303)
    redirect.delete_cookie("session_token")
    return redirect


# Routes principales


@app.get("/", response_class=HTMLResponse)
def show_portfolio(request: Request):
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


# Profile


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

    profile["name"] = name
    profile["titre"] = titre
    profile["bio"] = bio
    contact.email = email

    return RedirectResponse("/admin", status_code=303)


# Projects


@app.get("/projects/{project_id}")
def read_project(project_id: int):
    if project_id >= len(projects):
        raise HTTPException(status_code=404, detail="Project not found")
    return projects[project_id]


@app.post("/projects")
def create_project(
    request: Request,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    link: Annotated[str, Form()] = None,
    is_featured: Annotated[bool, Form()] = False,
):
    if not is_admin(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not admin"
        )

    projects.append(
        {
            "title": title,
            "description": description,
            "link": link,
            "is_featured": is_featured,
        }
    )

    return RedirectResponse("/admin", status_code=303)


@app.put("/projects/{project_id}")
def update_project(project_id: int, project: Project):
    if project_id >= len(projects):
        raise HTTPException(status_code=404, detail="Project not found")
    projects[project_id].update(project.model_dump())
    return {"project_title": projects[project_id]["title"], "project_id": project_id}


@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    if project_id >= len(projects):
        raise HTTPException(status_code=404, detail="Project not found")
    deleted_project = projects.pop(project_id)
    return {"deleted": deleted_project["title"]}


# Skills


@app.post("/skills")
def create_skill(
    request: Request,
    name: Annotated[str, Form()],
    level: Annotated[str, Form()],
):
    if not is_admin(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not admin"
        )

    skills.append({"name": name, "level": level})
    return RedirectResponse("/admin", status_code=303)


@app.put("/skills/{skill_id}")
def update_skill(skill_id: int, skill: Skill):
    if skill_id >= len(skills):
        raise HTTPException(status_code=404, detail="Skill not found")
    skills[skill_id].update(skill.model_dump())
    return {"skill_name": skills[skill_id]["name"], "skill_id": skill_id}


@app.delete("/skills/{skill_id}")
def delete_skill(skill_id: int):
    if skill_id >= len(skills):
        raise HTTPException(status_code=404, detail="Skill not found")
    deleted_skill = skills.pop(skill_id)
    return {"deleted": deleted_skill["name"]}
