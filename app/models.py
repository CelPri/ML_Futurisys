from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Input(Base):
    __tablename__ = "inputs"

    id_input = Column(Integer, primary_key=True, index=True)
    timestamp_input = Column(TIMESTAMP)
    employee_id = Column(Integer)
    age = Column(Integer)
    outputs = relationship("Output", back_populates="input")

class Output(Base):
    __tablename__ = "outputs"

    id_output = Column(Integer, primary_key=True, index=True)
    id_input = Column(Integer, ForeignKey("inputs.id_input"))
    prediction = Column(Integer)
    probabilite = Column("probabilite", Float)


    input = relationship("Input", back_populates="outputs")

class Employe(Base):
    __tablename__ = "employes"

    employee_id = Column(Integer, primary_key=True)



    age = Column(Integer)
    revenu_mensuel = Column(Float)
    statut_marital = Column(String)
    departement = Column(String)
    poste = Column(String)

    annee_experience_totale = Column(Integer)
    annees_dans_l_entreprise = Column(Integer)
    annees_dans_le_poste_actuel = Column(Integer)

    satisfaction_employee_environnement = Column(Integer)
    note_evaluation_precedente = Column(Float)
    satisfaction_employee_nature_travail = Column(Integer)
    satisfaction_employee_equipe = Column(Integer)
    satisfaction_employee_equilibre_pro_perso = Column(Integer)
    note_evaluation_actuelle = Column(Float)

    heure_supplementaires = Column(String)
    augementation_salaire_precedente = Column(Float)
    nombre_participation_pee = Column(Integer)
    frequence_deplacement = Column(String)

    annes_sous_responsable_actuel = Column(Integer)

