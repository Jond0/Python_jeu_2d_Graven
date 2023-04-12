import pygame

from player import Player
from monster import Alien, Monster, Mummy
from comet_event import CometFallEvent
from sounds import SoundManager



#creation de la seconde classe representation du jeu

class Game:
    
    def __init__(self):
        #definir si le jeu a commencé ou non si on remplace par True -> ça passe direct au jeu
        
        self.is_playing = False
        
        
        #generation du joueur
        
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        
        
        #generation de l'event
        
        self.comet_event = CometFallEvent(self)
        
        
        #groupe de monstres
        
        self.all_monsters = pygame.sprite.Group()
        
        #gestion du son
        
        self.sound_manager = SoundManager()
        #mettre le score à 0
        
        self.font = pygame.font.Font("assets/SHOWG.TTF", 35) #SysFont
        self.score = 0
        self.pressed = {}
        
    def start(self):
        self.is_playing = True
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)
        
    def add_score(self, points=10):
        
        self.score += points
        
    def game_over(self):
        #reset le jeu, retirer les monstres, reset les pv du joueur et le jeu en attente
        
        self.all_monsters = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.player.health=self.player.max_health
        self.comet_event.reset_percent()
        self.is_playing = False
        self.score = 0
        #jouer le son
        self.sound_manager.play('game_over')
        
    def update(self, screen):
        
        #afficher le score sur l'ecran
        
        score_text = self.font.render(f"Score : {self.score}", 1, (0, 0, 0))
        screen.blit(score_text, (20, 20))
        
        # appliquer l'image joueur
        
        screen.blit(self.player.image, self.player.rect)
    
        #actualiser la barre de vie du joueur
        
        self.player.update_health_bar(screen)
        
        #actualiser la barre d'event du jeu
        
        self.comet_event.update_bar(screen)
        
        #actualiser l'animation du joueur
        
        self.player.update_animation()
        
        #recuperer les projectiles du joueur
        
        for projectile in self.player.all_projectiles:
            projectile.move()
        
        #recuperer les monstres de notre jeu
        
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()
            
        #recuperer les comets du jeu
        
        for comet in self.comet_event.all_comets:
            comet.fall()
        
        # afficher l'image du projectile
        
        self.player.all_projectiles.draw(screen)
        
        #appliquer l'ensemble des images des monstres
        
        self.all_monsters.draw(screen)
        
        #appliquer l'ensemble des images du groupe comets
        
        self.comet_event.all_comets.draw(screen)
        
        # verfifier si le joueur va a droite ou guache
        
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()
    
    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
        
    def spawn_monster(self, monster_class_name):
        self.all_monsters.add(monster_class_name.__call__(self))