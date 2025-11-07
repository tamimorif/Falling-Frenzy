from pathlib import Path
from enum import Enum
from typing import Tuple

ROOT_DIR = Path(__file__).parent.parent
ASSETS_DIR = ROOT_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
FONTS_DIR = ASSETS_DIR / "fonts"
DATA_DIR = ROOT_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

HIGHSCORE_FILE = DATA_DIR / "highscore.txt"
SETTINGS_FILE = DATA_DIR / "settings.json"
STATISTICS_FILE = DATA_DIR / "statistics.json"

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
FPS = 60
GAME_TITLE = "Falling Frenzy"

BASKET_WIDTH = 100
BASKET_HEIGHT = 20
BASKET_SPEED = 15
BASKET_Y_OFFSET = 10

OBJECT_WIDTH = 40
OBJECT_HEIGHT = 40
OBJECT_BASE_SPEED = 5
OBJECT_SPAWN_DELAY = 1000
OBJECT_MAX_SPEED = 15
OBJECT_SPEED_INCREMENT = 0.1
SPAWN_POSITION_VARIANCE = 3

STARTING_SCORE = 10
MISS_PENALTY = 1
BOMB_DAMAGE = 3
COMBO_MULTIPLIER = 1.5
COMBO_TIMEOUT = 2000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 60, 60)
GREEN = (60, 255, 100)
YELLOW = (255, 220, 60)
BLUE = (60, 120, 255)
PURPLE = (180, 60, 255)
ORANGE = (255, 140, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
LIGHT_BLUE = (100, 180, 255)
GOLD = (255, 215, 0)

BG_COLOR_TOP = (20, 20, 40)
BG_COLOR_BOTTOM = (60, 40, 80)

class ObjectType(Enum):
    RED = ("red", RED, 1, False)
    GREEN = ("green", GREEN, 2, False)
    YELLOW = ("yellow", YELLOW, 3, False)
    PURPLE = ("purple", PURPLE, 5, False)
    BOMB = ("bomb", BLACK, -3, True)
    
    def __init__(self, name, color, points, is_bomb):
        self.object_name = name
        self.color = color
        self.points = points
        self.is_bomb = is_bomb

class GameState(Enum):
    MAIN_MENU = "main_menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    STATISTICS = "statistics"
    SETTINGS = "settings"

POWERUP_DURATION = 5000
POWERUP_SPAWN_CHANCE = 0.05

class PowerUpType(Enum):
    SLOW_MOTION = ("slow_mo", LIGHT_BLUE, 0.5)
    DOUBLE_POINTS = ("double_points", GOLD, 2.0)
    SHIELD = ("shield", PURPLE, 1.0)
    MAGNET = ("magnet", ORANGE, 1.0)
    
    def __init__(self, name, color, effect_value):
        self.powerup_name = name
        self.color = color
        self.effect_value = effect_value

PARTICLE_COUNT = 10
PARTICLE_LIFETIME = 500
PARTICLE_SPEED_MIN = 2.0
PARTICLE_SPEED_MAX = 5.0
PARTICLE_SIZE_MIN = 2
PARTICLE_SIZE_MAX = 6

ANIMATION_SPEED = 0.2
SHAKE_MAGNITUDE = 5
SHAKE_DURATION = 200

FONT_SMALL = 24
FONT_MEDIUM = 36
FONT_LARGE = 72
FONT_TITLE = 100

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
BUTTON_RADIUS = 10
BUTTON_PADDING = 20

DEFAULT_VOLUME = 0.7
MUSIC_VOLUME = 0.5

DIFFICULTY_INCREASE_INTERVAL = 10
SPAWN_DELAY_MIN = 500
SPAWN_DELAY_DECREASE = 50

STATS_GAME_PLAYED = "games_played"
STATS_TOTAL_SCORE = "total_score"
STATS_TOTAL_TIME = "total_time_seconds"
STATS_BEST_COMBO = "best_combo"
STATS_OBJECTS_CAUGHT = "objects_caught"
STATS_OBJECTS_MISSED = "objects_missed"
