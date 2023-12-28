from flask import jsonify, request
import datetime
import pytz

def register_routes(app, model, desired_timezone, logger, last_id):
    @app.route('/predict', methods=['POST'])
    def predict():

        current_time = datetime.datetime.now(pytz.timezone(desired_timezone)).isoformat()

        try:
            feature_1 = float(request.json['feature_1'])
            feature_2 = float(request.json['feature_2'])

            prediction = model.predict([[feature_1, feature_2]])[0]

            response = {
                "data": current_time,
                "predicao": round(prediction, 5),
                "id": last_id
            }

            logger.info(f"status: 200, id: {last_id}, feature_1: {feature_1}, feature_2: {feature_2}, predição: {prediction}")
            return jsonify(response)

        except ValueError as ve:
            # Dealing with value errors caused by invalid input data
            error_message = f"Invalid input data: {str(ve)}"
            logger.error(f"status: 400, id: {last_id}, mensagem de erro: {error_message}")
            return jsonify({"error": error_message}), 400

        except Exception as e:
            # Dealing with unexpected errors
            error_message = f"Unexpected error: {str(e)}"
            logger.error(f"status: 500, id: {last_id}, mensagem de erro: {error_message}")
            return jsonify({"error": error_message}), 500
