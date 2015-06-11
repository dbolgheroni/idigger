# declare a mapping and the models used

from __future__ import print_function

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, String, Float, Integer

Base = declarative_base()


class Stock(Base):
    __tablename__ = 'stocks'
    date = Column(Date, primary_key = True)
    code = Column(String, primary_key = True)
    ey = Column(Float)
    roc = Column(Float)
    pe = Column(Float)
    roe = Column(Float)
    pc = Column(Float)

    ey_order = Column(Integer)
    roc_order = Column(Integer)
    gb_eyroc_order = Column(Integer)

    pe_order = Column(Integer)
    roe_order = Column(Integer)
    gb_peroe_order = Column(Integer)

    sector = []
    @classmethod
    def add(cls, self):
        cls.sector.append(self)

    def __repr__(self):
        return '<Stock %r>' % (self.code)

    ######## P/E and ROE class methods #######
    # sort from low to high
    @classmethod
    def sort_pe(cls):
        # |      pe           |
        # | pe_ok | pe_rotten |
        # 0------->----------->
        #         +           -

        pe_ok = []
        pe_rotten = []

        for s in cls.sector:
            if s._pe >= 0:
                pe_ok.append(s)
            else:
                pe_rotten.append(s)

        pe_ok.sort(key=lambda s: s._pe)
        pe_rotten.sort(key=lambda s: s._pe, reverse=True)
        pe = pe_ok + pe_rotten

        for i, s in enumerate(pe, start=1):
            s.pe_order = i

    # sort from high to low
    @classmethod
    def sort_roe(cls):
        # |       roe           |
        # | roe_ok | roe_rotten |
        # <--------0------------>
        # +                     -

        roe_ok = []
        roe_rotten = []

        for s in cls.sector:
            if s._roe >= 0:
                roe_ok.append(s)
            else:
                roe_rotten.append(s)

        roe_ok.sort(key=lambda s: s._roe, reverse=True)
        roe_rotten.sort(key=lambda s: s._roe, reverse=True)
        roe = roe_ok + roe_rotten

        for i, s in enumerate(roe, start=1):
            s.roe_order = i

    # sort from low to high
    @classmethod
    def sort_gb_peroe(cls):
        # | greenblatt |
        # 0------------>
        #              +

        for s in cls.sector:
            s.gb_peroe_order = s.pe_order + s.roe_order

        cls.sector.sort(key=lambda s: s.gb_peroe_order)

    ######## EY and ROC class methods #######
    # ey
    @classmethod
    def sort_ey(cls):
        ey = []

        for s in cls.sector:
            ey.append(s)

        ey.sort(key=lambda s: s._ey, reverse=True)

        for i, s in enumerate(ey, start=1):
            s.ey_order = i

    # roc
    @classmethod
    def sort_roc(cls):
        roc = []

        for s in cls.sector:
            roc.append(s)

        roc.sort(key=lambda s: s._roc, reverse=True)

        for i, s in enumerate(roc, start=1):
            s.roc_order = i

    # sort greenblatt
    @classmethod
    def sort_gb_eyroc(cls):
        gb_eyroc_order = []

        for s in cls.sector:
            s.gb_eyroc_order = s.ey_order + s.roc_order

        cls.sector.sort(key=lambda s: s.gb_eyroc_order)

class Snapshot(Base):
    __tablename__ = 'snapshots'
    date = Column(Date, primary_key = True)
    code = Column(String, primary_key = True)
    pc = Column(Float)
