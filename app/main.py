# filepath: c:\Users\ACER\OneDrive\Documents\Kuliah\Semester_6\Komputasi_Awan\Tugas_Besar_EAS\flask-sanchez-similarity\app\main.py
import os
from flask import Flask

from .api.similarity import similarity_bp
from .controllers.main_controller import main_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(similarity_bp, url_prefix="/api")
    app.register_blueprint(main_bp)
    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080)) 
    app.run(host="0.0.0.0", port=port, debug=True)