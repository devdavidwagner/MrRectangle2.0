import pygame
from core.helpers.backgroundLayer import BackgroundLayer
from assets.objects.player import Direction

class BackgroundManager():
    def __init__(self, player, screen, height, screen_width, parallaxImage, speed):
        super().__init__()
        self.player = player
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = 600
        self.parallaxImage = parallaxImage
        self.backgroundSpeed = speed
        self.image = pygame.Surface((self.screen_width, self.screen_height))
        self.rect = self.image.get_rect()
        self.background_1 = BackgroundLayer(0,0,self.screen, self.screen_width, height, self.screen_width, self.parallaxImage, speed)
        self.background_2= BackgroundLayer(self.screen_width, 0, self.screen, self.screen_width, height,  self.screen_width, self.parallaxImage, speed)
        self.background_3 = BackgroundLayer(-self.screen_width, 0, self.screen, self.screen_width, height,  self.screen_width, self.parallaxImage, speed)
        self.backgrounds = [self.background_1, self.background_2, self.background_3]

    # def draw(self, screen):
    #     screen.blit(self.background_1.image, self.background_1.rect)
    #     screen.blit(self.background_2.image, self.background_2.rect)
    #     screen.blit(self.background_3.image, self.background_3.rect)

    def update(self, direction, noMovement, object_distance_speed):
        # Move the background layers based on the player's position
        player_x = self.player.rect.x
        screen_center_x = self.screen_width // 2
        # Move the main background layer
        self.background_1.move(direction, object_distance_speed)
           # Check if the background has gone off the screen and move it to the opposite side of the screen
        if self.background_1.rect.right < 0:
            self.background_1.rect.left = self.background_3.rect.right
        elif self.background_1.rect.left > self.screen_width:
            self.background_1.rect.right = self.background_2.rect.left

        self.background_2.rect.left = self.background_1.rect.right
        self.background_3.rect.right = self.background_1.rect.left
        
           

        # Update all the background layers
        for bg in self.backgrounds:            
                bg.update(direction, noMovement, object_distance_speed)

        # Check if the first background has gone off the screen
        if self.background_1.rect.right < 0:
            # Move the first background to the right of the third background
            self.background_1.rect.left = self.background_3.rect.right
            # Swap the positions of the backgrounds
            self.background_1, self.background_2, self.background_3 = self.background_2, self.background_3, self.background_1

        if self.background_1.rect.left > self.screen_width:
            # Move the first background to the right of the third background
            self.background_1.rect.right = self.background_2.rect.left
            # Swap the positions of the backgrounds
            self.background_1, self.background_2, self.background_3 = self.background_2, self.background_3, self.background_1

