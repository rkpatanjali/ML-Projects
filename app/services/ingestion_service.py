import pandas as pd
from sklearn.datasets import fetch_california_housing
from app.core.database import engine
from datetime import datetime


def generate_batch_id():
    return datetime.now().strftime("batch_%Y%m%d_%H%M%S")


def load_historical_data():
    housing = fetch_california_housing(as_frame=True)

    df = housing.frame

    df.columns = [
        "medinc",
        "houseage",
        "averooms",
        "avebedrms",
        "population",
        "aveoccup",
        "latitude",
        "longitude",
        "medhouseval"
    ]

    df["source_type"] = "historical"
    df["batch_id"] = generate_batch_id()

    return df


def ingest_historical_data():
    df = load_historical_data()

    df.to_sql(
        name="housing_raw",
        con=engine,
        schema="raw_data",
        if_exists="append",
        index=False
    )

    print("Historical data loaded successfully.")
def ingest_incremental_data(df):
    df["source_type"] = "incremental"
    df["batch_id"] = generate_batch_id()

    df.to_sql(
        name="housing_staging",
        con=engine,
        schema="raw_data",
        if_exists="append",
        index=False
    )

    print("Incremental data loaded.")
if __name__ == "__main__":
    ingest_historical_data()