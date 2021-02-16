__docformat__ = "google"

""" Provides some functions to plot data stored in Tables. """
from .helpers import is_iterable
from .required import PLT_ON

def plotxy(t, xcols, ycols, labels=["x", "y"], fmt=None, legend=True, newfig=True):
    """ Plots ycols vs xcols. 
        Args:
            t: Table.
            xcols: list of columns, e.g. [0,1,2] or ["col1", "col2"], that specifies list to be used as x-data.
                   If len(xcols) == 1, then all ycols are plotted against a single column. 
                   If len(xcols) > 1, then it must satisfy len(xcols) == len(ycols).
            ycols: list of columns, e.g. [0,1,2] or ["col1", "col2"], that specifies list to be used as y-data.
            fmt: list with strings that specify format to be used for lines and symbols.
                 If len(fmt) == 1, then use the same format for all series.
                 If len(fmt) > 1, then it must satisfy len(fmt) == len(ycols)
            labels: labels to be used as titles for axes. It should satisfy len(labels) == 2.
                    DEFAULT = ["x","y"].
            legend: if True include legend.
            newfig: If True, creates a new figure.
            
        
        Returns:
            Reference to matplotlib.pyplot that can be used to:
            - show figure, plt.show()
            - save figure, plt.savefig(), etc.
    """
    if not PLT_ON: 
        print("Missing matplotlib.pyplot")
        return
    else:
        import matplotlib.pyplot as plt
            
    assert is_iterable(xcols) and is_iterable(ycols)
    assert len(labels) == 2, str(labels)
    
    _ncols = len(ycols)
    
    if len(xcols) == 1:
        xcols = [xcols[0] for i in range(_ncols)]
    elif len(xcols) == len(ycols):
        pass
    else:
        assert False, "Number of xcols: %d, does not match number of ycols: %d"%(len(xcols),len(ycols))
        
    if fmt and len(fmt) == 1:
        fmt = [fmt[0] for i in range(_ncols)]
    elif fmt and len(fmt) == _ncols:
        pass
    else:  # use default matplotlib format
        pass
    
    if newfig: plt.figure()
    for i in range(len(xcols)):
        x = t[xcols[i]]
        y = t[ycols[i]]
        assert x.type != "s" and y.type != "s", "Plotting strings is not a good idea"
       
        id = y.name
        if not fmt:
            plt.plot(x.data, y.data, label = id)
        else:
            plt.plot(x.data, y.data, fmt[i], label = id)
    
    plt.xlabel(labels[0], fontsize=16) # TODO: add option to set defaults per package
    plt.ylabel(labels[1], fontsize=16)
    if legend: plt.legend()
    
    return plt
    
    # def plotts(self, xcols, ycols, labels=["x", "y"], newfig=True, fmt=None, legend=True):
        # p = self.plotxy(xcols, ycols, labels, newfig, fmt, legend)
        # p.gcf().autofmt_xdate()
        # return p
    