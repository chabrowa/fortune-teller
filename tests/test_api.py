"""Tests for the HTTP API that do not call the model."""

from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_requires_question():
    response = client.post("/predict", json={})
    assert response.status_code == 422