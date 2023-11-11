import pygame
import sys
from assets.objects.player import Player, Direction
from assets.objects.platform import StartPlatform, Platform, EndPlatform
from core.helpers.backgroundManager import BackgroundManager
from core.helpers.backgroundLayer import BackgroundLayer
from assets.objects.enemy import Enemy
from assets.objects.fruit import Fruit
from core.helpers.collideHelper import CollisionDetection
from core.helpers.soundManager import SoundManager

class LevelBuilder:
    def __init__(self, currentLevel, screen_width, screen_height, tile_size):
        self.filename = f"lvl{currentLevel}.txt"
        self.width = screen_width
        self.height = screen_height
        self.tile_size = tile_size

    def load_level(self):
        with open(self.filename, 'r') as file:
            level_data = []
            for line in file:
                row = []
                for char in line.strip():
                    # Add your character checking logic here
                    row.append(char)
                level_data.append(row)
            return level_data

    def draw_level(self, screen, platform_images):
        pass

# - 100px empty
# [ start platform 
# - 100px platform
# ]  end platform
# * fruit 
# X enemy 
# < start level 
# > end level