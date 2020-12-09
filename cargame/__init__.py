import arcade
from cargame.camera import Camera, Grid
from cargame.ui import GameUI
from cargame.car import Car, CarManager
from cargame.track import TrackManager
import cargame.globals as g
import cargame.util as util
from random import randint, random

WINDOW_TITLE = "Self Learning Cars"

# Class for the main game window
class Main(arcade.Window):
    
    def __init__(self):
        """ Initialize the window """
        # Create the object
        super().__init__(g.conf["screen_width"], g.conf["screen_height"], WINDOW_TITLE)

        # Set background color as white
        arcade.set_background_color(arcade.color.WHITE)
        # Camera object
        self.cam = Camera(
            g.conf["c_bound_left"],
            g.conf["c_bound_bottom"],
            g.conf["c_bound_right"],
            g.conf["c_bound_top"]
        )
        self.grid = Grid(self.cam)
        self.ui = GameUI(self.cam)

        self.fps_text = ""

        self.track_manager = TrackManager()
        self.track_manager.add_track([
            [150, 150],
            [500, 150],
            [700, 300],
            [1100, 300],
            [1400, 0],
            [1900, 0],
            [1900, 150],
            [1400, 150],
            [1150, 400],
            [650, 400],
            [450, 250],
            [150, 250],
            [150, 150]
        ])
        # self.track_manager.add_track([
        #     [0, 0],
        #     [256, 256]
        # ])

        self.car_manager = CarManager(self.track_manager)

        for _ in range(20):
            car = Car(200, 200)
            # car.set_speed(randint(30, 70))
            # car.set_wheel((random()*0.3) - 0.15)
            self.car_manager.insert_car(car)
        

        # Schedule fps update
        arcade.schedule(self.update_fps_counter, 0.5)

    def update(self, delta_time: float):
        """ Will be run every frame """
        # Update the camera at the start
        self.cam.on_start_update()
        
        # Updates the delta time on globals
        g.delta = delta_time

        # For test only
        # Uncomment for test
        # self.car_manager.cars[0].set_accel(50)
        # self.car_manager.cars[0].set_wheel(-0.033)
        # self.car_manager.cars[1].move_forward(80)
        # self.car_manager.cars[1].set_wheel(-0.033)

        self.car_manager.update()
    
    def update_fps_counter(self, delta_time):
        """ Used by scheduling to update the fps """
        self.fps_text = "FPS: " + str(round(1/g.delta))

    def on_draw(self):
        """ Will be called everytime the screen is drawn """

        # Clear the screen and start drawing
        arcade.start_render()

        # Draws the grid
        self.grid.draw_grid()

        # Draw the track manager
        self.track_manager.on_draw()

        self.car_manager.on_draw()

        # Draws the fps counter
        self.ui.set_text(self.fps_text)
        self.ui.on_draw()

        self.cam.update_viewport()

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, buttons: int, modifiers: int):
        """ Updates the camera if dragged. """
        if buttons == arcade.MOUSE_BUTTON_RIGHT:
            self.cam.handle_pan(dx, dy)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ Nothing yet """

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        """ Controls the zoom """
        self.cam.handle_zoom(x, y, scroll_y)


def run_game():
    game = Main()
    arcade.run()