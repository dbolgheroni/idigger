"""gi (GuiaInvest) module: contains functions to handle data obtained
from this provider."""

import os
import re
import urllib.request

from log import *

_relat = os.path.join(os.environ['HOME'], ".idigger", "rawdata")

# class methods
def fetch(c):
    """Fetch raw data to extract info needed by other classes."""

    log("downloading", c.rjust(6), end=" stock info... ")

    # define path for local file
    absol = os.path.join(_relat, c.lower() + ".aspx")

    # define URL
    baseurl = "http://guiainvest.com.br/raiox/"
    url = baseurl + c.lower() + '.aspx' 

    # download URL
    try:
        iurl = urllib.request.urlopen(url)
    except URLError:
        log(end="FAILED", prefix=False)
    else:
        log(end="OK", prefix=False)

    # write file
    try:
        ourl = open(absol, "w")
    except IOError:
        log(" (couldn't write to local file)", prefix=False)
    else:
        log(prefix=False)

    stock = iurl.read().decode("iso-8859-1")
    ourl.write(stock)

    # close descriptors
    iurl.close()
    ourl.close()

def extract_pe(stock):
    """Extract P/E value from raw data obtained by fetch()."""
    value = __extract_id(stock,
            'lbPrecoLucroAtual')
    return value

def extract_roe(stock):
    """Extract ROE value from raw data obtained by fetch()."""
    value = __extract_id(stock,
            'lbRentabilidadePatrimonioLiquido3')
    return value

def __extract_id(stock, v):
    value = -999

    path = os.path.join(_relat, stock + ".aspx")
    f = open(path, encoding="iso-8859-1")
    s = f.read()
    
    regex = v + r'">(?P<value>(-)?(\d)+,(\d)+)'
    pattern = re.compile(regex)
    match = pattern.search(s)
    if match:
        r = match.group('value')
        value = float(re.sub(r',', r'.', r))

    f.close()
    return value
