import pandas as pd
from sklearn.preprocessing import StandardScaler


def clean_data(df):
    df = df.drop_duplicates()
    df = df.dropna()

    return df


def scale_features(df):
    scaler = StandardScaler()

    feature_columns = [
        "medinc",
        "houseage",
        "averooms",
        "avebedrms",
        "population",
        "aveoccup",
        "latitude",
        "longitude"
    ]

    df[feature_columns] = scaler.fit_transform(df[feature_columns])

    return df

