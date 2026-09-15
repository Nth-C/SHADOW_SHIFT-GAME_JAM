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
        pg.display.set_caption("Shadow of PikPik");

        self.screen = Screen()
        self.timer = pg.time.Clock();
        
        self.map = Map(self.screen)
        self.map.switch_map("spawn")
        
        self.player = Body(400, 300);
        self.hud = HudManager()

        self.scroll = Scroll()
        self.zoom = 2
        self.fake_screen = pg.Surface((1024 // self.zoom, 768 // self.zoom))

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
            self.player.update_energy();

            self.fake_screen.fill((0,0,0))

            self.scroll.scroll_update(self.player, 1024 // self.zoom, 768 // self.zoom)
            self.map.draw(self.scroll, self.fake_screen)
            self.player_move = self.scroll.apply(self.player.rect)

            
            self.fake_screen.blit(self.player.image, self.player_move)
            screen_zoom = pg.transform.scale(self.fake_screen, (1024, 768))
            self.screen.display.blit(screen_zoom, (0, 0))
            
            self.hud.draw(self.screen.display, self.player)

            self.screen.update()
            self.timer.tick(60)

        pg.quit();
        sys.exit();