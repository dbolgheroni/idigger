--[[
module to work with Fundamentus provider

A method name convention used in this driver:

M.extract_whatever (): main methods (interface)
extract_whatever   (): aux methods used by main methods, not exposed
_extract_whatever  ():      basic aux methods to not duplicate code
__method           (): very basic aux methods used in _extract_whatever()
--]]

local base = require "base"

local M = {}

local fmpath = base.datapath .. "/" .. os.date("%Y%m%d") .. "-fm" 

local prefix = "[fmt] "

-- class variable
local rawdata = {}

-- fetch data from provider
function M.fetch (s)
    -- TODO: socket module with coroutines, and return status codes
    local filepath = fmpath .. "/" .. string.lower(s) .. ".html"
    command = "curl --create-dirs -so " .. filepath .. " 'http://www.fundamentus.com.br/detalhes.php?papel=" .. s .. "'" 

    return os.execute(command)
end

-- earnings yield (EY)
function M.extract_ey (s)
    -- ey = ebit / ev
    local ey
    if pcall(function ()
        ey = 1 / extract_evEbit(s)
    end) then
        return base.truncate(ey * 100, 2)
    end
end

-- return on capital (ROC)
function M.extract_roc (s)
    local roc
    if pcall(function ()
        roc = extract_ebit(s) / (extract_netWorkingCapital(s) + extract_netFixedAssets(s))
    end) then
        return base.truncate(roc * 100, 2)
    end
end

-- debug info extracted from Fundamentus and other internal formulas
function M.debug (s)
    local mv = extract_marketValue (s)
    local na = extract_netAssets(s)
    local nnfa = extract_netNonFixedAssets(s)
    local ebit = extract_ebit(s)
    local evebit = extract_evEbit(s)
    local mvnwc = extract_marketValueNetWorkingCapital (s)
    local nwc = extract_netWorkingCapital (s)
    local nfa = extract_netFixedAssets(s)
    local ey = M.extract_ey(s)
    local roc = M.extract_roc(s)

    local novalue = "*******"
    print(prefix .. s .. " Valor de mercado " .. (mv or novalue))
    print(prefix .. s .. " Ativo " .. (na or novalue))
    print(prefix .. s .. " Ativo Circulante " .. (nnfa or novalue))
    print(prefix .. s .. " EBIT " .. (ebit or novalue))
    print(prefix .. s .. " EV/EBIT " .. (evebit or novalue))
    print(prefix .. s .. " P/Cap. Giro " .. (mvnwc or novalue))
    print(prefix .. s .. " Net Working Capital " .. (nwc or novalue))
    print(prefix .. s .. " Net Fixed Assets " .. (nfa or novalue))
    print(prefix .. s .. " EY [%] " .. (ey or novalue))
    print(prefix .. s .. " ROC [%] " .. (roc or novalue))
end

-- load raw data fetched into internal module tables 
function M.init (l)
    for _, s in ipairs(l) do
        s = string.lower(s)
        local filepath = fmpath .. "/" .. s .. ".html"
        if not pcall(function () io.input(filepath) end) then
            print(prefix .. "couldn't open " .. filepath)
        end

        local ldata = {}
        for line in io.lines() do
            ldata[#ldata + 1] = line
        end

        rawdata[s] = ldata
    end
end

-- net fixed assets
function extract_netFixedAssets (s)
    local nfa
    if pcall(function ()
        nfa = extract_netAssets(s) - extract_netNonFixedAssets(s)
    end) then
        return nfa
    end
end

-- net assets
function extract_netAssets (s)
    -- Fundamentus: Ativo
    return _extract_integer(s, "Ativo", 8)
end

-- net non-fixed assets
function extract_netNonFixedAssets (s)
    return _extract_integer(s, "Ativo Circulante", 3)
end

-- ebit
function extract_ebit (s)
    return _extract_integer(s, "EBIT", 6)
end

-- ev / ebit
function extract_evEbit (s)
    return _extract_float(s, "EBIT", 5)
end

-- market value / net working capital
function extract_marketValueNetWorkingCapital (s)
    -- Fundamentus: P/Cap. Giro
    return _extract_float(s, "Cap%. Giro", 1)
end

-- market value 
function extract_marketValue (s)
    -- Fundamentus: Valor de mercado (P)
    return _extract_integer(s, "Valor de mercado", 1)
end

-- net working capital
function extract_netWorkingCapital (s)
    -- in Portuguese: Capital de Giro
    local nwc
    if pcall(function ()
        nwc = extract_marketValue(s) / extract_marketValueNetWorkingCapital(s)
    end) then
        return nwc
    end
end

-- extract integer
function _extract_integer (s, p, o) -- (s)tock; (p)attern; (o)cc. line
    s = string.lower(s)

    -- extract the value from a raw line of data
    local lines = __matchlines(s, p)
    local raw_value = rawdata[s][lines[o] + 1]

    local nodots = string.gsub(raw_value, "%.", "")
    local match = string.match(nodots, "%d+", 24)
    if match then
        local value = tonumber(match)
        return value
    end
end

-- extract float
function _extract_float (s, p, o) -- (s)tock; (p)attern; (o)cc. line
    s = string.lower(s)

    -- extract the value from a raw line of data
    local lines = __matchlines(s, p)
    local raw_value = rawdata[s][lines[o] + 2]

    -- process raw data
    local match = string.match(raw_value, "[-]?%d+,%d+")
    if match then
        local nocomma = string.gsub(match, ",", ".")
        local value = tonumber(nocomma)

        return value
    end
end

-- match lines the given pattern occurs
function __matchlines (s, p)
    local i = 1
    local matches = {}

    for _, line in ipairs(rawdata[s]) do
        if string.match(line, tostring(p)) then
            matches[#matches + 1] = i
        end

        i =  i + 1
    end

    return matches
end

return M
