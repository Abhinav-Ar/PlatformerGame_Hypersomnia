import arcade
from player import Player
from screen import Screen

# SCREEN CONSTANTS
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Hypersomnia"
# ======================================

# OBJECT CONSTANTS
TILE_SCALING = 0.5
PLAYER_SPEED = 8.0
PLAYER_JUMP_SPEED = 20.0
GRAVITY = 1.0
BLOCK_SIZE = 32
# ======================================


def wall(xVal, topYVal, bottomYVal):
    wall = []
    for i in range(topYVal, bottomYVal, -32):
        wall.append([xVal, i])
    return wall


def floor(yVal, startXVal, endXVal):
    wall = []
    for i in range(startXVal, endXVal, 32):
        wall.append([i, yVal])
    return wall


# LEVELS / SCREENS
tmp = list(range(0, SCREEN_WIDTH, BLOCK_SIZE))

flo = [*floor(32, 0, 1000)]
roof = [*floor(480, 0, 1000)]

tempf = [*flo]
tempf.pop(7)
tempf.pop(7)
tempf.pop(7)
tempf.pop(7)

tempf.pop(10)
tempf.pop(10)
tempf.pop(10)

tempf.pop(15)
tempf.pop(15)
tempf.pop(15)


screens = [
    Screen([*flo, [256, 64], [512, 64], [768, 64], *roof], 50, 200),
    Screen([*tempf, *roof], 50, 200),
    Screen([*flo, *roof], 50, 200),  # include an enemy here
    Screen([*floor(32, 0, 100), [256, 64], *floor(256, 512, 544),
           *floor(300, 768, 832), *floor(200, 880, 990), *roof], 50, 200),
    Screen([*roof, [0, 300], [32, 300], [64, 300],
           [64, 175], [400, 200], *wall(278, 370, 0),
           *wall(500, 480, 100), *floor(32, 384, 732), *wall(700, 380, 32),
           [670, 130], [525, 260], [670, 300]], 30, 350),
    Screen([*roof, *flo], 50, 200),
    Screen([*roof, *flo], 50, 200),

]

enemies = [
    Screen([], 1, 1),
    Screen([], 1, 1),
    Screen([[500, 105]], 1, 1),
    Screen([[528, 321], [803, 365]], 1, 1),
    Screen([], 1, 1),
    Screen([], 1, 1),
    Screen([], 1, 1),
]

s = arcade.Sound("./assets/sounds/theme.wav")


class MainMenu(arcade.View):
    def on_show_view(self):
        arcade.set_background_color((255, 255, 255))
        return
        arcade.set_background_color("assets/blocks/background.png")

    def on_draw(self):
        self.clear()
        font = "04b_19"
        arcade.draw_text("HYPERSOMNIA", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 10, (44, 44, 44),
                         font_size=100, font_name=font, anchor_x="center", anchor_y="baseline")
        arcade.draw_text("CLICK TO BEGIN", SCREEN_WIDTH / 2, SCREEN_HEIGHT/2 - 40, (40,
                         40, 40), font_size=30, font_name=font, anchor_x="center", anchor_y="baseline")

    def on_mouse_press(self, x, y, _button, _modifiers):
        sound = arcade.Sound("./assets/sounds/gui.wav")
        sound.play(volume=0.5)
        sp = arcade.Sound("./assets/sounds/theme.wav")
        sp.play(loop=True, volume=0.1)
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)


