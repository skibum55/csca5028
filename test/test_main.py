from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.text == "OK"

def test_read_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text != ''

def test_analyze():
    response = client.get(f"/analyze/So happy to be alive!")
    assert response.status_code == 201
    assert response.text == "POSITIVE"

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.text != ""