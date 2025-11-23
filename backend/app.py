# backend/app.py

from flask import Flask
from routes.geocoding import geocoding_bp

def create_app():
    app = Flask(__name__)

    # register blueprints
    app.register_blueprint(geocoding_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)