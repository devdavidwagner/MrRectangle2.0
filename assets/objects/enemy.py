import pygame
import time
from enum import Enum
from assets.objects.player import  Direction

class Direction(Enum):
    LEFT = 1
    RIGHT = 2

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, allImages, score):
        super().__init__()
        self.image = image
        self.rect = self.image.get_bounding_rect()
        self.rect.size
        self.rect.center = (x, y)
        self.score = score
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
        self.dying = False
        self.dead = False
        self.dyingTicks = 0
        self.splatSet = False
        self.splatTicks = 0
        self.playSound = True
        self.font = pygame.font.Font(None, 50)
        self.scoreTicks = 0

        self.text_rect = self.rect
        self.text_rect.center = (x, y)

        self.initX = 0
        self.initY = 0
        self.activated = False
        
    def reset(self):

        self.moving = False
        self.isSpawned = False

        self.SPEED = 2
        self.SPEED_RIGHT = 3
        self.SPEED_LEFT = 3
        self.GRAVITY = 2
        self.JUMP_SPEED = 4
        self.JUMP_LENGTH_IN_TICKS = 60
        self.FALL_LENGTH_IN_TICKS = 40
        self.movingTicks = 0
        self.dying = False
        self.dead = False
        self.dyingTicks = 0
        self.splatSet = False
        self.splatTicks = 0
        self.playSound = True
        self.scoreTicks = 0


    def LoadImages(self, images):
        self.enemyImages = images    
    
    def Activate(self):
        self.moving = True
        self.activated = True
            
    def UpdateEnemyRight(self,speed):
        self.movingTicks += 1
        self.rect.x -= self.SPEED_LEFT    
       # self.rect.x += self.SPEED / 2

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
        if self.movingTicks % 20 == 1:
            self.rect.x -= self.SPEED   
        if self.movingTicks > 20 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[0])
        if self.movingTicks > 80 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[1])
        if self.movingTicks > 160 and len(self.enemyImages)> 0:
            self.ActiveSprite(self.enemyImages[2])
        if  self.movingTicks > 240 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[0])
            
    def SetSplat(self, set):
        self.splatSet = set

    def display_enemy_score(self,screen, score):
        text = self.font.render(f"+{score}", True, "GREEN")
        if self.scoreTicks % 4 == 2:
            text = self.font.render(f"+{score}!", True, "RED")
        self.scoreTicks += 1
        screen.blit(text, self.text_rect)
        
    def UpdateEnemy(self,speed):
        self.movingTicks += 1
        self.rect.x -= self.SPEED / 2    
    

        if self.movingTicks > 20 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[0])
        if self.movingTicks > 80 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[1])
        if self.movingTicks > 160 and len(self.enemyImages)> 0:
            self.ActiveSprite(self.enemyImages[2])
        if  self.movingTicks > 240 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[0])
            self.movingTicks = 0

    def Hit(self):
        self.dying = True

    def Dying(self):
        self.rect.y += 2  
        self.dyingTicks += 1
        if self.dyingTicks > 0 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[3])
        if self.dyingTicks > 120 and len(self.enemyImages) > 0:
            self.ActiveSprite(self.enemyImages[4])
        if self.dyingTicks > 240 and len(self.enemyImages)> 0:
            self.ActiveSprite(self.enemyImages[5])
            self.dyingTicks = 0
            self.dead = True
            self.dying = False

    def ActiveSprite(self, image):
        self.image =  image

