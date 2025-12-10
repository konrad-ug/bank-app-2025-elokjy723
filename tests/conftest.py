import pytest
from src.account import Account

@pytest.fixture
def sample_account():
    return Account("Jan", "Kowalski", "12345673242")