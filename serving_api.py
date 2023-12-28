from flask import Flask, g
import joblib
import sqlite3
import logging
from routes import register_routes

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
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS identificadores (
                id INTEGER PRIMARY KEY
            )
        ''')
        conn.commit()

    def get_db(self):
        """
        Get the SQLite database connection. Step necessary due to the multithreading feature of Flask.

        Returns:
        - sqlite3.Connection: SQLite database connection.
        """
        with self.app.app_context():  # Use app.app_context() to work within the Flask context
            db = getattr(g, '_database', None)
            if db is None:
                db = g._database = sqlite3.connect(self.database_path)
            return db
    
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
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO identificadores (id) VALUES (NULL)')
            conn.commit()
            last_id = cursor.lastrowid
        register_routes(self.app, self.model, self.desired_timezone, self.logger, last_id)

    def setup_app(self):
        self.init_db()
        self.setup_logging()
        self.register_routes()
            
    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    model_path = "modelo.joblib"                
    database_path = "identificadores_db.db"    
    desired_timezone = "America/Sao_Paulo"      
    log_file_path = "log.txt"                   
    model_serving_api = ModelServingAPI(model_path, database_path, desired_timezone, log_file_path)
    model_serving_api.run()