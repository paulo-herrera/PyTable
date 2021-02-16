__docformat__ = "google"

from .ttypes import getType, isTypeStr, getTypeConverter, NUMPY_TYPE
from .helpers import is_iterable
from .required import NUMPY_ON
import sys
import inspect

class Column:
    """ General container to store data as column of a table. 
        Constructor should never be called from outside package. 
    """
    
    def __init__(self, name: str, desc: str = None):
        """ Creates a column with given name. 
        
            Args:
                name: name for this column.
                desc: description for this column [OPTIONAL]. 
                
            NOTE: type of data stored in this column is undefined until data is added calling addData. 
        """
        self.name: str = name
        self.data = []
        self.type: str = None                    # 1 character that indicates type of this column.
        self.fmt: str  = None                    # used to convert dates and float to strings. 
        self.tostr = None                        # converter to string
        self.attrs = {}                          # add attributes to save units, dates, etc
        if desc: self.setAttr("desc", desc)
    
    
    # TODO: ADD TEST
    def like(self, other):
        """ Set this table properties as other.
            
            Args:
                other: table that has the properties to be copied.
            
            Returns:
                This table.
        """
        self.type = other.type
        self.fmt  = other.fmt
        self.tostr = other.tostr
        self.attrs = other.attrs
    
    def setName(self, name: str):
        """ Sets name of this column.
            Returns: This column.
        """
        self.name = name
        return self
    
    def setAttr(self, name: str, value: str):
        """ Sets attribute for this column.
            
            Args:
                name: attribute name.
                value: attribute value.
            
            Returns:
                This table
        """
        self.attrs[name] = value
        return self
    
    def setFormatStr(self, fmt: str):
        """ Sets format used to print or convert elements in this column to strings.
            Returns:
                This column.
        """
        assert self.type, "Format cannot be assigned before assigning type for this column."
        self.tostr, self.fmt = getTypeConverter(self.type, "s", fmt)
        return self
    
    def format(self, idx: int):
        """ Returns a formatted string of element c[idx] in this column.
            Format used to make conversion should have been set calling setFormatStr. 
        """
        s = self.tostr(self.data[idx])
        return s
    
    def addData(self, data, ctype = None):
        """ Adds data to this column. 
            Args:
                data: list or tuple with data of this column.
                      If column already has data, then it is appended.
                      Type of data should match type of this column if already set.
                      It is possible to pass an empty list to create a column that
                      is a placeholder. 
                
                ctype: element of the same type of data stored in this column, e.g.
                      1, 0.1, "s". Only used if self.type has not been assigned.
                      If not present, then type is inferred from the first element in data.
                      This option should be used in combination with an empty list,
                      to create a column that is a placeholder for future data.
            
            Returns:
                This column.
            
            NOTE: Only use this function to append list of many elements. To add 
                  only one element use append instead.
        """
        assert is_iterable(data), "To add individual elements, use append"
        
        if not self.type and len(data) > 0:
            self.type = getType(data[0])
            self.tostr, self.fmt = getTypeConverter(self.type, "s", self.fmt)
        elif self.type and len(data) > 0:           # have to check if types match
            ntype = getType(data[0])
            assert(ntype == self.type)
        elif not self.type and ctype:
            ntype = getType(ctype)
            self.type = ntype
            self.data = data
            self.tostr, self.fmt = getTypeConverter(ntype, "s", self.fmt)
        else:
            assert False
        
        self.data = self.data + data        
        return self
    
    def append(self, e):
        """ Appends element e to this column. 
            Returns: This column.
        """
        # This can be costly, optimize later
        nt = getType(e)
        if not self.type: 
            self.type = nt
        else:
            assert nt == self.type, "self.type: %s, type(e): %s"%(self.type, nt)
        
        self.data.append(e)
        return self
        
    def convert(self, new: str = None, fmt: str = None): 
        """ Converts column data type from current type to new type.
        
            Args:
                new: new type as a one character string (see ttypes.ALLOWED_TYPES).
                     Optional only if old type is string "s" (automatic conversion of strings). 
                fmt: format used to convert dates and floats to strings.
                     If present, then self.fmt is updated to fmt.      
            
            Returns:
                This column.
        """
        assert isTypeStr(new), new
        
        self.fmt = fmt if fmt else self.fmt
        
        old = self.type
        #if old == "s" and not new:
        #    assert len(self.data) > 0
        #    d0 = self.data[0]
        #    new = getTypeStr(d0, self.fmt)
            
        f, fmt = getTypeConverter(old, new, self.fmt)
        dd = []
        for nd in self.data:
            a = f(nd)
            dd.append(a)
            
        self.data = dd
        self.type = new
        
        return self
    
    def indexes(self, filter):
        """ Return a list of indexes of the elements of the column that satisfy:
                filter(i, c[i]) = True
        """
        idx = []
        for i in range(len(self.data)):
            v = self.data[i]
            if filter(i, v): idx.append(i)
        return idx
    
    def at(self, idxs):
        """ Given a list of indexes of elements in this columns, creates a new column.
            
            Args:
                idxs: list or tuple with indexes of elements in this column that
                should be in new column, e.g. list returned by indexes.
                
            Returns:
                A new column with elements specified by idxs.
        """
        assert is_iterable(idxs)
        ndata = []
        for idx in idxs:
            nd = self.data[idx]
            ndata.append(nd)
        
        c = Column(name = self.name + "[idxs]")
        c.addData(ndata)
        return c
        
    def collect(self, filter):
        """ Returns a list of the elements (c[i]) of this column that satisfy:
               filter(i, c[i]) = True
            
            Returns:
                New list of values.
                
            NOTE: If you want a new columns, use column instead.
        """
        values = []
        for i in range(len(self.data)):
            v = self.data[i]
            if (filter(i, v)): values.append(v)
        return values

    def select(self, filter, name = None, desc = None):
        """ Creates a new column taking only the elements of this column that satisfy:
                filter(i, c[i]) = True
            
            Args:
                name: If present, then it is used as name of new column. 
                      Otherwise, name of new column is created as a combination
                      of the name of this column and the filter.
                desc: If present used as descriptor for new column. If not present,
                      then a string representation of the filter is used as descriptor.
                
            Returns:
                A new column with selected elements of this column.
        """
        nd = self.collect(filter)
        if not name: name = "select(" + self.name + ")" 
        if not desc: desc = inspect.getsource(filter)
            
        c = Column(name).addData(nd)
        c.setAttr("selec_filter", desc.strip())
        return c
    
    def remove(self, filter):
        """ Removes elements (e[i]) of this column that satisfy: 
                    filter(i, e[i]) = True
            
            Returns: This column after removing elements.
        """
        ndata = []
        for i in range(len(self.data)):
            v = self.data[i]
            if filter(i, v):
                pass
            else:
                ndata.append(v)
        self.data = ndata
        return self

    def clone(self):
        """ Returns an exact copy that does not shared data with this column (deep-copy)
        """    
        c = Column(self.name)
        c.fmt = self.fmt
        ndata = self.data.copy()
        c.addData(ndata)
        return c

    def apply(self, func):
        """ Creates a new list with elements e: 
                e[i] = func(i, c[i])
            
            Returns: 
                A new list of values
            
            NOTE: If you want to update elements in this column, use map instead.
        """
        nvals = []
        for i in range(len(self.data)):
            d = self.data[i]
            val = func(i, d)
            nvals.append(val)
        return nvals

    def map(self, func):
        """ Updates values of this column as:
                c[i] = func(i, c[i]) 
            
            Args: 
                desc: If True save the string representation of func as description
                      of this column.
                      
            Return: This column.
            
            NOTE: If want a new list of values, use apply instead.
        """
        nvals = []
        for i in range(len(self.data)):
            d = self.data[i]
            self.data[i] = func(i, d)
            
        desc = inspect.getsource(func).strip()
        self.setAttr("map_filter", desc)
        
        return self

    def reduce(self, func, result):
        """ Applies func on each element of this column and returns the final result.
            For example, to compute the minimum value of a column:
               c.reduce(func = lambda (i, e, result): e if e < result else result, result = BIG_NUMBER)
            
            Args:
                func: func(i, e, result), where i is the index of element e and 
                      result is the intial or temporal value of the result. 
                result: initial result. 
            
            Returns:
                The final result of calling func over all elements of this column.
        """
        for i in range(len(self.data)):
            e = self.data[i]
            result = func(i, e, result)
        return result

    def print(self, out = sys.stdout, sep = "\n", fmt = None, writeName = False, start = 0, end = None):
        """ Write elements of column to out.
        
            Args:
                out: a stream like object, e.g. sys.stdout.
                sep: a string used as separator of elements.
                fmt: string that defines format to be used to convert values to strings 
                     [OPTIONAL, USED FOR FLOATS AND DATES].
                writeName: if True, then write name of this column before writing elements.
                start: index of first element that should be printed 
                       [OPTIONAL, DEFAULT = 0]
                end: index of last element that should be printed 
                     [OPTIONAL, DEFAULT=NONE, last element]
        """
        self.fmt = fmt if fmt else self.fmt
        
        if writeName: 
            out.write(self.name)
            out.write(sep)
        
        end = end + 1 if end else len(self.data)
        
        c, fmt = getTypeConverter(self.type, "s", self.fmt)
        for i in range(start, end):
            e = self.data[i]
            s = c(e)
            out.write(s)
            out.write(sep)
    
    def head(self, n, out = sys.stdout, sep = "\n", fmt = None, writeName = False, ):
        """ Prints first n elements of this column.
            
            Args:
                out: a stream like object, e.g. sys.stdout.
                sep: a string used as separator of elements.
                writeName: if True, then write name of this column before writing elements.
                start: index of first element that should be printed [OPTIONAL, DEFAULT = 0]
                end: index of last element that should be printed [OPTIONAL, DEFAULT=NONE, last element]
        """
        end = n - 1 if n < len(self.data) else len(self.data) - 1
        self.print(out, sep, fmt, writeName, start = 0, end = end) # we add 1 later
    
    def tail(self, n, out = sys.stdout, sep = "\n", fmt = None, writeName = False, ):
        """ Prints last n elements of this column.
            
            Args:
                out: a stream like object, e.g. sys.stdout.
                sep: a string used as separator of elements.
                writeName: if True, then write name of this column before writing elements.
                start: index of first element that should be printed [OPTIONAL, DEFAULT = 0]
                end: index of last element that should be printed [OPTIONAL, DEFAULT=NONE, last element]
        """
        end = len(self)
        start = end - n
        self.print(out, sep, fmt, writeName, start = start, end = end - 1) # we add 1 later
    
    def np(self):
        """ Returns a Numpy array that contains data in this column.
            
            Returns: 
                A 1D Numpy array with data in this column. If Numpy is not installed,
                then throws an error.
                
            NOTE: Data is not shared with the array, so changes made to the array are
                 not applied to this column and vice versa.
                 String length is restricted to ttypes.MAX_STRING_LEN_NUMPY (=100)
        """
        assert NUMPY_ON, "Numpy is not installed."
        assert self.type != "d", "Not implemented for dates"
        import numpy as np
        
        nptype = NUMPY_TYPE[self.type]
        a = np.array(self.data, dtype = nptype)
        return a
    
    def isBlank(self):
        """ Returns true if all elements in this column are blank or empty strings.
        """
        assert self.type == "s"
        ns = self.reduce(func = lambda i, e, result: len(e.strip()) + result, result = 0)
        return ns == 0
    
    def longStr(self):
        """ Returns a string that describes content in this column, that it includes
            attributes. For a shorter version, use __str__."""
        s = "Col[%12s] \t %4s< \t %8d \t %10s\n"%(self.name, self.type, len(self.data), self.fmt)
        for k, a in self.attrs.items():
            s = s + "   -- %s: %s\n"%(k, a)
        return s
            
    def __str__(self):
        fmt = self.fmt if self.fmt else ""
        s = "Col[%12s] \t %4s< \t %8d \t %10s"%(self.name, self.type, len(self.data), self.fmt)
        return s

    def __getitem__(self, idx):
        #assert idx < len(self.data)
        return self.data[idx]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for v in self.data:
            yield v
        
if __name__ == "__main__":
    c = Column("Waste", 0)
    c.addData([1,2,3,4,5])
    print(c)

    sum = c.reduce(func = lambda i, d, result: result + d, result = 0)
    print("sum: %d"%sum)

    min = c.reduce(func = lambda i, d, result: result if result < d else d, result=100000)
    print("min: %d"%min)