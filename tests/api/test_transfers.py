import pytest
from app.api import app, registry
from src.account import Account

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        registry.accounts = []
        yield client

def create_account_with_balance(client, pesel, balance):
    acc = Account("Test", "User", pesel)
    acc.balance = balance
    registry.add_account(acc)

def test_transfer_incoming(client):
    pesel = "11111111111"
    create_account_with_balance(client, pesel, 0)
    
    payload = {"amount": 100, "type": "incoming"}
    response = client.post(f"/api/accounts/{pesel}/transfer", json=payload)
    
    assert response.status_code == 200
    account = registry.search_account_pesel(pesel)
    assert account.balance == 100

def test_transfer_outgoing_success(client):
    pesel = "22222222222"
    create_account_with_balance(client, pesel, 200)
    
    payload = {"amount": 100, "type": "outgoing"}
    response = client.post(f"/api/accounts/{pesel}/transfer", json=payload)
    
    assert response.status_code == 200
    account = registry.search_account_pesel(pesel)
    assert account.balance == 100

def test_transfer_outgoing_failure(client):
    pesel = "33333333333"
    create_account_with_balance(client, pesel, 50)
    
    payload = {"amount": 100, "type": "outgoing"}
    response = client.post(f"/api/accounts/{pesel}/transfer", json=payload)
    
    assert response.status_code == 422
    account = registry.search_account_pesel(pesel)
    assert account.balance == 50

def test_transfer_account_not_found(client):
    payload = {"amount": 100, "type": "incoming"}
    response = client.post("/api/accounts/00000000000/transfer", json=payload)
    
    assert response.status_code == 404

def test_transfer_invalid_type(client):
    pesel = "44444444444"
    create_account_with_balance(client, pesel, 100)
    
    payload = {"amount": 50, "type": "invalid"}
    response = client.post(f"/api/accounts/{pesel}/transfer", json=payload)
    
    assert response.status_code == 400