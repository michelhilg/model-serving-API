from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DBManager:
    """A Python class using SQLAlchemy for database related methods."""

    def __init__(self):
        self.db = db

    def init_table(self, app):
        self.db.init_app(app)
        with app.app_context():
            self.db.create_all()

    def write_prediction(self, table_class, feature_1, feature_2, predicao):
        """
        Write a new prediction in the database.

        Returns:
        - The id of the prediction.
        """
        new_entry = table_class(feature_1=feature_1, feature_2=feature_2, predicao=predicao)
        self.db.session.add(new_entry)
        self.db.session.commit()

        return new_entry.id


