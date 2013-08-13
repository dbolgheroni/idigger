# module with functions to print results/analysis

import datetime

from idiggerconf import *

style = ('<style>\n'
         'table,th,td { '
         'border:2px solid white; border-collapse:collapse }\n'
         'th { background:#778899; font-family:sans-serif }\n'
         'td { background:#f5f5f5; font-family:Courier New }\n'
         'td.ufloat { text-align:right }\n'
         'td.float { text-align:right; color:#ff0000 }\n'
         '</style>')

# internal functions to handle HTML
def _start_html():
    return('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 '
           'Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">')

def _end_html():
    return "</table></body></html>"

def _title(t):
    head = ('<head>'
            '<meta http-equiv="Content-Type" ' 
            'content="text/html;charset=utf-8">')
    head = ''.join([head, style])
    title = '<title>{0}</title></head>\n<body>'.format(t)

    updatet = datetime.datetime.now()
    agora = updatet.strftime(showdatef)
    update = ('<p><b>&Uacute;ltima atualiza&ccedil;&atilde;o:</b> '
              '{0}</p>'.format(agora))

    return head + title + update
 
def _table_hdr(cells):
    row = '<table><tr>'

    for c in cells:
        th = '<th>{0}</th>'.format(c)
        row = ''.join([row, th])

    row = ''.join([row, '</tr>'])
    return row

def _table_row(cells):
    row = '<tr>'

    for c in cells:
        try:
            float(c)

            if c >= 0:
                td = '<td class="ufloat">{0}</td>'.format(c)
            else:
                td = '<td class="float">{0}</td>'.format(c)
        except ValueError:
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
    hdr = ["#", "A&ccedil;&otilde;es", "EY", "ROC"]
    print(_table_hdr(hdr), file=output)

    # rows
    c = 1
    for s in sector:
        row = [c, s.code, s.ey, s.roc]
        print(_table_row(row), file=output)
        c += 1

    # end html
    print(_end_html(), file=output)
