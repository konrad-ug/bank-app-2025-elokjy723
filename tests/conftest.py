import pytest
from unittest.mock import patch
from src.account import Account, BusinessAccount

@pytest.fixture
def sample_account():
    return Account("Jan", "Kowalski", "12345678901")

@pytest.fixture
def sample_bussiness_account():
    with patch('src.account.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Czynny"
                }
            }
        }
        yield BusinessAccount("ABC", "1234567890")