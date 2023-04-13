import pygame
from assets.sprites.objects.rectangle import Direction

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image: pygame.image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        
        self.rectCollide = pygame.rect.Rect((0,0), (self.image.get_width(), self.image.get_height()))
        self.rectCollide.center = self.rect.center
    
    def Move(self, speed, direction):
        if direction == Direction.RIGHT:
            self.rect.x -= speed
        if direction == Direction.LEFT:
            self.rect.x += speed