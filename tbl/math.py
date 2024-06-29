######################################################################################
# MIT License
# 
# Copyright (c) 2010-2024 Paulo A. Herrera
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
######################################################################################
__docformat__ = "google"

""" Provides functions to do math operations on data stored in columns """

from .column import Column

import math
#import numpy as np

# def moving_average_fast(a, k: int):
    # #assert isinstance(c, Column)
    # #assert c.type == "f"
    
    # #a = np.array(c.data)   
    # nel = len(a)
    # b = np.zeros((nel))
    # #print(" >> a: ")       # DEBUG
    # #print(a.shape)         # DEBUG
    # #print(" >> b: ")       # DEBUG
    # #print(b.shape)         # DEBUG
    
    # first = k
    # last = nel - k
    
    # b[0:k] = math.nan
    # b[last:] = math.nan
    
    # temp = np.zeros((2*k+1,1))
    
    # for i in range(first, last):
        # down = i - k
        # up   = i + k
        # temp[:] = a[down:up+1].reshape(-1,1)
        # s = temp.sum()
        # b[i] = s / (up - down + 1)
        # if (i - first)%10000 == 0: print("%d out of %d"%(i - first, last - first))
    
    # #b_ = b.tolist()
    # #print(b_)           # DEBUG
    # #bb = Column("Moving average").addData(b_)
    # return b
    

def moving_average(a, k: int, printeach = 10):
    """ Computes the moving average of values using a window of size 2k+1 around 
        each element of a.
        
        Args:
            a: Column of floating point values.
            k: integer that specifies the half window to compute the moving average.
               For element i computes the mean = mean(a(i-k:i+k)).
            printeach: print some information each printeach values are processed.
                       Useful for debugging when call takes too long.
        
        Returns:
            A Column of the same size as a with first k and last k elements marked
            as NaN and the rest equal to the 2k + 1 moving average around a[i] for each
            element e[i].
            
        NOTE: Pure Python version. Runs reasonably well for small input arrays.
    """
    assert isinstance(a, Column)
    assert a.type == "f"
    
    
    nel = len(a)
    b = [math.nan for i in range(nel)]
    first = k
    last = nel - k
    
    aa = a.data
    for i in range(first, last):
        down = i - k
        up   = i + k
        #print("down: %d   i: %d   up: %d"%(down, i, up))   # DEBUG
        s = 0.0
        for j in range(down, up + 1):
            #print("    >> " + str(j))
            s = s + aa[j]
        #print("    >> sum:" + str(s))                      # DEBUG
        b[i] = s / (up - down + 1)
        if (i - first)%printeach == 0: print("%d out of %d"%(i - first, last - first))
        
    bb = Column("Moving average").addData(b)
    return bb
    
