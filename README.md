---
title: Futurisys API
emoji: 🚀
sdk: docker
pinned: false
---

# Futurisys - Déploiement d'un modèle de Machine Learning

## Sommaire

- [À propos](#à-propos)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Tests](#tests)
- [Déploiement](#déploiement)
- [Structure du projet](#structure-du-projet)
- [Technologies utilisées](#technologies-utilisées)
- [Contribution](#contribution)
- [Licence](#licence)

## À propos

L'entreprise Futurisys souhaite rendre ses modèles de machine learning opérationnels et accessibles via une API performante. L'objectif est de déployer un modèle prédictif issu du projet "Anticiper les départs potentiels d'employés". Cette API utilise FastAPI pour fournir des prédictions sur le départ potentiel des employés en se basant sur diverses caractéristiques.


## Prérequis

- Python 3.13
- uv (gestionnaire de paquets moderne pour Python)
- Git
- Docker (pour le déploiement en conteneur)

## Installation

### Cloner le dépôt

git clone https://CelPri/ML_Futurisys.git
cd ML_Futurisys


### Installer les dépendances

uv sync

## Utilisation

### Lancer l'API localement

uvicorn app.main:app --reload

API disponible sur :

    Dev : http://127.0.0.1:8000
    Prod : https://pcelia-futurisys-api.hf.space/docs
    → Swagger : http://127.0.0.1:8000/docs


### Endpoints principaux

- **GET /** : Message de bienvenue et lien vers la documentation.
- **GET /threshold** : Retourne le seuil de décision du modèle.
- **POST /predict** : Effectue une prédiction à partir de données brutes.
  - Corps de la requête : Objet JSON avec les caractéristiques de l'employé.
- **POST /predict_from_db_employe** : Effectue une prédiction pour un employé existant dans la DB.
  - Paramètre : `employee_id` (query parameter).
- **Docs** : Documentation Swagger
### Exemple de requête

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "age": 35,
       "revenu_mensuel": 5000.0,
       "statut_marital": "Marié",
       "departement": "IT",
       "poste": "Développeur",
       "annee_experience_totale": 10,
       "annees_dans_l_entreprise": 5,
       "annees_dans_le_poste_actuel": 3,
       "satisfaction_employee_environnement": 4,
       "note_evaluation_precedente": 3.5,
       "satisfaction_employee_nature_travail": 4,
       "satisfaction_employee_equipe": 4,
       "satisfaction_employee_equilibre_pro_perso": 3,
       "note_evaluation_actuelle": 4.0,
       "heure_supplementaires": "Non",
       "augementation_salaire_precedente": 0.05,
       "nombre_participation_pee": 2,
       "frequence_deplacement": "Rarement",
       "annes_sous_responsable_actuel": 2
     }'
```

## Tests

Exécuter les tests unitaires :

pytest

Pour la couverture :

pytest --cov=app


## Déploiement

### Avec Docker

Construire l'image :

```bash
docker build -t ml-futurisys .
```

Lancer le conteneur :

```bash
docker run -p 7860:7860 ml-futurisys
```

L'API sera accessible sur `http://localhost:7860`.


## Structure du projet

- `app/` : Code de l'application
  - `main.py` : Application FastAPI principale
  - `database.py` : Configuration de la base de données
  - `models.py` : Modèles de données SQLAlchemy
  - `feature_engineering.py` : Fonctions d'ingénierie des caractéristiques
- `model/` : Modèle entraîné (model_Futurisys.joblib)
- `data/` : Fichiers de données d'exemple
- `tests/` : Scripts de tests unitaires
- `docs/` : Documentation et supports de présentation
- `Dockerfile` : Configuration Docker
- `pyproject.toml` : Configuration du projet Python
- `requirements.txt` : Dépendances Python
- `import_csv_to_sqlite.py` : Script d'import des données CSV vers SQLite

## Technologies utilisées

- **FastAPI** : Framework web pour l'API
- **scikit-learn** : Bibliothèque de machine learning
- **SQLAlchemy** : ORM pour la base de données
- **Pydantic** : Validation des données
- **joblib** : Sérialisation du modèle
- **uvicorn** : Serveur ASGI
- **Docker** : Conteneurisation

## Contribution

Les contributions sont les bienvenues ! Veuillez créer une issue ou une pull request pour toute amélioration.

## Licence

Ce projet est sous licence MIT.

