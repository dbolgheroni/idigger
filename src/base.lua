-- common definitions and methods for all idigger utilities

local M = {}

M.basepath = os.getenv("HOME") .. "/.idigger"
M.datapath = M.basepath .. "/data"

M.conffile = M.basepath .. "/idiggerrc.lua"

M.truncate = function (n, d)
    d = 1 / 10^d
    n = n - n%d

    return n
end

return M
