import pygame
from enum import Enum

class Direction(Enum):
    LEFT = 1
    RIGHT = 2

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image =  pygame.transform.scale(image, (40, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collideRect = pygame.Rect(x, y, 40, 20)
        self.speed = 3
        self.ticksMoving = 1

    def moving(self):
        self.ticksMoving += 1
        self.rect.x += self.speed
        self.collideRect.x = self.rect.x

