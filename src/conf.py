# contains definitions common to 2+ modules

import datetime
import os.path

# date and time
startt = datetime.datetime.now()

today = startt.strftime('%Y%m%d')
now = startt.strftime('%Y%m%d %H:%M:%S')

# dir
homedir = os.path.join(os.environ['HOME'], ".idigger")
datadir = os.path.join(homedir, "data")
tmpdir = os.path.join(homedir, "tmp")

dbfile = os.path.join(homedir, "idigger.db")
