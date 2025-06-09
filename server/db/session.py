from sqlmodel import create_engine
from dotenv import load_dotenv
import os

load_dotenv()  # Charge les variables d'environnement depuis .env

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)  # echo=True pour debug SQL
