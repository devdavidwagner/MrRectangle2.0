import pygame
from enum import Enum

class Direction(Enum):
    LEFT = 1
    RIGHT = 2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.moving = False
        self.jumping = False
        self.shooting = False
        self.fallAfterJump = False
        self.falling = False
        self.ticksJumping = 1
        self.ticksFallingAfterJump = 1
        self.ticks = 1
        self.shootingTicks = 1
        self.projectilesFired = 0

        self.SPEED = 4
        self.GRAVITY = 2
        self.JUMP_SPEED = 5
        self.JUMP_LENGTH_IN_TICKS = 60
        self.FALL_LENGTH_IN_TICKS = 40
        self.SHOOTING_LENGTH_IN_TICKS = 100
        
        

    def Action(self, moving, direction = Direction.RIGHT, falling = False, initJump = False, shooting = False):  
        self.moving = moving
        self.falling = falling
        self.shooting = shooting
        self.ticks += 1

        if shooting:
            self.shootingTicks += 1
        
        if self.SHOOTING_LENGTH_IN_TICKS < self.shootingTicks:
            shooting = False
            self.shootingTicks = 0
            
        if initJump == True and not self.jumping and not self.falling:
            self.jumping = initJump
                   
        if self.falling and not self.jumping or self.fallAfterJump:
            self.rect.y += self.GRAVITY

        if self.ticks % 20 == 1:
            
            if self.jumping == True:
                self.ticksJumping += 1
                self.rect.y -= self.JUMP_SPEED - self.GRAVITY

            if self.JUMP_LENGTH_IN_TICKS % self.ticksJumping == 1:
                self.jumping = False
                self.fallAfterJump = True
                self.ticksJumping = 1

            if  self.fallAfterJump:
                self.ticksFallingAfterJump += 1
                self.rect.y += self.GRAVITY

            if self.FALL_LENGTH_IN_TICKS % self.ticksFallingAfterJump  == 1:
                self.fallAfterJump = False
                self.ticksFallingAfterJump = 1
        


    def ActiveSprite(self, image):
        self.image =  pygame.transform.scale(image, (40, 80))

