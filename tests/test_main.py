# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello from FastAPI!"}

def test_add():
    r = client.get("/add?a=3&b=5")
    assert r.status_code == 200
    assert r.json() == {"result": 8}
