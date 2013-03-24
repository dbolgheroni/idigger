-- common definitions and methods for all idigger utilities

local M = {}

M.confdir = os.getenv("HOME") .. "/.idigger/"
M.datadir = M.confdir .. "data/"

M.conffile = M.confdir .. "config.lua"

return M
