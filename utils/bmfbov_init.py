#!/usr/bin/env python
#
# IMPORTANT: For some reason, sometimes this script needs to run more
# than one time, since the url often fails to respond at the first try.

import sys
#import urllib.request
import urllib2
#from html.parser import HTMLParser
from HTMLParser import HTMLParser

class StockParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inTag = None;

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if 'lblCodigo' in value:
                self.inTag = True;

    def handle_data(self, data):
        if self.inTag:
            stocks.append(data)

    def handle_endtag(self, tag):
        self.inTag = False

# urlopen() returns a byte object, since it can't automatically
# determine the encoding it receives from the server. So, we use
# decode(), since it's specified in the content.
try:
    #html = urllib.request.urlopen("http://www.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=IBrA&idioma=pt-br").read().decode('utf-8')
    html = urllib2.urlopen("http://www.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=IBrA&idioma=pt-br").read().decode('utf-8')
except ConnectionResetError:
    print("can't connect to BMF&Bovespa, try running it again")
    exit(1)

stocks = []
parser = StockParser()
parser.feed(html)

for s in stocks:
    print(s)
