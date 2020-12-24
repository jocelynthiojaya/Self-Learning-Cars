import arcade
import numpy as np
import cargame.globals as g
import numpy as np

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

def draw_rectangle_rounded(center_x, center_y, width, height, radius, color):
    """ Custom function to draw a rounded rectangle """
    shape_list = arcade.ShapeElementList()

    # Draw the 2 rectangles
    shape_list.append(arcade.create_rectangle_filled(center_x, center_y, width, height - radius*2, color))
    shape_list.append(arcade.create_rectangle_filled(center_x, center_y, width - radius*2, height, color))

    # Draw the circle border
    shape_list.append(arcade.create_ellipse(center_x - width/2 + radius, center_y - height/2 + radius, radius, radius, color))
    shape_list.append(arcade.create_ellipse(center_x - width/2 + radius, center_y + height/2 - radius, radius, radius, color))
    shape_list.append(arcade.create_ellipse(center_x + width/2 - radius, center_y - height/2 + radius, radius, radius, color))
    shape_list.append(arcade.create_ellipse(center_x + width/2 - radius, center_y + height/2 - radius, radius, radius, color))

    # Draw
    shape_list.draw()

def draw_arrow(center_x, center_y, length, direction, color, line_width=1, arrow_length=10):
    """ Draws an arrow, direction is in degrees """
    # Get the sins and coses
    sind = np.sin(np.radians(direction))
    cosd = np.cos(np.radians(direction))

    # Divide by 2
    length /= 2

    # Edge point of the line
    edgex = center_x + length*cosd
    edgey = center_y + length*sind

    arcade.draw_lines([
        [center_x - length*cosd, center_y - length*sind],
        [edgex, edgey],
        [edgex, edgey],
        [edgex + arrow_length*np.cos(np.radians(direction+135)), edgey + arrow_length*np.sin(np.radians(direction+135))],
        [edgex, edgey],
        [edgex + arrow_length*np.cos(np.radians(direction-135)), edgey + arrow_length*np.sin(np.radians(direction-135))]
    ], color, line_width)

def rotation_matrix(x, y, theta):
    """ Calculate the rotation matrix. Origin is assumed to be (0, 0)
    theta must be in radians
    """
    return [np.cos(theta) * x - np.sin(theta) * y, np.sin(theta) * x + np.cos(theta) * y]

def delta_unit(value):
    """ This will return a value processed according to the delta time frame.

    value: value per second.
    delta: frame time difference
    """
    return value * g.delta

def clamp(val, min, max):
    """ Clamps the number """
    if val > max:
        return max
    elif val < min:
        return min
    return val

def distance(x1, y1, x2, y2, root=True):
    """ Pythagorean theorem. can be rooted can be not for performance """
    return ((x2-x1)**2 + (y2-y1)**2)**0.5 if root else (x2-x1)**2 + (y2-y1)**2

def get_luminance(color):
    """ Return the luminance from a RGB value 0-255 """
    return (0.2126*color[0]) + (0.7152*color[1]) + (0.0722*color[2])
