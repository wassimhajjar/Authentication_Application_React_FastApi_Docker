from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL=os.getenv("POSTGRESQL_DATABASE_URL")

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocomplete=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    """
    The function `get_db` creates a database session and yields it for use, ensuring the session is
    closed properly afterwards.
    """
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


