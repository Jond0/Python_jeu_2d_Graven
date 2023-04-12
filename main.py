import pygame
import math
from game import Game
pygame.init()


#definir une clock
clock = pygame.time.Clock()
FPS = 60

# generer la fenetre de jeu
pygame.display.set_caption("Comet Fall Game")
screen = pygame.display.set_mode((1080,720))

# import de l'arriere plan
background = pygame.image.load('assets/bg.jpg')
background = pygame.transform.scale(background, (1080+50, 720+50))


#importer charger notre bannière
banner = pygame.image.load('assets/banner.png')
banner = pygame.transform.scale(banner, (500, 500))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)

#importer charger le bouton pour lancer la partie
play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 2.4) #/3.33 de base
play_button_rect.y = math.ceil(screen.get_height() /1.85) #/2 de base

#charger le jeu
game = Game()

running = True

# boucle tant que la condition est vrai
while running:
    
    # appliquer l'arriere plan
    screen.blit(background, (0,-20))#0,-200
    
    #verifier si le jeu a commencé ou non
    if game.is_playing:
        #déclencher les instructions de la partie
        game.update(screen)
    #verifier si le jeu n'a pas commencé
    else:
        #ajouter l'écran de bienvenue
        
        screen.blit(banner, banner_rect)
        screen.blit(play_button, play_button_rect)
        
        
    
    # mettre a jour l'ecran
    pygame.display.flip()
    
    # si le joueur ferme la fenetre
    for event in pygame.event.get():
        # que l'evenement est fermetrue de la fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture du jeu")
        # detection touche clavier
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            
            #detection de la touche espace pour lancer le projectile
            if event.key == pygame.K_SPACE:
                if game.is_playing:
                    game.player.lunch_projectile()
                else:
                    #mettre le jeu en mode lancer
                    game.start()
                    #jouer le son
                    game.sound_manager.play('click')
            
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #verification si la souris est en collision avec le bouton jouer
            if play_button_rect.collidepoint(event.pos):
                #mettre le jeu en mode lancer
                game.start()
                #jouer le son
                game.sound_manager.play('click')
                
    #fixation du nombre de FPS sur ma clock
    clock.tick(FPS)