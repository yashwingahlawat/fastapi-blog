from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv('DATABASE_URL','Ok')
    SECRET_KEY = os.getenv('SECRET_KEY','Ok')
    ALGORITHM = os.getenv('ALGORITHM','Ok')
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES','Ok')

settings = Settings()