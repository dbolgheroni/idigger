#!/usr/bin/env python
#
# Copyright (c) 2012, Daniel Bolgheroni. All rights reserved.
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

import argparse
import datetime
import os
import sqlite3

# import idigger modules
#import gi
from stock import Stock
from fmt_drv import Fundamentus
from idiggerconf import *

opts = argparse.ArgumentParser()

opts.add_argument("conf", 
        help="the file which contains stocks codes, one per line")
opts.add_argument("-D",
        help="don't dowload info from source (useful to debug)",
        action="store_true")
# unused yet, there is only 1 driver
opts.add_argument("-d",
        help="specify which driver to use")
args = opts.parse_args()

# local definitions
prefix = "[fch]"

# presentation
print(prefix, "conf file:", args.conf)

# open conf file
try:
    f = open(args.conf)
except IOError:
    print(prefix, " can't open ", args.conf, ", exiting", sep="")
    exit(1)
else:
    conf = tuple(f.read().splitlines())
    f.close()

# open database file
try:
    db = sqlite3.connect(dbfile)
except IOError:
    print(prefix, " can't open db ", dbfile, ", exiting", sep="")
    exit(1)

# create tables dinamically if it don't exist
for c in conf:
    query = "SELECT * FROM sqlite_master WHERE TYPE='table' AND NAME=?"
    result = db.execute(query, (c,))

    # only first fetchall() returns something, so assign it
    r = result.fetchall()

    if not r:
        print(prefix, "table", c.rjust(6),
                "doesn't exists, creating")
        db.execute("CREATE TABLE %s ( \
                    date INTEGER PRIMARY KEY, \
                    ey DOUBLE, \
                    roc DOUBLE)" % c)

# instantiate stocks
stock = {}
for c in conf:

    # -D argument
    if args.D:
        stock[c] = Fundamentus(c, fetch=False)
    else:
        stock[c] = Fundamentus(c)

# populate database
for c in conf:
    ey = stock[c].earnings_yield()
    roc = stock[c].return_on_capital()

    # do not populate database with invalid values
    if ey and roc:
        # do not populate database with too much decimas
        eyf = "{:.2f}".format(ey)
        rocf = "{:.2f}".format(roc)

        t = (today, eyf, rocf)
        query = "INSERT INTO %s VALUES (?, ?, ?)" % c
        try:
            db.execute(query, t)
        except sqlite3.IntegrityError:
            print(prefix, " ", c, " date is primary key, skipping",
                    sep="")
    else:
        print(prefix, " invalid value for ", c, ", skipping", sep="")
        continue

    db.commit()

# debug
def print_debug(): # give a scope
    prefix = "[dbg]"

    for c in conf:
        mv = stock[c].market_value()
        na = stock[c].net_assets()
        nnfa = stock[c].net_nonfixed_assets()
        ebit = stock[c].ebit()
        evebit = stock[c].ev_ebit()
        mvnwc = stock[c].market_value_net_working_capital()
        nwc = stock[c].net_working_capital()
        nfa = stock[c].net_fixed_assets()
        ey = stock[c].earnings_yield()
        roc = stock[c].return_on_capital()

        print(prefix, c.ljust(6), "Valor de mercado".ljust(24, "."), mv)
        print(prefix, c.ljust(6), "Ativo".ljust(24, "."), na)
        print(prefix, c.ljust(6), "Ativo Circulante".ljust(24, "."), nnfa)
        print(prefix, c.ljust(6), "EBIT".ljust(24, "."), ebit)
        print(prefix, c.ljust(6), "EV/EBIT".ljust(24, "."), evebit)
        print(prefix, c.ljust(6), "P/Cap. Giro".ljust(24, "."), mvnwc)
        print(prefix, c.ljust(6), "Net Working Capital".ljust(24, "."), nwc)
        print(prefix, c.ljust(6), "Net Fixed Assets".ljust(24, "."), nfa)
        print(prefix, c.ljust(6), "EY [%]".ljust(24, "."), ey)
        print(prefix, c.ljust(6), "ROC [%]".ljust(24, "."), roc)

if debug:
    print(prefix, "debug enabled")
    print_debug()
