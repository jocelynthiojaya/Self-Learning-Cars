import arcade
from cargame.globals import conf
from cargame import util

# This math is for getting the ratio from zoom. I honestly
# don't know what it is called, i just constructed it by hand
# Long form is 1 - (x - 1) / 2
zoom_multiplexer = lambda x : (3 - x)/2

# TODO: Implement anchor
class Camera:

    def __init__(self, left_bound, bottom_bound, right_bound, top_bound):
        """ Set every camera variables
        s_width: Screen width
        s_height: Screen height
        """
        self.x = 0
        self.y = 0
        self.right = conf["screen_width"]
        self.top = conf["screen_height"]

        # Camera bounds
        self.left_bound = left_bound
        self.bottom_bound = bottom_bound
        self.right_bound = right_bound
        self.top_bound = top_bound

        # The zoom of the main canvas
        self.zoom = 1

        # Whether zoom is enabled.
        self.can_zoom = True

        # Marker when camera port will be updated this frame
        self.moved = False

    def on_start_update(self):
        """ Will be run at the beginning of them main update function """
        self.moved = False

    def handle_border(self):
        """ Handles if the camera went out of bounds """

        bound_left = self.x < self.left_bound
        bound_right = self.right > self.right_bound
        if bound_left or bound_right:

            x_diff = self.left_bound - self.x if bound_left else self.right_bound - self.right
            self.x += x_diff
            self.right += x_diff

        bound_bot = self.y < self.bottom_bound
        bound_top = self.top > self.top_bound
        if bound_bot or bound_top:

            y_diff = self.bottom_bound - self.y if bound_bot else self.top_bound - self.top
            self.y += y_diff
            self.top += y_diff

    def update_camera_pos(self, x=None, y=None, zoom=None):
        """
        Updates the position according to the x, y, and zoom
        """
        
        # Mark camera as moved this frame
        self.moved = True

        # Move and do maths
        zoom_mult = zoom_multiplexer(self.zoom)
        if x != None:
            self.right = x + conf["screen_width"] * zoom_mult
            self.x = x

        if y != None:
            self.top = y + conf["screen_height"] * zoom_mult
            self.y = y

        self.handle_border()
        # print("Port size: ({}, {}) zoom: {}".format(self.right - self.x, self.top - self.y, self.zoom))

    def update_zoom(self, zoom, anchor_x, anchor_y):
        """ Updates the zoom of the main canvas """

        # Check first whether zoom is enabled
        if not self.can_zoom: return

        # Mark camera as moved
        self.moved = True

        # Clamp the zoom
        zoom = util.clamp(zoom, -5.0, 2.95)

        # Calculate zoom increment
        zoom_inc = self.zoom - zoom
        
        # Get the linear interpolation so that the zoom is
        # focused on the anchor
        x_lerp = util.invlerp(0, conf["screen_width"], anchor_x)
        y_lerp = util.invlerp(0, conf["screen_height"], anchor_y)

        # print("x: {} y: {} right: {} top: {}".format(self.x, self.y, self.right, self.top))
        # print("xlerp: {} ylerp: {}".format(x_lerp, y_lerp))
        
        # Camera view ports
        lp = self.x - (x_lerp * conf["screen_width"] * zoom_inc) / 2
        bp = self.y - (y_lerp * conf["screen_height"] * zoom_inc) / 2
        rp = self.right + ((1-x_lerp) * conf["screen_width"] * zoom_inc) / 2
        tp = self.top + ((1-y_lerp) * conf["screen_height"] * zoom_inc) / 2

        # If camera view port is within the bounds, do the zoom.
        if (rp - lp) < (self.right_bound - self.left_bound) and (tp - bp) < (self.top_bound - self.bottom_bound):

            # Calculate the camera maths here
            self.x = lp
            self.y = bp
            self.right = rp
            self.top = tp

            self.zoom = round(zoom, 3)
            self.handle_border()
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

    def reset_zoom(self):
        """ Reset the zoom of the camera to 1x """
        self.update_zoom(1, conf["screen_width"]/2, conf["screen_height"]/2)
    
    def set_can_zoom(self, state):
        self.can_zoom = state

class Grid():

    grid_size = 128

    def __init__(self, camera):
        """
        Detects the camera movement
        """
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
        for i in range(int(viewport[0]) // Grid.grid_size + 2):
            self.grid_lines.append([self.camera.x + Grid.grid_size * i - (self.camera.x % Grid.grid_size), self.camera.y + -Grid.grid_size])
            self.grid_lines.append([self.camera.x + Grid.grid_size * i - (self.camera.x % Grid.grid_size), self.camera.y + viewport[1] + Grid.grid_size])

        # Horizontal lines
        for i in range(int(viewport[1]) // Grid.grid_size + 2):
            self.grid_lines.append([self.camera.x + -Grid.grid_size, self.camera.y + Grid.grid_size * i - (self.camera.y % Grid.grid_size)])
            self.grid_lines.append([self.camera.x + viewport[0] + Grid.grid_size, self.camera.y + Grid.grid_size * i - (self.camera.y % Grid.grid_size)])

    def draw_grid(self):
        """ Draws the grid based on the configuration """

        # Only update grid when camera is moved.
        if self.camera.moved:
            # Recreate every line grid
            self.recreate_grid()

        arcade.draw_lines(self.grid_lines, (235, 235, 235))