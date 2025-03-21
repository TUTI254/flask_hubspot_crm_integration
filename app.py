import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from config import load_config
from utils.logging_config import configure_logging
from routes.routes import routes_bp

def create_app(env_name=None):
    
    app = Flask(__name__)

    db = SQLAlchemy()
    
    # Load config from environment
    config_obj = load_config(env_name)
    app.config.from_object(config_obj)

    # Setup logging
    log_level = app.config.get("LOG_LEVEL", "INFO")
    configure_logging(log_level)

    logging.info("Creating Flask app with environment: %s", env_name)

    # Initialize DB
    db.init_app(app)    

    
    # Configure Swagger
    app.config['SWAGGER'] = {
        "title": "HubSpot CRM Integration API",
        "description": "API for managing HubSpot CRM objects.",
        "version": "1.0.0",
        "uiversion": 3
    }
    Swagger(app)
    
    @app.route('/')
    def index():
        return " Project is running!"
    
    app.register_blueprint(routes_bp)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)