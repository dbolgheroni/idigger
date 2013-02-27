-- common definitions and methods for all idigger utilities

local M = {}

M.basepath = os.getenv("HOME") .. "/.idigger"
M.datapath = M.basepath .. "/data"

M.conffile = M.basepath .. "/idiggerrc.lua"

M.today = os.date("%Y%m%d")

return M
