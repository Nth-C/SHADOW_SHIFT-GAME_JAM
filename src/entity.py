import pygame as pg


# Class parent qui represente une entité dans le jeu (joueur, ennemi, etc.)
class Entity(pg.sprite.Sprite):
    def __init__(
            self, 
            x: int, # position x
            y: int, # position y
            color: tuple[int, int, int], # couleur rgb
            width: int,
            height: int, 
            hp: int, 
            attack: int, 
            speed: int,
            energy: int = 0,
            health: int = 100
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