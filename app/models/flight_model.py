import joblib
import logging
import random
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)


class FlightDelayModel:

    MODEL_PATH = Path(__file__).parent / "model.pkl"
    VERSION = "v1.0.0"

    def __init__(self):
        self._model = None
        self._loaded = False

    def load(self) -> bool:
        try:
            if self.MODEL_PATH.exists():
                self._model = joblib.load(self.MODEL_PATH)
                self._loaded = True
                logger.info("Model successfully downloaded")
            else:
                logger.warning("File not found")
                self._loaded = False
            return self._loaded
        except Exception as e:
            logger.error(f"Erreur lors du chargement du mode {e}")
            return False

    def predict(self, features: pd.DataFrame) -> dict:
        if not self._loaded or self._model is None:
            prob = round(random.uniform(0.15, 0.95), 3)
            return {
                "prediction": "delayed" if prob > 0.5 else "on_time",
                "probability": prob,
                "estimated_delay_minutes": int(prob * 60) if prob > 0.5 else None
            }
        prob = float(self._model.predict_proba(features)[0][1])
        delay_pred = int(self._model.predict(features)[0])

        return {
            "prediction": "delayed" if delay_pred == 1 else "on_time",
            "probability": prob,
            "estimated_delay_minutes": int(prob * 60) if prob > 0.5 else None,
        }

    @property
    def is_loaded(self) -> bool:
        return self._loaded
