# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

---

## [v1.0.1] - 2026-06-05

### Modifications
- Renommage des fichiers services (suppression du suffixe _service)
  - `auth_service.py` → `auth.py`
  - `profile_service.py` → `profile.py`
  - `project_service.py` → `project.py`
  - `skill_service.py` → `skill.py`
  - `contact_service.py` → `contact.py`
- Ajout de commentaires dans tous les scripts Python
- Mise à jour du README avec versioning et rôles utilisateurs

---

## [v1.0.0] - 2026-06-05

### Ajouts majeurs
- Transformation en générateur de e-portfolio multi-utilisateurs
- Système d'inscription et de connexion par nom d'utilisateur
- Chaque utilisateur possède son propre portfolio accessible via `/portfolio/{username}`
- Page d'accueil publique listant tous les portfolios créés
- Restructuration complète en architecture 3-tiers (routers, services, database)
- Déploiement sur Render : https://portfolio-21ax.onrender.com
- Intégration du CSS personnalisé développé par Etienne Girard
- Documentation technique complète (README, fiche projet, commentaires dans le code)

### Modifications
- La base de données SQLite lie désormais chaque donnée à un utilisateur via `user_id`
- Le système d'authentification utilise désormais des comptes utilisateurs au lieu d'un mot de passe global
- Les sessions sont gérées par token aléatoire stocké en cookie httponly

### Sécurité
- Hashage des mots de passe en SHA-256
- Isolation des données par `user_id` dans toutes les requêtes SQL
- Cookie de session httponly avec expiration après 1 heure

---

## [v0.2.0] - 2026-06-05

### Ajouts
- Persistance des données via base de données SQLite
- Tables : profile, projects, skills, contact
- Modification et suppression des skills et projets depuis le panneau admin
- Section contact sur la page portfolio publique (email, LinkedIn, GitHub, localisation)

### Modifications
- Les données ne sont plus stockées en mémoire mais en base de données
- Le panneau admin permet désormais de modifier et supprimer chaque entrée

---

## [v0.1.0] - 2026-04-05

### Version initiale
- Portfolio personnel d'Enzo Augie développé avec FastAPI et Jinja2
- Page portfolio publique avec profil, skills et projets
- Authentification admin par mot de passe unique
- Panneau d'administration pour modifier le profil, ajouter des skills et des projets
- Déploiement du code sur GitHub
