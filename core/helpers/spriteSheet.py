import pygame

class SpriteSheet(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path):
        super().__init__()
        self.sprite_sheet_path = sprite_sheet_path

    def load_image(self, x,y,width,height):       
        sprite_sheet = pygame.image.load(self.sprite_sheet_path)
        sprite_rect = pygame.Rect(x, y, width, height)
        sprite_image = sprite_sheet.subsurface(sprite_rect)
        return sprite_image
