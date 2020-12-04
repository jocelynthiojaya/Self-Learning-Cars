import arcade

# TODO: Implement anchor
class Camera:

    def __init__(self, s_width, s_height):
        """ Set every camera variables
        s_width: Screen width
        s_height: Screen height
        """
        self.x = 0
        self.y = 0
        self.right = s_width
        self.top = s_height

    def update_camera_pos(self, x=None, y=None, zoom=None):
        """
        Updates the position according to the x, y, and zoom
        """
        if x:
            self.right += x - self.x
            self.x = x
        if y:
            self.top += y - self.y
            self.y = y

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