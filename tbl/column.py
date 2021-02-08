from .ttypes import Types
from .helpers import _is_iterable
import sys

try:
    import numpy as np
    NUMPY_OFF = False
except:
    NUMPY_OFF = True
    
class Column:
    """ General container to store data as column of a table. 
        Constructor should never be called from outside package. 
    """
    
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.data = []
        self.type = None
        self.fmt = None   # used to convert dates and float to strings. 

    def setPos(self, newPos):
        """ Updates position of this column in the table. 
            It is intended to only be called from methods in Table.
        """
        self.pos = newPos
    
    def setName(self, name):
        """ Sets name of this column.
        """
        self.name = name
        
    def addData(self, data, ctype = None):
        """ Adds data to this column. 
        :param data: list or tuple with data of this column.
                     If column already has data, then it is appended.
                     Type of data should match type of this column if already set. 
        :param ctype: if present, then it indicates type of column.
                      It should an element of the intended type, e.g. 1, 0.1, "s".
                      It should only be passed if self.type has not been set.
                      This option should be used in combination with an empty list,
                      to create a column that is a placeholder for future data.
        """
        assert _is_iterable(data)
        
        if not self.type and len(data) > 0:
            self.type = Types.getType(data[0])
        elif self.type and len(data) > 0:           # have to check if types match
            ntype = Types.getType(data[0])
            assert(ntype == self.type)
        elif not self.type and ctype:
            ntype = Types.getType(ctype)
            self.type = ntype
            self.data = data
        else:
            assert False
            
        self.data = self.data + data                  # should combine lists
        return self
    
    def append(self, e):
        """ Appends element e to this column. 
        """
        nt = Types.getType(e)
        if not self.type: 
            self.type = nt
        else:
            assert nt == self.type, "self.type: %s, type(e): %s"%(self.type, nt)
        self.data.append(e)
        
    def convertToString(self, fmt = None):
        """ Converts this column to a column of strings. 
            To convert float and dates, it uses self.fmt, which it should have been set 
        """
        self.fmt = fmt if fmt else self.fmt
        self.convert(self.type, "s", self.fmt)
    
    def convertFromString(self, fmt = None, ntype = None):
        """ Converts this column of strings to the natural type of the data. 
            To convert float and dates, it uses fmt or self.fmt, which it should have been set 
            :param ntype: new type. if not present, then new type is inferred from the data in this column.
        """
        self.fmt = fmt if fmt else self.fmt
        d0 = self.data[0]
        if not ntype:
            ntype = Types.getStrType(d0, self.fmt)
        
        #print(self.name) # DEBUG
        self.convert("s", ntype, self.fmt)
        
    def convert(self, old, new, fmt = None):
        """ Converts column data type from old to new type.
        :param old: old type as a one character string (see Types.ALLOWED_TYPES). 
        :param new: new type as a one character string (see Types.ALLOWED_TYPES).
        :param fmt: format used to convert from old to string type, when old = ["f", "d"]. 
        """
        assert Types.isType(old), old
        assert Types.isType(new), new 
        
        f, fmt = Types.getConverter(old, new, fmt)
        dd = []
        for d in self.data:
            nd = f(d)
            dd.append(nd)
        
        self.data = dd
        self.type = new
        self.fmt = fmt
    
    # Create new list of values
    def indexOf(self, filter):
        """ Return a list of indexes of the elements of the column that satisfy:
                filter(i, c[i]) = True
        """
        idx = []
        for i in range(len(self.data)):
            v = self.data[i]
            if filter(i, v): idx.append(i)
        return idx

    def collect(self, filter):
        """ Returns a list of the elements (e[i]) of the data that satisfy:
               filter(i, e[i]) = True
        """
        values = []
        for i in range(len(self.data)):
            v = self.data[i]
            if (filter(i, v)): values.append(v)
        return values

    def sample(self, each):
        """ Creates a new column taking only few elements of the original column.
            :param each: take only one element each elements.
        """
        nd = self.collect(filter = lambda i, e: i%each == 0)
        c = Column(self.name, self.pos).addData(nd)
        return c
    
    def remove(self, filter):
        """ Removes elements (e[i]) of this column that satisfy: filter(i, e[i]) = True
            The number of elements stored in this column may be fewer after calling this function.
        """
        ndata = []
        for i in range(len(self.data)):
            v = self.data[i]
            if filter(i, v):
                pass
            else:
                ndata.append(v)
        self.data = ndata

    def clone(self):
        """ Returns an exact copy of this column that does not shared data with 
            this column (deep-copy)
        """    
        c = Column(self.name, self.pos)
        c.addData(self.data.copy())
        return c

    def apply(self, func):
        """ Creates a new list with element i in this column as: c[i] = func(i, c[i])
            Similar to apply, but it returns a new list with values.
        """
        nvals = []
        for i in range(len(self.data)):
            d = self.data[i]
            val = func(i, d)
            nvals.append(val)
        return nvals

    def map(self, func):
        """ Assign value to element i in this column as: c[i] = func(i, c[i]) 
            Similar to apply, but it changes the values in place.
        """
        nvals = []
        for i in range(len(self.data)):
            d = self.data[i]
            self.data[i] = func(i, d)
        return self

    def reduce(self, func, result):
        """ Applies func on each element of this column and returns the final result.
            The function func must have the type: func(i, e, result), where result is 
            either the value passed to the function or the result of the last call to 
            func.
            For example, to compute the minimum value of a column:
            c.reduce(func = lambda (i, e, result): e if e < result else result, result = BIG_NUMBER )
        """
        
        for i in range(len(self.data)):
            e = self.data[i]
            result = func(i, e, result)
        return result

    def display(self, out = sys.stdout, writeName = False):
        """ Write elements of column to out. """
        if writeName: print(self.name) 
        for e in self.data: print(e)
    
    def __str__(self):
        s = "Col[%4s]: \t %20s \t %4s< \t %6d"%(self.pos, self.name, self.type, len(self.data) )
        return s

    def __getitem__(self, idx):
        assert idx < len(self.data)
        return self.data[idx]

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        for v in self.data:
            yield v
    
    def addMissingValues(self, nmissing, mark):
        """ Adds a string to mark missing values in this column. 
            It is useful to visualize data gaps when displaying or writing to a file.
            This only makes sense if this column stores strings.
            :param nmissing: number of missing items to be appended.
            :param mark: string used to indicate missing values.
        """ 
        assert self.type == "s"
        for i in range(nmissing):
            self.data.append(mark)
    
    def removeMissingValues(self, mark):
        """ Removes missing values indicated by mark from this column.
        :param mark: string used to indicate missing values.
        """
        assert self.type == "s"
        ndata = []
        for d in self.data:
            if d == mark:
                pass
            else:
                ndata.append(d)
        self.data = ndata
        
if __name__ == "__main__":
    c = Column("Waste", 0)
    c.addData([1,2,3,4,5])
    print(c)

    sum = c.reduce(func = lambda i, d, result: result + d, result = 0)
    print("sum: %d"%sum)

    min = c.reduce(func = lambda i, d, result: result if result < d else d, result=100000)
    print("min: %d"%min)