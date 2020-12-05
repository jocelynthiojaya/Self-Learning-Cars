import cargame as game
import cargame.globals as g
import json
from os import path

# Configuration file name
conf_file = "conf.json"
CONF_PATH = path.join(path.dirname(path.abspath(__file__)), conf_file)

# Load the configuration if exists 😊
if path.exists(CONF_PATH) and path.isfile(CONF_PATH):
    with open(CONF_PATH, "r") as file:

        # Load and convert to json object
        j_file = json.load(file)

        # If the key does not exist in the json, just keep the default value.
        # Otherwise, replace it with the user configured one.
        for key in j_file:
            if key in g.conf:
                g.conf[key] = j_file[key]

else:
    # If file does not exist, then create it based on the default values.
    with open(CONF_PATH, "w+") as file:
        file.write(json.dumps(g.conf))

# Run the game
game.run_game()