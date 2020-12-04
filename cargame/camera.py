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

        # Marker when camera port will be updated this frame
        self.moved = False

    def on_start_update(self):
        """ Will be run at the beginning of them main update function """
        self.moved = False

    def update_camera_pos(self, x=None, y=None, zoom=None):
        """
        Updates the position according to the x, y, and zoom
        """
        
        # Mark camera as moved this frame
        self.moved = True

        # Move and do maths
        zoom_mult = zoom_multiplexer(self.zoom)
        if x != None:
            self.right = x + int(g.screen_width * zoom_mult)
            self.x = x

        if y != None:
            self.top = y + int(g.screen_height * zoom_mult)
            self.y = y

        # print("Port size: ({}, {}) zoom: {}".format(self.right - self.x, self.top - self.y, self.zoom))

    def update_zoom(self, zoom, anchor_x, anchor_y):
        """ Updates the zoom of the main canvas """

        # Mark camera as moved
        self.moved = True

        # Calculate zoom increment
        zoom_inc = self.zoom - zoom
        
        # Get the linear interpolation so that the zoom is
        # focused on the anchor
        x_lerp = util.invlerp(0, g.screen_width, anchor_x)
        y_lerp = util.invlerp(0, g.screen_height, anchor_y)

        # print("x: {} y: {} right: {} top: {}".format(self.x, self.y, self.right, self.top))
        # print("xlerp: {} ylerp: {}".format(x_lerp, y_lerp))

        # Calculate the camera maths here
        self.x = self.x - (x_lerp * g.screen_width * zoom_inc) / 2
        self.y = self.y - (y_lerp * g.screen_height * zoom_inc) / 2
        self.right = self.right + ((1-x_lerp) * g.screen_width * zoom_inc) / 2
        self.top = self.top + ((1-y_lerp) * g.screen_height * zoom_inc) / 2

        self.zoom = round(zoom, 3)
        # print("x: {} y: {} right: {} top: {}".format(self.x, self.y, self.right, self.top))
        # print("Port size: ({}, {}) zoom: {}".format(self.right - self.x, self.top - self.y, self.zoom))

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

    def get_viewport(self):
        """ Gets the size of the viewport """
        return (self.right - self.x, self.top - self.y)

class Grid():

    def __init__(self, camera):
        """
        Detects the camera movement
        """
        self.grid_size = 40
        self.grid_lines = []
        self.camera: Camera = camera
        self.recreate_grid()

    def update(self):
        """ Update """

    def recreate_grid(self):
        """ Recreate the grid from the ground up
        
        This will recreate the grids with an offset based on the camera position.
        Therefore, grids will be only drawn in the place of the camera, not outside."""

        # Reset the grid lines
        self.grid_lines = []

        # Recreate the vertical lines
        viewport = self.camera.get_viewport()
        for i in range(int(viewport[0]) // self.grid_size + 2):
            self.grid_lines.append([self.camera.x + self.grid_size * i - (self.camera.x % self.grid_size), self.camera.y + -self.grid_size])
            self.grid_lines.append([self.camera.x + self.grid_size * i - (self.camera.x % self.grid_size), self.camera.y + viewport[1] + self.grid_size])

        # Horizontal lines
        for i in range(int(viewport[1]) // self.grid_size + 2):
            self.grid_lines.append([self.camera.x + -self.grid_size, self.camera.y + self.grid_size * i - (self.camera.y % self.grid_size)])
            self.grid_lines.append([self.camera.x + viewport[0] + self.grid_size, self.camera.y + self.grid_size * i - (self.camera.y % self.grid_size)])

    def draw_grid(self):
        """ Draws the grid based on the configuration """

        # Only update grid when camera is moved.
        if self.camera.moved:
            # Recreate every line grid
            self.recreate_grid()
        
        arcade.draw_lines(self.grid_lines, (220, 220, 220))