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
from log import *
from show import *
from stock import *

opts = argparse.ArgumentParser()

opts.add_argument("conf", 
        help="the file which contains stocks codes, one per line")
opts.add_argument("output", 
        help="the filename for the HTML output")
args = opts.parse_args()

# presentation
log("conf file:", args.conf)

# open conf file
try:
    f = open(args.conf)
except IOError:
    log("can't open %s, exiting" % args.conf)
    exit(1)
else:
    conf = tuple(f.read().splitlines())
    f.close()

# open output file
try:
    output = open(args.output, "w")
except IOError:
    log("can't open %s for writing, exiting" % args.output)
    exit(1)

# open database file
log("reading db file:", dbfile)
try:
    db = sqlite3.connect(dbfile)
except IOError:
    log("can't open db %s, exiting" % dbfile)
    exit(1)

# instantiate stocks
sector = []
for c in conf:
    # "constructor"
    obj = Stock(c) 

    query = "SELECT pe FROM %s WHERE date=?" % c.lower()
    try:
        obj.pe = db.execute(query, (today,)).fetchone()[0]
    except TypeError:
        log("empty db entry for stock" % c.upper())
        continue

    query = "SELECT roe FROM %s WHERE date=?" % c.lower()
    try:
        obj.roe = db.execute(query, (today,)).fetchone()[0] 
    except TypeError:
        log("empty db entry for stock" % c.upper())
        continue

    # only instantiate "good" stocks (with valid non-negative values)
    if (obj.pe > 0) and (obj.roe > 0):
        sector.append(obj)

# sort P/E order
Stock.sort_pe(sector)

# sort ROE order
Stock.sort_roe(sector)

# sort Greenblatt order
Stock.sort_greenblatt(sector)

# HTML output
show(sector, output, driver="html")
