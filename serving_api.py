# Testing the prediction process over the use of the API
from flask import Flask, request, jsonify
import datetime
import joblib
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Loading the model
model = joblib.load("modelo.joblib")

# Route for the POST method
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Request data
        feature_1 = float(request.json['feature_1'])
        feature_2 = float(request.json['feature_2'])

        # Model prediction
        prediction = model.predict([[feature_1, feature_2]])[0]

        # Generating the JSON answer
        response = {
            "data": datetime.datetime.utcnow().isoformat(),
            "predicao": round(prediction, 5),
            "id": "identificador_aqui"
        }

        return jsonify(response)

    except Exception as e:
        # Dealing with the errors
        error_message = f"Request error: {str(e)}"
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)


