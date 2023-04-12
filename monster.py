import pygame
import random
import math
import animation


#création de la classe monstre

class Monster(animation.AnimateSprite):
    
    def __init__(self, game, name, size, offset=0):
        super().__init__(name, size)
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.1
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 300)
        self.rect.y = 540 - offset #540 de base
        self.loot_amount = 10
        self.start_animation()
        

    def set_speed(self, speed):
        self.default_speed = speed
        self.velocity = random.uniform(0.5, speed)
        
    def set_loot_amount(self, amount):
        self.loot_amount = amount
        
    def damage(self, amount):
        
        #infliger des degats
        
        self.health -= amount
        
        
        #verifier si le nb de pts de vie est inf ou = a 0
        
        if self.health <= 0:
            #faire reaparaitre en nouveau monstre
            
            self.rect.x = 1000 + random.randint (0, 300)
            self.velocity = random.randint(1, self.default_speed)
            self.health = self.max_health

            #ajouter le nombre de points
            
            self.game.add_score(self.loot_amount)

            #verifier si la barre d'event est chargée a 100%
            
            if self.game.comet_event.is_full_loaded():
                
                #reitrer du jeu
                
                self.game.all_monsters.remove(self)
                
                #appel de la methode pour essayer de declancher la pluie de cometes
                
                self.game.comet_event.attempt_fall()
                
                
    def update_animation(self):
        
        self.animate(loop=True)
        
    def update_health_bar(self, surface):
        
        
        #definition de la couleur de barre de vie
        
        bar_color = (111, 210, 46)
        
        
        #couleur de l'arriere plan de la jauge
        
        back_bar_color = (226, 9, 9)
        
        
        #definition de la position de barre de vie et les dimensions
        
        bar_position = [self.rect.x + 10, self.rect.y -20, self.health, 5]
        #definition de la position de la barre d'arrière plan
        back_bar_position = [self.rect.x + 10, self.rect.y -20, self.max_health, 5]
        
        
        #dessiner la barre de vie
        
        pygame.draw.rect(surface, back_bar_color, back_bar_position)
        pygame.draw.rect(surface, bar_color, bar_position)
        
        

    def forward(self):
        
        #deplacement s'il n'y a pas de collision avec un joueur
        
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
            
            
        #si le monstre est en collision avec le joueur
        
        else:
            #infliger des déggats au joueur
            self.game.player.damage(self.attack)
            
            
#définir une classe momie

class Mummy(Monster):
    
    def __init__(self, game):
        super().__init__(game, "mummy", (130, 130))
        self.set_speed(3)
        self.set_loot_amount(20)
        
        
#définir une classe pour l'alien

class Alien(Monster):
    def __init__(self, game):
        super().__init__(game, "alien", (300, 300), 165) #dernière variable 130 de base
        self.health = 250
        self.max_health = 250
        self.attack = 0.8
        self.set_speed(1)
        self.set_loot_amount(80)