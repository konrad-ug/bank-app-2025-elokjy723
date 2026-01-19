import pytest
from src.account import Account, BusinessAccount, AccountRegistry

class TestAccount:
    def test_account_creation(self, sample_account):
        assert sample_account.first_name == "Jan"
        assert sample_account.last_name == "Kowalski"
        assert sample_account.balance == 0.0

    @pytest.mark.parametrize("pesel,promo,expected", [
        ("123456789", "INVALID", "invalid"),
        ("12345678912314323453425", "INVALID", "invalid"),
        ("12345678901", "INVALID", "12345678901"),
    ])
    def test_account_creation_pesel(self, pesel, promo, expected):
        account = Account("John", "Doe", pesel, promo)
        assert account.pesel == expected

    @pytest.mark.parametrize("code,pesel,expected", [
        ("PROM_XYZ", "12345678901", 50),
        ("SPROM_XYZ", "12345678901", 0),
        ("PROM_XY", "12345678901", 0),
        ("SWER_XY", "12345678901", 0),
        ("PROM_XYZ", "61010100016", 50),
        ("PROM_XYZ", "59010100013", 0),
        ("PROM_XYZ", "60010100019", 0),
        ("PROM_XYZ", "00000000000", 50),
        (None, "12345678901", 0),
    ])
    def test_account_promo_code_valid(self, code, pesel, expected):
        account = Account("John", "Doe", pesel, code)
        assert account.balance == expected


class TestTransfers:
    @pytest.mark.parametrize("start_balance,amount,expected_balance,expected_transfers", [
        (0, 100, 100, [100]),
        (0, 0, 0, []),
        (0, -50, 0, []),
    ])
    def test_transfer_incoming(self, sample_account, start_balance, amount, expected_balance, expected_transfers):
        sample_account.balance = start_balance
        sample_account.transfer_incoming(amount)
        assert sample_account.balance == expected_balance
        assert sample_account.transfers == expected_transfers

    @pytest.mark.parametrize("start_balance,amount,expected_result,expected_balance,expected_transfers", [
        (200, 100, True, 100, [-100, -1]),
        (50, 100, False, 50, []),
        (0, 0, False, 0, []),
    ])
    def test_transfer_outgoing(self, sample_account, start_balance, amount, expected_result, expected_balance, expected_transfers):
        sample_account.balance = start_balance
        result = sample_account.transfer_outgoing(amount)
        assert result is expected_result
        assert sample_account.balance == expected_balance
        assert sample_account.transfers == expected_transfers


class TestExpressTransfer:
    @pytest.mark.parametrize("start_balance,amount,expected_result,expected_balance", [
        (100, 50, True, 49),
        (0, 1, True, -2),
        (0, 10, False, 0),
        (0, 0.5, True, -1.5),
    ])
    def test_express_transfer_personal(self, sample_account, start_balance, amount, expected_result, expected_balance):
        sample_account.balance = start_balance
        result = sample_account.express_transfer(amount)
        assert result is expected_result
        assert sample_account.balance == expected_balance


class TestBusinessAccount:

    @pytest.mark.parametrize("start_balance,amount,expected_result,expected_balance", [
        (100, 50, True, 45),
        (0, 1, True, -6),
        (0, 10, False, 0),
    ])
    def test_business_express_transfer(self, sample_bussiness_account, start_balance, amount, expected_result, expected_balance):
        biz = sample_bussiness_account
        biz.balance = start_balance
        result = biz.express_transfer(amount)
        assert result is expected_result
        assert biz.balance == expected_balance


class TestHistoryTransfer:
    @pytest.mark.parametrize("ops,expected", [
        (["+500", "-300"], [500, -300, -1]),
        (["-300", "+500"], [-300, -1, 500]),
        (["+500"], [500]),
        (["-300"], [-300, -1]),
    ])
    def test_transfer_history(self, sample_account, ops, expected):
        for op in ops:
            amount = int(op[1:])
            if op.startswith("+"):
                sample_account.transfer_incoming(amount)
            else:
                sample_account.balance = max(sample_account.balance, amount)
                sample_account.transfer_outgoing(amount)
        assert sample_account.transfers == expected


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

    def test_condition1_none_case(self, sample_account):
        sample_account.transfer_incoming(100)
        assert sample_account.condition1() is None

    def test_condition2_short_history(self, sample_account):
        sample_account.transfer_incoming(100)
        assert sample_account.condition2(500) is False


class TestBussinessLoan:
    def test_loan_bussiness_pos(self, sample_bussiness_account):
        sample_bussiness_account.balance = 10000
        sample_bussiness_account.express_transfer(1775)
        sample_bussiness_account.take_loan(200)
        assert sample_bussiness_account.balance == 8420

    def test_loan_bussiness_withoutZUS(self, sample_bussiness_account):
        sample_bussiness_account.balance = 10000
        sample_bussiness_account.take_loan(200)
        assert sample_bussiness_account.balance == 10000

    def test_loan_bussiness_without2timesmore(self, sample_bussiness_account):
        sample_bussiness_account.balance = 10000
        sample_bussiness_account.express_transfer(1775)
        sample_bussiness_account.take_loan(6000)
        assert sample_bussiness_account.balance == 8220

    def test_loan_bussiness_other_transfer_no_loan(self, sample_bussiness_account):
        sample_bussiness_account.balance = 10000
        sample_bussiness_account.express_transfer(1000)
        sample_bussiness_account.take_loan(200)
        assert sample_bussiness_account.balance == 8995


class TestAccountRegister:
    
    def test_account_register(self,sample_account):
        reg = AccountRegistry()
        assert reg.add_account(sample_account) is True
        assert reg.number_of_accounts() == 1
        assert reg.all_accounts() == [sample_account]
        assert reg.search_account_pesel("12345678901") == sample_account

    def test_account_register_neg(self):
        reg = AccountRegistry()
        acc1 = Account("Jan", "Kowalski", "213131241242354")
        assert reg.add_account(acc1) is False
        assert reg.number_of_accounts() == 0
    
    def test_registry_add_duplicate(self, sample_account):
        registry = AccountRegistry()
        assert registry.add_account(sample_account) is True
        assert registry.add_account(sample_account) is False
        assert registry.number_of_accounts() == 1