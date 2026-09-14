import pygame

# Class parent qui represente une entité dans le jeu (joueur, ennemi, etc.)
class Entity(pygame.sprite.Sprite):
    def __init__(
            self, 
            x, # position x
            y, # postion y
            color, # couleur rgb
            size, 
            hp, 
            attack, 
            speed,
            energy
        ):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.energy = energy

    def take_damage(self, amount):
        self.hp -= amount

        if self.hp <= 0:
            self.die()

    def die(self):
        # supprime automatiquement l'entité
        self.kill()