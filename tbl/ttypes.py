__docformat__ = "google"

"""
    Definition of types that can be stored in columns and methods to check and get type of a variable
    and convert between types.
"""

from typing import TypeVar, Generic
from datetime import datetime, date

ALLOWED_TYPES = ['i', 'f', 'd', 's']   # int, float, datetime, string
MAX_STRING_LEN_NUMPY = 100             # IF CHANGED UPDATE BELOW TOO FOR s AND d
MAX_STRING_DATE_LEN_NUMPY = 20         # IF CHANGED UPDATE BELOW TOO FOR s AND d
NUMPY_TYPE = { 'i' : 'i8', 'f' : 'f8', 's' : 'S100', 'd' : 'S20'}
    
def isTypeStr(stype: str) -> bool:
    """ Returns True if string stype represents one of the allowed types.
    """
    return stype in ALLOWED_TYPES
    
def getTypeConverter(old: str, new: str, fmt: str = None):
    """ Returns a function used to convert data from old type to new type. 
        
        Args:        
            old: type that must be converted.
            new: new type.
            fmt: format used to convert from old type to string. 
                 Only required to convert date from string and to convert float and date to string.
        Returns:
            A tuple(f, fmt), where f: converter and  fmt is the format used to make conversion (string or None).
         
        NOTE: Only conversions from string to any type, and from any type to string are implemented. 
    """
    assert isTypeStr(old), old
    assert isTypeStr(new), new 
    
    if old == "s":
        if new == "i": 
            return int, None
        elif new == "f":
            return float, None #Test if this works. 
        elif new == "d":
            assert fmt, "Missing format to convert to date"
            fmt_date = fmt
            return lambda sstr: datetime.strptime(sstr, fmt_date), fmt_date
        elif new == "s": 
            fmt_str = fmt if fmt else "%s" # useful to print strings with some specific format
            return lambda f: fmt_str%(f), fmt_str
        
    elif old == "i" and new == "s":
        fmt_int = fmt if fmt else "%d"
        return lambda f: fmt_int%(f), fmt_int
    
    elif old == "f" and new == "i":
        return int, None
    
    elif old == "f" and new == "s":
        fmt_float = fmt if fmt else "%g"
        return lambda f: fmt_float%(f), fmt_float
    
    elif old == "d" and new == "s":
        assert fmt, "Missing format to convert to string"
        fmt_date = fmt
        return lambda x: datetime.strftime(x, fmt_date), fmt_date
    else:
        assert False, "Converting between %s and %s is not supported"%(old, new)
        

def isDateStr(sstr: str, fmt: str) -> bool:
    """ Returns True if sstr can be interpreted as a date.
        
        Args:
            sstr: string that may represent date.
            fmt: format for date, e.g. %d/%m/%Y.
    """
    try:
        d = datetime.strptime(sstr, fmt)
        if isinstance(d, datetime):
            return True
        else:
            return False
    except ValueError:
        return False


def getTypeStr(sstr: str, fmt_date: str = None) -> str:
    """ Returns interpreted type for sstr.
        
        Types are checked in the following order: int, float, date, string.
        
        Args:
            sstr: string that represents a single element of data.
            fmt_date: string that specifies format that should be used to parse a date, e.g. %d/%m/%Y.
        
        Returns: 
            A single character that specifies the type associated to the input string.
    """
    assert isinstance(sstr, str)
    #print("sstr: %s"%(sstr))
    
    try:
        i = int(sstr)
        return "i"
    except:
        #print("  FAILED INT")
        pass 
     
    try:
        f = float(sstr)
        return "f"
    except:
        #print("  FAILED FLOAT")
        pass 
    
    if fmt_date:
        try:
            f = isDateStr(sstr, fmt_date)
            if f:
                return "d"
            else:
                pass
        except ValueError:
            #print("  FAILED DATE")
            pass 
    
    try:
        f = str(sstr)
        return "s"
    except:
        #print("  FAILED STR")
        pass 
        
    assert False, "Unknown type for: " + str(sstr)
            
def getType(val):
    """ Returns a single character that specifies the type of val.
        
        Args: 
            val: int, float, date or string.
    """
    #print(val)
    #print("input: " + str(type(val)) )
    if isinstance(val, int):
        return "i"
    elif isinstance(val, float):
        return "f"
    elif isinstance(val, date):
        return "d"
    elif isinstance(val, str):
        return "s"
    else:
        assert False, "Unknown type for: " + str(val)
        
def getH5TypeStr(stype: str) -> str:
    """ Given a string that describes one of the types that can stored in a column, 
        returns the corresponding type that is used to store data in HDF5 files.
        
        Args:
            stype: string, e.g. "i", "f" or "d".
            
        NOTE: Dates are saved as strings.
    """
    assert (stype in ALLOWED_TYPES)
    return NUMPY_TYPE[stype]
    
if __name__ == "__main__":
    pass
    #print(Types.getType(1.0))
    #print(Types.getType(1))
    #print(Types.getType("1.0"))
    #print(Types.getType("02/06/1998"))

    #print(Types.isDate("01/june/1988"))
