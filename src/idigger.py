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
from idiggerconf import *
from show import *
from stock import *

opts = argparse.ArgumentParser()

opts.add_argument("conf", 
        help="the filename with the stocks codes, one per line")
opts.add_argument("output", 
        help="the filename for the HTML output")
args = opts.parse_args()

# local definitions
prefix = "[idg]"

# presentation
print(prefix, "idigger started")
print(prefix, "reading conf file", args.conf)

# open conf file
try:
    f = open(args.conf)
except IOError:
    print(prefix, " can't open ", args.conf, ", exiting", sep="")
    exit(1)
else:
    conf = tuple(f.read().splitlines())
    f.close()

# open output file
try:
    output = open(args.output, "w")
except IOError:
    print(prefix, "can't open", args.output, "for writing, exiting")
    exit(1)

# open database file
print(prefix, "reading db file", dbfile)
try:
    db = sqlite3.connect(dbfile)
except IOError:
    print(prefix, " can't open db ", dbfile, ", exiting", sep="")
    exit(1)

# instantiate stocks
sector = []
for c in conf:
    s = Stock(c)

    # TODO one loop to rule them all
    # earnings yield
    query = "SELECT ey FROM %s WHERE date=?" % c
    s.ey = db.execute(query, (today,)).fetchone()[0]

    # return on capital
    query = "SELECT roc FROM %s WHERE date=?" % c
    s.roc = db.execute(query, (today,)).fetchone()[0]

    # price-earnings
    query = "SELECT pe FROM %s WHERE date=?" % c
    s.pe = db.execute(query, (today,)).fetchone()[0]

    # return on equity
    query = "SELECT roe FROM %s WHERE date=?" % c
    s.roe = db.execute(query, (today,)).fetchone()[0]

    # day oscilation
    query = "SELECT do FROM %s WHERE date=?" % c
    s.do = db.execute(query, (today,)).fetchone()[0]

    # previous close
    query = "SELECT pc FROM %s WHERE date=?" % c
    s.pc = db.execute(query, (today,)).fetchone()[0]

    # only instantiate stocks with both ey and roc
    if s.ey and s.roc:
        sector.append(s)

# sort EY order
Stock.sort_ey(sector)

# sort ROC order
Stock.sort_roc(sector)

# sort Greenblatt order
Stock.sort_gb_eyroc(sector)

## HTML output ##
# define header
th = ["#", "A&ccedil;&otilde;es", "EY[%]", "ROC[%]",
      "P/L", "ROE[%]",
      "Osc.Dia[%]", "&Uacute;lt.Fech.[R$]"]

print(prefix, "generating", args.output)
show(sector, output, title="idigger", tablehdr=th)
