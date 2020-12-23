import arcade
from cargame.camera import Camera
import cargame.util as util
import cargame.globals as g
from time import time

Y_UI_CENTER = 75

UI_WIDTH = 600
UI_HEIGHT = 100

TEXT_WIDTH = 180
TEXT_HEIGHT = 85
TEXT_MARGIN = 5

class Button():

    width = 50
    height = 70
    
    # How many seconds is the button down after pressing
    pressed_length = 0.1

    def __init__(self, text, x, y, color, pressed_color, function, icon=None, variety=0):
        """ Create a new button with or without a sprite.
        :text: display string text
        :x: x coordinates relative to the viewport
        :y: y coordinates relative to the viewport
        :color: Button color
        :icon: path to file of the icon of the button
        :variety: 0-1, the variety of the button """
        # Resize the sprite to 64x64
        self.sprite = arcade.Sprite(icon, image_width=32, image_height=32) if icon!=None else None
        self.set_coords(x - Button.width/2,
        y - Button.height/2)

        self.text = text
        self.color = color
        self.pressed_color = pressed_color

        # Marker variable to indicate when button is pressed for animations.
        self.down_left = 0

        self.func = function

    def button_pressed(self):
        """ When the button is pressed, this function triggers """
        self.down_left = Button.pressed_length
        self.func()

    def set_coords(self, x, y):
        self.x = x
        self.y = y
        # Relative distances to the center of the sprite
        self.scenter_x = x + Button.width/2
        self.scenter_y = y + Button.height - 16 - 9

    def on_draw(self, camx, camy):
        """ Needs the camx and camy coordinates to draw it relatively """
        if self.down_left <= 0:
            arcade.draw_rectangle_filled(camx + self.x + Button.width/2, camy + self.y + Button.height/2, Button.width, Button.height, self.color)
        else:
            arcade.draw_rectangle_filled(camx + self.x + Button.width/2, camy + self.y + Button.height/2, Button.width, Button.height, self.pressed_color)
            self.down_left -= g.delta
        arcade.draw_text(self.text, camx + self.x, camy + self.y + 3, (255, 255, 255), 10, Button.width, "center")
        if self.sprite:
            self.sprite.center_x = camx + self.scenter_x
            self.sprite.center_y = camy + self.scenter_y
            self.sprite.draw()

class GameUI():

    def __init__(self, camera):
        """ Inits the UI using the camera as the reference """
        self.cam: Camera = camera
        self.ui_text = ""

        # The buttons inside the ui
        self.buttons = []

    def set_text(self, text):
        """ Sets the new UI Text """
        self.ui_text = text

    def append_text(self, text):
        """ Appends to the new UI Text """
        self.ui_text += text

    def on_click(self, x, y, button):
        """ Trigger click for the buttons """
        # Will return true if a the click is in an UI element
        click_ui = False
        if (x > g.conf["screen_width"]/2 - UI_WIDTH/2 and x < g.conf["screen_width"]/2 + UI_WIDTH/2 and
            y > Y_UI_CENTER - UI_HEIGHT/2 and y < Y_UI_CENTER + UI_HEIGHT/2):
            click_ui = True
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Check every button whether the mouse is within the button box.
            for btn in self.buttons:
                if (x > btn.x and x < btn.x+Button.width and
                    y > btn.y and y < btn.y+Button.height):
                    # Trigger the function.
                    btn.button_pressed()
                    click_ui = True
                    break
        return click_ui

    def on_draw(self):
        
        # start = time()
        # Only draws when the camera has 1x magnification.
        camx, _, camy, _ = arcade.get_viewport()
        if self.cam.zoom == 1:
            # Base UI Rectangle
            util.draw_rectangle_rounded(camx + g.conf["screen_width"]/2, camy + Y_UI_CENTER, UI_WIDTH, UI_HEIGHT, 15, (240, 240, 240))
            
            # Draw the text container and text
            text_rect_x = camx + g.conf["screen_width"]/2 + UI_WIDTH/2 - TEXT_WIDTH/2 - 10
            text_rect_y = camy + Y_UI_CENTER
            arcade.draw_rectangle_outline(text_rect_x, text_rect_y, TEXT_WIDTH, TEXT_HEIGHT, (50, 50, 50))
            arcade.draw_rectangle_filled(text_rect_x, text_rect_y, TEXT_WIDTH, TEXT_HEIGHT, (255, 255, 255))

            arcade.draw_text(self.ui_text, text_rect_x - TEXT_WIDTH/2 + TEXT_MARGIN, text_rect_y - TEXT_HEIGHT/2 + TEXT_MARGIN, (10, 10, 10), 12, TEXT_WIDTH - TEXT_MARGIN*2, font_name="courbd")

            # Draw the buttons
            for button in self.buttons:
                button.on_draw(camx, camy)
            
        else:
            arcade.draw_text("Press ` to reset zoom.", camx + 10, camy + 10, (10, 10, 10), 12, font_name="courbd")

        # print("gui_draw_time: {}ms".format(round((time() - start) * 1000, 2)))