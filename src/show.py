"""show module: contains functions to print results/analysis."""

# internal functions to handle HTML
def _start_html():
    return('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 '
           'Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">')

def _end_html():
    return "</table></body></html>"

def _title(t):
    return('<head>'
           '<meta http-equiv="Content-Type" ' 
           'content="text/html;charset=utf-8">'
           '<title>%s</title></head><body><h2>%s</h2>' % (t, t))
 
def _table_hdr(cells):
    row = '<table border=1><tr bgcolor="#c0c0c0">'

    # join() avoids the performance cost of operations like a += b for
    # string concatenation on non-CPython implementations (like JPython)
    for c in cells:
        th = "<th>%s</th>" % c
        row = ''.join([row, th])

    row = ''.join([row, "</tr>"])
    return row

def _table_row(cells):
    row = "<tr>"

    # join() avoids the performance cost of operations like a += b for
    # string concatenation on non-CPython implementations (like JPython)
    for c in cells:
        td = "<td>%s</td>" % c
        row = ''.join([row, td])

    row = ''.join([row, "</tr>"])
    return row

# interface
def show(sector, output, driver="html", title="idigger"):
    """Output the results in a table.

    There are optional parameters defined, which are:

    title=  Defines the title that will appear on output (defaults to
            'idigger').
    driver= Defines the file format. Available options are 'html' and
            'text' (defaults to 'html').

    """

    if driver == "text": 
        # print header
        print("Ação".ljust(9),
              "P/L".rjust(6),
              #"ordem P/L".rjust(9),
              "ROE".rjust(6), file=output) # adjust to debug
              #"ordem ROE".rjust(9),
              #"ordem Greenblatt".rjust(16), file=output)

        # print stocks
        for s in sector:
            print(s.code.ljust(9),
                  str(s.pe).rjust(6),
                  #str(s.pe_order).rjust(9),
                  str(s.roe).rjust(6), file=output) # adjust to debug
                  #str(s.roe_order).rjust(9),
                  #str(s.greenblatt_order).rjust(16), file=output)

    if driver == "html":
        print(_start_html(), file=output)
        print(_title(title), file=output)

        hdr = ["Ações", "P/L", "ROE"]
        print(_table_hdr(hdr), file=output)

        for s in sector:
            row = [s.code, s.pe, s.roe]
            print(_table_row(row), file=output)
        
        print(_end_html(), file=output)
