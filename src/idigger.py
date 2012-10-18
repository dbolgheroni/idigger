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
        gi.fetch(c)

# instantiate stocks
sector = []
for s in conf:
    # "constructor"
    obj = stock.Stock(s) 
    sector.append(obj)

    # extract P/E from raw data
    obj.pe = gi.extract_pe(s.lower())

    # extract P/VB from raw data
    obj.roe = gi.extract_roe(s.lower())

# sort P/E order
stock.Stock.sort_pe(sector)

# sort ROE order
stock.Stock.sort_roe(sector)

# sort Greenblatt
stock.Stock.sort_greenblatt(sector)

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

