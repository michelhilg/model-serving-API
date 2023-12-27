# Testing the load process of the model
import joblib
from sklearn.linear_model import LinearRegression

model = joblib.load('modelo.joblib')

feature_1 = float(1)
feature_2 = float(2)

# Realizando a predição com o modelo
prediction = model.predict([[feature_1, feature_2]])[0]

print(prediction)


