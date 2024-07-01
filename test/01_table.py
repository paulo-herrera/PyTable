import sys
sys.path.append('/home/paulo/Documents/Programming/pytable')

from tbl.table import Table
from tbl.column import Column
from tbl.helpers import timeit

def test00_create_add():
    t = Table("table0").add("time", [0.0, 0.1, 0.2, 0.3])
    t.add("pressure", [0.1, 1.2, 0.3, 2.5, 0.8])
    print(t)
    
    t1 = Table("table1")
    a = [1,2,3,4,5]
    c = Column("c1").addData(data=a,ctype=a[0])
    t1.add(c.name, c)
    t1.head()
    t1.what()

def test01_setname():
    t = Table("table0").add("time", [0.0, 0.1]).setName("ttable1")
    assert t.name == "ttable1" 

def test02_all():
    t = Table("table0").add("time", [0.0, 0.1, 0.2]).add("pressure", [0.0, 1.2, 0.0])
    all = t.all()
    assert len(all) == 2
    assert all[1] == 1
    
def test03_names():
    t = Table("table0").add("time", [0.0, 0.15, 0.3]).add("pressure", [0.0, 1.2, 0.0])
    ids = t.names() 
    assert len(ids) == 2
    assert ids[1] == "pressure"
    
    ids = t.names(case="U")
    assert len(ids) == 2
    assert ids[1] == "PRESSURE"
    
def test04_index():
    t = Table("table0")
    t.add("time", [0.0, 0.1, 0.2, 0.3])
    t.add("pressure", [0.1, 1.2, 0.3, 2.5, 0.8])

    id0 = t.index(["time"])
    print(id0)
    assert len(id0) == 1
    assert id0[0] == 0
    
    id1 = t.index(["pressure"])
    assert id1[0] == 1

def test05_has():
    t = Table("table0").add("t", [0.0, 0.1]).add("p", [0.1, 1.2])
    a = t.has("t")
    assert a
    
    a = t.has("q")
    assert not a
    
    a = t.has(1)
    assert a
    
    a = t.has(2)
    assert not a

def test06_add():
    t = Table("table0")
    t.add("t", [0.0, 0.1])
    t.add("p")
    c = Column("col").addData([1,2,3])
    t.add(c.name, c)
    
    try:
        t.add("t", allowRepetition=False)
        assert False
    except:
        assert True
        
    t.add(data = [1, 2, 3]) # no name
    c = t[3]
    c.name == "col03", c.name
    
    
def test07_len():
    t = Table("table0").add("time", [0.0, 0.0, 0.0, 0.3]).add("pressure", [0.0, 1.2, 0.0, 0.0, 0.0])
    assert len(t) == 2

def test08_iter():
    t = Table("table0").add("time", [0.0, 0.0]).add("pressure", [0.0, 1.2])
    for c in t: 
        #print(c)
        pass

def test09_item():
    t = Table("table0").add("time", [0.0, 0.0]).add("pressure", [0.0, 1.2])
    c = t[0]
    assert c.name == "time"
    
    c = t["time"]
    assert c.name == "time"
    
    c = t[5]
    assert not c

def test10_at():
    t = Table("table0").add("c1", [0.0, 0.0]).add("c2", [0.0, 1.2]).add("c3", [1, 2])
    c = t.at([0,2])
    assert c[0].name == "c1"
    assert c[1].name == "c3"
 
def test11_pop():
    t = Table("table0").add("c1", [0.0, 0.0]).add("c2", [0.0, 1.2]).add("c3", [1, 2])
    assert len(t) == 3
    
    c = t.pop("c2")
    assert c.name == "c2"
    assert len(t) == 2
    
    c = t.pop(0)
    assert len(t) == 1
    assert c.name == "c1"
    
def test12_remove():
    t = Table("table0")
    for i in range(25):
        t.add(data=[1, 2, 3, 4, 5])
    assert len(t) == 25
    
    cols = t.remove([1, 5, 10, 14])
    assert len(t) == 21
    #for c in cols: print(c)
    
def test13_select():
    t = Table("table0").add("p1", [0.0, 0.0]).add("t1", [0.0, 1.2]).add("e1", [1, 2])
    t2 = t.select(filter=lambda i, name: i <= 1)
    assert len(t2) == 2
    
    t2 = t.select(filter=lambda i, name: "p" in name)
    assert len(t2) == 1
    assert t[0].name == "p1"

