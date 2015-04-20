# Stock class

class Stock:
    #def __init__(self, c):
    #    self.code = c

    ######## P/E and ROE class methods #######
    # sort from low to high
    @classmethod
    def sort_pe(cls, sector):
        # |      pe           |
        # | pe_ok | pe_rotten |
        # 0------->----------->
        #         +           -

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
        # |       roe           |
        # | roe_ok | roe_rotten |
        # <--------0------------>
        # +                     -

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
    def sort_gb_peroe(cls, sector):
        # | greenblatt |
        # 0------------>
        #              +

        for s in sector:
            s.greenblatt_order = s.pe_order + s.roe_order

        sector.sort(key=lambda s: s.greenblatt_order)

    ######## EY and ROC class methods #######
    # ey
    @classmethod
    def sort_ey(cls, sector):
        ey = []

        for s in sector:
            ey.append(s)

        ey.sort(key=lambda s: s.ey, reverse=True)

        for i, s in enumerate(ey, start=1):
            s.ey_order = i

    # roc
    @classmethod
    def sort_roc(cls, sector):
        roc = []

        for s in sector:
            roc.append(s)

        roc.sort(key=lambda s: s.roc, reverse=True)

        for i, s in enumerate(roc, start=1):
            s.roc_order = i

    # sort greenblatt
    @classmethod
    def sort_gb_eyroc(cls, sector):
        gb_order = []

        for s in sector:
            s.gb_order = s.ey_order + s.roc_order

        sector.sort(key=lambda s: s.gb_order)
