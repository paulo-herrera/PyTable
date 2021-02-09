__docformat__ = "google"

from .ttypes import getType, isTypeStr, getTypeConverter
from .helpers import is_iterable
import sys
import inspect

try:
    import numpy as np
    NUMPY_OFF = False
except:
    NUMPY_OFF = True    

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
        self.desc: str = desc if desc else None  # description of this column
    
    def setName(self, name: str):
        """ Sets name of this column.
            Returns: This column.
        """
        self.name = name
        return self
    
    def setDescription(self, desc: str):
        """ Sets description of this column.
            Returns: This column.
        """
        self.desc = desc
        return self
    
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
        """
        assert is_iterable(data), "To add individual elements, use append"
        
        if not self.type and len(data) > 0:
            self.type = getType(data[0])
        elif self.type and len(data) > 0:           # have to check if types match
            ntype = getType(data[0])
            assert(ntype == self.type)
        elif not self.type and ctype:
            ntype = getType(ctype)
            self.type = ntype
            self.data = data
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
        
    def convert(self, old: str, new: str = None, fmt = None):
        """ Converts column data type from old to new type.
        
            Args:
                old: old type as a one character string (see ttypes.ALLOWED_TYPES). 
                new: new type as a one character string (see ttypes.ALLOWED_TYPES).
                     Optional only if old type is string "s" (automatic conversion of strings). 
                fmt: format used to convert dates and floats to strings.
                     If present, then self.fmt is updated to fmt.      
            
            Returns:
                This column.
        """
        assert isTypeStr(old), old
        assert isTypeStr(new), new 
        
        self.fmt = fmt if fmt else self.fmt
        
        if old == "s" and not new:
            assert len(self.data) > 0
            d0 = self.data[0]
            new = getTypeStr(d0, self.fmt)
            
        f, fmt = getTypeConverter(old, new, self.fmt)
        dd = [f(nd) for nd in self.data]                
        self.data = dd
        self.type = new
        
        return self
        
    def index(self, filter):
        """ Return a list of indexes of the elements of the column that satisfy:
                filter(i, c[i]) = True
        """
        idx = []
        for i in range(len(self.data)):
            v = self.data[i]
            if filter(i, v): idx.append(i)
        return idx

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

    def column(self, filter, name = None, desc = None):
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
        if not name: name = "sample(" + self.name + ")" 
        if not desc: desc = inspect.getsource(filter)
            
        c = Column(name).addData(nd).setDescription(desc.strip())
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
        c = Column(self.name, self.pos)
        c.addData(self.data.copy())
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

    def map(self, func, desc=True):
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
            
        if desc: self.desc = inspect.getsource(func).strip()
        
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

    def write(self, out = sys.stdout, sep = "\n", fmt = None, writeName = False):
        """ Write elements of column to out.
        
            Args:
                out: a stream like object, e.g. sys.stdout.
                sep: a string used as separator of elements.
                writeName: if True, then write name of this column before writing elements.
        """
        self.fmt = fmt if fmt else self.fmt
        
        if writeName: 
            out.write(self.name)
            out.write(sep)
        
        c, fmt = getTypeConverter(self.type, "s", self.fmt)
        for e in self.data:
            s = c(e)
            out.write(s)
            out.write(sep)
    
    def __str__(self):
        s = "Col[%12s]: \t %4s< \t %8d"%(self.name, self.type, len(self.data) )
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