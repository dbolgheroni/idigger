"""gi (GuiaInvest) module: contains functions to handle data obtained
from this provider."""

import os
import re
import urllib.request

from idiggerconf import *
from log import *

# local definitions
_baseurl = "http://guiainvest.com.br/raiox/"
_localdir = os.path.join(homedir, today + "-gi")
me = "fetcher"

# INTERFACE
def makedir():
    """Make dir to fetch files into it."""
    if not os.path.exists(_localdir):
        try:
            log("making " + _localdir + "/ dir", caller=me)
            os.makedirs(_localdir)
        except OSError:
            log("can't make " + _localdir + "/, exiting", caller=me)
            exit(1)

def fetch(c):
    """Fetch files to extract info needed by other classes."""

    log("fetch", c.rjust(6), end=" stock data ", caller=me)

    # download URL
    url = _baseurl + c.lower() + '.aspx' 
    try:
        iurl = urllib.request.urlopen(url)
    except urllib.error.URLError:
        log("(FAILED)", prefix=False, caller=me)
        return None
    else:
        log("(OK)", prefix=False, caller=me)

    # write file
    stockfile = os.path.join(_localdir, c.lower() + ".aspx")
    try:
        ourl = open(stockfile, "w")
    except IOError:
        log("can't open %s for writing" % stockfile, caller=me)

    stock = iurl.read().decode("iso-8859-1")
    ourl.write(stock)

    # close descriptors
    iurl.close()
    ourl.close()

def extract_pe(stock):
    """Extract P/E value. Returns 'None' if not found."""
    return __extract_id(stock, 'lbPrecoLucroAtual')

def extract_roe(stock):
    """Extract ROE value. Returns 'None' if not found."""
    return __extract_id(stock, 'lbRentabilidadePatrimonioLiquido3')

# INTERNAL METHODS
def __extract_id(stock, v):
    path = os.path.join(_localdir, stock + ".aspx")
    try:
        f = open(path, encoding="iso-8859-1")
    except:
        log("can't open %s" % path, caller=me)
        return None

    s = f.read()
    
    regex = v + r'">(?P<value>(-)?(\d)+(\.(\d)+)?(,)?(\d)+)'
    pattern = re.compile(regex)
    match = pattern.search(s)
    if match:
        t = re.sub(r'\.', r'', match.group('value')) # remove dot
        value = float(re.sub(r',', r'.', t)) # remove BRA notation

        # enable for debugging
        #log("%s: %s = %s" % (stock.upper().rjust(6), v, value),
        #        caller=me)
    else:
        value = None

    f.close()
    return value
