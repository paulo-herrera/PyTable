from tbl.helpers import split_line, is_iterable

def test00_split_line():
    line = "  hello, world!"
    v = split_line(line, ",")
    assert len(v) == 2
    assert v[0] == "hello"
    assert v[1] == " world!"
    
    v = split_line(line, ",", strip = True)
    assert len(v) == 2
    assert v[0] == "hello"
    assert v[1] == "world!"
 
def test01_is_iterable():
    b = is_iterable([1, 2, 3])
    assert b, b
    
    b = is_iterable((1, 2, 3))
    assert b, b
    
    b = is_iterable({0:1, 1:2, 2:3})
    assert b, b
    
    b = is_iterable("hello")
    assert not b, b
    
def testit(t):
    try:
        t()
        print("PASSED>> " + t.__name__)
    except:
        print("FAILED>> " + t.__name__)   
   
if __name__ == '__main__':
    testit(test00_split_line) 
    testit(test01_is_iterable)