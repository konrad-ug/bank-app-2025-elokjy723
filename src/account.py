class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None, transfers=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        self.pesel = pesel
        self.promo_code = promo_code
        self.transfers = []
        if self.is_pesel_valid(pesel):
            self.pesel = pesel
        else:
            self.pesel = "invalid"
        if self.validate_code(promo_code) and not self.validate_year_birth(promo_code):
            self.balance += 50
    
    def condition1(self):
        if len(self.transfers)>=3:
            trzy_ostatnie = self.transfers[-3:]
            for i in trzy_ostatnie:
                if i < 0:
                    return False
            return True
    def condition2(self, loan):
        if len(self.transfers)>=5:
            piec_ostatnich = self.transfers[-5:]
            if sum(piec_ostatnich) >= loan:
                return True
        return False

    def submit_for_loan(self, loan):
        if self.condition1() or self.condition2(loan):
            self.balance += loan
            return True
        else:
            return False
    def transfer_incoming(self, amount):
        if amount > 0:
            self.balance += amount
            self.transfers.append(amount)
    def transfer_outgoing(self, amount):
        fee = -1
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.transfers.append(-amount)
            self.transfers.append(fee)

            return True
        return False
    def express_transfer(self, amount):
        fee = 1
        total = amount + fee
        if amount > 0 and self.balance + fee >= total:
            self.balance -= total
            return True
        elif amount > 0 and self.balance >= amount - fee:
            self.balance -= total
            return True
        return False
    def is_pesel_valid(self, pesel):
        return isinstance(pesel, str) and len(pesel) == 11
    def validate_code(self, promo_code):
        return isinstance(promo_code, str) and promo_code.startswith("PROM_") and len(promo_code) == 8
    def validate_year_birth(self, promo_code):
        year_birth = int(self.pesel[0:2])
        stulecie = int(self.pesel[2:4])
        return year_birth <= 60 and 1 <= stulecie <= 12
class BusinessAccount(Account):
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip
        self.balance = 0.0
        self.transfers=[]
        if not (isinstance(nip, str) and len(nip) == 10 and nip.isdigit()):
            self.nip = "Invalid"

    def express_transfer(self, amount):
        fee = 5
        total = amount + fee
        if amount > 0 and self.balance + fee >= total:
            self.balance -= total
            self.transfers.append(-1*amount)
            self.transfers.append(-1*fee)
            return True
        elif amount > 0 and self.balance >= amount - fee:
            self.balance -= total
            self.transfers.append(-1*amount)
            self.transfers.append(-1*fee)
            return True
        return False
    
    def take_loan(self, amount):
        warunek1 = False
        warunek2 = False
        if self.balance >= (2*amount):
            warunek1 = True
        else:
            return False
        for transfer in self.transfers:
            if transfer == -1775:
                warunek2 = True
        if warunek2 and warunek1:
            self.balance += amount
            return True
        return False

class AccountRegistry:
    def __init__(self):
        self.accounts = []
    
    def add_account(self, account: Account):
        if self.search_account_pesel(account.pesel):
            return False
            
        if account.pesel != "invalid":
            self.accounts.append(account)
            return True
        return False

    def search_account_pesel(self, pesel):
        for acc in self.accounts:
            if acc.pesel == pesel:
                return acc
    
    def all_accounts(self):
        return self.accounts
    
    def number_of_accounts(self):
        return len(self.accounts)
            