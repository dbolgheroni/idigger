# driver module to handle Fundamentus provider

import os
import re
import urllib.request

from idiggerconf import *
from stock import Stock

# for name conventions, see PEP 8 - Style Guide for Python Code
class Fundamentus(Stock):
    __baseurl = "http://www.fundamentus.com.br/detalhes.php?papel="
    __localdir = os.path.join(datadir, today + "-fmt")
    __rawdata = {}
    __prefix = "[fmt]"

    def __init__(self, c, fetch=True):
        super().__init__(c)

        localfile = os.path.join(self.__localdir, self.code + ".html")

        if fetch:
            # check for directories where files is stored
            if not os.path.exists(self.__localdir):
                try:
                    print(self.__prefix, " making ", self.__localdir, "/ dir",
                            sep="")
                    os.makedirs(self.__localdir)
                except OSError:
                    print(self.__prefix, " can't make ", self.__localdir,
                            "/, exiting", sep="")
                    exit(1)

            # download URL
            url = self.__baseurl + self.code.lower()
            try:
                iurl = urllib.request.urlopen(url)
            except urllib.error.URLError:
                print(self.__prefix, "failed to fetch data for", self.code)
                return None

            # write file
            try:
                ourl = open(localfile, "w")
            except IOError:
                print(self.__prefix, "can't open", localfile, "for writing")

            contents = iurl.read().decode("iso-8859-1")
            ourl.write(contents)

            # close descriptors
            iurl.close()
            ourl.close()

        # read file

        try:
            f = open(localfile)
        except:
            print(self.__prefix, "can't open", localfile)
            return None

        self.__rawdata[c] = f.readlines()

    # market value
    def market_value(self):
        # Fundamentus: Valor de mercado (P)
        return self.__extract_int("Valor de mercado", 0)

    # net assets
    def net_assets(self):
        # Fundamentus: Ativo
        return self.__extract_int("Ativo", 7)

    # net non-fixed assets
    def net_nonfixed_assets(self):
        # Fundamentus: Ativo Circulante
        return self.__extract_int("Ativo Circulante", 2)

    # ebit
    def ebit(self):
        # Fundamentus: EBIT
        return self.__extract_int("EBIT", 5)

    # ev / ebit
    def ev_ebit(self):
        # Fundamentus: EV/EBIT
        return self.__extract_float("EBIT", 4)

    # market value / net working capital
    def market_value_net_working_capital(self):
        # Fundamentus: P/Cap. Giro
        return self.__extract_float("Cap\. Giro", 0)

    # net working capital
    def net_working_capital(self):
        mv = self.market_value()
        mvnwc = self.market_value_net_working_capital()

        if mv and mvnwc:
            nwc = mv / mvnwc
            return nwc

    # net fixed assets
    def net_fixed_assets(self):
        na = self.net_assets()
        nnfa = self.net_nonfixed_assets()

        if na and nnfa:
            nfa = na - nnfa
            return nfa

    # earnings yield (EY)
    def earnings_yield(self):
        # ey = ebit / ev
        evebit = self.ev_ebit()

        if evebit:
            ey = 1 / evebit

            # don't clutter the db
            return ey * 100

    # return on capital (ROC)
    def return_on_capital(self):
        ebit = self.ebit()
        nwc = self.net_working_capital()
        nfa = self.net_fixed_assets()

        if ebit and nwc and nfa:
            roc = ebit / (nwc + nfa)

            return roc * 100

    ####### auxiliary private methods #######
    def __extract_int(self, indicator, occline):
        lines = self.__matchlines(self.code, indicator)

        # with ints, the line where the value is located is always 1
        # after the occurrence of the indicator
        content = self.__rawdata[self.code][lines[occline]+1]

        # remove points
        regex = re.compile(r"\.")
        c1 = regex.sub("", content)

        # clean whitespace/tags before int
        regex = re.compile(r".*\">")
        c2 = regex.sub("", c1)

        # extract the number per se
        regex = re.compile(r"(?P<int>\d+)")
        c3 = regex.search(c2)

        if c3:
            return int(c3.group('int'))

    def __extract_float(self, indicator, occline):
        lines = self.__matchlines(self.code, indicator)

        # with floats, the line where the value is located is always 2 
        # after the occurrence of the indicator
        content = self.__rawdata[self.code][lines[occline]+2]

        regex = re.compile(r"(?P<float>[-]?\d+,\d+)")
        match = regex.search(content)

        if match:
            c1 = match.group('float')

            # Brazil uses 3,14 instead of 3.14 (computer notation), so
            # change commas for points
            regex = re.compile(r",")
            c2 = regex.sub(".", c1)
            return float(c2)

    # return a list with the line number where every occurrence of the
    # indicator occurs; it's a hint of where to find the real value
    def __matchlines(self, code, indicator):
        lines = []

        c = 0
        for l in self.__rawdata[code]:
            pattern = re.compile(indicator)
            match = pattern.search(l)

            if match:
                lines.append(c)

            c += 1

        return lines
