from flask import Flask
from app.views import app_blueprint
import joblib
import logging
from config import DevelopmentConfig, TestingConfig, ProductionConfig
import argparse
from database.database import DBManager

def create_app(mode):
    """Initialize the Flask application"""
    app = Flask(__name__)
    
    app.config.from_object(get_config(mode))
    app.model = load_model(app.config.get("MODEL_PATH"))
    app.desired_timezone = app.config.get("DESIRED_TIMEZONE")
    log_file_path = app.config.get("LOG_FILE_PATH")
    app.logger = setup_logging(log_file_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = app.config.get("SQLALCHEMY_TRACK_MODIFICATIONS") 

    db_manager = DBManager()
    db_manager.init_table(app)

    app.register_blueprint(app_blueprint)

    return app

def get_config(mode):
    if mode == "production":
        return ProductionConfig
    elif mode == "testing":
        return TestingConfig
    else:
        return DevelopmentConfig

def load_model(model_path):
    try:
        return joblib.load(model_path)
    except Exception as e:
        logging.error(f"Failed to load the model: {str(e)}")
        raise

def setup_logging(log_file_path):
    """Set up the custom log for the application."""
    logger = logging.getLogger('model_serving_logger')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info("Application initialized")
    return logger

def parse_arguments():
    """Enable the selection of the environment from the command line."""
    parser = argparse.ArgumentParser(description="Run the ModelServingAPI application.")
    parser.add_argument('--mode', choices=['development', 'testing'], default='development', help="Specify the execution mode.")
    args = parser.parse_args()
    return args.mode

if __name__ == '__main__':
    mode = parse_arguments()
    myapp = create_app(mode)
    myapp.run()
