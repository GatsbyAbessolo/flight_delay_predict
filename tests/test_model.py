import pandas as pd
from datetime import datetime
from app.models.flight_model import FlightDelayModel
from app.utils.preprocessing import preprocess_flight_data


def test_preprocessing_output():
    req = {"airline": "AF", "origin": "CDG", "destination": "JFK", "scheduled_departure": datetime(2026, 6, 15, 14, 30), "weather": "rainy"}

    df = preprocess_flight_data(req)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df["weather_encoded"].iloc[0] == 2
    assert df["hour"].iloc[0] == 14


def test_model_mock_prediction():
    model = FlightDelayModel()
    features = pd.DataFrame([{"hour": 8, "day_of_week": 1, "weather_encoded": 0}])
    result = model.predict(features)
    assert result["prediction"] in ["on_time", "delayed"]
    assert 0.0 <= result["probability"] <= 1.0
