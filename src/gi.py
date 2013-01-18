"""gi (GuiaInvest) module: contains functions to handle data obtained
from this provider."""

import os
import re
import urllib.request

from idiggerconf import *

# local definitions
_baseurl = "http://guiainvest.com.br/raiox/"
_localdir = os.path.join(homedir, today + "-gi")
prefix = "[fetcher]"

# INTERFACE
def makedir():
    """Make dir to fetch files into it."""
    if not os.path.exists(_localdir):
        try:
            print(prefix, " making ", _localdir, "/ dir", sep="")
            os.makedirs(_localdir)
        except OSError:
            print(prefix, " can't make ", _localdir, "/, exiting",
                    sep="")
            exit(1)

def fetch(c):
    """Fetch files to extract info needed by other classes."""

    # download URL
    url = _baseurl + c.lower() + '.aspx' 
    try:
        iurl = urllib.request.urlopen(url)
    except urllib.error.URLError:
        print(prefix, "failed to fetch data for", c)
        return None

    # write file
    stockfile = os.path.join(_localdir, c.lower() + ".aspx")
    try:
        ourl = open(stockfile, "w")
    except IOError:
        print(prefix, "can't open", stockfile, "for writing")

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
        print(prefix, "can't open", path)
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
