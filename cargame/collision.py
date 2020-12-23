""" General collision functions """

from numpy.lib.polynomial import poly1d


def lineline(x1, y1, x2, y2, x3, y3, x4, y4, get_intersection=False):
    """ Used to detect line on line intersection (Medium-fast) """
    try:
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    except ZeroDivisionError:
        if y2-y1 == 0 and y4-y3 == 0:
            return False
        return [0, 0] if get_intersection else True

    if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
        return [x1 + (uA * (x2-x1)), y1 + (uA * (y2-y1))] if get_intersection else True
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

def correct_bounding_box(x1, y1, x2, y2):
    """ Corrects the bounding box, so that the coordinates are small to big """
    xmin = 0
    ymin = 0
    xmax = 0
    ymax = 0

    if x1 < x2:
        xmin = x1
        xmax = x2
    else:
        xmin = x2
        xmax = x1
    if y1 < y2:
        ymin = y1
        ymax = y2
    else:
        ymin = y2
        ymax = y1

    return [xmin, ymin, xmax, ymax]

def pointpoly(x1, y1, poly):
    collision = False

    next = 0
    for i in range(len(poly)):

        # get next vertex in list
        # if we've hit the end, wrap around to 0
        next = i + 1
        if next == len(poly): next = 0

        # get the PVectors at our current position
        # this makes our if statement a little cleaner
        vc = poly[i]
        vn = poly[next]

        # compare position, flip 'collision' variable
        # back and forth
        if (((vc[1] > y1 and vn[1] < y1) or (vc[1] < y1 and vn[1] > y1)) and
            (x1 < (vn[0]-vc[0])*(y1-vc[1]) / (vn[1]-vc[1])+vc[0])):
                collision = not collision
        
    return collision

def linepoly(x1, y1, x2, y2, poly):
    
    # go through each of the vertices, plus the next
    # vertex in the list
    next = 0
    for i in range(len(poly)):

        # get next vertex in list
        # if we've hit the end, wrap around to 0
        next = i + 1
        if next == len(poly): next = 0

        # get the PVectors at our current position
        # extract X/Y coordinates from each
        x3 = poly[i][0]
        y3 = poly[i][1]
        x4 = poly[next][0]
        y4 = poly[next][1]

        # do a Line/Line comparison
        # if true, return 'true' immediately and
        # stop testing (faster)
        if lineline(x1, y1, x2, y2, x3, y3, x4, y4): return True

    # never got a hit
    return False

def polypoly(poly1, poly2):
    """ Narrow phase collision, heavy function """
    # go through each of the vertices, plus the next
    # vertex in the list
    next = 0
    for i in range(len(poly1)):

        # get next vertex in list
        # if we've hit the end, wrap around to 0
        next = i + 1
        if next == len(poly1): next = 0

        # get the PVectors at our current position
        # this makes our if statement a little cleaner
        vc = poly1[i];    # c for "current"
        vn = poly1[next];       # n for "next"

        # now we can use these two points (a line) to compare
        # to the other polygon's vertices using polyLine()
        collision = linepoly(vc[0],vc[1],vn[0],vn[1], poly2)
        if collision: return True

        # optional: check if the 2nd polygon is INSIDE the first
        collision = pointpoly(poly2[0][0], poly2[0][1], poly1)
        if collision: return True

    return False

def pointrect(x, y, rx1, ry1, rx2, ry2):
    """ Fast """
    return x > rx1 and x < rx2 and y > ry1 and y < ry2