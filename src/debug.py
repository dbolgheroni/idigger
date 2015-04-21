# debug
# -*- coding: utf-8 -*-

from __future__ import print_function

prefix = '[dbg]'

def print_stock(stock):
    mv = stock.market_value()
    na = stock.net_assets()
    nnfa = stock.net_nonfixed_assets()
    ebit = stock.ebit()
    evebit = stock.ev_ebit()
    mvnwc = stock.market_value_net_working_capital()
    nwc = stock.net_working_capital()
    nfa = stock.net_fixed_assets()
    ey = stock.earnings_yield()
    roc = stock.return_on_capital()
    pe = stock.price_earnings()
    roe = stock.return_on_equity()
    pc = stock.previous_close()

    print(prefix, stock.code.ljust(6), "Valor de mercado".ljust(24, "."), mv)
    print(prefix, stock.code.ljust(6), "Ativo".ljust(24, "."), na)
    print(prefix, stock.code.ljust(6), "Ativo Circulante".ljust(24, "."), nnfa)
    print(prefix, stock.code.ljust(6), "EBIT".ljust(24, "."), ebit)
    print(prefix, stock.code.ljust(6), "EV / EBIT".ljust(24, "."), evebit)
    print(prefix, stock.code.ljust(6), "P/Cap. Giro".ljust(24, "."), mvnwc)
    print(prefix, stock.code.ljust(6), "Net Working Capital".ljust(24, "."), nwc)
    print(prefix, stock.code.ljust(6), "Net Fixed Assets".ljust(24, "."), nfa)
    print(prefix, stock.code.ljust(6), "EY [%]".ljust(24, "."), ey)
    print(prefix, stock.code.ljust(6), "ROC [%]".ljust(24, "."), roc)
    print(prefix, stock.code.ljust(6), "P/L".ljust(24, "."), pe)
    print(prefix, stock.code.ljust(6), "ROE [%]".ljust(24, "."), roe)
    print(prefix, stock.code.ljust(6), \
            "Cotação [R$]".decode('utf-8').ljust(24, "."), pc)

