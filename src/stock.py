"""stock module contains classes to manipulate data related to stocks"""

class Stock:
    def __init__(self, c):
        self.__code = c

    # code attribute
    def get_code(self):
        return self.__code

    def set_code(self, c):
        self.__code = c

    # real attributes
    def get_pe(self):
        return self.__pe

    def set_pe(self, v):
        self.__pe = v

    def get_roe(self):
        return self.__roe

    def set_roe(self, v):
        self.__roe = v

    # order attributes
    def get_pe_order(self):
        return self.__pe_order

    def set_pe_order(self, v):
        self.__pe_order = v

    def get_roe_order(self):
        return self.__roe_order

    def set_roe_order(self, v):
        self.__roe_order = v

    def get_greenblatt_order(self):
        return self.__greenblatt_order

    def set_greenblatt_order(self, v):
        self.__greenblatt_order = v

