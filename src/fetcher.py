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
import gi
from idiggerconf import *

opts = argparse.ArgumentParser()

opts.add_argument("conf", 
        help="the file which contains stocks codes, one per line")
opts.add_argument("-D",
        help="don't dowload info from source (useful to debug)",
        action="store_true")
opts.add_argument("-e", 
        help="specify which engine to use")
args = opts.parse_args()

# local definitions
prefix = "[fetcher]"

# initializations

# presentation
print(prefix, "start:", now)
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
    result = db.execute(query, (c.lower(),))

    # only first fetchall() returns something, so assign it
    r = result.fetchall()

    if not r:
        print(prefix, "table", c.lower().rjust(6),
                "doesn't exists, creating")
        db.execute("CREATE TABLE %s (date INTEGER PRIMARY KEY, pe DOUBLE, roe DOUBLE)" % c.lower()) 

# -D argument
if not args.D:
    # create a dir to the files to
    gi.makedir()

    print(prefix, "fetching data for stocks")
    for c in conf:
        gi.fetch(c)
else:
    print(prefix, "dummy mode selected, won't download files")

# populate database
for c in conf:
    pe = gi.extract_pe(c.lower())
    roe = gi.extract_roe(c.lower())

    # does not populate database with invalid values
    if pe and roe:
        t = (today, pe, roe)
        query = "INSERT INTO %s VALUES (?, ?, ?)" % c.lower()
        try:
            db.execute(query, t)
        except sqlite3.IntegrityError:
            print(prefix, " ", c.lower().rjust(6),
                    ": date is primary key, skipping", sep="")
    else:
        print(prefix, " invalid value for ", c.upper().rjust(6),
                ", skipping", sep="")
        continue

    db.commit()

# statistics
endt = datetime.datetime.now()
totalt = endt - startt
print(prefix, " total time: ", totalt.seconds, "s", sep="")
