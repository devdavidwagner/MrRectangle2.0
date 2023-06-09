import pygame

class Splat(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.DEFAULT_IMAGE_SIZE_VAL = 75
        self.DEFAULT_IMAGE_SIZE = (100, 100)
        self.image = pygame.transform.scale(image, self.DEFAULT_IMAGE_SIZE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.collideRect = pygame.Rect(x, y, 100, 100)
        self.splatTicks = 0

  
    def move(self,x,y):
        self.rect.topleft = (x, y)
        self.splatTicks += 1

    def ActiveSprite(self, image):
        self.image =  pygame.transform.scale(image, self.DEFAULT_IMAGE_SIZE)
    
