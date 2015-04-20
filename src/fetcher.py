#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012-2015, Daniel Bolgheroni. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
# 
# THIS SOFTWARE IS PROVIDED BY DANIEL BOLGHERONI ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL DANIEL BOLGHERONI OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import print_function

import argparse, datetime, os
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from models import Base, Stock
from fmt_drv import Fundamentus

# local definitions
prefix = "[fch]"

# handle command line arguments
opts = argparse.ArgumentParser()
opts.add_argument("-d",
        help="enable debug, print intermediary operations",
        action="store_true")
opts.add_argument("-D",
        help="do not download info from source (useful with debug)",
        action="store_true")
opts.add_argument("conf",
        help="the file which contains stocks codes, one per line")
args = opts.parse_args()

# presentation
print(prefix, "fetcher started")
print(prefix, "conf file:", args.conf)

# read configuration file
with open(args.conf, 'r') as f:
    conf = tuple(f.read().splitlines())

# sqlalchemy config
basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + os.path.join(basedir, 'idigger.db'))
session = sessionmaker()
session.configure(bind=engine)
Stock.metadata.create_all(engine)
s = session()

# handle -d option
debug = False
if args.d:
    debug = True

# handle -D option
if args.D:
    fetchopt = False
else:
    print(prefix, "downloading raw data")
    fetchopt = True

##
today = datetime.datetime.today();
todaystr = today.strftime('%Y%m%d')
stock = {}
for code in conf:
    # stocks which failed to instantiate are marked as None
    stock[code] = Fundamentus(code, fetch=fetchopt, date=todaystr)

# populate database
for code in stock.keys(): # readability
    print(prefix, 'parsing ', code)
    if stock[code]:
        ey = stock[code].earnings_yield()
        roc = stock[code].return_on_capital()
        pe = stock[code].price_earnings()
        roe = stock[code].return_on_equity()
        pc = stock[code].previous_close()
        x = Stock(date=today, code=code, \
                ey=ey, roc=roc, pe=pe, roe=roe, pc=pc)

        s.add(x)

print(prefix, 'commiting to database')
try:
    s.commit()
except IntegrityError:
    print(prefix, 'error commiting to database')

# debug
def print_debug(): # give a scope
    prefix = "[dbg]"

    for code in stock.keys():
        if stock[code]:
            mv = stock[code].market_value()
            na = stock[code].net_assets()
            nnfa = stock[code].net_nonfixed_assets()
            ebit = stock[code].ebit()
            evebit = stock[code].ev_ebit()
            mvnwc = stock[code].market_value_net_working_capital()
            nwc = stock[code].net_working_capital()
            nfa = stock[code].net_fixed_assets()
            ey = stock[code].earnings_yield()
            roc = stock[code].return_on_capital()
            pe = stock[code].price_earnings()
            roe = stock[code].return_on_equity()
            pc = stock[code].previous_close()

            print(prefix, code.ljust(6), "Valor de mercado".ljust(24, "."), mv)
            print(prefix, code.ljust(6), "Ativo".ljust(24, "."), na)
            print(prefix, code.ljust(6), "Ativo Circulante".ljust(24, "."), nnfa)
            print(prefix, code.ljust(6), "EBIT".ljust(24, "."), ebit)
            print(prefix, code.ljust(6), "EV / EBIT".ljust(24, "."), evebit)
            print(prefix, code.ljust(6), "P/Cap. Giro".ljust(24, "."), mvnwc)
            print(prefix, code.ljust(6), "Net Working Capital".ljust(24, "."), nwc)
            print(prefix, code.ljust(6), "Net Fixed Assets".ljust(24, "."), nfa)
            print(prefix, code.ljust(6), "EY [%]".ljust(24, "."), ey)
            print(prefix, code.ljust(6), "ROC [%]".ljust(24, "."), roc)
            print(prefix, code.ljust(6), "P/L".ljust(24, "."), pe)
            print(prefix, code.ljust(6), "ROE [%]".ljust(24, "."), roe)
            print(prefix, code.ljust(6), \
                    "Cotação [R$]".decode('utf-8').ljust(24, "."), pc)

if debug:
    print(prefix, "debug enabled")
    print_debug()

#stocks = s.query(Stock).order_by(Stock.ey.desc())
#for i in stocks:
#    print(i.code, i.ey, i.roc)
