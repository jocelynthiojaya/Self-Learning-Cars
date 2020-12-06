import arcade
from cargame.camera import Camera, Grid
from cargame.ui import GameUI
from cargame.car import Car, CarManager
from cargame.track import Track, TrackManager
from cargame.globals import conf
import cargame.util as util

WINDOW_TITLE = "Self Learning Cars"

# Class for the main game window
class Main(arcade.Window):
    
    def __init__(self):
        """ Initialize the window """
        # Create the object
        super().__init__(conf["screen_width"], conf["screen_height"], WINDOW_TITLE)

        # Set background color as white
        arcade.set_background_color(arcade.color.WHITE)
        # Camera object
        self.cam = Camera(
            conf["c_bound_left"],
            conf["c_bound_bottom"],
            conf["c_bound_right"],
            conf["c_bound_top"]
        )
        self.grid = Grid(self.cam)
        self.ui = GameUI(self.cam)

        self.fps = 0
        self.fps_text = ""

        self.car_manager = CarManager()
        self.car = Car(200, 200)
        self.track = Track([
            [150, 150],
            [500, 150],
            [700, 300],
            [1100, 300],
            [1100, 400],
            [650, 400],
            [450, 250],
            [150, 250],
            [150, 150]
        ])

        # Schedule fps update
        arcade.schedule(self.update_fps_counter, 0.5)

    def update(self, delta_time: float):
        """ Will be run every frame """
        self.cam.on_start_update()
        self.fps = 1/delta_time

        self.car.move_forward(util.delta_unit(100, delta_time))
        self.car.rotate(self.car.direction + util.delta_unit(30, delta_time))
    
    def update_fps_counter(self, delta_time):
        """ Used by scheduling to update the fps """
        self.fps_text = "FPS: " + str(round(self.fps))

    def on_draw(self):
        """ Will be called everytime the screen is drawn """

        # Clear the screen and start drawing
        arcade.start_render()

        # Draws the grid
        self.grid.draw_grid()

        self.track.on_draw()

        self.car.on_draw()

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