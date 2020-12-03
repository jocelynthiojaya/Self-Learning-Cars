import cargame as g
import json
from os import path

# Configuration file name
conf_file = "conf.json"
CONF_PATH = path.join(path.dirname(path.abspath(__file__)), conf_file)

# Load the configuration if exists 😊
if path.exists(CONF_PATH) and path.isfile(CONF_PATH):
    with open(CONF_PATH) as file:

        # Make the json object
        j_file = json.load(file)

        # Load everything
        g.screen_width = j_file.get("window_width", g.screen_width)
        g.screen_height = j_file.get("window_height", g.screen_height)

# Run the game
g.run_game()