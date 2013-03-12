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

-- fetchfiles option from conf
if fetchfiles then
    for _, s in ipairs(stocklist) do
        print(prefix .. "downloading " .. s .. " stock data")
        fm.fetch(s)
    end
end

-- loads raw data fetched into internal module tables (REQUIRED)
fm.init()

-- print debug info
if debug then
    for _, s in ipairs(stocklist) do fm.debug(s) end
end

-- instantiate stocks
sector = {}
for _, s in ipairs(stocklist) do
    local obj = Stock:new{code = s}

    obj.ey = fm.extract_ey(s)
    obj.roc = fm.extract_roc(s)

    -- FILTER code
    -- only instantiate "good" stocks
    if obj.ey > 0 and obj.roc > 0 then
        sector[#sector + 1] = obj
    else
        print(prefix .. "invalid value for " .. s .. ", skipping")
    end
end

-- class methods
Stock:sort_ey(sector)
Stock:sort_roc(sector)
Stock:sort_greenblatt(sector)

print(prefix .. "generating HTML output")
show.html(sector, outputfile)

print(prefix .. "run time: " .. os.clock())
