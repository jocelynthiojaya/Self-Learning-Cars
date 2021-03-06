import arcade
import numpy as np
from cargame.util import rotation_matrix, delta_unit, clamp, distance
import cargame.collision as col
import cargame.globals as g

from time import time
from carbrain.neuralnetwork import NeuralNetwork
from carbrain.geneticAlgorithm import geneticAlgorithm
from random import randint, random

# The sensor of the cars. Is an array of point pairs
CAR_SENSOR = [
        [30, 0], [140, 0],
        [25, 10], [80, 70],
        [25, -10], [80, -70],
        [20, 10], [35, 65],
        [20, -10], [35, -65]
    ]

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

    # Just inherit from constant
    car_sensor = CAR_SENSOR

    # Calculate the individual maximum distances of the sensors.
    sensor_max_dist = [ distance(*CAR_SENSOR[i*2], *CAR_SENSOR[i*2 + 1]) for i in range(len(CAR_SENSOR)//2) ]

    car_maxturnrate = 120

    outline_col = arcade.color.CELESTIAL_BLUE

    # This is in pixel per second
    max_speed = 100

    # Calculate distance fitness every x seconds
    fit_calc = 3

    def __init__(self, x, y, weights=None):
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
        # 1 means no collision is detected in the line of sight.
        # 0-1 means the distance.
        self.sensors = [ 1 for _ in range(len(Car.car_sensor)//2) ]
        
        # Car's speed
        self.speed = 0
        self.accel = 0

        # Car's weights
        self.weights = np.array([random() for _ in range(38)]) if weights == None else weights
        
        # Car's neural network
        self.neuralnetwork = NeuralNetwork(self.weights)

        # Car's state. If true, then the car will be calculated in collisions
        self.active = True

        # Car fitness for genetic algorithm
        # The means that is calculates the fitness is through the distance traveled.
        # Distance traveled is counted every x seconds from the start, calculating distance from the previous.
        self.fit = 0.0

        # Helper to calculate the coordinates
        self.fit_last_coords = [x, y]

    def update(self):
        """ Update every frame """
        # TODO: Put AI Code here.
        ########################################

        ff = self.neuralnetwork.feedforward(self.sensors)
        self.speed = ff[0]*100
        self.wheel_turn = (ff[1]*2)-1

        ########################################
        # Handle acceleration and speed
        self.speed += delta_unit(self.accel)
        if self.speed != 0: self.move_forward(self.speed)

        # Handle rotation and movements
        self.rotate(self.direction - clamp(self.wheel_turn, -1, 1) * delta_unit(Car.car_maxturnrate) + self.fdirection - self.direction)
        # self.rotate(self.direction - self.wheel_turn * delta_unit(Car.car_maxturnrate) + self.fdirection - self.direction)
        
        # Reset sensor
        self.sensors = [ 1 for _ in range(len(Car.car_sensor)//2) ]

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

    def set_accel(self, accel):
        """ Set the car's acceleration """
        """ Accel is pixel per second second """
        self.accel = accel

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

    def set_speed(self, speed):
        """ Sets the constant speed of the car """
        self.speed = speed

    def move_forward(self, speed):
        """ Moves the car forward according to the direction. The speed unit is pixels.
        if speed is minus, then car will move backwards. """

        # Clamp the speed
        speed = clamp(delta_unit(speed), 0, delta_unit(Car.max_speed))

        # Appends the speed according to the direction
        rad = np.radians(self.direction)
        self.fx += speed * np.cos(rad)
        self.fy += speed * np.sin(rad)

        # Set marker to move
        self.moved = True

    def on_draw(self):
        """ Draw """
        arcade.draw_polygon_filled(self.res_poly, self.car_color)
        # arcade.draw_polygon_outline(self.res_poly,  Car.outline_col)
        # self.draw_bounding_box()
        # This is to draw the sensor lines
        # arcade.draw_lines(self.res_sensor, (50, 50, 50, 50))

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

    def __init__(self, trackmanager, x_begin=0, y_begin=0, direction=0, count=0):
        """ Inits the Carmanager, needs a trackmanager as a parameter to calculate the collisions"""

        self.trackmanager = trackmanager

        # Cars that this car manager contains
        self.cars = []
        
        # If sensor point is enabled
        self.draw_sensor = True

        # Store sensor collision points here for drawing.
        self.collision_points = []

        # Coordinates from which the cars would begin
        self.x_begin = x_begin
        self.y_begin = y_begin

        # Amount of cars to be created.
        self.count = count
        
        # Set the initial directions
        self.direction = direction

        # Paused state
        self.paused = False

        # Create the cars
        for _ in range(count):
            car = Car(x_begin, y_begin)
            car.rotate(direction)
            self.insert_car(car)

        # Fit timer for calculating the distance of every car.
        self.fit_timer = 0.0

        # Fit list that contains a list of index and fit [[car_index, fit], ...]
        self.fit_list = []

        # List containing 2 values, containing the best cars in each checks. Contains the index
        self.best_fit = [randint(0, g.conf["car_count"]-1), randint(0, g.conf["car_count"]-1)]

        # Duration left in a generation.
        self.generation_timer = g.conf["gen_duration"]

        # Iteration count
        self.iteration = 1

    def reset_gen(self): 
        """ use this function to reset every generation """
        # Create a new batch of cars based on the best ones.
        new_cars = []
        for _ in range(g.conf["car_count"]):
            # Generate new set of weights using the genetic algorithm
            gen_alg = geneticAlgorithm(self.cars[self.best_fit[0]].weights, self.cars[self.best_fit[1]].weights)

            # Get the new weights
            new_cars.append(Car(self.x_begin, self.y_begin, list(gen_alg.mutation(g.conf["gen_mutation"])[0])))

        # Replace the current cars
        del self.cars[:]
        self.cars = new_cars

        # Reset everything
        self.fit_timer = 0.0
        self.best_fit = [randint(0, g.conf["car_count"]-1), randint(0, g.conf["car_count"]-1)]
        self.generation_timer = g.conf["gen_duration"]
        self.iteration += 1

    def insert_car(self, car):
        self.cars.append(car)

    def set_paused(self, state):
        self.paused = state

    def update_cars(self):
        """ Does all the collision algorithms for the car, and the update mechanism with the track also. """
        """ Reconstructs and handles the collision on the fly, to be more efficient """

        # Run the cars if the sim is not paused.
        if self.paused: return

        if self.draw_sensor: self.collision_points = []

        # Calculate the delta of fit_timer and generation timer
        self.fit_timer += g.delta
        self.generation_timer -= g.delta

        # If the timer is up, then go to the next generation.
        if self.generation_timer <= 0:
            self.reset_gen()

        # Determine whether the fitness of each car will be calculated in this frame.
        calc_fit = False
        if self.fit_timer > Car.fit_calc:
            self.fit_timer -= Car.fit_calc
            calc_fit = True

            # Reset list
            self.fit_list = []

        # Grid size
        size = g.conf["col_grid_size"]
        # start = time()

        # Counter for the cars
        counter = 0
        for car in self.cars:
            # We check first if the car is active.
            # If its not, move on to the next car.
            counter += 1

            # Calculate the fitness, if it's determined to be calculated this frame.
            if calc_fit:
                # Only calculate if car is active
                if car.active:
                    car.fit += distance(car.x, car.y, *car.fit_last_coords)
                    car.fit_last_coords = [car.x, car.y]
                self.fit_list.append([counter - 1, car.fit])

            if not car.active:
                continue

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

            # Move the car if collision is not detected.
            if not collision:
                car.handle_movement(f_poly)
            else:
                # Don't move the car and deactivate.
                car.handle_movement()
                car.active = False
                        
            # Here, we can do one more iteration to get all the distances from the sensors.
            for s in range(len(car.res_sensor)//2):

                # Gets the bounding box for the current sensor
                # This is an array length of 4 [x1, y1, x2, y2]
                sensor = car.res_sensor[s*2] + car.res_sensor[s*2 +1]
                
                # Get the correct bounding box
                x1, y1, x2, y2 = col.correct_bounding_box(*sensor)

                # Iterate all the collision objects
                collision = False
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
                                    car.sensors[s] = distance(sensor[0], sensor[1], *intersection, True) / Car.sensor_max_dist[s]
                                    collision = True
                                    if self.draw_sensor: self.collision_points.append(intersection)

                # Draw the dot at the tip of the sensor if collision is not detected.
                if self.draw_sensor and not collision:
                    self.collision_points.append([sensor[2], sensor[3]])

        if calc_fit:
            max_fit = max(self.fit_list, key=lambda x : x[1])[1]

            # Calculate fit based on the normalized value from the distance fit,
            # and the speed of the car.
            fit_final = list(map(
                lambda x : [x[0], (x[1]/max_fit) + self.cars[x[0]].speed/Car.max_speed * 0.5],
                self.fit_list
            ))
            fit_final.sort(key=lambda x: x[1], reverse=True)

            # Set the best fit
            self.best_fit = [fit_final[0][0], fit_final[1][0]]
            
            # Change the color according the best.
            for i in range(len(self.cars)):
                self.cars[i].car_color = arcade.color.ALLOY_ORANGE if i in self.best_fit else (arcade.color.BLUE_SAPPHIRE if self.cars[i].active else arcade.color.RED_DEVIL)

        g.ui_text += "Time Left: {}\nIteration: {}\n".format(round(self.generation_timer), self.iteration)
        # print("col_time: {}ms".format(round((time() - start) * 1000, 2)))
    
    def update(self):
        self.update_cars()

    def on_draw(self):
        # start = time()
        for car in self.cars:
            car.on_draw()

        # print("draw_time: {}ms".format(round((time() - start) * 1000, 2)))
        if self.draw_sensor and len(self.collision_points) != 0:
            arcade.draw_points(self.collision_points, arcade.color.GRAY, 3)