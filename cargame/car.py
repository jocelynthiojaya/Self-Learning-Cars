import arcade
import numpy as np
from cargame.util import rotation_matrix

class Car:
    """ Car object, with collisions """

    car_poly = [
            [5, 0],
            [0, 10],
            [-30, 10],
            [-30, -10],
            [0, -10]
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
        """ In degrees, rotate the car """
        
        # If the direction is actually different, then rotate the polygons
        if direction != self.direction:
            self.res_poly = [ np.add(rotation_matrix(i, j, np.radians(direction)), [self.x, self.y]) for i, j in Car.car_poly ]
            self.direction = direction

    def on_draw(self):
        """ Draw """
        arcade.draw_polygon_filled(self.res_poly, arcade.color.BLUE_SAPPHIRE)


class CarManager:
    """ Contains many car """