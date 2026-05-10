from fastapi import APIRouter
from app.schemas.prediction_schema import HousingPredictionRequest
from app.services.prediction_service import predict_house_price


router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.post("/predict")
def predict(request: HousingPredictionRequest):
    prediction = predict_house_price(request.model_dump())

    return {
        "predicted_house_value": prediction
    }