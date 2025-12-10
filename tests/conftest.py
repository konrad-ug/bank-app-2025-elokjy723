import pytest
from src.account import Account, BusinessAccount

@pytest.fixture
def sample_account():
    return Account("Jan", "Kowalski", "12345673242")

@pytest.fixture
def sample_bussiness_account():
    return BusinessAccount("ABC", "1234567890")