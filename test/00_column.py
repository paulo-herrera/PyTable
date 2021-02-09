from tbl.column import Column

def test00_create():
    col = Column(name = "pressure")
    col.addData(data = [0.1, 0.5, 0.25, 0.33, 0.45, 0.96])
    assert col.type == "f"
    assert len(col) == 6
           
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
    
    c.convert("s", "f")
    assert c.type == "f"
    
    c.convert("f", "s", "%4.2f")
    assert c.type == "s"
    c[1] == "2.00"
    
    c = Column("ints").addData([0.0, 1.0, 2.0, 3.0])
    c.convert("f", "i")

def test05_convert_dates():
    c = Column("test").addData(["01/05/1977 00:00:00", "01/07/1977 00:15:20"]) 
    c.type = "s"
    
    c.convert("s", "d", fmt = "%d/%m/%Y %H:%M:%S")
    assert c.type == "d"
    
    c.convert("d", "s", fmt = "%d.%m.%Y %H:%M:%S")
    assert c.type == "s"
    assert c[0] == "01.05.1977 00:00:00" 
    
    try:
        c.convert("d", "s")
        assert False
    except:
        pass
        
def test06_index():
    c = Column("index").addData([0.0, 2.0, 1.0, 3.0])
    idx = c.index(filter = lambda i, v: v < 2.0 )
    assert len(idx) == 2
    assert idx[1] == 2
 

def test07_collect():
    c = Column("collect").addData([2.0, 0.0, 1.0, 3.0])
    vals = c.collect(filter = lambda i, v: v < 0.45)
    assert len(vals) == 1
    assert vals[0] == 0.0
        
def test08_sample():
    c = Column("sample")
    n = 10000
    s = 20
    d = [i for i in range(n)]
    c.addData(d)
       
    cc = c.column(filter = lambda i, x: i % s == 0)
    assert len(cc) == int(n/s)
    assert cc.name == "sample(sample)"
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

def test13_write():
    c = Column("write").addData([1,  4, 2, 3])
    c.write(sep=",")
    
    c.write()
    
    c.write(writeName = True)

def test14_write_fmt():
    c = Column("write").addData([1.00, 4.03, 2.0, 3.])
    c.write(sep=",")
    
    c.write()
    
    c.write(writeName = True, fmt = "%4.2f")

def test15_write_file():  
    c = Column("write").addData([1.00, 4.03, 2.0, 3.])  
    w = open("00_column_test14.txt", "w")
    c.write(sep="\t", writeName=True, out = w)
    w.close()
    
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
    testit(test06_index)
    testit(test07_collect)
    testit(test08_sample)
    testit(test09_remove)
    testit(test10_apply)
    testit(test11_map)
    testit(test12_reduce)
    #testit(test13_write)
    #testit(test14_write_fmt)
    #testit(test15_write_file)
    print("*** ALL DONE ***")
