import pytest
from flask import Flask
from app.routes.rota_pesquisa import pesquisa_bp  # Corrigido para importar da pasta 'routes/pesquisa.py'
from app.config import Config


# Fixture que cria e configura a aplicação Flask para os testes
@pytest.fixture(scope="module")
def app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Carrega as configurações do arquivo config.py
    app.register_blueprint(pesquisa_bp)  # Registra o Blueprint da rota de pesquisa
    yield app  # Faz o Flask ser disponibilizado para os testes
    

# Fixture que cria o cliente de teste
@pytest.fixture(scope="module")
def cliente(app):
    return app.test_client()  # Cria um cliente para testar a aplicação
