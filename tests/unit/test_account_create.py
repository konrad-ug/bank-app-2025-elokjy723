import pytest
from src.account import Account, BusinessAccount


class TestAccount:
    def test_account_creation(self, sample_account):
        assert sample_account.first_name == "Jan"
        assert sample_account.last_name == "Kowalski"
        assert sample_account.balance == 0.0

    @pytest.mark.parametrize("pesel, expected", [("123456789", "invalid"),("12345678912314323453425", "invalid")])
    def test_account_creation_pesel(self, pesel, expected):
        account = Account("John", "Doe", pesel, expected)
        assert account.pesel == expected

    @pytest.mark.parametrize("code, pesel, expected", [("PROM_XYZ","12345678901",50),("SPROM_XYZ","12345678901",0),("PROM_XY","12345678901", 0),("SWER_XY","12345678901",0),("PROM_XYZ","61010100016",50),("PROM_XYZ","59010100013",0),("PROM_XYZ","60010100019",0)])
    def test_account_promo_code_valid(self, code,pesel, expected):
        account = Account("John", "Doe", pesel, code)
        assert account.balance == expected

    


class TestTransfers:
    def test_transfer_incoming(self, sample_account):
        sample_account.transfer_incoming(100)
        assert sample_account.balance == 100

    def test_transfer_outgoing_success(self, sample_account):
        sample_account.balance = 200
        result = sample_account.transfer_outgoing(100)
        assert result is True
        assert sample_account.balance == 100

    def test_transfer_outgoing_fail(self, sample_account):
        sample_account.balance = 50
        result = sample_account.transfer_outgoing(100)
        assert result is False
        assert sample_account.balance == 50


class TestExpressTransfer:
    def test_express_transfer_personal_success(self, sample_account):
        sample_account.balance = 100
        result = sample_account.express_transfer(50)
        assert result is True
        assert sample_account.balance == 49

    def test_express_transfer_personal_negative_limit(self, sample_account):
        sample_account.balance = 0
        result = sample_account.express_transfer(1)
        assert result is True
        assert sample_account.balance == -2

    def test_express_transfer_personal_fail(self, sample_account):
        sample_account.balance = 0
        result = sample_account.express_transfer(10)
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
    def test_transfer_history_plus(self, sample_account):
        sample_account.transfer_incoming(500)
        sample_account.transfer_outgoing(300)
        assert sample_account.transfers == [500, -300, -1]

    def test_transfer_history_minus(self, sample_account):
        sample_account.balance = 400
        sample_account.transfer_outgoing(300)
        sample_account.transfer_incoming(500)
        assert sample_account.transfers == [-300, -1, 500]

    def test_transfer_history_only_plus(self, sample_account):
        sample_account.transfer_incoming(500)
        assert sample_account.transfers == [500]

    def test_transfer_history_only_minus(self, sample_account):
        sample_account.balance = 400
        sample_account.transfer_outgoing(300)
        assert sample_account.transfers == [-300, -1]


class TestLoanCapability:
    def test_loan_capability_pos1(self, sample_account):
        sample_account.transfer_incoming(300)
        sample_account.transfer_incoming(300)
        sample_account.transfer_incoming(300)
        sample_account.submit_for_loan(1000)
        assert sample_account.balance == 1900

    def test_loan_capability_pos2(self, sample_account):
        for _ in range(7):
            sample_account.transfer_incoming(300)
        sample_account.submit_for_loan(1000)
        assert sample_account.balance == 3100

    def test_loan_capability_neg1(self, sample_account):
        sample_account.transfer_incoming(300)
        sample_account.transfer_incoming(300)
        sample_account.transfer_outgoing(300)
        sample_account.submit_for_loan(1000)
        assert sample_account.balance == 300

    def test_loan_capability_pos_5over(self, sample_account):
        for _ in range(5):
            sample_account.transfer_incoming(300)
        sample_account.transfer_outgoing(300)
        sample_account.submit_for_loan(200)
        assert sample_account.balance == 1400

    def test_loan_capability_neg_5over(self, sample_account):
        for _ in range(5):
            sample_account.transfer_incoming(300)
        sample_account.transfer_outgoing(300)
        sample_account.submit_for_loan(1400)
        assert sample_account.balance == 1200
