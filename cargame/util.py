import arcade
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
    # Draw the 2 rectangles
    arcade.draw_rectangle_filled(center_x, center_y, width, height - radius*2, color)
    arcade.draw_rectangle_filled(center_x, center_y, width - radius*2, height, color)

    # Draw the circle border
    arcade.draw_circle_filled(center_x - width/2 + radius, center_y - height/2 + radius, radius, color)
    arcade.draw_circle_filled(center_x - width/2 + radius, center_y + height/2 - radius, radius, color)
    arcade.draw_circle_filled(center_x + width/2 - radius, center_y - height/2 + radius, radius, color)
    arcade.draw_circle_filled(center_x + width/2 - radius, center_y + height/2 - radius, radius, color)

def rotation_matrix(x, y, theta):
    """ Calculate the rotation matrix. Origin is assumed to be (0, 0)
    theta must be in radians
    """
    return [np.cos(theta) * x - np.sin(theta) * y, np.sin(theta) * x + np.cos(theta) * y]