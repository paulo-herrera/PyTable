__docformat__ = "google"

from .column import Column
from .ttypes import ALLOWED_TYPES, MAX_STRING_LEN_NUMPY, MAX_STRING_DATE_LEN_NUMPY, \
                    getH5TypeStr
from .helpers import split_line, is_iterable, read_tab_file
from .required import H5_ON
from .plot import plotxy
#from .version import PYTABLE_VERSION

import sys
import inspect
from typing import List, Union, Callable

# TODO: add shortcuts for cmd line use, e.g. a = addColumn, t=tail, h=head, s=save, r=Read 
class Table:
    """ Class to store a table as a collection of Columns. """
    
    def __init__(self, name):
        self.name = name
        self.cols = []
        self.max_rows = -1
        self.desc = None   # some extra description that can be useful to identify source of data.


    def setName(self, name: str):
        """ Sets name (title) of this table. Allows chaining calls.

            Args:
                name: new name for this table.
           
            Returns:
                This table
        """
        self.name = name
        return self

    
    def all(self):
        """ Returns a list with the indexes of all positions in this list. 
            Mostly used as a easier way to create a list of all columns to be used as 
            input parameter of other methods in Table.
        """
        cols = [i for i in range(len(self.cols))]
        return cols

    
    def names(self):
        """ Returns a list with ids (names) of columns in this table.
        """
        names = [c.name for c in self.cols]
        return names

    
    def hasColumn(self, key):
        """ Given a key returns True if it is in list of columns. 
            key: an integer number or a name. 
                 It should be faster to call with key as an integer.
        """
        assert not is_iterable(key), key
        
        if (isinstance(key, int)):
            return (key >= 0 and key < len(self.cols))
            
        elif (isinstance(key, str)):
            ids = self.names()
            return key in ids
            
        else:
            assert False, "Unknown type for key: " + str(key)

        
    def addColumn(self, name: str = None, data = None, allowRepetition = False):
        """ Adds a column to this table.
            
            Args:
                name: column id. If not passed, then column is assigned a generic id,
                      e.g col1
                data: a list of data or Column to be added as data to the new column. 
                allowRepetition: if True, columns with similar name can be stored in this table.
            
            Returns:
                This table.
        """
        name = name if name else "col%02d"%len(self.cols)
        
        if self.hasColumn(name) and not allowRepetition:
            assert False, "name is already in table: " + name
        
        if data and (isinstance(data, Column)): # and data == None:
            data.name = name
            self.cols.append(data)    
        elif data:
            c = Column(name)
            c.addData(data)
            self.cols.append(c)
        else:
            c = Column(name)
            self.cols.append(c)
        
        if data:
            self.max_rows = self.max_rows if (self.max_rows >= len(data)) else len(data)
        
        return self

    
    def select(self, filter: Callable[[int, str], bool]): # -> Table
        """ Returns a new table with columns that satisfy the filter criteria.
            
            Args:
                filter: function with signature filter(pos, name) -> (True or False)
            Returns:
                A new table that contains the columns of this table for which filter == True.

            NOTE: Both tables share the same columns, so changes apply to one table 
                  are also propagated to the other one.
        """
        source = inspect.getsource(filter)
        # #print(source)
        sel = Table(self.name)
        sel.desc = "select(filter): " + source.strip() 
        
        for i in range(len(self.cols)):
            c = self.cols[i]
            if filter(i, c.name):
                sel.addColumn(c.name, c.data)
        return sel

   
    def clone(self, shallow = True, newName = None):
        """ Creates a shallow or deep copy of this table.
            
            Args:
                shallow: if True, only pass references to columns in this table to new
                         table. If False, then creates a deep copy, so that this table
                         and new table do not share information.
                newName: if present, then use it as title of new table.
            
            Returns:
                New table.
        """
        newName = self.name + "(Copy)" if not newName else newName 
        t = Table(newName)
        for col in self.cols:
            ncol = col if shallow else col.clone() 
            t.addColumn(ncol.name, ncol)
        return t

        
    def append(self, other):
        """ Appends columns of other to this table.
        
            Args:
                other: Table to append to this table.
                
            Returns:
                This table with appended values.
            
            Note: If you need to get a new table by merging this and other, then
                  clone this table first and then append other.
        """
        assert (isinstance(other,Table))
        assert len(self) == len(other)
        
        for i in range(len(self)):
            ic = self.cols[i]
            oc = other.cols[i]
            ic.addData(oc.data)   # type is checked internally
        
        self.__setMaxRows()
        return self

    
    def index(self, names: List[str], verbose = False):
        """ Given a list of column ids, returns a list with their positions in the table.
            
            Args:
                names: list of column ids.
                verbose: if True, prints a warning if name is not in Table.
            
            Returns:
                A list with positions of specified columns.
        """
        assert is_iterable(names)
        
        ids = self.names()    # maybe optimize later if needed, create list at insertion of column
        pos = []
        for k in names:
            if k in ids:
                idx = ids.index(k)
                pos.append(idx)
            elif verbose:
                print(" WARNING: Key is not in Table. [key - %s]"%(k))
            else:
                pass   
        return pos

        
    def at(self, keys: List[Union[int,str]]) -> List[Column]:
        """ Returns a list of columns given a list of key (strings or ints).
            Similar to table[key] but for list of keys.
            
            Args:
                keys: list of int or strings that specifiy columns in the table.
            
            Returns:
                A list of columns.
        """
        assert is_iterable(keys)
        cols = []
        for k in keys:
            c = self.__getitem__(k)
            if c:
                cols.append(c)
            else:
                print("WARNING - Key is not present in table: " + str(k))
        return cols


    def pop(self, key: Union[int, str]):
        """ Removes column specified by key.
        
        Args:
            key: int or string that specifies column.
        
        Returns:
            Removed column or None if key is not in this table. 
        """
        assert not is_iterable(key), "Only single keys accepted"
        
        if self.hasColumn(key):
            if isinstance(key, int):
                c = self.cols.pop(key)
                return c
                
            elif isinstance(key, str):
                idx = self.index([key])    # OPTIMIZE LATER, LIST CREATION
                c = self.cols.pop(idx[0])
                return c
        return None


    def remove(self, keys: List[Union[int,str]]):
        """ Removes columns specified by list of keys
            
            Args:
                keys: List of ints or strings that specify columns that should be removed.
            
            Returns:
                This table.
        """
        assert is_iterable(keys)
        
        k = keys[0]
        if isinstance(k, str):
            idxs = self.index(keys)
        elif isinstance(k, int):
            idxs = keys
        
        # Safe way to remove from the list, order in decreasing order, so pop works.
        idxs = sorted(idxs, reverse=True)
        
        removed = []
        for idx in idxs:
            #assert self.hasColumn(idx), "Column[%d] not in table."%(idx)
            c = self.cols.pop(idx)
            removed.append(c)
        
        return removed


    def ncols(self):
        """ Returns the number of cols in this table. Similar to __len__.
        """
        return len(self.cols)


    def nrows(self):
        """ Returns the maximum number of rows in this table.
        """
        return self.max_rows


    def what(self, out = sys.stdout, wait = False):
        """ Prints a summary of (what is in) this table including name and information about 
            each column such as: name, type and number of rows.
        """
        out.write("=" * 80 + "\n")
        out.write("Table: %s\n"%(self.name))
        if self.desc: out.write("  %s\n"%(self.desc))
        out.write("-"*80 + "\n")
        out.write("Col[%4s]: %20s \t %3s< \t %8s \n" % ("Pos", "Name", "Type", "#Rows"))
        out.write("-" * 80 + "\n")
        for i in range(len(self.cols)):
            c = self.cols[i]
            s =   "Col[%04d]: %20s \t %3s< \t %08d \n" % (i, c.name, c.type, len(c))
            out.write(s)
        out.write("=" * 80 + "\n")
        
        if wait: input("PRESS ENTER...")


    def setFormatStr(self, fmt_int: Union[str,None], fmt_float: Union[str,None], \
                           fmt_date: Union[str,None], fmt_str: Union[str,None]):
        """ Sets format used to convert to string or print elements of columns in 
            this table.
            
            Args:
                fmt_int: format used to convert ints.
                fmt_float: format used to convert floats.
                fmt_date: format used to convert dates.
                fmt_string: format used to print strings.
            
            Returns:
                This table.
            
            NOTE: It is also possible to set the format of individual columns by calling
                  col.setFormatStr(fmt).
                  Formats are only used to convert TO string, not to convert TO STRING.
        """
        for c in self.cols:
            if c.type == "i": c.setFormatStr(fmt_int)
            if c.type == "f": c.setFormatStr(fmt_float)
            if c.type == "d": c.setFormatStr(fmt_date)
            if c.type == "s": c.setFormatStr(fmt_str)
        
        return self


    def convert(self, cols: List[int], types: List[str], fmt_date = None):
        """ Attempt to convert each column of this table to the specified type provided in the list fmt.
            
            Args:
                cols: list with columns indexes that should be converted.
                types: a list with single characters that specify the new type of each column, 
                     i.e.["i", "f", "d", "s"].
                     If shorter than cols, then the last element is repeated.
                fmt_date: format used to convert strings to datetime objects.
                          Only needed if converting to dates.
            Returns:
                This table.
                
        # """
        for t in types:
            assert t in ALLOWED_TYPES, t
        
        if len(types) < len(cols):
            missing = len(cols) - len(types)
            append = missing * [types[-1]]
            types = types + append
        elif len(types) == len(cols):
            pass
        else:
            assert False
        
        for i in range(len(cols)):
            idx = cols[i]
            c = self.cols[idx]
            nt = types[i]
            if (c.type == "s") and (nt == "d"):
                assert fmt_date
                c.convert(nt , fmt_date)
            else:
                c.convert(nt) # using the default format. 
        
        return self



    def print(self, maxRows: int = -1, writeTitle: bool=True, out = sys.stdout, \
              sep: str="\t", columnWidth: int=10, missing: str="-", verbose: bool=False, \
              start: int=0, lineBelow = True):
        """ Prints each elements in columns of this table in tabular format. 
            
            Args:
                maxRows: maximum number of rows to be printed. 
                         If <0, then all rows are printed.
                writeTitle: If true, prints name of table.
                out: stream where data should be printed.
                sep: string used as separator between columns.
                columnWidth: default width used to print columns. 
                             There is no guarantee that the formats used to print
                             elements of column fit withing this width.                              
                missing: string used to represent missing values in table. DEFAULT: "-"
                verbose: if True, then prints some additional information to sys.stdout.
                start: start printing at this row.
                lineBelow: if True, prints a line below column headers.
                
            Returns:
                Stream where data was printed. 
        """
        _fmt = "%" + str(columnWidth) + "s"

        if writeTitle:
            out.write("=" * 80 + "\n")
            out.write("Table: %s\n" % (self.name))
            out.write("-" * 80 + "\n")

        for c in self.cols:
            out.write( _fmt%c.name )
            out.write(sep)
        out.write("\n")
        if lineBelow: out.write("-" * 80 + "\n")
    
        nrows = maxRows if (maxRows > 0 and self.max_rows > maxRows) else self.max_rows 
        for r in range(start, nrows):
            for c in self.cols:
                if len(c) >r:
                    s = c.format(r)
                    out.write(_fmt%s)
                else:
                    out.write(_fmt%(missing) )
                out.write(sep)
            out.write("\n")
        
        return out

    
    def head(self, n = 5):
        """ Prints first n rows with default formatting. Same can be achieved with print,
            but calling head may be self-explanatory.
            Args:
                n: number of rows to print.
            Returns:
                This table.
        """
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> HEAD >>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        end = n if n < self.max_rows else self.max_rows
        self.print(start = 0, maxRows = end)
        return self
        
        
    def tail(self, n = 5):
        """ Prints last n rows with default formatting.
            Args:
                n: number of rows to print.
            Returns:
                This table.
        """
        maxRows = self.max_rows
        start = maxRows - n
        start = start if start >=0 else 0
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TAIL <<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        self.print(start = start, maxRows = -1)
        return self
    
    
    def save(self, dst: str, sep = ",", columnWidth = 10, missing = "-", verbose = False):
        """ Saves table to file. Similar to print, but with default values.
            Args:
                dst: path to destination file.
                sep: string used as separator between columns.
                columnWidth: default width used to print columns. 
                             There is no guarantee that the formats used to print
                             elements of column fit withing this width.                              
                missing: string used to represent missing values in table. DEFAULT: "-"
                verbose: if True, then prints some additional information to sys.stdout.
        """
        if verbose:
            print("Saving table: " + self.name)
            print("          to: " + dst)
            
        with open(dst, "w") as sdst:
            self.print(writeTitle = False, out = sdst, sep = sep, \
                       columnWidth = columnWidth, missing = missing, \
                       verbose = verbose, lineBelow=False)
        
    @staticmethod
    def read(src: str, sep: str=",", header=1, removeEmptyColumn=True, \
             verbose=True, encoding: str = "utf-8", allowRepetition = True, skip = 0):
        """ Reads table from file.
            
            Args:
                src: path to file.
                sep: string that separates columns. 
                header: line number that contains header (0 or 1, DEFAULT = 1). 
                removeEmptyColumn: if True, check and removed columns that only have empty strings.
                                   needed for ill-formed files. [DEFAULT=False]
                                   Alternative is modifying the files before reading them,
                                   which could be faster. 
                                   For large tables, it may be cheaper import them, 
                                   and remove specific columns later.
                verbose: if True, prints some additional information.
                encoding: string that indicates file encoding.
                allowRepetition: if True, allows columns with same header id.
                skip: number of lines at beginning of file that should be skipped, 
                      e.g. comment lines [DEFAULT = 0]. 
                
            Returns:
                A new table with data read from file. 
        """
        assert header <= 1, header
        
        if verbose:
            print("Reading table from: ")
            print("   " + src)
        
        strs, skipped = read_tab_file(src, sep, strip=True, verbose=False, encoding = encoding, skip=skip)
        nlines= len(strs)
        ncols = len(strs[0])
        if verbose:
            print("   Read %d lines"%nlines)
            print("   %d columns"%ncols)
            if skipped and len(skipped) >0: print("   >>SKIPPED<<" + skipped[0])          # version
        
        h = strs[0] if header == 1 else ["col%04d"%c for c in range(ncols)]
        t = Table(name = src)
        for hh in h: t.addColumn(name = hh, data=[], allowRepetition=allowRepetition)
        
        for c in range(ncols):
            cdata = []
            for r in range(header, nlines):
                v = strs[r][c]
                cdata.append(v)
            t[c].addData(cdata)
        
        if removeEmptyColumn:
            for c in range(ncols - 1, -1, -1):
                col = t.cols[c]
                if col.isBlank(): t.pop(c)
                
        t.__setMaxRows()
        
        return t
    
    def toH5(self, dst, root = None, append = False, compress = True, verbose = True, fmt_date = None):
        """ Saves table to HDF5 file.
            Args:
                dst: path to HDF5 file. Recommended extension to be .h5, 
                     but not enforce it. 
                root: string used as root of the group that contains the table in the 
                      HDF5 file [DEFAULT = "/"].
                append: if True, append table to existing file.
                compress: save data in compressed format (gzip supported by HDF5).
                          Useful for big files.
                verbose: if True, print some warnings and additional information 
                         to sys.stdout.
                fmt_date: format used to convert dates to strings.
                          Only needed if there is a single column of type "d". 
                         
            Return: 
                Full path to saved HDF5 file.
            
            NOTE: Dates are converted to string using default format specified in setFormatStr.
        """
        # TODO: Add attributes for columns
        from datetime import datetime as dt
        import os
        assert H5_ON, "h5py is not available"
        import h5py
        
        if verbose:
            print("WARNING<Table.toH5>: Strings are limited to %d characters"%(MAX_STRING_LEN_NUMPY))
            print("WARNING<Table.toH5>: Dates are saved as strings of max %d characters"%(MAX_STRING_DATE_LEN_NUMPY))
        
        flag = "w" if not append else "r+"
        dst = os.path.abspath(dst)
        h5 = h5py.File(dst, flag)
        
        g = h5.create_group(root) if root else h5["/"]
        g.attrs["table"] = self.name
        g.attrs["date"] = dt.now().strftime("%d_%m_%Y__%H_%M_%S")
        
        for c in self.cols:
            print("COLUMN NAME: " + c.name)  # DEBUG
            dtype = getH5TypeStr(c.type)
            nelem = len(c)
            
            if verbose: print("Dataset<%s> - type<%s> - nelem<%d>"%(c.name, dtype, nelem))
            if compress:
                dset = g.create_dataset(c.name, (nelem), dtype=dtype, compression = "gzip")
            else:
                dset = g.create_dataset(c.name, (nelem), dtype=dtype)
                
            if c.type == "d":
                assert fmt_date, "Missing format to convert to date"
                cc = c.clone()    
                cc.convert("s", fmt_date)   # has to convert special for date 
            else:
                cc = c
            
            dset[:] = cc.data[:]
        
        h5.close()
        if verbose: print("   Finished saving HDF5 file")
        return dst
    
    
    def fromH5(self, src, root = None, verbose = False):
        """ Reads table from HDF5 file saved by calling toH5 or with a similar format.
            
            Args:
                root: 
            Returns:
                Read table and full path to file, (t, f).
        """
        from datetime import datetime as dt
        import os
        assert H5_ON, "h5py is not available"
        import h5py
        
        if verbose: 
            print("Reading table from: " + src)
            
        src = os.path.abspath(src)
        h5 = h5py.File(src, "r")
        
        root = root if root else "/"
        g = h5[root]
        name = g.attrs["table"]
        date = g.attrs["date"]
        if verbose:
            print(" Table: " + name)
            print("   Saved on: " + date)
        
        t = Table(name)
        for name in g:
            #print(name)       # DEBUG
            ds = h5[root + "/" + name]
            id = name
            nvals = len(ds)
            dtype = str(ds.dtype)
            if verbose: print("   DATASET<%s>: %d values, type: %s"%(name, nvals, dtype))
            
            # Check if it creates too many temporaries
            a = ds[:]
            if "S" in dtype:            # strings are passed as raw binary, need to decode
                data = [e.decode("utf-8") for e in a]
            else:
                data = a.tolist()
            t.addColumn(id, data)
            
        h5.close()
        if verbose: print("   Finished reading table")
        return t, src
        
    
    def plotxy(self, xcols, ycols, labels=["x", "y"], fmt=None, legend=True, new=True):
        """ Plots ycols vs xcols. 
        
            Args:
                xcols: list of columns, e.g. [0,1,2] or ["col1", "col2"], that specifies list to be used as x-data.
                       If len(xcols) == 1, then all ycols are plotted against a single column. 
                       If len(xcols) > 1, then it must satisfy len(xcols) == len(ycols).
                ycols: list of columns, e.g. [0,1,2] or ["col1", "col2"], that specifies list to be used as y-data.
                fmt: list with strings that specify format to be used for lines and symbols.
                     If len(fmt) == 1, then use the same format for all series.
                     If len(fmt) > 1, then it must satisfy len(fmt) == len(ycols)
                labels: labels to be used as titles for axes. It should satisfy len(labels) == 2.
                        DEFAULT = ["x","y"].
                legend: if True include legend [DEFAULT=True].
                new: If True, creates a new figure [DEFAULT=True].
                
            
            Returns:
                Reference to matplotlib.pyplot that can be used to:
                - show figure, plt.show()
                - save figure, plt.savefig(), etc.
        """
        p = plotxy(self, xcols, ycols, labels, fmt, legend, newfig = new)
        return p
    
    def __setMaxRows(self):
        """ To be called internally to set max number of rows in table.
        """
        self.max_rows = -1
        for c in self.cols:
            if len(c) > self.max_rows: self.max_rows = len(c)


    def __str__(self):
        s = "Table: %s  #columns: %d"%(self.name, len(self.cols))
        return s


    def __iter__(self):
        """ Provides an iterator interface to allow looping over columns.
        """
        for c in self.cols:
            yield c


    def __len__(self) -> int:
        """ Returns number of columns in this table.
        """
        return len(self.cols)


    def __getitem__(self, key):
        """ Returns column that corresponds to key, which can a string or int.
            
            Returns:
                The column that corresponds to key or None if not present. 
                
            NOTE: Using an int as key should be faster.
        """
        assert not is_iterable(key), "Only single keys accepted"
        
        if self.hasColumn(key):
            if isinstance(key, int):
                return self.cols[key]
            elif isinstance(key, str):
                idx = self.index([key])
                return self.cols[idx[0]]
        else:
            None

    
if __name__ == "__main__":
    pass
    # t = Table("table0")
    # t.addCol("time", [0, 0.1, 0.2, 0.3])
    # t.addCol("pressure", [0.1, 1.2, 0.3, 2.5, 0.8])
    # t.addCol("time", [0.2, 0.33, 0.4, 0.5], allowRepetition= True)
    # for c in t: 
        # print(c.name)
    
    # t.select(filter = lambda i, n: True)
    # t.summary()
