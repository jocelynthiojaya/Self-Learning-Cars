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
        self.ui = self.build_ui

        # Text for showing FPS
        self.fps_text = ""

        # Add the new track manager
        self.track_manager = TrackManager()
        
        # Car spawner location
        self.car_spawn = [0, 0]

        # Mouse pos
        self.mx = 0
        self.my = 0

        # State of the game.
        # 0 = build mode
        # 1 = add wall mode
        # 2 = delete wall mode
        # 3 = set car spawn mode
        # 4 = simulation mode
        self.state = 0

        self.car_manager = CarManager(self.track_manager)

        # Temporary road when in add wall mode
        # These stores an array of points
        self.temp_road = []

        # Add buttons to the UI here
        self.sim_ui.buttons = [
            ui.Button("Play", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 50, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), lambda : self.pause_sim(False), "./cargame/sprites/play.png"),
            ui.Button("Pause", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 120, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), lambda : self.pause_sim(True), "./cargame/sprites/pause.png"),
            ui.Button("Skip", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 190, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), lambda : print("Bruh")),
            ui.Button("Exit Sim", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 260, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), self.switch_build_mode),
            ui.Button("Save Car", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 330, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), lambda : print("Bruh"))
        ]

        # There are 2 build ui buttons. This is so that the user can scroll through a button list.
        self.build_button1 = [
            ui.Button("Run Sim!", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 50, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), self.switch_run_sim, "./cargame/sprites/play.png"),
            ui.Button("Wall+", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 120, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), self.switch_add_wall_mode, "./cargame/sprites/pause.png"),
            ui.Button("Wall-", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 190, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), self.switch_del_wall_mode),
            ui.Button("Set Spawn", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 260, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), self.switch_set_car_spawn),
            ui.Button("Next>", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 330, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), self.switch_ui)
        ]

        self.build_button2 = [
            ui.Button("<Back", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 50, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), self.switch_ui, "./cargame/sprites/play.png"),
            ui.Button("Save Track", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 120, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), lambda : self.pause_sim(True), "./cargame/sprites/pause.png"),
            ui.Button("Load Track", g.conf["screen_width"]/2 - ui.UI_WIDTH/2 + 190, ui.Y_UI_CENTER, (245, 71, 71), (225, 51, 51), lambda : print("Bruh"))
        ]

        # Set the build ui buttons
        self.build_ui.buttons = self.build_button1

        # Schedule fps update
        arcade.schedule(self.update_fps_counter, 0.5)

    def pause_sim(self, state):
        self.car_manager.set_paused(state)

    def switch_ui(self):
        # Switch the button list
        self.build_ui.buttons = self.build_button1 if self.build_ui.buttons == self.build_button2 else self.build_button2

    def switch_build_mode(self):
        # Return to normal build mode
        self.temp_road = []
        self.state = 0
        
        # Reenable zoom
        self.cam.set_can_zoom(True)

        # Set the ui to build
        self.ui = self.build_ui

    def switch_add_wall_mode(self):
        # Helper function to change the game state to wall mode, disable zoom.
        self.state = 1
        self.cam.set_can_zoom(False)

    def switch_del_wall_mode(self):
        # Mode when deleting wall, disable zoom
        self.state = 2
        self.cam.set_can_zoom(False)
    
    def switch_set_car_spawn(self):
        # Set the mode for setting car spawn
        self.state = 3
        self.cam.set_can_zoom(True)

    def switch_run_sim(self):
        # Run the simulation!
        self.state = 4
        self.car_manager = CarManager(self.track_manager, *self.car_spawn, count=20)

        # Enable zoom
        self.cam.set_can_zoom(True)

        # Change UI
        self.ui = self.sim_ui

    def update(self, delta):
        """ Will be run every frame """
        # Update the camera at the start
        self.cam.on_start_update()
        
        # Updates the delta time on globals
        g.delta = delta

        g.ui_text += self.fps_text
        self.ui.set_text(g.ui_text.strip())

        # Update the cars if state is run simulation
        if self.state == 4:
            self.car_manager.update()

    def on_draw(self):
        # Clear the screen and start drawing
        arcade.start_render()

        # Draws the grid
        self.grid.draw_grid()

        # Draw the track manager
        self.track_manager.on_draw()

        # Draw the car spawn point
        arcade.draw_arc_filled(*self.car_spawn, 32, 32, (5, 5, 5), -60, 240)

        # Draws all the car if simulation is runned
        if self.state == 4:
            self.car_manager.on_draw()

        camx, _, camy, _ = arcade.get_viewport()

        if self.state == 1:
            # Draw instruction
            arcade.draw_text("Press [LEFT MOUSE] to add road, [ENTER] to add the roads, [ESC] to quit this mode.", camx + 5, camy + 5, (0, 0, 0))
            
            # Draw the temporary road
            arcade.draw_line_strip(self.temp_road, (0, 120, 0), 5)

            # Draw the last road leading to the mouse
            if len(self.temp_road) > 0:
                arcade.draw_line(*self.temp_road[-1], self.mx + camx, self.my + camy, (0, 0, 120), 5)
        
        if self.state == 2:
            # Instruction
            arcade.draw_text("[LEFT MOUSE] on the walls to delete them, [ESC] to quit this mode.", camx + 5, camy + 5, (0, 0, 0))

        if self.state == 3:
            # Instruction
            arcade.draw_text("[LEFT MOUSE] to set where the cars will spawn, [ESC] to quit this mode.", camx + 5, camy + 5, (0, 0, 0))

        # Draws the UI, and update viewport
        self.ui.on_draw()
        self.cam.update_viewport()

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, buttons: int, modifiers: int):
        """ Updates the camera if dragged. """
        if buttons == arcade.MOUSE_BUTTON_RIGHT:
            self.cam.handle_pan(dx, dy)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ Nothing yet """
        self.mx = x
        self.my = y

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        """ Controls the zoom """
        self.cam.handle_zoom(x, y, scroll_y)

    def on_key_press(self, symbol: int, modifiers: int):

        # Reset zoom when grave is pressed (`)
        if symbol == arcade.key.GRAVE:
            self.cam.reset_zoom()

        if self.state == 1:
            if symbol == arcade.key.ESCAPE:
                self.switch_build_mode()
            elif symbol == arcade.key.ENTER:
                # Insert all the temp road into the road manager, then clear it.
                self.track_manager.add_track(self.temp_road)
                self.temp_road = []

        if self.state == 2:
            if symbol == arcade.key.ESCAPE:
                self.switch_build_mode()

        if self.state == 3:
            if symbol == arcade.key.ESCAPE:
                self.switch_build_mode()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Handle UI mouse click, and
        # If the mouse click is not in the GUI element
        camx, _, camy, _ = arcade.get_viewport()
        if not self.ui.on_click(x, y, button):
            if self.state == 1:
                if button == arcade.MOUSE_BUTTON_LEFT:
                    # Add a new road to the temp_road
                    self.temp_road.append([camx + x, camy + y])

            if self.state == 2:
                if button == arcade.MOUSE_BUTTON_LEFT:
                    # Delete the road intersecting within the cursor.
                    self.track_manager.del_track_at_pos(camx + x, camy + y, 5)

            if self.state == 3:
                if button == arcade.MOUSE_BUTTON_LEFT:
                    # Delete the road intersecting within the cursor.
                    self.car_spawn = [camx + x, camy + y]
                    self.switch_build_mode()

        # Update mouse pos
        self.mx = x
        self.my = y

    def update_fps_counter(self, delta_time):
        """ Used by scheduling to update the fps """
        self.fps_text = "FPS: {}\n".format(round(1/g.delta))