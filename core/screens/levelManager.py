from enum import Enum
from core.engine import Engine
import pygame


class MySprite(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Level(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4

inGame = True
class LevelManager():
    def __init__(self, currentLevel, screen, screen_width, screen_height):
        self.currentLevel = currentLevel
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
       


        imageCharStillLeft = pygame.image.load("assets\sprites\RectangleStillLeft.png").convert_alpha()
        imageCharStillRight = pygame.image.load("assets\sprites\RectangleStillRight.png").convert_alpha()      
        imagecharMoveLeft = pygame.image.load("assets\sprites\RectangleStillLeft.png").convert_alpha()
        imageCharMoveRight = pygame.image.load("assets\sprites\RectangleStillRight.png").convert_alpha()
        

        self.playerImages = [imageCharStillLeft, imageCharStillRight, imagecharMoveLeft, imageCharMoveRight]
        self.engine = Engine(self.screen, self.currentLevel, self.screen_width, self.screen_height, self.playerImages)











    def runLevel(self):
        self.engine.runGame()
