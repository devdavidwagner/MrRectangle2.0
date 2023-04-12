import pygame
from enum import Enum

class Direction(Enum):
    LEFT = 1
    RIGHT = 2

class Rectangle(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.moving = False
        self.ticks = 1
        

    def Action(self, moving, direction):
        self.ticks += 1
        if moving and direction == direction.RIGHT and self.ticks > 4:
            self.rect.x += self.speed 
        if moving and direction == direction.LEFT and self.ticks > 4:
            self.rect.x -= self.speed 

        if self.ticks > 4:
            self.ticks = 0

        print("Player X = " + str(self.rect.x))
        print("Player TICK = " + str(self.ticks))
        


    def ActiveSprite(self, image):
        self.image =  pygame.transform.scale(image, (40, 80))