-- common definitions and methods for all idigger utilities

local M = {}

M.confdir = os.getenv("HOME") .. "/.idigger"
M.datadir = M.confdir .. "/data"

M.conffile = M.confdir .. "/config.lua"

M.truncate = function (n, d)
    d = 1 / 10^d
    n = n - n%d

    return n
end

return M
