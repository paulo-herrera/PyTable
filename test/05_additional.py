from tbl.table import Table

def test0_convert():
    t = Table("t0")
    t.addCol("time", ["0.0", "0.1", "0.2", "0.3"])
    t.addCol("pressure", ["0.1", "1.2", "0.3", "2.5", "0.8"])
    t.addCol("pressure2", ["0.1", "1.2", "0.3", "2.5", "0.8"])
    t.addCol("dates", ["01/01/1973", "01/03/2000", "01/06/2010", "01/12/1998", "11/09/2001"])

    t.display()
    
    t.summary()
    t.convert(t.all(), ["f", "f", "f", "d"], fmt_date = "%d/%m/%Y")
    t.summary()
    
    t.display()

def test1_h5():
    fpath = "test5_h5.h5"
    
    t = Table("t0")
    t.addCol("time", [0.0, 0.1, 0.2, 0.3])
    t.addCol("pressure", [1, 2, 3, 4, 5])
    t.addCol("pressure2", ["0.1", "1.2", "0.3", "2.5", "0.8"])
    t.addCol("dates", ["01/01/1973", "01/03/2000", "01/06/2010", "01/12/1998", "11/09/2001"])
    t.summary()
     
    t.convert([3], ["d"], fmt_date = "%d/%m/%Y")
    
    t.summary()
    t.display()
    t.toH5("test5_h5.h5", root = "t0")
    
    t.toH5("test5_h5.h5", root = "t1", append = True)
    
if __name__ == "__main__":
    #test0_convert()
    test1_h5()