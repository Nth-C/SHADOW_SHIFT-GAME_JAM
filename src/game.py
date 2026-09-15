import sys
import pygame as pg
from player import Body
import constants.settings as settings_constants
from hud.hud import HudManager
from map import Map
from screen import Screen
from entity import Entity
from scroll import Scroll

class Game:
    def __init__(self):
        pg.display.set_caption("Shadow of PikPik")
        self.screen = Screen()
        self.timer = pg.time.Clock()
        
        self.map = Map(self.screen)
        self.map.switch_map("spawn")
        
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
                                     
                self.player.event_handler(event, self.walls)
                             
            self.player.move(self.walls)
            if not self.player.capacity_active:
                self.player.regen_energy();
            self.player.update_energy();

            self.scroll.scroll_update(self.player, 1024 // self.zoom, 768 // self.zoom)

            self.fake_screen.fill((0, 0, 0))

            self.map.draw(self.scroll, self.fake_screen, ("sol", "objet"))
            
            self.map.draw(self.scroll, self.fake_screen, ("mur", "barriere", "armoire"), mur_bas_rects=self.mur_bas_rects, draw_foreground=False)
            self.player_move = self.scroll.apply(self.player.rect)

            
            self.fake_screen.blit(self.player.image, self.player_move)

            self.map.draw(self.scroll, self.fake_screen, ("mur", "barriere", "armoire"), mur_bas_rects=self.mur_bas_rects, draw_foreground=True)

            screen_zoom = pg.transform.scale(self.fake_screen, (1024, 768))
            self.screen.display.blit(screen_zoom, (0, 0))
            
            self.hud.draw(self.screen.display, self.player)
            
            self.screen.update()
            self.timer.tick(60)

        pg.quit()
        sys.exit()