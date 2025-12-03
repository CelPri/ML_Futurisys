import pandas as pd


def transform_fe(df):
    df = df.copy()

    df["heure_supplementaires"] = df["heure_supplementaires"].replace({"Oui":1, "Non":0})

    # Convertir en string si c'est un nombre
    df["augementation_salaire_precedente"] = df["augementation_salaire_precedente"].astype(str)
    # Retirer le % si présent
    df["augementation_salaire_precedente"] = (
    df["augementation_salaire_precedente"].str.replace("%", "").astype(float)
)


    df["revenu_par_anciennete"] = df["revenu_mensuel"] / (df["annee_experience_totale"] + 1)
    df["ratio_exp_entreprise_externe"] = df["annees_dans_l_entreprise"] / (df["annee_experience_totale"] + 1)
    df["ratio_manager"] = df["annes_sous_responsable_actuel"] / (df["annees_dans_l_entreprise"] + 1)



    return df