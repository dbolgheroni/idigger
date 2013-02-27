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

local fmpath = base.datapath .. "/" .. base.today .. "-fm" 

-- class variable
local rawdata = {}

-- fetch data from provider
function M.fetch (s)
    -- TODO: socket module with coroutines
    local filepath = fmpath .. "/" .. string.lower(s) .. ".html"
    command = "curl --create-dirs -so " .. filepath .. " 'http://www.fundamentus.com.br/detalhes.php?papel=" .. s .. "'" 

    print("downloading " .. s .. " stock data into " .. filepath)
    os.execute(command)
end

-- earnings yield
function M.extract_ey (s)
    -- ey = ebit / ev
    local ey
    if pcall(function ()
        ey = 1 / extract_evEbit(s)
    end) then
        return ey * 100
    else
        return nil
    end
end

-- return on capital
function M.extract_roc (s)
    local roc
    if pcall(function ()
        roc = extract_ebit(s) / (extract_netWorkingCapital(s) + extract_netFixedAssets(s))
    end) then
        return roc * 100
    else 
        return nil
    end
end

-- debug as shown in Fundamentus
function M.debug (s)
    print("debug for " .. s)
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

    print("  (fm) Valor de mercado    ", mv)
    print("  (fm) Ativo               ", na)
    print("  (fm) Ativo Circulante    ", nnfa)
    print("  (fm) EBIT                ", ebit)
    print("  (fm) EV/EBIT             ", evebit)
    print("  (fm) P/Cap. Giro         ", mvnwc)
    print("  (..) Net Working Capital ", nwc)
    print("  (..) Net Fixed Assets    ", nfa)
    print("  (in) EY [%]              ", ey)
    print("  (in) ROC [%]             ", roc)
end

-- store all raw data in a class variable
function M.init ()
    for _, s in ipairs(stocklist) do
        s = string.lower(s)
        local filepath = fmpath .. "/" .. s .. ".html"
        io.input(filepath)

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
    else
        return nil
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
    else
        return nil
    end
end

-- extract integer
-- s: stock; p: pattern; o: nth-line occurrence in the data file
function _extract_integer (s, p, o)
    s = string.lower(s)

    local lines = __matchlines(s, p)
    local raw_value = rawdata[s][lines[o] + 1]

    local nodots = string.gsub(raw_value, "%.", "")
    local match = string.match(nodots, "%d+", 24)
    local value = tonumber(match)

    return value 
end

-- extract float
-- s: stock; p: pattern; o: nth-line occurrence in the data file
function _extract_float (s, p, o)
    s = string.lower(s)

    -- extract the value from a raw line of data
    local lines = __matchlines(s, p)

    local raw_value = rawdata[s][lines[o] + 2]

    -- process raw data
    local match = string.match(raw_value, "[-]?%d+,%d+")
    local comma
    if match then
        nocomma = string.gsub(match, ",", ".")
    else
        return nil
    end

    local value = tonumber(nocomma)

    return value
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
