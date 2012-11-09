"""gi (GuiaInvest) module: contains functions to handle data obtained
from this provider."""

import os
import re
import urllib.request

from idiggerconf import *
from log import *


# local definitions
_baseurl = "http://guiainvest.com.br/raiox/"
me = "fetcher"

# interface
def fetch(c):
    """Fetch files to extract info needed by other classes."""

    log("fetch", c.rjust(6), end=" stock data ", caller=me)

    # define path for local file
    stockfile = os.path.join(tmpdir, c.lower() + ".aspx")

    # define URL
    url = _baseurl + c.lower() + '.aspx' 

    # download URL
    try:
        iurl = urllib.request.urlopen(url)
    except urllib.error.URLError:
        log("(FAILED)", prefix=False, caller=me)
        return None
    else:
        log("(OK)", prefix=False, caller=me)

    # write file
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

# internal functions
def __extract_id(stock, v):
    path = os.path.join(tmpdir, stock + ".aspx")
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
    else:
        value = None

    f.close()
    return value
