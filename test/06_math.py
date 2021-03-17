from tbl.math import moving_average #, moving_average_fast
from tbl.column import Column

import numpy as np
import math

def test00_moving_average():
    c = Column("floats").addData([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
    b = moving_average(c, k = 1)
    b.print()
    assert math.isnan(b.data[0])
    assert math.isnan(b.data[9])
    assert int(b.data[1]) == 1
    
    ca = list(np.random.randn(200))
    c = Column("rand").addData(ca)
    b = moving_average(c, k = 1, printeach=10)
    
def testit(t, wait = False):
    #try:
        #timeit(t, source=False)
        t()
        print("PASSED>> " + t.__name__)
        #if wait: input("ENTER...")
    #except:
    #    print("FAILED>> " + t.__name__)  
    
    
if __name__ == '__main__':
    testit(test00_moving_average)