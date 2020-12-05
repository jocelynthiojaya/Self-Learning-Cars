import arcade
from cargame.camera import Camera
import cargame.util as util
from cargame.globals import conf

Y_UI_CENTER = 75

UI_WIDTH = 600
UI_HEIGHT = 100

TEXT_WIDTH = 180
TEXT_HEIGHT = 85
TEXT_MARGIN = 5

class GameUI():

    def __init__(self, camera):
        """ Inits the UI using the camera as the reference """
        self.cam: Camera = camera
        self.ui_text = ""

    def set_text(self, text):
        """ Sets the new UI Text """
        self.ui_text = text

    def on_draw(self):

        camx, _, camy, _ = arcade.get_viewport()
        # Base UI Rectangle
        util.draw_rectangle_rounded(camx + conf["screen_width"]/2, camy + Y_UI_CENTER, UI_WIDTH, UI_HEIGHT, 15, (230, 230, 230))
        
        # Draw the text container and text
        text_rect_x = camx + conf["screen_width"]/2 + UI_WIDTH/2 - TEXT_WIDTH/2 - 10
        text_rect_y = camy + Y_UI_CENTER
        arcade.draw_rectangle_outline(text_rect_x, text_rect_y, TEXT_WIDTH, TEXT_HEIGHT, (50, 50, 50))
        arcade.draw_rectangle_filled(text_rect_x, text_rect_y, TEXT_WIDTH, TEXT_HEIGHT, (255, 255, 255))

        arcade.draw_text(self.ui_text, text_rect_x - TEXT_WIDTH/2 + TEXT_MARGIN, text_rect_y - TEXT_HEIGHT/2 + TEXT_MARGIN, (10, 10, 10), 12, TEXT_WIDTH - TEXT_MARGIN*2, font_name="courbd")