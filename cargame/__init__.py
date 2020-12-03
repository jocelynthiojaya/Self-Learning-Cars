import arcade

screen_width = 800
screen_height = 600
WINDOW_TITLE = "Self Learning Cars"

# Class for the main game window
class Main(arcade.Window):
    
    def __init__(self):
        """ Initialize the window """
        # Create the object
        super().__init__(screen_width, screen_height, WINDOW_TITLE)

        # Set background color as white
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """ Will be called everytime the screen is drawn """

        # Clear the screen and start drawing
        arcade.start_render()

        # Draw a blue circle
        arcade.draw_circle_filled(
            400, 300, 300, arcade.color.BLUE
        )


def run_game():
    game = Main()
    arcade.run()