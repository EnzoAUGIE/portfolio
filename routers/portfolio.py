# Tier 1 — Présentation
# Ce fichier gère les routes des pages publiques :
# page d'accueil et affichage des portfolios
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services.auth_service import get_all_users, get_current_user_id
from services.profile_service import get_profile
from services.project_service import get_projects
from services.skill_service import get_skills
from services.contact_service import get_contact
from database.db import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def show_home(request: Request):
    users = get_all_users()
    portfolios = []
    for user in users:
        profile = get_profile(user["id"])
        portfolios.append(
            {
                "username": user["username"],
                "name": profile.get("name", user["username"]),
                "titre": profile.get("titre", ""),
            }
        )
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "portfolios": portfolios,
            "logged_in": get_current_user_id(request) is not None,
        },
    )


@router.get("/portfolio/{username}", response_class=HTMLResponse)
def show_portfolio(username: str, request: Request):
    con = get_db()
    row = con.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
    con.close()
    if not row:
        return RedirectResponse("/", status_code=303)
    user_id = row["id"]
    current_user_id = get_current_user_id(request)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "profile": get_profile(user_id),
            "projects": get_projects(user_id),
            "skills": get_skills(user_id),
            "contact": get_contact(user_id),
            "is_owner": current_user_id == user_id,
            "username": username,
        },
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user_id = get_current_user_id(request)
    if not user_id:
        return RedirectResponse("/login", status_code=303)
    con = get_db()
    row = con.execute("SELECT username FROM users WHERE id=?", (user_id,)).fetchone()
    con.close()
    return RedirectResponse(f"/portfolio/{row['username']}", status_code=303)
