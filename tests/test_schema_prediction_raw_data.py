from pydantic import ValidationError
from app.main import PredictionRawData

def test_schema_accepts_valid_age():
    data = {
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

    obj = PredictionRawData(**data)
    assert obj.age == 30

def test_schema_rejects_invalid_age():
    # on met une valeur FAUSSE juste pour tester l'erreur
    data = {
        "age": "pas_un_nombre"
    }

    try:
        PredictionRawData(**data)
        assert False  # si ça ne plante pas, c'est mauvais
    except ValidationError:
        assert True   # si ça plante comme prévu, c'est bon
