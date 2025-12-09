import sqlite3
import csv

db = sqlite3.connect("futurisys.db")
cursor = db.cursor()

# Supprimer l'ancienne table si elle existe
cursor.execute("DROP TABLE IF EXISTS employes;")

# Créer la table avec EXACTEMENT les colonnes du CSV
cursor.execute("""
CREATE TABLE employes (
    employee_id INTEGER,
    age INTEGER,
    revenu_mensuel FLOAT,
    statut_marital TEXT,
    departement TEXT,
    poste TEXT,
    annee_experience_totale INTEGER,
    annees_dans_l_entreprise INTEGER,
    annees_dans_le_poste_actuel INTEGER,
    satisfaction_employee_environnement INTEGER,
    note_evaluation_precedente FLOAT,
    satisfaction_employee_nature_travail INTEGER,
    satisfaction_employee_equipe INTEGER,
    satisfaction_employee_equilibre_pro_perso INTEGER,
    note_evaluation_actuelle FLOAT,
    heure_supplementaires TEXT,
    augementation_salaire_precedente FLOAT,
    nombre_participation_pee INTEGER,
    frequence_deplacement TEXT,
    annes_sous_responsable_actuel INTEGER
);
""")

# Charger le CSV
with open("employes.csv", newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = [(
        row["employee_id"],
        row["age"],
        row["revenu_mensuel"],
        row["statut_marital"],
        row["departement"],
        row["poste"],
        row["annee_experience_totale"],
        row["annees_dans_l_entreprise"],
        row["annees_dans_le_poste_actuel"],
        row["satisfaction_employee_environnement"],
        row["note_evaluation_precedente"],
        row["satisfaction_employee_nature_travail"],
        row["satisfaction_employee_equipe"],
        row["satisfaction_employee_equilibre_pro_perso"],
        row["note_evaluation_actuelle"],
        row["heure_supplementaires"],
        row["augementation_salaire_precedente"],
        row["nombre_participation_pee"],
        row["frequence_deplacement"],
        row["annes_sous_responsable_actuel"]
    ) for row in reader]

# Insérer les données
cursor.executemany("""
INSERT INTO employes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
""", rows)

db.commit()
db.close()

print("🎉 Import terminé à 100 % avec 20 colonnes !")
