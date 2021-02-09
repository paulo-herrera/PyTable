from tbl.ttypes import isTypeStr, getTypeConverter, getType, isDateStr, getTypeStr, getH5TypeStr
from datetime import datetime 

__TOL = 1.0e-16

def test00_isTypeStr():
    it = isTypeStr("i")
    assert it, it
    
    it = isTypeStr("f")
    assert it, it
    
    it = isTypeStr("d")
    assert it, it
    
    it = isTypeStr("s")
    assert it, it
    
    it = isTypeStr("is")
    assert not it, it
    
    it = isTypeStr("g")
    assert not it, it
    
    it = isTypeStr("m")
    assert not it, it
    
def test01_getTypeConverter():
    # from string
    c, fmt = getTypeConverter("s", "i")
    v = c("0")
    assert v == 0, v
    assert not fmt, fmt
     
    c, fmt = getTypeConverter("s", "f")
    v = c("2.0")
    assert abs(v - 2.0) < __TOL, v
    assert not fmt
    
    c, fmt = getTypeConverter("s", "d", fmt = "%d/%m/%Y %H:%M:%S")
    v = c("02/05/2000 13:00:00")
    d = datetime(2000,5,2,13,00,00,00)
    assert v == d, str(v)
    assert fmt == "%d/%m/%Y %H:%M:%S"
    
    # to string
    c, fmt = getTypeConverter("i", "s")
    v = c(2)
    assert v == "2", str(v)
    
    c, fmt = getTypeConverter("f", "s", "%4.2f")
    v = c(2.0)
    assert v == "2.00"
    
    c, fmt = getTypeConverter("d", "s", "%d/%m/%Y %H:%M:%S")
    v = c(d)
    assert v == "02/05/2000 13:00:00"
    assert fmt == "%d/%m/%Y %H:%M:%S"
    
def test02_getType():
    ft = getType(1.0)
    it = getType(1)
    st = getType("hello")
    d = datetime.strptime("02/06/1998", "%d/%m/%Y")
    dt = getType(d)
    
    assert ft == "f", ft
    assert it == "i", it
    assert st == "s", st
    assert dt == "d", dt
    
def test03_isDateStr():
    a = isDateStr("02/06/1998", "%d/%m/%Y")
    b = isDateStr("02.06.1998", "%d.%m.%Y")
    c = isDateStr("12.31.2000", "%m.%d.%Y")
    
    assert a
    assert b
    assert c
  
def test04_getTypeStr():
    ft = getTypeStr("1.0")
    assert ft == "f", ft
    
    it = getTypeStr("1") 
    assert it == "i", it
    
    st = getTypeStr("hello")
    assert st == "s", st
    
    dt = getTypeStr("02/06/1998", "%d/%m/%Y")
    assert dt == "d", dt
    
    dt = getTypeStr("01/01/1991 00:00:00", "%d/%m/%Y %H:%M:%S")
    assert dt == "d", dt

def test05_getH5TypeStr():
    ft = getH5TypeStr("i")
    assert ft == "i8", ft
    
    it = getH5TypeStr("f") 
    assert it == "f8", it
    
    dt = getH5TypeStr("d")
    assert dt == "S20", dt
    
    st = getH5TypeStr("s")
    assert st == "S100", st
    
def testit(t):
    try:
        t()
        print("PASSED>> " + t.__name__)
    except:
        print("FAILED>> " + t.__name__)   
   
if __name__ == '__main__':
    testit(test00_isTypeStr) 
    testit(test01_getTypeConverter)
    testit(test02_getType)
    testit(test03_isDateStr)
    testit(test04_getTypeStr)
    testit(test05_getH5TypeStr)