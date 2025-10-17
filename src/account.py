class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        self.pesel = pesel
        self.promo_code = promo_code
        print(self.promo_code)
        if self.is_pesel_valid(pesel):
            self.pesel = pesel
        else:
            self.pesel = "invalid"
        if self.validate_code(promo_code) and self.validate_year_birth(promo_code) != True:
            self.balance += 50

    def is_pesel_valid(self, pesel):
        if isinstance(pesel, str) and len(pesel) == 11:
            return True
    def validate_code(self, promo_code):
        if isinstance(promo_code, str) and promo_code.startswith("PROM_") and len(promo_code) == 8:
            return True
    def validate_year_birth(self, promo_code):
        year_birth = self.pesel[0] + self.pesel[1]
        stulecie = self.pesel[2] + self.pesel[3]
        print(year_birth, stulecie)
        if(int(year_birth) <= 60 and int(stulecie) >= 1 and int(stulecie) <= 12):
            return True