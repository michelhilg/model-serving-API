# Testing the prediction process over the use of the API
from flask import Flask, request, jsonify, g
import datetime
import joblib
import pytz
import sqlite3

app = Flask(__name__)

# Loading the model
model = joblib.load("modelo.joblib")

# Set the desired timezone to São Paulo
desired_timezone = 'America/Sao_Paulo'

# Connection to the database and creation of the table if necessary
DATABASE = 'identificadores_db.db'
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

# Define the file and function for deal with the logs
log_filename = "log.txt"
def log(data):
    with open(log_filename, "a") as log_file:
        log_file.write(data + "\n")

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
        log(f"status: 200, id: {last_id}, data: {response['data']}, feature_1: {feature_1}, feature_2: {feature_2}, predição: {prediction}")

        return jsonify(response)

    except Exception as e:
        # Dealing with the errors
        error_message = f"Request error: {str(e)}"

        # Saving the error log
        log(f"status: 400, id: {last_id}, data: {current_time}, mensagem de erro: {error_message}")

        return jsonify({"error": error_message}), 400

if __name__ == '__main__':
    app.run(debug=True)


