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