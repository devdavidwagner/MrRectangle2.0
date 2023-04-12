import pygame
from core.stateManager import State

class Menu:
    def __init__(self, options, screen_width):
        self.options = options
        self.screen_width = screen_width
        self.font = pygame.font.Font(None, 36)
        self.font_color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.option_rects = []
        self.menu_rect = None
        self.selected = 0

        self.render_options()

    def render_options(self):
        # Clear the option rects list
        self.option_rects = []

        # Render each option and store its rect
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, self.font_color)
            rect = text.get_rect(center=(self.screen_width/2, 200 + i*50))
            self.option_rects.append(rect)

        # Render the menu text and store its rect
        menu_text = self.font.render("Menu", True, self.font_color)
        self.menu_rect = menu_text.get_rect(center=(self.screen_width/2, 100))

    def draw(self, screen):
        # Clear the screen
        screen.fill(self.bg_color)

        # Draw the menu options
        screen.blit(self.font.render("Menu", True, self.font_color), self.menu_rect)
        for i, rect in enumerate(self.option_rects):
            if i == self.selected:
                pygame.draw.rect(screen, (100, 100, 100), rect, 5)
            screen.blit(self.font.render(self.options[i], True, self.font_color), rect)

        # Update the display
        pygame.display.update()

    def handle_event(self, event, screen):
        currentState = State.MENU
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected -= 1
                if self.selected < 0:
                    self.selected = len(self.options) - 1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected += 1
                if self.selected == len(self.options):
                    self.selected = 0
            elif event.key == pygame.K_RETURN:
                if self.selected == 0:
                    # Start the game
                    currentState = State.GAME
                elif self.selected == 1:
                    # Show the instructions
                    pass
                elif self.selected == 2:
                    # Quit the game
                    pygame.quit()

        self.draw(screen)

        return currentState