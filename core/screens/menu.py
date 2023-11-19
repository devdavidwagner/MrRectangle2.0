import pygame
from core.stateManager import State
from core.stateManager import State, GameState

class Menu:
    def __init__(self, screen_width, screen_height, width,height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fontMain = pygame.font.Font(None, 56)
        self.font = pygame.font.Font(None, 46)
        self.font_color = (0,250,154)  # light green
        self.bg_color = (255, 255, 255)
        self.option_rects = []
        self.menu_rect = pygame.Rect((screen_width / 2) - width / 4, screen_height /2, width, height)
        self.highScoreRect = pygame.Rect(screen_width / 2, (screen_height /2) + height, width, height)
        self.selected = 0
        self.background_image = pygame.image.load("assets\sprites\mainMenu.png")

        # Set up flashing variables
        self.flash_interval = 250  # in milliseconds
        self.last_flash_time = pygame.time.get_ticks()
        self.flash_color = (0,255,0)
        self.highScore = self.load_high_score()


    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                high_score_str = file.read()
                if high_score_str.isdigit():
                    high_score = int(high_score_str)
                    print("High score loaded successfully:", high_score)
                    return high_score
                else:
                    print("Invalid high score format in the file.")
                    return None
        except IOError as e:
            print("Error loading high score:", str(e))
            return None

    def draw(self, screen):
         # Check if it's time to toggle the flash color
        current_time = pygame.time.get_ticks()
        if current_time - self.last_flash_time >= self.flash_interval:
            self.last_flash_time = current_time
            if self.flash_color == (0,250,154):
                self.flash_color = (255,255,0)  # yellow
            else:
                self.flash_color = (0,250,154)  # light green
        # Clear the screen
        screen.blit(self.background_image, (0, 0))
        # Render and draw the flashing text
        text_surface = self.fontMain.render("Press Enter to Start!", True, self.flash_color)
        menu_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(text_surface, menu_rect)
        screen.blit(self.font.render("High Score: " + str(self.highScore), True, self.font_color), self.highScoreRect)

        # Update the display
        pygame.display.update()

    def handle_event(self, event, screen):
        currentState = GameState.get_instance()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.selected == 0:
                    # Start the game
                    currentState.state = State.GAME

        self.draw(screen)
