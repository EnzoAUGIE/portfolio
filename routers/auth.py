# Tier 1 — Présentation
# Ce fichier gère les routes d'authentification :
# inscription, connexion et déconnexion
from typing import Annotated
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services.auth import create_user, login_user, logout_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
def show_register(request: Request, error: int = 0):
    return templates.TemplateResponse(
        request=request, name="register.html", context={"error": error}
    )


@router.post("/register")
def do_register(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    success = create_user(username, password)
    if not success:
        return RedirectResponse("/register?error=1", status_code=303)
    return RedirectResponse("/login", status_code=303)


@router.get("/login", response_class=HTMLResponse)
def show_login(request: Request, error: int = 0):
    return templates.TemplateResponse(
        request=request, name="login.html", context={"error": error}
    )


@router.post("/login")
def do_login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    token = login_user(username, password)
    if not token:
        return RedirectResponse("/login?error=1", status_code=303)
    redirect = RedirectResponse("/dashboard", status_code=303)
    redirect.set_cookie(key="session_token", value=token, httponly=True, max_age=3600)
    return redirect


@router.get("/logout")
def logout(request: Request):
    token = request.cookies.get("session_token")
    logout_user(token)
    redirect = RedirectResponse("/", status_code=303)
    redirect.delete_cookie("session_token")
    return redirect
