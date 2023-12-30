from flask import Blueprint, jsonify, request, current_app
import datetime
import pytz
from database.database import DatabaseManager

app_blueprint = Blueprint('app', __name__)

@app_blueprint.route('/predict', methods=['POST'])
def predict():
    """
    Handle POST requests to the '/predict' endpoint.

    Returns:
    - JSON: A JSON response with prediction results or error messages.
    """
    
    model = current_app.model
    desired_timezone = current_app.desired_timezone
    logger = current_app.logger
    database_path = current_app.database_path

    db_manager = DatabaseManager(database_path)

    # Autoincrement in SQLite for the request id
    with db_manager.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO identificadores (id) VALUES (NULL)')
        conn.commit()
        last_id = cursor.lastrowid  

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
