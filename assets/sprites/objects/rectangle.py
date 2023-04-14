import pygame
from enum import Enum

class Direction(Enum):
    LEFT = 1
    RIGHT = 2

class Rectangle(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


        self.moving = False
        self.jumping = False
        self.fallAfterJump = False
        self.falling = False
        self.ticksJumping = 0
        self.ticksFallingAfterJump = 0
        self.ticks = 1

        self.SPEED = 1
        self.GRAVITY = 1
        self.JUMP_SPEED = 4
        self.JUMP_LENGTH_IN_TICKS = 40
        self.FALL_LENGTH_IN_TICKS = 40
        
        

    def Action(self, moving, direction = Direction.RIGHT, falling = False, initJump = False):
        self.ticks += 1
        # if moving and direction == direction.RIGHT and self.ticks > 4:
        #     self.rect.x += self.SPEED 
        # if moving and direction == direction.LEFT and self.ticks > 4:
        #     self.rect.x -= self.SPEED 

    
        self.moving = moving
        self.falling = falling
            

        if initJump == True:
            self.jumping = initJump
            

        if self.fallAfterJump and self.ticks % 30 == 2 and not self.falling:
            self.ticksFallingAfterJump += 1
            self.rect.y += self.GRAVITY
        
        if self.falling and not self.jumping:
            self.rect.y += self.GRAVITY

            
        if self.jumping == True and self.ticks % 40 == 2:
            self.ticksJumping += 1
            self.rect.y -= self.JUMP_SPEED - self.GRAVITY

        if self.ticksJumping >= self.JUMP_LENGTH_IN_TICKS:
            self.jumping = False
            self.falling = True
            self.ticksJumping = 0

        if self.ticksFallingAfterJump >= self.FALL_LENGTH_IN_TICKS:
            self.fallAfterJump = False
            self.ticksFallingAfterJump = 0

        # print("Player X = " + str(self.rect.x))
        # print("Player TICK = " + str(self.ticks))
        


    def ActiveSprite(self, image):
        self.image =  pygame.transform.scale(image, (40, 80))