-- Stock class

-- instance values
Stock = { ey = 0, roc = 0 }

-- constructor
function Stock:new(o)
    o = o or {}
    setmetatable(o, self)
    self.__index = self
    return o
end
