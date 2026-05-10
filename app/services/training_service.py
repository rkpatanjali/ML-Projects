import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from app.core.database import engine
from sqlalchemy import text

def fetch_processed_data():
    query = "SELECT * FROM processed_data.housing_features"

    df = pd.read_sql(query, engine)

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

    joblib.dump(model, "artifacts/linear_regression_model.pkl")

    print("Model saved successfully.")
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
            "artifact_path": "artifacts/linear_regression_model.pkl"
        }
    )
    conn.commit()
    rf_model = RandomForestRegressor(random_state=42)

    rf_model.fit(X_train, y_train)

    rf_predictions = rf_model.predict(X_test)
    rf_mse = mean_squared_error(y_test, predictions)
    rf_r2 = r2_score(y_test, rf_predictions)

    print(f"RF R2 Score: {rf_r2}")
    joblib.dump(rf_model, "artifacts/rf_model.pkl")
    print("Model saved successfully.")
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
            "artifact_path": "artifacts/rf_model.pkl"
        }
    )
    conn.commit()
    

if __name__ == "__main__":
    train_model()