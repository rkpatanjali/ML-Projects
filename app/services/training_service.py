import pandas as pd
import joblib
from pathlib import Path

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from app.core.database import engine
from sqlalchemy import text

ROOT_DIR = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = ROOT_DIR / "artifacts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = ARTIFACT_DIR / "linear_regression_model.pkl"
RF_MODEL_PATH = ARTIFACT_DIR / "rf_model.pkl"

def fetch_processed_data():
    query = "SELECT * FROM processed_data.housing_features"
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Database load failed: {e}")
        print("Falling back to local California housing dataset for training.")
        dataset = fetch_california_housing(as_frame=True)
        df = dataset.frame
        if "MedHouseValue" in df.columns:
            df = df.rename(columns={"MedHouseValue": "medhouseval"})
        elif "MedHouseVal" in df.columns:
            df = df.rename(columns={"MedHouseVal": "medhouseval"})
        df["id"] = range(1, len(df) + 1)
        df["batch_id"] = 1
        df["created_at"] = pd.Timestamp("2020-01-01")
        return df


def train_model():
    df = fetch_processed_data()

    X = df.drop(columns=["id", "medhouseval", "batch_id", "created_at"])
    y = df["medhouseval"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()  

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print(f"MSE: {mse}")
    print(f"R2 Score: {r2}")

    joblib.dump(model, MODEL_PATH,compress=3)

    print("Model saved successfully.")
    try:
        with engine.connect() as conn:
            conn.execute(
            text("""
                INSERT INTO model_registry.models
                (model_name, version, mse, r2_score, artifact_path)
                VALUES
                (:model_name, :version, :mse, :r2_score, :artifact_path)
            """),
            {
                "model_name": "linear_regression",
                "version": "v1",
                "mse": mse,
                "r2_score": r2,
                "artifact_path": str(MODEL_PATH)
            }
        )
            conn.commit()
    except Exception as e:
        print(f"Database write failed (non-critical): {e}")
    rf_model = RandomForestRegressor(random_state=42)

    rf_model.fit(X_train, y_train)

    rf_predictions = rf_model.predict(X_test)
    rf_mse = mean_squared_error(y_test, predictions)
    rf_r2 = r2_score(y_test, rf_predictions)

    print(f"RF R2 Score: {rf_r2}")
    joblib.dump(rf_model, RF_MODEL_PATH,compress=3)
    print("Model saved successfully.")
    try:
        with engine.connect() as conn:
            conn.execute(
            text("""
                INSERT INTO model_registry.models
                (model_name, version, mse, r2_score, artifact_path)
                VALUES
                (:model_name, :version, :mse, :r2_score, :artifact_path)
            """),
            {
                "model_name": "randomforest_regression",
                "version": "v1",
                "mse": rf_mse,
                "r2_score": rf_r2,
                "artifact_path": str(RF_MODEL_PATH)
            }
        )
            conn.commit()
    except Exception as e:
        print(f"Database write failed (non-critical): {e}")
    

if __name__ == "__main__":
    train_model()