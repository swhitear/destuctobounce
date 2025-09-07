import yaml
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (120, 120, 120)
COLOR_YELLOW = (255, 255, 0)
ORB_SPEED = 7
ORB_RADIUS = 5
ORB_COLOR = COLOR_WHITE
BLOCK_WIDTH = 40
BLOCK_HEIGHT = 20
BLOCK_PADDING = 2
BLOCK_COLOR = COLOR_GREY

class Config:
    # Defaults
    SCREEN_WIDTH = SCREEN_WIDTH
    SCREEN_HEIGHT = SCREEN_HEIGHT
    FPS = FPS
    COLOR_BLACK = COLOR_BLACK
    COLOR_WHITE = COLOR_WHITE
    COLOR_GREY = COLOR_GREY
    COLOR_YELLOW = COLOR_YELLOW
    ORB_SPEED = ORB_SPEED
    ORB_RADIUS = ORB_RADIUS
    ORB_COLOR = ORB_COLOR
    BLOCK_WIDTH = BLOCK_WIDTH
    BLOCK_HEIGHT = BLOCK_HEIGHT
    BLOCK_PADDING = BLOCK_PADDING
    BLOCK_COLOR = BLOCK_COLOR

    def __init__(self, yaml_path=None):
        if yaml_path and os.path.exists(yaml_path):
            with open(yaml_path, "r") as f:
                data = yaml.safe_load(f)
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
