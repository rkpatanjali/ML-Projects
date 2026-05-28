import os
import streamlit as st
import requests


st.title("Housing Price Prediction")

medinc = st.number_input("Median Income")
houseage = st.number_input("House Age")
averooms = st.number_input("Average Rooms")
avebedrms = st.number_input("Average Bedrooms")
population = st.number_input("Population")
aveoccup = st.number_input("Average Occupancy")
latitude = st.number_input("Latitude")
longitude = st.number_input("Longitude")


API_BASE = os.environ.get("API_URL", "http://127.0.0.1:8000")

if st.button("Predict"):
    payload = {
        "medinc": medinc,
        "houseage": houseage,
        "averooms": averooms,
        "avebedrms": avebedrms,
        "population": population,
        "aveoccup": aveoccup,
        "latitude": latitude,
        "longitude": longitude
    }

    response = requests.post(f"{API_BASE}/predict", json=payload)

    result = response.json()

    st.success(
        f"Predicted House Value: {result['predicted_house_value']}"
    )