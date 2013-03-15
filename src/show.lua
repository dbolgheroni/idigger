-- show definitions module

local b = require "base"

local M = {}

function M.html (group, output)
    assert(io.output(output))

    io.write(start_html())
    io.write(title("idigger"))

    io.write(last_update())

    local cells = { "#", "A&ccedil;&otilde;es", "E/Y", "ROC" }
    io.write(table_hdr(cells))

    for i, s in ipairs(group) do
        local data = { i,
                       s.code,
                       string.format("%.2f", s.ey),
                       string.format("%.2f", s.roc)
                     }
        io.write(table_row(data))
    end

    io.write(end_html())
end

function start_html ()
    return '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 ' ..
           'Transitional//EN" ' ..
           '"http://www.w3.org/TR/html4/loose.dtd">\n'
end

function end_html ()
    return '</table></body></html>\n'
end

function last_update ()
    return '<p><b>&Uacute;ltima atualiza&ccedil;&atilde;o:</b> ' ..
           os.date("%Y-%m-%d %H:%M") .. '</p>'
end

function title (t)
    local head = ('<head>' ..
                  '<meta http-equiv="Content-Type" ' ..
                  'content="text/html;charset=utf-8">' ..
                  '</head>\n')
    local title = '<title>' .. t .. '</title></head><body>\n'

    return head, title
end

function table_hdr (cells)
    local row = '<table border=1><tr bgcolor="#c0c0c0">'

    for _, c in ipairs(cells) do
        th = '<th>' .. c .. '</th>'
        row = row .. th
    end

    return row .. '</tr>\n'
end

function table_row (cells)
    local row = '<tr>'

    for _, c in ipairs(cells) do
        td = '<td>' .. c .. '</td>'
        row = row .. td
    end

    return row .. '</tr>\n'
end

return M
