
import logging
import uuid
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from app.schemas.prediction import FlightRequest, PredictionResponse
from app.models.flight_model import FlightDelayModel
from app.utils.preprocessing import preprocess_flight_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Démarrage du service Flight Delay Predictor...")
    app.state.model = FlightDelayModel()
    app.state.model.load()
    yield
    logger.info("Arrêt du service...")

app = FastAPI(
    title="Flight Delay Predictor API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Flight Delay Predictor API is running!", "status": "ok"}


@app.get("/health", tags=["Health"])
async def health():
    model = getattr(app.state, "model", None)
    return {
        "status": "healthy",
        "model_loaded": model.is_loaded if model else False,
        "version": model.VERSION if model else "unknown"
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_flight_delay(request: FlightRequest):
    """Prédit si un vol sera retardé."""
    # Vérifier que le modèle est disponible
    model = getattr(app.state, "model", None)
    if not model:
        logger.error("Modèle non initialisé dans app.state")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service non prêt - modèle non chargé")
    try:
        features = preprocess_flight_data(request.model_dump())

        result = model.predict(features)

        return PredictionResponse(
            prediction=result["prediction"],
            probability=result["probability"],
            estimated_delay_minutes=result.get("estimated_delay_minutes"),
            model_version=model.VERSION,
            request_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Erreur de prédiction: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne lors de la prédiction")
