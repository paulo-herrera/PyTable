# INTRODUCTION

^PyTable is a small pure python library to work with tabular data stored as delimited 
text files.

The main purpose of PyTable is to make working with tabular data easy and even "enjoyable" (if that is possible).

It provides an interface for creating a table from lists of data and write it to and read it from text files. In addition, it provides some methods for filtering columns and data, and applying operations on data, e.g. mathematical operations on all elements of a column, computing max and min values, etc.

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
# The read table has all columns stored as strings, so they need to be 
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
t.wait()  # this line will stop the script and ask to press ENTER

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
```

do something with the stored data, e.g. sort/filter/transform, and write the new table
to a file.

```
t.save(dst=path-to-file, sep=",")
```

The easiest way to modified data is using a direct access, e.g.

```
# Change the value of the second element of the third column
t[2][1] =   1.2 # indexing in Python starts at 0, so t[2] is the third column

# or, to make self-explanatory
t["Pressure"][1] = 1.2

# if multiple values must be changed, if could be easier,
c = t["Pressure"]  # c is a reference to the data stored in t, so any changes applied to both objects
c[1] = 1.2
c[2] = 2.0
c[3] = 2.4

# after modifying values is useful to print the table, 3 ways
t.head(10)  #prints first 10 lines, useful for long tables
t.tail(10)  #prints last 10 lines
t.print()   #prints full table to sys.stdout, check options in docs
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

    - Python 3 (tested with Python 3.7)
    - h5Py, only required to export to/and import from HDF5 files  [OPTIONAL]

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

## DEVELOPER NOTES:

It is useful to build and install the package to a temporary location without
touching the global python site-packages directory while developing. To do
this, while in the root directory, one can type:

    1. python setup.py build --debug install --prefix=./tmp
    2. export PYTHONPATH=./tmp/lib/python2.7/site-packages/:$PYTHONPATH (UNIX)
	2. set PYTHONPATH=%ROOT_DIR%/tmp/lib/site-packages/;%PYTHONPATH%             (WINDOWS)

NOTE: you may have to change the Python version depending of the installed
version on your system. 

To test the package one can run some of the examples, e.g.:
./tmp/lib/python2.7/site-packages/pytable/examples/XXXX.py

That should create a XXXX.csv file in the current directory.

An alternative is creating a virtual environment as explained here:
https://docs.python.org/3/tutorial/venv.html

To generate distribution files (tar.gz and .whl files) in build directory:

1. python setup.py sdist
2. python setup.py bdist_wheel

To create docs from the root directory type:
    pdoc -d google -o ./docs ./tbl
    
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
