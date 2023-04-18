import pygame
from assets.sprites.objects.rectangle import Direction
from core.helpers.collideHelper import CollisionDetection

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image: pygame.image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 2
        self.customDetect = CollisionDetection()
    
    def move(self, direction):       
        if direction == Direction.LEFT:
            self.rect.x += self.speed
        if direction == Direction.RIGHT:
            self.rect.x -= self.speed

    def update(self, onPlatform, playerRect, direction = Direction.RIGHT, noMovement = False):
            if not noMovement:
                self.move(direction)