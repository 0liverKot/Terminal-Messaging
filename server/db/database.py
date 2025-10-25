from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
URL_DATABASE = os.environ.get("URL_DATABASE")
ROOT_URL = os.environ.get("ROOT_URL")

if URL_DATABASE is None:
    raise Exception("issue loading environment variables")

engine =create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close
