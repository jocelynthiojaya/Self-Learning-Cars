from cargame.camera import Camera, Grid
import cargame.ui as ui
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
        - Buttons function registered function belongs here.
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

        # Create 2 UIs. For build mode and simulation mode
        self.build_ui = ui.GameUI(self.cam)
        self.sim_ui = ui.GameUI(self.cam)
        self.ui = self.sim_ui

        # Text for showing FPS
        self.fps_text = ""

        # Add the new track manager
        self.track_manager = TrackManager()

        # State of the game. 0 is for build mode, 1 is for simulation mode
        self.state = 0

        self.car_manager = CarManager(self.track_manager)

        # Add buttons to the UI here
        self.sim_ui.buttons = [
            ui.Button("Play", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 50, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), lambda : self.car_manager.set_paused(False), "./cargame/sprites/play.png"),
            ui.Button("Pause", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 120, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), lambda : self.car_manager.set_paused(True), "./cargame/sprites/pause.png"),
            ui.Button("Skip", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 190, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), lambda : print("Bruh")),
            ui.Button("Exit Sim", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 260, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), lambda : print("Bruh")),
            ui.Button("Save Car", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 330, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), lambda : print("Bruh"))
        ]

        # Schedule fps update
        arcade.schedule(self.update_fps_counter, 0.5)

    def update(self, delta):
        """ Will be run every frame """
        # Update the camera at the start
        self.cam.on_start_update()
        
        # Updates the delta time on globals
        g.delta = delta

        g.ui_text += self.fps_text
        self.ui.set_text(g.ui_text.strip())

    def on_draw(self):
        # Clear the screen and start drawing
        arcade.start_render()

        # Draws the grid
        self.grid.draw_grid()

        # Draw the track manager
        self.track_manager.on_draw()

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