from tbl.column import Column

def test00_create():
    col = Column(name = "pressure")
    col.addData(data = [0.1, 0.5, 0.25, 0.33, 0.45, 0.96])
    assert col.type == "f"
    assert len(col) == 6
    
    assert col.tostr, col.tostr
    
def test01_addData():
    col = Column(name = "pressure").addData([0.1, 0.5, 0.25, 0.33, 0.45, 0.96])
    assert col.type == "f"
    try:
        col.addData(data = [0, 1, 2, 3])
    except:
        pass
    
def test02_addData_Empty():
    col = Column("col").addData(data=[], ctype=0.1)
    assert col.type == "f"
    col.addData([0.27, 0.41, 0.33])
    try:
        col.addData(data = [0, 1, 2, 3])
        assert False
    except:
        pass
        
def test03_append():
    c = Column("col")
    c.addData(data=[], ctype=0.1)
    c.append(0.2)
    try:
        c.append(1)
        assert False
    except:
        pass
               
def test04_convert():
    c = Column("test").addData(["0.0", "1.0", "2.0", "3.0"])
    assert c.type == "s"
    
    c.convert("f")
    assert c.type == "f"
    
    c.convert("s", "%4.2f")
    assert c.type == "s"
    c[1] == "2.00"
   
    c = Column("ints").addData([0.0, 1.0, 2.0, 3.0])
    c.convert("i")
    
    c = Column("s").addData(['a', 'b', 'c'])
    c.setFormatStr("<<%s>>").convert("s")
    #c.head(3)
    
    #print("READING DATES")
    c = Column("d").addData(["01/01/1900", "02/01/1900"])
    c.setFormatStr("%d/%m/%Y").convert("d")
    #c.head(2)

def test05_convert_dates():
    c = Column("test").addData(["01/05/1977 00:00:00", "01/07/1977 00:15:20"]) 
    c.type = "s"
    
    c.convert("d", fmt = "%d/%m/%Y %H:%M:%S")
    assert c.type == "d"
    
    c.convert("s", fmt = "%d.%m.%Y %H:%M:%S")
    assert c.type == "s"
    assert c[0] == "01.05.1977 00:00:00" 
    
    try:
        c.convert("s")
        assert False
    except:
        pass
        
def test06a_indexes():
    c = Column("indexes").addData([0.0, 2.0, 1.0, 3.0])
    idx = c.indexes(filter = lambda i, v: v < 2.0 )
    assert len(idx) == 2
    assert idx[1] == 2

def test06b_at():
    c = Column("indexes").addData([0.0, 2.0, 1.0, 3.0])
    idx = [0, 3]
    cc = c.at(idx)
    assert len(cc) == 2
    assert cc.type == "f"
    #cc.print(fmt="%4.2f")
    
def test07_collect():
    c = Column("collect").addData([2.0, 0.0, 1.0, 3.0])
    vals = c.collect(filter = lambda i, v: v < 0.45)
    assert len(vals) == 1
    assert vals[0] == 0.0
        
def test08_select():
    c = Column("select")
    n = 10000
    s = 20
    d = [i for i in range(n)]
    c.addData(d)
       
    cc = c.select(filter = lambda i, x: i % s == 0)
    assert len(cc) == int(n/s)
    assert cc.name == "select(select)"
    #print(cc)
    #print(cc.desc)
 
def test09_remove():
    c = Column("remove").addData([2.0, 0.0, 1.0, 3.0])
    c = c.remove(filter = lambda i, v: v < 1.01)
    assert len(c) == 2
    assert c[0] == 2.0
    
def test10_apply():
    c = Column("apply").addData([1, 2, 3, 4])
    r = c.apply(lambda i, x: x*x)
    assert c.type == "i"
    assert len(r) == 4
    assert r[2] == 9

def test11_map():
    c = Column("map").addData([1, 2, 3, 4])
    c = c.map(lambda i, x: x*x)
    assert c.type == "i"
    assert c[2] == 9
    #print(c.desc)
    
    
def test12_reduce():
    c = Column("apply").addData([1,  4, 2, 3])
    maxval = c.reduce(func = lambda i, v, result: result if result > v else v, result = -1)
    assert maxval == 4

    minval = c.reduce(func = lambda i, v, result: result if result < v else v, result = 100000)
    assert minval == 1
    
    sum = c.reduce(func = lambda i, v, result: result + v, result = 0)
    assert sum == 10

def test13_print():
    c = Column("write").addData([1, 4, 2, 3])
    c.print(sep=",")
    c.print()
    c.print(writeName = True)

def test14_print_fmt():
    c = Column("write").addData([1.00, 4.03, 2.0, 3.])
    c.print(sep=",")
    c.print()
    c.print(writeName = True, fmt = "%4.2f")

def test15_print_file():  
    c = Column("write").addData([1.00, 4.03, 2.0, 3.])  
    w = open("00_column_test14.txt", "w")
    c.print(sep="\t", writeName=True, out = w)
    w.close()

def test16_print_range():  
    c = Column("write").addData([1.00, 4.03, 2.0, 3.])  
    c.print(start = 1, end = 2)

def test17_head_tail():  
    d = [i for i in range(100)]
    c = Column("headtail").addData(d)  
    print(">>>>HEAD<<<<")
    c.head(5)
     
    print(">>>>TAIL<<<<")
    c.tail(5)
    
def test18_np():
    d = [i for i in range(100)]
    i = Column("int").addData(d)
    ia = i.np()
    assert ia.dtype == "int64", ia.dtype
    #print(ia.dtype)
    
    d = [i*1.0 for i in range(100)]
    f = Column("float").addData(d)
    fa = f.np()
    assert fa.dtype == "float64", fa.dtype
    #print(fa.dtype)
    
    d = [str(i) for i in range(100)]
    s = Column("string").addData(d)
    sa = s.np()
    assert sa.dtype == "|S100", sa.dtype
    #print(sa.dtype)

def test19_fmt():
    i = Column("int").addData([0, 1, 2, 3])
    i.setFormatStr("%05d")
    s = i.format(2)
    assert s == "00002", s
    
    f = Column("float").addData([0.0, 1.2, 2.1, 3.0])
    f.setFormatStr("%4.2f")   # investigate later how to add padding with 0s
    s = f.format(2)
    assert s == "2.10", ">" + s + "<"
    
def test20_blank():
    i = Column("s").addData(["","","",""])
    assert i.isBlank()
    
    i = Column("s").addData(["","","","a"])
    assert not i.isBlank()
    
    i = Column("s").addData([1,2,3,4])
    try:
        i.isBlank() 
        assert False
    except:
        pass

def test21_longstr():
    c = Column("i").addData([1,2,3,4])
    c.setAttr("unit", "m/s")
    s = c.longStr()
    print(s)
    
def testit(t):
    #try:
        t()
        print("PASSED>> " + t.__name__)
    #except:
    #    print("FAILED>> " + t.__name__)  
        
if __name__ == '__main__':
    testit(test00_create)
    testit(test01_addData)
    testit(test02_addData_Empty)
    testit(test03_append)
    testit(test04_convert)
    testit(test05_convert_dates)
    testit(test06a_indexes)
    testit(test06b_at)
    testit(test07_collect)
    testit(test08_select)
    testit(test09_remove)
    testit(test10_apply)
    testit(test11_map)
    testit(test12_reduce)
    #testit(test13_print)
    #testit(test14_print_fmt)
    #testit(test15_print_file)
    #testit(test16_print_range)
    #testit(test17_head_tail)
    testit(test18_np)
    testit(test19_fmt)
    testit(test20_blank)
    testit(test21_longstr)
    print("*** ALL DONE ***")
