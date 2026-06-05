from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.auth_service import is_admin
from services.profile_service import get_profile
from services.project_service import get_projects
from services.skill_service import get_skills
from services.contact_service import get_contact

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def show_portfolio(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={
        "profile": get_profile(),
        "projects": get_projects(),
        "skills": get_skills(),
        "contact": get_contact(),
        "admin": is_admin(request),
    })
