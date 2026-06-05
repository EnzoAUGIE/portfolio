from typing import Annotated
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services.auth_service import is_admin
from services.profile_service import get_profile, update_profile
from services.project_service import get_projects, create_project, update_project, delete_project
from services.skill_service import get_skills, create_skill, update_skill, delete_skill
from services.contact_service import get_contact, update_contact

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def require_admin(request: Request):
    if not is_admin(request):
        raise HTTPException(status_code=401, detail="Not admin")

@router.get("/admin", response_class=HTMLResponse)
def show_admin(request: Request):
    if not is_admin(request):
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(request=request, name="admin.html", context={
        "profile": get_profile(),
        "projects": get_projects(),
        "skills": get_skills(),
        "contact": get_contact(),
    })

# ── Profile ──
@router.post("/profile")
def update_profile_route(request: Request, name: Annotated[str, Form()],
                          titre: Annotated[str, Form()], bio: Annotated[str, Form()],
                          email: Annotated[str, Form()]):
    require_admin(request)
    update_profile(name, titre, bio, email)
    return RedirectResponse("/admin", status_code=303)

# ── Contact ──
@router.post("/contact")
def update_contact_route(request: Request, email: Annotated[str, Form()],
                          linkedin: Annotated[str, Form()] = None,
                          github: Annotated[str, Form()] = None,
                          localisation: Annotated[str, Form()] = None):
    require_admin(request)
    update_contact(email, linkedin, github, localisation)
    return RedirectResponse("/admin", status_code=303)

# ── Projects ──
@router.post("/projects")
def create_project_route(request: Request, title: Annotated[str, Form()],
                          description: Annotated[str, Form()], link: Annotated[str, Form()] = None):
    require_admin(request)
    create_project(title, description, link)
    return RedirectResponse("/admin", status_code=303)

@router.post("/projects/{project_id}/edit")
def edit_project_route(request: Request, project_id: int, title: Annotated[str, Form()],
                        description: Annotated[str, Form()], link: Annotated[str, Form()] = None):
    require_admin(request)
    update_project(project_id, title, description, link)
    return RedirectResponse("/admin", status_code=303)

@router.post("/projects/{project_id}/delete")
def delete_project_route(request: Request, project_id: int):
    require_admin(request)
    delete_project(project_id)
    return RedirectResponse("/admin", status_code=303)

# ── Skills ──
@router.post("/skills")
def create_skill_route(request: Request, name: Annotated[str, Form()], level: Annotated[str, Form()]):
    require_admin(request)
    create_skill(name, level)
    return RedirectResponse("/admin", status_code=303)

@router.post("/skills/{skill_id}/edit")
def edit_skill_route(request: Request, skill_id: int, name: Annotated[str, Form()],
                      level: Annotated[str, Form()]):
    require_admin(request)
    update_skill(skill_id, name, level)
    return RedirectResponse("/admin", status_code=303)

@router.post("/skills/{skill_id}/delete")
def delete_skill_route(request: Request, skill_id: int):
    require_admin(request)
    delete_skill(skill_id)
    return RedirectResponse("/admin", status_code=303)
