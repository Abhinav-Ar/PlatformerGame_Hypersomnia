import arcade


PLAYER_SCALING = 2

# Index of textures, first element faces left, second faces right
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1


class Player(arcade.Sprite):
    hit_box_algorithm = "Simple"

    def __init__(self, tex_in):
        super().__init__()

        self.scale = PLAYER_SCALING
        self.textures = []

        # load left and right facing textures
        # left (original)
        texture = arcade.load_texture(tex_in)
        self.textures.append(texture)
        # right (flipped)
        texture = arcade.load_texture(tex_in,
                                      flipped_horizontally=True)
        self.textures.append(texture)

        # By default, face right.
        self.texture = texture

    def face_right(self):
        self.texture = self.textures[TEXTURE_RIGHT]

    def face_left(self):
        self.texture = self.textures[TEXTURE_LEFT]
