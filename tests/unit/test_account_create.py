from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0

    def test_account_creation_pesel_short(self):
        account = Account("John", "Doe", "123456789")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "invalid"
    def test_account_creation_pesel_long(self):
        account = Account("John", "Doe", "12345678912314323453425")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "invalid"
    def test_account_promo_code(self):
        account = Account("John", "Doe", "12345678901","PROM_XYZ")
        assert account.balance == 50
    def test_account_promo_code(self):
        account = Account("John", "Doe", "12345678901","SPROM_XYZ")
        assert account.balance == 0
    def test_account_promo_code(self):
        account = Account("John", "Doe", "12345678901","PROM_XY")
        assert account.balance == 0
    def test_account_promo_code(self):
        account = Account("John", "Doe", "12345678901","SWER_XY")
        assert account.balance == 0
    def test_account_promo_code_year_more(self):
        account = Account("John", "Doe", "61010100016","PROM_XYZ")
        assert account.balance == 50
    def test_account_promo_code_year_less(self):
        account = Account("John", "Doe", "59010100013","PROM_XYZ")
        assert account.balance == 0
    def test_account_promo_code_year_equal(self):
        account = Account("John", "Doe", "60010100019","PROM_XYZ")
        assert account.balance == 0