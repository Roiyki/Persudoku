from flask import Flask
from config import Config
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__, template_folder=Config.TEMPLATE_FOLDER, static_folder='static')
    app.config.from_object(Config)

    try:
        mongo.init_app(app)
    except Exception as e:
        print(f"Failed to initialize PyMongo: {str(e)}")
        # Handle initialization error as needed

    with app.app_context():
        from .routes import bp as main_bp
        app.register_blueprint(main_bp, url_prefix='/main')

    return app
