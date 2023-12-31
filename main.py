from flask import Flask
from app.views import app_blueprint
import joblib
import logging
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from database.database import DatabaseManager
import argparse

class ModelServingAPI:

    """
    A Python class using a Flask application for prediction a target value based on two features 
    using a pretrained machine learning model in .joblib format.
    """

    def __init__(self, mode):
        """
        Initialize the ModelServingAPI instance.

        Parameters:
        - model_path (str): Path to the machine learning model file.
        - database_path (str): Path to the SQLite database file.
        - desired_timezone (str): The desired timezone for date and time operations.
        - log_file_path (str): Path to the text log file.
        """
        self.app = Flask(__name__)
        self.configure_app(mode)
        self.model = self.load_model(self.app.config.get("MODEL_PATH"))
        self.database_path = self.app.config.get("DATABASE_PATH")
        self.desired_timezone = self.app.config.get("DESIRED_TIMEZONE")
        self.log_file_path = self.app.config.get("LOG_FILE_PATH")
        self.setup_app()

    def configure_app(self, mode):
        """Configure App based on the --mode parameter"""
        if mode == "production":
            self.app.config.from_object(ProductionConfig)
        elif mode == "testing":
            self.app.config.from_object(TestingConfig)
        else:
            self.app.config.from_object(DevelopmentConfig)

    def load_model(self, model_path):
        """
        Load a machine learning model from the specified file path using joblib.

        Returns:
        - object: The loaded machine learning model.
        """
        try:
            return joblib.load(model_path)
        except Exception as e:
            self.app_logger.error(f"Failed to load the model: {str(e)}")
            raise

    def init_db(self):
        """Create a database file and table if not exists using SQLite Python library."""
        self.db_manager = DatabaseManager(self.database_path)
    
    def setup_logging(self):
        """Define the custom logger for the application with format and information level."""
        self.logger = logging.getLogger('model_serving_logger')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.info("Application initialized")
    
    def register_routes(self):
        """Register application routes and pass the required information for handling requests."""
        self.app.register_blueprint(app_blueprint)

    def setup_app(self):
        self.init_db()
        self.setup_logging()
        self.app.model = self.model
        self.app.desired_timezone = self.desired_timezone
        self.app.logger = self.logger
        self.app.database_path = self.database_path
        self.register_routes()
            
    def run(self):
        return self.app

def create_app():
    model_serving_api = ModelServingAPI("production")
    return model_serving_api.run()  

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the ModelServingAPI application.")
    parser.add_argument('--mode', choices=['development', 'testing'], default='development', help="Specify the execution mode.")
    args = parser.parse_args()
    
    model_serving_api = ModelServingAPI(args.mode)
    myapp = model_serving_api.run().run()


