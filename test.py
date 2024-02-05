from fastapi.testclient import TestClient

# Assuming your FastAPI application is defined in a module named main
from main import app

client = TestClient(app)

def test_word_frequency():
    response = client.get("/wordFrequency?topic=python&top_n=5")
    assert response.status_code == 200
    assert "Python programming language" in response.json()

def test_search_history():
    response = client.get("/searchHistory")
    assert response.status_code == 200
    assert "Search History" in response.json()
