# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
import pandas as pd
from joblib import load
from app.database import Base, engine, SessionLocal
from app.models import Input, Output
import datetime
from app.feature_engineering import transform_fe


# Création automatique des tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Chargement du modèle
bundle = load("app/model/model_Futurisys.joblib")
pipeline = bundle["model"]
threshold = bundle["threshold"]  # 0.31



# Définition du schéma d'entrée

class PredictionRawData(BaseModel):
    age: int
    revenu_mensuel: float
    statut_marital: str
    departement: str
    poste: str

    annee_experience_totale: int
    annees_dans_l_entreprise: int
    annees_dans_le_poste_actuel: int

    satisfaction_employee_environnement: int
    note_evaluation_precedente: float
    satisfaction_employee_nature_travail: int
    satisfaction_employee_equipe: int
    satisfaction_employee_equilibre_pro_perso: int
    note_evaluation_actuelle: float

    heure_supplementaires: Literal["Oui", "Non"]
    augementation_salaire_precedente: float
    nombre_participation_pee: int
    frequence_deplacement: str

    annes_sous_responsable_actuel: int


# Création de l'application

app = FastAPI(title="API Futurisys")

@app.get("/")
def read_root():
    return {
        "message": "Bienvenue dans l'API Futurisys",
        "info": "Accedez au Swagger : https://huggingface.co/spaces/PCelia/futurisys-api"
        
    }

@app.get("/threshold")
def read_threshold():
    return {"threshold": threshold}



# Endpoint de prédiction

@app.post("/predict")
def predict(data: PredictionRawData):

    # Convertir en DataFrame
    df = pd.DataFrame([data.dict()])
    df = transform_fe(df)

    # Prédiction
    proba = pipeline.predict_proba(df)[0][1]
    pred = bool(proba >= threshold)

    # --- Enregistrement dans la DB ---
    db = SessionLocal()

    # 1) Input

    new_input = Input(
    timestamp_input=datetime.datetime.now(),
    employee_id=data.dict().get("employee_id", None),
    age=data.age )

    db.add(new_input)
    db.commit()
    db.refresh(new_input)

    # 2) Output
    new_output = Output(
        id_input = new_input.id_input,
        prediction = int(pred),
        probability = float(proba)
    )
    db.add(new_output)
    db.commit()
    # --- FIN enregistrement ---

    return {
        "probabilité": round(float(proba), 3),
        "prédiction": pred
    }

