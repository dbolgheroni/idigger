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
import urllib

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
        action="store_true"); # flag (option without value)
opts.add_argument("-e", 
        help="specify which engine to use")
args = opts.parse_args()

#print(args.output) # automagically sets output

version = "0.1"

# read stocks from stocklist
f = open(args.conf)
conf = tuple(f.read().splitlines())
f.close()

# instantiate stocks
sector = []
for s in conf:
    # "constructor"
    obj = stock.Stock(s) 
    sector.append(obj)

    # extract P/E from raw data
    obj.set_pe(gi.GuiaInvest.extract_pe(s.lower())) 

# sort based on P/E
#
# negative P/E -> pe_rotten
# positive P/E -> pe_ok
#
# | pe_rotten | pe_ok |
# <-----------0------->
# -                   + 
#
# becomes
#
# |     pe_ordered    | (1)
# | pe_ok | pe_rotten | 
# 0------->----------->
#         +           - 
pe_ok = []
pe_rotten = []
for s in sector:
    if s.get_pe() >= 0:
        pe_ok.append(s)
    else:
        pe_rotten.append(s)

pe_ok.sort(key=lambda s: s.get_pe())
pe_rotten.sort(key=lambda s: s.get_pe(), reverse=True)
sector = pe_ok + pe_rotten

for s in sector:
    print(s.get_code().ljust(9), str(s.get_pe()).rjust(6))

# download rawdata related to stocks
#for c in conf:
#    gi.GuiaInvest.fetch(c)
