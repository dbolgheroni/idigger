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

# import idigger modules
import gi
import stock

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

#print(args.output) # automagically sets output

version = "0.1"

# read stocks from stocklist
f = open(args.conf)
conf = tuple(f.read().splitlines())
f.close()

# -D argument
if not args.D:
    for c in conf:
        gi.GuiaInvest.fetch(c)

# instantiate stocks
sector = []
for s in conf:
    # "constructor"
    obj = stock.Stock(s) 
    sector.append(obj)

    # extract P/E from raw data
    obj.pe = gi.GuiaInvest.extract_pe(s.lower())

    # extract P/VB from raw data
    obj.roe = gi.GuiaInvest.extract_roe(s.lower())

# sort P/E
#
# negative P/E -> pe_rotten
# positive P/E -> pe_ok
#
# |      pe           | (1)
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

# sort ROE
#
# negative ROE -> roe_rotten
# positive ROE -> roe_ok
#
# |       roe           | (1)
# | roe_ok | roe_rotten | 
# <--------0------------->
# +                      - 
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

# sort Greenblatt
#
# | greenblatt |
# 0------------>
#              +

for s in sector:
    s.greenblatt_order = s.pe_order + s.roe_order

sector.sort(key=lambda s: s.greenblatt_order)

# print header
print("Ação".ljust(9),
      "P/L".rjust(6),
      "ordem P/L".rjust(9),
      "ROE".rjust(6),
      "ordem ROE".rjust(9),
      "ordem Greenblatt".rjust(16))

# print stocks
for s in sector:
    print(s.code.ljust(9),
          str(s.pe).rjust(6),
          str(s.pe_order).rjust(9),
          str(s.roe).rjust(6),
          str(s.roe_order).rjust(9),
          str(s.greenblatt_order).rjust(16))

