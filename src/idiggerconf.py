"""idiggerconf module: contains definitions common to 2+ modules."""

import datetime
import os.path

# definitions
homedir = os.path.join(os.environ['HOME'], ".idigger")
tmpdir = os.path.join(homedir, "tmp")

dbfile = os.path.join(homedir, "idigger.db")
