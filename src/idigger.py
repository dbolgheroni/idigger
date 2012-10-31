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

# import idigger modules
import gi
from idiggerconf import *
from log import *
from show import *
from stock import *

opts = argparse.ArgumentParser()

opts.add_argument("conf", 
        help="the file which contains stocks codes, one per line")
opts.add_argument("output", 
        help="the filename for the HTML output")
opts.add_argument("-D",
        help="don't dowload info from source (useful to debug)",
        action="store_true")
opts.add_argument("-e", 
        help="specify which engine to use")
args = opts.parse_args()

# local definitions
logdtfm= "%Y%m%d %H:%M:%S"

# presentation
startt = datetime.datetime.now()
now = startt.strftime(logdtfm)
log("version:", version)
log("start:", now)
log("conf file:", args.conf)

# read stocks from stocklist
try:
    f = open(args.conf)
except IOError:
    log("couldn't open %s (check for permissions)" % args.conf)
    exit(1)
else:
    conf = tuple(f.read().splitlines())
    f.close()

# create temporary dirs
if not (os.path.exists(tmpdir)):
    try:
        log("required temporary directories don't exist, creating")
        os.makedirs(tmpdir)
    except OSError:
        log("can't create temporary dirs, quitting")
        exit(1)

# -D argument
if not args.D:
    for c in conf:
        gi.fetch(c)
else:
    log("dummy mode selected, won't download files")

# open file for output
try:
    output = open(args.output, "w")
except IOError:
    log("couldn't open %s (check for permissions)" % args.output)
    exit(1)

# instantiate stocks
sector = []
for s in conf:
    # "constructor"
    obj = Stock(s) 

    # extract P/E from file
    obj.pe = gi.extract_pe(s.lower())
    if not obj.pe or obj.pe < 0:
        continue

    # extract P/VB from file
    obj.roe = gi.extract_roe(s.lower())
    if not obj.roe or obj.pe < 0:
        continue

    # only instantiate "good" stocks (with valid non-negative values)
    sector.append(obj)

# sort P/E order
Stock.sort_pe(sector)

# sort ROE order
Stock.sort_roe(sector)

# sort Greenblatt order
Stock.sort_greenblatt(sector)

# show results
gent = datetime.datetime.now()
now = gent.strftime(logdtfm)
log("output generated time:", now)
show(sector, output, gent, driver="html")

totalt = gent - startt
log("total time:", "%d s" % totalt.seconds)
