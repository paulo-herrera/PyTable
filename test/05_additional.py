""" Random collection of scripts that show different ways to accomplish some 
    common tasks.
"""
from tbl.table import Table
from tbl.helpers import file_hash, timeit

def subtable():
    t = Table("intersection")
    nrows = 30
    a = [i for i in range(nrows)]
    b = [i * i for i in range(nrows)]
    
    t.addColumn("i", a)
    t.addColumn("i*i", b)
    
    f1 = t[0].indexes(filter = lambda i, e: i > 5)
    f2 = t[1].indexes(filter = lambda i, e: e < 100)
    
    t2, idx = t.table(f1, f2)
    t2.print()
    print(idx)
    

def create_date_elap_time_list():
    from tbl.helpers import datetime_list, elapsed_time
    
    dates = datetime_list(year0 = 1970, year1 = 2023, monthly=True, verbose=False)
    telap = elapsed_time(dates, start="01/01/1970 00:00:00", fmt_date = "%d/%m/%Y %H:%M:%S", verbose=True, verbose2=True)


def read_save_table():
    from tbl.table import Table
    from tbl.helpers import  elapsed_time
    src = r"Z:\Documents\ProjectSWM\tmp4_pytable\pytable\test\data\biggertable.dat"
    t = Table.read(src, sep=";", header=0, skip = 0)
    #t.what()   # CHECK
    t.remove([2,3])
    
    t.convert([0], ["d"], fmt_date="%Y-%m-%d %H:%M")
    t.convert([1], ["f"])
    t[0].name = "Dates"
    t[1].name = "WL(m)"
    
    t.what(wait=True)
    #t.head(40)
    
    telap = elapsed_time(t[0].data, start="01/01/1970", fmt_date="%d/%m/%Y", verbose=True)
    t.addColumn("telap_01_01_1970", telap)
    #check results
    t.what()
    t.head(20)
    
    dst = r"Z:\Documents\ProjectSWM\tmp4_pytable\pytable\test\bigtable_modified.csv"
    t.write(dst, sep=",", verbose=True)
    
    # next step should not be necessary. FIX BUG in toH5
    #t.convert([0],["s"], fmt_date="%d/%m/%Y %H:%M:%S")
    dst = r"Z:\Documents\ProjectSWM\tmp4_pytable\pytable\test\bigtable_modified.h5"
    #This takes a while, but file size is reduced by almost 10X
    # almost the same time without compressing.
    t.toH5(dst, compress=True, verbose=True, root=None) 


def hash():
    src = "data/biggertable.dat"
    file_hash(src, verbose=True) # TIMEIT LATER


if __name__ == "__main__":
    #create_date_elap_time_list()
    #read_save_table()
    #subtable()
    hash()
    