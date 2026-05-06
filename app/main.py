from fastapi import FastAPI
import uuid
from datetime import datetime
from app.schemas.prediction import FlightRequest, PredictionResponse

app = FastAPI(title = "Flight Delay Predictor", version = "1.0")

@app.get("/")
async def root():
    return {"message": "L'application tourne", "status" : "ok"}

@app.get("/health")
async def health():
    return {"status" : "all good"}

@app.post("/predict", response_model = PredictionResponse)
async def predict_flight_delay(request: FlightRequest):

    return PredictionResponse(
        prediction = "on_time",
        probability = 0.0,
        estimated_delay_minutes = None,
        model_version = "v1.0.0",
        request_id = str(uuid.uuid4()),
        timestamp = datetime.utcnow()
    )