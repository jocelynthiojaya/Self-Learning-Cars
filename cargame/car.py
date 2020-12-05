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

        # Poly appended with only the coordinates (not rotation)
        self.poly = [ [i + x, j + y] for i, j in Car.car_poly ]

        # Result poly, this will be drawn.
        self.res_poly = [ [i + x, j + y] for i, j in Car.car_poly ]

    def update(self):
        """ Update every frame """

    def rotate(self, direction):
        """ In degrees, set the car's direction to the value, rotate the car polygons, and 
        set the forward direction. """
        
        # If the direction is actually different, then rotate the polygons
        if direction != self.direction:
            self.res_poly = [ np.add(rotation_matrix(i, j, np.radians(direction)), [self.x, self.y]) for i, j in Car.car_poly ]
            self.direction = direction

    def move_forward(self, speed):
        """ Moves the car forward according to the direction. The speed unit is pixels.
        if speed is minus, then car will move backwards. """

        rad = np.radians(self.direction)
        self.x += speed * np.cos(rad)
        self.y += speed * np.sin(rad)

    def on_draw(self):
        """ Draw """
        arcade.draw_polygon_filled(self.res_poly, arcade.color.BLUE_SAPPHIRE)


class CarManager:
    """ Contains many car """