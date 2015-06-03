# contains definitions common to 2+ modules

from __future__ import print_function

import datetime
import os
import os.path

prefix = "[cnf]"

# date and time
startt = datetime.datetime.now()

today = startt.strftime('%Y%m%d')
now = startt.strftime('%Y%m%d %H:%M:%S')

# dir
homedir = os.path.join(os.environ['HOME'], ".idigger")
datadir = os.path.join(homedir, "data")
tmpdir = os.path.join(homedir, "tmp")

dbfile = os.path.join(homedir, "idigger.db")

# create homedir if it does not exist
def create_homedir():
    if (not os.path.isdir(homedir)):
        print(prefix, "homedir does not exist, creating")

        try:
            os.makedirs(homedir)
        except OSError:
            print(prefix, "can't create homedir, exitting")
            exit(1)
