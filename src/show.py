# module with functions to print results/analysis

import datetime

from idiggerconf import *

# internal functions to handle HTML
def _start_html():
    return('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 '
           'Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">')

def _end_html():
    return "</table></body></html>"

def _title(t):
    # format in output isn't the same as in log, so redefine
    head = ('<head>'
            '<meta http-equiv="Content-Type" ' 
            'content="text/html;charset=utf-8">'
            '</head>')
    title = '<title>{0}</title></head><body>'.format(t)

    updatet = datetime.datetime.now()
    agora = updatet.strftime(showdatef)
    update = ('<p><b>&Uacute;ltima atualiza&ccedil;&atilde;o:</b> '
              '{0}</p>'.format(agora))

    return head + title + update
 
def _table_hdr(cells):
    row = '<table border=1><tr bgcolor="#c0c0c0">'

    # join() avoids the performance cost of operations like a += b for
    # string concatenation on non-CPython implementations (like JPython)
    for c in cells:
        th = '<th>{0}</th>'.format(c)
        row = ''.join([row, th])

    row = ''.join([row, '</tr>'])
    return row

def _table_row(cells):
    row = '<tr>'

    # join() avoids the performance cost of operations like a += b for
    # string concatenation on non-CPython implementations (like JPython)
    for c in cells:
        td = '<td>{0}</td>'.format(c)
        row = ''.join([row, td])

    row = ''.join([row, '</tr>'])
    return row

# interface
def show(sector, output, title="idigger"):
    # html header
    print(_start_html(), file=output)
    print(_title(title), file=output)

    # table header
    #hdr = ["A&ccedil;&otilde;es", "P/L", "ROE",
    #        "ordem P/L", "ordem ROE", "ordem Greenblatt"]
    hdr = ["A&ccedil;&otilde;es", "EY", "ROC"]
    print(_table_hdr(hdr), file=output)

    # rows
    for s in sector:
        #row = [s.code, s.pe, s.roe]
        #row = [s.code, s.pe, s.roe,
        #        s.pe_order, s.roe_order, s.greenblatt_order]
        row = [s.code, s.ey, s.roc]
        print(_table_row(row), file=output)

    # end html
    print(_end_html(), file=output)
