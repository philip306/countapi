from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

def test_create_randomkey():
    key = str(uuid.uuid4())
    response = client.get("/create?key=" + key)
    assert response.status_code == 200
    assert response.json() == {"namespace": "default", "key": key, "value": "0"}

def test_create_randomkeyandns():
    namespace = str(uuid.uuid4())
    key = str(uuid.uuid4())
    response = client.get("/create?namespace=" + namespace + "&key=" + key)
    assert response.status_code == 200
    assert response.json() == {"namespace": namespace, "key": key, "value": "0"}

def test_create_existingkey():
    key = str(uuid.uuid4())
    client.get("/create?key=" + key)
    response = client.get("/create?key=" + key)
    assert response.status_code == 400
    assert response.json() == {"detail": "Namespace and key default: " + key + " already exist"}

def test_create_statsnamespace():
    key = str(uuid.uuid4())
    response = client.get("/create?namespace=stats&key=" + key)
    assert response.status_code == 403
    assert response.json() == {"detail": "Reserved keyword stats cannot be used for namespace"}

def test_create_test():
    key = "*%26^%)(%26%(^$)" + str(uuid.uuid4())
    response = client.get("/create?key=" + key)
    assert response.status_code == 200
    assert response.json() == {"namespace": "default", "key": key, "value": "0"}