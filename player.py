import pygame
from projectile import Projectiles
import random
import animation




#creation premiere classe joueur
class Player(animation.AnimateSprite):
    
    def __init__(self, game):
        super().__init__('player')
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 10 + random.randint(0,20)#rajoute une valeur de dégat aléatoire
        self.velocity = 5
        self.all_projectiles = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500
        
    def damage(self, amount):
        if self.health - amount > amount :
            self.health -= amount
        else:
        #si le joueur n'a plus de pv
            self.game.game_over()
            
    def update_animation(self):
        self.animate()
        
    def update_health_bar(self, surface):
        #definition de la couleur de barre de vie
        bar_color = (111, 210, 46)
        #couleur de l'arriere plan de la jauge
        back_bar_color = (226, 9, 9)
        
        #definition de la position de barre de vie et les dimensions
        bar_position = [self.rect.x + 50, self.rect.y -15, self.health, 7]
        #definition de la position de la barre d'arrière plan
        back_bar_position = [self.rect.x + 50, self.rect.y -15, self.max_health, 7]
        
        #dessiner la barre de vie
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)
        
    def lunch_projectile(self):
        #creation de la nouvelle instance de la classe projectile
        self.all_projectiles.add(Projectiles(self))
        #demarrer l'animation pour le lancer
        self.start_animation()
        #jouer le son
        self.game.sound_manager.play('tir')
    
    def move_right(self):
        #si le joueur ne rentre pas en collision avec le monstre
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity
    def move_left(self):
        self.rect.x -= self.velocity
