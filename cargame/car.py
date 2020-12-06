import arcade
import numpy as np
from cargame.util import rotation_matrix

class Car:
    """ Car object, with collisions """

    car_poly = [
            [30, 0],
            [25, 10],
            [-5, 10],
            [-5, -10],
            [25, -10]
        ]

    def __init__(self, x, y):
        """ Inits the car """
        # The coordinates of the origin point
        self.x = x
        self.y = y

        # 90 is up, 0 is right.
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

    def update(self):
        """ Update every frame """

    def rotate(self, direction):
        """ In degrees, set the car's direction to the value, rotate the car polygons, and 
        set the forward direction. """
        
        # If the direction is actually different, then rotate the polygons
        if direction != self.direction:
            self.res_poly = [ np.add(rotation_matrix(i, j, np.radians(direction)), [self.x, self.y]) for i, j in Car.car_poly ]
            self.direction = direction

        # Set bounding box to change
        self.bounds_changed = True

    def move_forward(self, speed):
        """ Moves the car forward according to the direction. The speed unit is pixels.
        if speed is minus, then car will move backwards. """

        # Appends the speed according to the direction
        rad = np.radians(self.direction)
        self.x += speed * np.cos(rad)
        self.y += speed * np.sin(rad)

        self.res_poly = np.add([self.x, self.y], Car.car_poly)

    def on_draw(self):
        """ Draw """
        arcade.draw_polygon_filled(self.res_poly, arcade.color.BLUE_SAPPHIRE)
        self.draw_bounding_box()

    def get_bounding_box(self):
        """ Gets the bounding box of the polygons. (Updates it if necessary)
        :return -> [xmin, ymin, xmax, ymax] """

        # Updates the bounds
        if self.bounds_changed:
            # Gets the minimum and maximum value of each bounds.
            self.xmin = float('inf')
            self.ymin = float('inf')
            self.xmax = float('-inf')
            self.ymax = float('-inf')

            for points in self.res_poly:
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