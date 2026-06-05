# Point d'entrée de l'application
# Ce fichier est exécuté en premier quand on lance uvicorn main:app
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database.init_db import init_db
from routers import auth, portfolio, admin

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Création de l'instance FastAPI
# Montage du dossier static pour servir les fichiers CSS
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialisation de la base de données au démarrage
# Crée les tables si elles n'existent pas encore
init_db()

# Enregistrement des routers dans l'application
# Chaque router gère un groupe de routes spécifiques
app.include_router(auth.router)  # Routes d'authentification
app.include_router(portfolio.router)  # Routes des pages publiques
app.include_router(admin.router)  # Routes d'administration (protégées)
