import math

import pygame as pg
from pygame.event import Event

import constants.game_states as game_constants
import constants.settings as settings_constants
from eclipse import Eclipse
from enemy import Enemy
from hud.hint import Hint
from hud.hud import HudManager
from light import _iter_light_sources, render_lights
from map import Map
from player.body import Body
from player.shadow import Shadow
from scenarioManager import ScenarioManager
from screen import Screen
from scroll import Scroll
from sound import Sound


class Playing:
    def __init__(self):
        pg.display.set_caption(settings_constants.NAME_GAME)
        self.screen = Screen()
        self.timer = pg.time.Clock()
        self.state = game_constants.MENU
        
        pg.font.init()
        self.font_hint = pg.font.SysFont("Arial", 16)
        self.font_title = pg.font.SysFont("Arial", 50, bold=True)
        self.font_instruction = pg.font.SysFont("Arial", 25)

        self.sound = Sound()
        self.sound.play_music()

        self.last_hit_time = 0
        self.hit_cooldown = 800
        
        self.map = Map(self.screen)
        self.map.switch_map("spawn")
        self.refresh_map_data()
        
        self.hud = HudManager();

        self.zoom = 2

        self.enemies = pg.sprite.Group()
        
        self.enemies.add(Enemy(600, 600, 50))
        self.enemies.add(Enemy(200, 150, 50))
        
        self.spawn_entities_at_player()

        self.entity_active = self.player

        self.hud = HudManager()
        self.shadow_hint = Hint("A pour passer en ombre", pg.K_a, True)

        self.scroll = Scroll()
        self.fake_screen = pg.Surface((1024 // self.zoom, 768 // self.zoom))
        self.light_surface = pg.Surface((1024 // self.zoom, 768 // self.zoom), pg.SRCALPHA)

        self.scenario = ScenarioManager()

        self.eclipse = Eclipse(500, 350)

    # evenement du player
    def handle_event(self, event: Event) -> None:
        # gestion des dialogues
        if self.scenario.is_dialog_playing():
            self.scenario.event_handler(event)
        else:
            used_walls = self.walls_shadow if self.entity_active == self.shadow else self.walls_player
            self.entity_active.event_handler(event, used_walls)

            # hint
            if self.shadow_hint:
                self.shadow_hint.handle_event(event)

            # --- capacite ombre
            # active la capacite de se spéarer de son ombre
            if event.type == pg.KEYDOWN and event.key == pg.K_a:
                if self.entity_active == self.player and self.player.energy > 0:
                    self.player.toggle_capacity();
                    self.shadow.rect.topleft = self.player.rect.topleft
                    self.entity_active = self.shadow

                    # pour debug le mouvement en changant d'etat
                    self.player.reset_movement()
                    self.shadow.reset_movement()

                elif self.entity_active == self.shadow:
                    self.player.toggle_capacity()
                    self.entity_active = self.player

                    self.player.reset_movement()
                    self.shadow.reset_movement()

            # permet de se téléporter à l'ombre
            if self.entity_active == self.shadow:
                if event.type == pg.KEYDOWN and event.key == pg.K_c:
                    self.player.rect.topleft = self.shadow.rect.topleft
                    self.player.toggle_capacity()
                    self.entity_active = self.player

                    self.player.reset_movement()
                    self.shadow.reset_movement()

    def refresh_map_data(self):
        self.mur_bas_rects = []
        mur_bas_layer = next(
            (
                layer
                for layer in self.map.tmx_data.visible_layers
                if layer.name == "mur_bas"
            ),
            None,
        )
        if mur_bas_layer is not None:
            for obj in mur_bas_layer:
                self.mur_bas_rects.append(pg.Rect(obj.x, obj.y, obj.width, obj.height))

        self.walls_player = [
            pg.Rect(obj.x, obj.y, obj.width, obj.height)
            for obj in self.map.tmx_data.objects
            if obj.type in ("collision", "ombre", "wave_exit")
        ]
        self.walls_shadow = [
            pg.Rect(obj.x, obj.y, obj.width, obj.height)
            for obj in self.map.tmx_data.objects
            if obj.type in ("collision", "switch_map", "wave_exit")
        ]

        switch_map = next(
            (obj for obj in self.map.tmx_data.objects if obj.type == "switch_map"),
            None,
        )

        if switch_map is not None:
            self.switch_map_rect = (pg.Rect(switch_map.x, switch_map.y, switch_map.width, switch_map.height))
            self.target_map_name = getattr(switch_map, "target_map", "spawn") 
        else:
            self.switch_map_rect = None
            self.target_map_name = None

    def spawn_entities_at_player(self):
        player_position = self.map.tmx_data.get_object_by_name("player")
        self.player = Body(player_position.x, player_position.y)
        self.shadow = Shadow(player_position.x, player_position.y)
        

        self.background_galaxy = pg.image.load('assets/images/galaxie.png').convert()
        self.background_galaxy = pg.transform.scale(
            self.background_galaxy,
            (1024 // self.zoom, 768 // self.zoom)
        )

    def update(self) -> str:
        if self.entity_active.is_attacking:
            zone_attaque = self.entity_active.get_attack_range()
            for ennemi in self.enemies:
                if zone_attaque.colliderect(ennemi.rect):
                    ennemi.take_damage(self.entity_active.attack)
            self.entity_active.is_attacking = False

        self.scenario.update_dialog(self)
        self.eclipse.update()

        if not self.scenario.is_dialog_playing():
            # Choix des murs selon qui on contrôle
            if self.entity_active == self.shadow:
                used_walls = self.walls_shadow
            else:
                used_walls = self.walls_player
            
            self.entity_active.move(used_walls)
            self.player.update_energy()
            
            for enemy in self.enemies:
                enemy.update(self.player)

        ennemis_touches = pg.sprite.spritecollide(self.player, self.enemies, False)
        if ennemis_touches:
            now = pg.time.get_ticks()
            if now - self.last_hit_time >= self.hit_cooldown:
                self.player.take_damage(ennemis_touches[0].attack)
                self.sound.play_hit();
                self.last_hit_time = now

        if len(self.enemies) == 0:
            self.walls_player = [
                pg.Rect(obj.x, obj.y, obj.width, obj.height)
                for obj in self.map.tmx_data.objects
                if obj.type in ("collision", "ombre")
            ]
            self.walls_shadow = [
                pg.Rect(obj.x, obj.y, obj.width, obj.height)
                for obj in self.map.tmx_data.objects
                if obj.type in ("collision", "switch_map")
            ]

            if self.entity_active == self.shadow and not self.player.capacity_active:
                self.entity_active = self.player

            if self.entity_active == self.player:
                if self.switch_map_rect and self.player.feet.colliderect(self.switch_map_rect):
                    if self.target_map_name: 
                        self.map.switch_map(self.target_map_name)
                        self.refresh_map_data()
                        self.spawn_entities_at_player()
                        self.entity_active = self.player

        if self.entity_active == self.shadow and not self.player.capacity_active:
            self.entity_active = self.player

        if self.entity_active == self.shadow:
            shadow_x, shadow_y = self.shadow.rect.center
            for lampe_x, lampe_y, rayon in _iter_light_sources(self.map.tmx_data):
                if math.hypot(lampe_x - shadow_x, lampe_y - shadow_y) <= rayon:
                    self.player.toggle_capacity()
                    self.entity_active = self.player
                    self.player.reset_movement()
                    self.shadow.reset_movement()
                    break

        # mort
        if self.player.hp <= 0:
            self.sound.play_death()
            return game_constants.GAME_OVER

        # continuer le jeu
        return game_constants.PLAYING

    # --- affichage
    def draw(self):
        self.scroll.scroll_update(self.entity_active, 1024 // self.zoom, 768 // self.zoom)

        self.fake_screen.blit(self.background_galaxy, (0, 0))

        self.map.draw(self.scroll, self.fake_screen, mur_bas_rects=self.mur_bas_rects, draw_foreground=False)

        if self.eclipse.is_animating:
            self.eclipse.draw(self.fake_screen, self.scroll)

        if self.player.capacity_active:
            self.shadow_move = self.scroll.apply(self.shadow.rect)
            self.fake_screen.blit(self.shadow.image, self.shadow_move)

        for enemy in self.enemies:
            enemy_move = self.scroll.apply(enemy.rect)
            enemy.draw_aggro_range(self.fake_screen, enemy_move)
            self.fake_screen.blit(enemy.image, enemy_move)
            enemy.draw_hp_bar(self.fake_screen, enemy_move)

        self.player_move = self.scroll.apply(self.player.rect)
        self.fake_screen.blit(self.player.image, self.player_move)
            
        # map
        self.map.draw(self.scroll, self.fake_screen, mur_bas_rects=self.mur_bas_rects, draw_foreground=True)

        # light
        self.light_surface.fill((0, 0, 0, 0))
        render_lights(self.light_surface, self.map.tmx_data, camera_offset=(self.scroll.x, self.scroll.y))
        self.fake_screen.blit(self.light_surface, (0, 0))

        # zoom
        screen_zoom = pg.transform.scale(self.fake_screen, (1024, 768))
        self.screen.display.blit(screen_zoom, (0, 0))
            
        # hud
        self.hud.draw(self.screen.display, self.player)
        self.scenario.dialog_draw(self.screen.display)

        # hint
        if self.shadow_hint:
            self.shadow_hint.draw(self.screen.display)