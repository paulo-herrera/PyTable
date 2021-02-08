import sys
sys.path.append(r"Z:\Documents\ProjectSWM\tmp4_pytable\PyTable\tmp\Lib\site-packages")

import unittest
from tbl.table import Table
from tbl.column import Column

# Method	Equivalent to
# .assertEqual(a, b)	a == b
# .assertTrue(x)	bool(x) is True
# .assertFalse(x)	bool(x) is False
# .assertIs(a, b)	a is b
# .assertIsNone(x)	x is None
# .assertIn(a, b)	a in b
# .assertIsInstance(a, b)	isinstance(a, b)

class TestTable(unittest.TestCase):

    def setUp(self):
        t = Table("table0")
        t.addCol("time", [0.0, 0.1, 0.2, 0.3])
        t.addCol("pressure", [0.1, 1.2, 0.3, 2.5, 0.8])
        self.table = t

    def test_ncols(self):
        pos = self.table.ncols(["time", "pressure"])
        self.assertEqual(pos[0], 0)
        self.assertEqual(pos[1], 1)   

        pos = self.table.ncols([0])
        self.assertEqual(pos[0], 0)
         
    def test_len(self):
        nc = len(self.table)
        self.assertEqual(nc, 2)
    
    def test_all_names(self):
        a = self.table.all()
        self.assertEqual(a[1], 1)
        
        b = self.table.names()
        self.assertEqual(b[0], "time")
        
    def test_hasColumn(self):
        a = self.table.hasColumn("time")
        b = self.table.hasColumn(1)
        c = self.table.hasColumn(4)
        self.assertTrue(a)
        self.assertTrue(b)
        self.assertFalse(c)
        
    def test_addCol(self):
        try: # this should fail, already in table
            self.table.addCol("time", [0, 1, 1, 1, 0])
        except:
            self.assertTrue(0==0)
        
        self.table.addCol("time", [0, 1, 1, 1, 0], allowRepetition = True)
        self.assertTrue(0==0)
     
    def test_appendCol(self):
        c = Column("temp1", [0, 1, 2, 3])
        self.table._appendCol(c)
    
    def test_removeCol(self):
        self.table.addCol("temp1", [0, 0, 0])
        self.table.removeColByName("temp1")
        self.assertTrue(0==0)
        
        self.table.addCol("temp1", [0, 0, 0])
        self.table.removeColByPos(2)
        self.assertTrue(0==0)
        #self.table.summary()
    
    def test_removeCols(self):
        self.table.addCol("t1", [0, 0, 0])
        self.table.addCol("t2", [0, 0, 0])
        self.table.addCol("t3", [0, 0, 0])
        #self.table.summary()
        
        self.table.removeCols(["t1", "t2"])
        #self.table.summary()
        self.assertTrue(0==0)
        
        self.table.removeCols([2])
        #self.table.summary()
        self.assertTrue(0==0)
    
    def test_getCol(self):
        c = self.table.getColByName("time")
        self.assertEqual(c.pos, 0)
        
        c = self.table.getColByPosition(1)
        self.assertEqual(c.name, "pressure")
        
        # Operator, __getitem__
        c = self.table["time"]
        self.assertEqual(c.pos, 0)
        c = self.table[1]
        self.assertEqual(c.name, "pressure")
        
        # getCols
        self.table.addCol("t1", [0, 0, 0])
        self.table.addCol("t2", [0, 0, 0])
        self.table.addCol("t3", [0, 0, 0])
        cols = self.table.getCols(["t1", "t2", "t3"])
        self.assertEqual(len(cols), 3)
        
        cols = self.table.getCols([0, 1])
        self.assertEqual(len(cols), 2)
    
    def test_select(self):
        print("test_select")
        t2 = self.table.select(filter=lambda i, name: i == 0)
        self.assertEqual(len(t2), 1)
        
        self.table.addCol("c1", [0, 0, 0])
        self.table.addCol("c2", [0, 0, 0])
        self.table.addCol("c3", [0, 0, 0])
        t2 = self.table.select(filter=lambda i, name: "c" in name)
        t2.summary()
        print(t2.desc)
        self.assertEqual(len(t2), 3)

    def test_clone(self):
        self.table.addCol("c1", [0.0, 1.0, 2.0]) 
        #print(self.table)
        #self.table.display()
        
        t2 = self.table.clone(shallow=True)
        t2.name = t2.name + "_Shallow"
        t2.getColByName("c1").data[0] = 0.1
        #print(t2)
        #t2.display()
        
        #print(self.table)
        #self.table.display()
        
        t2 = self.table.clone(shallow=False)
        t2.name = t2.name + "_Deep"
        t2.getColByName("c1").data[1] = 1.1
        #print(t2)
        #t2.display()
        
        #print(self.table)
        #self.table.display()
        
        self.assertTrue(0==0)
        
    def test_append(self):
        #print(self.table)
        #self.table.display()
        
        t = Table("t2")
        t.addCol("time2", [0, 0.1, 0.2, 0.3])
        t.addCol("pressure2", [0.1, 1.2, 0.3, 2.5, 0.8])
        self.table.append(t)
        #print( str(self.table) + " (appended)")
        #self.table.display()
        
        t = Table("t3")
        t.addCol("time3", [0, 0.1, 0.2, 0.3])
        t.addCol("pressure3", [0.1, 1.2, 0.3, 2.5, 0.8])
        t2 = self.table.clone().setName("Merged table").append(t)
        #print(t2)
        #t2.display()
        
        self.assertTrue(0==0)
    
    def test_iter(self):
        for c in self.table:
            print("Col: %s  Pos: %d"%(c.name, c.pos))
            pass
        self.assertTrue(True)
    
    def test_io(self):
        print(self.table)
        #self.table.summary()
        #self.table.display()
        #self.table.display(writeTitle = True, out = sys.stdout, sep = ",", columnWidth = 8, format = True)
        self.assertTrue(0==0)
    
    def test_convert(self):
        t = Table("t0")
        t.addCol("time", ["0.0", "0.1", "0.2", "0.3"])
        t.addCol("pressure", ["0.1", "1.2", "0.3", "2.5", "0.8"])
        t.convert(["f", "f"])
        self.assertTrue(True)
        
    def test_write_read(self):
        filename = "test.csv"
        self.table.write(dst=filename, sep=",", verbose=True, fmt_date="%d/%m/%Y", fmt_float="%6.2f")
        t2 = Table.read(src=filename, verbose=True)
        t2.summary()
        #t2.display()
        self.assertEqual(t2[0].type, "s")
        self.assertEqual(len(t2), 2)
        
        t2 = Table.read(src=filename, convert=True, verbose=True)
        t2.summary()
        self.assertEqual(t2[0].type, "f")
        self.assertEqual(t2[1].type, "f")
        self.assertEqual(len(t2), 2)

    def test_plotxy(self):
        t = Table("plot")
        t.addCol("x", [1, 2, 3])
        
        p = t.plotxy([0], [0])
        #p.show()
        
        self.assertTrue(0==0)
    
def touchit():
    r = [(",", "."), (";", ",")]
    src = "./test/data/touchme.txt"
    Table.touchit(src, r, dst="touchme_new.txt")
    
    
if __name__ == '__main__':
    touchit()
    unittest.main()
    print("*** ALL DONE ***")