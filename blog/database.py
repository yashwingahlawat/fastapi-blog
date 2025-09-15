import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from . import config

DATABASE_URL = config.settings.DATABASE_URL

# connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal=sessionmaker(bind=engine,autoflush=False)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()