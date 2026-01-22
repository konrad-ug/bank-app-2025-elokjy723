import pytest
from unittest.mock import Mock, MagicMock, patch
from src.account import Account
from src.accounts_repository import MongoAccountsRepository

class TestMongoRepository:
    @patch('src.accounts_repository.MongoClient')
    def test_save_all(self, mock_mongo_client):
        mock_collection = Mock()
        
        mock_db = MagicMock()
        mock_db.__getitem__.return_value = mock_collection
        
        mock_client_instance = MagicMock()
        mock_client_instance.__getitem__.return_value = mock_db
        
        mock_mongo_client.return_value = mock_client_instance

        repo = MongoAccountsRepository()
        
        acc1 = Account("Jan", "Kowalski", "12345678901")
        acc2 = Account("Anna", "Nowak", "98765432109")
        accounts = [acc1, acc2]

        repo.save_all(accounts)

        mock_collection.delete_many.assert_called_once_with({})
        
        assert mock_collection.insert_one.call_count == 2

    @patch('src.accounts_repository.MongoClient')
    def test_load_all(self, mock_mongo_client):
        mock_collection = Mock()
        
        fake_data = [
            {
                "first_name": "Jan", "last_name": "Kowalski", "pesel": "12345678901",
                "balance": 100.0, "transfers": [100], "promo_code": None, "type": "personal"
            }
        ]
        mock_collection.find.return_value = fake_data
        
        mock_db = MagicMock()
        mock_db.__getitem__.return_value = mock_collection
        
        mock_client_instance = MagicMock()
        mock_client_instance.__getitem__.return_value = mock_db
        
        mock_mongo_client.return_value = mock_client_instance

        repo = MongoAccountsRepository()
        
        loaded = repo.load_all()

        assert len(loaded) == 1
        assert loaded[0].first_name == "Jan"
        assert loaded[0].balance == 100.0