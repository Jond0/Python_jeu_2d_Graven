import pygame

#definition de la classe de projectile
class Projectiles(pygame.sprite.Sprite):
    
    # def constructeur de la classe
    def __init__(self, player):
        super().__init__()
        self.velocity = 2.5
        self.player = player
        self.image = pygame.image.load('assets/projectile.png')
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 80
        self.origin_image = self.image
        self.angle = 0
        
        
    def rotate(self):
        #faire tourner le projectie
        self.angle += 4 # 8 de base
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def remove(self):
        self.player.all_projectiles.remove(self)
        
    def move(self):
        self.rect.x += self.velocity
        #effectue la rotation
        self.rotate()
        
        #verifier si le projectile rentre en collisionavec le monstre
        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            #suppression du projectil au contact du monstre
            self.remove()
            #infliger des degats
            monster.damage(self.player.attack)
        #verifier si le projectil n'est plus à l'écran
        if self.rect.x > 1080:
            #les supprimer
            self.remove()
            #print("Projectile supprimé !")