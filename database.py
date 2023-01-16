from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values
import models

config = dotenv_values()
DEBUG_QUERIES = True if config.get("DEBUG_QUERIES") == 'True' or config.get("DEBUG_QUERIES") == 'true' else False
DB_DRIVER = config.get("DB_DRIVER")
DB_USER = config.get("DB_USER")
DB_PASSWORD = config.get("DB_PASSWORD")
DB_HOST = config.get("DB_HOST")
DB_NAME = config.get("DB_NAME")

# SQLite
#SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'

# Postgres
SQLALCHEMY_DATABASE_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    echo=DEBUG_QUERIES
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def db_models_create_all():
    models.Base.metadata.create_all(bind=engine)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
