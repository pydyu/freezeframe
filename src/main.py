import pygame
import sys
import os
import math
import random
import asyncio

# -----------------------------
# CONFIG
# -----------------------------
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 1000

# Logical/world tile size
TILE_SIZE = 64

# Visual size of snowy wall tiles
SNOW_TILE_SIZE = 183

# Visual size of water tiles
WATER_TILE_SIZE = 183

# Extra padding around the map so oversized tiles are never cut off
WORLD_PADDING = max(0, (max(SNOW_TILE_SIZE, WATER_TILE_SIZE) - TILE_SIZE) // 2)

# Border size grows with snow tile size
BORDER_SIZE = SNOW_TILE_SIZE // 2

LEVELS = [
    [
        "######################",
        "#         E    W   G #",
        "#   #######    W     #",
        "#   #     #    W     #",
        "# P #     #######    #",
        "#   #              ###",
        "#   ######     E     #",
        "#   W  C #           #",
        "#   W  C #   ####    #",
        "#   W  C # C         #",
        "######################",
    ],
    [
        "######################",
        "#P     W      E      #",
        "# #### W ####### ### #",
        "#    # W    C        #",
        "## # # ####### ###   #",
        "#  # #         #     #",
        "#  # #####     #  E  #",
        "#  #     #  C  #     #",
        "#  ##### # ####### G #",
        "#        #           #",
        "######################",
    ],
    [
        "######################",
        "#P   C    ####    G  #",
        "# ######  #  #  W##  #",
        "#      #  #  #  W    #",
        "# E    #  #  ######  #",
        "###### #  #          #",
        "#    # #  ####### ## #",
        "# W  # #     C    ##E#",
        "# W  # ####### ####  #",
        "#    #               #",
        "######################",
    ],
    [
        "######################",
        "#P      E      ## G  #",
        "# ####### ## #  # ####",
        "#   C     ## #  #    #",
        "### ##### ## #  #### #",
        "#   #   #    #     # #",
        "# E # W ###### ### # #",
        "#   # W      #  C  # #",
        "# ### W #### # ####  #",
        "#            #       #",
        "######################",
    ],
    [
        "######################",
        "#P   ####   E   W    #",
        "# ##    # #### W #####",
        "#  C ## #    # W     #",
        "## ## ## #### # ###  #",
        "#      E    # #   #  #",
        "# ####### # # ### #  #",
        "#         # #   # #  #",
        "# ##### ### ### # #  #",
        "#     C    E     G   #",
        "######################",
    ],
    [
        "######################",
        "#P     E      W    G #",
        "# ####### ##  W  ## ##",
        "#   C     ##  W      #",
        "### ##### ####### ## #",
        "#   #   #      S     #",
        "# E #   ###### ### # #",
        "#   #      C  #   #  #",
        "# ### ####### # ###  #",
        "#                  E #",
        "######################",
    ],
    [
        "######################",
        "#P   W     E      G  #",
        "# ## W ####### ## ## #",
        "# C  W       #  S    #",
        "# ####### ## # ##### #",
        "#       # ## #     # #",
        "#  E    #    ##### # #",
        "# ##### ######   # # #",
        "#     #      C   #   #",
        "################## ###",
        "######################",
    ],
    [
        "######################",
        "#P      ####    E   G#",
        "# ######   # ###### ##",
        "#   C   S  #      #  #",
        "### ###### ###### #  #",
        "#   #    #      # #  #",
        "# E # W  ###### # #  #",
        "#   # W    C    # #  #",
        "# ### W ####### # ## #",
        "#                   ##",
        "######################",
    ],
    [
        "######################",
        "#P   C    E   W    G #",
        "# ###### ###  W #### #",
        "#      #   #  W    # #",
        "# S    ### ######  # #",
        "###### #        #  # #",
        "#    # #  ####  #  # #",
        "# E  # #    C   #    #",
        "# #### ####### ####  #",
        "#                    #",
        "######################",
    ],
    [
        "######################",
        "#P   ####   E      G #",
        "# ##    # ####### ## #",
        "#  C ## #    S  #    #",
        "## ## ## #### # #### #",
        "#      E    # #    # #",
        "# ####### # # ###  # #",
        "#         # #   #  # #",
        "# ##### ### ### #  # #",
        "#     C          #   #",
        "######################",
    ],
    [
        "######################",
        "#P    E      W     G #",
        "# ####### ## W #### ##",
        "#   C     ## W   S   #",
        "### ##### ####### ## #",
        "#   #   #      E     #",
        "#   #   ###### ### # #",
        "#   #      C  #   #  #",
        "# ### ####### # ###  #",
        "#                  S #",
        "######################",
    ],
    [
        "######################",
        "#P   W   E    ####  G#",
        "# # W ######  #     ##",
        "# # W    C #  #  S   #",
        "# # ###### #  ###### #",
        "# #      # #       # #",
        "# #### E # ######  # #",
        "#    #   #      #  # #",
        "#### # ### #### #  # #",
        "#      C      S #    #",
        "######################",
    ],
    [
        "######################",
        "#P      ####    E   G#",
        "# ######   # ###### ##",
        "#   C   S  #  C   #  #",
        "### ###### ###### #  #",
        "#   #    #      # #  #",
        "# E # W  ###### # #  #",
        "#   # W       S # #  #",
        "# ### W ####### # ## #",
        "#            E      ##",
        "######################",
    ],
    [
        "######################",
        "#P   C   E  W     G  #",
        "# ###### #  W ###### #",
        "#      # #  W   S    #",
        "# #### # ####### ### #",
        "# #    #       #   # #",
        "# # E  ######  ### # #",
        "# #    C    #    # # #",
        "# #######   #### # # #",
        "#          S       E #",
        "######################",
    ],
    [
        "######################",
        "#P  E   W    S    G  #",
        "# #### W ####### ## ##",
        "# C    W     E  #    #",
        "###### ###### ## ### #",
        "#    #      # ##   # #",
        "# S  ###### # #### # #",
        "#    #  C   #    # # #",
        "#### # ###   ### # # #",
        "#         E     S    #",
        "######################",
    ],
]

LEVEL_MAP = LEVELS[0]

MAP_COLS = len(LEVEL_MAP[0])
MAP_ROWS = len(LEVEL_MAP)
MAP_PIXEL_WIDTH = MAP_COLS * TILE_SIZE + WORLD_PADDING * 2
MAP_PIXEL_HEIGHT = MAP_ROWS * TILE_SIZE + WORLD_PADDING * 2

PLAYER_SCALE = 0.8
PLAYER_SPEED = 180

ANIM_FPS_MOVING = 8
ANIM_FPS_IDLE = 3
ENEMY_ANIM_FPS_IDLE = 4

FREEZE_RADIUS = 90
FREEZE_DURATION = 3.5

# Enemy settings
ENEMY_SHOOT_INTERVAL = 4.0
ENEMY_MAX_BULLETS = 3
ENEMY_MELEE_SPEED = 150
ENEMY_FREEZE_HIT_DURATION = 1.0
ENEMY_HITS_TO_KILL = 5

SPECIAL_ENEMY_SHOOT_INTERVAL = 3.2
SPECIAL_ENEMY_MAX_BULLETS = 5
SPECIAL_ENEMY_SPREAD = 0.38
SPECIAL_ENEMY_BULLET_OFFSET = 10

PROJECTILE_SPEED = 140
PROJECTILE_FREEZE_DECAY = 1.2
PROJECTILE_FREEZE_RADIUS = 95

ASSET_DIR = "Assets/Player"
MAP_PATH = "Assets/maps/snowterrain.png"
SHADOW_PATH = r"Assets/shadows/Pixelated dark gray oval shadow.png"

SNOW_TILE_1_PATH = r"Assets/maps/00_pixilart-sprite (5).png"
SNOW_TILE_2_PATH = r"Assets/maps/01_pixilart-sprite (5).png"

WATER_TILE_1_PATH = r"Assets/maps/02_pixilart-sprite (6).png"
WATER_TILE_2_PATH = r"Assets/maps/03_pixilart-sprite (6).png"
WATER_TILE_3_PATH = r"Assets/maps/04_pixilart-sprite (6).png"

# WATER FREEZE ANIMATION FRAMES
WATER_FREEZE_FRAME_1_PATH = r"Assets\maps\02_pixilart-sprite (6).png"
WATER_FREEZE_FRAME_2_PATH = r"Assets\maps\01_pixilart-sprite (11).png"
WATER_FREEZE_FRAME_3_PATH = r"Assets\maps\02_pixilart-sprite (11).png"
WATER_FREEZE_ANIM_FPS = 2

GOAL_IMAGE_PATH = r"Assets\maps\01_pixilart-sprite (8).png"
GOAL_DRAW_SIZE = (170, 170)

ENEMY_FRAME_1_PATH = r"Assets\Enemies\00_pixilart-sprite (7).png"
ENEMY_FRAME_2_PATH = r"Assets\Enemies\01_pixilart-sprite (7).png"

SPECIAL_ENEMY_FRAME_1_PATH = r"Assets\Enemies\02_pixilart-sprite (9).png"
SPECIAL_ENEMY_FRAME_2_PATH = r"Assets\Enemies\03_pixilart-sprite (9).png"

SLIME_FRAME_PATH_CANDIDATES = [
    [r"Assets\Enemies\01_pixilart-sprite (12).png", r"01_pixilart-sprite (12).png"],
    [r"Assets\Enemies\02_pixilart-sprite (12).png", r"02_pixilart-sprite (12).png"],
    [r"Assets\Enemies\03_pixilart-sprite (12).png", r"03_pixilart-sprite (12).png"],
    [r"Assets\Enemies\04_pixilart-sprite (12).png", r"04_pixilart-sprite (12).png"],
    [r"Assets\Enemies\05_pixilart-sprite (12).png", r"05_pixilart-sprite (12).png"],
    [r"Assets\Enemies\06_pixilart-sprite (12).png", r"06_pixilart-sprite (12).png"],
]
SLIME_DRAW_SIZE = (82, 82)
SLIME_ANIM_FPS = 10
SLIME_SQUISH_FRAME_INDEX = 5
SLIME_JUMP_DISTANCE = 26

ENEMY_DRAW_OFFSET_Y = -18
ENEMY_DRAW_SIZE = (86, 86)
ENEMY_COLLISION_SIZE = (38, 38)

# -----------------------------
# MUSIC / SFX
# -----------------------------
MUSIC_PATH = r"Sounds And Music\freeze-frame-ost.ogg"
MUSIC_VOLUME = 0.15

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

FREEZE_SOUND_PATHS = [
    "Sounds And Music\ice-freeze-1.mp3",
    "Sounds And Music\ice-freeze-2.mp3",
    "Sounds And Music\ice-freeze-3.mp3",
]

FREEZE_SOUND_VOLUME = 0.6
freeze_sounds = []

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(32)  # lets freeze sounds overlap nicely
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Freeze Frame")
clock = pygame.time.Clock()

# kept your existing font setup unchanged
font = pygame.font.Font(r"C:\code\pydyu\freezeframe\fonts\LowresPixel-Regular.otf", 28)
big_font = pygame.font.Font(r"C:\code\pydyu\freezeframe\fonts\LowresPixel-Regular.otf", 56)

# -----------------------------
# HELPERS
# -----------------------------
def load_sprite(filename, scale=1):
    path = os.path.join(ASSET_DIR, filename)
    image = pygame.image.load(path).convert_alpha()
    image.set_colorkey((0, 0, 0))

    if scale != 1:
        w, h = image.get_size()
        image = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
    return image


def load_image(path, size=None, colorkey=None):
    image = pygame.image.load(path).convert_alpha()
    if colorkey is not None:
        image.set_colorkey(colorkey)
    if size is not None:
        image = pygame.transform.scale(image, size)
    return image


def load_shadow(path):
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (42, 14))
    return image


