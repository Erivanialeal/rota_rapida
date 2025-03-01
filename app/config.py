import os
from dotenv import load_dotenv
import googlemaps

load_dotenv()  # Carrega as variáveis do .env


class Config:
    SECRET_KEY = os.getenv('CHAVE_SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')  # banco de dados MySQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET')
    API_KEY = os.getenv("API_KEY")
    
    # Verificação para garantir que a URI do banco de dados está sendo lida corretamente
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("A variável 'SQLALCHEMY_DATABASE_URI' não foi encontrada no arquivo .env")
    
    gmaps = googlemaps.Client(key=API_KEY)
