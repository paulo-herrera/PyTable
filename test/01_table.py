from tbl.table import Table
from tbl.column import Column
from tbl.helpers import timeit

def test00_create_addColumnumn():
    t = Table("table0").addColumn("time", [0.0, 0.1, 0.2, 0.3])
    t.addColumn("pressure", [0.1, 1.2, 0.3, 2.5, 0.8])
    print(t)

def test01_setname():
    t = Table("table0").addColumn("time", [0.0, 0.0]).addColumn("pressure", [0.0, 0.0])
    t.setName("ttable1")
    assert t.name == "ttable1" 

def test02_all():
    t = Table("table0").addColumn("time", [0.0, 0.0, 0.0]).addColumn("pressure", [0.0, 1.2, 0.0])
    all = t.all()
    assert len(all) == 2
    assert all[1] == 1
    
def test03_names():
    t = Table("table0").addColumn("time", [0.0, 0.0, 0.3]).addColumn("pressure", [0.0, 1.2, 0.0])
    ids = t.names() 
    assert len(ids) == 2
    assert ids[1] == "pressure"
    
def test04_index():
    t = Table("table0")
    t.addColumn("time", [0.0, 0.1, 0.2, 0.3])
    t.addColumn("pressure", [0.1, 1.2, 0.3, 2.5, 0.8])

    id0 = t.index(["time"])
    assert len(id0) == 1
    assert id0[0] == 0
    
    id1 = t.index(["pressure"])
    assert id1[0] == 1

def test05_hascolumn():
    t = Table("table0").addColumn("t", [0.0, 0.1]).addColumn("p", [0.1, 1.2])
    a = t.hasColumn("t")
    assert a
    
    a = t.hasColumn("q")
    assert not a
    
    a = t.hasColumn(1)
    assert a
    
    a = t.hasColumn(2)
    assert not a

def test06_addColumnumn():
    t = Table("table0")
    t.addColumn("t", [0.0, 0.1])
    t.addColumn("p")
    c = Column("col").addData([1,2,3])
    t.addColumn(c.name, c)
    
    try:
        t.addColumn("t", allowRepetition=False)
        assert False
    except:
        assert True
        
    t.addColumn(data = [1, 2, 3]) # no name
    c = t[3]
    c.name == "col03", c.name
    
    
def test07_len():
    t = Table("table0").addColumn("time", [0.0, 0.0, 0.0, 0.3]).addColumn("pressure", [0.0, 1.2, 0.0, 0.0, 0.0])
    assert len(t) == 2

def test00_iter():
    t = Table("table0").addColumn("time", [0.0, 0.0]).addColumn("pressure", [0.0, 1.2])
    for c in t: 
        #print(c)
        pass

def test00_item():
    t = Table("table0").addColumn("time", [0.0, 0.0]).addColumn("pressure", [0.0, 1.2])
    c = t[0]
    assert c.name == "time"
    
    c = t["time"]
    assert c.name == "time"
    
    c = t[5]
    assert not c

def test00_at():
    t = Table("table0").addColumn("c1", [0.0, 0.0]).addColumn("c2", [0.0, 1.2]).addColumn("c3", [1, 2])
    c = t.at([0,2])
    assert c[0].name == "c1"
    assert c[1].name == "c3"
 
def test00_pop():
    t = Table("table0").addColumn("c1", [0.0, 0.0]).addColumn("c2", [0.0, 1.2]).addColumn("c3", [1, 2])
    assert len(t) == 3
    
    c = t.pop("c2")
    assert c.name == "c2"
    assert len(t) == 2
    
    c = t.pop(0)
    assert len(t) == 1
    assert c.name == "c1"
    
def test00_remove():
    t = Table("table0")
    for i in range(25):
        t.addColumn(data=[1, 2, 3, 4, 5])
    assert len(t) == 25
    
    cols = t.remove([1, 5, 10, 14])
    assert len(t) == 21
    #for c in cols: print(c)
    
def test00_select():
    t = Table("table0").addColumn("p1", [0.0, 0.0]).addColumn("t1", [0.0, 1.2]).addColumn("e1", [1, 2])
    t2 = t.select(filter=lambda i, name: i <= 1)
    assert len(t2) == 2
    
    t2 = t.select(filter=lambda i, name: "p" in name)
    assert len(t2) == 1
    assert t[0].name == "p1"

def test00_clone():
    t = Table("table0").addColumn("p1", [0.0, 0.0]).addColumn("t1", [0.0, 1.2]).addColumn("e1", [1, 2])
    t2 = t.clone(shallow=True)
    assert t.name + "(Copy)" == t2.name
    assert len(t2) == len(t)
    
    t2 = t.clone(shallow=False, newName="t2")
    assert t2.name == "t2"
    assert len(t2) == len(t)
    # check deep copy

def test00_append():
    t  = Table("table0").addColumn("p1", [0.0, 1.0]).addColumn("t1", [1, 2]).addColumn("e1", ['a', 'b'])
    t2 = Table("table1").addColumn("p1", [2.0, 3.0]).addColumn("t1", [3, 4]).addColumn("e1", ['c', 'd'])
    assert t.nrows() == 2
    assert t.ncols() == 3
    
    t.append(t2)
    assert t.nrows() == 4
    assert t.ncols() == 3
    
    assert t[2][2] == 'c'
    assert t[1][2] == 3

def test00_ncols_nrows():
    t  = Table("table0").addColumn("p1", [0.0, 1.0]).addColumn("t1", [1, 2, 3, 4]).addColumn("e1", ['a', 'b'])
    assert t.nrows() == 4
    assert t.ncols() == 3

