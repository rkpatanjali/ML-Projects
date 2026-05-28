import joblib
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = ROOT_DIR / "artifacts"

model = joblib.load(ARTIFACT_DIR / "linear_regression_model.pkl")
rf_model = joblib.load(ARTIFACT_DIR / "rf_model.pkl")


def predict_house_price(data):
    df = pd.DataFrame([data])

    prediction = rf_model.predict(df)

    return float(prediction[0])