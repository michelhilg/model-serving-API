from flask import Flask, g
import joblib
import sqlite3
import logging
from routes import register_routes
import os
from dotenv import find_dotenv, load_dotenv
from database_tools import DatabaseManager

# Load up the entries as environment variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
MODEL_PATH = os.getenv("MODEL_PATH")                
DATABASE_PATH = os.getenv("DATABASE_PATH")    
DESIRED_TIMEZONE = os.getenv("DESIRED_TIMEZONE")       
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH") 

class ModelServingAPI:

    """
    A Python class using a Flask application for prediction a target value based on two features 
    using a pretrained machine learning model in .joblib format.
    """

    def __init__(self, model_path, database_path, desired_timezone, log_file_path):
        """
        Initialize the ModelServingAPI instance.

        Parameters:
        - model_path (str): Path to the machine learning model file.
        - database_path (str): Path to the SQLite database file.
        - desired_timezone (str): The desired timezone for date and time operations.
        - log_file_path (str): Path to the text log file.
        """
        self.app = Flask(__name__)
        self.model = self.load_model(model_path)
        self.database_path = database_path
        self.desired_timezone = desired_timezone
        self.log_file_path = log_file_path
        self.setup_app()

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
        register_routes(self.app, self.model, self.desired_timezone, self.logger)

    def setup_app(self):
        self.init_db()
        self.setup_logging()
        self.register_routes()
            
    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    model_serving_api = ModelServingAPI(MODEL_PATH, DATABASE_PATH, DESIRED_TIMEZONE, LOG_FILE_PATH)
    model_serving_api.run()