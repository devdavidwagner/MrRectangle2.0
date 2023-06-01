# Import standard modules.
import sys
 
# Import non-standard modules.
import pygame
from pygame.locals import *

from core.stateManager import State, GameState
from core.screens.menu import Menu
from core.screens.levelManager import LevelManager, Level
from core.screens.death import Death
from core.screens.win import Win

def update(dt):
  """
  Update game. Called once per frame.
  dt is the amount of time passed since last frame.
  If you want to have constant apparent movement no matter your framerate,
  what you can do is something like
  
  x += v * dt
  
  and this will scale your velocity based on time. Extend as necessary."""
  
  # Go through events that are passed to the script by the window.
  for event in pygame.event.get():
    # We need to handle these events. Initially the only one you'll want to care
    # about is the QUIT event, because if you don't handle it, your game will crash
    # whenever someone tries to exit.
    if event.type == QUIT:
      pygame.quit() # Opposite of pygame.init
      sys.exit() # Not including this line crashes the script on Windows. Possibly
      # on other operating systems too, but I don't know for sure.
    # Handle other events as you wish.
 
def draw(screen):
  """
  Draw things to the window. Called once per frame.
  """
  screen.fill((0, 0, 0)) # Fill the screen with black.
  
  # Redraw screen here.
  
  # Flip the display so that the things we drew actually show up.
  pygame.display.flip()
 
def runPyGame():
  # Initialise PyGame.
  pygame.init()
  
  # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
  fps = 60.0
  fpsClock = pygame.time.Clock()
  
  # Set up the window.
  screen_width = 800
  screen_height = 600
  screen = pygame.display.set_mode((screen_width, screen_height))
  
  # screen is the surface representing the window.
  # PyGame surfaces can be thought of as screen sections that you can draw onto.
  # You can also draw surfaces onto other surfaces, rotate surfaces, and transform surfaces.
  currentState = State.MENU

  # Main game loop.
  dt = 1/fps # dt is the time since last frame.
  menu_options = ["Start Game", "Controls", "About", "Quit Game"]
  menu = Menu(menu_options, screen_width)

  currentLevel = Level.ONE
  levelMan = LevelManager(Level.ONE, screen, screen_width, screen_height)
  deadImg = pygame.image.load("assets\sprites\dead.png").convert_alpha()
  deathScreen = Death(screen_width, screen_height, deadImg)
  winImg = pygame.image.load("assets\sprites\win.png").convert_alpha()
  winBg = pygame.image.load("assets\sprites\para0.png").convert_alpha()
  winScreen = Win(screen_width, screen_height,winImg, winBg)
  isAlive = True
  gameState = GameState()
  
  while True: # Loop forever!
    gameState.get_instance()

    if gameState.state == State.MENU:
      #run menu  
      menu.draw(screen)
      menu.render_options()

    if gameState.state == State.GAME:
      #run level 1   
      levelMan.reset()
      levelMan.runLevel()
    
    if gameState.state == State.DEATH:
      deathScreen.display(screen)
      deathScreen.handle_event(event,screen)

    if gameState.state == State.WIN:
      winScreen.display(screen)
      winScreen.handle_event(event,screen)

    #events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

      if gameState.state == State.MENU:
          menu.handle_event(event, screen)

    
    dt = fpsClock.tick(fps)


