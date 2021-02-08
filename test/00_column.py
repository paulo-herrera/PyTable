import sys
sys.path.append(r"Z:\Documents\ProjectSWM\tmp4_pytable\PyTable\tmp\Lib\site-packages")

import unittest
from tbl.column import Column

class TestColumn(unittest.TestCase):

    def setUp(self):
        self.column = Column(name = "pressure", pos = 0)
        self.column.addData(data = [0.1, 0.5, 0.25, 0.33, 0.45, 0.96])
        t = self.column.type 
        self.assertEqual(t,"f")
    
    def test_addData(self):
        self.column.addData(data = [0.1, 0.5, 0.25, 0.33, 0.45, 0.96])
        t = self.column.type 
        self.assertEqual(t,"f")
        
        try:
            self.column.addData(data = [0, 1, 2, 3])
        except:
            self.assertTrue(True)
    
    def test_addData_empty(self):
        c = Column("col", pos=0)
        c.addData(data=[], ctype=0.1)
        t = self.column.type 
        self.assertEqual(t,"f")
        
        c.addData([0.27, 0.41, 0.33])
        self.assertTrue(True)
        
        try: # should fail
            self.column.addData(data = [0, 1, 2, 3])
        except:
            self.assertTrue(True)
        
    def test_append(self):
        c = Column("col", pos=0)
        c.addData(data=[], ctype=0.1)
        
    # def test_convert(self):
        # c = Column("test", 0).addData(["0.0", "1.0", "2.0", "3.0"])
        # self.assertEqual(c.type, "s")
        
        # try: 
            # c.convert("s", "f")
            # self.assertTrue(False)
        # except:
            # self.assertTrue(True)
        
        # c.convert("s", "f")
        # self.assertEqual(c.type, "f")
        
        # c.convert("f", "s")
        # self.assertEqual(c.type, "s")
    
    # def test_convertToString(self):
        # c = Column("test", 0).addData([0.0, 1.0, 2.0, 3.0])
        # c.convertToString(fmt="%4.2f")
        # a = c.data[0]
        # self.assertEqual(a, "0.00")
    
        # c = Column("test", 0).addData([0.0, 1.0, 2.0, 3.0])
        # c.convertToString()
        # a = c.data[0]
        # self.assertTrue( isinstance(a,str) )
    
    # def test_convertFromString(self):
        # c = Column("test", 0).addData(["0.0", "1.0", "2.0", "3.0"])
        # c.convertFromString(fmt="%4.2f")
        # a = c.data[0]
        # self.assertTrue( isinstance(a,float) )
        # self.assertEqual(a, 0.0)
    
        # c = Column("test", 0).addData(["0", "1", "2", "3"])
        # c.convertFromString()
        # a = c.data[0]
        # self.assertTrue( isinstance(a,int) )
        # self.assertEqual(c.type, "i")
        
    # def test_indexOf(self):
        # idx = self.column.indexOf(filter = lambda i, v: v == 0.25  )
        # self.assertEqual(1, len(idx))
        # self.assertEqual(idx[0], 2)
        
    # def test_sample(self):
        # c = Column(name = "test", pos = 1)
        # d = [i for i in range(10000)]
        # c.addData(d)
       
        # cc = c.sample(each = 20)
        # print("len(c): %d"%(len(c)))
        # print("len(cc): %d"%(len(cc)))
        
    # def test_appendElement(self):
        # self.column.appendElement(1.25)
        # self.assertEqual(self.column[-1], 1.25)

    # def test_collect(self):
        # vals = self.column.collect(filter = lambda i, v: v < 0.34)
        # self.assertEqual(len(vals), 3)

    # def test_remove(self):
        # self.column.remove(filter = lambda i, v: v < 0.34)
        # self.assertEqual(len(self.column), 3)
        # self.assertEqual(self.column[0], 0.5)

    # def test_map(self):
        # c = self.column.clone()
        # c.map(func = lambda i, x: 2.0*x)
        # self.assertEqual(c[0], 0.2)
        # self.assertEqual(c[1], 1.0)

#    def test_reduce(self):
#        maxval = self.column.reduce(func = lambda i, v, result: result if result > v else v, result = -1.0)
#        self.assertEqual(maxval, 0.96)

if __name__ == '__main__':
    unittest.main()
