__docformat__ = "google"

""" Helper functions commonly used when processing data stored in multiple text files.
"""

# TODO: implement some generic wait method, and some debugging, warning, error messages

import os
import sys
import inspect
import time
from datetime import datetime 

def break_date(sdate: str, dsep: str = "/", hsep: str = ":", sep=" "):
    """ Given a date as a string returns 6 integers. 
        
        Args:
            sdate: dates as string.  It assumes a common format, e.g.
                   'day/month/year hour:minute:second', however separators can be 
                   modified by passing different arguments. If hour is not present
                   then it assumes '00:00:00'.
                   If minutes or seconds are missing, then it assume they are 00.
                   It expects that dates are given in international format, with
                   day before month and month before year. Adjust accordingly if 
                   not the case.
            dsep: separator between day, month, year     [OPTIONAL, DEFAULT = /]
            hsep: separator between hour, minute, second [OPTIONAL, DEFAULT = :]
        Returns:
            6 integers: day, month, year, hour, minute, second.
    """
    #add regex to check input later
    sdate = sdate.strip()
    
    p = sdate.split(sep)
    assert len(p) >= 1
    dp = p[0]
    if len(p) == 2:
        hp = p[1]
    else:
        hp = None
        
    ddd = dp.split(dsep)
    assert len(ddd) == 3, str(sdate)
    
    dd = (int(ddd[0]), int(ddd[1]), int(ddd[2]))
    
    if hp:
        hhh = hp.split(hsep)
        if len(hhh) == 3:
            hh = (int(hhh[0]), int(hhh[1]), int(hhh[2]))
        elif len(hhh) == 2:
            #print("ASSUMING Seconds is missing")                  # DEBUG
            hh = (int(hhh[0]), int(hhh[1]), 0) 
        elif len(hhh) == 1:
            #print("ASSUMING Minutes and Seconds are missing")     # DEBUG
            hh = (int(hhh[0]), 0, 0) 
        else:
            assert False
            
    return dd[0], dd[1], dd[2], hh[0], hh[1], hh[2]


def datetime_list(year0, year1, monthly=True, verbose=False):
    """ Returns a list of datetimes between two years.
        Args:
            year0: initial year as int, e.g. 1970.
            year1: final year as int, e.g. 1980.
            monthy: If True, then include the first day of each month.
            verbose: if True, print list of dates.
        Returns:
            List of datetime objects between both years.
    """
    dates = []
    for y in range(year0, year1):
        d = datetime(year = y, month=1, day=1)
        dates.append(d)
        if monthly:
            for m in range(2, 13):
                d = datetime(year = y, month=m, day=1)
                dates.append(d)
    
    if verbose:
        print("Generated dates: ")
        for d in dates: print(str(d))
    
    return dates


def elapsed_time(dates, start, fmt_date = "%d/%m/%Y H:M:S", verbose=False, verbose2=False):
    """ Given a list of dates as datetime, returned a list of elapsed times in days
        since start.
        
        Args:
            dates: list of dates as datetime objects.
            start: string that specifies initial date.
            fmt_date: format that must be used to parse start string. [OPTIONAL]
            verbose: if True, print some additional information.
            verbose2: if True, print more additional information (list of dates and times).
    """
    d0 = datetime.strptime(start, fmt_date)
    if verbose: 
        print("Creating list of elapsed times")
        print("  Initial date (str): " + start)
        print("  Parsed initial date: " + str(d0) )
    
    telap = []
    for d in dates:
        delta = d - d0
        t = delta.days + delta.seconds / 86400.0 + delta.microseconds / (86400.0 * 1.e6)
        telap.append(t)
    
    if verbose2:
        print("Date \t Telap \t [days]")
        for i in range(len(telap)):
            sdate = dates[i].strftime(fmt_date)
            print("%s \t %g \t [days]"%(sdate, telap[i]))
        
    return telap
    

def is_iterable(obj):
    """ Returns true if obj is a tuple, list or dictionary so it can be iterated.
    """
    return isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, dict)
    

def process_text(src, do, out = sys.stdout, encoding = "utf-8", original=False):
    """ Basic text processing function: 
            Read all lines in file src, and pass it to function do, which returns 
            a modified list of lines that are printed to out.
        
        Args:
            src: path to file.
            do: function (list[str] -> list[str])
            out: stream-like object to print resulting lines.
            encoding: string that defines encoding of file.
            original: if True, then print original before printing modified lines.
    """
    with open(src, encoding=encoding) as f:
        lines = f.readlines()
    
    plines = []
    for l in lines:
        plines.append(l.strip())
        
    if original:
        print(40*">" + "ORIGINAL" + 40*"<" )
        for l in plines: print(l)
        print(120*"-")
        print(120*"=")
    
    nlines = do(plines)
    for l in nlines: print(l.strip())
    
    
def read_tab_file(src: str, sep: str, strip: bool=False, verbose: bool=True, encoding: str = "utf-8", skip = 0):
    """ Reads data from a text file that has tabular format, i.e. columns of data
        are separated by a string.
        
        Args:
            src: path to file that should be read.
            sep: String used as column separator. All lines in the file should have
                 the same number of separators.
            strip: if True, then strip blank space from strings.
            verbose: if True, print some information. 
            encoding: encoding of the file.
            skip: number of lines to be skipped at the beginning of file.
        
        Returns:
            List of list of values in the file as strings. Each line in the file,
            corresponds to a list of values. It also returns list of skipped lines.
            return (values, skipped)
            
        
        NOTE: All content of the file is read at once, which should be ok for most files
             that are smaller than available memory. 
    """
    if verbose: print("Reading file: " + src)
    
    s = open(src, "r", encoding=encoding)
    lines = s.readlines()
    s.close()
    
    if verbose: print("   Read %d lines"%(len(lines)))
    
    if skip > 0:
        skipped = lines[0:skip]
        lines = lines[skip:]
    else:
        skipped = []
    
    v = lines[0].split(sep)
    nsep = len(v)
    if verbose: 
        print("   # separators in first line: %d  skip: %d"%(nsep, skip))
    
    values = []
    for l in lines:
        ll = l.strip()                 #FIX LAST EMPTY LINE
        if len(ll) == 0: 
            if verbose: print("    WARNING - Skipping empty line")
            continue
            
        v = ll.split(sep)
        assert len(v) == nsep, "Line have different number of separators. nsep: %d  line: >>%s<<\n"%(nsep, ll)
        if strip:
            for i in range(len(v)):
                v[i] = v[i].strip()
        values.append(v)
    
    return values, skipped

    
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
    