def test14_clone():
    t = Table("table0").add("p1", [0.0, 0.0]).add("t1", [0.0, 1.2]).add("e1", [1, 2])
    t2 = t.clone(shallow=True)
    assert t.name + "(Copy)" == t2.name
    assert len(t2) == len(t)
    
    t2 = t.clone(shallow=False, newName="t2")
    assert t2.name == "t2"
    assert len(t2) == len(t)
    # check deep copy

def test15_append():
    t  = Table("table0").add("p1", [0.0, 1.0]).add("t1", [1, 2]).add("e1", ['a', 'b'])
    t2 = Table("table1").add("p1", [2.0, 3.0]).add("t1", [3, 4]).add("e1", ['c', 'd'])
    assert t.nrows() == 2
    assert t.ncols() == 3
    
    t.append(t2)
    assert t.nrows() == 4
    assert t.ncols() == 3
    
    assert t[2][2] == 'c'
    assert t[1][2] == 3

def test16_ncols_nrows():
    t  = Table("table0").add("p1", [0.0, 1.0]).add("t1", [1, 2, 3, 4]).add("e1", ['a', 'b'])
    assert t.nrows() == 4
    assert t.ncols() == 3

def test17_what():
    t  = Table("table0").add("p1", [0.0, 1.0]).add("t1", [1, 2, 3, 4]).add("e1", ['a', 'b'])
    t.what()

def test18_print():
    t  = Table("table0").add("p1", [0.0, 1.0]).add("t1", [1, 2, 3, 4]).add("e1", ['a', 'b'])
    print("DEFAULT FORMATTING")
    t.print()
    
    print("FORMATTED")
    t.setFormatStr(fmt_int="%04d", fmt_float="%4.2f", fmt_date=None, fmt_str="%10s")
    t.print()

def test19_head_tail():
    t  = Table("table0")
    d1 = [i for i in range(99)]
    d2 = [i*1.0 for i in range(99)]
    t.add("p1", d1)
    t.add("t1", d2)
    
    t.head(5)
    
    t.tail(5)
    
def test20_print_file():
    t  = Table("table0").add("p1", [0.0, 1.0]).add("t1", [1, 2, 3, 4]).add("e1", ['a', 'b'])
    
    t.setFormatStr(fmt_int="%04d", fmt_float="%4.2f", fmt_date=None, fmt_str="%10s")
    dst = open("test_01table_print_file.txt", "w")
    t.print(sep=",", out = dst, verbose = True).close()

def test21_write():
    t  = Table("table0").add("p1", [0.0, 1.0]).add("t1", [1, 2, 3, 4]).add("e1", ['a', 'b'])
    t.save("test_01table_write.txt", verbose = True)

def test22_read():
    src= "./data/dates1.csv"
    t, sk = Table.read(src, sep=",", header=1, verbose=True)
    t.what()
    t.print()

def test23_read_big():
    src= "./data/bigtable.csv"
    t,sk = Table.read(src, header=0, verbose=True)
    #t.what()
    t.print(maxRows=15)

def test24_read_empty_column():
    src= "./data/dates3.csv"
    t, sk = Table.read(src, sep=",", header=1, verbose=True, removeEmptyColumn=False, skip=1)
    assert len(t) == 4
    t.what()
    #t.print()
    
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("AFTER REMOVING EMPTY COLUMNS")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    t, sk = Table.read(src, sep=",", header=1, verbose=True, removeEmptyColumn=True, skip=1)
    assert len(t) == 2
    t.what()

def test25_convert():
    t  = Table("table0").add("p1", ["0.0", "1.0"]).add("t1", ["1", "2", "3", "4"]).add("e1", ['a', 'b'])
    #t.what()
    
    t.convert(cols=[0, 1], types=["f", "i"])
    #t.what()
    #t.print(2)
    
    t.setFormatStr("%d","%f","%d/%m/%Y","<<%s>>")
    #print(t[2].fmt)
    t.convert(cols=[2], types=["s"])
    t.what()
    #t.print(2)
    
    t  = Table("table0").add("p1", ["0.0", "1.0", "2.0", "3.0"]).add("t1", ["1", "2", "3", "4"])
    t.wh()
    t.convert(cols=[], types=["f"])
    t.wh()

