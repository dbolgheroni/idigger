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

# activate pre-installed virtual environment containing the libraries;
# in other words, run from $HOME
this_file = "idigger/src/venv/bin/activate_this.py"
execfile(this_file, dict(__file__=this_file))

import argparse, datetime, os
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from conf import dbfile
from models import Base, Stock
from fmt_drv import Fundamentus
from debug import print_stock

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
engine = create_engine('sqlite:///' + dbfile)
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
    fetchopt = True

# instantiate stocks
# the complexity is hidden inside the driver and in the Stock class
today = datetime.datetime.today();
todaystr = today.strftime('%Y%m%d')
print(prefix, 'downloading raw data and parsing stock info')
for code in conf:
    # stocks which failed to instantiate are marked as None
    Fundamentus(code, fetch=fetchopt, date=todaystr);

# sorting, and it's where the Greenblatt method actually is
Stock.sort_ey()
Stock.sort_roc()
Stock.sort_gb_eyroc()
Stock.sort_pe()
Stock.sort_roe()
Stock.sort_gb_peroe()

# populate database
# use a leading underscore to differ from the model access to the db
for stock in Stock.sector:
    x = Stock( \
            date = today, \
            code = stock.code, \
            ey = stock._ey, \
            roc = stock._roc, \
            pe = stock._pe, \
            roe = stock._roe, \
            pc = stock._pc, \

            ey_order = stock.ey_order, \
            roc_order = stock.roc_order, \
            gb_eyroc_order = stock.gb_eyroc_order, \

            pe_order = stock.pe_order, \
            roe_order = stock.roe_order, \
            gb_peroe_order = stock.gb_peroe_order)

    s.add(x)

print(prefix, 'commiting to database')
try:
    s.commit()
except IntegrityError:
    print(prefix, 'error commiting to database')

# debug
if debug:
    for stock in sector:
        print_stock(stock)
