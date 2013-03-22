-- show definitions module

local b = require "base"

local M = {}

function M.html (group, output)
    assert(io.output(output))

    io.write(start_html())
    io.write(title("idigger"))

    io.write(last_update())

    local hdr = { "#", "A&ccedil;&otilde;es", "E/Y", "ROC" }
    io.write(table_hdr(hdr))

    for i, s in ipairs(group) do io.write(table_row(i, s)) end

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

function table_hdr (hdr)
    local row = '<table style="border-collapse:collapse" border=1><tr bgcolor="#c0c0c0">'

    for _, c in ipairs(hdr) do
        th = '<th>' .. c .. '</th>'
        row = row .. th
    end

    return row .. '</tr>\n'
end

function table_row (i, s)
    -- no Javascript, no CSS, just pure HTML
    local row = '<tr>'
    local td

    -- #
    td = '<td>' .. i .. '</td>'
    row = row .. td

    -- code
    td =  '<td>' .. s.code .. '</td>'
    row = row .. td

    -- ey
    if s.ey == -math.huge then
        -- grey
        td = '<td><font color="#c0c0c0">no data</font></td>'
    elseif s.ey < 0 then
        -- red
        td = '<td><font color="#ff0000">' .. s.ey .. '</font></td>'
    else
        -- default
        td = '<td>' .. s.ey .. '</td>'
    end
    row = row .. td

    -- roc
    if s.roc == -math.huge then
        -- grey
        td = '<td><font color="#c0c0c0">no data</font></td>'
    elseif s.roc < 0 then
        -- red
        td = '<td><font color="#ff0000">' .. s.roc .. '</font></td>'
    else
        -- default
        td = '<td>' .. s.roc .. '</td>'
    end
    row = row .. td

    return row .. '</tr>\n'
end

return M