def test00_what():
    t  = Table("table0").addColumn("p1", [0.0, 1.0]).addColumn("t1", [1, 2, 3, 4]).addColumn("e1", ['a', 'b'])
    t.what()

def test00_print():
    t  = Table("table0").addColumn("p1", [0.0, 1.0]).addColumn("t1", [1, 2, 3, 4]).addColumn("e1", ['a', 'b'])
    print("DEFAULT FORMATTING")
    t.print()
    
    print("FORMATTED")
    t.setFormatStr(fmt_int="%04d", fmt_float="%4.2f", fmt_date=None, fmt_str="%10s")
    t.print()

def test00_print_file():
    t  = Table("table0").addColumn("p1", [0.0, 1.0]).addColumn("t1", [1, 2, 3, 4]).addColumn("e1", ['a', 'b'])
    
    t.setFormatStr(fmt_int="%04d", fmt_float="%4.2f", fmt_date=None, fmt_str="%10s")
    dst = open("test_01table_print_file.txt", "w")
    t.print(sep=",", out = dst, verbose = True).close()

def test00_write():
    t  = Table("table0").addColumn("p1", [0.0, 1.0]).addColumn("t1", [1, 2, 3, 4]).addColumn("e1", ['a', 'b'])
    t.write("test_01table_write.txt", verbose = True)

def test00_read():
    src= "./data/dates1.csv"
    t = Table.read(src, sep=",", header=1, verbose=True)
    t.what()
    t.print()

def test00_read_big():
    src= "./data/bigtable.csv"
    t = Table.read(src, header=0, verbose=True)
    #t.what()
    t.print(maxRows=15)

def test00_read_empty_column():
    src= "./data/dates3.csv"
    t = Table.read(src, sep=",", header=1, verbose=True)
    assert len(t) == 4
    t.what()
    #t.print()
    
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("AFTER REMOVING EMPTY COLUMNS")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    t = Table.read(src, sep=",", header=1, verbose=True, removeEmptyColumn=True)
    assert len(t) == 2
    t.what()

def test00_convert():
    t  = Table("table0").addColumn("p1", ["0.0", "1.0"]).addColumn("t1", ["1", "2", "3", "4"]).addColumn("e1", ['a', 'b'])
    t.what()
    
    t.convert(cols=[0, 1], types=["f", "i"])
    t.what()
    t.print(2)
    
    t.setFormatStr("%d","%f","%d/%m/%Y","<<%s>>")
    print(t[2].fmt)
    t.convert(cols=[2], types=["s"])
    t.what()
    t.print(2)

def test00_convert_date():
    t  = Table("table0")
    t.addColumn("d1", ["01.01.1900", "02.01.1900"])
    t.addColumn("d2", ["01/01/1900 00:00:00", "02/01/1900 00:15:00"])
    t.what()
    
    t.setFormatStr("%d","%f","%d.%m.%Y","%s")
    t.convert([0], ["d"])
    t.what()
    t.print(2)
    
# def test_iter(self):
    # for c in self.table:
        # print("Col: %s  Pos: %d"%(c.name, c.pos))
        # pass
    # self.assertTrue(True)

# def test_io(self):
    # print(self.table)
    # #self.table.summary()
    # #self.table.display()
    # #self.table.display(writeTitle = True, out = sys.stdout, sep = ",", columnWidth = 8, format = True)
    # self.assertTrue(0==0)

# def test_convert(self):
    # t = Table("t0")
    # t.addColumn("time", ["0.0", "0.1", "0.2", "0.3"])
    # t.addColumn("pressure", ["0.1", "1.2", "0.3", "2.5", "0.8"])
    # t.convert(["f", "f"])
    # self.assertTrue(True)
    
# def test_write_read(self):
    # filename = "test.csv"
    # self.table.write(dst=filename, sep=",", verbose=True, fmt_date="%d/%m/%Y", fmt_float="%6.2f")
    # t2 = Table.read(src=filename, verbose=True)
    # t2.summary()
    # #t2.display()
    # self.assertEqual(t2[0].type, "s")
    # self.assertEqual(len(t2), 2)
    
    # t2 = Table.read(src=filename, convert=True, verbose=True)
    # t2.summary()
    # self.assertEqual(t2[0].type, "f")
    # self.assertEqual(t2[1].type, "f")
    # self.assertEqual(len(t2), 2)

# def test_plotxy(self):
    # t = Table("plot")
    # t.addColumn("x", [1, 2, 3])
    
    # p = t.plotxy([0], [0])
    # #p.show()
    
    # self.assertTrue(0==0)
   
def testit(t):
    #try:
        #timeit(t, source=False)
        t()
        print("PASSED>> " + t.__name__)
    #except:
    #    print("FAILED>> " + t.__name__)  
        
if __name__ == '__main__':
    testit(test00_create_addColumnumn)
    testit(test01_setname)
    testit(test02_all)
    testit(test03_names)
    testit(test04_index)
    testit(test05_hascolumn)
    testit(test06_addColumnumn)
    testit(test07_len)
    testit(test00_iter)
    testit(test00_item)
    testit(test00_at)
    testit(test00_pop)
    testit(test00_remove)
    testit(test00_select)
    testit(test00_clone)
    testit(test00_append)
    testit(test00_ncols_nrows)
    #testit(test00_what)
    #testit(test00_print)
    #testit(test00_print_file)
    #testit(test00_write)
    #testit(test00_read)
    #testit(test00_read_big)
    #testit(test00_read_empty_column)
    testit(test00_convert)
    testit(test00_convert_date)
    
    print("*** ALL DONE ***")