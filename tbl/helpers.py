def _split_line(l, sep):
    l = l.strip().rstrip(sep)
    return l.split(sep)

def _is_iterable(obj):
    return isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, dict)