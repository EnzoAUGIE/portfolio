# Tier 1 — Présentation
# Ce fichier gère toutes les routes du panneau d'administration
# Chaque utilisateur connecté peut modifier uniquement ses propres données
from typing import Annotated
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services.auth_service import get_current_user_id
from services.profile_service import get_profile, update_profile
from services.project_service import (
    get_projects,
    create_project,
    update_project,
    delete_project,
)
from services.skill_service import get_skills, create_skill, update_skill, delete_skill
from services.contact_service import get_contact, update_contact
from database.db import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def require_user(request: Request) -> int:
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="Non connecté")
    return user_id


@router.get("/admin", response_class=HTMLResponse)
def show_admin(request: Request):
    user_id = get_current_user_id(request)
    if not user_id:
        return RedirectResponse("/login", status_code=303)
    con = get_db()
    row = con.execute("SELECT username FROM users WHERE id=?", (user_id,)).fetchone()
    con.close()
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "profile": get_profile(user_id),
            "projects": get_projects(user_id),
            "skills": get_skills(user_id),
            "contact": get_contact(user_id),
            "username": row["username"],
        },
    )


@router.post("/profile")
def update_profile_route(
    request: Request,
    name: Annotated[str, Form()] = "",
    titre: Annotated[str, Form()] = "",
    bio: Annotated[str, Form()] = "",
):
    user_id = require_user(request)
    update_profile(user_id, name, titre, bio, "")
    return RedirectResponse("/admin", status_code=303)


@router.post("/contact")
def update_contact_route(
    request: Request,
    email: Annotated[str, Form()] = "",
    linkedin: Annotated[str, Form()] = None,
    github: Annotated[str, Form()] = None,
    localisation: Annotated[str, Form()] = None,
):
    user_id = require_user(request)
    update_contact(user_id, email, linkedin, github, localisation)
    return RedirectResponse("/admin", status_code=303)


@router.post("/projects")
def create_project_route(
    request: Request,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    link: Annotated[str, Form()] = None,
):
    user_id = require_user(request)
    create_project(user_id, title, description, link)
    return RedirectResponse("/admin", status_code=303)


@router.post("/projects/{project_id}/edit")
def edit_project_route(
    request: Request,
    project_id: int,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    link: Annotated[str, Form()] = None,
):
    user_id = require_user(request)
    update_project(project_id, user_id, title, description, link)
    return RedirectResponse("/admin", status_code=303)


@router.post("/projects/{project_id}/delete")
def delete_project_route(request: Request, project_id: int):
    user_id = require_user(request)
    delete_project(project_id, user_id)
    return RedirectResponse("/admin", status_code=303)


@router.post("/skills")
def create_skill_route(
    request: Request, name: Annotated[str, Form()], level: Annotated[str, Form()]
):
    user_id = require_user(request)
    create_skill(user_id, name, level)
    return RedirectResponse("/admin", status_code=303)


@router.post("/skills/{skill_id}/edit")
def edit_skill_route(
    request: Request,
    skill_id: int,
    name: Annotated[str, Form()],
    level: Annotated[str, Form()],
):
    user_id = require_user(request)
    update_skill(skill_id, user_id, name, level)
    return RedirectResponse("/admin", status_code=303)


@router.post("/skills/{skill_id}/delete")
def delete_skill_route(request: Request, skill_id: int):
    user_id = require_user(request)
    delete_skill(skill_id, user_id)
    return RedirectResponse("/admin", status_code=303)
