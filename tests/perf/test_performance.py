import requests
import pytest

BASE_URL = "http://127.0.0.1:5000/api"

def test_perf_create_delete_account():
    
    for i in range(100):
        pesel = f"90000000{i:03d}"
        payload = {"name": "Perf", "surname": "Test", "pesel": pesel}
        
        response = requests.post(f"{BASE_URL}/accounts", json=payload, timeout=0.5)
        assert response.status_code == 201
        
        response = requests.delete(f"{BASE_URL}/accounts/{pesel}", timeout=0.5)
        assert response.status_code == 200

def test_perf_transfers():
    pesel = "88888888888"
    payload = {"name": "Transfer", "surname": "Test", "pesel": pesel}
    
    requests.delete(f"{BASE_URL}/accounts/{pesel}")
    requests.post(f"{BASE_URL}/accounts", json=payload)
    
    transfer_payload = {"amount": 10, "type": "incoming"}
    
    for _ in range(100):
        response = requests.post(f"{BASE_URL}/accounts/{pesel}/transfer", json=transfer_payload, timeout=0.5)
        assert response.status_code == 200

    response = requests.get(f"{BASE_URL}/accounts/{pesel}")
    assert response.status_code == 200
    assert response.json()['balance'] == 1000
    
    requests.delete(f"{BASE_URL}/accounts/{pesel}")