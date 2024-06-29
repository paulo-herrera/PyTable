# INTRODUCTION

^PyTable is a small pure python library to work with tabular data stored as delimited 
text files.

The main purpose of PyTable is to make working with tabular data easy and even "enjoyable" (if that is possible).

It provides an interface for creating a table from lists of data and write it to and read it from text files. In addition, it provides some methods for filtering columns and data, and applying operations on data, e.g. mathematical operations on all elements of a column, computing max and min values, etc.

# EXAMPLE

```
>> t = Table("table0")
>> t.addColumn("time", [0, 0.1, 0.2, 0.3])
>> t.addColumn("pressure", [0.1,1.2,0.3,2.5,0.8])
>>
>> # SOME EXAMPLES
>> # REMOVE ELEMENTS OF COLUMN PRESSURE THAT ARE > 1.0
>> t.getColumnByName("pressure").remove(filter = lambda x: x > 1.0)
>>
>> # COLLECT IN A LIST ELEMENTS OF COLUMN TIME THAT ARE < 0.2
>> vals = t.getColumnByName("time").collect(lambda x: x < 0.2)
>>
>> # SAVE TABLE TO FILE
>> t.write(dst = "table.csv", sep = ",", verbose = True)
>> 
>> # READ TABLE FROM FILE 
>> t1 = Table.read(src = "table.csv", verbose = True)
```

# INSTALLATION

Go to the source directory and type:
python setup.py install

# DOCUMENTATION

This file together with the included examples in the examples directory in the
source tree provide enough information to start using the package.

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
