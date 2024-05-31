# test_main.py
from fastapi.testclient import TestClient


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_item():
    response = client.post("/items/", json={"name": "Test Item", "description": "Test Description", "price": 10, "on_offer": True})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_update_item():
    response = client.put("/items/1", json={"name": "Updated Item", "description": "Updated Description", "price": 20, "on_offer": False})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Item"

def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Item"

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 0