def timeit(f, verbose = False, source=False):
    """ Time the execution time of function f. 
    
    Args:
        f: callable.
        verbose: if True, prints results.
        source: if True, print source
    Returns: 
        Time in seconds. 
    """
    source = inspect.getsource(f)
    start = time.perf_counter_ns()
    f()
    end = time.perf_counter_ns()
    elap = (end - start) / 1.e9
    
    if source: print(source)
    if verbose: print("   +++Elapsed time %g [sec]"%elap)
    return elap
    
    
def touchit(src, replace, dst = None, verbose = False, src_encoding="utf-8", dst_encoding="utf-8", test = False, debug=False):
    """ Replace each appearance of old string in file src by new string specified in the list replace. 
    
        This is useful when a file needs some touches before it 
        can imported into a Table, e.g. replace "," by a "." as decimal
        separator. It also allows changing the encoding of a text file.
        
        It is a very simple version of what is provided by grep or similar programs.
        
        Args:
            src: full path to source file.
            replace: a list of (old,new) regexes that must be substituted.
                     Replacement is performed one by one in the given order of pairs.
            dst: if present, then new file is writen to this path.
                 If not present (default), existing file is overwritten.
            verbose: if True, then prints some information to standard output.
            src_encoding: file encoding for source file as accepted by Python open function, e.g. utf-8.
            dst_encoding: file encoding for destination file as accepted by Python open function, e.g. ascii.
                          For details, see https://docs.python.org/3/library/codecs.html#module-codecs
            test: if True, then print resulting text to standard output. 
            
        NOTE: All content of the file is read in memory to make the process faster. 
              And the replacement is done all at once by calling replace(old, new).
    """
    assert is_iterable(replace)
    
    if verbose: print("Touchit: " + src)
    
    s = open(src, "r", encoding=src_encoding)
    txt = s.read()
    s.close()
    
    for r in replace:
        old = r[0]
        new = r[1]
        if debug: print("(old, new): >>%s<< >>%s<<"%(old, new))
        txt = txt.replace(old, new)
    
    if not dst and test: 
        print(txt)
        #input("PRESS ENTER")
        if verbose: print("    Touchit FINISHED")
        return 
        
    elif not dst:
        dst = src
    
    if verbose: print("    Modified text saved to: " + dst)
    w = open(dst, "w", encoding=dst_encoding) 
    w.write(txt)
    w.close()
    #input("PRESS ENTER") # DEBUG
    
    if verbose: print("    Touchit FINISHED")
    return

    
def walker(fpath: str, ffilter = lambda x: True, verbose = False, level = 0, lfiles = [], absPath = True):
    """ Returns a list of full path to all files in root directory and subdirectories.
    
        Args:
            fpath: path to root directory.
            ffilter: function used to check filenames, if ffilter(fpath) = True, then
                     file is included in the returned list. fpath is path to file 
                     including directories.
            verbose: if True, prints output while visit the directory tree.
            level: directory level, passed as argument to call function recursively.
                   Default value should not be changed when call directly.
            lfiles: list of files, passed as argument to call function recursively.
                    Default value should not be changed when call directly.
            absPath = if True, then include absolute path in list. If False, then
                      includes relative path.
        Returns:
            List of full path to files in directory.
    """
    indent = level*"   "
    apath = os.path.abspath(fpath)
    fname = os.path.basename(fpath)
    
    if os.path.isdir(fpath):
        if verbose and not absPath: 
            print(indent + "+" + str(level) + ": " + fpath)
        elif verbose:
            print(indent + "+" + str(level) + ": " + apath)
            
        ld = os.listdir(fpath)
        for f in ld:
            af = os.path.join(fpath, f)
            lfiles = walker(af, ffilter, verbose, level + 1, lfiles, absPath)
        
        return lfiles
    else:
        if verbose and not absPath:     
            print(indent + "     -" + fname, end="")
        else:
            print(indent + "     -" + apath, end="")
        
        if ffilter(fpath):
            if absPath:
                lfiles.append(apath)
            else:
                lfiles.append(fpath)     
            if verbose: print(" \t\t\t+")
        else:
            if verbose: print("")
            
        return lfiles

# TODO: ADD TEST
def dict_from_txt(src, sep = ",", converter = None, verbose = False, skip = 0, encoding = "utf-8"):
    """ Reads a dictionary {key:value} from text file.
        
        Args:
            src: path to text file.
            sep: separartor between key, value pair.
            converter: if present, use it to convert values from strings.
            verbose: if True, prints some information to stdout.
            skip: skip this number of lineas before reading values.
            encoding: use this encoding to read the content of the file.
    """
    lines, skipped = read_tab_file(src, sep = sep, strip = True, verbose = verbose, encoding = encoding, skip = skip)
    
    nvalues = len(lines)
    d = {}
    for l in lines:
        assert len(l) == 2, l
        k = l[0]
        v = l[1]
        if converter: v = converter(v)
        d[k] = v
    
    return d 
    