from fastapi.testclient import TestClient
from app.main import app
from app.main import get_db


client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Bienvenue dans l'API Futurisys"
    assert data["documentation"] == "/docs"

def test_threshold_endpoint():
    response = client.get("/threshold")
    assert response.status_code == 200

    data = response.json()
    assert "threshold" in data
    assert isinstance(data["threshold"], float)

def test_predict_valid():
    payload = {
        "age": 30,
        "revenu_mensuel": 2500.0,
        "statut_marital": "Marié(e)",
        "departement": "IT",
        "poste": "Développeur",
        "annee_experience_totale": 5,
        "annees_dans_l_entreprise": 2,
        "annees_dans_le_poste_actuel": 2,
        "satisfaction_employee_environnement": 3,
        "note_evaluation_precedente": 4.2,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 4,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "note_evaluation_actuelle": 4.5,
        "heure_supplementaires": "Oui",
        "augementation_salaire_precedente": 2.0,
        "nombre_participation_pee": 1,
        "frequence_deplacement": "Rare",
        "annes_sous_responsable_actuel": 1
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "probabilité" in data
    assert "prédiction" in data
    assert isinstance(data["probabilité"], float)
    assert isinstance(data["prédiction"], bool)

def test_predict_invalid_type_age():
    payload = {
        "age": "abc",  # type incorrect
        "revenu_mensuel": 2500.0,
        "statut_marital": "Marié(e)",
        "departement": "IT",
        "poste": "Développeur",
        "annee_experience_totale": 5,
        "annees_dans_l_entreprise": 2,
        "annees_dans_le_poste_actuel": 2,
        "satisfaction_employee_environnement": 3,
        "note_evaluation_precedente": 4.2,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 4,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "note_evaluation_actuelle": 4.5,
        "heure_supplementaires": "Oui",
        "augementation_salaire_precedente": 2.0,
        "nombre_participation_pee": 1,
        "frequence_deplacement": "Rare",
        "annes_sous_responsable_actuel": 1
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_predict_missing_field():
    payload = {
        "age": 30,
        # "revenu_mensuel" est manquant volontairement
        "statut_marital": "Marié(e)",
        "departement": "IT",
        "poste": "Développeur",
        "annee_experience_totale": 5,
        "annees_dans_l_entreprise": 2,
        "annees_dans_le_poste_actuel": 2,
        "satisfaction_employee_environnement": 3,
        "note_evaluation_precedente": 4.2,
        "satisfaction_employee_nature_travail": 4,
        "satisfaction_employee_equipe": 4,
        "satisfaction_employee_equilibre_pro_perso": 3,
        "note_evaluation_actuelle": 4.5,
        "heure_supplementaires": "Oui",
        "augementation_salaire_precedente": 2.0,
        "nombre_participation_pee": 1,
        "frequence_deplacement": "Rare",
        "annes_sous_responsable_actuel": 1
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_predict_from_db_employe_not_found():
    response = client.post("/predict_from_db_employe?employee_id=999999")
    assert response.status_code == 200
    assert "Aucun employé trouvé" in response.json()["message"]

from app.database import SessionLocal
from app.models import Employe

def test_predict_from_db_employe_found():
    # 1. Créer un employé dans la base
    db = SessionLocal()
    employe = Employe(
        employee_id=999,
        age=30,
        revenu_mensuel=2500.0,
        statut_marital="Marié(e)",
        departement="IT",
        poste="Développeur",
        annee_experience_totale=5,
        annees_dans_l_entreprise=2,
        annees_dans_le_poste_actuel=2,
        satisfaction_employee_environnement=3,
        note_evaluation_precedente=4.2,
        satisfaction_employee_nature_travail=4,
        satisfaction_employee_equipe=4,
        satisfaction_employee_equilibre_pro_perso=3,
        note_evaluation_actuelle=4.5,
        heure_supplementaires="Oui",
        augementation_salaire_precedente=2.0,
        nombre_participation_pee=1,
        frequence_deplacement="Rare",
        annes_sous_responsable_actuel=1
    )
    db.add(employe)
    db.commit()

    # 2. Appeler l'endpoint
    response = client.post("/predict_from_db_employe?employee_id=999")

    # 3. Assertions
    assert response.status_code == 200
    res = response.json()
    assert "probabilité" in res
    assert "prédiction" in res
    assert isinstance(res["probabilité"], float)
    assert isinstance(res["prédiction"], bool)


def test_get_db():
    gen = get_db()          # on récupère le générateur
    db = next(gen)          # exécute "db = SessionLocal()" et "yield db"
    assert db is not None   # couvre la partie try / yield
    try:
        next(gen)           # va provoquer StopIteration
    except StopIteration:
        pass                # couvre le finally: db.close()

