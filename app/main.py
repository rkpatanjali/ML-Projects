from fastapi import FastAPI
from app.api.routes import router


app = FastAPI(
    title="Housing Prediction API"
)

app.include_router(router)