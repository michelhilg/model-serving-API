# Import dependencies
from flask import Flask, request, jsonify, g
import datetime
import joblib
import pytz
import sqlite3
import logging

class ModelServingAPI:
    def __init__(self, model_path="modelo.joblib", database_path='identificadores_db.db', desired_timezone='America/Sao_Paulo'):
        self.app = Flask(__name__)
        self.model = self.load_model(model_path)
        self.database_path = database_path
        self.desired_timezone = desired_timezone
        self.init_app()

    def load_model(self, model_path):
        try:
            return joblib.load(model_path)
        except Exception as e:
            self.app_logger.error(f"Failed to load the model: {str(e)}")
            raise

    def init_db(self):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS identificadores (
                id INTEGER PRIMARY KEY
            )
        ''')
        conn.commit()

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(self.database_path)
        return db

    def init_app(self):
        self.init_db()

        # Set up logging
        self.app_logger = logging.getLogger('application_logger')
        self.app_logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        file_handler = logging.FileHandler("app.txt")
        file_handler.setFormatter(formatter)
        self.app_logger.addHandler(file_handler)

        self.app_logger.info("Application initialized")

        # Route for the POST method
        @self.app.route('/predict', methods=['POST'])
        def predict():
            #global last_id

            # Update the last id (using the autoincrement from SQLite)
            with self.get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO identificadores (id) VALUES (NULL)')
                conn.commit()
                last_id = cursor.lastrowid

            # Get the current time in São Paulo timezone in the isoformat
            current_time = datetime.datetime.now(pytz.timezone(self.desired_timezone)).isoformat()

            try:
                # Request data
                feature_1 = float(request.json['feature_1'])
                feature_2 = float(request.json['feature_2'])

                # Model prediction
                prediction = self.model.predict([[feature_1, feature_2]])[0]

                # Generating the JSON response
                response = {
                    "data": current_time,
                    "predicao": round(prediction, 5),
                    "id": last_id
                }

                # Saving the success log
                self.app_logger.info(f"status: 200, id: {last_id}, feature_1: {feature_1}, feature_2: {feature_2}, predição: {prediction}")
                return jsonify(response)
            
            except ValueError as ve:
                # Dealing with value errors
                error_message = f"Invalid input data: {str(ve)}"
                self.app_logger.error(f"status: 400, id: {last_id}, mensagem de erro: {error_message}")
                return jsonify({"error": error_message}), 400

            except Exception as e:
                # Dealing with unexpected errors
                error_message = f"Unexpected error: {str(e)}"
                self.app_logger.error(f"status: 500, id: {last_id}, mensagem de erro: {error_message}")
                return jsonify({"error": error_message}), 500
            
    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    my_app = ModelServingAPI()
    my_app.run()