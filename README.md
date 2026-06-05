# Portfolio Generator

Portfolio Generator est une application web permettant à n'importe quel utilisateur de créer, personnaliser et publier son propre portfolio en ligne. Développée avec FastAPI et Jinja2, elle repose sur une architecture 3-tiers claire et une base de données SQLite pour la persistance des données.

## Démonstration en ligne

L'application est accessible à l'adresse suivante :
https://portfolio-21ax.onrender.com

## Fonctionnalités

### Côté utilisateur
- Création d'un compte avec nom d'utilisateur et mot de passe
- Connexion et déconnexion sécurisées via cookie de session
- Portfolio accessible publiquement via une URL personnalisée : `/portfolio/{username}`
- Panneau d'administration personnel permettant de :
  - Modifier son profil (nom complet, titre, biographie)
  - Gérer ses compétences (ajout, modification, suppression)
  - Gérer ses projets (ajout, modification, suppression, lien vers le projet)
  - Renseigner ses informations de contact (email, LinkedIn, GitHub, localisation)

### Côté application
- Page d'accueil listant tous les portfolios publiés
- Deux rôles utilisateurs : visiteur (lecture seule) et utilisateur connecté (modification de son portfolio)
- Chaque utilisateur ne peut modifier que son propre portfolio
- Les données sont persistées dans une base de données SQLite
- L'application se redéploie automatiquement à chaque push sur GitHub via Render

---

## Versions

| Version | Date | Description |
|---|---|---|
| v0.1.0 | Avril 2026 | Portfolio personnel avec authentification admin |
| v0.2.0 | Juin 2026 | Ajout persistance SQLite, modification et suppression des données |
| v1.0.0 | Juin 2026 | Générateur multi-utilisateurs, architecture 3-tiers, déploiement Render |
| v1.0.1 | Juin 2026 | Renommage des services, commentaires dans le code |

Le détail de chaque version est disponible dans le fichier [CHANGELOG.md](./CHANGELOG.md).

---

## Architecture 3-tiers

L'application est structurée selon une architecture 3-tiers qui sépare clairement les responsabilités :

### Tier 1 — Présentation (routers/)
Ce niveau gère la réception des requêtes HTTP et le retour des réponses (pages HTML ou redirections). Il ne contient aucune logique métier.

- `routers/auth.py` : gestion des routes d'inscription, connexion et déconnexion
- `routers/portfolio.py` : affichage de la page d'accueil et des portfolios publics
- `routers/admin.py` : gestion du panneau d'administration de chaque utilisateur

### Tier 2 — Logique métier (services/)
Ce niveau contient toutes les règles et opérations de l'application. Il fait le lien entre les routers et la base de données, sans jamais interagir directement avec les requêtes HTTP.

- `services/auth.py` : création de compte, vérification des identifiants, gestion des sessions
- `services/profile.py` : lecture et mise à jour du profil utilisateur
- `services/project.py` : création, modification et suppression de projets
- `services/skill.py` : création, modification et suppression de compétences
- `services/contact.py` : lecture et mise à jour des informations de contact

### Tier 3 — Données (database/)
Ce niveau gère uniquement la connexion à la base de données et l'initialisation des tables. Il ne connaît ni les routes ni la logique métier.

- `database/db.py` : connexion SQLite
- `database/init_db.py` : création des tables au démarrage de l'application

---

## Structure du projet

```
portfolio/
├── main.py
├── requirements.txt
├── start.sh
├── CHANGELOG.md
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── portfolio.py
│   └── admin.py
├── services/
│   ├── __init__.py
│   ├── auth.py
│   ├── profile.py
│   ├── project.py
│   ├── skill.py
│   └── contact.py
├── database/
│   ├── __init__.py
│   ├── db.py
│   └── init_db.py
├── templates/
│   ├── home.html
│   ├── index.html
│   ├── admin.html
│   ├── login.html
│   └── register.html
└── static/
    └── style.css
```

---

## Rôles utilisateurs

| Rôle | Accès |
|---|---|
| Visiteur (non connecté) | Consultation de tous les portfolios publics |
| Utilisateur connecté | Modification de son propre portfolio uniquement |

