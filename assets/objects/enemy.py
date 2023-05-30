import pygame
import time
from enum import Enum
from assets.objects.player import  Direction

class Direction(Enum):
    LEFT = 1
    RIGHT = 2

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, allImages):
        super().__init__()
        self.image = image
        self.rect = self.image.get_bounding_rect()
        self.rect.size
        self.rect.center = (x, y)

        self.moving = False
        self.isSpawned = False
        self.originX = x
        self.originY = y

        self.SPEED = 2
        self.SPEED_RIGHT = 3 
        self.SPEED_LEFT = 3
        self.GRAVITY = 2
        self.JUMP_SPEED = 4
        self.JUMP_LENGTH_IN_TICKS = 60
        self.FALL_LENGTH_IN_TICKS = 40
        self.movingTicks = 0
        self.enemyImages = allImages
        

    def LoadImages(self, images):
        self.enemyImages = images    
    
    def Activate(self, spawn):
        if spawn != self.isSpawned:
            self.moving = True\
            
    def UpdateEnemyRight(self,speed):
        self.movingTicks += 1
        self.rect.x -= self.SPEED_RIGHT
       # self.rect.x += self.SPEED
        if self.rect.x < 0:
            self.rect.x = self.originX

        if self.movingTicks > 20 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[0])
        if self.movingTicks > 80 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[1])
        if self.movingTicks > 160 and len(self.enemyImages)> 0:
            self.ActiveSprite(self.enemyImages[2])
        if  self.movingTicks > 240 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[0])
            self.movingTicks = 0

    def UpdateEnemyLeft(self,speed):
        self.movingTicks += 1
        self.rect.x -= self.SPEED_RIGHT
        self.rect.x += self.SPEED

        if self.rect.x < 0:
            self.rect.x = self.originX

        if self.movingTicks > 20 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[0])
        if self.movingTicks > 80 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[1])
        if self.movingTicks > 160 and len(self.enemyImages)> 0:
            self.ActiveSprite(self.enemyImages[2])
        if  self.movingTicks > 240 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[0])
            self.movingTicks = 0

    def UpdateEnemy(self,speed):
        self.movingTicks += 1
        self.rect.x -= self.SPEED_LEFT    
        self.rect.x += self.SPEED
        if self.rect.x < 0:
            self.rect.x = self.originX

        if self.movingTicks > 20 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[0])
        if self.movingTicks > 80 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[1])
        if self.movingTicks > 160 and len(self.enemyImages)> 0:
            self.ActiveSprite(self.enemyImages[2])
        if  self.movingTicks > 240 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[0])
            self.movingTicks = 0


    def ActiveSprite(self, image):
        self.image =  image

