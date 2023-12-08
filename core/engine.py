import pygame
import time
from assets.objects.player import Player, Direction
from assets.objects.enemy import Enemy
from assets.objects.platform import Platform
from core.stateManager import State, GameState
from core.helpers.collideHelper import CollisionDetection
from core.helpers.backgroundManager import BackgroundManager
from core.helpers.soundManager import SoundManager
from core.helpers.backgroundLayer import BackgroundLayer
from core.helpers.levelBuilder import LevelBuilder
from assets.objects.endPlatform import EndPlatform
from assets.objects.startPlatform import StartPlatform
from assets.objects.projectile import Projectile
from assets.objects.splat import Splat
from assets.objects.fruit import Fruit
from assets.objects.jumpBlock import JumpBlock
from assets.objects.diamond import Diamond
from assets.objects.playerLife import PlayerrLIfe

class Engine():
    def __init__(self, screen, currentLevel, screen_width, screen_height , playerImages:list, platformImages:list, parallaxImages:list, enemyImages:list, fruitImages:list, effectImages:list, soundEffects:list, jumpBlockImages:list, diamondImages:list, playerImagesUpgrade1:list):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.currentLevel = currentLevel
        self.ticks = 1
        self.font = pygame.font.Font(None, 36)
        self.bg_color = (255, 255, 255)
        self.startingX = (screen_width / 2) - 100
        self.endingX = 6000
        self.startingY = 200
        self.startingY_StartPlatform = 200
        self.startingXPlayer = (screen_width / 2) + 50
        self.startingYPlayer = self.startingY - 64
        self.playerImages = playerImages
        self.platformImages = platformImages
        self.effectImages = effectImages
        gameState = GameState.get_instance()
        self.playerImagesUpgrade1 = playerImagesUpgrade1
        self.player = Player(self.startingXPlayer, self.startingYPlayer, self.playerImages[1], self.playerImages, gameState.get_score(), self.playerImagesUpgrade1)
        
        self.level_builder = LevelBuilder(currentLevel, screen_width, screen_height, 40)
        self.levelData = self.level_builder.load_level()
        

        self.startPlatform = None
        self.endPlatform = None
        self.platforms = []
        self.enemies = []
        self.fruits = []
        self.jumpBlocks = []
        self.diamonds = []
        
        self.fruitImages = fruitImages
        self.enemyImages = enemyImages

        self.enemyGroup = []

        self.jumpBlockImages = jumpBlockImages

        
        self.noMovement = False

        self.parallaxImages = parallaxImages

        self.cloudSpeed = 350
        self.backgroundSpeed = 300
        self.backgroundSpeed2 = 250
        #background
        self.background_0 = BackgroundLayer(0,0,self.screen, self.screen_width, self.screen_height, self.screen_width, self.parallaxImages[0], 0)

        #parallax foregound
        self.backgroundManagerCloud = BackgroundManager(self.player, self.screen, 200, self.screen_width, self.parallaxImages[1], self.cloudSpeed)
        self.backgroundManagerHill = BackgroundManager(self.player, self.screen,  self.screen_height, self.screen_width, self.parallaxImages[2], 2)
        self.backgroundManagerMtn = BackgroundManager(self.player, self.screen,  self.screen_height, self.screen_width, self.parallaxImages[3], 3)
        

        self.projectileImage = self.playerImages[18]
        self.projectilesInAir = []

        self.diamondImages = diamondImages
        self.diamonds = []

        self.playerImageLeftStill = self.playerImages[0]
        self.playerImageRightStill = self.playerImages[1]
        self.playerImageLeftMoving = self.playerImages[2] 
        self.playerImageLeftMoving2 = self.playerImages[3] 
        self.playerImageLeftMoving3 = self.playerImages[4] 
        self.playerImageRightMoving = self.playerImages[5]
        self.playerImageRightMoving2 = self.playerImages[6]
        self.playerImageRightMoving3 = self.playerImages[7]
        self.playerImageLeftJumping = self.playerImages[8] 
        self.playerImageLeftJumping2 = self.playerImages[9] 
        self.playerImageLeftJumping3 = self.playerImages[10] 
        self.playerImageRightJumping = self.playerImages[11]
        self.playerImageRightJumping2 = self.playerImages[12]
        self.playerImageRightJumping3 = self.playerImages[13]

        self.lastDirection = Direction.RIGHT
        
        self.playerOnPlatform = False
        self.noMovement = False
        self.playerWin = False
        self.currentPlatform = None

        self.collisionDetect = CollisionDetection()

        self.soundManager = SoundManager()
        self.soundEffects = soundEffects
        self.startFruitX = 800
        
        self.objects = pygame.sprite.Group()
        self.generateObjects(self.levelData)

        self.ticks = 0
        self.playerPos = self.player.rect.x
        
    def generateObjects(self, levelData):
        currentCoods = (0,0)
        # Loop through rows
        self.buildPlatform = False
        self.platformWidth = 0

        self.buildStartPlatform = False
        self.startPlatformWidth = 0 

        self.buildEndPlatform = False
        self.endPlatformWidth = 0  
        xCoods = 0

        charWidth = 50
        for row in levelData: #every row is 100px height         
            currentCoods = (currentCoods[0], currentCoods[1] + charWidth)
            xCoods = 0
            print(f"ROW COODS = {currentCoods}")
            for char in row: #every char is x px width  
                xCoods += charWidth                                  
                print(f"CHAR COODS = {xCoods,currentCoods[1]}")
                if self.buildPlatform:
                    self.platformWidth += charWidth
                    print(f"Build Platform Width = {self.platformWidth}")
                if char == '-':
                    if self.buildStartPlatform:
                        self.buildStartPlatform = False
                        self.startPlatform = StartPlatform(xCoods, currentCoods[1], self.platformImages[0])                    
                        print(f"Start Platform Built and Added")     
                        self.platforms.append(self.startPlatform)
                    if self.buildEndPlatform:
                        self.buildEndPlatform = False
                        self.endPlatform = EndPlatform(xCoods, currentCoods[1], self.platformImages[3])
                        print(f"End Platform Built and Added at: {xCoods}")   
                        self.platforms.append(self.endPlatform)
                elif char == '*': #fruit
                    newFruit = Fruit(xCoods, currentCoods[1], self.fruitImages[0], self.fruitImages)
                    self.fruits.append(newFruit)
                elif char == '^': #jumpBlock:
                    newJumpBlock = JumpBlock(xCoods, currentCoods[1], self.jumpBlockImages[0])
                    self.jumpBlocks.append(newJumpBlock)
                elif char == '<': #start lvl platform
                    if self.buildStartPlatform:
                        self.startPlatformWidth += charWidth
                        print(f"Start Platform Width = {self.platformWidth}")
                    else:
                        self.buildStartPlatform = True
                elif char == '>': #end lvl platform
                    if self.buildEndPlatform:
                        self.endPlatformWidth += charWidth
                        print(f"End Platform Width = {self.endPlatformWidth}")
                    else:
                        self.buildEndPlatform = True 
                elif char == 'X':  #enemy
                    newEnemy = Enemy(xCoods, currentCoods[1], self.enemyImages[0], self.enemyImages, 100)
                    self.enemies.append(newEnemy)
                    self.enemyGroup.append(newEnemy)
                    print(f"Enemy Added")
                elif char == '[': #building platform
                    self.buildPlatform = True
                    print(f"Starting platform build..")      
                elif char == ']': #end building platform
                    newPlatform = Platform(xCoods, currentCoods[1], self.platformImages[1])
                    self.platforms.append(newPlatform)
                    self.buildPlatform = False   
                    print(f"Platform Built and Added")  
                elif char == 'D': #end building platform
                    newDiamond = Diamond(xCoods, currentCoods[1], self.diamondImages[0], self.diamondImages)
                    self.diamonds.append(newDiamond)  
                    print(f"Diamond Added")  
        print("LOOP ENDED...build over...")           
                

    def reset(self):
        print("reset game...")
        self.player = Player(self.startingXPlayer, self.startingYPlayer, self.playerImages[1], self.playerImages)
        self.soundManager.stop_all_sound_effects()
        self.playerOnPlatform = False
        self.noMovement = False
        self.playerWin = False
        self.currentPlatform = None


        for enemy in self.enemyGroup:
            self.enemyGroup.append(enemy)
            self.objects.add(enemy)
            enemy.LoadImages(self.enemyImages)
          
    def runGame(self):
        print("Running game....")
        self.ticks = 1
       # print(f"Ticks....{self.ticks}")
        engineOn = True

        #backgrounds
        self.objects.add(self.background_0)
        for bg in self.backgroundManagerCloud.backgrounds:
            self.objects.add(bg)
        for bg in self.backgroundManagerHill.backgrounds:
            self.objects.add(bg)
        for bg in self.backgroundManagerMtn.backgrounds:
            self.objects.add(bg)

        print(f"Backgrounds added...")
        #platforms
        platform_group = pygame.sprite.Group()
        for platform in self.platforms:
            platform_group.add(platform)
            self.objects.add(platform)

        #jumpBlock
        for block in self.jumpBlocks:
            self.objects.add(block)

        print(f"Platforms added...")
        #enemy       
        for enemy in self.enemyGroup:
            enemy.LoadImages(self.enemyImages)
            self.objects.add(enemy)
            

        print("Enemy added...")

        #fruit
        for fruit in self.fruits:
            self.objects.add(fruit)

        print("Fruits added...")

        #diamond
        for diamond in self.diamonds:
            self.objects.add(diamond)

        print("Diamonds added...")

        #sound
        self.soundManager.load_sound_effect("Laser", self.soundEffects[0])
        self.soundManager.load_sound_effect("Jet", self.soundEffects[1])
        self.soundManager.load_sound_effect("Hit", self.soundEffects[2])
        self.soundManager.load_sound_effect("EnemyHit", self.soundEffects[3])
        self.soundManager.load_sound_effect("Theme", "assets\sounds\Theme.mp3")
        
        #player
        self.objects.add(self.player)
        self.splats = []
        last_time = 0
        self.movingTicks = 0

        self.soundManager.playTheme("Theme", 0)
        print("Engine starting...")

        while engineOn:
            self.ticks += 1
         #   print(f"ticks...{self.ticks}")
            # Calculate the time that has passed since the last frame
            current_time = pygame.time.get_ticks()
            delta_time = current_time - last_time
            last_time = current_time
            #print(f"Current Time: {current_time} Delta Time: {delta_time} Last Time: {current_time}")
            
            # Calculate the distance that the clouds/bg should move this frame
            cloud_distance = self.cloudSpeed * delta_time / 1000
            bg_distance = self.backgroundSpeed * delta_time / 1000
            bg_distance2 = self.backgroundSpeed * delta_time / 1000


            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE and self.playerOnPlatform  and self.player.falling == False:
                     #JUMPING
                    self.player.jumping = True
                    self.soundManager.play_sound_effect("Jet", 3)

            if not self.player.jumping:
                self.soundManager.stop_sound_effect("Jet")
           

            self.playerOnPlatform = False       
            self.playerWin = False
            #collision (on platform)        
            for platform in self.platforms:            
                if self.collisionDetect.check_collisionTop(self.player.rect, platform.collideRect):
                    self.playerOnPlatform = True
                    self.currentPlatform = platform          
                    if platform is self.endPlatform:
                        self.playerWin = True        
                    break
            
            self.noMovement = False

            if self.playerOnPlatform:
                self.player.Action(False, None, False, False)  #on platform
            else:
                self.player.Action(False,  None, True, False) #falling
                self.currentPlatform = None

            keys = pygame.key.get_pressed()

        #KEYS/ACTIONS     

            if self.player.rect.y <= 50:
                self.player.rect.y = 50
            #JUMPING 
            
            if self.player.jumping == True and self.lastDirection == Direction.RIGHT:
                    self.player.Action(True, Direction.RIGHT,  False, True)
                
            elif self.player.jumping == True and self.lastDirection == Direction.LEFT:
                    self.player.Action(True, Direction.LEFT, False, True)

            #MOVING RIGHT
            stuck = False
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:      
                self.lastDirection = Direction.RIGHT
                self.playerPos += 1
                if not self.player.ducked:
                    #enemies
                    for fruit in self.fruits:
                        fruit.update(Direction.RIGHT, self.noMovement)
                    for block in self.jumpBlocks:
                        block.update(Direction.RIGHT, self.noMovement)
                    for diamond in self.diamonds:
                        diamond.update(Direction.RIGHT, self.noMovement)
                    self.player.Action(True, Direction.RIGHT)    
                    self.backgroundManagerHill.update(Direction.RIGHT, self.noMovement, bg_distance)                   
                    self.backgroundManagerMtn.update(Direction.RIGHT, self.noMovement, bg_distance2)  
                    self.backgroundManagerCloud.update(Direction.RIGHT, self.noMovement, cloud_distance) 
                    for platform in self.platforms:                           
                        platform.update(self.playerOnPlatform, self.player.rect, Direction.RIGHT, self.noMovement)              
           
           
            #MOVING LEFT
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:             
                self.lastDirection = Direction.LEFT
                self.playerPos -= 1
                if not self.player.ducked:
                    #enemies           
                    for fruit in self.fruits:
                        fruit.update(Direction.LEFT, self.noMovement)
                    for block in self.jumpBlocks:
                        block.update(Direction.LEFT, self.noMovement)
                    for diamond in self.diamonds:
                        diamond.update(Direction.LEFT, self.noMovement)
                    self.player.Action(True, Direction.LEFT)
                    self.backgroundManagerHill.update(Direction.LEFT, self.noMovement, bg_distance)    
                    self.backgroundManagerMtn.update(Direction.LEFT, self.noMovement, bg_distance2)    
                    self.backgroundManagerCloud.update(Direction.LEFT, self.noMovement, cloud_distance) 
                    for platform in self.platforms:                         
                        platform.update(self.playerOnPlatform, self.player.rect, Direction.LEFT, self.noMovement)                            
            #STILL
            else:
                #enemies
                if self.lastDirection == Direction.RIGHT:
                    self.player.Action(False, Direction.RIGHT)
                elif self.lastDirection == Direction.LEFT:
                    self.player.Action(False, Direction.LEFT)

        #shooting
            if self.player.shooting == False and (keys[pygame.K_p] or keys[pygame.K_q] ) and len(self.projectilesInAir) < 5:
                self.player.Action(False,Direction.RIGHT,False,False,True)
                self.soundManager.play_sound_effect("Laser", 1)
      

        #environment                               
        #set sprites
            #shooting
            if self.player.shooting and self.player.upgradeLVL == 0:
                print("SHOOTING")
                self.projectileImage = self.playerImages[18]
                if self.player.shootingTicks > 0 and self.player.shootingTicks < 50:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImages[15])
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[15])
                elif self.player.shootingTicks >= 50 and self.player.shootingTicks < 100:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImages[16])
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[16])
                elif self.player.shootingTicks >= 100 and self.player.shootingTicks < 150:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImages[17])
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[17])
                    newProjectile = Projectile(self.player.rect.x + 20, self.player.rect.y + 65, self.projectileImage)
                    self.projectilesInAir.append(newProjectile)
                    self.objects.add(newProjectile)        
                    self.player.shooting = False
                    self.player.shootingTicks = 0
            elif self.player.shooting and self.player.upgradeLVL > 0:
                self.projectileImage = self.playerImages[28]
                if self.player.shootingTicks > 0 and self.player.shootingTicks < 25:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImages[15])
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[15])
                elif self.player.shootingTicks >= 25 and self.player.shootingTicks < 50:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImages[16])
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[16])
                elif self.player.shootingTicks >= 50 and self.player.shootingTicks < 75:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImages[17])
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[17]) 
                    newProjectile = Projectile(self.player.rect.x + 20, self.player.rect.y + 65, self.projectileImage)
                    self.projectilesInAir.append(newProjectile)
                    self.objects.add(newProjectile)        
                    self.player.shooting = False
                    self.player.shootingTicks = 0
            #jumping
            elif self.player.jumping and self.lastDirection == Direction.RIGHT:
                if self.ticks % 2 == 0:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImageRightJumping)
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[11])
                    
                elif self.ticks % 2 == 2:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImageRightJumping2)
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[12])
                else:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImageRightJumping3)
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[13])
            elif self.player.jumping and self.lastDirection == Direction.LEFT:
                if self.ticks % 2 == 0:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImageLeftJumping)
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[8])
                elif self.ticks % 2 == 2:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImageLeftJumping2)
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[9])
                else:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImageLeftJumping3)
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[10])
            #still
            elif not self.player.moving and self.lastDirection == Direction.RIGHT:
                if self.player.upgradeLVL == 0:
                    self.player.ActiveSprite(self.playerImageRightStill)
                if self.player.upgradeLVL > 0:
                    self.player.ActiveSprite(self.playerImagesUpgrade1[1])
            elif not self.player.moving and self.lastDirection == Direction.LEFT:
                if self.player.upgradeLVL == 0:
                    self.player.ActiveSprite(self.playerImageLeftStill)
                if self.player.upgradeLVL > 0:
                    self.player.ActiveSprite(self.playerImagesUpgrade1[0])
            #moving
            elif self.player.moving and self.lastDirection == Direction.RIGHT:
                if self.ticks % 2 == 0:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImageRightMoving2)
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[6])
                elif self.ticks % 2 == 2:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImageRightMoving3)
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[7])
                else:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImageRightMoving)
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[5])
            elif self.player.moving and self.lastDirection == Direction.LEFT:
                if self.ticks % 2 == 0:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImageLeftMoving2)
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[3])
                elif self.ticks % 2 == 2:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImageLeftMoving3)
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[4])
                else:
                    if self.player.upgradeLVL == 0:
                        self.player.ActiveSprite(self.playerImageLeftMoving)
                    if self.player.upgradeLVL > 0:
                        self.player.ActiveSprite(self.playerImagesUpgrade1[2])
            
            
            
            if len(self.projectilesInAir) > 0:
                print("Projectiles in air")
                for projectile in self.projectilesInAir: 
                    print("PROJECTILE X: " + str(projectile.collideRect.x))                   
                    projectile.moving()
                    
                    if projectile.rect.x > self.screen_width:
                       # print("PROJECTILE LEFT SCREEN")
                        self.projectilesInAir.remove(projectile)
            
                        self.objects.remove(projectile)        
            #duck
            if keys[pygame.K_s]:
                self.player.Action(False,Direction.RIGHT,False,False,False, True)
                #print("DUCKING Y: " + str(self.player.rect.y))
                self.player.duckingTicks += 1
                if not self.player.ducked:
                    self.player.ducked = True
                    self.player.Duck()
                if self.player.duckingTicks > 0 and self.player.duckingTicks < 20:
                    self.player.ActiveSpriteAndResize(self.playerImages[23], 40, 40)
                elif self.player.duckingTicks > 20 and self.player.duckingTicks < 40:
                    self.player.ActiveSpriteAndResize(self.playerImages[24], 40, 40)
                elif self.player.duckingTicks > 40:
                    self.player.ActiveSpriteAndResize(self.playerImages[25], 40, 40)  
                    
            
            if self.player.ducked and not keys[pygame.K_s]:
                if self.player.upgradeLVL == 0:
                        self.player.ActiveSpriteAndResize(self.playerImages[0], 40, 80)  
                if self.player.upgradeLVL > 0:
                    self.player.ActiveSpriteAndResize(self.playerImagesUpgrade1[0], 40, 80)  
                self.player.duckingTicks = 0  
                self.player.ducked = False
                self.player.rect.y -= 40
                self.player.EndDuck()

            if not self.playerOnPlatform and not self.player.jumping and not self.player.fallAfterJump and self.player.rect.y > 300:
                self.player.fallingTicks += 1
                if self.player.fallingTicks > 0 and self.player.fallingTicks < 70:
                    self.player.ActiveSprite(self.playerImages[26])
                elif self.player.fallingTicks > 70:
                    self.player.ActiveSprite(self.playerImages[27])
            else:
                self.player.fallingTicks = 0
            
            #fruits
            for fruit in self.fruits:
                if not fruit.eaten:
                    if self.collisionDetect.check_collisionFruit(self.player.rect, fruit.collideRect):
                        fruit.collided = True
                        print("Player collided fruit")
                else:
                    if not fruit.addedScore:
                        self.player.AddToScore(fruit.score)
                        fruit.addedScore = True
                        self.objects.remove(fruit)

            #diamonds
            for diamond in self.diamonds:
                if not diamond.eaten:
                    if self.collisionDetect.check_collisionFruit(self.player.rect, diamond.collideRect):
                        diamond.collided = True
                        self.player.Upgrade()
                        print("Player collided diamond")
                        self.player.shooting = False
                        self.player.shootingTicks = 0
                else:
                    if not diamond.addedScore:
                        self.player.AddToScore(diamond.score)
                        diamond.addedScore = True
                        self.objects.remove(diamond)

            
            #jump blocks
            for block in self.jumpBlocks:
                if self.collisionDetect.check_collisionTop(self.player.rect, block.collideRect):
                    self.player.jumpBoost = True
                    if block.hit:
                        block.ActiveSprite(self.jumpBlockImages[0])
                        block.hit = False
                    else:
                        block.ActiveSprite(self.jumpBlockImages[1])
                        block.hit = True

                    print("COLLISION")
                    break
                

            if self.player.jumpBoost:
                self.player.JumpBoost()
                    
            print("player " + str(self.playerPos)) 
                
            #enemies              
            for enemy in self.enemies:   
                print(enemy.originX)
                if self.playerPos + 500 > enemy.originX:         
                    enemy.activated = True
                if not self.objects.__contains__(enemy):
                    enemy.reset()
                    self.objects.add(enemy)
                if not enemy.playSound:
                    enemy.playSound = True
                    self.soundManager.play_sound_effect("EnemyHit",2)   
                if enemy.dying:
                    enemy.Dying()
                    if not enemy.splatSet:
                        splat = Splat(enemy.rect.x, enemy.rect.y, self.effectImages[0])
                        self.objects.add(splat)
                        self.splats.append(splat)    
                        enemy.SetSplat(True)                    
                elif enemy.dead:
                    if self.enemies.__contains__(enemy):
                        self.enemies.remove(enemy)
                    if self.objects.__contains__(enemy):
                        self.objects.remove(enemy)
                elif enemy.activated:    
                    speed = 2                
                    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        enemy.UpdateEnemyRight(speed)
                    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        enemy.UpdateEnemyLeft(speed)  
                    else:
                        enemy.UpdateEnemy(speed)  
                                            
                    if pygame.Rect.colliderect(enemy.rect, self.player.rect):
                        self.player.Hit()
                        self.soundManager.play_sound_effect("Hit", 4)

                    if len(self.projectilesInAir) > 0:
                        for projectile in self.projectilesInAir: 
                            if pygame.Rect.colliderect(enemy.rect, projectile.collideRect) and enemy.rect.left < self.screen_width - 200:
                                self.projectilesInAir.remove(projectile)
                                self.objects.remove(projectile)
                                enemy.Hit()
                                self.player.AddToScore(enemy.score)
                                enemy.playSound = False
                

            #death
            if self.player.rect.top > self.screen_height:
                self.player.InstaDie()
            
            if self.player.dying:
                self.player.Dying()
                if not self.player.splatSet:
                    splat = Splat(self.player.rect.x, self.player.rect.y, self.effectImages[0])
                    self.objects.add(splat)
                    self.splats.append(splat) 
                    self.player.splatSet = True


            for splat in self.splats:
                splat.move(splat.rect.x, splat.rect.y)
                splat.splatTicks += 1
                if splat.splatTicks < 50:
                    splat.ActiveSprite(self.effectImages[0])
                if splat.splatTicks > 50 and splat.splatTicks < 100:
                    splat.ActiveSprite(self.effectImages[1])
                if splat.splatTicks > 100 and splat.splatTicks < 200:
                    splat.ActiveSprite(self.effectImages[2])
                if splat.splatTicks > 200:                     
                    self.objects.remove(splat)
                    self.splats.remove(splat)

            
            if self.player.dead:
                self.soundManager.stop_all_sound_effects()
                engineOn = False
                #dead
                gameState = GameState.get_instance()
                gameState.remove_player_life()
                if gameState.get_player_life() < 0:
                    gameState.state = State.GAME_OVER
                else:
                    gameState.state = State.DEATH
                    gameState.set_score(self.player.score)
                

            #draw
            
            self.draw()

            if self.playerWin == True:
                engineOn = False
                #win
                gameState = GameState.get_instance()
                gameState.set_score(self.player.score)
                gameState.state = State.WIN

        self.soundManager.stop_all_sound_effects()
        print("Engine over.")

            
            

    def draw(self):
        # Clear the screen
        self.screen.fill("black")
        self.objects.draw(self.screen)
        self.player.draw(self.screen)
        # self.player.draw_collision_rect(self.screen)
        # for platform in self.platforms:
        #     platform.draw_collision_rect(self.screen)

        for enemy in self.enemies:
            if enemy.dying:
                enemy.display_enemy_score(self.screen, enemy.score)


        for fruit in self.fruits:
            #fruit.draw_collision_rect(self.screen)
            if fruit.collided:
                fruit.display_fruity_score(self.screen)

        for diamond in self.diamonds:
            #fruit.draw_collision_rect(self.screen)
            if diamond.collided:
                diamond.display_fruity_score(self.screen)
        #level count
        # Create a text surface with the player's score
        level_text = self.font.render(f"Level: {self.currentLevel}", True, (255, 255, 255))  # You can change the color (here, white) as needed

        # Get the rectangle that represents the text surface
        level_rect = level_text.get_rect()
        level_rect.width = level_rect.width  * 2
        level_rect.height = level_rect.height * 1.5


        # Set the position of the text (top-left corner)
        level_rect.topleft = (self.screen_width - 150, 10)  # Adjust the position as needed

        
        # Create a translucent box behind the score
        level_box = pygame.Surface((level_rect.width, level_rect.height))
        level_box.set_alpha(200)  # Set the alpha value to control the transparency (0 is fully transparent, 255 is fully opaque)
        level_box.fill((29,118,76))  # Set the color of the box (gray in this case)
        self.screen.blit(level_box, level_rect.topleft)

        # Blit the text surface onto the screen
        self.screen.blit(level_text, (level_rect.x + level_rect.width /4, level_rect.y ))
        
        # Update the display
        pygame.display.update()



    
