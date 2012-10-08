"""stock module contains classes to manipulate data related to stocks"""

class Stock:
    def __init__(self, c):
        self.code = c

    def get_code(self):
        return self.code

    def set_code(self, c):
        self.code = c

    def get_pe(self):
        return self.pe

    def set_pe(self, v):
        self.pe = v

    def get_pe_order(self):
        return self.pe_order

    def set_pe_order(self, v):
        self.pe_order = v
