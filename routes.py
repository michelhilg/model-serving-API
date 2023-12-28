from flask import jsonify, request
import datetime
import pytz

def register_routes(app, model, desired_timezone, logger, last_id):
    """
    Register routes for handling prediction requests.

    Parameters:
    - model_path (str): Path to the machine learning model file.
    - database_path (str): Path to the SQLite database file.
    - desired_timezone (str): The desired timezone for date and time operations.
    - log_file_path (str): Path to the text log file.
    - last_id (integer): The last inserted identifier in the database.
    """
    
    @app.route('/predict', methods=['POST'])
    def predict():
        """
        Handle POST requests to the '/predict' endpoint

        Returns:
        - JSON: A JSON response with prediction results or error messages.
        """
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
            # Handling value errors caused by invalid input data
            error_message = f"Invalid input data: {str(ve)}"
            logger.error(f"status: 400, id: {last_id}, mensagem de erro: {error_message}")
            return jsonify({"error": error_message}), 400

        except Exception as e:
            # Handling unexpected errors
            error_message = f"Unexpected error: {str(e)}"
            logger.error(f"status: 500, id: {last_id}, mensagem de erro: {error_message}")
            return jsonify({"error": error_message}), 500
