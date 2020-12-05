import arcade

class Track:

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

    def __init__(self):
        """ Contains all the track objects and handles them """

    def update(self):
        """ Updates every frame """

    def on_draw(self):
        """ Draw """
