# module with functions to print results/analysis

import datetime

from idiggerconf import *

style = ('<style>\n'
         'table,th,td { '
         'border:2px solid white; border-collapse:collapse }\n'
         'th { background:#778899; font-family:sans-serif }\n'
         'td { background:#f5f5f5; font-family:Courier New }\n'
         'td.pos { text-align:right }\n'
         'td.sdigit { text-align:right; color:#0000ff }\n'
         'td.udigit { text-align:right; color:#ff0000 }\n'
         'td.nodata { text-align:right; background:#ff0000 }\n'
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

def _table_row(pos, code, values):
    row = '<tr><td class="pos">{0}</td><td>{1}</td>'.format(pos, code)

    for v in values:
        try:
            float(v)

            if v >= 0:
                td = '<td class="sdigit">{0}</td>'.format(v)
            else:
                td = '<td class="udigit">{0}</td>'.format(v)
        except TypeError:
            if not v:
                td = '<td class="nodata"></td>'

        row = ''.join([row, td])

    row = ''.join([row, '</tr>'])
    return row

# interface
def show(sector, output, title, tablehdr):
    # html header
    print(_start_html(), file=output)
    print(_title(title), file=output)

    # TODO generalize
    # table header
    print(_table_hdr(tablehdr), file=output)

    # rows
    p = 1
    for s in sector:
        v = [s.ey, s.roc, s.pe, s.roe, s.do, s.pc]
        print(_table_row(p, s.code, v), file=output)
        p += 1

    # end html
    print(_end_html(), file=output)
