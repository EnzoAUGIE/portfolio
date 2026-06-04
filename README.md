# Portfolio Web — Enzo Augie

Portfolio personnel développé avec **FastAPI** et **Jinja2**, avec un panneau d'administration pour gérer le contenu dynamiquement.

## Fonctionnalités

- Page portfolio publique (profil, skills, projets, contact)
- Authentification admin par mot de passe
-️ Panneau admin pour :
  - Modifier le profil et les infos de contact
  - Ajouter, modifier et supprimer des skills
  - Ajouter, modifier et supprimer des projets
- Persistance des données via **SQLite**

##️ Technologies

- [FastAPI](https://fastapi.tiangolo.com/) — Backend Python
- [Jinja2](https://jinja.palletsprojects.com/) — Templates HTML
- [SQLite](https://www.sqlite.org/) — Base de données locale
- [Simple.css](https://simplecss.org/) — Style CSS minimaliste

## Lancer le projet

### 1. Cloner le repo

```bash
git clone https://github.com/EnzoAUGIE/portfolio.git
cd portfolio
```

### 2. Créer un environnement virtuel et installer les dépendances

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn jinja2 python-dotenv
```

### 3. Configurer le mot de passe admin

Crée un fichier `.env` à la racine :

```
ADMIN_PASSWORD=ton_mot_de_passe
```

### 4. Lancer l'application

```bash
uvicorn main:app --reload
```

Puis ouvre [http://127.0.0.1:8000](http://127.0.0.1:8000) dans ton navigateur.

## Structure du projet

```
portfolio/
├── main.py          # Backend FastAPI
├── templates/
│   ├── index.html   # Page portfolio publique
│   ├── admin.html   # Panneau d'administration
│   └── login.html   # Page de connexion
├── .env             # Mot de passe admin (non commité)
├── .gitignore
└── README.md
```

## 👤 Auteur

**Enzo Augie** — Étudiant ingénieur à l'EPF, majeure Data/IA  
[GitHub](https://github.com/EnzoAUGIE) · [LinkedIn](https://fr.linkedin.com/in/enzo-augie)
