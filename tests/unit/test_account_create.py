import pytest
from src.account import Account, BusinessAccount


class TestAccount:
    @pytest.mark.parametrize("first,last,balance", [
        ("Jan", "Kowalski", 0.0)
    ])
    def test_account_creation(self, sample_account, first, last, balance):
        assert sample_account.first_name == first
        assert sample_account.last_name == last
        assert sample_account.balance == balance

    @pytest.mark.parametrize("pesel, promo, expected", [
        ("123456789", "PROM_ABC", "invalid"),
        ("12345678912314323453425", "PROM_ABC", "invalid"),
        ("12345678901", "PROM_ABC", "12345678901"),
    ])
    def test_account_creation_pesel(self, pesel, promo, expected):
        account = Account("John", "Doe", pesel, promo)
        assert account.pesel == expected

    @pytest.mark.parametrize("code, pesel, expected", [
        ("PROM_XYZ", "12345678901", 50),
        ("SPROM_XYZ", "12345678901", 0),
        ("PROM_XY", "12345678901", 0),
        ("SWER_XY", "12345678901", 0),
        ("PROM_XYZ", "61010100016", 50),
        ("PROM_XYZ", "59010100013", 0),
        ("PROM_XYZ", "60010100019", 0),
        ("PROM_XYZ", "00000000000", 0),
        (None, "12345678901", 0),
    ])
    def test_account_promo_code_valid(self, code, pesel, expected):
        account = Account("John", "Doe", pesel, code)
        assert account.balance == expected


class TestTransfers:
    @pytest.mark.parametrize("amount,balance,expected_balance,expected_transfers", [
        (100, 0, 100, [100]),
        (0, 0, 0, []),
    ])
    def test_transfer_incoming(self, sample_account, amount, balance, expected_balance, expected_transfers):
        sample_account.balance = balance
        sample_account.transfer_incoming(amount)
        assert sample_account.balance == expected_balance
        assert sample_account.transfers == expected_transfers

    @pytest.mark.parametrize("balance,amount,expected_result,expected_balance", [
        (200, 100, True, 100),
        (50, 100, False, 50),
    ])
    def test_transfer_outgoing(self, sample_account, balance, amount, expected_result, expected_balance):
        sample_account.balance = balance
        result = sample_account.transfer_outgoing(amount)
        assert result is expected_result
        assert sample_account.balance == expected_balance


class TestExpressTransfer:
    @pytest.mark.parametrize("start_balance,amount,expected_result,expected_end", [
        (100, 50, True, 49),
        (0, 1, True, -2),
        (0, 10, False, 0),
        (0, 0.5, True, -1.5),
    ])
    def test_express_transfer_personal(self, sample_account, start_balance, amount, expected_result, expected_end):
        sample_account.balance = start_balance
        result = sample_account.express_transfer(amount)
        assert result is expected_result
        assert sample_account.balance == expected_end


class TestBusinessAccount:
    @pytest.mark.parametrize("company,nip,expected_nip", [
        ("ABC", "1234567890", "1234567890"),
        ("ABC", "12", "Invalid"),
    ])
    def test_business_account_creation(self, company, nip, expected_nip):
        biz = BusinessAccount(company, nip)
        assert biz.company_name == company
        assert biz.nip == expected_nip

    @pytest.mark.parametrize("start_balance,amount,expected_result,expected_end", [
        (100, 50, True, 45),
        (0, 1, True, -6),
        (0, 10, False, 0),
        (0, 0.5, True, -5.5),
    ])
    def test_business_express_transfer(self, start_balance, amount, expected_result, expected_end):
        biz = BusinessAccount("ABC", "1234567890")
        biz.balance = start_balance
        result = biz.express_transfer(amount)
        assert result is expected_result
        assert biz.balance == expected_end


class TestHistoryTransfer:
    @pytest.mark.parametrize("ops,expected", [
        (["+500", "-300"], [500, -300, -1]),
        (["-300", "+500"], [-300, -1, 500]),
        (["+500"], [500]),
        (["-300"], [-300, -1]),
    ])
    def test_transfer_history(self, sample_account, ops, expected):
        for op in ops:
            if op.startswith("+"):
                sample_account.transfer_incoming(int(op[1:]))
            else:
                sample_account.balance = max(sample_account.balance, int(op[1:]))
                sample_account.transfer_outgoing(int(op[1:]))
        assert sample_account.transfers == expected


class TestLoanCapability:
    @pytest.mark.parametrize("transfers,loan,expected_balance", [
        ([300,300,300], 1000, 1900),
        ([300]*7, 1000, 3100),
    ])
    def test_loan_capability_pos(self, sample_account, transfers, loan, expected_balance):
        for t in transfers:
            sample_account.transfer_incoming(t)
        sample_account.submit_for_loan(loan)
        assert sample_account.balance == expected_balance

    @pytest.mark.parametrize("ops,loan,expected_balance", [
        (["+300","+300","-300"], 1000, 300),
        (["+300"]*5 + ["-300"], 200, 1400),
        (["+300"]*5 + ["-300"], 1400, 1200),
    ])
    def test_loan_capability_mixed(self, sample_account, ops, loan, expected_balance):
        for op in ops:
            amount = int(op[1:])
            if op.startswith("+"):
                sample_account.transfer_incoming(amount)
            else:
                sample_account.balance += amount + 1000
                sample_account.transfer_outgoing(amount)
        sample_account.submit_for_loan(loan)
        assert sample_account.balance == expected_balance

    @pytest.mark.parametrize("transfers,loan,expected", [
        ([100], 500, False),
    ])
    def test_condition2_short_history(self, sample_account, transfers, loan, expected):
        for t in transfers:
            sample_account.transfer_incoming(t)
        assert sample_account.condition2(loan) is expected

    @pytest.mark.parametrize("transfers,expected", [
        ([100], None),
    ])
    def test_condition1_none_case(self, sample_account, transfers, expected):
        for t in transfers:
            sample_account.transfer_incoming(t)
        assert sample_account.condition1() is expected


class TestBussinessLoan:
    @pytest.mark.parametrize("start_balance,transfer,loan,expected", [
        (10000, 1775, 200, 8420),
        (10000, None, 200, 10000),
        (10000, 1775, 6000, 8220),
        (10000, 1000, 200, 10000),
    ])
    def test_business_loan(self, sample_bussiness_account, start_balance, transfer, loan, expected):
        sample_bussiness_account.balance = start_balance
        if transfer is not None:
            sample_bussiness_account.express_transfer(transfer)
        sample_bussiness_account.take_loan(loan)
        assert sample_bussiness_account.balance == expected
