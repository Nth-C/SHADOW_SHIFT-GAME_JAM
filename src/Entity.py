import pygame as pg

# Class parent qui represente une entité dans le jeu (joueur, ennemi, etc.)
class Entity(pg.sprite.Sprite):
    def __init__(
            self, 
            x, # position x
            y, # postion y
            color, # couleur rgb
            width,
            height, 
            hp, 
            attack, 
            speed,
            energy,
            health
        ):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.energy = energy
        self.health = health

    def take_damage(self, amount: int) -> None:
        self.hp -= amount

        if self.hp <= 0:
            self.die()

    def die(self):
        # supprime automatiquement l'entité
        self.kill()