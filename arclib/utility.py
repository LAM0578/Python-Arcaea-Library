
_BOOL_STRING = ['false', 'true']

def parseBool(raw:str):
    if raw not in _BOOL_STRING:
        return False
    return _BOOL_STRING.index(raw) != 0

def tryParseInt(raw:str):
    try:
        return True, int(raw)
    except ValueError:
        return False, 0

def parseFloat(raw:str):
    return 0.0 if raw == '.' else float(raw)

def tryParseFloat(raw:str):
    try:
        return True, float(raw)
    except ValueError:
        return False, 0

def tryParseNumber(raw:str):
    try:
        return int(raw)
    except ValueError:
        return float(raw)

def tryParseNumberWithString(raw:str):
    try:
        return int(raw)
    except ValueError:
        try:
            return float(raw)
        except ValueError:
            return raw

def lastIndex(lst:list, item):
    try:
        return len(lst) - lst[::-1].index(item) - 1
    except ValueError:
        return -1
