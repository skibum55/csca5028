"""Function printing python version."""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_collect():
    """Function testing message collection."""
    response = client.get("/collect")
    assert response.status_code == 201
    assert response.json() == ['hola mundo']

def test_read_health():
    """Function testing health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.text == "OK"

def test_read_home():
    """Function validating homepage rendering."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.text != ''

def test_analyze():
    """Function testing sentiment analysis."""
    response = client.get(f"/analyze/So happy to be alive!")
    assert response.status_code == 201
    assert response.text == "POSITIVE"

def test_metrics():
    """Function testing scrape endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.text != ""

