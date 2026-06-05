from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database.init_db import init_db
from routers import auth, portfolio, admin

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

init_db()

app.include_router(auth.router)
app.include_router(portfolio.router)
app.include_router(admin.router)
