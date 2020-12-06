import arcade
import cargame.globals as g

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

    def reconstruct_track_poly(self):
        """ Reconstruct the cache for track poly """
        self.track_poly = []
        for lines in self.tracks:
            self.track_poly.append([lines[0], lines[1]])
            self.track_poly.append([lines[2], lines[3]])

    def update(self):
        """ Updates every frame """

    def on_draw(self):
        """ Draw """
        arcade.draw_lines(self.track_poly, (20, 20, 20), TrackManager.track_width)