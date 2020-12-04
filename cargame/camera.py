import arcade
import cargame.globals as g
from cargame import util

# This math is for getting the ratio from zoom. I honestly
# don't know what it is called, i just constructed it by hand
# Long form is 1 - (x - 1) / 2
zoom_multiplexer = lambda x : (3 - x)/2

# TODO: Implement anchor
class Camera:

    def __init__(self):
        """ Set every camera variables
        s_width: Screen width
        s_height: Screen height
        """
        self.x = 0
        self.y = 0
        self.right = g.screen_width
        self.top = g.screen_height

        # The zoom of the main canvas
        self.zoom = 1

    def update_camera_pos(self, x=None, y=None, zoom=None):
        """
        Updates the position according to the x, y, and zoom
        """
        
        zoom_mult = zoom_multiplexer(self.zoom)
        if x != None:
            self.right = x + int(g.screen_width * zoom_mult)
            self.x = x
            # TODO: Calculation for real_x
            # self.real_x = x
        if y != None:
            self.top = y + int(g.screen_height * zoom_mult)
            self.y = y
            # self.real_y = y

        print("Port size: ({}, {}) zoom: {}".format(self.right - self.x, self.top - self.y, self.zoom))

    def update_zoom(self, zoom, anchor_x, anchor_y):
        """ Updates the zoom of the main canvas """
        zoom_inc = self.zoom - zoom
        
        # Get the linear interpolation so that the zoom is
        # focused on the anchor
        x_lerp = util.invlerp(0, g.screen_width, anchor_x)
        y_lerp = util.invlerp(0, g.screen_height, anchor_y)

        print("x: {} y: {} right: {} top: {}".format(self.x, self.y, self.right, self.top))
        print("xlerp: {} ylerp: {}".format(x_lerp, y_lerp))

        self.x = self.x - (x_lerp * g.screen_width * zoom_inc) / 2
        self.y = self.y - (y_lerp * g.screen_height * zoom_inc) / 2
        self.right = self.right + ((1-x_lerp) * g.screen_width * zoom_inc) / 2
        self.top = self.top + ((1-y_lerp) * g.screen_height * zoom_inc) / 2

        self.zoom = round(zoom, 3)
        print("x: {} y: {} right: {} top: {}".format(self.x, self.y, self.right, self.top))
        print("Port size: ({}, {}) zoom: {}".format(self.right - self.x, self.top - self.y, self.zoom))

    def move_camera_pos(self, dx, dy):
        """ Moves the camera by appending the variables to
        the individual coordinates.
        """
        self.update_camera_pos(self.x + dx, self.y + dy)

    def update_viewport(self):
        """ Updates the camera by updating
        the viewport of arcade
        """
        arcade.set_viewport(self.x, self.right, self.y, self.top)

    def handle_pan(self, dx, dy):
        """ Handles the camera pan from data gotten from
        mouse drag """

        # Here, we adjust the pan speed according to the level of zoom too.
        zoom_mult = zoom_multiplexer(self.zoom)
        self.move_camera_pos(-dx * zoom_mult, -dy * zoom_mult)

    def handle_zoom(self, mouse_x, mouse_y, scroll_y):
        """ Handles the camera scroll from data gotten from
        mouse scroll """

        # Must adjust according to where the pointer is.
        self.update_zoom(self.zoom + scroll_y * 0.05, mouse_x, mouse_y)