def test26_convert_date():
    t  = Table("table0")
    t.add("d1", ["01.01.1900", "02.01.1900"])
    t.add("d2", ["01/01/1900 00:00:00", "02/01/1900 00:15:00"])
    t.what()
    
    t.setFormatStr("%d","%g","%d.%m.%Y","%s") # only used for printing
    print(t[0])
    
    t.convert([0], ["d"], fmt_date = "%d.%m.%Y")
    t.what()
    t.head(2)
    
def test27_io():
    t  = Table("table0")
    t.add("p1", [0.0, 1.0])
    t.add("t1", [1, 2, 3, 4])
    t.add("e1", ['a', 'b'])
    assert len(t) == 3, "len(t): " + str(len(t))
    t.what()
    t.head()
    t.save("test_01table_io.txt")
    
    t0, sk = Table.read("test_01table_io.txt")
    t0.what()
    t0.head()
    for c in t0: print(c.name)
    assert len(t0) == 3, "len(t0): " + str(len(t0)) # trailing separator
    
def test28_toh5():
    fpath = "test_01table_toh5.h5"
    t  = Table("table0")
    t.add("floats", [0.0, 1.0])
    t.add("ints", [1, 2, 3, 4])
    t.add("strings", ['a', 'b'])
    t.add("dates", ['01/01/1970 00:00:00', '01/03/1980 00:15:00'])
    t.convert([3], ["d"], fmt_date = "%d/%m/%Y %H:%M:%S")
    t.setFormatStr("%d", "%g", "%d/%m/%Y %H:%M:%S", "%s")
    t.toH5(dst=fpath, root=None, append=False, verbose=True, fmt_date="%d/%m/%Y %H:%M:%S")
    t.what().wait()
    
    t, fpath = t.fromH5(src=fpath, root = None, verbose = True)
    t.what()

def test29_plotxy():
    t  = Table("table0")
    t.add("time", [0.0, 1.0, 2.0, 3.0])
    t.add("temp", [0.0, 1.0, 4.0, 9.0])
    t.add("pressure", [0.0, 1.5, 6.0, 11.0])
    t.add("ec", [0.0, 2.5, 7.0, 13.0])
    p = t.plotxy(["time"], ["temp", "pressure"])
    p.show()
    
    p = t.plotxy([0], [1, 2])
    p = t.plotxy([0], [3], new = False)
    p.show()

def test30_row():
    t  = Table("table0")
    t.add("time", [2.0, 1.0, 4.0, 3.0])
    t.add("temp", [0, 10, 40, 90])
    t.add("pressure", [0.0, 1.5, 6.0, 11.0])
    t.add("ec", [0, 25, 70, 130])
    
    r = t.row(1)
    assert r[1] == 10
    assert r[3] == 25
    
    r = t.row(3)
    assert r[1] == 90
    assert r[3] == 130
    
def test31_rows():
    t  = Table("table0")
    t.add("time", [0.0, 1.0, 2.0, 3.0])
    t.add("temp", [0, 10, 40, 90])
    t.add("pressure", [0.0, 1.5, 6.0, 11.0])
    t.add("ec", [00, 25, 70, 130])
    
    rows = t.rows([1,3])
    assert len(rows) == 2
    assert len(rows[0]) == 4
    assert (rows[0][1] == 10)
    assert (rows[1][3] == 130)

# def test32_table():
    # t  = Table("table0")
    # t.add("time", [0.0, 1.0, 2.0, 3.0])
    # t.add("temp", [0, 10, 40, 90])
    # t.add("pressure", [0.0, 1.5, 6.0, 11.0])
    # t.add("ec", [0, 25, 70, 130])
    
    # t1, idx = t.table([1,3])
    # t1.what()
    # t1.head().wait()
    # assert len(t1) == 4
    # assert len(t1[0]) == 2
    # assert (t1[1][0] == 10)
    # assert (t1[3][1] == 130)
    # assert idx[0] == 1
    # assert idx[1] == 3
    
   
# def test33_table2():
    # t  = Table("table0")
    # t.add("time", [0.0, 1.0, 2.0, 3.0])
    # t.add("temp", [1, 10, 40, 90])
    # t.add("pressure", [2.0, 1.5, 6.0, 11.0])
    # t.add("ec", [3, 25, 70, 130])
    
    # t2, idx = t.table([0, 2, 3], [0, 1])
    # assert t2.nrows() == 1
    # assert t2[1][0] == 1
    # assert t2[3][0] == 3
    # assert len(idx) == 1
    # assert idx[0] == 0
 

