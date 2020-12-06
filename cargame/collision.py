""" General collision functions """

def lineline(x1, y1, x2, y2, x3, y3, x4, y4):

    try:
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    except ZeroDivisionError:
        if y2-y1 == 0 and y4-y3 == 0:
            return False
        return True

    if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
        return True
    return False

def linerect(x1, y1, x2, y2, rx3, ry3, rx4, ry4):

    if (
        lineline(x1, y1, x2, y2, rx3, ry3, rx3, ry4) or
        lineline(x1, y1, x2, y2, rx3, ry3, rx4, ry3) or
        lineline(x1, y1, x2, y2, rx4, ry3, rx4, ry4) or
        lineline(x1, y1, x2, y2, rx3, ry4, rx4, ry4)
    ): return True
    return False