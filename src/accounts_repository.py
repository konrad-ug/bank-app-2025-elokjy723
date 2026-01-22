from pymongo import MongoClient
from src.account import Account, BusinessAccount

class MongoAccountsRepository:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['bank_db']
        self.collection = self.db['accounts']

    def save_all(self, accounts):
        self.collection.delete_many({})
        
        for account in accounts:
            self.collection.insert_one(account.to_dict())

    def load_all(self):
        accounts = []
        for data in self.collection.find():
            if data.get("type") == "personal":
                acc = Account(data["first_name"], data["last_name"], data["pesel"], data["promo_code"])
                acc.balance = data["balance"]
                acc.transfers = data["transfers"]
                accounts.append(acc)
            elif data.get("type") == "business":
                try:
                    acc = BusinessAccount(data["company_name"], data["nip"])
                    acc.balance = data["balance"]
                    acc.transfers = data["transfers"]
                    accounts.append(acc)
                except ValueError:
                    pass
                    
        return accounts