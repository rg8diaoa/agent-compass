from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_create_task():
    r = client.post("/tasks", json={"title": "Buy milk"})
    assert r.status_code == 201
    assert r.json()["title"] == "Buy milk"

def test_list_tasks():
    r = client.get("/tasks")
    assert r.status_code == 200

def test_delete_task():
    r = client.post("/tasks", json={"title": "Test"})
    task_id = r.json()["id"]
    r = client.delete(f"/tasks/{task_id}")
    assert r.status_code == 200
