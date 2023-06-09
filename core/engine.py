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
from assets.objects.endPlatform import EndPlatform
from assets.objects.startPlatform import StartPlatform
from assets.objects.projectile import Projectile
from assets.objects.splat import Splat

class Engine():
    def __init__(self, screen, currentLevel, screen_width, screen_height , playerImages:list, platformImages:list, parallaxImages:list, enemyImages:list, effectImages:list, soundEffects:list):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.currentLevel = currentLevel
        self.ticks = 1
        self.font = pygame.font.Font(None, 36)
        self.bg_color = (255, 255, 255)
        self.startingX = (screen_width / 2) - 100
        self.endingX = 6000
        self.startingY = 400
        self.startingY_StartPlatform = 200
        self.startingXPlayer = (screen_width / 2) - 50
        self.startingYPlayer = self.startingY - 64
        self.playerImages = playerImages
        self.platformImages = platformImages
        self.effectImages = effectImages
        self.player = Player(self.startingXPlayer, self.startingYPlayer, self.playerImages[1], self.playerImages)

        self.startPlatform = StartPlatform(self.startingX, self.startingY_StartPlatform, self.platformImages[0])
        self.platformSmall2 = Platform(self.startingX + 1600, self.startingY, self.platformImages[1])
        self.platformSmall3 = Platform(self.startingX + 2700, self.startingY, self.platformImages[1])
        self.platformSmall4 = Platform(self.startingX + 3400, self.startingY, self.platformImages[1])
        self.platformSmall5 = Platform(self.startingX + 4100, self.startingY, self.platformImages[1])
        self.platformSmall6 = Platform(self.startingX + 4800, self.startingY, self.platformImages[1])
        self.endPlatform = EndPlatform(self.endingX, self.startingY_StartPlatform, self.platformImages[3])

        self.platforms = [self.startPlatform,  self.platformSmall2, self.platformSmall3, 
                        self.platformSmall4, self.platformSmall5, self.platformSmall6, self.endPlatform]
        
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
        

        self.projectileImage = self.playerImages[10]
        self.projectilesInAir = []

        self.playerImageLeftStill = self.playerImages[0]
        self.playerImageRightStill = self.playerImages[1]
        self.playerImageLeftMoving = self.playerImages[2] 
        self.playerImageRightMoving = self.playerImages[3]
        self.playerImageLeftJumping = self.playerImages[4] 
        self.playerImageRightJumping = self.playerImages[5]
        self.lastDirection = Direction.RIGHT

        #enemies
        self.startingEnemy = self.startingXPlayer + 800
        self.startingYEnemy = (self.startingY - enemyImages[0].get_height() / 2) + 10
        
        self.enemyImages = enemyImages
  
        self.enemy = Enemy(self.startingEnemy, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy2 = Enemy(self.startingEnemy + 1000, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy3 = Enemy(self.startingEnemy + 1500, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy4 = Enemy(self.startingEnemy + 2000, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy5 = Enemy(self.startingEnemy + 2200, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy6 = Enemy(self.startingEnemy + 3000, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy7 = Enemy(self.startingEnemy + 4000, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy8 = Enemy(self.startingEnemy + 4500, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy9 = Enemy(self.startingEnemy + 5000, self.startingYEnemy, self.enemyImages[0], self.enemyImages)

        self.enemy10 = Enemy(self.startingEnemy + 1500, 300, self.enemyImages[0], self.enemyImages)
        self.enemy11 = Enemy(self.startingEnemy + 2500, 100, self.enemyImages[0], self.enemyImages)
        self.enemy12 = Enemy(self.startingEnemy + 4500, 140, self.enemyImages[0], self.enemyImages)
        self.enemy13 = Enemy(self.startingEnemy + 5000, 180, self.enemyImages[0], self.enemyImages)



        self.enemies = [self.enemy,self.enemy2,self.enemy3, self.enemy4, self.enemy5, self.enemy6, self.enemy7, self.enemy8, self.enemy9,self.enemy10, self.enemy11, self.enemy12, self.enemy13]
        self.enemy_group = pygame.sprite.Group()
        
        self.playerOnPlatform = False
        self.noMovement = False
        self.playerWin = False
        self.currentPlatform = None

        self.collisionDetect = CollisionDetection()

        self.soundManager = SoundManager()
        self.soundEffects = soundEffects
        
        

    def reset(self):
        self.player = Player(self.startingXPlayer, self.startingYPlayer, self.playerImages[1], self.playerImages)

        self.soundManager.stop_all_sound_effects()
        self.startPlatform = StartPlatform(self.startingX, self.startingY_StartPlatform, self.platformImages[0])
        self.platformSmall2 = Platform(self.startingX + 1600, self.startingY, self.platformImages[1])
        self.platformSmall3 = Platform(self.startingX + 2700, self.startingY, self.platformImages[1])
        self.platformSmall4 = Platform(self.startingX + 3400, self.startingY, self.platformImages[1])
        self.platformSmall5 = Platform(self.startingX + 4100, self.startingY, self.platformImages[1])
        self.platformSmall6 = Platform(self.startingX + 4800, self.startingY, self.platformImages[1])
        self.endPlatform = EndPlatform(self.endingX, self.startingY_StartPlatform, self.platformImages[3])

        self.platforms = [self.startPlatform,  self.platformSmall2, self.platformSmall3, 
                          self.platformSmall4, self.platformSmall5, self.platformSmall6, self.endPlatform]
        
        #background
        self.background_0 = BackgroundLayer(0,0,self.screen, self.screen_width, self.screen_height, self.screen_width, self.parallaxImages[0], 0)

        #parallax foregound
        self.backgroundManagerCloud = BackgroundManager(self.player, self.screen, 200, self.screen_width, self.parallaxImages[1], self.cloudSpeed)
        self.backgroundManagerHill = BackgroundManager(self.player, self.screen,  self.screen_height, self.screen_width, self.parallaxImages[2], 2)
        self.backgroundManagerMtn = BackgroundManager(self.player, self.screen,  self.screen_height, self.screen_width, self.parallaxImages[3], 3)
        
        #enemies
        self.enemy = Enemy(self.startingEnemy, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy2 = Enemy(self.startingEnemy + 1000, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy3 = Enemy(self.startingEnemy + 1500, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy4 = Enemy(self.startingEnemy + 2000, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy5 = Enemy(self.startingEnemy + 2200, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy6 = Enemy(self.startingEnemy + 3000, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy7 = Enemy(self.startingEnemy + 4000, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy8 = Enemy(self.startingEnemy + 4500, self.startingYEnemy, self.enemyImages[0], self.enemyImages)
        self.enemy9 = Enemy(self.startingEnemy + 5000, self.startingYEnemy, self.enemyImages[0], self.enemyImages)

        self.enemy10 = Enemy(self.startingEnemy + 1500, 300, self.enemyImages[0], self.enemyImages)
        self.enemy11 = Enemy(self.startingEnemy + 2500, 100, self.enemyImages[0], self.enemyImages)
        self.enemy12 = Enemy(self.startingEnemy + 4500, 140, self.enemyImages[0], self.enemyImages)
        self.enemy13 = Enemy(self.startingEnemy + 5000, 180, self.enemyImages[0], self.enemyImages)



        self.enemies = [self.enemy,self.enemy2,self.enemy3, self.enemy4, self.enemy5, self.enemy6, self.enemy7, self.enemy8, self.enemy9,self.enemy10, self.enemy11, self.enemy12, self.enemy13]


        self.playerOnPlatform = False
        self.noMovement = False
        self.playerWin = False
        self.currentPlatform = None


        for enemy in self.enemy_group:
            self.enemy_group.add(enemy)
            self.objects.add(enemy)
            enemy.LoadImages(self.enemyImages)
        



    
    def runGame(self):
        self.ticks = 1
        engineOn = True
        self.objects = pygame.sprite.Group()
        customDetect = CollisionDetection()

        #backgrounds
        self.objects.add(self.background_0)
        for bg in self.backgroundManagerCloud.backgrounds:
            self.objects.add(bg)
        for bg in self.backgroundManagerHill.backgrounds:
            self.objects.add(bg)
        for bg in self.backgroundManagerMtn.backgrounds:
            self.objects.add(bg)
       
        #platforms
        platform_group = pygame.sprite.Group()
        for platform in self.platforms:
            platform_group.add(platform)
            self.objects.add(platform)

        #enemy
        for enemy in self.enemies:
            self.objects.add(enemy)
       
        
        for enemy in self.enemy_group:
            self.enemy_group.add(enemy)
            self.objects.add(enemy)
            enemy.LoadImages(self.enemyImages)

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
        while engineOn:
            self.ticks += 1
            
            # Calculate the time that has passed since the last frame
            current_time = pygame.time.get_ticks()
            delta_time = current_time - last_time
            last_time = current_time
            #print(f"Current Time: {current_time} Delta Time: {delta_time} Last Time: {current_time}")
            
            # Calculate the distance that the clouds/bg should move this frame
            cloud_distance = self.cloudSpeed * delta_time / 1000
            bg_distance = self.backgroundSpeed * delta_time / 1000
            bg_distance2 = self.backgroundSpeed * delta_time / 1000
           # print(f"Cloud Speed/Dist: {cloud_distance} BG Speed/Dist: {bg_distance}")

            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE and not self.player.jumping and not self.player.falling:
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
            #collision (left/right)
            for platform in self.platforms:            
                if self.collisionDetect.check_collisionRight(self.player.rect, platform.collideRect):
                    #self.noMovement = True
                    break
                if self.collisionDetect.check_collisionLeft(self.player.rect, platform.collideRect):
                   # self.noMovement = True
                    break
 
            if self.playerOnPlatform:
                self.player.Action(False, None, False, False)  #on platform
            else:
                self.player.Action(False,  None, True, False) #falling

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
                #enemies
           
                self.player.Action(True, Direction.RIGHT)
                self.lastDirection = Direction.RIGHT
                self.backgroundManagerHill.update(Direction.RIGHT, self.noMovement, bg_distance)                   
                self.backgroundManagerMtn.update(Direction.RIGHT, self.noMovement, bg_distance2)  
                self.backgroundManagerCloud.update(Direction.RIGHT, self.noMovement, cloud_distance) 
                for platform in self.platforms:                           
                    platform.update(self.playerOnPlatform, self.player.rect, Direction.RIGHT, self.noMovement)              
            #MOVING LEFT
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                 #enemies           
                self.player.Action(True, Direction.LEFT)
                self.lastDirection = Direction.LEFT
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
            if self.player.shooting == False and (keys[pygame.K_p] or keys[pygame.K_q] ) and len(self.projectilesInAir) < 50:
                self.player.Action(False,Direction.RIGHT,False,False,True)
                self.soundManager.play_sound_effect("Laser", 1)

        #environment                               
        #set sprites
            #shooting
            if self.player.shooting:
                newProjectile = Projectile(self.player.rect.x + 20, self.player.rect.y + 65, self.projectileImage)
                self.projectilesInAir.append(newProjectile)
                self.objects.add(newProjectile)
                if self.player.shootingTicks > 0 and self.player.shootingTicks < 80:
                    self.player.ActiveSprite(self.playerImages[6])
                elif self.player.shootingTicks > 80 and self.player.shootingTicks < 160:
                    self.player.ActiveSprite(self.playerImages[7])
                elif self.player.shootingTicks > 340 and self.player.shootingTicks < 420:
                    self.player.ActiveSprite(self.playerImages[8])
            
            #jumping
            elif self.player.jumping and self.lastDirection == Direction.RIGHT:
                self.player.ActiveSprite(self.playerImageRightJumping)
            elif self.player.jumping and self.lastDirection == Direction.LEFT:
                self.player.ActiveSprite(self.playerImageLeftJumping)
            #still
            elif not self.player.moving and self.lastDirection == Direction.RIGHT:
                self.player.ActiveSprite(self.playerImageRightStill)
            elif not self.player.moving and self.lastDirection == Direction.LEFT:
                self.player.ActiveSprite(self.playerImageLeftStill)
            #moving
            elif self.player.moving and self.lastDirection == Direction.RIGHT:
                self.player.ActiveSprite(self.playerImageRightMoving)
            elif self.player.moving and self.lastDirection == Direction.LEFT:
                self.player.ActiveSprite(self.playerImageLeftMoving)
                
            
            if len(self.projectilesInAir) > 0:
                for projectile in self.projectilesInAir: 
                    if len(self.enemy_group) == 0:   
                       # print("PROJECTILE X: " + str(projectile.collideRect.x))
                        projectile.moving()

                    
                    if projectile.rect.x > self.screen_width:
                       # print("PROJECTILE LEFT SCREEN")
                        self.projectilesInAir.remove(projectile)
                        self.objects.remove(projectile)
               
                            
            
                         
            #enemies        
                
            for enemy in self.enemies:    
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
                else:    
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
                            if pygame.Rect.colliderect(enemy.rect, projectile.collideRect):
                                self.projectilesInAir.remove(projectile)
                                self.objects.remove(projectile)
                                enemy.Hit()
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
                gameState.state = State.DEATH

            #draw
            
            self.draw(self.objects)

            if self.playerWin == True:
                engineOn = False
                #win
                gameState = GameState.get_instance()
                gameState.state = State.WIN
        self.soundManager.stop_all_sound_effects()

            
            

    def draw(self, objects):
        # Clear the screen
        self.screen.fill("black")

        objects.draw(self.screen)

        # Update the display
        pygame.display.update()



    
