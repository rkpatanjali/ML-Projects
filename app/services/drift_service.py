import pandas as pd
from app.core.database import engine


def detect_mean_drift():
    raw_query = "SELECT AVG(medinc) AS avg_medinc FROM raw_data.housing_raw"
    stage_query = "SELECT AVG(medinc) AS avg_medinc FROM raw_data.housing_staging"

    raw_avg = pd.read_sql(raw_query, engine).iloc[0]["avg_medinc"]
    stage_avg = pd.read_sql(stage_query, engine).iloc[0]["avg_medinc"]

    drift = abs(stage_avg - raw_avg)

    print(f"Drift detected: {drift}")

    return drift