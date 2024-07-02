# INTRODUCTION

^PyTable is a small pure python library to work with tabular data stored as delimited 
text files.

The main purpose of PyTable is to make working with tabular data easy and even "enjoyable" (if that is possible).

It provides an interface for creating a table from lists of data and write it to and read it from text files. 
In addition, it provides some methods for filtering columns and data, and 
applying operations on data, e.g. mathematical operations on all elements 
of a column, computing max and min values, etc.

It is intended to be used to handle relatively small tables of up to a few MB (< 100 MB).
However, it is likely that will work withouth significant issues with larger tables.


# EXAMPLE

```
>> t = Table("table0")
>> t.add("time", [0, 0.1, 0.2, 0.3])
>> t.add("pressure", [0.1,1.2,0.3,2.5,0.8])
>>
>> # SOME EXAMPLES
>> # REMOVE ELEMENTS OF COLUMN PRESSURE THAT ARE > 1.0
>> t["pressure"].remove(filter = lambda x: x > 1.0)
>>
>> # COLLECT ELEMENTS OF COLUMN TIME THAT ARE < 0.2
>> vals = t["time"].collect(lambda x: x < 0.2)
>>
>> # SAVE TABLE TO FILE
>> t.write(dst = "table.csv", sep = ",", verbose = True)
>> 
>> # READ TABLE FROM FILE 
>> t1 = Table.read(src = "table.csv", verbose = True)
```

# GETTING STARTED

**PyTable** is a small library to work with tabular data, i.e. data stored
as columns in a text file. It includes methods to read/write tables, display (pretty print) tables,
filter/search/remove data, easily plot columns against each other, generate new tables from columns, etc.

It relies in only two main classes: Column (a simple wrapper around a Python list) and 
a Table (a wrapper around a list of Columns).

A **Column** has a name, a type (int, float, string or date), a list that contains the data (called data),
and a format that defines how data in the column must be pretty-printed.

A **Table** has a name and a list of columns.


The usual workflow involves creating or reading a Table, i.e.

```
from tbl import Table

# ALTERNATIVE 1
t = Table.read(src=path-to-file, sep=",")  # sep can be any regex

# After Table.read all columns are stored as strings, so they need to be 
# converted to the proper type before use. For example, for a table that 
# has 2 columns of integers and one column of strings
t.convert(cols = [0,1,2], types=["i","i","s"])

# It is usual that all columns have the same type, for e.g. floats
t.convert(cols=[], types=["f"]) #or, shorter
t.convert([],["f"])


# ALTERNATIVE 2
# alternatively, one can create a table from scratch
t  = Table("table0")
t.add("time", [2.0, 1.0, 4.0, 3.0])      # types are assigned automatically when Columns are added manually
t.add("temp", [0, 10, 40, 90])
t.add("pressure", [0.0, 1.5, 6.0, 11.0])
t.add("ec", [0, 25, 70, 130])  


# After the table has been created, it is a good idea to check what is stored on it
t.what()  # prints a summary of the columns in the table
t.wait()  # this line will stop the script and ask to press ENTER before continuing

# that should print something like this
#================================================================================
#Table: table0
#--------------------------------------------------------------------------------
#Col[ Pos]:                 Name 	 Type< 	    #Rows 
#--------------------------------------------------------------------------------
#Col[0000]:                 time 	   f< 	 00000004 
#Col[0001]:                 temp 	   i< 	 00000004 
#Col[0002]:             pressure 	   f< 	 00000004 
#Col[0003]:                   ec 	   i< 	 00000004 
#================================================================================

# Alternatively, one may want to loop over columns and print their content indiviually
for c in t: c.print()
```

do something with the stored data, e.g. sort/filter/transform, and write the new table
to a file.

```
t.save(dst=path-to-file, sep=",")
```

The easiest way to modify data is using direct access, e.g.

```
# Change the value of the second element of the third column
t[2][1] =   1.2 # indexing in Python starts at 0, so t[2] is the third column

# or, to make it more self-explanatory
t["Pressure"][1] = 1.2

# if multiple values must be changed, if could be easier,
c = t["Pressure"]  # c is a reference to the data stored in t, so any changes apply to both objects
c[1] = 1.2
c[2] = 2.0
c[3] = 2.4

# After modifying values is useful to print the table. 
# Formatting is controlled by calling t.setFormatStr() or by calling it on each Column
# There are 3 ways to print rows in a table:
t.head(10)    #prints first 10 rows, useful for long tables
t.tail(10)    #prints last 10 rows
t.print()     #prints full table to sys.stdout, check options in docs


# Finally, to add more elements to a column
t[0].append(2.4)
```

A common need when working with long tables is searching for specific columns,

```
# get the position of all columns that have a name that contains the word "Saturation"
idxs = t.index(filter = lambda c, name: "Saturation" in name)

# sometimes it is easier to create a new table that has only those columns
t1 = t.select(filter = lambda c, name: "Saturation" in name)

# Creating a table based on a filter that applies to values and column and row indexes,
t1 = t.subtable(func = lambda r, c, e: r in [0,3])  # creates a new table with only the first and fourth row

# similarly, to create a table that has only positive values (>= 0.0)
t2 = t.subtable(func = lambda r, c, e: e >= 0.0)

# of course, for all calls is possible to not use the name of the argument, e.g. func
```
**Important** new tables DO NOT SHARE data with original table, so changes do not propagate to the original.

