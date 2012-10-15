"""stock module contains classes to manipulate data related to stocks"""

class Stock:
    def __init__(self, c):
        self.__code = c

    # code attribute
    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, c):
        self.__code = c

    # real attributes
    @property
    def pe(self):
        return self.__pe

    @pe.setter
    def pe(self, v):
        self.__pe = v

    @property
    def roe(self):
        return self.__roe

    @roe.setter
    def roe(self, v):
        self.__roe = v

    # order attributes
    @property
    def pe_order(self):
        return self.__pe_order

    @pe_order.setter
    def pe_order(self, v):
        self.__pe_order = v

    @property
    def roe_order(self):
        return self.__roe_order

    @roe_order.setter
    def roe_order(self, v):
        self.__roe_order = v

    @property
    def greenblatt_order(self):
        return self.__greenblatt_order

    @greenblatt_order.setter
    def greenblatt_order(self, v):
        self.__greenblatt_order = v

