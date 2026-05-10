import joblib
import pandas as pd


model = joblib.load("artifacts/linear_regression_model.pkl")
rf_model = joblib.load("artifacts/rf_model.pkl")


def predict_house_price(data):
    df = pd.DataFrame([data])

    prediction = rf_model.predict(df)

    return float(prediction[0])