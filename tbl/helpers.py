__docformat__ = "google"

""" 
    Helper functions used internally by PyTable.
"""

def split_line(l: str, sep: str, strip = False) -> list[str]:
    """ Split a line using sep as separator. 
        Blank space at beginning and end are removed before splitting.
        
        Args:
            l: line as a string.
            sep: separator as a string.
            strip: if True, then additionally strip blank space from substrings.
    """
    l = l.strip().rstrip(sep)
    v = l.split(sep)
    if strip: v = [vv.strip() for vv in v]
    
    return v

def is_iterable(obj):
    """ Returns true if obj is a tuple, list or dictionary so it can be iterated.
    """
    return isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, dict)