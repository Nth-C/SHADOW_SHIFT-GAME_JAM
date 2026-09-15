import sys
import pygame as pg
from player import Body
import constants.settings as settings_constants
from hud.hud import HudManager
from map import Map
from screen import Screen
from entity import Entity
from enemy import Enemy

class Game:
    def __init__(self):
        pg.display.set_caption("Shadow of PikPik");

        self.screen = Screen()
        self.timer = pg.time.Clock();
        
        self.map = Map(self.screen)
        self.map.switch_map("spawn")
        
        self.player = Body(400, 300);
        self.hud = HudManager();

        self.enemies = pg.sprite.Group()
        
        self.enemies.add(Enemy(600, 600, 50))
        self.enemies.add(Enemy(200, 150, 50))
        self.enemies.add(Enemy(750, 400, 50))

    def run(self):
        # boucle de jeu
        running = True;

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False;
                    
                self.player.event_handler(event);
                
            self.player.move();
            self.player.regen_energy();

            # colisions avc tout les enemies
            ennemis_touches = pg.sprite.spritecollide(self.player, self.enemies, False)
            for ennemi in ennemis_touches:
                self.player.take_damage(ennemi.attack)
                break

            self.map.draw()
            
            self.screen.display.blit(self.player.image, self.player.rect)
            self.hud.draw(self.screen.display, self.player)

            self.enemies.draw(self.screen.display)

            for enemy in self.enemies:
                enemy.draw_hp_bar(self.screen.display)
                enemy.draw_aggro_range(self.screen.display)
                enemy.update(self.player)


            # attaque
            if self.player.is_attacking:
                # recupere la zone d'attaque
                zone_attaque = self.player.get_attack_range()

                # verfie si un enemie est dans une zone d'attaque
                for ennemi in self.enemies:
                    if zone_attaque.colliderect(ennemi.rect):
                        ennemi.take_damage(self.player.attack)
                        
                self.player.is_attacking = False

            self.screen.update()
            self.timer.tick(60)

        pg.quit();
        sys.exit();