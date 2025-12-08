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
    def IsLaon(self, loan):
        warunek1 = True
        warunek2 = False
        if len(self.transfers)>=3:
            trzy_ostatnie = self.transfers[-3:]
            for i in trzy_ostatnie:
                if i < 0:
                    warunek1 = False
                    break
            if len(self.transfers)>=5:
                piec_ostatnich = self.transfers[-5:]
                if sum(piec_ostatnich) >= loan:
                    warunek2 = True
        if warunek1 or warunek2:
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