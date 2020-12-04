import arcade
from cargame.camera import Camera
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

    def on_draw(self):
        """ Will be called everytime the screen is drawn """

        # Clear the screen and start drawing
        arcade.start_render()

        # Draw a blue circle
        arcade.draw_circle_filled(
            400, 300, 300, arcade.color.BLUE
        )
        self.cam.update_viewport()

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, buttons: int, modifiers: int):
        """ Updates the camera if dragged. """
        if buttons == arcade.MOUSE_BUTTON_RIGHT:
            self.cam.move_camera_pos(-dx, -dy)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ Nothing yet """


def run_game():
    game = Main()
    arcade.run()