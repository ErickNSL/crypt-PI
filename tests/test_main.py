import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

# Test the core analytics endpoint
def test_analytics_endpoint_structure():
    response = client.get("/analytics/avg-price")
    assert response.status_code == 200
    

    data = response.json()
    assert "analytics" in data
    assert isinstance(data["analytics"], list)
    
# Test the ingestion  (E, L, T steps)
def test_ingestion_endpoint():
    response = client.get("/ingest")
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "Ingested"

    assert data["rows"] >= 3