La séparation des rôles est garantie par le champ `user_id` présent dans toutes les requêtes SQL de modification. Un utilisateur connecté ne peut jamais accéder ni modifier les données d'un autre utilisateur.

---

## Schéma de la base de données

```
users        → id, username, password (hashé SHA-256)
profile      → id, user_id, name, titre, bio, email
projects     → id, user_id, title, description, link
skills       → id, user_id, name, level
contact      → id, user_id, email, linkedin, github, localisation
```

---

## Endpoints de l'application

| Méthode | Route | Accès | Description |
|---|---|---|---|
| GET | `/` | Public | Page d'accueil avec la liste des portfolios |
| GET | `/register` | Public | Formulaire d'inscription |
| POST | `/register` | Public | Création d'un compte |
| GET | `/login` | Public | Formulaire de connexion |
| POST | `/login` | Public | Authentification |
| GET | `/logout` | Connecté | Déconnexion |
| GET | `/portfolio/{username}` | Public | Portfolio public d'un utilisateur |
| GET | `/dashboard` | Connecté | Redirige vers son propre portfolio |
| GET | `/admin` | Connecté | Panneau d'administration |
| POST | `/profile` | Connecté | Modifier son profil |
| POST | `/contact` | Connecté | Modifier ses infos de contact |
| POST | `/skills` | Connecté | Ajouter une compétence |
| POST | `/skills/{id}/edit` | Connecté | Modifier une compétence |
| POST | `/skills/{id}/delete` | Connecté | Supprimer une compétence |
| POST | `/projects` | Connecté | Ajouter un projet |
| POST | `/projects/{id}/edit` | Connecté | Modifier un projet |
| POST | `/projects/{id}/delete` | Connecté | Supprimer un projet |

---

## Technologies utilisées

| Technologie | Rôle |
|---|---|
| Python 3.11 | Langage principal |
| FastAPI | Framework web backend |
| Jinja2 | Moteur de templates HTML |
| SQLite | Base de données locale |
| Simple.css | Framework CSS minimaliste |
| Uvicorn | Serveur ASGI |
| python-dotenv | Gestion des variables d'environnement |
| Git / GitHub | Versioning et collaboration |
| Render | Hébergement et déploiement continu |

---

## Installation et lancement en local

### Prérequis
- Python 3.11 ou supérieur
- Git

### Étapes

**1. Cloner le repository**
```bash
git clone https://github.com/EnzoAUGIE/portfolio.git
cd portfolio
```

**2. Créer et activer un environnement virtuel**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Installer les dépendances**
```bash
pip install -r requirements.txt
```

**4. Créer le fichier .env**
```bash
echo "ADMIN_PASSWORD=votre_mot_de_passe" > .env
```

**5. Lancer l'application**
```bash
uvicorn main:app --reload
```

L'application est accessible sur http://127.0.0.1:8000

---

## Déploiement sur Render

L'application est déployée sur Render avec déploiement continu :

1. Créer un compte sur render.com et connecter son compte GitHub
2. Créer un nouveau Web Service en sélectionnant le repository
3. Choisir la branche `main`
4. Renseigner les paramètres :
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Ajouter la variable d'environnement `ADMIN_PASSWORD`

Render redéploie automatiquement l'application à chaque push sur `main`.

---

## Versioning

Le projet suit la convention Semantic Versioning (SemVer) :

- `v0.1.0` : Portfolio personnel initial
- `v0.2.0` : Ajout de la persistance SQLite
- `v1.0.0` : Générateur multi-utilisateurs avec architecture 3-tiers
- `v1.0.1` : Renommage des services et documentation

Stratégie de branches :
- `main` : version stable déployée en production
- `feature/*` : branches de développement des nouvelles fonctionnalités

---

## Auteurs

- **Enzo Augie** — Etudiant ingénieur à l'EPF, majeure Data/IA — [GitHub](https://github.com/EnzoAUGIE)
- **Etienne Girard** — Etudiant ingénieur à l'EPF — [GitHub](https://github.com/etienneg92i)
