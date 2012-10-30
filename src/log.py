"""log module: contains simple function to decorate (not in a Python
sense) output, instead of using the more complex 'logging' module."""

# variable number of arguments
def log(*pos, **keyw):
    """Print messages to console. Emulates 'print' function (as with
    end=).
    
    """

    if keyw.get("prefix", True):
        print(end="[idigger] ")

    if "end" in keyw:
        print(*pos, end=keyw["end"])
    else:
        print(*pos)