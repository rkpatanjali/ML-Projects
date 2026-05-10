from pydantic import BaseModel


class HousingPredictionRequest(BaseModel):
    medinc: float
    houseage: float
    averooms: float
    avebedrms: float
    population: float
    aveoccup: float
    latitude: float
    longitude: float