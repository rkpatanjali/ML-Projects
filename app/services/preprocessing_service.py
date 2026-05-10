import pandas as pd
from app.core.database import engine
from app.models.preprocess import clean_data, scale_features


def fetch_raw_data():
    query = "SELECT * FROM raw_data.housing_raw"

    df = pd.read_sql(query, engine)
    print("Fetched data!!")

    return df


def process_and_store():
    df = fetch_raw_data()

    df = clean_data(df)

    df = scale_features(df)

    df = df.drop(columns=["id", "source_type", "created_at"])

    df.to_sql(
        name="housing_features",
        con=engine,
        schema="processed_data",
        if_exists="append",
        index=False
    )

    print("Preprocessing completed successfully.")


if __name__ == "__main__":
    process_and_store()