-- Stock class

-- instance values
Stock = {
    ey = -math.huge,
    roc = -math.huge,
    ey_order = 0,
    roc_order = 0,
    greenblatt_order = 0
}

-- constructor
function Stock:new(o)
    o = o or {}
    setmetatable(o, self)
    self.__index = self
    return o
end

-- EY sort
function Stock:sort_ey (group)
    table.sort(group, function (a, b) return a.ey > b.ey end) -- reverse order

    for i, s in ipairs(group) do
        s.ey_order = i
    end
end

-- ROC sort
function Stock:sort_roc (group)
    table.sort(group, function (a, b) return a.roc > b.roc end) -- reverse order

    for i, s in ipairs(group) do
        s.roc_order = i
    end
end

-- Greenblatt sort
function Stock:sort_greenblatt (group)
    for _, s in ipairs(group) do
        s.greenblatt_order = s.ey_order + s.roc_order
    end

    table.sort(group, function (a, b)
        return a.greenblatt_order < b.greenblatt_order
    end)
end
