#!/usr/bin/env lua
--[[
Copyright (c) 2012, Daniel Bolgheroni. All rights reserved.
 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.

  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in
     the documentation and/or other materials provided with the
     distribution.

THIS SOFTWARE IS PROVIDED BY DANIEL BOLGHERONI ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL DANIEL BOLGHERONI OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--]]

local b = require "base"
local fm = require "fm"
local show = require "show"
require "stock"

prefix = "[idg] "

-- international date format (ISO 8601)
print(prefix .. "idigger started at " .. os.date("%Y-%m-%d %H:%M:%S"))

print(prefix .. "loading conf file " .. b.conffile)
local conf = dofile(b.conffile) -- TODO: assert

if debug then print(prefix .. "debug enabled") end

-- fetch option from conf
local dlok = {}
if fetch then
    local dlstatus

    for _, s in ipairs(fetchlist) do
        print(prefix .. "fetching " .. s .. " raw data")
        dlstatus = fm.fetch(s)

        if dlstatus then
            dlok[#dlok + 1] = s
        else
            print(prefix .. "error fetching " .. s .. " raw data")
        end
    end
else
    dlok = fetchlist
end

-- load raw data fetched into internal module tables (REQUIRED)
fm.init(dlok)

-- print debug info
if debug then
    for _, s in ipairs(dlok) do fm.debug(s) end
end

-- instantiate all stocks
print(prefix .. "extracting info from raw data")
Stocks = {}
for _, s in ipairs(dlok) do
    --local obj = Stock:new{code = s}
    local obj = Stock:new{}

    obj.ey = fm.extract_ey(s)
    obj.roc = fm.extract_roc(s)

    --Stocks[#Stocks + 1] = obj
    Stocks[s] = obj
end

-- main
for _, group in ipairs(active) do
    local Group = {}

    for _, s in ipairs(group) do
        -- FILTER
        if Stocks[s].ey > 0 and Stocks[s].roc > 0 then
            Group[#Group + 1] = Stocks[s]
            Group[#Group].code = s
        else
            print(prefix .. "group " .. group.name .. ", stock "
                  .. s .. " filtered")
        end
    end

    Stock:sort_ey(Group)
    Stock:sort_roc(Group)
    Stock:sort_greenblatt(Group)

    --[[ debug
    for k, v in pairs(Group) do
        print(k, v.code, v.ey, v.roc,
              v.ey_order, v.roc_order, v.greenblatt_order)
    end
    --]]

    print(prefix .. "generating group " .. group.name .. " output (" ..
          group.output .. ")")
    show.html(Group, outputdir .. group.output)
end
