from fastapi import status


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "ok"


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_predict_valid_request(client, valid_flight_request):
    response = client.post("/predict", json=valid_flight_request)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["prediction"] in ["on_time", "delayed"]
    assert 0.0 <= data["probability"] <= 1.0
    assert "request_id" in data
    assert "timestamp" in data


def test_predict_invalid_airline(client):
    payload = {"airline": "INVALID", "origin": "CDG", "destination": "JFK", "scheduled_departure": "2026-06-15T14:30:00Z"}
    response = client.post("/predict", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_predict_missing_filed(client):
    payload = {"airline": "AF", "origin": "CDG"}
    response = client.post("/predict", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
