

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Detect HF Space or test environment
RUNNING_IN_HF = os.getenv("SPACE_ID") is not None
RUNNING_TESTS = os.getenv("ENV") == "test"

if RUNNING_IN_HF or RUNNING_TESTS:
    # Use SQLite for HuggingFace and for tests
    DATABASE_URL = "sqlite:///./futurisys.db"
    print("DATABASE_URL =", DATABASE_URL)

else:
    # Normal PostgreSQL configuration
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

