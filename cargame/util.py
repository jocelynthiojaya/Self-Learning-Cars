def invlerp(a, b, v):
    """ Inverse lerp.
    a: left range
    b: right range
    v: value

    Will give a fraction of where v is between a and b.
    """
    try:
        return (v - a) / (b - a)
    except ZeroDivisionError:
        return 0