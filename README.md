# INTRODUCTION

*PyTable* is a small python library for working with data stored as delimited 
text files, e.g. comma delimited files (.csv). The main purpose is making 
the work with tabular data easy and even "enjoyable" (if that is possible).

It is intended to be used to handle relatively small tables of up to a few MB (<= 100 MB).
However, it can work with larger files withouth significant issues.


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

*PyTable* is a small library for working with tabular data, i.e. data stored
as columns in a text file. It includes methods to read/write and display (pretty print) tables,
filter/search/remove data, easily plot columns against each other, generate new tables, etc.
It includes two main classes: Column (a simple wrapper around a Python list) and 
a Table (a wrapper around a list of Columns).

A **Column** has a name, a type (int, float, string or date), a list that 
contains the data, and a format that defines how data in the column must 
be pretty-printed.

A **Table** has a name and a list of columns.


The usual workflow involves creating or reading a Table, i.e.

```
from tbl import Table

# ALTERNATIVE 1
t = Table.read(src=path-to-file, sep=",")  # sep can be any regex

# After calling Table.read, all columns are stored as strings, so they need 
# to be converted to the proper type before use. For example, for a table that 
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


# After the table has been created, it is a good idea to check what is stored in it
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

# Alternatively, one may want to loop over columns and print their content
for c in t: c.print()
```

then, do something with the stored data, e.g. sort/filter/transform or write 
the new table to a file.

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

# To add more elements to a column
t[0].append(2.4)

# After modifying values, it is useful to print the table. 
# Formatting is controlled by calling t.setFormatStr() or by calling it on each Column
# There are 3 ways to print rows in a table:
t.head(10)    #prints first 10 rows, useful for long tables
t.tail(10)    #prints last 10 rows
t.print()     #prints full table to sys.stdout, check options in docs

```

A common need when working with long tables is searching for specific columns,

```
# get the position of all columns that have a name that contains the word "Saturation"
idxs = t.index(filter = lambda c, name: "Saturation" in name)

# sometimes it is easier to create a new table that has only those columns
t1 = t.select(filter = lambda c, name: "Saturation" in name)

# Creating a table based on a filter that applies to (c)olumn,  (r)ow indexes and/or (v)alues,
t1 = t.subtable(func = lambda r, c, v: r in [0,3])  # creates a new table with only the first and fourth row

# similarly, to create a table with only elements that are greater than zero
t2 = t.subtable(func = lambda r, c, v: v >= 0.0)

# of course, it is possible to not use the name of the argument for all calls, e.g. func,
# so the script is self-documented and easier to read/understand
```

**Important** new tables DO NOT SHARE data with the original table, so changes 
do not propagate to the original one.


There are many cases when it is necessary to collect values in the table 
that satisfy some criteria, e.g. get all values greater than 100.0

```
values = t.collect(func = lambda r, c, v: v > 100.0)     # returns a standard list with values v > 100.0
```

There are other cases when one is interested in locating the position in 
the table for values that satisfy some criteria, e.g. which are the rows 
and columns for values greater than 250.0?

```
values = t.collectrc(func = lambda r, c, v: v > 100.0)   # returns a standard list of tuples (r,c,v) for v > 250.0
```


*PyTable* stores data in columns, so it has limited support to work with rows. 
However, it is possible to get the elements stored in a row or a few rows,

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

To plot columns against each other, e.g. temperature measured at two sensors 
versus time

```
plt = t.plotxy(xcols["time"], ycols["Sensor1", "Sensor2"], labels=["Time", "Temperature [C]"])
plt.show()   

# plt is just a handle to matplotlib.pyplot. 
# Check https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html for details
```

A handy way to plot all columns versus the first one (common task for time series analysis),
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

Finally, *PyTable* provides some convenience methods to work with dates, e.g.
to convert dates stored in a column as strings "day/month/year" to a datetime object

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

The recommended way to use *PyTable* is setting the PYTHONPATH dynamically 
within the script, e.g. add these two lines to the beginning of the script

```
import sys
sys.path.append('/home/user/Documents/Programming/pytable')
```

Alternatively, the package can be installed in the default Python site-package:
go to the source directory and type ```python setup.py install```


# DOCUMENTATION

This file together with the examples directory in the
source tree provide enough information to start using the package. 

The docs folder distributed with the source package contains reference 
documentation for all classes and methods as standard html files.


# REQUIREMENTS

    - Python3 (tested with Python 3.7)
    - h5Py, only required to export to/and import from HDF5 files  [OPTIONAL]
    - matplotlib.pyplot [OPTIONAL]
    - Numpy [OPTIONAL]
    

## CONTRIBUTE:

I am open to incorporate bug fixes and additional improvements contributed by other
developers. As a non-native English speaker, I would also appreciate proof reading of
the this page and interesting examples to demonstrate the use of *PyTable*.


# SUPPORT:

I will continue releasing this package as open source, so it is free to be used 
in any kind of project. I will also continue providing support for simple questions 
and making incremental improvements as time allows.


  *PyTable* is a small library to work with relatively small data sets and 
  should not be confused with **PyTables**, which was developed to work with 
  large data sets in distributed environments. ** BOTH PROJECTS ARE NOT AFFILIATED. **
