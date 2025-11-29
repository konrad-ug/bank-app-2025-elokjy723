from src.account import Account, BusinessAccount

class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0

    def test_account_creation_pesel_short(self):
        account = Account("John", "Doe", "123456789")
        assert account.pesel == "invalid"

    def test_account_creation_pesel_long(self):
        account = Account("John", "Doe", "12345678912314323453425")
        assert account.pesel == "invalid"

    def test_account_promo_code_valid(self):
        account = Account("John", "Doe", "12345678901", "PROM_XYZ")
        assert account.balance == 50

    def test_account_promo_code_invalid_prefix(self):
        account = Account("John", "Doe", "12345678901", "SPROM_XYZ")
        assert account.balance == 0

    def test_account_promo_code_invalid_length(self):
        account = Account("John", "Doe", "12345678901", "PROM_XY")
        assert account.balance == 0

    def test_account_promo_code_invalid_format(self):
        account = Account("John", "Doe", "12345678901", "SWER_XY")
        assert account.balance == 0

    def test_account_promo_code_year_more(self):
        account = Account("John", "Doe", "61010100016", "PROM_XYZ")
        assert account.balance == 50

    def test_account_promo_code_year_less(self):
        account = Account("John", "Doe", "59010100013", "PROM_XYZ")
        assert account.balance == 0

    def test_account_promo_code_year_equal(self):
        account = Account("John", "Doe", "60010100019", "PROM_XYZ")
        assert account.balance == 0


class TestTransfers:
    def test_transfer_incoming(self):
        account = Account("Alice", "Johnson", "12345678901")
        account.transfer_incoming(100)
        assert account.balance == 100

    def test_transfer_outgoing_success(self):
        account = Account("Alice", "Johnson", "12345678901")
        account.balance = 200
        result = account.transfer_outgoing(100)
        assert result is True
        assert account.balance == 100

    def test_transfer_outgoing_fail(self):
        account = Account("Alice", "Johnson", "12345678901")
        account.balance = 50
        result = account.transfer_outgoing(100)
        assert result is False
        assert account.balance == 50


class TestExpressTransfer:
    def test_express_transfer_personal_success(self):
        account = Account("Jan", "Kowalski", "12345678901")
        account.balance = 100
        result = account.express_transfer(50)
        assert result is True
        assert account.balance == 49

    def test_express_transfer_personal_negative_limit(self):
        account = Account("Jan", "Kowalski", "12345678901")
        account.balance = 0
        result = account.express_transfer(1)
        assert result is True
        assert account.balance == -2

    def test_express_transfer_personal_fail(self):
        account = Account("Jan", "Kowalski", "12345678901")
        account.balance = 0
        result = account.express_transfer(10)
        assert result is False


class TestBusinessAccount:
    def test_business_account_creation_valid_nip(self):
        biz = BusinessAccount("ABC", "1234567890")
        assert biz.company_name == "ABC"
        assert biz.nip == "1234567890"
        assert biz.balance == 0.0

    def test_business_account_invalid_nip(self):
        biz = BusinessAccount("ABC", "12")
        assert biz.nip == "Invalid"

    def test_business_express_transfer_success(self):
        biz = BusinessAccount("ABC", "1234567890")
        biz.balance = 100
        result = biz.express_transfer(50)
        assert result is True
        assert biz.balance == 45

    def test_business_express_transfer_negative_limit(self):
        biz = BusinessAccount("ABC", "1234567890")
        biz.balance = 0
        result = biz.express_transfer(1)
        assert result is True
        assert biz.balance == -6

    def test_business_express_transfer_fail(self):
        biz = BusinessAccount("ABC", "1234567890")
        biz.balance = 0
        result = biz.express_transfer(10)
        assert result is False
class TestHistoryTransfer:
    def test_transfer_history_plus(self):
        account = Account("Jan", "Kowalski", "12345673242",[])
        account.transfer_incoming(500)
        account.transfer_outgoing(300)
        assert account.transfers == [500, -300, -1]
    def test_transfer_history_minus(self):
        account = Account("Jan", "Kowalski", "12345673242",[])
        account.balance = 400
        account.transfer_outgoing(300)
        account.transfer_incoming(500)
        assert account.transfers == [-300, -1, 500]
    def test_transfer_history_only_plus(self):
        account = Account("Jan", "Kowalski", "12345673242",[])
        account.transfer_incoming(500)
        assert account.transfers == [500]
    def test_transfer_history_only_minus(self):
        account = Account("Jan", "Kowalski", "12345673242",[])
        account.balance = 400
        account.transfer_outgoing(300)
        assert account.transfers == [-300, -1]