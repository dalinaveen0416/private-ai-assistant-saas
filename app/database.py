from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse


# Credentials
USER_NM = "username"

PASSWORD = "Password"

HOST = "127.0.0.1" or "localhost"

PORT = "3306" #change accordingly if you have a different port

DB_NAME = "genai_saas"


# Encode password (important for special characters like @)
ENCODED_PASSWORD = urllib.parse.quote_plus(PASSWORD)


# Database URL
DATABASE_URL = f"mysql+pymysql://{USER_NM}:{ENCODED_PASSWORD}@{HOST}:{PORT}/{DB_NAME}"


# Engine
engine = create_engine(
    DATABASE_URL,
    echo=True
)


# Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base
Base = declarative_base()


# Dependency
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