def test34_issquare():
    t  = Table("original")
    t.add("time", [2.0, 1.0, 4.0, 3.0])
    t.add("temp", [0, 10, 40, 90])
    assert t.isSquare()
    
    t  = Table("original")
    t.add("time", [2.0, 1.0, 4.0, 3.0])
    t.add("temp", [0, 10, 40])
    assert not t.isSquare()
    
def test35_sort():
    t  = Table("original")
    t.add("time", [2.0, 1.0, 4.0, 3.0])
    t.add("temp", [0, 10, 40, 90])
    t.add("pressure", [0.0, 1.5, 6.0, 11.0])
    t.add("ec", [0, 25, 70, 130])
    t.print()
    
    t.sort(key = lambda x: x[0])
    t.setName("sorted")
    assert t[1][0] == 10
    assert t[3][0] == 25
    assert t[3][2] == 130
    t.print()
    
    t.sort(key = lambda x: x[0], reverse=True)
    t.setName("sorted_reverse")
    assert t[1][0] == 40
    assert t[3][0] == 70
    assert t[3][1] == 130
    t.print()
   
def test36_addID():
    t  = Table("original")
    t.add("time", [2.0, 1.0, 4.0, 3.0])
    t.add("temp", [0, 10, 40, 90])
    t.addID()
    t.what().wait()
    assert len(t) == 3
    assert t[0][0] == 0
    assert t[0][2] == 2
    
    t.name = "modified"
    t[2].append(120)
    t.addID(gen = lambda r: "row%02d"%r)
    t.what()
    t.tail().wait()
    assert len(t) == 3
    assert len(t[2]) == 5
    assert t[0][4] == "row04"
    
def test37_rename():
    t  = Table("original")
    t.add("time", [2.0, 1.0, 4.0, 3.0])
    t.add("pressure", [0.0, 1.2, 4.5, 9.2])
    t.add("temp", [0, 10, 40, 90])
    assert t.cols[0].name == "time"
    assert t.cols[2].name == "temp"
    
    t = t.rename({"time" : "time_00", "temp" : "temp_00"})
    assert t.cols[0].name == "time_00"
    assert t.cols[2].name == "temp_00"
    t.tail()

def test38_transpose():
    t  = Table("original")
    t.add("c1", [11, 21, 31])
    t.add("c2", [12, 22, 32])
    t.add("c3", [13, 23, 33])
    t.head()
    
    tt = t.transpose()
    tt.head()
    
    t.wh()
    tt.wh()


def test39_uniques():
    t  = Table("original")
    t.add("c1", [11, 21, 31])
    t.add("c2", [12, 22, 32])
    t.add("c1", [13, 23, 33], allowRepetition = True)
    t.add("c3", [13, 23, 33])
    t.head()
    
    tt = t.uniques()
    tt.head()

def test40_zip():
    t  = Table("original")
    t.add("time", [2.0, 1.0, 4.0, 3.0])
    t.add("pressure", [0.0, 1.2, 4.5, 9.2])
    t.add("temp", [0, 10, 40, 90])
    t.head()
    
    lz = t.zip(cols=[0,2])
    print(lz)

# def test41__intersect():
    # a = [1, 2, 3, 4]
    # b = [0, 2, 4, 6]
    # t = Table("t0")
    
    # c = t._intersect([a, b])
    # assert len(c) == 2
    # assert c[0] == 2
    # assert c[1] == 4

def test42__contains():
    t  = Table("original")
    t.add("time", [2.0, 1.0, 4.0, 3.0])
    t.add("temp", [0, 10, 40, 90])
    
    assert 0 in t
    assert 1 in t
    assert 2 not in t
    assert "time" in t
    assert "temp" in t
    assert "pressure" not in t

def test43__collect():
    t  = Table("original")
    t.add("time", [2.0, 1.0, 4.0, 3.0])
    t.add("temp", [0, 10, 40, 90])
    t.head()
    
    l = t.collect(func = lambda r, c, e: c==1 and e > 40)
    print(l)
    assert len(l) == 1
    assert l[0] == 90
    
