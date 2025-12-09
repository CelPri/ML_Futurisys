import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Détecter environnement HF Space ou de tests
RUNNING_IN_HF = os.getenv("SPACE_ID") is not None
RUNNING_TESTS = os.getenv("ENV") == "test"

# Utiliser SQLite pour Hugging Face et pour les tests  
    # Sinon : configuration PostgreSQL normale**
if True:

    DATABASE_URL = "sqlite:///./futurisys.db"


else:
    # PostgreSQL configuration normale
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

