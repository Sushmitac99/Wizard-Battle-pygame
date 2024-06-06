##Art Contributions: Wizard:Sollision & Jordan Irwin (AntumDeluge)
##Forest background: Tamara Ramsay
#Lasers: Wenrexa 


import pygame
from sys import exit

class Redlaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Player/redlaser.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 8
    
    def update(self):
        self.rect.x += self.speed
        # Remove the laser if it goes off the screen
        if self.rect.left > 800:
            self.kill()

class Greenlaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Player/greenlaser.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 50))
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 8

    def update(self):
        self.rect.x -= self.speed
        # Remove the laser if it goes off the screen
        if self.rect.right < 0:
            self.kill()



def collision_sprite():
    global wizard1_health, wizard2_health
    lasercollided = False
    for i in Redlaser_group.sprites():      
       if i.rect.colliderect(wizard_rect_2):
                wizard2_health -= 1
                lasercollided = True
                i.kill()
            
    
    for i in Greenlaser_group.sprites():
        if i.rect.colliderect(wizard_rect):
            wizard1_health -= 1
            lasercollided = True
            i.kill()

    return lasercollided



pygame.init()
screen = pygame.display.set_mode((800,500))
pygame.display.set_caption('Battle of the Wizards')
clock = pygame.time.Clock()
font = pygame.font.Font(None,40)


GREEN = (0, 255, 0)
RED = (255, 0, 0)

wizard1_health = 18
wizard2_health = 18 

#Groups
Redlaser_group = pygame.sprite.Group()
Greenlaser_group = pygame.sprite.Group()


forest_surface = pygame.image.load('Background/forest.png').convert()


wizard_walk_1 = pygame.image.load('Player/wizardwalk1.png').convert_alpha()
wizard_walk_2 = pygame.image.load('Player/wizardwalk2.png').convert_alpha()
wizard_walk_3 = pygame.image.load('Player/wizardwalk3.png').convert_alpha()
wizard_walks = [wizard_walk_1, wizard_walk_2, wizard_walk_3]
wizard_walks = [pygame.transform.rotozoom(img, 0, 2.4) for img in wizard_walks]
wizard_walk_index = 0
wizard_surface = wizard_walks[wizard_walk_index]



wizard_rect = wizard_surface.get_rect(bottomright = (100,340))


# Load image for second wizard
wizard_walk_index_2 = 0
wizard_surface_2 = pygame.transform.flip(wizard_walks[wizard_walk_index_2],True, False)
wizard_rect_2 = wizard_surface_2.get_rect(bottomleft = (700,340)) 



#TIMER

wizard_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(wizard_animation_timer,200)


wizard_animation_timer_2 = pygame.USEREVENT + 4
pygame.time.set_timer(wizard_animation_timer_2, 200)


  
wizard_rect_2_previous = wizard_rect_2.copy()   



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == wizard_animation_timer:
            wizard_walk_index = (wizard_walk_index +1) % 3
        
        if event.type == wizard_animation_timer_2:
            wizard_walk_index_2 = (wizard_walk_index_2 + 1) % 3
            wizard_surface_2 = wizard_walks[wizard_walk_index_2]


        keys = pygame.key.get_pressed()
        keys_2 = pygame.key.get_pressed()


        if keys[pygame.K_w]:
            # Move wizard up
            wizard_rect.y -= 10
        if keys[pygame.K_s]:
            # Move wizard down
            wizard_rect.y += 10
        if keys[pygame.K_a]:
            # Move wizard left
            wizard_rect.x -= 10
        if keys[pygame.K_d]:
            # Move wizard right
            wizard_rect.x += 10
        

        #second wizard keys
        
        if keys_2[pygame.K_UP]:
            wizard_rect_2.y -= 10
        if keys_2[pygame.K_DOWN]:
            wizard_rect_2.y += 10
        if keys_2[pygame.K_LEFT]:
            wizard_rect_2.x -= 10
        if keys_2[pygame.K_RIGHT]:
            wizard_rect_2.x += 10
        

        if keys[pygame.K_SPACE]:
            Redlaser_group.add(Redlaser(wizard_rect.centerx,wizard_rect.centery))


        if keys[pygame.K_COMMA]:
            Greenlaser_group.add(Greenlaser(wizard_rect_2.centerx,wizard_rect_2.centery))


            
    
    #draw all elements
    #update everything
    
    screen.blit(forest_surface,(0,0))
    screen.blit(wizard_surface,wizard_rect)
    screen.blit(pygame.transform.flip(wizard_surface_2, True, False), wizard_rect_2)
    Redlaser_group.draw(screen)
    Redlaser_group.update()
    Greenlaser_group.draw(screen)
    Greenlaser_group.update()
    collision_sprite()


    

    #Draw wizard1's health bar
    pygame.draw.rect(screen, RED, (27, 50, wizard1_health * 18, 20))

    # Draw wizard2's health bar
    pygame.draw.rect(screen, GREEN, (450, 50, wizard2_health * 18, 20))
    
    #display the winner 
    if wizard1_health <= 0:
        game_over_text = font.render("Wizard 2 Wins!", True, (255, 0, 0))
        screen.blit(game_over_text, (300, 200))
    elif wizard2_health <= 0:
        game_over_text = font.render("Wizard 1 Wins!", True, (255, 0, 0))
        screen.blit(game_over_text, (300, 200))

 

    
    pygame.display.update()
    clock.tick(60)