import os
import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60
TILE_SIZE = 32

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FONT_PATH = os.path.join(BASE_DIR, "assets", "fonts", "BoldPixels.ttf")
DEFAULT_FONT_SIZE = 28

pygame.font.init()
DEFAULT_FONT = pygame.font.Font(FONT_PATH, DEFAULT_FONT_SIZE)

GAMESTATE_TITLE = "title"
GAMESTATE_OVERWORLD = "overworld"
GAMESTATE_INVENTORY = "inventory"
GAMESTATE_DIALOGUE = "dialogue"
GAMESTATE_COMBAT = "combat"
GAMESTATE_PAUSE = "pause"

