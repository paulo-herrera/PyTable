ROOT_DIR = r"Z:/Documents/ProjectSWM/tmp4_pytable/PyTable"

import sys
sys.path.append(ROOT_DIR + r"/tmp/Lib/site-packages")

from tbl.table import Table

def t1(t):
    p = t.plotxy([0], [0,1], fmt=["md", "b+"])
    p = t.plotxy([0], [2], fmt=["go"], newfig=False)
    p.show()

def t2(t):
    p2 = t.plotxy([0], t.all()[1:])
    p2.show()

def t3(t):
    p3 = t.plotxy(["x"], ["x^2"])
    p3.show()

def t4():
    t = Table.read(ROOT_DIR + "/test/data/dates2.csv")
    t.summary()
    
    p = t.plotxy([0], [1], labels=[None, "T[°C]"])
    #p.show()
    
    p = t.plotts([0], [1], labels=[None, "T[°C]"])
    p.show()

def t5():
    #28/11/1991 00:00:00,638.08
    t = Table.read(ROOT_DIR + "/test/data/borehole_gwl.csv", fmt_date="%d/%m/%Y %H:%M:%S", convert=True, header=0)
    t.summary()
   
    #p = t.plotxy([0], [1], labels=[None, "T[°C]"])
    #p = t.plotts([0], [1], labels=[None, "T[°C]"])
    #p.show()
    
if __name__ == "__main__":
    t = Table("plot")
    t.addCol("x", [1, 2, 3])
    t.addCol("x^2", [1, 4, 9])
    t.addCol("x^3", [1, 16, 81])
    
    #t1(t)
    #t2(t)
    #t3(t)
    #t4()
    t5()
    
    print("*** ALL DONE ***")