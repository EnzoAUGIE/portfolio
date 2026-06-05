import os
from dotenv import load_dotenv
from fastapi import FastAPI
from database.init_db import init_db
from routers import auth, portfolio, admin

load_dotenv()

app = FastAPI()

# Initialisation de la base de données
init_db()

# Enregistrement des routers
app.include_router(auth.router)
app.include_router(portfolio.router)
app.include_router(admin.router)
