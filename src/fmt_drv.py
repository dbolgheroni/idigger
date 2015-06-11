# driver module to handle Fundamentus provider
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import re
import time
#import urllib.request
#import urllib.error
import urllib2
#from html.parser import HTMLParser
from HTMLParser import HTMLParser

from conf import *
from models import Stock


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

    def extract_int(self, value):
        # remove points
        regex = re.compile(r"\.")
        try:
            c1 = regex.sub("", value)
        except TypeError:
            #print("lookup=", self.__lookup, ", value=", value, sep="")
            return None

        # extract the number per se
        regex = re.compile(r"(?P<int>\d+)")
        c2 = regex.search(c1)

        if c2:
            return int(c2.group('int'))


    def extract_float(self, value):
        regex = re.compile(r"(?P<float>[-]?\d+,\d+)")
        try:
            match = regex.search(value)
        except TypeError:
            return None

        if match:
            c1 = match.group('float')

            # Brazil uses 3,14 instead of 3.14 (computer notation), so
            # change commas for points
            regex = re.compile(r",")
            c2 = regex.sub(".", c1)
            return float(c2)

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
        self.code = c

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
                    #iurl = urllib.request.urlopen(url)
                    iurl = urllib2.urlopen(url)
                    break
                #except urllib.error.URLError:
                except urllib2.URLError:
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
            ourl.write(self.__contents.encode('utf-8'))

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

        # instance variables for the used values
        self._ey = self.earnings_yield()
        self._roc = self.return_on_capital()
        self._pe = self.price_earnings()
        self._roe = self.return_on_equity()
        self._pc = self.previous_close()

        # add to a tracking class variable for the sorts algorithms
        # this should give a cleaner interface, such as Stock.sort_x()
        self.add(self)

    # market value
    def market_value(self):
        # Fundamentus: Valor de mercado (P)
        parser = FundamentusParser('Valor de mercado')
        parser.feed(self.__contents)

        return parser.extract_int(parser.result)

    # net assets
    def net_assets(self):
        # Fundamentus: Ativo
        parser = FundamentusParser('Ativo')
        parser.feed(self.__contents)

        return parser.extract_int(parser.result)

    # net non-fixed assets
    def net_nonfixed_assets(self):
        # Fundamentus: Ativo Circulante
        parser = FundamentusParser('Ativo Circulante')
        parser.feed(self.__contents)

        return parser.extract_int(parser.result)

    # ebit
    def ebit(self):
        # Fundamentus: EBIT
        parser = FundamentusParser('EBIT')
        parser.feed(self.__contents)

        return parser.extract_int(parser.result)

    def ev_ebit(self):
        # Fundamentus: EV / EBIT
        parser = FundamentusParser('EV / EBIT')
        parser.feed(self.__contents)

        return parser.extract_float(parser.result)

    # market value / net working capital
    def market_value_net_working_capital(self):
        # Fundamentus: P/Cap. Giro
        parser = FundamentusParser('P/Cap. Giro')
        parser.feed(self.__contents)

        return parser.extract_float(parser.result)

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
            return round(ey * 100, 2)

    # return on capital (ROC)
    def return_on_capital(self):
        ebit = self.ebit()
        nwc = self.net_working_capital()
        nfa = self.net_fixed_assets()

        if ebit and nwc and nfa:
            roc = ebit / (nwc + nfa)
            return round(roc * 100, 2)

    # price-earnings (P/E)
    def price_earnings(self):
        # Fundamentus: P/L
        parser = FundamentusParser('P/L')
        parser.feed(self.__contents)

        return parser.extract_float(parser.result)

    # return on equity (ROE)
    def return_on_equity(self):
        # Fundamentus: ROE
        parser = FundamentusParser('ROE')
        parser.feed(self.__contents)

        return parser.extract_float(parser.result)

    # previous close
    def previous_close(self):
        # Fundamentus: Cotação
        parser = FundamentusParser('Cotação')
        parser.feed(self.__contents)

        return parser.extract_float(parser.result)
