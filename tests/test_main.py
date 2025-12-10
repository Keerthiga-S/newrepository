from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "Hello from FastAPI!" in r.json().get("message")

def test_add_default():
    r = client.get("/add")
    assert r.status_code == 200
    assert r.json() == {"result": 0}

def test_add_values():
    r = client.get("/add?a=3&b=5")
    assert r.status_code == 200
    assert r.json() == {"result": 8}
