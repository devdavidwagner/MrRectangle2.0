import pygame
from assets.sprites.objects.rectangle import Direction

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
     
    
    def Move(self, speed, direction):
        if direction == Direction.RIGHT:
            self.rect.x -= speed
        if direction == Direction.LEFT:
            self.rect.x += speed