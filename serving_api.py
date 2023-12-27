# Testing the prediction process over the use of the API
from flask import Flask, request, jsonify
import datetime
import joblib
import pytz 

app = Flask(__name__)

# Loading the model
model = joblib.load("modelo.joblib")

# Set the desired timezone to São Paulo
desired_timezone = 'America/Sao_Paulo'

# Route for the POST method
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Request data
        feature_1 = float(request.json['feature_1'])
        feature_2 = float(request.json['feature_2'])

        # Get the current time in São Paulo timezone
        current_time = datetime.datetime.now(pytz.timezone(desired_timezone))

        # Model prediction
        prediction = model.predict([[feature_1, feature_2]])[0]

        # Generating the JSON response
        response = {
            "data": current_time.isoformat(),
            "predicao": round(prediction, 5),
            "id": "id_here"
        }

        return jsonify(response)

    except Exception as e:
        # Dealing with the errors
        error_message = f"Request error: {str(e)}"
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)


