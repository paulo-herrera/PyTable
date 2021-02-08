from .column import Column
from .ttypes import Types
from .helpers import _split_line, _is_iterable
import sys
import inspect

# Attemtp to make some kind of failsafe if matplotlib is not installed
try:
    import matplotlib.pyplot as plt
    PLT_OFF = False
except:
    PLT_OFF = True
    
try:
    import h5py
    H5_OFF = False
except:
    H5_OFF = True
    
# Helpers and global default values
__NOT_A_VALUE__ = "-"
    
class Table:

    def __init__(self, name):
        self.name = name
        self.ids = {}    
        self.cols = {}
        self.max_rows = -1
        self.desc = None   # some extra description that can be useful to identify source of data.

    def setName(self, _name):
        """ Sets name (title) of this table. Allows chaining calls.
            :param _name: new name for this table.
            :returns this table
        """
        self.name = _name
        return self
        
    def ncols(self, names, verbose = False):
        """ Given a list of column ids, returns a list with their positions in the table.
            :param names: list of column ids or list of ints that specify position in Table.
                          If list of ints, then it returns the same list. Useful to make generic
                          code.
            :param verbose: flag, if True, prints a warning if name is not in Table.
        """
        assert _is_iterable(names)
        
        if isinstance(names[0], int):
            return names
        else:
            pos = []
            for k in names:
                if k in self.ids:
                    p = self.ids[k]
                    pos.append(p)
                elif verbose:
                    print(" WARNING: Key is not in Table. [key - %s]"%(k))
                else:
                    pass   
            return pos
        
    def all(self):
        """ Returns a list with the indexes of all positions in this list. 
            Mostly used as a easier way to create a list of all columns to be used as 
            input parameter of other methods in Table.
        """
        cols = list(self.cols.keys())
        return cols
    
    def names(self):
        """ Returns a list with ids (names) of columns in this table.
        """
        names = list(self.ids.keys())
        return names
        
    def __len__(self):
        """ Returns number of columns in this table.
            Same as ncols, pure 'synthactic sugar'
        """
        return len(self.cols.keys())
        
    def hasColumn(self, key):
        """ Given a key returns True if it is in list of columns. 
            key: an integer number or a name. 
        """
        assert not _is_iterable(key)
        if (isinstance(key, str)):
            return key in self.ids.keys()
        elif (isinstance(key, int)):
            return key in self.cols.keys()
        else:
            assert False

    def _appendCol(self, c, allowRepetition = False):
        """ Adds a column to this table that contains the same name and data as the old c column.
            The main purpose of this is internal. 
        """
        assert isinstance(c, Column)
        self.addCol(c.name, data = c.data, allowRepetition = allowRepetition)
        return self
        
    def addCol(self, name, data = None, allowRepetition = False):
        """ Adds a column to this table.
            name: an id (string). 
            data: a list of data to be added as data to the new column. 
            TODO: Override this call with old addColumn
        """
        #if (isinstance(col, Column)): # and data == None:
        #     self.addCol(col.name, data = col.data, allowRepetition = allowRepetition)     
        if (isinstance(name, str)): 
            pos = len(self.cols)
            if self.hasColumn(name) and allowRepetition:
                name = name + str(pos)
            elif self.hasColumn(name):
                assert False, "name is already in dictionary: " + name
            
            c = Column(name, pos)
            if data:
                c.addData(data)    
            self.cols[pos] = c
            self.ids[name] = pos
            self.max_rows = self.max_rows if (self.max_rows >= len(c)) else len(c) # this should be done also when removing data 
            return self
        else:
            assert False, "col: " + str(name) + str(type(name))
            return None
    
    def removeColByName(self, name):
        """ Removes column that has id == name
        """
        assert isinstance(name, str)
        # this will change the position of the columns in the table. 
        # Then, it is safer to create new dicts to store names and positions.
        # If applied few times, it should not create problems with garbage collector for
        # creating temporaries.
        #print("removeColByName: " + name) # DEBUG
        if name in self.ids.keys():
            pos = self.ids[name]
            self.removeColByPos(pos)
        else:
            assert False, "Key is not in table: " + name
        return self
        
    def removeColByPos(self, pos):
        #print("removeColByPos: " + str(pos)) # DEBUG
        assert isinstance(pos, int)
        
        if pos not in self.cols.keys():
            print("WARNING - col[%d] not in table"%pos)
        else:
            ncols = {}
            nids = {}
            count = 0
            for k, c in self.cols.items():
                if k != pos:
                    c.setPos(count)
                    ncols[count] = c
                    nids[c.name] = count
                    count = count + 1
            self.cols = ncols
            self.ids = nids 
        return self
        
    def removeCols(self, keys):
        """ Removes columns that are in keys list. 
            keys: a list or tuple of strings.
        """           
        if _is_iterable(keys): # list, tuple, dict
            key = keys[0]
            if (isinstance(key, str)):
                for k in keys:
                    self.removeColByName(k)
            # elif (isinstance(key, int)):
                # for k in keys:
                    # self.removeColByPos(k)
            else:
                assert False
                
        else:
            assert False
        
        return self # avoid setting variable to None 
        
    def getColByName(self, name):
        """ Returns column that has id == name """
        assert name in self.ids.keys(), "Wrong name"
        pos = self.ids[name]
        return self.cols[pos]

    def getColByPosition(self, pos):
        """ Returns column at position pos """
        assert pos in self.cols.keys()
        return self.cols[pos]
            
    def __getitem__(self, key):
        """ Returns column that corresponds to key = (string, int) """
        assert not _is_iterable(key), "Only single keys accepted"
        
        if isinstance(key, int):
            return self.getColByPosition(key)
        elif isinstance(key, str):
            return self.getColByName(key)
        else:
            assert False, "Unknown type for key: " + str(key)
    
    def getCols(self, keys):
        """ Returns a list of columns given a list of key (strings or ints).
            If you need to search considering some criteria for ids and/or position of 
            columns, consider using select. 
        """
        assert _is_iterable(keys)
        cols = []
        key = keys[0]
        if isinstance(key, str):
            for i in keys:
                c = self.getColByName(i)
                cols.append(c)
        elif isinstance(key, int):
            for i in keys:
                c = self.getColByPosition(i)
                cols.append(c)
        else:
            assert False, "Wrong key type: " + type(key)

        return cols
        
    def select(self, filter):
        """ Returns a new table with columns that satisfy the filter criteria.
            :param filter: function with signature filter(index, name) -> (True or False)
            :return: a new Table that contains the columns of this table that satisfy the filter criteria.

             NOTE: Since both tables share the same columns, changes apply to one table are automatically
                   propagated to the other one.
        """
        source = inspect.getsource(filter)
        #print(source)
        
        sel = Table(self.name)
        sel.desc = "select(filter): " + source.strip() 
        for i in range(len(self)):
            c = self.cols[i]
            if filter(i, c.name):
                sel.addCol(c.name, c.data)
        return sel #, source
   
    def clone(self, shallow = True, newName = None):
        """ Creates a shallow copy of this table. 
            If shallow == True, columns are only references to the old columns, so data is not copied (shallow copy).
                          Then, if you modify data in the new table, also data in the old table is modified.
            If shallow == False, columns are exact deep copies of the old columns. Use when new table is used to modify data,
                          but old data should be unchanged.
            :param newName if present, then new table has this title.
        """
        newName = self.name + "(Copy)" if not newName else newName 
        t = Table(newName)
        for pos, col in self.cols.items():
            ncol = col if shallow else col.clone() 
            t._appendCol(ncol)
        return t
        
    def append(self, other):
        """ Appends columns of table other to this table.
            Columns in this table appears first in the result table.
            If you need to get a new table by merging this and other, then
            clone this table first and then append other.
            :param other: other table.
            :returns this table.
        """
        assert (isinstance(other,Table))
        for c in other:
            self._appendCol(c)
        return self
        
    #def merge(self, tbl1, newname=None):
    #    """ Merges this table with table tbl1.
    #        Columns in this table appears first in the result table.
    #        Columns of both table are only shallow copies.
    #        If a new completely new table must be created, then clone(shallow=False) both tables first.
    #        RETURN a new table.
    #    """
    #    assert (isinstance(tbl1,Table))
    #    if not newname:
    #        newname="Merged:" + self.name + "-" + tbl1.name 
    #    t = self.clone(shallow=True, newName = newname)
    #    return t
        
    def __str__(self):
        s = "Table: %s  #columns: %d"%(self.name, len(self.cols))
        return s

    def __iter__(self):
        """ Provides an iterator interface, so one can loop over columns.
        """
        for idx, c in self.cols.items():
            yield c

    def _setMaxRows(self):
        for k, c in self.cols.items():
            if len(c) > self.max_rows:
                self.max_rows = len(c)

    def plotxy(self, xcols, ycols, labels=["x", "y"], newfig=True, fmt=None, legend=True):
        """ Plots ycols vs xcols. 
            :param xcols: list of columns, e.g. [0,1,2] or ["col1", "col2"], that specifies list to be used as x-data.
                          If len(xcols) == 1, then all ycols are plotted against a single column. 
                          If len(xcols) > 1, then it must satisfy len(xcols) == len(ycols).
            :param ycols: list of columns, e.g. [0,1,2] or ["col1", "col2"], that specifies list to be used as y-data.
            :param fmt: list with strings that specify format to be used for lines and symbols.
                        If len(fmt) == 1, then use the same format for all series.
                        If len(fmt) > 1, then it must satisfy len(fmt) == len(ycols)
            :param legend: flag, if True show legend.
            :param labels: labels to be used as titles for axes. It should satisfy len(labels) == 2.
                           If labels[0] == None, then xlabel is not included. Similar for ylabel.
            :param newfig: If False, then do not create a new figure and use old one for plotting.
            :returns reference to matplotlib.pyplot that can be used to:
                     - show figure, plt.show()
                     - save figure, plt.savefig(), etc.
        """
        if PLT_OFF: 
            print("Missing matplotlib.pyplot")
            return # not matplotlib => not plots 
            
        assert _is_iterable(xcols) and _is_iterable(ycols)
        assert len(labels) == 2, str(labels)
        
        # just in case we got list of column names
        xcols = self.ncols(xcols)
        ycols = self.ncols(ycols)
        
        _ncols = len(ycols)
        
        if len(xcols) == 1:
            xx = [xcols[0] for i in range(_ncols)]
            yy = ycols
        else:
            assert len(xcols) == len(ycols)
            xx = xcols
            yy = ycols
        
        if fmt and len(fmt) == 1:
            fmt = [fmt[0] for i in range(_ncols)]
        elif fmt:
            assert len(fmt) == _ncols
            pass
        else:  # use default matplotlib format
            pass
        
        if newfig: plt.figure()
        for i in range(len(xx)):
            x = self.getColByPosition(xx[i])
            y = self.getColByPosition(yy[i])
            assert x.type != "s" and y.type != "s"
           
            id = self.cols[yy[i]].name
            if not fmt:
                plt.plot(x, y, label = id)
            else:
                plt.plot(x, y, fmt[i], label = id)
        
        if labels[0]: plt.xlabel(labels[0], fontsize=16) # TODO: add option to set defaults per package
        if labels[1]: plt.ylabel(labels[1], fontsize=16)
        if legend: plt.legend()
        
        return plt
    
    def plotts(self, xcols, ycols, labels=["x", "y"], newfig=True, fmt=None, legend=True):
        p = self.plotxy(xcols, ycols, labels, newfig, fmt, legend)
        p.gcf().autofmt_xdate()
        return p
    
    def addMissingValues(self):
        ''' Add elements to rows that are shorter than the longest one.
            It is always called when writing or displaying elements of the table.
        '''
        self._setMaxRows()
        for k, c in self.cols.items():
            missing = self.max_rows - len(c)
            c.addMissingValues(missing, mark = __NOT_A_VALUE__)

    def removeMissingValues(self):
        ''' Removes elements that are equal to the string ___NOT_A_VALUE__ '''
        for k, c in self.cols.items():
            c.removeMissingValues(mark = __NOT_A_VALUE__)

    def summary(self, out = sys.stdout, wait = False):
        """ Prints a brief summary of this table including name and information about 
            each column such as: name, type and number of rows.
        """
        out.write("=" * 80 + "\n")
        out.write("Table: %s\n"%(self.name))
        if self.desc: out.write("  %s\n"%(self.desc))
        out.write("-"*80 + "\n")
        out.write("Col[%4s]: %20s  \t Type \t #Rows \n" % ("Pos", "Name"))
        out.write("-" * 80 + "\n")
        for p, c in self.cols.items():
            out.write( str(c)  + "\n")
        out.write("=" * 80 + "\n")
        
        if wait: input("PRESS ENTER...")

    def display(self, writeTitle = True, out = sys.stdout, sep = "\t", columnWidth = 10, missing = "-"):
        """ Prints each elements in columns of this table in tabular format. 
            :param writeTitle: If true, then first prints name of table.
            :param out: stream where data should be printed.
            :param sep: string used as separator for columns.
            :param columnWidth: default width used to print columns. 
            :param missing: string used to represent missing values in table. DEFAULT: "-"
            
            TODO: fix formatting for dates.
        """
        #self.addMissingValues()
        fmt = "%" + str(columnWidth) + "s"

        if writeTitle:
            out.write("=" * 80 + "\n")
            out.write("Table: %s\n" % (self.name))
            out.write("-" * 80 + "\n")

        for k, c in self.cols.items():
            out.write( fmt%c.name )
            out.write(sep)
        out.write("\n")

        for r in range(self.max_rows):
            for k, c in self.cols.items():
                if len(c) >r:
                    out.write( fmt%str(c.data[r]) )
                else:
                    out.write( fmt%(missing) )
                out.write(sep)
            out.write("\n")

    def setFormats(self, fmt_float, fmt_date):
        for p,c in self.cols.items():
            if c.type == "f": c.fmt = fmt_float
            if c.type == "d": c.fmt = fmt_date
    
    def write(self, dst, sep = ",", verbose = False, fmt_date = None, fmt_float=None):
        """ Writes table to file text file.
            :param dst: full path to where file should be saved.
            :param sep: string used as separator.
            :param verbose: flag. If true, print some extra information.
        """
        if verbose:
            print("Writing table to: ")
            print("   " + dst)
        
        # Convert to strings first. 
        self.setFormats(fmt_float, fmt_date)
        for c in self:
            c.convertToString()
            
        self.addMissingValues() # This only makes sense if we convert to strings first
        self.display(writeTitle = False, sep = sep) # DEBUG
 
        f = open(dst, "w")
        self.display(writeTitle = False, out = f, sep = sep)
        f.close()

    def convert(self, cols, fmt, fmt_date = "%d/%m/%Y %H:%M", fmt_float="%g"):
        """ Attempt to convert each column of this table to the specified format 
            provided in the list fmt.
            The original table should contain only strings. 
            
            :param cols: list with columns indexes that should be converted.
            :param fmt: a list with single characters that specify the format of each column.
                        Allowed types ["i", "f", "d", "s"].
                        If shorter than cols, then the last element is repeated.
            :param fmt_date: a string that specificies the format that should be used to convert dates.
            :param fmt_float: a string that specifies the format that should be used to read floats from strings.
        """
        for f in fmt:
            assert f in Types.ALLOWED_TYPES
        
        # Change it for long tables
        if len(fmt) < len(cols):
            missing = len(cols) - len(fmt)
            # repeat the last type to complete the number of columns
            append = missing * [fmt[-1]]
            fmt = fmt + append
        elif len(fmt) == len(cols):
            pass
        else:
            assert False
            
        assert len(fmt) == len(cols)
        
        for i in range(len(cols)):
            idx = cols[i]      
            c = self.cols[idx]
            assert c.type == "s", c.name
            ff = fmt[i]
            sfmt = fmt_date if ff == "d" else fmt_float
            c.convertFromString(fmt = sfmt, ntype = ff)
    
    def toH5(self, dst, fmt_date = "%d/%m/%Y %H:%M:%S", root = None, append = False):
        """ Saves table to HDF5 file.
            :param root: name of group that will be used to save this table. DEFAULT=/
        """
        from datetime import datetime as dt
        assert not H5_OFF, "h5py is not available"
        print("WARNING<Table.toH5>: Strings are limited to %d characters"%(Types.MAX_STRING_LEN_NUMPY))
        print("WARNING<Table.toH5>: Dates are saved as strings of max %d characters"%(Types.MAX_STRING_DATE_LEN_NUMPY))
        
        flag = "w" if not append else "r+"
        h5 = h5py.File(dst, flag)
        
        if root:
            g = h5.create_group(root)
        else:
            g = h5
        g.attrs["table"] = self.name
        g.attrs["date"] = dt.now().strftime("%d_%m_%Y__%H_%M_%S")
        
        for c in self:
            #print("COLUMN NAME: " + c.name)  # DEBUG
            dtype = Types.getH5Type(c.type)
            nelem = len(c)
            dset = g.create_dataset(c.name, (nelem), dtype=dtype, compression = "gzip")
            if c.type == "d":
                cc = c.clone()
                cc.convertToString(fmt_date)
            else:
                cc = c
            
            dset[:] = cc.data[:]
            #for i in range(len(cc)):
            #    dset[i] = cc[i]
        
        h5.close()
        
    @staticmethod
    def read(src, sep = ",", convert = False, header = 1, verbose = False, allowRepetition = False, fmt_date=None, fmt_float=None, encoding="utf-8"):
        """ Reads table from text file. 
            :param src: full path to file that should be read.
            :param sep: string used as separator.
            :param convert: if True, then try to convert strings to values. 
            :param verbose: flag. If true, print some extra information.
            :param allowRepetition: If true, then repeated ids for columns are allowed. Ids that are repeated are modified by appending a number. 
            :param fmt_date: string that specifies the format used to read dates from strings.
                             Only used if the file contains dates. 
            :param header: number of lines that contain header. DEFAULT = 1
            :param encoding: enconding of src. DEFAULT to utf-8.
                             See https://docs.python.org/3/library/codecs.html#module-codecs
        """
        print("Reading table from: ")
        print("   " + src)

        # This is required, so dates are converted correctly when read it.
        if fmt_date: Types.FMT_DATE = fmt_date

        t = Table(name = src)

        f = open(src, "r", encoding = encoding)
        lines = f.readlines() # no problem for files that are less than few Gb
        f.close()

        # headers
        h = _split_line(lines[0], sep)
        if header == 1:
            for hh in h:
                t.addCol(hh, data = [], allowRepetition= allowRepetition)
        elif header == 0:
            for i in range(len(h)):
                colname = "col%03d"%(i)
                t.addCol(colname, data = [], allowRepetition= allowRepetition)
        else:
            assert False, "Did not expect header = " + str(header)

        if verbose: 
            print(  "   Number of columns: " + str(len(t)) )
            scols = "   [" + ",".join(t.ids) + "]"
            print(scols)

        # data
        for line in lines[header:]:
            v = _split_line(line, sep)
            assert len(v) == len(t), line 
            for i in range(len(t)):
                t.getColByPosition(i).append(v[i])  # OPTIMIZE LATER
        t._setMaxRows()
        
        if convert:
            if fmt_date: Types.FMT_DATE = fmt_date
            if fmt_float: Types.FMT_FLOAT = fmt_float
            t.removeMissingValues()
            for c in t: c.convertFromString()
            
        return t

    @staticmethod
    def touchit(src, replace, dst = None, src_encoding="utf-8", dst_encoding="utf-8"):
        """ Replace each appearance of old string by new string specified in the list replace. 
        
            This is useful when a file needs some touches before it 
            can imported into a Table, e.g. replace "," by a "." as decimal
            separator. It also allows changing the encoding of a text file.
            
            It is a very simple version of what is provided by grep or similar
            programs.
            
            :param src: full path to source file.
            :param replace: a list of (old,new) regexes that must be substituted.
                            Replacement is performed one by one in the given order of 
                            pairs.
            :param dst: if present, then new file is writen to this path.
                        if not present (default), existing file is overwritten.
            
            :param src_encoding: encoding for the src file. DEFAULT to UTF-8 as in Python 3.X.
            :param dst_encoding: encoding for the dst file. DEFAULT to UTF-8 as in Python 3.X.
                             See https://docs.python.org/3/library/codecs.html#module-codecs
            
            NOTE: All content of the file is read in memory to make the process
                  faster. And the replacement is done all at once by calling 
                  replace(old, new). So, at least 2x memory is needed, where 
                  x is the size of the original file. 
        """
        assert _is_iterable(replace)
        
        s = open(src, "r", encoding=src_encoding)
        txt = s.read()
        s.close()
        
        for r in replace:
            old = r[0]
            new = r[1]
            txt = txt.replace(old, new)
        
        if not dst: dst = src
        #print(dst) # DEBUG
        #input("PRESS ENTER")
        w = open(dst, "w", encoding=dst_encoding) 
        w.write(txt)
        w.close()
        #input("PRESS ENTER") # DEBUG
        
if __name__ == "__main__":
    t = Table("table0")
    t.addCol("time", [0, 0.1, 0.2, 0.3])
    t.addCol("pressure", [0.1, 1.2, 0.3, 2.5, 0.8])
    t.addCol("time", [0.2, 0.33, 0.4, 0.5], allowRepetition= True)
    for c in t: 
        print(c.name)
    
    t.select(filter = lambda i, n: True)
    t.summary()