def test44__collectrc():
    t  = Table("original")
    t.add("time", [2.0, 1.0, 4.0, 3.0])
    t.add("temp", [0, 10, 40, 90])
    t.head()
    
    l = t.collectrc(func = lambda r, c, e: c==1 and e > 40)
    print(l)
    assert len(l) == 1
    r, c, e = l[0]
    assert r == 3
    assert c == 1
    assert e == 90

def test45__map():
    t  = Table("original")
    t.add("time", [2.0, 1.0, 4.0, 3.0])
    t.add("temp", [0, 10, 40, 90])
    t.head()
    
    t1 = t.clone()
    t1 = t1.map(func = lambda r, c, e: 0 if (r == 3) else e) # change row 3 to 0
    assert int(t1[0][3]) == 0
    assert t1[1][3] == 0
    t1.head()
    
    t2 = t.clone()
    t2 = t2.map(func = lambda r, c, e: e * e if (c == 1) else e)
    assert t2[1][0] == 0
    assert t2[1][1] == 10*10
    assert t2[1][2] == 40*40
    assert t2[1][3] == 90*90
    t2.head()
    
    
def test46__subtable():
    t  = Table("original")
    t.add("time", [2.0, 1.0, 4.0, 3.0])
    t.add("temp", [0, 10, 40, 90])
    t.add("pressure", [0, 5, 8, 7])
    t.add("saturation", [0.2, 1.0, 0.1, 0.6])
    t.head()
    #t.what()
    
    t1 = t.subtable(func = lambda r, c, e: r in [0,3])
    t1.head()
    #t1.what()
    
    t2 = t.subtable(func = lambda r, c, e: c in [0,2])
    t2.head()
    #t2.what()
    
    t3 = t.subtable(func = lambda r, c, e: c == 1 and e >= 40)
    t3.head()
    #t3.what()
    
    t4 = t.subtable(func = lambda r, c, e: r == 1 and (e == 10 or e == 5))
    t4.head()
    #t4.what()

def testit(t, wait = False):
    #try:
        #timeit(t, source=False)
        print()
        print()
        print(50*"/")
        print("RUNNING >> " + t.__name__)
        t()
        print("PASSED>> " + t.__name__)
        #if wait: input("ENTER...")
    #except:
    #    print("FAILED>> " + t.__name__)  
    

def test_all():
    testit(test00_create_add, wait=False)
    testit(test01_setname, wait=False)
    testit(test02_all, wait=False)
    testit(test03_names, wait=False)
    testit(test04_index, wait=False)
    testit(test05_has, wait=False)
    testit(test06_add, wait=False)
    testit(test07_len, wait=False)
    testit(test08_iter, wait=False)
    testit(test09_item, wait=False)
    testit(test10_at, wait=False)
    testit(test11_pop, wait=False)
    testit(test12_remove, wait=False)
    testit(test13_select, wait=False)
    testit(test14_clone, wait=False)
    testit(test15_append, wait=False)
    testit(test16_ncols_nrows, wait=False)
    testit(test17_what, wait=False)
    testit(test18_print, wait=False)
    testit(test19_head_tail, wait=False)
    testit(test20_print_file)
    testit(test21_write)
    testit(test22_read, wait = True)
    testit(test23_read_big, wait = True)
    testit(test24_read_empty_column, wait = True)
    testit(test25_convert, wait=True)
    testit(test26_convert_date, wait=False)
    testit(test27_io, wait = False)
    testit(test28_toh5, wait=False)
    testit(test29_plotxy, wait=False)
    testit(test30_row, wait=False)
    testit(test31_rows, wait=False)
#    testit(test32_table, wait=False)
#    testit(test33_table2, wait=False)
    testit(test34_issquare, wait=False)
    testit(test35_sort, wait=False)
    testit(test36_addID, wait=False)
    testit(test37_rename, wait=False)
    testit(test38_transpose, wait=False)
    testit(test39_uniques, wait=False)
    testit(test40_zip, wait=False)
#    testit(test41__intersect, wait=False)
    testit(test42__contains, wait=False)
    testit(test43__collect, wait=False)
    testit(test44__collectrc, wait=False)
    testit(test45__map, wait=False)
    testit(test46__subtable, wait=False)

if __name__ == '__main__':
    test_all()
    #test00_create_add()
    #test46__subtable()
    
    print("*** ALL DONE ***")
