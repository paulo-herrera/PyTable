######################################################################################
# MIT License
# 
# Copyright (c) 2010-2024 Paulo A. Herrera
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
######################################################################################
__docformat__ = "google"

"""
**PyTable** is a small python library to work with tabular data stored as delimited 
text files.

The main purpose of PyTable is to make working with tabular data easy and even "enjoyable" (if that is possible).

## Features

PyTable provides:

   + Methods for easy reading from and writing to text files. For example, to read a table separated by ",", with a header row and two first lines that should be skipped:
   
   ```
   from tbl.table import Table
   
   # sep can be a full regex
   t = Table.read("path-to-table.txt", sep="\t", header=1, skip=2)
   
   #.... so something with the table .....
   t.save(dest="path-to-file.csv", sep=',', columnWidth=10, missing='-', verbose=False)
   ```
   + Methods to export tables to other formats, e.g. to save a table as an HDF5 file
   ```
   # requires H5PY installed
   t.toH5(dst="path-to-.h5")
   ```
   
   
   + Methods to display information in tables, e.g. to see all columns in the table, or to display the first 5 rows of the table or the last 5 rows,
   
   ```
   t.what()
   t.head(5) 
   t.tail(5) 
   ```
   
   + Methods to look for data, e.g. to get the column indexes for a list of columns with headers in the list h,
   
   ```
   h = ["Time1", "Time2"]
   cols = t.index(h)
   ```
   
   + Methods to add data and to convert data to other types, e.g. to convert elements in column *Pressure* to floats,  or to convert all columns
   
   ``` 
   t["Pressure"].convert["f"] 
   t.convert(cols=[], types=["f"])
   ```
   or, to get the data in column 2 as a Numpy array
   
   ```
   a = t[2].np()
   ```
   
   To merge to tables, i.e. append data from table2 to table1,
   
   ```
   t1.append(t2)
   ```
   
   + Methods to filter columns and data to create new tables, e.g. to create a new table with only columns that have a header that contains the word "Time", 
   
   ```
   st = t.select(filter = lambda c, name: "Time" in name)
   ```
   
   + Methods to work with data in columns using a functional style, e.g.
   
   ```
   col = t["Pressure[Pa]"]
   # transform to kPa and add a new column
   colk = col.clone()
   colk.map(func = lambda i, e: e / 1000.0)
   t.addColumn("Pressure[kPa]", colk)
   ```
   
   or, to remove all values greater than 20.0
   
   ```
   col.remove(filter = lambda i, c: c > 20.0)
   ```
   
   or, to collect all values that are less than 100.0,
   
   ```
   vals = col.collect(filter= lambda i, e: e < 100.0)
   ```
   
   or, to obtain the minimun value in the column
   
   ```
   minval = col.reduce(func = lambda (i, e, result): e if e < result else result, result = BIG_NUMBER)

   ```
   
   + Methods to better document data stored in columns, e.g.
   
   ```
   t["Pressure"].setAttr("Units","Pa")
   ```
   
   + Methods for simple analysis of data in columns, e.g.
   ```
   stats = col.stats(verbose=True) # print to stdout
   ```
   
   + Methods to plot data in columns, e.g. to plot all columns versus the first column
   
   ```
   #requires MATPLOTLIB installed
   plt = t.plotxy(xcols=[0], ycols=[-1])
   
   # plt is a handle to the matplotlib.pyplot module, so...
   plt.savefig("path-to-png")
   plt.show()
   ```
   
## Design guidelines

+ Tabular data stored as text files tend to be *small* for current standards, e.g. less than a few MB. Then, performance is less of a concern versus convenience or easy use. **PyTables** uses a few programming practices that are known to be *slow*, but that makes its use more convenient.

+ Try to provide only **one way** to do things.

+ Try to use functional style to handle data.

+ Library should be small and rely only in common python packages.


## Caveats

**PyTable** is a relatively young library, so expect changes in the future.

**PyTable** is a small library to work with relatively small data sets and should not be
confused with PyTables, which was developed to work with large data sets in distributed
environments. **BOTH PROJECTS ARE NOT AFFILIATED.**

"""
