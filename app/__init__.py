from flask import Flask

def create_app():
    app = Flask(__name__)

    with app.app_context():
        from .api.similarity import similarity_bp
        app.register_blueprint(similarity_bp)

    return app