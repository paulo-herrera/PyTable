#import sys
#sys.path.append(r"Z:\Documents\ProjectSWM\tmp4_pytable\PyTable\tmp\Lib\site-packages")

import unittest
from tbl.ttypes import Types

from datetime import datetime 

class TestTypes(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_isType(self):
        it = Types.isType("i")
        self.assertTrue(it)
        
        it = Types.isType("f")
        self.assertTrue(it)
        
        it = Types.isType("d")
        self.assertTrue(it)
        
        it = Types.isType("s")
        self.assertTrue(it)
        
        it = Types.isType("is")
        self.assertFalse(it)
        
        it = Types.isType("g")
        self.assertFalse(it)
        
        it = Types.isType("m")
        self.assertFalse(it)
    
    def test_converter(self):
        # from string
        c, fmt = Types.getConverter("s", "i")
        v = c("0")
        self.assertEqual(v, 0)
        self.assertEqual(fmt, None)
        
        c, fmt = Types.getConverter("s", "f")
        v = c("2.0")
        self.assertEqual(v, 2.0)
        self.assertEqual(fmt, Types.FMT_FLOAT)
        
        c, fmt = Types.getConverter("s", "d", fmt = "%d/%m/%Y %H:%M:%S")
        v = c("02/05/2000 13:00:00")
        d = datetime(2000,5,2,13,00,00,00)
        self.assertEqual(v, d)
        self.assertEqual(fmt, "%d/%m/%Y %H:%M:%S")
        
        # to string
        c, fmt = Types.getConverter("i", "s")
        v = c(2)
        self.assertEqual(v, "2")
        
        c, fmt = Types.getConverter("f", "s", "%4.2f")
        v = c(2.0)
        self.assertEqual(v, "2.00")
        
        c, fmt = Types.getConverter("d", "s", "%d/%m/%Y %H:%M:%S")
        v = c(d)
        self.assertEqual(v, "02/05/2000 13:00:00")
        self.assertEqual(fmt, "%d/%m/%Y %H:%M:%S")
    
    def test_getType(self):
        ft = Types.getType(1.0)
        it = Types.getType(1)
        st = Types.getType("hello")
        d = datetime.strptime("02/06/1998", "%d/%m/%Y")
        dt = Types.getType(d)
        
        self.assertEqual(ft, "f")
        self.assertEqual(it, "i")
        self.assertEqual(st, "s")
        self.assertEqual(dt, "d")
    
    def test_isDate(self):
        a = Types.isDate("02/06/1998", "%d/%m/%Y")
        b = Types.isDate("02.06.1998", "%d.%m.%Y")
        c = Types.isDate("12.31.2000", "%m.%d.%Y")
        
        self.assertTrue(a)
        self.assertTrue(b)
        self.assertTrue(c)
        
    def test_getStrType(self):
        ft = Types.getStrType("1.0")
        self.assertEqual(ft, "f")
        
        it = Types.getStrType("1") 
        self.assertEqual(it, "i")
        
        st = Types.getStrType("hello")
        self.assertEqual(st, "s")
        
        dt = Types.getStrType("02/06/1998", "%d/%m/%Y")
        self.assertEqual(dt, "d")
        
        dt = Types.getStrType("01/01/1991 00:00:00", "%d/%m/%Y %H:%M:%S")
        self.assertEqual(dt, "d")
        
if __name__ == '__main__':
    unittest.main()        