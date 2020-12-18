import arcade
from cargame.game_manager import MainGame
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
        
        # Create the main game manager
        self.game = MainGame()

    def update(self, delta_time: float):
        """ Will be run every frame """
        g.ui_text = ""
        self.game.update(delta_time)

    def on_draw(self):
        """ Will be called everytime the screen is drawn """
        self.game.on_draw()

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, buttons: int, modifiers: int):
        """ Updates the camera if dragged. """
        self.game.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ Nothing yet """
        self.game.on_mouse_motion(x, y, dx, dy)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        """ Controls the zoom """
        self.game.on_mouse_scroll(x, y, scroll_x, scroll_y)

    def on_key_press(self, symbol: int, modifiers: int):
        self.game.on_key_press(symbol, modifiers)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.game.on_mouse_press(x, y, button, modifiers)


def run_game():
    game = Main()
    arcade.run()