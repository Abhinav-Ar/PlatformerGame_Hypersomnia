import arcade


class Screen:
    def __init__(self, coordinate_map, theX, theY):
        self.coordinate_map = coordinate_map  # list of blocks / where they are
        self.x = theX
        self.y = theY
