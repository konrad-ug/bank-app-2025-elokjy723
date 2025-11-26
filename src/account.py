class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        self.pesel = pesel
        self.promo_code = promo_code
        if self.is_pesel_valid(pesel):
            self.pesel = pesel
        else:
            self.pesel = "invalid"
        if self.validate_code(promo_code) and not self.validate_year_birth(promo_code):
            self.balance += 50

    def transfer_incoming(self, amount):
        if amount > 0:
            self.balance += amount

    def transfer_outgoing(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
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
        if not (isinstance(nip, str) and len(nip) == 10 and nip.isdigit()):
            self.nip = "Invalid"

    def express_transfer(self, amount):
        fee = 5
        total = amount + fee
        if amount > 0 and self.balance + fee >= total:
            self.balance -= total
            return True
        elif amount > 0 and self.balance >= amount - fee:
            self.balance -= total
            return True
        return False
