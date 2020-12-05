import arcade
from cargame.camera import Camera, Grid
from cargame.ui import GameUI
from cargame.car import Car, CarManager
import cargame.globals as g

WINDOW_TITLE = "Self Learning Cars"

# Class for the main game window
class Main(arcade.Window):
    
    def __init__(self):
        """ Initialize the window """
        # Create the object
        super().__init__(g.screen_width, g.screen_height, WINDOW_TITLE)

        # Set background color as white
        arcade.set_background_color(arcade.color.WHITE)
        # Camera object
        self.cam = Camera()
        self.grid = Grid(self.cam)
        self.ui = GameUI(self.cam)
        self.car_manager = CarManager()
        self.car = Car(200, 200)
        self.fps = 0
        self.fps_text = ""

        # Schedule fps update
        arcade.schedule(self.update_fps_counter, 0.5)

    def update(self, delta_time: float):
        """ Will be run every frame """
        self.cam.on_start_update()
        self.fps = 1/delta_time
    
    def update_fps_counter(self, delta_time):
        """ Used by scheduling to update the fps """
        self.fps_text = "FPS: " + str(round(self.fps))

    def on_draw(self):
        """ Will be called everytime the screen is drawn """

        # Clear the screen and start drawing
        arcade.start_render()

        # Draw a blue circle
        arcade.draw_circle_filled(400, 300, 100, arcade.color.BLUE)

        # Draws the grid
        self.grid.draw_grid()

        self.car.rotate(self.car.direction + 1)
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