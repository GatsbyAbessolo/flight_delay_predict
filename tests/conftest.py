import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.flight_model import FlightDelayModel


@pytest.fixture(autouse=True)
def setup_model_for_tests():
    if not hasattr(app.state, "model"):
        app.state.model = FlightDelayModel()
        app.state.model.load()
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def valid_flight_request():
    return {
        "airline": "AF",
        "origin": "CDG",
        "destination": "JFK",
        "scheduled_departure": "2026-06-15T14:30:00Z",
        "weather": "rainy"
    }
