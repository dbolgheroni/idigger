"""gi (GuiaInvest) module: contains functions to handle data obtained
from this provider."""

import os
import re
import urllib.request

from idiggerconf import *
from log import *

# local definitions
_baseurl = "http://guiainvest.com.br/raiox/"

# interface
def fetch(c):
    """Fetch files to extract info needed by other classes."""

    log("fetch", c.rjust(6), end=" stock data ")

    # define path for local file
    stockfile = os.path.join(tmpdir, c.lower() + ".aspx")

    # define URL
    url = _baseurl + c.lower() + '.aspx' 

    # download URL
    try:
        iurl = urllib.request.urlopen(url)
    except urllib.error.URLError:
        log(end="(FAILED)", prefix=False)
        return None
    else:
        log(end="(OK)", prefix=False)

    # write file
    try:
        ourl = open(stockfile, "w")
    except IOError:
        log(" couldn't store data into", stockfile, prefix=False)

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
    f = open(path, encoding="iso-8859-1")
    s = f.read()
    
    regex = v + r'">(?P<value>(-)?(\d)+,(\d)+)'
    pattern = re.compile(regex)
    match = pattern.search(s)
    if match:
        r = match.group('value')
        value = float(re.sub(r',', r'.', r))
    else:
        value = None

    f.close()
    return value
