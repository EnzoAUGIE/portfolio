import os
from typing import Annotated
from fastapi import APIRouter, Form, Response, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from services.auth_service import create_session, delete_session, is_admin

router = APIRouter()
templates = Jinja2Templates(directory="templates")
from dotenv import load_dotenv

load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


@router.get("/login")
def show_login(request: Request, error: int = 0):
    return templates.TemplateResponse(
        request=request, name="login.html", context={"error": error}
    )


@router.post("/login")
def do_login(response: Response, password: Annotated[str, Form()]):
    if password != ADMIN_PASSWORD:
        return RedirectResponse("/login?error=1", status_code=303)
    token = create_session()
    redirect = RedirectResponse("/admin", status_code=303)
    redirect.set_cookie(key="session_token", value=token, httponly=True, max_age=3600)
    return redirect


@router.get("/logout")
def logout(request: Request):
    token = request.cookies.get("session_token")
    delete_session(token)
    redirect = RedirectResponse("/", status_code=303)
    redirect.delete_cookie("session_token")
    return redirect
