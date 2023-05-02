import pygame
from enum import Enum
from assets.objects.player import  Direction

class Direction(Enum):
    LEFT = 1
    RIGHT = 2

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_bounding_rect()
        self.rect.size
        self.rect.center = (x, y)

        self.moving = False
        self.isSpawned = False

        self.SPEED = 1
        self.GRAVITY = 2
        self.JUMP_SPEED = 4
        self.JUMP_LENGTH_IN_TICKS = 60
        self.FALL_LENGTH_IN_TICKS = 40
        
        
    
    def Activate(self, spawn):
        if spawn != self.isSpawned:
            self.moving = True

    def UpdateEnemy(self,playerSpeed = 0, direction = None):
        if self.moving == True:
            if direction is None or direction == Direction.RIGHT:
                self.rect.x -= self.SPEED
            else:
                self.rect.x += self.SPEED - playerSpeed


        print("ENEMY POS: " + str(self.rect.x))


    def ActiveSprite(self, image):
        self.image =  image

