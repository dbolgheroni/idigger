"""gi (GuiaInvest) module contains classes to manipulate data obtained
from this provider."""

import os
import re

class GuiaInvest:
    rel = os.path.join(os.environ['HOME'], ".idigger", "rawdata")

    # class methods
    def fetch(c):
        """fetch raw data to extract info needed by other classes"""


        print("downloading", c.rjust(6), end=" stock info... ")

        rawstockdata = os.path.join(__class__.rel, c.lower() + ".aspx")
        command = "curl -s 'http://www.guiainvest.com.br/raiox/" \
                + c + ".aspx' > " + rawstockdata

        # TODO: check for curl
        
        dl_status = os.system(command)
        if dl_status:
            print("FAILED")
        else:
            print("OK")


    def extract_pe(stock):
        pe = -999
        path = os.path.join(__class__.rel, stock + ".aspx")
        f = open(path, encoding='iso-8859-1')
        s = f.read()
        
        pattern = re.compile(r'lbPrecoLucroAtual">(?P<pe>(-)?(\d)+,(\d)+)')
        match = pattern.search(s)
        if match:
            r = match.group('pe')
            pe = float(re.sub(r',', r'.', r))

        f.close()
        return pe

