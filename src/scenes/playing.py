import pygame as pg
from pygame.event import Event
from player import Body, Shadow
from enemy import Enemy
from map import Map
from hud.hud import HudManager
from scroll import Scroll

class Playing:
    def __init__(self, screen):
        self.screen = screen
        self.map = Map(self.screen)
        self.map.switch_map("spawn")

        player_position = self.map.tmx_data.get_object_by_name("player")
        self.player = Body(player_position.x, player_position.y)
        self.shadow = Shadow(player_position.x, player_position.y)
        self.entity_active = self.player
        self.hud = HudManager()

        # enemie
        self.enemies = pg.sprite.Group()
        self.enemies.add(Enemy(600, 600, 50))
        self.enemies.add(Enemy(200, 150, 50))
        self.enemies.add(Enemy(750, 400, 50))

        # scroll
        self.scroll = Scroll()
        self.zoom = 2
        self.fake_screen = pg.Surface((1024 // self.zoom, 768 // self.zoom))

        # wall
        self.mur_bas_rects = []
        for obj in self.map.tmx_data.get_layer_by_name("mur_bas"):
            self.mur_bas_rects.append(pg.Rect(obj.x, obj.y, obj.width, obj.height))
            
        self.walls = [
            pg.Rect(object.x, object.y, object.width, object.height)
            for object in self.map.tmx_data.objects
            if object.type == "collision"
        ]

    # event clique
    def event_playing(self, event: Event):
        self.entity_active.event_handler(event, self.walls)
        # TODO a suppr
        # --- capacite ombre
        # active la capacite de se spéarer de son ombre
        if event.type == pg.KEYDOWN and event.key == pg.K_a:
            if self.entity_active == self.player and self.player.energy > 0:
                self.player.toggle_capacity();
                self.shadow.rect.topleft = self.player.rect.topleft
                self.entity_active = self.shadow
        
            elif self.entity_active == self.shadow:
                self.player.toggle_capacity()
                self.entity_active = self.player
        
        # permet de se téléporter à l'ombre
        if self.entity_active == self.shadow:
            if event.type == pg.KEYDOWN and event.key == pg.K_c:
                self.player.rect.topleft = self.shadow.rect.topleft
                self.player.toggle_capacity()
                self.entity_active = self.player

    # gere les updates
    def update(self):
        if self.player.is_attacking:
            zone_attaque = self.player.get_attack_range()
            for ennemi in self.enemies:
                if zone_attaque.colliderect(ennemi.rect):
                    ennemi.take_damage(self.player.attack)
            self.player.is_attacking = False

        self.entity_active.move(self.walls)
        self.player.update_energy()
        
        for enemy in self.enemies:
            enemy.update(self.player)
                                        
        ennemis_touches = pg.sprite.spritecollide(self.player, self.enemies, False)
        for ennemi in ennemis_touches:
            self.player.take_damage(ennemi.attack)
            break
        
        if self.entity_active == self.shadow and not self.player.capacity_active:
            self.entity_active = self.player
        
        self.scroll.scroll_update(self.entity_active, 1024 // self.zoom, 768 // self.zoom)

    # gere l'afichage
    def draw(self):
        self.fake_screen.fill((0, 0, 0))
        
        self.map.draw(self.scroll, self.fake_screen, ("sol", "objet"))
        self.map.draw(self.scroll, self.fake_screen, ("mur", "barriere", "armoire"), mur_bas_rects=self.mur_bas_rects, draw_foreground=False)
                        
        self.player_move = self.scroll.apply(self.player.rect)
        self.fake_screen.blit(self.player.image, self.player_move)
        
        if self.player.capacity_active:
            self.shadow_move = self.scroll.apply(self.shadow.rect)
            self.fake_screen.blit(self.shadow.image, self.shadow_move)
        
        for enemy in self.enemies:
            enemy_move = self.scroll.apply(enemy.rect)
            self.fake_screen.blit(enemy.image, enemy_move)
        
        self.map.draw(self.scroll, self.fake_screen, ("mur", "barriere", "armoire"), mur_bas_rects=self.mur_bas_rects, draw_foreground=True)
        
        screen_zoom = pg.transform.scale(self.fake_screen, (1024, 768))
        self.screen.display.blit(screen_zoom, (0, 0))
                        
        self.hud.draw(self.screen.display, self.player)