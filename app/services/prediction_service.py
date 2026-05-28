import joblib
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = ROOT_DIR / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "linear_regression_model.pkl"
RF_MODEL_PATH = ARTIFACT_DIR / "rf_model.pkl"

model = None
rf_model = None


def load_models():
    global model, rf_model

    if model is not None and rf_model is not None:
        return

    if not MODEL_PATH.exists() or not RF_MODEL_PATH.exists():
        from app.services.training_service import train_model
        train_model()

    try:
        model = joblib.load(MODEL_PATH)
        rf_model = joblib.load(RF_MODEL_PATH)
    except Exception as e:
        print(f"Model load failed: {e}. Re-training models.")
        from app.services.training_service import train_model
        train_model()
        model = joblib.load(MODEL_PATH)
        rf_model = joblib.load(RF_MODEL_PATH)


def predict_house_price(data):
    load_models()
    df = pd.DataFrame([data])

    prediction = rf_model.predict(df)

    return float(prediction[0])