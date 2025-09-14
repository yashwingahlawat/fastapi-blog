from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv('DATABASE_URL','Ok')

settings = Settings()