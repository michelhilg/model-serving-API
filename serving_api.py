# Testing the prediction process over the use of the API
from flask import Flask, request, jsonify, g
import datetime
import joblib
import pytz
import sqlite3
import logging

app = Flask(__name__)

# Loading the model
model = joblib.load("modelo.joblib")

# Set the desired timezone to São Paulo
desired_timezone = 'America/Sao_Paulo'

# Connection to the database and creation of the table if necessary
DATABASE = 'identificadores_db.db'
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS identificadores (
            id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()

# Function to further connect to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Define the file for dealing with the logs 
log_filename = "app.txt"

# Create a custom logger
app_logger = logging.getLogger('application_logger')
app_logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(formatter)
app_logger.addHandler(file_handler)

# Route for the POST method
@app.route('/predict', methods=['POST'])
def predict():
    global last_id

    # Update the last id (using the autoincrement from SQLite)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO identificadores (id) VALUES (NULL)')
        conn.commit()
        last_id = cursor.lastrowid

    # Get the current time in São Paulo timezone in the isoformat
    current_time = datetime.datetime.now(pytz.timezone(desired_timezone)).isoformat()

    try:
        # Request data
        feature_1 = float(request.json['feature_1'])
        feature_2 = float(request.json['feature_2'])

        # Model prediction
        prediction = model.predict([[feature_1, feature_2]])[0]

        # Generating the JSON response
        response = {
            "data": current_time,
            "predicao": round(prediction, 5),
            "id": last_id
        }

        # Saving the success log
        app_logger.info(f"status: 200, id: {last_id}, feature_1: {feature_1}, feature_2: {feature_2}, predição: {prediction}")
        return jsonify(response)
    
    except ValueError as ve:
        # Dealing with value errors
        error_message = f"Invalid input data: {str(ve)}"
        app_logger.error(f"status: 400, id: {last_id}, mensagem de erro: {error_message}")
        return jsonify({"error": error_message}), 400

    except Exception as e:
        # Dealing with unexpected errors
        error_message = f"Unexpected error: {str(e)}"
        app_logger.error(f"status: 500, id: {last_id}, mensagem de erro: {error_message}")
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)
    init_db()


