from datetime import datetime, date

class Types:
    FMT_DATE  = "%d/%m/%Y"
    FMT_FLOAT = "%6.2f"
    ALLOWED_TYPES = ["i", "f", "d", "s"]
    MAX_STRING_LEN_NUMPY = 100             # IF CHANGED UPDATE BELOW TOO.
    MAX_STRING_DATE_LEN_NUMPY = 20         # IF CHANGED UPDATE BELOW TOO.
    NUMPY_MAP = { "i" : "i8", "f" : "f8", "s" : "S100", "d" : "S20"}
    
    @staticmethod
    def getH5Type(stype):
        """ Given a string that describes one of the types accepted for
            a column, returns the corresponding type accepted for h5py.
            Dates are saved as strings.
        """
        assert (stype in Types.ALLOWED_TYPES)
        return Types.NUMPY_MAP[stype]
    
    @staticmethod
    def isType(stype):
        """ Returns True if string stype represents one of the allowed types.
        """
        # I do not think we can optimize the native way
        return stype in Types.ALLOWED_TYPES
    
    @staticmethod
    def getConverter(old, new, fmt = None):
        """ Returns a function used to convert data from old type to new type. 
            Only conversions from string to any type, and from any type to string
            are implemented for now. 
            
            :param fmt: format used to convert from old type to string.
                        If not present, then Types.FMT_FLOAT and Types.FMT_DATE 
                        are used as default.
            :returns a tuple(f, fmt), where f: converter and 
                                          fmt: format used to make conversion (string or None).
        """
        assert Types.isType(old), old
        assert Types.isType(new), new 
        
        if old == "s":
            if new == "i": 
                return int, None
            elif new == "f":
                return float, Types.FMT_FLOAT #Test if this works. 
            elif new == "d":
                fmt_date = fmt if fmt else Types.FMT_DATE
                return lambda sstr: datetime.strptime(sstr, fmt_date), fmt_date
            else: 
                return str, None
        
        if old == "i" and new == "s":
            return str, None
        elif old == "f" and new == "s":
            fmt_float = fmt if fmt else Types.FMT_FLOAT
            return lambda f: fmt_float%(f), fmt_float
        elif old == "d" and new == "s":
            fmt_date = fmt if fmt else Types.FMT_DATE
            return lambda x: datetime.strftime(x, fmt_date), fmt_date
        elif old == "s" and new == "s":
            assert False, "Converting to same type %s"%(old) # it could be possible, but a waste of CPU
        else:
            assert False, "Converting betweem %s and %s is not supported"%(old, new)
        
    @staticmethod
    def isDate(sstr, fmt=None):
        """ Returns whether the string can be interpreted as a date.
            :param sstr: string that may represent date.
            :param fmt: format for date. If not passed then, Types.FMT_DATE used. 
        """
        fmt = fmt if fmt else Types.FMT_DATE
        try:
            d = datetime.strptime(sstr, fmt)
            if isinstance(d, datetime):
                return True
            else:
                return False
        except ValueError:
            return False

    @staticmethod
    def getStrType(sstr, fmt_date = None):
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
        
        try:
            f = Types.isDate(sstr, fmt_date)
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
            
    @staticmethod
    def getType(val):
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

if __name__ == "__main__":
    pass
    #print(Types.getType(1.0))
    #print(Types.getType(1))
    #print(Types.getType("1.0"))
    #print(Types.getType("02/06/1998"))

    #print(Types.isDate("01/june/1988"))