class MyGame(arcade.View):

    def __init__(self):

        # set up the window
        super().__init__()
        self.scene = None
        self.player_sprite = None
        self.background = None
        self.physics_engine = None
        self.level = 0
        self.facing_left = False

    def setup(self):
        self.clear()
        # create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.blocks_list = arcade.SpriteList(use_spatial_hash=True)

        # initialize Scene and sprite lists
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Background")
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("blocks", use_spatial_hash=True)
        self.scene.add_sprite_list("Enemy")

        self.scene.add_sprite_list("proj")

        # set up the player
        self.player_sprite = Player("assets/sprites/player.png")
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        # CREATING SCENE

        current_screen = screens[self.level]
        current_enemyList = enemies[self.level]

        # change the background for each floor
        if self.level < 3:
            self.final_background = arcade.Sprite(
                "assets/blocks/FinalBackground.png")
            self.final_background.center_x = SCREEN_HEIGHT / 2 + 250
            self.final_background.center_y = SCREEN_HEIGHT / 2
            self.scene.add_sprite("Background", self.final_background)
        elif self.level < 6:
            self.final_background = arcade.Sprite(
                "assets/blocks/Background#2.jpeg")
            self.final_background.center_x = SCREEN_HEIGHT / 2 + 250
            self.final_background.center_y = SCREEN_HEIGHT / 2
            self.scene.add_sprite("Background", self.final_background)
        else:
            self.final_background = arcade.Sprite(
                "assets/blocks/Background#3.jpeg")
            self.final_background.center_x = SCREEN_HEIGHT / 2 + 250
            self.final_background.center_y = SCREEN_HEIGHT / 2
            self.scene.add_sprite("Background", self.final_background)

        # place blocks down
        for coordinate in current_screen.coordinate_map:
            block = arcade.Sprite(
                "assets/blocks/block.png", TILE_SCALING
            )
            block.position = coordinate
            self.scene.add_sprite("Blocks", block)

        # placing the enemies down
        for coordinate in current_enemyList.coordinate_map:
            if self.level < 3:
                enemy = arcade.Sprite(
                    "assets/sprites/Enemy1Rescale.png", TILE_SCALING
                )
            elif self.level < 6:
                enemy = arcade.Sprite(
                    "assets/sprites/Enemy2Rescale.png", TILE_SCALING
                )
            else:
                enemy = enemy(arcade.Sprite(
                    "assets/sprites/Enemy#3.png", TILE_SCALING
                ))
            enemy.position = coordinate
            self.scene.add_sprite("Enemy", enemy)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Blocks"]
        )

    # render
    def on_draw(self):
        self.clear()
        # draw sprites
        self.scene.draw(
            pixelated=True
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            so = arcade.Sound("./assets/sounds/jump.wav")
            arcade.play_sound(so)
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_SPEED
            self.player_sprite.face_left()
            self.facing_left = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_SPEED
            self.player_sprite.face_right()
            self.facing_left = True
        elif key == arcade.key.F:
            so = arcade.Sound("./assets/sounds/throw.wav")
            arcade.play_sound(so)
            # fire projectile
            proj = arcade.Sprite(
                "./assets/sprites/projectile_a.png", scale=1.5)
            proj.change_angle = -10
            if self.facing_left:
                proj.change_x = 10
            else:
                proj.change_x = -10
            proj.center_x = self.player_sprite.center_x
            proj.center_y = self.player_sprite.center_y
            self.scene.add_sprite("proj", proj)
        elif key == arcade.key.Q:
            print(self.player_sprite.center_x)
            print(self.player_sprite.center_y)
        elif key == arcade.key.P:
            self.player_sprite.center_x = 1000

    def on_key_release(self, key, modifiers):
        # called when the user releases a key.

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        # movement and game logic
        try:
            self.scene.update(["proj"])
            if self.scene.proj >= SCREEN_WIDTH - 32:
                self.scene.remove_sprite_list_by_name("proj")
        except:
            True
        # check if the player has hit the bottom, and send them back to the beginning of the screen
        if self.player_sprite.center_y < 0:
            current_screen = screens[self.level]

            self.player_sprite.center_x = current_screen.x
            self.player_sprite.center_y = current_screen.y

        # move the player with the physics engine
        self.physics_engine.update()

        # check right wall
        if self.player_sprite.center_x >= SCREEN_WIDTH - 32:
            # send to left side of screen
            temp = self.player_sprite.center_y
            self.level += 1
            # CHANGE THE LEVEL
            self.setup()
            current_screen = screens[self.level]

            self.player_sprite.center_x = current_screen.x
            self.player_sprite.center_y = current_screen.y


def main():
    # Main function
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
