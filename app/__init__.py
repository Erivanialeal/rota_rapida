from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa as extensões
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Registra blueprints
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    return app