from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from app.routes.rota_pesquisa import pesquisa_bp #importar o blueprint

#from app.models import Pesquisa



db = SQLAlchemy()
migrate = Migrate()

def create_app():
    from app.config import Config  # Importação dentro da função
    
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from app.models import Pesquisa,Filtros,HistoricoPesquisa,ResultadoPesquisa
    # Registro do Blueprint
    app.register_blueprint(pesquisa_bp, url_prefix='/')

    return app