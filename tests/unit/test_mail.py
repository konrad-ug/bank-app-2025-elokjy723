import pytest
from unittest.mock import patch
from src.account import Account, BusinessAccount
import datetime

class TestMail:
    def test_send_email_personal_account_success(self):
        account = Account("Jan", "Kowalski", "12345678901")
        account.transfer_incoming(100) 
        account.transfer_outgoing(50)
        email = "jan@test.pl"

        with patch('src.account.SMTPClient') as MockSMTP:
            mock_smtp_instance = MockSMTP.return_value
            mock_smtp_instance.send.return_value = True

            result = account.send_history_via_email(email)

            assert result is True
            
            today = datetime.date.today().strftime("%Y-%m-%d")
            expected_subject = f"Account Transfer History {today}"
            expected_text = f"Personal account history: [100, -50, -1]"
            
            mock_smtp_instance.send.assert_called_once_with(expected_subject, expected_text, email)

    def test_send_email_personal_account_failure(self):
        account = Account("Jan", "Kowalski", "12345678901")
        email = "fail@test.pl"

        with patch('src.account.SMTPClient') as MockSMTP:
            mock_smtp_instance = MockSMTP.return_value
            mock_smtp_instance.send.return_value = False

            result = account.send_history_via_email(email)
            assert result is False

    @patch('src.account.requests.get')
    def test_send_email_business_account(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {"subject": {"statusVat": "Czynny"}}
        }

        biz = BusinessAccount("Firma", "1234567890")
        biz.balance = 1000 
        biz.express_transfer(100)
        email = "ceo@firma.pl"

        with patch('src.account.SMTPClient') as MockSMTP:
            mock_smtp_instance = MockSMTP.return_value
            mock_smtp_instance.send.return_value = True

            result = biz.send_history_via_email(email)

            assert result is True
            
            today = datetime.date.today().strftime("%Y-%m-%d")
            expected_subject = f"Account Transfer History {today}"
            expected_text = f"Company account history: [-100, -5]"
            
            mock_smtp_instance.send.assert_called_once_with(expected_subject, expected_text, email)