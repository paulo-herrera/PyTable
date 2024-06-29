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


""" Module to check for installed packages """

try:
    import numpy as np
    NUMPY_ON = True
except:
    NUMPY_ON = False   
    
try:
    import matplotlib.pyplot as plt
    PLT_ON = True
except:
    PLT_ON = False
    
try:
    import h5py
    H5_ON = True
except:
    H5_ON = False

def report():
    print("NUMPY installed: \t\t %b",      NUMPY_ON)
    print("MATPLOTLIB installed: \t\t %b", PLT_ON)
    print("H5PY installed: \t\t %b",       H5_ON)
