"""stock module: contains the Stock class."""

class Stock:
    """Stock class contains attributes to handle stock specific data,
    such as stock instances, sorting methods, etc.

    """

    #
    # class methods
    #

    # sort from low to high
    @classmethod
    def sort_pe(cls, sector):
        """Sort stocks based on P/E and assign order as an instance
        attribute for each stock.

        |      pe           |
        | pe_ok | pe_rotten |
        0------->----------->
                +           -

        """

        pe_ok = []
        pe_rotten = []

        for s in sector:
            if s.pe >= 0:
                pe_ok.append(s)
            else:
                pe_rotten.append(s)

        pe_ok.sort(key=lambda s: s.pe)
        pe_rotten.sort(key=lambda s: s.pe, reverse=True)
        pe = pe_ok + pe_rotten

        for i, s in enumerate(pe, start=1):
            s.pe_order = i

    # sort from high to low
    @classmethod
    def sort_roe(cls, sector):
        """Sort stocks based on ROE and assign order as an instance
        attribute for each stock.

        |       roe           |
        | roe_ok | roe_rotten |
        <--------0------------>
        +                     -

        """

        roe_ok = []
        roe_rotten = []

        for s in sector:
            if s.roe >= 0:
                roe_ok.append(s)
            else:
                roe_rotten.append(s)

        roe_ok.sort(key=lambda s: s.roe, reverse=True)
        roe_rotten.sort(key=lambda s: s.roe, reverse=True)
        roe = roe_ok + roe_rotten

        for i, s in enumerate(roe, start=1):
            s.roe_order = i

    # sort from low to high
    @classmethod
    def sort_greenblatt(cls, sector):
        """Sort stocks based on Greenblatt order, which, by itself, is
        based on P/E and ROE orders, and assign order as an instance
        attribute for each stock.

        | greenblatt |
        0------------>
                     +

        """

        for s in sector:
            s.greenblatt_order = s.pe_order + s.roe_order

        sector.sort(key=lambda s: s.greenblatt_order)

    #
    # instance methods
    #

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