def first_existing_path(candidates):
    for path in candidates:
        if os.path.exists(path):
            return path
    return candidates[0]


def make_placeholder_surface(size, color, border_color=None):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill(color)
    if border_color:
        pygame.draw.rect(surf, border_color, surf.get_rect(), 2)
    return surf


def make_key_surface(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    green = (60, 220, 90)
    dark_green = (20, 120, 40)

    pygame.draw.circle(surf, green, (size // 3, size // 2), size // 6)
    pygame.draw.circle(surf, dark_green, (size // 3, size // 2), size // 6, 3)

    shaft_w = max(6, size // 8)
    shaft_h = max(18, size // 3)
    shaft_x = size // 3 + size // 10
    shaft_y = size // 2 - shaft_w // 2
    pygame.draw.rect(surf, green, (shaft_x, shaft_y, shaft_h, shaft_w))

    tooth_w = max(5, size // 10)
    tooth_h = max(8, size // 8)
    pygame.draw.rect(surf, green, (shaft_x + shaft_h - tooth_w * 2, shaft_y + shaft_w, tooth_w, tooth_h))
    pygame.draw.rect(surf, green, (shaft_x + shaft_h - tooth_w, shaft_y + shaft_w, tooth_w, tooth_h * 2))

    pygame.draw.rect(surf, dark_green, (shaft_x, shaft_y, shaft_h, shaft_w), 2)
    return surf


def tile_to_world(tx, ty):
    return WORLD_PADDING + tx * TILE_SIZE, WORLD_PADDING + ty * TILE_SIZE


def rect_center_distance(rect_a, rect_b):
    ax, ay = rect_a.center
    bx, by = rect_b.center
    return math.hypot(ax - bx, ay - by)


def set_current_level(level_rows):
    global LEVEL_MAP, MAP_COLS, MAP_ROWS, MAP_PIXEL_WIDTH, MAP_PIXEL_HEIGHT, background

    LEVEL_MAP = level_rows
    MAP_COLS = len(LEVEL_MAP[0])
    MAP_ROWS = len(LEVEL_MAP)
    MAP_PIXEL_WIDTH = MAP_COLS * TILE_SIZE + WORLD_PADDING * 2
    MAP_PIXEL_HEIGHT = MAP_ROWS * TILE_SIZE + WORLD_PADDING * 2

    background = pygame.image.load(MAP_PATH).convert()
    background = pygame.transform.scale(background, (MAP_PIXEL_WIDTH, MAP_PIXEL_HEIGHT))


def start_background_music():
    if not os.path.exists(MUSIC_PATH):
        print(f"Background music file not found: {MUSIC_PATH}")
        return

    try:
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Could not play background music: {e}")


def load_freeze_sounds():
    loaded = []
    for path in FREEZE_SOUND_PATHS:
        if not os.path.exists(path):
            print(f"Freeze sound file not found: {path}")
            continue
        try:
            snd = pygame.mixer.Sound(path)
            snd.set_volume(FREEZE_SOUND_VOLUME)
            loaded.append(snd)
            print(f"Loaded freeze sound: {path}")
        except pygame.error as e:
            print(f"Could not load freeze sound {path}: {e}")
    return loaded


def play_random_freeze_sound():
    if not freeze_sounds:
        return
    random.choice(freeze_sounds).play()


# -----------------------------
# CAMERA
# -----------------------------
class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def update(self, target_x, target_y):
        self.x = int(target_x - SCREEN_WIDTH // 2)
        self.y = int(target_y - SCREEN_HEIGHT // 2)

        self.x = max(0, min(self.x, max(0, self.width - SCREEN_WIDTH)))
        self.y = max(0, min(self.y, max(0, self.height - SCREEN_HEIGHT)))

    def apply_rect(self, rect):
        return rect.move(-self.x, -self.y)

    def apply_point(self, x, y):
        return x - self.x, y - self.y


# -----------------------------
# LOAD FIRST BACKGROUND
# -----------------------------
background = pygame.image.load(MAP_PATH).convert()
background = pygame.transform.scale(background, (MAP_PIXEL_WIDTH, MAP_PIXEL_HEIGHT))

# -----------------------------
# LOAD MAP TILES
# -----------------------------
snow_tile_1_img = load_image(SNOW_TILE_1_PATH, (SNOW_TILE_SIZE, SNOW_TILE_SIZE))
snow_tile_2_img = load_image(SNOW_TILE_2_PATH, (SNOW_TILE_SIZE, SNOW_TILE_SIZE))

water_tile_1_img = load_image(WATER_TILE_1_PATH, (WATER_TILE_SIZE, WATER_TILE_SIZE))
water_tile_2_img = load_image(WATER_TILE_2_PATH, (WATER_TILE_SIZE, WATER_TILE_SIZE))
water_tile_3_img = load_image(WATER_TILE_3_PATH, (WATER_TILE_SIZE, WATER_TILE_SIZE))

water_freeze_frame_1_img = load_image(WATER_FREEZE_FRAME_1_PATH, (WATER_TILE_SIZE, WATER_TILE_SIZE))
water_freeze_frame_2_img = load_image(WATER_FREEZE_FRAME_2_PATH, (WATER_TILE_SIZE, WATER_TILE_SIZE))
water_freeze_frame_3_img = load_image(WATER_FREEZE_FRAME_3_PATH, (WATER_TILE_SIZE, WATER_TILE_SIZE))

WATER_FREEZE_FRAMES = [
    water_freeze_frame_2_img,
    water_freeze_frame_3_img,
]

goal_tile_img = load_image(GOAL_IMAGE_PATH, GOAL_DRAW_SIZE)

# -----------------------------
# PLAYER FRAMES
# -----------------------------
frames = {}
for i in range(15):
    filename = f"{i:02d}_pixilart-sprite (4).png"
    frames[i] = load_sprite(filename, PLAYER_SCALE)

shadow_image = load_shadow(SHADOW_PATH)

ANIMS = {
    "down":  [frames[0], frames[1], frames[2], frames[2]],
    "up":    [frames[3], frames[4], frames[5], frames[6]],
    "right": [frames[7], frames[8], frames[9], frames[10]],
    "left":  [frames[11], frames[12], frames[13], frames[14]],
}

IDLE_FRAME_INDEXES = {
    "down":  [2, 3],
    "up":    [2, 3],
    "right": [2, 3],
    "left":  [2, 3],
}

# -----------------------------
# PLACEHOLDER TILE IMAGES
# -----------------------------
ice_img = make_placeholder_surface((TILE_SIZE, TILE_SIZE), (180, 230, 255), (120, 190, 240))

enemy_frame_1 = load_image(ENEMY_FRAME_1_PATH, ENEMY_DRAW_SIZE)
enemy_frame_2 = load_image(ENEMY_FRAME_2_PATH, ENEMY_DRAW_SIZE)
ENEMY_IDLE_FRAMES = [enemy_frame_1, enemy_frame_2]

special_enemy_frame_1 = load_image(SPECIAL_ENEMY_FRAME_1_PATH, ENEMY_DRAW_SIZE)
special_enemy_frame_2 = load_image(SPECIAL_ENEMY_FRAME_2_PATH, ENEMY_DRAW_SIZE)
SPECIAL_ENEMY_IDLE_FRAMES = [special_enemy_frame_1, special_enemy_frame_2]

enemy_frozen_img = pygame.image.load(r"C:\code\pydyu\freezeframe\Assets\Enemies\01_pixilart-sprite (14).png").convert_alpha()
enemy_frozen_img_2 = pygame.image.load(r"C:\code\pydyu\freezeframe\Assets\Enemies\pixil-frame-0.png").convert_alpha()
special_enemy_melee_img = make_placeholder_surface(ENEMY_DRAW_SIZE, (120, 80, 230), (70, 40, 140))

SLIME_FRAMES = [
    load_image(first_existing_path(path_candidates), SLIME_DRAW_SIZE)
    for path_candidates in SLIME_FRAME_PATH_CANDIDATES
]

key_img = make_key_surface(TILE_SIZE)

# -----------------------------
# COIN IMAGE
# -----------------------------
coin_img = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
coin_radius = max(8, TILE_SIZE // 4)
pygame.draw.circle(coin_img, (245, 220, 60), (TILE_SIZE // 2, TILE_SIZE // 2), coin_radius)
pygame.draw.circle(coin_img, (255, 245, 140), (TILE_SIZE // 2, TILE_SIZE // 2), coin_radius, 3)
pygame.draw.circle(
    coin_img,
    (255, 255, 190),
    (TILE_SIZE // 2 - 3, TILE_SIZE // 2 - 3),
    max(2, coin_radius // 4),
)

# -----------------------------
# PROJECTILE IMAGE
# -----------------------------
projectile_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(projectile_img, (0, 0, 255), (7, 7), 6)
pygame.draw.circle(projectile_img, (0, 0, 255), (7, 7), 6, 2)

frozen_projectile_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(frozen_projectile_img, (180, 235, 255), (7, 7), 6)
pygame.draw.circle(frozen_projectile_img, (220, 245, 255), (7, 7), 6, 2)

special_projectile_img = pygame.Surface((14, 14), pygame.SRCALPHA)
pygame.draw.circle(special_projectile_img, (140, 90, 255), (7, 7), 6)
pygame.draw.circle(special_projectile_img, (210, 190, 255), (7, 7), 6, 2)

# load freeze SFX after mixer init
freeze_sounds = load_freeze_sounds()

# -----------------------------
# GAME OBJECTS
# -----------------------------
class Wall:
    def __init__(self, tx, ty, level_rows):
        x, y = tile_to_world(tx, ty)

        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.image = random.choice([snow_tile_1_img, snow_tile_2_img])

        offset = (SNOW_TILE_SIZE - TILE_SIZE) // 2
        self.draw_rect = pygame.Rect(x - offset, y - offset, SNOW_TILE_SIZE, SNOW_TILE_SIZE)

    def draw(self, surface, camera):
        surface.blit(self.image, camera.apply_rect(self.draw_rect))


class Water:
    def __init__(self, tx, ty):
        self.tx = tx
        self.ty = ty

        x, y = tile_to_world(tx, ty)
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

        self.image = random.choice([
            water_tile_1_img,
            water_tile_2_img,
            water_tile_3_img
        ])

        self.draw_rect = self.image.get_rect(center=self.rect.center)

        self.frozen = False
        self.freeze_timer = 0.0

        self.freeze_anim_playing = False
        self.freeze_anim_timer = 0.0
        self.freeze_anim_index = 0

        self.connect_up = False
        self.connect_down = False
        self.connect_left = False
        self.connect_right = False

    def freeze(self):
        if self.frozen or self.freeze_anim_playing:
            return False

        self.frozen = True
        self.freeze_timer = FREEZE_DURATION
        self.freeze_anim_playing = True
        self.freeze_anim_timer = 0.0
        self.freeze_anim_index = 0
        return True

    def update(self, dt):
        if self.freeze_anim_playing:
            self.freeze_anim_timer += dt
            frame_duration = 1.0 / WATER_FREEZE_ANIM_FPS

            while self.freeze_anim_timer >= frame_duration:
                self.freeze_anim_timer -= frame_duration
                self.freeze_anim_index += 1

                if self.freeze_anim_index >= len(WATER_FREEZE_FRAMES):
                    self.freeze_anim_index = len(WATER_FREEZE_FRAMES) - 1
                    self.freeze_anim_playing = False
                    break

        if self.frozen:
            self.freeze_timer -= dt
            if self.freeze_timer <= 0:
                self.frozen = False
                self.freeze_timer = 0.0
                self.freeze_anim_playing = False
                self.freeze_anim_timer = 0.0
                self.freeze_anim_index = 0

    def draw(self, surface, camera):
        draw_rect = camera.apply_rect(self.draw_rect)

        if self.freeze_anim_playing:
            surface.blit(WATER_FREEZE_FRAMES[self.freeze_anim_index], draw_rect)
            return

        if self.frozen:
            surface.blit(WATER_FREEZE_FRAMES[-1], draw_rect)
            return

        surface.blit(self.image, draw_rect)

class IceBlock:
    def __init__(self, tx, ty):
        x, y = tile_to_world(tx, ty)
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    def draw(self, surface, camera):
        surface.blit(ice_img, camera.apply_rect(self.rect))


class Goal:
    def __init__(self, tx, ty):
        x, y = tile_to_world(tx, ty)
        self.tx = tx
        self.ty = ty

        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.draw_rect = goal_tile_img.get_rect(center=self.rect.center)

    def draw(self, surface, camera):
        surface.blit(goal_tile_img, camera.apply_rect(self.draw_rect))


class LevelKey:
    def __init__(self, tx, ty):
        x, y = tile_to_world(tx, ty)
        self.tx = tx
        self.ty = ty
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.collected = False

    def draw(self, surface, camera):
        if not self.collected:
            surface.blit(key_img, camera.apply_rect(self.rect))


class Coin:
    def __init__(self, tx, ty):
        x, y = tile_to_world(tx, ty)
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.collected = False

    def draw(self, surface, camera):
        if not self.collected:
            surface.blit(coin_img, camera.apply_rect(self.rect))


class Projectile:
    def __init__(self, x, y, vx, vy, image=None):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)

        self.frozen = False
        self.decay_timer = PROJECTILE_FREEZE_DECAY
        self.alive = True

        self.image = image if image is not None else projectile_img
        self.rect = pygame.Rect(0, 0, 14, 14)
        self.update_rect()

    def update_rect(self):
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def update(self, dt, walls, ice_blocks, waters):
        if not self.alive:
            return

        if self.frozen:
            self.decay_timer -= dt
            if self.decay_timer <= 0:
                self.alive = False
            return

        self.x += self.vx * dt
        self.y += self.vy * dt
        self.update_rect()

        if self.x < 0 or self.y < 0 or self.x > MAP_PIXEL_WIDTH or self.y > MAP_PIXEL_HEIGHT:
            self.alive = False
            return

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.alive = False
                return

        for ice in ice_blocks:
            if self.rect.colliderect(ice.rect):
                self.alive = False
                return

        for water in waters:
            if self.rect.colliderect(water.rect) and not water.frozen:
                self.alive = False
                return

    def freeze(self):
        if self.frozen or not self.alive:
            return False
        self.frozen = True
        self.decay_timer = PROJECTILE_FREEZE_DECAY
        return True

    def draw(self, surface, camera):
        if not self.alive:
            return

        img = frozen_projectile_img if self.frozen else self.image
        surface.blit(img, camera.apply_rect(self.rect))


class Enemy:
    def __init__(self, tx, ty):
        x, y = tile_to_world(tx, ty)
        self.x = float(x + TILE_SIZE // 2)
        self.y = float(y + TILE_SIZE // 2)

        self.rect = pygame.Rect(0, 0, ENEMY_COLLISION_SIZE[0], ENEMY_COLLISION_SIZE[1])
        self.update_rect()

        self.frozen = False
        self.freeze_timer = 0.0

        self.freeze_hits = 0
        self.alive = True

        self.shots_left = ENEMY_MAX_BULLETS
        self.shoot_timer = ENEMY_SHOOT_INTERVAL

        self.anim_timer = 0.0
        self.anim_index = 0
        self.image = ENEMY_IDLE_FRAMES[self.anim_index]

        # slime animation
        self.slime_anim_timer = 0.0
        self.slime_anim_index = 0

        # smooth melee movement tuning
        self.melee_speed = ENEMY_MELEE_SPEED
        self.slime_bob_timer = 0.0
        self.slime_bob_amount = 8.0

    def update_rect(self):
        self.rect = pygame.Rect(0, 0, ENEMY_COLLISION_SIZE[0], ENEMY_COLLISION_SIZE[1])
        self.rect.center = (int(self.x), int(self.y))

    def animate(self, dt):
        self.anim_timer += dt
        frame_duration = 1.0 / ENEMY_ANIM_FPS_IDLE

        while self.anim_timer >= frame_duration:
            self.anim_timer -= frame_duration
            self.anim_index = (self.anim_index + 1) % len(ENEMY_IDLE_FRAMES)

        self.image = ENEMY_IDLE_FRAMES[self.anim_index]

    def animate_slime(self, dt):
        self.slime_anim_timer += dt
        frame_duration = 1.0 / SLIME_ANIM_FPS

        while self.slime_anim_timer >= frame_duration:
            self.slime_anim_timer -= frame_duration
            self.slime_anim_index = (self.slime_anim_index + 1) % len(SLIME_FRAMES)

    def freeze(self, duration=FREEZE_DURATION, count_hit=False):
        if not self.alive:
            return False

        newly_frozen = not self.frozen
        self.frozen = True
        self.freeze_timer = duration

        if count_hit and newly_frozen:
            self.freeze_hits += 1
            if self.freeze_hits >= ENEMY_HITS_TO_KILL:
                self.alive = False

        return newly_frozen

    def collides_blocking(self, test_rect, walls, ice_blocks, waters):
        for wall in walls:
            if test_rect.colliderect(wall.rect):
                return True

        for ice in ice_blocks:
            if test_rect.colliderect(ice.rect):
                return True

        for water in waters:
            if test_rect.colliderect(water.rect) and not water.frozen:
                return True

        return False

    def move_toward_player(self, dt, player, walls, ice_blocks, waters):
        dx = player.hitbox.centerx - self.rect.centerx
        dy = player.hitbox.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            return

        dx /= dist
        dy /= dist

        move_x = dx * self.melee_speed * dt
        move_y = dy * self.melee_speed * dt

        test_rect = self.rect.copy()
        test_rect.x += int(move_x)
        if not self.collides_blocking(test_rect, walls, ice_blocks, waters):
            self.x += move_x
            self.update_rect()

        test_rect = self.rect.copy()
        test_rect.y += int(move_y)
        if not self.collides_blocking(test_rect, walls, ice_blocks, waters):
            self.y += move_y
            self.update_rect()

    def shoot_at_player(self, projectiles, player):
        dx = player.hitbox.centerx - self.rect.centerx
        dy = player.hitbox.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            dx, dy, dist = 1, 0, 1

        vx = (dx / dist) * PROJECTILE_SPEED
        vy = (dy / dist) * PROJECTILE_SPEED
        projectiles.append(Projectile(self.rect.centerx, self.rect.centery, vx, vy))

    def update(self, dt, player, projectiles, walls, ice_blocks, waters):
        if not self.alive:
            return

        if self.frozen:
            self.freeze_timer -= dt
            if self.freeze_timer <= 0:
                self.frozen = False
                self.freeze_timer = 0.0
            return

        if self.shots_left > 0:
            self.animate(dt)
            self.shoot_timer -= dt
            if self.shoot_timer <= 0:
                self.shoot_at_player(projectiles, player)
                self.shots_left -= 1
                self.shoot_timer = ENEMY_SHOOT_INTERVAL
        else:
            self.animate_slime(dt)
            self.move_toward_player(dt, player, walls, ice_blocks, waters)
            self.slime_bob_timer += dt

    def draw(self, surface, camera):
        if not self.alive:
            return

        if self.frozen:
            img = enemy_frozen_img
            bob_y = 0
        elif self.shots_left <= 0:
            img = SLIME_FRAMES[self.slime_anim_index]
            bob_y = math.sin(self.slime_bob_timer * 10.0) * self.slime_bob_amount
        else:
            img = self.image
            bob_y = 0

        draw_rect = img.get_rect(center=self.rect.center)
        draw_rect.y += ENEMY_DRAW_OFFSET_Y - int(bob_y)
        surface.blit(img, camera.apply_rect(draw_rect))


class DoubleShotEnemy(Enemy):
    def __init__(self, tx, ty):
        super().__init__(tx, ty)
        self.shots_left = SPECIAL_ENEMY_MAX_BULLETS
        self.shoot_timer = SPECIAL_ENEMY_SHOOT_INTERVAL
        self.image = SPECIAL_ENEMY_IDLE_FRAMES[self.anim_index]
        self.move_cycle_timer = 0.0
        self.move_cycle_interval = 0.38

    def animate(self, dt):
        self.anim_timer += dt
        frame_duration = 1.0 / ENEMY_ANIM_FPS_IDLE

        while self.anim_timer >= frame_duration:
            self.anim_timer -= frame_duration
            self.anim_index = (self.anim_index + 1) % len(SPECIAL_ENEMY_IDLE_FRAMES)

        self.image = SPECIAL_ENEMY_IDLE_FRAMES[self.anim_index]

    def shoot_at_player(self, projectiles, player):
        dx = player.hitbox.centerx - self.rect.centerx
        dy = player.hitbox.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            dx, dy, dist = 1, 0, 1

        nx = dx / dist
        ny = dy / dist

        perp_x = -ny
        perp_y = nx

        dir1_x = nx + perp_x * SPECIAL_ENEMY_SPREAD
        dir1_y = ny + perp_y * SPECIAL_ENEMY_SPREAD
        dir2_x = nx - perp_x * SPECIAL_ENEMY_SPREAD
        dir2_y = ny - perp_y * SPECIAL_ENEMY_SPREAD

        len1 = math.hypot(dir1_x, dir1_y)
        len2 = math.hypot(dir2_x, dir2_y)

        dir1_x /= len1
        dir1_y /= len1
        dir2_x /= len2
        dir2_y /= len2

        spawn1_x = self.rect.centerx + perp_x * SPECIAL_ENEMY_BULLET_OFFSET
        spawn1_y = self.rect.centery + perp_y * SPECIAL_ENEMY_BULLET_OFFSET
        spawn2_x = self.rect.centerx - perp_x * SPECIAL_ENEMY_BULLET_OFFSET
        spawn2_y = self.rect.centery - perp_y * SPECIAL_ENEMY_BULLET_OFFSET

        projectiles.append(
            Projectile(
                spawn1_x,
                spawn1_y,
                dir1_x * PROJECTILE_SPEED,
                dir1_y * PROJECTILE_SPEED,
                image=special_projectile_img,
            )
        )
        projectiles.append(
            Projectile(
                spawn2_x,
                spawn2_y,
                dir2_x * PROJECTILE_SPEED,
                dir2_y * PROJECTILE_SPEED,
                image=special_projectile_img,
            )
        )

    def update(self, dt, player, projectiles, walls, ice_blocks, waters):
        if not self.alive:
            return

        if self.frozen:
            self.freeze_timer -= dt
            if self.freeze_timer <= 0:
                self.frozen = False
                self.freeze_timer = 0.0
            return

        self.animate(dt)

        if self.shots_left > 0:
            self.shoot_timer -= dt
            if self.shoot_timer <= 0:
                self.shoot_at_player(projectiles, player)
                self.shots_left -= 1
                self.shoot_timer = SPECIAL_ENEMY_SHOOT_INTERVAL
        else:
            self.move_cycle_timer += dt
            if self.move_cycle_timer >= self.move_cycle_interval:
                self.move_cycle_timer = 0.0
                self.move_toward_player(dt * 6.0, player, walls, ice_blocks, waters)

    def draw(self, surface, camera):
        if not self.alive:
            return

        if self.frozen:
            img = enemy_frozen_img_2
        else:
            img = self.image

        draw_rect = img.get_rect(center=self.rect.center)
        draw_rect.y += ENEMY_DRAW_OFFSET_Y
        surface.blit(img, camera.apply_rect(draw_rect))


class Player:
    def __init__(self, x, y):
        self.spawn_x = float(x)
        self.spawn_y = float(y)

        self.x = float(x)
        self.y = float(y)

        self.direction = "down"
        self.anim_index = 2
        self.image = ANIMS[self.direction][self.anim_index]

        self.anim_timer = 0.0
        self.was_moving = False
        self.shadow = shadow_image

        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self.hitbox = pygame.Rect(0, 0, 18, 12)
        self.update_rects()

        self.freeze_flash_timer = 0.0
        self.has_level_key = False

    def update_rects(self):
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self.hitbox.centerx = int(self.x)
        self.hitbox.centery = int(self.y + 12)

    def reset_to_spawn(self):
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.direction = "down"
        self.anim_index = 2
        self.image = ANIMS[self.direction][self.anim_index]
        self.anim_timer = 0.0
        self.was_moving = False
        self.update_rects()

    def handle_input(self):
        keys = pygame.key.get_pressed()

        move_x = 0
        move_y = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_x += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move_y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move_y += 1

        return move_x, move_y

    def collides_blocking(self, test_hitbox, walls, ice_blocks, waters):
        for wall in walls:
            if test_hitbox.colliderect(wall.rect):
                return True

        for ice in ice_blocks:
            if test_hitbox.colliderect(ice.rect):
                return True

        for water in waters:
            if test_hitbox.colliderect(water.rect) and not water.frozen:
                return True

        return False

    def update(self, dt, walls, ice_blocks, waters):
        move_x, move_y = self.handle_input()
        moving = (move_x != 0 or move_y != 0)

        if move_x != 0 and move_y != 0:
            move_x *= 0.7071
            move_y *= 0.7071

        dx = move_x * PLAYER_SPEED * dt
        dy = move_y * PLAYER_SPEED * dt

        if moving:
            if abs(move_x) > abs(move_y):
                self.direction = "right" if move_x > 0 else "left"
            else:
                self.direction = "down" if move_y > 0 else "up"

        test_hitbox = self.hitbox.copy()
        test_hitbox.x += int(dx)
        if not self.collides_blocking(test_hitbox, walls, ice_blocks, waters):
            self.x += dx
            self.hitbox = test_hitbox

        test_hitbox = self.hitbox.copy()
        test_hitbox.y += int(dy)
        if not self.collides_blocking(test_hitbox, walls, ice_blocks, waters):
            self.y += dy
            self.hitbox = test_hitbox

        left_limit = WORLD_PADDING + BORDER_SIZE
        right_limit = MAP_PIXEL_WIDTH - WORLD_PADDING - BORDER_SIZE
        top_limit = WORLD_PADDING + BORDER_SIZE
        bottom_limit = MAP_PIXEL_HEIGHT - WORLD_PADDING - BORDER_SIZE

        self.x = max(left_limit, min(right_limit, self.x))
        self.y = max(top_limit, min(bottom_limit, self.y))

        self.animate(dt, moving)
        self.update_rects()
        self.was_moving = moving

        if self.freeze_flash_timer > 0:
            self.freeze_flash_timer -= dt

    def animate(self, dt, moving):
        anim_list = ANIMS[self.direction]

        if moving:
            if not self.was_moving:
                self.anim_index = 0
                self.anim_timer = 0.0

            self.anim_timer += dt
            frame_duration = 1.0 / ANIM_FPS_MOVING

            if self.anim_timer >= frame_duration:
                self.anim_timer -= frame_duration
                self.anim_index = (self.anim_index + 1) % len(anim_list)

            self.image = anim_list[self.anim_index]

        else:
            idle_indexes = IDLE_FRAME_INDEXES[self.direction]

            if self.was_moving or self.anim_index not in idle_indexes:
                self.anim_index = idle_indexes[0]
                self.anim_timer = 0.0

            self.anim_timer += dt
            frame_duration = 1.0 / ANIM_FPS_IDLE

            if self.anim_timer >= frame_duration:
                self.anim_timer -= frame_duration
                current = idle_indexes.index(self.anim_index)
                self.anim_index = idle_indexes[(current + 1) % len(idle_indexes)]

            self.image = anim_list[self.anim_index]

    def freeze_pulse(self, waters, enemies, projectiles):
        self.freeze_flash_timer = 0.18
        anything_newly_frozen = False

        for water in waters:
            if rect_center_distance(self.hitbox, water.rect) <= FREEZE_RADIUS:
                if water.freeze():
                    anything_newly_frozen = True

        for enemy in enemies:
            if enemy.alive and rect_center_distance(self.hitbox, enemy.rect) <= FREEZE_RADIUS:
                if enemy.freeze(duration=ENEMY_FREEZE_HIT_DURATION, count_hit=True):
                    anything_newly_frozen = True

        for projectile in projectiles:
            if not projectile.alive or projectile.frozen:
                continue
            if projectile.rect.colliderect(self.hitbox):
                continue
            if rect_center_distance(self.hitbox, projectile.rect) <= PROJECTILE_FREEZE_RADIUS:
                if projectile.freeze():
                    anything_newly_frozen = True

        if anything_newly_frozen:
            play_random_freeze_sound()

    def draw(self, surface, camera):
        shadow_x, shadow_y = camera.apply_point(int(self.x), int(self.y + 11))
        shadow_rect = self.shadow.get_rect(center=(shadow_x, shadow_y))
        surface.blit(self.shadow, shadow_rect)

        draw_rect = self.rect.move(-camera.x, -camera.y)
        surface.blit(self.image, draw_rect)

        if self.freeze_flash_timer > 0:
            alpha = int(120 * (self.freeze_flash_timer / 0.18))
            radius = int(FREEZE_RADIUS)
            pulse = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(pulse, (180, 235, 255, alpha), (radius, radius), radius, 4)
            pulse_x, pulse_y = camera.apply_point(self.hitbox.centerx - radius, self.hitbox.centery - radius)
            surface.blit(pulse, (pulse_x, pulse_y))


# -----------------------------
# LEVEL BUILD
# -----------------------------
def find_random_key_tile(level_rows, goal_pos, player_spawn_tile):
    goal_tx, goal_ty = goal_pos
    spawn_tx, spawn_ty = player_spawn_tile

    candidates = []
    fallback_candidates = []

    for ty, row in enumerate(level_rows):
        for tx, ch in enumerate(row):
            if ch != " ":
                continue

            dist_to_goal = abs(tx - goal_tx) + abs(ty - goal_ty)
            dist_to_spawn = abs(tx - spawn_tx) + abs(ty - spawn_ty)

            if dist_to_goal >= 7 and dist_to_spawn >= 4:
                candidates.append((tx, ty))

            fallback_candidates.append((tx, ty))

    if candidates:
        return random.choice(candidates)

    if fallback_candidates:
        return random.choice(fallback_candidates)

    return goal_tx, goal_ty


def build_level(level_rows, level_index):
    walls = []
    waters = []
    ice_blocks = []
    enemies = []
    coins = []
    goal = None
    level_key = None
    player_spawn = None

    water_lookup = {}
    goal_pos = None
    player_spawn_tile = None

    for ty, row in enumerate(level_rows):
        for tx, ch in enumerate(row):
            if ch == "#":
                walls.append(Wall(tx, ty, level_rows))
            elif ch == "W":
                water = Water(tx, ty)
                waters.append(water)
                water_lookup[(tx, ty)] = water
            elif ch == "I":
                ice_blocks.append(IceBlock(tx, ty))
            elif ch == "E":
                enemies.append(Enemy(tx, ty))
            elif ch == "S":
                if level_index >= 5:
                    enemies.append(DoubleShotEnemy(tx, ty))
            elif ch == "G":
                goal = Goal(tx, ty)
                goal_pos = (tx, ty)
            elif ch == "C":
                coins.append(Coin(tx, ty))
            elif ch == "P":
                px = tile_to_world(tx, ty)[0] + TILE_SIZE // 2
                py = tile_to_world(tx, ty)[1] + TILE_SIZE // 2
                player_spawn = (px, py)
                player_spawn_tile = (tx, ty)

    if goal_pos is not None and player_spawn_tile is not None:
        key_tx, key_ty = find_random_key_tile(level_rows, goal_pos, player_spawn_tile)
        level_key = LevelKey(key_tx, key_ty)

    for (tx, ty), water in water_lookup.items():
        water.connect_up = (tx, ty - 1) in water_lookup
        water.connect_down = (tx, ty + 1) in water_lookup
        water.connect_left = (tx - 1, ty) in water_lookup
        water.connect_right = (tx + 1, ty) in water_lookup

    return walls, waters, ice_blocks, enemies, coins, goal, level_key, player_spawn


def load_level(level_index):
    set_current_level(LEVELS[level_index])
    walls, waters, ice_blocks, enemies, coins, goal, level_key, player_spawn = build_level(LEVEL_MAP, level_index)

    if player_spawn is None:
        player_spawn = (WORLD_PADDING + TILE_SIZE * 2, WORLD_PADDING + TILE_SIZE * 2)

    player = Player(*player_spawn)
    camera = Camera(MAP_PIXEL_WIDTH, MAP_PIXEL_HEIGHT)
    projectiles = []

    return walls, waters, ice_blocks, enemies, coins, goal, level_key, player, camera, projectiles


# -----------------------------
# MAIN
# -----------------------------
async def main():
    start_background_music()

    current_level_index = 0
    walls, waters, ice_blocks, enemies, coins, goal, level_key, player, camera, projectiles = load_level(current_level_index)

    game_won = False
    game_finished = False
    coin_count = 0
    total_coins = 0

    easter_egg_timer = 0.0
    easter_egg_text = "+1 Coin, note from dyu, STOP CHEATING"

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_won and not game_finished:
                    player.freeze_pulse(waters, enemies, projectiles)

                elif event.key == pygame.K_r:
                    walls, waters, ice_blocks, enemies, coins, goal, level_key, player, camera, projectiles = load_level(current_level_index)
                    game_won = False
                    game_finished = False
                    coin_count = 0
                    player.has_level_key = False

                elif event.key in (pygame.K_RETURN, pygame.K_n):
                    if game_won and not game_finished:
                        current_level_index += 1
                        if current_level_index >= len(LEVELS):
                            game_finished = True
                            current_level_index = len(LEVELS) - 1
                        else:
                            walls, waters, ice_blocks, enemies, coins, goal, level_key, player, camera, projectiles = load_level(current_level_index)
                            game_won = False
                            coin_count = 0

                elif event.key == pygame.K_x:
                    mods = pygame.key.get_mods()
                    if (mods & pygame.KMOD_CTRL) and (mods & pygame.KMOD_SHIFT):
                        easter_egg_timer = 2.0
                        coin_count += 1
                        total_coins += 1

        if easter_egg_timer > 0:
            easter_egg_timer -= dt
            if easter_egg_timer < 0:
                easter_egg_timer = 0

        if not game_won and not game_finished:
            for water in waters:
                water.update(dt)

            for enemy in enemies:
                enemy.update(dt, player, projectiles, walls, ice_blocks, waters)

            for projectile in projectiles:
                projectile.update(dt, walls, ice_blocks, waters)

            projectiles = [p for p in projectiles if p.alive]
            enemies = [e for e in enemies if e.alive]

            player.update(dt, walls, ice_blocks, waters)

            for coin in coins:
                if not coin.collected and player.hitbox.colliderect(coin.rect):
                    coin.collected = True
                    coin_count += 1
                    total_coins += 1

            if level_key and not level_key.collected and player.hitbox.colliderect(level_key.rect):
                level_key.collected = True
                player.has_level_key = True

            for projectile in projectiles:
                if not projectile.frozen and projectile.rect.colliderect(player.hitbox):
                    player.reset_to_spawn()
                    projectiles = []
                    break

            for enemy in enemies:
                if not enemy.frozen and enemy.rect.colliderect(player.hitbox):
                    player.reset_to_spawn()
                    projectiles = []
                    break

            if goal and player.hitbox.colliderect(goal.rect) and player.has_level_key:
                if current_level_index == len(LEVELS) - 1:
                    game_finished = True
                else:
                    game_won = True

        camera.update(player.x, player.y)

        screen.blit(background, (-camera.x, -camera.y))

        for wall in walls:
            wall.draw(screen, camera)

        for coin in coins:
            coin.draw(screen, camera)

        for water in waters:
            water.draw(screen, camera)

        for ice in ice_blocks:
            ice.draw(screen, camera)

        if goal:
            goal.draw(screen, camera)

        if level_key:
            level_key.draw(screen, camera)

        for projectile in projectiles:
            projectile.draw(screen, camera)

        for enemy in enemies:
            enemy.draw(screen, camera)

        player.draw(screen, camera)

        # only keep coins visible on the main HUD
        coin_text = font.render(f"Coins: {coin_count}", True, (0, 0, 0))
        screen.blit(coin_text, (16, 12))

        if game_won:
            win_surf = big_font.render("LEVEL CLEAR", True, (230, 245, 255))
            hint_surf = font.render("Press ENTER or N for next level", True, (230, 245, 255))
            restart_surf = font.render("Press R to restart this level", True, (230, 245, 255))
            screen.blit(win_surf, (SCREEN_WIDTH // 2 - win_surf.get_width() // 2, 90))
            screen.blit(hint_surf, (SCREEN_WIDTH // 2 - hint_surf.get_width() // 2, 150))
            screen.blit(restart_surf, (SCREEN_WIDTH // 2 - restart_surf.get_width() // 2, 182))

        if game_finished:
            win_surf = big_font.render(f"YOU BEAT ALL {len(LEVELS)} LEVELS", True, (0, 0, 0))
            hint_surf = font.render("Press R to replay the current level", True, (0, 5, 0))
            screen.blit(win_surf, (SCREEN_WIDTH // 2 - win_surf.get_width() // 2, 90))
            screen.blit(hint_surf, (SCREEN_WIDTH // 2 - hint_surf.get_width() // 2, 150))

        if easter_egg_timer > 0:
            easter_egg_surf = font.render(easter_egg_text, True, (0, 0, 0))
            screen.blit(
                easter_egg_surf,
                (16, SCREEN_HEIGHT - easter_egg_surf.get_height() - 16)
            )

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    asyncio.run(main())