import pygame
from assets.sprites.objects.rectangle import Rectangle, Direction

class Engine():
    def __init__(self, screen, currentLevel, screen_width, screen_height , playerImages:list):
        self.screen = screen
        self.screen_width = screen_width
        self.currentLevel = currentLevel
        self.font = pygame.font.Font(None, 36)
        self.font_color = (0, 0, 0)
        menu_text = self.font.render("Menu", True, self.font_color)
        self.menu_rect = menu_text.get_rect(center=(self.screen_width/2, 100))
        self.bg_color = (255, 255, 255)
        self.startingX = 200
        self.startingY = 400
        self.playerImages = playerImages
        self.player = Rectangle(self.startingX, self.startingY, self.playerImages[1])
        

    def runGame(self):
        engineOn = True
        self.objects = pygame.sprite.Group()
        self.objects.add(self.player)
        while engineOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    


            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.player.rect.right < self.screen_width:
                self.player.Action(True, Direction.RIGHT)
                self.player.ActiveSprite(self.playerImages[1])
            if keys[pygame.K_LEFT] or keys[pygame.K_a] and self.player.rect.left > 0:
                self.player.Action(True, Direction.LEFT)
                self.player.ActiveSprite(self.playerImages[0])

            self.draw(self.objects)
            

    def draw(self, objects):
        # Clear the screen
        self.screen.fill("black")

        objects.draw(self.screen)

        # Update the display
        pygame.display.update()



    
