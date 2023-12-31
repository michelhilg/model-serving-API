from database.database import db
import datetime

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    feature_1 = db.Column(db.Float, unique=False)
    feature_2 = db.Column( db.Float, unique=False)
    predicao = db.Column(db.Float, unique=False)

    def __init__(self, feature_1, feature_2, predicao):
        self.feature_1 = feature_1
        self.feature_2 = feature_2
        self.predicao = predicao
