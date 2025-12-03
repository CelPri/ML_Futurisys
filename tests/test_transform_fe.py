import pandas as pd
from app.feature_engineering import transform_fe

def test_transform_fe():
    df = pd.DataFrame([{
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
        "augementation_salaire_precedente": "10%",
        "nombre_participation_pee": 1,
        "frequence_deplacement": "Rare",
        "annes_sous_responsable_actuel": 1
    }])

    out = transform_fe(df)

    # 1. La fonction renvoie bien un DataFrame
    assert isinstance(out, pd.DataFrame)

    # 2. Vérifier que les colonnes calculées existent
    assert "revenu_par_anciennete" in out.columns
    assert "ratio_exp_entreprise_externe" in out.columns
    assert "ratio_manager" in out.columns

    # 3. Vérifier que Oui -> 1
    assert out.loc[0, "heure_supplementaires"] == 1

    # 4. Vérifier que "10%" devient 10.0
    assert out.loc[0, "augementation_salaire_precedente"] == 10.0
