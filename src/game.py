import sys
import pygame as pg
from player import Body
from player import Shadow
import constants.settings as settings_constants
from hud.hud import HudManager
from map import Map
from screen import Screen
from entity import Entity
from enemy import Enemy
from scroll import Scroll

class Game:
    def __init__(self):
        pg.display.set_caption("Shadow of PikPik")
        self.screen = Screen()
        self.timer = pg.time.Clock()

        self.state = "MENU"
        
        pg.font.init()
        self.font_title = pg.font.SysFont("Arial", 50, bold=True)
        self.font_instruction = pg.font.SysFont("Arial", 25)
        
        self.map = Map(self.screen)
        self.map.switch_map("spawn")
        
        self.player = Body(400, 300);
        self.hud = HudManager();

        self.enemies = pg.sprite.Group()
        
        self.enemies.add(Enemy(600, 600, 50))
        self.enemies.add(Enemy(200, 150, 50))
        self.enemies.add(Enemy(750, 400, 50))
        self.mur_bas_rects = []
        for obj in self.map.tmx_data.get_layer_by_name("mur_bas"):
            self.mur_bas_rects.append(pg.Rect(obj.x, obj.y, obj.width, obj.height))
        
            
        self.walls = [
            pg.Rect(object.x, object.y, object.width, object.height)
            for object in self.map.tmx_data.objects
            if object.type == "collision"
        ]
        
        player_position = self.map.tmx_data.get_object_by_name("player")
        self.player = Body(player_position.x, player_position.y)
        self.shadow = Shadow(player_position.x, player_position.y)

        self.entity_active = self.player


        self.hud = HudManager()

        self.scroll = Scroll()
        self.zoom = 2
        self.fake_screen = pg.Surface((1024 // self.zoom, 768 // self.zoom))

    def run(self):
        # boucle de jeu
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if self.state == "MENU":
                    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                        self.state = "PLAYING"
                
                elif self.state == "PLAYING":
                    self.entity_active.event_handler(event, self.walls)  

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

                # --- capacite ombre
                # active la capacite de se spéarer de son ombre
                if event.type == pg.KEYDOWN and event.key == pg.K_f:
                    if self.entity_active == self.player and self.player.energy > 0:
                        self.player.toggle_capacity();
                        self.shadow.rect.topleft = self.player.rect.topleft
                        self.entity_active = self.shadow

                    elif self.entity_active == self.shadow:
                        self.player.toggle_capacity()
                        self.entity_active = self.player

                # permet de se téléporter à l'ombre
                if self.entity_active == self.shadow:
                    if event.type == pg.KEYDOWN and event.key == pg.K_j:
                        self.player.rect.topleft = self.shadow.rect.topleft
                        self.player.toggle_capacity()
                        self.entity_active = self.player

            if self.state == "MENU":  
                self.screen.display.fill((20, 20, 40))
                
                title_surf = self.font_title.render("Shadow of PikPik", True, (255, 255, 255))
                title_rect = title_surf.get_rect(center=(1024 // 2, 768 // 3))
                self.screen.display.blit(title_surf, title_rect)
                
                inst_surf = self.font_instruction.render("Appuyez sur ESPACE pour commencer", True, (0, 255, 200))
                inst_rect = inst_surf.get_rect(center=(1024 // 2, 768 // 2))
                self.screen.display.blit(inst_surf, inst_rect)

            elif self.state == "PLAYING":
                self.entity_active.move(self.walls)
                
                self.player.update_energy()

                if self.entity_active == self.shadow and not self.player.capacity_active:
                    self.entity_active = self.player

                self.scroll.scroll_update(self.entity_active, 1024 // self.zoom, 768 // self.zoom)

                self.fake_screen.fill((0, 0, 0))

                self.map.draw(self.scroll, self.fake_screen, ("sol", "objet"))
                self.map.draw(self.scroll, self.fake_screen, ("mur", "barriere", "armoire"), mur_bas_rects=self.mur_bas_rects, draw_foreground=False)
                
                self.player_move = self.scroll.apply(self.player.rect)
                self.fake_screen.blit(self.player.image, self.player_move)

                if self.player.capacity_active:
                    self.shadow_move = self.scroll.apply(self.shadow.rect)
                    self.fake_screen.blit(self.shadow.image, self.shadow_move)

                self.map.draw(self.scroll, self.fake_screen, ("mur", "barriere", "armoire"), mur_bas_rects=self.mur_bas_rects, draw_foreground=True)

                screen_zoom = pg.transform.scale(self.fake_screen, (1024, 768))
                self.screen.display.blit(screen_zoom, (0, 0))
                
                self.hud.draw(self.screen.display, self.player)
            
            self.screen.update()
            self.timer.tick(60)