import pytest
from app.api import app, registry

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        registry.accounts = []
        yield client

def test_create_account(client):
    payload = {
        "name": "Jan",
        "surname": "Kowalski",
        "pesel": "12345678901"
    }
    response = client.post("/api/accounts", json=payload)
    assert response.status_code == 201
    assert response.get_json()["message"] == "Account created"
    assert registry.number_of_accounts() == 1

def test_get_account_by_pesel(client):
    payload = {"name": "Anna", "surname": "Nowak", "pesel": "99999999999"}
    client.post("/api/accounts", json=payload)

    response = client.get(f"/api/accounts/{payload['pesel']}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["name"] == "Anna"
    assert data["pesel"] == "99999999999"

def test_get_account_not_found(client):
    response = client.get("/api/accounts/00000000000")
    assert response.status_code == 404

def test_update_account(client):
    pesel = "88888888888"
    client.post("/api/accounts", json={"name": "Tomasz", "surname": "Błąd", "pesel": pesel})

    update_payload = {"surname": "Poprawny"}
    response = client.patch(f"/api/accounts/{pesel}", json=update_payload)
    
    assert response.status_code == 200
    
    get_response = client.get(f"/api/accounts/{pesel}")
    account_data = get_response.get_json()
    assert account_data["surname"] == "Poprawny"
    assert account_data["name"] == "Tomasz"

def test_delete_account(client):
    pesel = "77777777777"
    client.post("/api/accounts", json={"name": "Do", "surname": "Usunięcia", "pesel": pesel})
    assert registry.number_of_accounts() == 1

    response = client.delete(f"/api/accounts/{pesel}")
    assert response.status_code == 200

    get_response = client.get(f"/api/accounts/{pesel}")
    assert get_response.status_code == 404
    assert registry.number_of_accounts() == 0

def test_create_duplicate_account(client):
    registry.accounts = []
    payload = {"name": "Jan", "surname": "Nowak", "pesel": "12345678901"}
    
    client.post("/api/accounts", json=payload)
    
    response = client.post("/api/accounts", json=payload)
    assert response.status_code == 409
    assert response.get_json()["message"] == "Account with this pesel already exists"