from cargame.camera import Camera, Grid
from cargame.ui import GameUI
from cargame.car import Car, CarManager
from cargame.track import TrackManager
import cargame.globals as g
import cargame.util as util
import arcade

class MainGame:

    def __init__(self):
        """
        TODO:
        - Register buttons from here
        - Store every class here
        - Connect functions from here
        """
        # Camera object
        self.cam = Camera(
            g.conf["c_bound_left"],
            g.conf["c_bound_bottom"],
            g.conf["c_bound_right"],
            g.conf["c_bound_top"]
        )
        # Grid and UI Object
        self.grid = Grid(self.cam)
        self.ui = GameUI(self.cam)

        # Text for showing FPS
        self.fps_text = ""

        # Add the new track manager
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

        # Create the new car manager
        self.car_manager = CarManager(self.track_manager, 200, 200, 0, 20)

        # State of the game. 0 is for build mode, 1 is for simulation mode
        self.state = 0

        # Schedule fps update
        arcade.schedule(self.update_fps_counter, 0.5)

    def update(self, delta):
        """ Will be run every frame """
        # Update the camera at the start
        self.cam.on_start_update()
        
        # Updates the delta time on globals
        g.delta = delta

        self.car_manager.update()
        g.ui_text += self.fps_text
        self.ui.set_text(g.ui_text.strip())

    def on_draw(self):
        # Clear the screen and start drawing
        arcade.start_render()

        # Draws the grid
        self.grid.draw_grid()

        # Draw the track manager
        self.track_manager.on_draw()

        self.car_manager.on_draw()

        # Draws the fps counter
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

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.GRAVE:
            self.cam.update_zoom(1, g.conf["screen_width"]/2, g.conf["screen_height"]/2)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.ui.on_click(x, y, button)

    def update_fps_counter(self, delta_time):
        """ Used by scheduling to update the fps """
        self.fps_text = "FPS: {}\n".format(round(1/g.delta))