# app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
import pandas as pd
from joblib import load
from app.database import Base, engine, SessionLocal
from app.models import Input, Output, Employe
import datetime
from app.feature_engineering import transform_fe
from fastapi import Query

from app.database import DATABASE_URL


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
        "documentation": "/docs",
        "info": "Accedez au Swagger : https://pcelia-futurisys-api.hf.space/docs"
        
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

    # Enregistrement dans la DB 
    db = SessionLocal()

    # Input

    new_input = Input(
    timestamp_input=datetime.datetime.now(),
    employee_id=data.dict().get("employee_id", None),
    age=data.age )

    db.add(new_input)
    db.commit()
    db.refresh(new_input)

    # Output
    new_output = Output(
        id_input = new_input.id_input,
        prediction = int(pred),
        probabilite = float(proba)

    )
    db.add(new_output)
    db.commit()
    #  FIN enregistrement 

    return {
        "probabilité": round(float(proba), 3),
        "prédiction": pred
    }
from sqlalchemy import text

@app.get("/test_ids")
def test_ids():
    db = SessionLocal()
    from sqlalchemy import text
    result = db.execute(text("SELECT employee_id FROM employes LIMIT 20;")).fetchall()
    return {"ids": result}



import traceback


@app.post("/predict_from_db_employe")
def predict_from_db_employe(
    employee_id: int = Query(..., ge=1)
):
    try:
        db = SessionLocal()

        employe = db.query(Employe).filter(Employe.employee_id == employee_id).first()
        if not employe:
            return {"message": f"Aucun employé trouvé avec l'id {employee_id}"}

        data = employe.__dict__.copy()
        data.pop("_sa_instance_state", None)

        df = pd.DataFrame([data])
        df = transform_fe(df)

        proba = pipeline.predict_proba(df)[0][1]
        pred = proba >= threshold

        new_input = Input(
            timestamp_input=datetime.datetime.now(),
            employee_id=employee_id,
            age=employe.age
        )
        db.add(new_input)
        db.commit()
        db.refresh(new_input)

        new_output = Output(
            id_input=new_input.id_input,
            prediction=int(pred),
            probabilite=float(proba)

        )
        db.add(new_output)
        db.commit()

        return {
            "params": data,
            "probabilité": round(float(proba), 3),
            "prédiction": bool(pred)

        }

    except Exception as e:
        print("ERROR PREDICT_FROM_DB:", e)
        traceback.print_exc()
        return {"error": str(e)}
