from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_total_grants_endpoint():
    response = client.get("/v1/grants/total?donor=France&sector=Health&modality=Grant")
    assert response.status_code == 200
    data = response.json()
    assert "total_grant_usd" in data
    assert isinstance(data["total_grant_usd"], float)

def test_by_year_endpoint():
    response = client.get("/v1/grants/by_year?donor=France&sector=Health&modality=Grant")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "year" in data[0]
        assert "total_grant_usd" in data[0]