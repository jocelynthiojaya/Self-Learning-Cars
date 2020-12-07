""" General collision functions """

from numpy.lib.polynomial import poly1d


def lineline(x1, y1, x2, y2, x3, y3, x4, y4):
    """ Used to detect line on line intersection (Medium-fast) """
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

def linerect(x1, y1, x2, y2, rx1, ry1, rx2, ry2):
    """ Used to detect line on rectangle intersection (Medium) """
    if (
        lineline(x1, y1, x2, y2, rx1, ry1, rx1, ry2) or
        lineline(x1, y1, x2, y2, rx1, ry1, rx2, ry1) or
        lineline(x1, y1, x2, y2, rx2, ry1, rx2, ry2) or
        lineline(x1, y1, x2, y2, rx1, ry2, rx2, ry2)
    ): return True
    return False

def rectrect(x1, y1, x2, y2, x3, y3, x4, y4):
    """ Used to check whether the bounding box is colliding (Fastest) """
    if (
        x2 >= x3 and x1 <= x4 and
        y2 >= y3 and y1 <= y4
    ): return True
    return False

def poly_bounding_box(poly):
    """ Gets the bounding box of the polygons. (Updates it if necessary)
    :poly: use a custom polygon for the bounding box. If not supplied, use the result poly.
    :return -> [xmin, ymin, xmax, ymax] """

    # Gets the minimum and maximum value of each bounds.
    xmin = float('inf')
    ymin = float('inf')
    xmax = float('-inf')
    ymax = float('-inf')

    for x, y in poly:

        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y
    
    return [xmin, ymin, xmax, ymax]