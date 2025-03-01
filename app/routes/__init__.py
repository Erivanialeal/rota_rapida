

def registrar_blueprint(app):
    from routes.rota_pesquisa import pesquisa_bp

    app.registrar_blueprint(pesquisa_bp,url_prefix='pesquisa')