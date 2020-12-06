import arcade
import numpy as np
from cargame.util import rotation_matrix, delta_unit, clamp
import cargame.globals as g

class Car:
    """ Car object, with collisions """

    car_poly = [
            [30, 0],
            [25, 10],
            [-5, 10],
            [-5, -10],
            [25, -10]
        ]

    car_maxturnrate = 120

    def __init__(self, x, y):
        """ Inits the car """
        # The coordinates of the origin point

        # all the variables with the f (future) prefix is to keep track of the
        # value after moving it.
        # Useful for collision detection.
        self.fx = x
        self.x = x
        self.fy = y
        self.y = y

        # 90 is up, 0 is right.
        self.fdirection = 0
        self.direction = 0

        # Result poly, this will be drawn.
        self.res_poly = np.add([x, y], Car.car_poly)

        # The bounding box variables
        # Note: The bounding box is relative to 0. Not yet appended with the
        # current coordinate.
        self.xmin = 0
        self.ymin = 0
        self.xmax = 0
        self.ymax = 0

        # Whether the bounding box changes
        self.bounds_changed = True

        # Whether the car is moved.
        self.moved = False

        # Turn rate
        # -1.0 = left, 0 = straight, 1.0 = right
        self.wheel_turn = 0

    def update(self):
        """ Update every frame """

        # Script will only be run if object is moved.
        if self.moved:
            self.handle_movement()
            self.moved = False

    def handle_movement(self):
        """ Script to handle movement with futures and collisions """

        # Handle the turn
        self.rotate(self.direction - self.wheel_turn * delta_unit(Car.car_maxturnrate))

        # First, move the car into position on which we want to check the collision
        future_poly = None

        # If direction is changed, then run the rotation matrix poly. If not, just translation.
        if self.fdirection != self.direction:
            # Translation and rotation matrix
            future_poly = [ np.add(rotation_matrix(i, j, np.radians(self.fdirection)), [self.x, self.y]) for i, j in Car.car_poly ]
        else:
            # Do normal translation
            future_poly = np.add([self.fx, self.fy], Car.car_poly)
            
        # Detects for collisions with the future values
        # TODO: Change the True statement into a collision checking algorithm.
        if True:
            self.x = self.fx
            self.y = self.fy
            self.direction = self.fdirection
            self.res_poly = future_poly
        else:
            # If collision is detected then reset the future value.
            # Do the on collision script
            self.on_collision()
            self.fx = self.x
            self.fy = self.y
            self.fdirection = self.direction

    def on_collision(self):
        """ Will be run if collision is detected. """

    def rotate(self, direction):
        """ In degrees, set the car's direction to the value, rotate the car polygons, and 
        set the forward direction. """
        
        # If the direction is actually different, then rotate the polygons
        if direction != self.direction:
            self.fdirection = direction

            # Set bounding box to change
            self.bounds_changed = True

            # Set marker to move
            self.moved = True
        
    def set_wheel(self, wheel):
        """ Sets the wheel's direction.
        -1.0 = left
        0 = straight
        1.0 = right
        """
        self.wheel_turn = clamp(wheel, -1, 1)

    def move_forward(self, speed):
        """ Moves the car forward according to the direction. The speed unit is pixels.
        if speed is minus, then car will move backwards. """

        # Appends the speed according to the direction
        
        rad = np.radians(self.direction)
        self.fx += speed * np.cos(rad)
        self.fy += speed * np.sin(rad)

        # Set marker to move
        self.moved = True

    def on_draw(self):
        """ Draw """
        arcade.draw_polygon_filled(self.res_poly, arcade.color.BLUE_SAPPHIRE)
        self.draw_bounding_box()

    def get_bounding_box(self, poly=None):
        """ Gets the bounding box of the polygons. (Updates it if necessary)
        :poly: use a custom polygon for the bounding box. If not supplied, use the result poly.
        :return -> [xmin, ymin, xmax, ymax] """

        use_poly = poly if poly else self.res_poly

        # TODO: Test to comply with future values.
        # Updates the bounds
        if self.bounds_changed:
            # Gets the minimum and maximum value of each bounds.
            self.xmin = float('inf')
            self.ymin = float('inf')
            self.xmax = float('-inf')
            self.ymax = float('-inf')

            for points in use_poly:
                x = points[0] - self.x
                y = points[1] - self.y

                if x < self.xmin:
                    self.xmin = x
                if x > self.xmax:
                    self.xmax = x
                if y < self.ymin:
                    self.ymin = y
                if y > self.ymax:
                    self.ymax = y

            # Set bounds changed to be false
            self.bounds_changed = False
        
        return [self.xmin + self.x,
        self.ymin + self.y,
        self.xmax + self.x,
        self.ymax + self.y]

    def draw_bounding_box(self):
        """ Draws the bounding box """
        # Gets the bounding box
        xmin, ymin, xmax, ymax = self.get_bounding_box()

        # Gets the actual coordinates
        width = xmax - xmin
        height = ymax - ymin
        center_x = xmin + (width)/2
        center_y = ymin + (height)/2

        arcade.draw_rectangle_outline(center_x, center_y, width, height, (255, 0, 0))


class CarManager:
    """ Contains many car """