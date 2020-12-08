import arcade
import numpy as np
from cargame.util import rotation_matrix, delta_unit, clamp, distance
import cargame.collision as col
import cargame.globals as g
from time import time

class Car:
    """ Car object, with collisions """

    # The shape of the car
    car_poly = [
            [30, 0],
            [25, 10],
            [-5, 10],
            [-5, -10],
            [25, -10]
        ]

    # The sensor of the cars. Is an array of point pairs
    car_sensor = [
        [30, 0], [100, 0],
        [25, 10], [65, 50],
        [25, -10], [65, -50],
        [20, 10], [20, 50],
        [20, -10], [20, -50]
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
        self.res_poly = [ [self.x + x, self.y + y] for x, y in Car.car_poly ]

        # Sensor poly, this is used to gather collision information
        self.res_sensor = [ [self.x + x, self.y + y] for x, y in Car.car_sensor ]

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

        # Car color. Will change if collision is detected.
        self.car_color = arcade.color.BLUE_SAPPHIRE

        # Car sensors, AI information can be gotten from this.
        # -1 means no collision is detected in the line of sight.
        # 0-1 means the distance.
        self.sensors = [ -1 for _ in range(len(Car.car_sensor)//2) ]

    def update(self):
        """ Update every frame """
        # TODO: Put AI Code here.

        # Handle rotation and movements
        # Handle the turn
        self.rotate(self.direction - self.wheel_turn * delta_unit(Car.car_maxturnrate))
        
        # Reset sensor
        self.sensors = [ -1 for _ in range(len(Car.car_sensor)//2) ]

    def handle_movement(self, future_poly=None):
        """ Script to handle movement with futures and collisions.
        If future poly is None, then the car does not move.
        If it is not empty, then car will be moved to the current polygon """

        if not future_poly:
            # If collision is detected then reset the future value.
            # Do the on collision script
            self.on_collision()
            self.fx = self.x
            self.fy = self.y
            self.fdirection = self.direction
        else:
            # If no collision, then replace the current poly with the new poly, and calculate poly for sensors
            self.res_sensor = self.get_future_poly(Car.car_sensor)
            self.x = self.fx
            self.y = self.fy
            self.direction = self.fdirection
            self.res_poly = future_poly
            
    def get_future_poly(self, poly):
        """ Gets the future poly """
        # If direction is changed, then run the rotation matrix poly. If not, just translation.
        if self.fdirection != self.direction:
            # Translation and rotation matrix
            new_poly = []
            for x, y in poly:
                rot = rotation_matrix(x, y, np.radians(self.fdirection))
                new_poly.append([rot[0] + self.fx, rot[1] + self.fy])
            return new_poly
        else:
            # Do normal translation
            return [ [self.fx + x, self.fy + y] for x, y in poly ]

    def on_collision(self):
        """ Will be run if collision is detected. """
        self.car_color = arcade.color.RED_DEVIL

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
        arcade.draw_polygon_filled(self.res_poly, self.car_color)
        self.draw_bounding_box()
        arcade.draw_lines(self.res_sensor, (50, 50, 50, 80))

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

    def __init__(self, trackmanager):
        """ Inits the Carmanager, needs a trackmanager as a parameter to calculate the collisions"""

        self.trackmanager = trackmanager

        # Cars that this car manager contains
        self.cars = []

        # The collision dictionary
        self.coll_dict = {}

    def insert_car(self, car):
        self.cars.append(car)

    def update_cars(self):
        """ Does all the collision algorithms for the car, and the update mechanism with the track also. """
        """ Reconstructs and handles the collision on the fly, to be more efficient """
        self.coll_dict = {}

        # Grid size
        size = g.conf["col_grid_size"]

        for car in self.cars:
            # Update the car vars
            car.update()
            
            # Get the future polygon, and use it for collision
            f_poly = car.get_future_poly(Car.car_poly)

            # First, based on the car's bounding box insert it into the coll_dict.
            x1, y1, x2, y2 = col.poly_bounding_box(f_poly)

            # Whether the car is colliding or not.
            collision = False

            ## Checks and inserts the bounding box into the grids that it overlaps
            # Gets all the grid it consumes
            for i in range(int(x1 // size), int(x2 // size + 1)):
                for j in range(int(y1 // size), int(y2 // size + 1)):
                    # Check the collision first
                    # Iterate every collidable object in the coll_dict and in the coll_dict of track manager.
                    
                    # If a collision has not been confirmed yet, then check it.
                    # Track collision
                    if not collision:
                        for obj in self.trackmanager.coll_dict.get((i, j), []):
                            # Check the AABB of the current car and the destination object
                            if col.rectrect(x1, y1, x2, y2, *col.correct_bounding_box(obj[0], obj[1], obj[2], obj[3])):
                                # AABB collision detected
                                if col.linepoly(obj[0], obj[1], obj[2], obj[3], f_poly):
                                    collision = True
                                break
                    # Car collision
                    if not collision:
                        for obj in self.coll_dict.get((i, j), []):
                            # Check the AABB of the current car and the destination object
                            if col.rectrect(x1, y1, x2, y2, obj[0], obj[1], obj[2], obj[3]):
                                # AABB collision detected
                                if col.polypoly(f_poly, obj.res_poly):
                                    collision = True
                                break
                    
                    # Insert into grid.
                    if (i, j) not in self.coll_dict:
                        self.coll_dict[(i, j)] = [[x1, y1, x2, y2]]
                    else:
                        self.coll_dict[(i, j)].append([x1, y1, x2, y2])

            # Move the car if collision is not detected.
            if not collision:
                car.handle_movement(f_poly)
            else:
                car.handle_movement()

        # Here, we can do one more iteration to get all the distances from the sensors.
        # We are doing it here because only here all the collision map for the moment is done.
        for car in self.cars:

            # First, iterate all the individual sensors
            for s in range(len(car.res_sensor)//2):

                # Gets the bounding box for the current sensor
                # This is an array length of 4 [x1, y1, x2, y2]
                sensor = car.res_sensor[s*2] + car.res_sensor[s*2 +1]
                x1, y1, x2, y2 = col.correct_bounding_box(*sensor)

                # Iterate all the collision objects
                for i in range(int(x1 // size), int(x2 // size + 1)):
                    for j in range(int(y1 // size), int(y2 // size + 1)):
                        
                        # First, iterate over the roads
                        for obj in self.trackmanager.coll_dict.get((i, j), []):
                            # If a bounding box is found
                            if col.rectrect(x1, y1, x2, y2, *col.correct_bounding_box(*obj)):
                                # print("Sensor {}:".format(s), *sensor, *obj)
                                # Find the line intersection.
                                intersection = col.lineline(*sensor, *obj, True)
                                if intersection:
                                    # Add the sensor data to the car object.
                                    car.sensors[s] = distance(sensor[0], sensor[1], *intersection, True)
    
    def update(self):
        self.update_cars()

    def on_draw(self):
        for car in self.cars:
            car.on_draw()