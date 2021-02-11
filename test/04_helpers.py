from tbl.helpers import split_line, is_iterable, walker, break_date, touchit, read_tab_file, timeit
import os

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

def test02_walker():
    src = "./data" # has to be run from test directory
    
    # Full path
    print(">>> FULL PATH <<<")
    ffiles = walker(src, verbose= True)
    assert len(ffiles) == 14, len(ffiles)
    #for f in ffiles: print(f)
    
    # Relative path
    print(">>> RELATIVE PATH <<<")
    ffiles = walker(src, verbose= True, lfiles = [], absPath = False)
    assert len(ffiles) == 14, len(ffiles)
    #for f in ffiles: print(f)
    
    # Filter
    print(">>> FILTER <<<")
    ffiles = walker(src, ffilter = lambda x: x.endswith(".txt"), verbose= True, lfiles = [])
    assert len(ffiles) == 7, len(ffiles)
    #for f in ffiles: print(f)
    
    # some test to see how difficult is to generate a list of file names
    import os
    ids = [os.path.basename(f) for f in ffiles]
    #for i in ids: print(i)

def test03_break_date():
    d, m, y, h, mm, s = break_date('01/05/1974 00:02:45')
    assert (d==1) and (m==5) and (y==1974)
    assert (h==0) and (mm==2) and (s==45)
    
    d, m, y, h, mm, s = break_date('01.05.1974-00_02_45', dsep=".", hsep="_",sep="-")
    assert (d==1) and (m==5) and (y==1974)
    assert (h==0) and (mm==2) and (s==45)
    
    d, m, y, h, mm, s = break_date('01/05/1974')
    assert (d==1) and (m==5) and (y==1974)
    assert (h==0) and (mm==0) and (s==0)

def test04_touchit():
    r = [(",", "."), (";", ",")]
    src = "data/touchit.txt"
    touchit(src, replace = r, dst = None, verbose = True, test = True, debug=True)
    
    touchit(src, replace = r, dst = "./test_helpers_touched.txt", verbose = True, test = False, debug=False)

def test05_read_tab_file():
    import os
    
    src = "data/dates1.csv"
   
    vals = read_tab_file(src, sep=",", strip = True, verbose=True)
    assert len(vals) == 4
    assert len(vals[0]) == 2

    src = "data/dates3.csv"
    vals = read_tab_file(src, sep=",", strip = True, verbose=True)
    assert len(vals) == 4
    assert len(vals[0]) == 4
    for v in vals[1]: print (v)

def test06_read_tab_file2():
    src = "./data/dates1.csv"
    mbytes = os.path.getsize(src) / 1024 / 1024
    f = lambda: read_tab_file(src, sep=",", strip = True, verbose=True)
    t = timeit(f, source = True)
    
    print("File size: %g [MB]   Elapsed time: %g [sec]"%(mbytes, t))
    print("Reading speed: %g [MB/sec]"%(mbytes/t))
    
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    src = "./data/bigtable.csv"
    mbytes = os.path.getsize(src) / 1024 / 1024
    f = lambda: read_tab_file(src, sep=",", strip = True, verbose=True)
    t = timeit(f, source = True)
    
    print("File size: %g [MB]   Elapsed time: %g [sec]"%(mbytes, t))
    print("Reading speed: %g [MB/sec]"%(mbytes/t))
    
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    src = "./data/biggertable.dat"
    mbytes = os.path.getsize(src) / 1024 / 1024
    f = lambda: read_tab_file(src, sep=";", strip = True, verbose=True)
    t = timeit(f, source = True)
    
    print("File size: %g [MB]   Elapsed time: %g [sec]"%(mbytes, t))
    print("Reading speed: %g [MB/sec]"%(mbytes/t))
    
def testit(t):
    #try:
        t()
        print("PASSED>> " + t.__name__)
    #except:
    #    print("FAILED>> " + t.__name__)   
   
if __name__ == '__main__':
    testit(test00_split_line) 
    testit(test01_is_iterable)
    testit(test02_walker)
    testit(test03_break_date)
    testit(test04_touchit)
    testit(test05_read_tab_file)
    testit(test06_read_tab_file2)