There are many cases when it is necessary to locate data in the table, e.g. get all values greater than 100.0

```
values = t.collect(func = lambda r, c, e: e > 100.0)     # returns a standard list with values e > 100.0
```

There are other cases when one is interested in locating values, e.g. 
which is the row and column for all values greater than 250.0?

```
values = t.collectrc(func = lambda r, c, e: e > 100.0)   # returns a standard list of tuples (r,c,e) for e > 250.0
```


PyTable stores data in columns, so it has limited support to work with rows. However,
it is possible to get the elements in a row or a few rows,

```
r = t.row(1)        # returns a python list with elemens in second row
lr = t.rows([0,2])  # returns a list of two tuples that contain elements of the first and third rows.
```
**Important** rows returned as lists DO NOT share data with the table, so any changes apply to them
do not propagate to the source table.


The last two common tasks are related to transforming and plotting data on a table. 
For example, to convert times stored as seconds to days in all columns of a table

```
# maps assign the value of element e at row r in column c to the result of fun(r,c,e)
t.map(func = lambda r, c, e: e/ 86400.0)   # note that map changes the data *in-place*
```

There are a couple of similar functions for columns,
```
t[0].map(func = lambda r, c, e: e/ 86400.0)
tday = t[0].apply(func = lambda r, c, e: e/ 86400.0) # apply returns a standard list that stores the results
```

For the second task: To plot columns against each other, e.g. plot pressure and temperature versus time

```
plt = t.plotxy(xcols["time"], ycols["temperature", "pressure"], labels=["Time", "Temp/Pressure"])
# plt is just a handle to matplotlib.pyplot. 
# Check https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html for details

plt.legend()
plt.show()   
```

A handy way to plot all columns versus the first one (common task for the analysis of time series),
```
t.plotxy(xcols[0], ycols[-1])
```

To have figures with multiple plots (subplots)

```
import matplotlib.pyplot as plt

plt.subplot(2,1,1)
t.plotxy(xcols[0], ycols[1], new=False)

plt.subplot(2,1,2)
t.plotxy(xcols[0], ycols[2], new=False)

plt.show()
```

Finally, PyTable provides some convenience methods to work with dates, e.g.
to convert dates stored in a columns as strings "day/month/year" to a datetime object

```
c = Column("dates").addData(["01/05/1977 00:00:00", "01/07/1977 00:15:20"]) 
c.convert("d", fmt = "%d/%m/%Y %H:%M:%S")
```

I recommend working with elapsed time instead of dates, though, so

```
# returns days since January 1st, 1990, for dates stored in column c 
te = c.telap(start = "01/01/1990", fmt_date = '%d/%m/%Y') 
```


# INSTALLATION

The recommended way to use is to set the PYTHONPATH dynamically within the script,
e.g. add these two lines to the beginning of the script

```
import sys
sys.path.append('/home/paulo/Documents/Programming/pytable')
```

Alternatively, the package can be installed in the default Python site-package:
Go to the source directory and type: ```python setup.py install```


# DOCUMENTATION

This file together with the included examples in the examples directory in the
source tree provide enough information to start using the package. 

There is also reference documentation for all classes and methods in the package 
in the docs folder distributed with the sources.


# REQUIREMENTS

    - Python3 (tested with Python 3.7)
    - h5Py, only required to export to/and import from HDF5 files  [OPTIONAL]
    - matplotlib.pyplot [OPTIONAL]
    - Numpy [OPTIONAL]
    

# DEVELOPMENT

## DESIGN GUIDELINES:

The design of the package considered the following objectives:

1. Self-contained. The package does not require any external library.

2. Easy of use. It tries to make working with tabular data easy and flexible. It provides
   default methods for simple operations, but it also implements methods that accept
   functions as parameters (i.e. a functional interface), e.g. map, apply, etc. hence
   it is also possible to implement additional operations with minimum effort.

3. Performance was considered as part of the design, but it was not an objective. 
   However, it is possible to work with tables that contain few hundred or even millions of 
   elements and hundred of columns with ease. 


## CONTRIBUTE:

I am open to incorporate bug fixes and additional improvements contributed by other
developers. As a non-native English speaker, I would also appreciate proof reading of
the this page and interesting examples to demonstrate the use of the PyTable.


# SUPPORT:

I will continue releasing this package as open source, so it is free to be used 
in any kind of project. I will also continue providing support for simple questions 
and making incremental improvements as time allows. However, I also  provide 
contract based support for commercial or research projects interested in this 
package and/or I am open to discuss possible commercial licensing.

For further details, please contact me to: paulo.herrera.eirl@gmail.com.

^ PyTable is a small library to work with relatively small data sets and should not be
  confused with PyTables, which was developed to work with large data sets in distributed
  environments. 
  ** BOTH PROJECTS ARE NOT AFFILIATED. **
