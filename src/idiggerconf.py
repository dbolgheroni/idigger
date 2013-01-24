"""idiggerconf module: contains definitions common to 2+ modules."""

import datetime
import os.path

# date and time
logdatef= "%Y%m%d %H:%M:%S"
dbdatef = "%Y%m%d"
showdatef = "%d/%m/%Y %H:%M:%S"

startt = datetime.datetime.now()

today = startt.strftime(dbdatef)
now = startt.strftime(logdatef)

# dir
homedir = os.path.join(os.environ['HOME'], ".idigger")
tmpdir = os.path.join(homedir, "tmp")

dbfile = os.path.join(homedir, "idigger.db")
