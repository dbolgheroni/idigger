"""gi (GuiaInvest) module contains classes to manipulate data obtained
from this provider."""

import os
import re
import urllib.request

class GuiaInvest:
    relat = os.path.join(os.environ['HOME'], ".idigger", "rawdata")

    # class methods
    @classmethod
    def fetch(cls, c):
        """fetch raw data to extract info needed by other classes"""

        print("downloading", c.rjust(6), end=" stock info... ")

        # define path for local file
        absol = os.path.join(cls.relat, c.lower() + ".aspx")

        # define URL
        baseurl = "http://guiainvest.com.br/raiox/"
        url = baseurl + c.lower() + '.aspx' 

        # download URL
        try:
            iurl = urllib.request.urlopen(url)
        except URLError:
            print(end="FAILED")
        else:
            print(end="OK")
        
        # write file
        try:
            ourl = open(absol, "w")
        except IOError:
            print(" (couldn't write to local file)")
        else:
            print()

        stock = iurl.read().decode("iso-8859-1")
        ourl.write(stock)

        # close descriptors
        iurl.close()
        ourl.close()

    @classmethod
    def extract_pe(cls, stock):
        value = cls.__extract_id(stock,
                'lbPrecoLucroAtual')
        return value

    @classmethod
    def extract_roe(cls, stock):
        value = cls.__extract_id(stock,
                'lbRentabilidadePatrimonioLiquido3')
        return value

    @classmethod
    def __extract_id(cls, stock, v):
        value = -999
    
        path = os.path.join(cls.relat, stock + ".aspx")
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
