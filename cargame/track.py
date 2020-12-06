import arcade
import cargame.globals as g
import cargame.collision as col

class Track:
    """ OBSOLETE """

    track_width = 5

    def __init__(self, polygon=[]):
        """ Basically, a track is a polygon. All of the points are tracked
        so that the collisions can be calculated. """

        # Polygon of the track
        self.polygon = polygon

    def update(self):
        """ Updates every frame """

    def on_draw(self):
        """ Draw """

        # Draws the track
        arcade.draw_line_strip(self.polygon, (20, 20, 20), 5)

class TrackManager:

    track_width = 5

    def __init__(self):
        """ Contains all the track objects and handles them """
        # Dictionary of coordinates with tracks values
        self.coll_dict = {}

        # Track is a list of lists.
        # The nested list is [x1, y1, x2, y2]
        self.tracks = []

        # All the tracks, cache so that it's not heavy
        self.track_poly = []

    def add_track(self, track):
        """ Add a new track to the track manager, and constructs the collisions.
        :track: array of points of the track """

        # Add the points to the track
        for i in range(len(track) - 1):
            self.tracks.append([track[i][0], track[i][1], track[i + 1][0], track[i + 1][1]])

        # Reconstruct everything
        self.reconstruct_collisions()
        self.reconstruct_track_poly()

    def reconstruct_collisions(self):
        """ Reconstructs all the static collisions """
        
        # Clear the dictionary
        self.coll_dict = {}

        x1 = x2 = y1 = y2 = 0
        # Get all the true bounding box value, and insert it into the dictionary.
        for lines in self.tracks:
            # Get proper bounding box
            if lines[0] < lines[2]:
                x1 = lines[0]
                x2 = lines[2]
            else:
                x1 = lines[2]
                x2 = lines[0]
            if lines[1] < lines[3]:
                y1 = lines[1]
                y2 = lines[3]
            else:
                y1 = lines[3]
                y2 = lines[1]
            
            # Gets the range of the bounding box in the collision grid, and insert it
            # to the dictionary.
            size = g.conf["col_grid_size"]
            a = 0
            for i in range(int(x1 // size), int(x2 // size + 1)):
                for j in range(int(y1 // size), int(y2 // size + 1)):
                    # Detect whether the track line is intersecting with the collision grid.
                    # This is so that one long line does not take the whole i*j grid.
                    if col.linerect(x1, y1, x2, y2, i*size, j*size, (i+1)*size, (j+1)*size):
                        # Insert them
                        a += 1
                        if (i, j) not in self.coll_dict:
                            self.coll_dict[(i, j)] = [lines]
                        else:
                            self.coll_dict[(i, j)].append(lines)

    def reconstruct_track_poly(self):
        """ Reconstruct the cache for track poly """
        self.track_poly = []
        for lines in self.tracks:
            self.track_poly.append([lines[0], lines[1]])
            self.track_poly.append([lines[2], lines[3]])

    def update(self):
        """ Updates every frame """

    def draw_debug_squares(self):
        """ Draws the collision squares tracked by this object for debugging purposes """
        
        size = g.conf["col_grid_size"]
        for grid in self.coll_dict:
            for _ in range(len(self.coll_dict[grid])):
                arcade.draw_rectangle_filled(grid[0]*size + size/2, grid[1]*size + size/2, size, size, (255, 0, 0, 50))

    def on_draw(self):
        """ Draw """
        arcade.draw_lines(self.track_poly, (20, 20, 20), TrackManager.track_width)
        self.draw_debug_squares()