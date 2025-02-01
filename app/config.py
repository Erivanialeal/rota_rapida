import os
from dotenv import load_dotenv


class Config:
    load_dotenv()  # Carrega as variáveis do .env
    SECRET_KEY=os.environ.get("CHAVE_SECRET")
    SQLALCHEMY_DATABASE_URL=os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET') 