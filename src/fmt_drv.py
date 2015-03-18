# driver module to handle Fundamentus provider

import os
import re
import time
import urllib.request
import urllib.error
from html.parser import HTMLParser

from idiggerconf import *
from stock import Stock


# keep the class generic and treat the raw values outside
class FundamentusParser(HTMLParser):
    def __init__(self, lookup):
        HTMLParser.__init__(self)

        self.__lookup = lookup
        self.__near = False
        self.__found = False
        self.__result = None

    @property
    def result(self):
        return self.__result

    # some values are returned with a lot of leading spaces, so we need
    # to delete it
    def delete_space(self, value):
        regex = re.compile(r"[[:space:]]+")
        return regex.sub("", value)

    # some integer values are returned as 100.000.000.000 and these are
    # not convertible into an integer unless we remove the dots
    def delete_int_dot(self, value):
        regex = re.compile(r"\.")
        return int(regex.sub("", value))

    # some float values are returned as 100,00 but decimal separation in
    # common computer systems is the dot, so we need to substitute
    def sub_comma_for_point(self, value):
        regex = re.compile(r",")
        return regex.sub(".", value)

    def handle_starttag(self, tag, attrs):
        if self.__near:
            for name, value in attrs:
                if 'txt' in value: 
                    self.__found = True

    def handle_data(self, data):
        if self.__lookup == data:
            self.__near = True

        if self.__found:
            self.__result = data

    def handle_endtag(self, tag):
        if self.__found:
            self.__near = False
            self.__found = False


# for name conventions, see PEP 8 - Style Guide for Python Code
class Fundamentus(Stock):
    __baseurl = "http://www.fundamentus.com.br/detalhes.php?papel="
    __rawdata = {} # TODO make it an instance variable
    __prefix = "[fmt]"

    __contents = None

    def __init__(self, c, fetch=True, date=today):
        super().__init__(c)

        localdir = os.path.join(datadir, date + "-fmt")
        localfile = os.path.join(localdir, self.code + ".html")

        if fetch:
            # check for directories where files is stored
            if not os.path.exists(localdir):
                try:
                    print(self.__prefix, " making ", localdir,
                            "/ dir", sep="")
                    os.makedirs(localdir)
                except OSError:
                    print(self.__prefix, " can't make ", localdir,
                            "/, exiting", sep="")
                    exit(1)

            url = self.__baseurl + self.code.lower()

            # download URL
            attempts = 0
            while True:
                try:
                    #print(self.__prefix, self.code, "downloading data")
                    iurl = urllib.request.urlopen(url)
                    break
                except urllib.error.URLError:
                    attempts += 1
                    print(self.__prefix, self.code,
                            "error downloading, retrying in 30 seconds")
                    time.sleep(30) # wait 30 s to retry

                    if attempts == 5: # max retry
                        print(self.__prefix, self.code,
                                "download failed, giving up")
                        return None

            # write file
            try:
                ourl = open(localfile, "w")
            except IOError:
                print(self.__prefix, "can't open", localfile,
                        "for writing")

            self.__contents = iurl.read().decode("iso-8859-1")
            ourl.write(self.__contents)

            # close descriptors
            iurl.close()
            ourl.close()

        # open file
        try:
            f = open(localfile)
        except IOError:
            print(self.__prefix, "can't open", localfile)
            return None

        self.__rawdata[c] = f.readlines()

        f.seek(0)
        self.__contents = f.read()

    ####### values parsed from page #######
    # market value
    def market_value(self):
        # Fundamentus: Valor de mercado (P)
        return self.__extract_int("Valor de mercado", 0)

    # market value 2
    def market_value2(self):
        # Fundamentus: Valor de mercado (P)
        parser = FundamentusParser('Valor de mercado')
        parser.feed(self.__contents)

        # remove points
        return parser.delete_int_dot(parser.result)

    # net assets
    def net_assets(self):
        # Fundamentus: Ativo
        return self.__extract_int("Ativo", 7)

    # net assets 2
    def net_assets2(self):
        # Fundamentus: Ativo
        parser = FundamentusParser('Ativo')
        parser.feed(self.__contents)

        # remove points
        return parser.delete_int_dot(parser.result)

    # net non-fixed assets
    def net_nonfixed_assets(self):
        # Fundamentus: Ativo Circulante
        return self.__extract_int("Ativo Circulante", 2)

    # net non-fixed assets 2
    def net_nonfixed_assets2(self):
        # Fundamentus: Ativo Circulante 2
        parser = FundamentusParser('Ativo Circulante')
        parser.feed(self.__contents)

        # remove points
        return parser.delete_int_dot(parser.result)

    # ebit
    def ebit(self):
        # Fundamentus: EBIT
        return self.__extract_int("EBIT", 5)

    # ebit 2
    def ebit2(self):
        # Fundamentus: EBIT
        parser = FundamentusParser('EBIT')
        parser.feed(self.__contents)

        # remove points
        return parser.delete_int_dot(parser.result)

    # ev / ebit
    def ev_ebit(self):
        # Fundamentus: EV / EBIT
        return self.__extract_float("EBIT", 4)

    # ev / ebit 2
    def ev_ebit2(self):
        # Fundamentus: EV / EBIT
        parser = FundamentusParser('EV / EBIT')
        parser.feed(self.__contents)

        rresult = parser.delete_space(parser.result)
        return float(parser.sub_comma_for_point(rresult))

    # market value / net working capital
    def market_value_net_working_capital(self):
        # Fundamentus: P/Cap. Giro
        return self.__extract_float("Cap\. Giro", 0)

    # market value / net working capital 2
    def market_value_net_working_capital2(self):
        # Fundamentus: P/Cap. Giro
        parser = FundamentusParser('P/Cap. Giro')
        parser.feed(self.__contents)

        rresult = parser.delete_space(parser.result)
        return float(parser.sub_comma_for_point(rresult))

    ####### values calculated from values extract from page #######
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
            return "{:.2f}".format(ey * 100)

    # return on capital (ROC)
    def return_on_capital(self):
        ebit = self.ebit()
        nwc = self.net_working_capital()
        nfa = self.net_fixed_assets()

        if ebit and nwc and nfa:
            roc = ebit / (nwc + nfa)
            return "{:.2f}".format(roc * 100)

    # price-earnings (P/E)
    def price_earnings(self):
        # Fundamentus: P/L
        return self.__extract_float("P/L", 0, 1)

    # return on equity (ROE)
    def return_on_equity(self):
        # Fundamentus: ROE
        return self.__extract_float("ROE", 0)

    # day oscilation
    def day_oscilation(self):
        # Fundamentus: Oscilações Dia
        return self.__extract_float("Dia", 0, 1)

    # previous close
    def previous_close(self):
        # Fundamentus: Cotação
        return self.__extract_float("Cotação", 0, 1)

    ####### auxiliary private methods #######
    def __extract_int(self, indicator, occline):
        lines = self.__matchlines(self.code, indicator)

        # with ints, the line where the value is located is always 1
        # after the occurrence of the indicator
        try:
            content = self.__rawdata[self.code][lines[occline]+1]
        except IndexError:
            print(self.__prefix, self.code,
                    "incompatible raw data, consider deleting the stock")
            return None

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

    def __extract_float(self, indicator, occline, offset=2):
        lines = self.__matchlines(self.code, indicator)

        # the value is located almost always 2 lines below indicator,
        # but there are exceptions, so use an adjustable offset
        try:
            content = self.__rawdata[self.code][lines[occline]+offset]
        except IndexError:
            print(self.__prefix, self.code,
                    "incompatible raw data, consider deleting the stock")
            return None

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
