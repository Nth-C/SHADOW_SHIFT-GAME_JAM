import math

import pygame as pg
from pygame.event import Event

import constants.game_states as game_constants
import constants.settings as settings_constants
from eclipse import Eclipse
from enums.direction import Direction
from hud.hint import Hint
from hud.hud import HudManager
from light import draw_light_objects, iter_light_sources, render_lights
from map import Map
from player.body import Body
from player.shadow import Shadow
from scenarioManager import ScenarioManager
from screen import Screen
from scroll import Scroll
from sound import Sound
from timer import Timer
from utils_wave import get_enemies_of_waves
from waves import Waves


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

        self.map = Map(self.screen)
        self.map.switch_map("spawn")
        self.refresh_map_data()

        self.hud = HudManager()
        self.zoom = 2

        vague_1 = get_enemies_of_waves(self, 1, 9, 6)

        self.waves = Waves([vague_1])
        self.waves.start_wave()

        self.spawn_entities_at_player()

        self.entity_active = self.player

        self.hud = HudManager()
        self.shadow_hint = Hint("A pour passer en ombre", pg.K_a, True)

        self.scroll = Scroll()
        self.fake_screen = pg.Surface((1024 // self.zoom, 768 // self.zoom))
        self.light_surface = pg.Surface(
            (1024 // self.zoom, 768 // self.zoom), pg.SRCALPHA
        )

        self.scenario = ScenarioManager()

        self.eclipse = Eclipse(-5000, -5000)

        self.game_timer = Timer()
        self.game_timer.start()

    # evenement du player
    def handle_event(self, event: Event) -> None:
        # gestion des dialogues
        if self.scenario.is_dialog_playing():
            self.scenario.event_handler(event)
            self.player.reset_movement()
            self.shadow.reset_movement()
        else:
            used_walls = (
                self.walls_shadow
                if self.entity_active == self.shadow
                else self.walls_player
            )
            self.entity_active.event_handler(event, used_walls)

            # hint
            if self.shadow_hint:
                self.shadow_hint.handle_event(event)

            # --- capacite ombre
            # active la capacite de se spéarer de son ombre
            if event.type == pg.KEYDOWN and event.key == pg.K_a:
                if self.entity_active == self.player and self.player.energy > 0:
                    self.player.toggle_capacity()
                    self.shadow.rect.topleft = self.player.rect.topleft
                    self.entity_active = self.shadow
                    self.sound.play_shadow_enter()

                    # pour debug le mouvement en changant d'etat
                    self.player.reset_movement()
                    self.shadow.reset_movement()

                elif self.entity_active == self.shadow:
                    self.player.toggle_capacity()
                    self.entity_active = self.player
                    self.sound.play_shadow_exit()

                    self.player.reset_movement()
                    self.shadow.reset_movement()

            # permet de se téléporter à l'ombre
            if (
                self.entity_active == self.shadow
                and event.type == pg.KEYDOWN
                and event.key == pg.K_c
            ):
                self.player.rect.topleft = self.shadow.rect.topleft
                self.player.toggle_capacity()
                self.entity_active = self.player
                self.sound.play_shadow_exit()

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

        self.refresh_collision_walls(include_wave_exit=True)

        self.walls_dialogs = [
            (pg.Rect(obj.x, obj.y, obj.width, obj.height), obj.type)
            for obj in self.map.tmx_data.objects
            if obj.type in ("dialogue", "wave_exit", "dialogue 1")
        ]

        switch_map = next(
            (obj for obj in self.map.tmx_data.objects if obj.type == "switch_map"),
            None,
        )

        if switch_map is not None:
            self.switch_map_rect = pg.Rect(
                switch_map.x, switch_map.y, switch_map.width, switch_map.height
            )
            self.target_map_name = getattr(switch_map, "target_map", "spawn")
        else:
            self.switch_map_rect = None
            self.target_map_name = None

    def refresh_collision_walls(self, include_wave_exit):
        blocked_player_types = {"collision", "ombre"}
        blocked_shadow_types = {"collision", "switch_map"}
        blocked_enemy_types = {"collision", "ombre", "switch_map", "wave_exit"}

        if include_wave_exit:
            blocked_player_types.add("wave_exit")
            blocked_shadow_types.add("wave_exit")

        self.walls_player = [
            pg.Rect(obj.x, obj.y, obj.width, obj.height)
            for obj in self.map.tmx_data.objects
            if obj.type in blocked_player_types
        ]
        self.walls_shadow = [
            pg.Rect(obj.x, obj.y, obj.width, obj.height)
            for obj in self.map.tmx_data.objects
            if obj.type in blocked_shadow_types
        ]
        self.walls_enemies = [
            pg.Rect(obj.x, obj.y, obj.width, obj.height)
            for obj in self.map.tmx_data.objects
            if obj.type in blocked_enemy_types
        ]

    def spawn_entities_at_sun(self):
        sun_position = self.map.tmx_data.get_object_by_name("soleil")
        self.eclipse = Eclipse(sun_position.x, sun_position.y)

    def spawn_entities_at_player(self):
        player_position = self.map.tmx_data.get_object_by_name("player")
        self.player = Body(player_position.x, player_position.y)
        self.shadow = Shadow(player_position.x, player_position.y)

        spawn_dir = getattr(player_position, "direction", "down")

        self.player.change_animation(spawn_dir)

        self.player.current_dir_x = None
        self.player.current_dir_y = None

        if spawn_dir == "up":
            self.player.current_dir_y = Direction.UP
        elif spawn_dir == "down":
            self.player.current_dir_y = Direction.DOWN
        elif spawn_dir == "left":
            self.player.current_dir_x = Direction.LEFT
        elif spawn_dir == "right":
            self.player.current_dir_x = Direction.RIGHT

        self.background_galaxy = pg.image.load("assets/images/galaxie.png").convert()
        self.background_galaxy = pg.transform.scale(
            self.background_galaxy, (1024 // self.zoom, 768 // self.zoom)
        )

    def respawn_player(self):
        self.map.switch_map("spawn")
        self.refresh_map_data()
        self.spawn_entities_at_player()
        self.entity_active = self.player

        vague_1 = get_enemies_of_waves(self, 1, 9, 6)
        self.waves = Waves([vague_1])
        self.waves.start_wave()

        self.eclipse.reset()
        self.scenario.reset()

        self.game_timer.start()

    def update(self) -> str:
        if self.entity_active.is_attacking:
            zone_attaque = self.entity_active.get_attack_range()
            for ennemi in self.waves.get_current_enemies():
                if zone_attaque.colliderect(ennemi.rect):
                    ennemi.take_damage(self.entity_active.attack)

                    if not ennemi.alive():
                        self.sound.play_enemy_death()

            self.entity_active.is_attacking = False
            self.sound.play_attack()

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

            self.waves.wave_update(self.player, self.walls_enemies)
            self.waves.update_wave_status()

        ennemis_touches = pg.sprite.spritecollide(
            self.player, self.waves.get_current_enemies(), False
        )

        if ennemis_touches and self.player.take_damage(ennemis_touches[0].attack):
            self.sound.play_hit()

        if (
            self.waves.room_is_clear()
            and len(self.waves.list_of_waves) > 0
            and self.scenario.wave == 0
        ):
            self.refresh_collision_walls(include_wave_exit=False)

            if self.entity_active == self.shadow and not self.player.capacity_active:
                self.entity_active = self.player

            if (
                self.entity_active == self.player
                and self.switch_map_rect
                and self.player.feet.colliderect(self.switch_map_rect)
                and self.target_map_name
            ):
                self.map.switch_map(self.target_map_name)
                self.refresh_map_data()
                self.spawn_entities_at_player()
                self.entity_active = self.player

        if self.entity_active == self.shadow and not self.player.capacity_active:
            self.entity_active = self.player

        if self.entity_active == self.shadow:
            shadow_x, shadow_y = self.shadow.rect.center
            for lampe_x, lampe_y, rayon in iter_light_sources(self.map.tmx_data):
                if math.hypot(lampe_x - shadow_x, lampe_y - shadow_y) <= rayon:
                    self.player.toggle_capacity()
                    self.entity_active = self.player
                    break

        # mort
        if self.player.hp <= 0:
            self.game_timer.stop()
            self.sound.play_death()
            return game_constants.GAME_OVER

        # fin / crédit
        if self.scenario.step == 4:
            self.game_timer.stop()
            return game_constants.END

        # continuer le jeu
        return game_constants.PLAYING

    # --- affichage
    def draw(self):
        self.scroll.scroll_update(
            self.entity_active, 1024 // self.zoom, 768 // self.zoom
        )

        self.fake_screen.blit(self.background_galaxy, (0, 0))

        self.map.draw(
            self.scroll,
            self.fake_screen,
            mur_bas_rects=self.mur_bas_rects,
            draw_foreground=False,
        )

        if self.eclipse.rect.x > -4000:
            self.eclipse.draw(self.fake_screen, self.scroll)

        if self.player.capacity_active:
            self.shadow_move = self.scroll.apply(self.shadow.rect)
            self.fake_screen.blit(self.shadow.image, self.shadow_move)

        self.waves.draw_waves(self.fake_screen, self.scroll)

        self.player_move = self.scroll.apply(self.player.rect)
        self.fake_screen.blit(self.player.image, self.player_move)

        # map
        self.map.draw(
            self.scroll,
            self.fake_screen,
            mur_bas_rects=self.mur_bas_rects,
            draw_foreground=True,
        )

        # light
        draw_light_objects(
            self.fake_screen,
            self.map.tmx_data,
            camera_offset=(self.scroll.x, self.scroll.y),
        )
        self.light_surface.fill((0, 0, 0, 0))
        render_lights(
            self.light_surface,
            self.map.tmx_data,
            camera_offset=(self.scroll.x, self.scroll.y),
        )
        self.fake_screen.blit(self.light_surface, (0, 0))

        # zoom
        screen_zoom = pg.transform.scale(self.fake_screen, (1024, 768))
        self.screen.display.blit(screen_zoom, (0, 0))

        # filtre noir eclipse fin
        if self.eclipse.fade > 0:
            black_filter = pg.Surface((1024, 768), pg.SRCALPHA)
            black_filter.fill((0, 0, 0, int(self.eclipse.fade)))
            self.screen.display.blit(black_filter, (0, 0))

        # hud
        self.hud.draw(self.screen.display, self.player)
        self.scenario.dialog_draw(self.screen.display)

        # hint
        if self.shadow_hint:
            self.shadow_hint.draw(self.screen.display)
