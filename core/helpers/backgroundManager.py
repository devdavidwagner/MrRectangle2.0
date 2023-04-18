import pygame
from core.helpers.backgroundLayer import BackgroundLayer
from assets.sprites.objects.rectangle import Direction

class BackgroundManager(pygame.sprite.Sprite):
    def __init__(self, player, screen, screen_width, parallaxImages):
        self.player = player
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = 600
        self.parallaxImages = parallaxImages
        
        # Set up the background layers
        self.background_0 = BackgroundLayer(0,0, self.screen, self.screen_width, self.screen_height, self.screen_width, self.parallaxImages[0], 0)
        self.background_1 = BackgroundLayer(0,0,self.screen, 400, 600, self.screen_width, self.parallaxImages[1], self.player.SPEED)
        self.background_1_ahead = BackgroundLayer(self.screen_width, 0, self.screen, 400, 600,  self.screen_width, self.parallaxImages[1], self.player.SPEED)
        self.background_1_behind = BackgroundLayer(-self.screen_width, 0, self.screen, 400, 600,  self.screen_width, self.parallaxImages[1], self.player.SPEED)
        self.backgrounds = [self.background_0, self.background_1, self.background_1_ahead, self.background_1_behind]

    def draw(self, screen):
        screen.blit(self.background_0.image, self.background_0.rect)
        screen.blit(self.background_1.image, self.background_1.rect)
        screen.blit(self.background_1_ahead.image, self.background_1_ahead.rect)
        screen.blit(self.background_1_behind.image, self.background_1_behind.rect)

    def update(self, direction, noMovement):
        # Move the background layers based on the player's position
        player_x = self.player.rect.x
        screen_center_x = self.screen_width // 2

        # Move the main background layer
        self.background_1.move(direction)

        # Move the extra layers depending on the player's position relative to the screen center
        if player_x > screen_center_x:
            # Player is to the right of the screen center, so move the "ahead" layer to the left of the main layer
            self.background_1_ahead.rect.x = self.background_1.rect.right
            self.background_1_ahead.move(Direction.LEFT)

            # If the "behind" layer is off the screen to the left, move it to the right of the main layer
            if self.background_1_behind.rect.right < 0:
                self.background_1_behind.rect.x = self.background_1.rect.right
                self.background_1_behind.move(Direction.RIGHT)
        else:
            # Player is to the left of the screen center, so move the "behind" layer to the right of the main layer
            self.background_1_behind.rect.right = self.background_1.rect.left
            self.background_1_behind.move(Direction.RIGHT)

            # If the "ahead" layer is off the screen to the right, move it to the left of the main layer
            if self.background_1_ahead.rect.left > self.screen_width:
                self.background_1_ahead.rect.right = self.background_1.rect.left
                self.background_1_ahead.move(Direction.LEFT)

        # Update all the background layers
        for bg in self.backgrounds:
            bg.update(direction, noMovement)
