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

            self.scroll.scroll_update(self.player, 1024, 768)

            self.map.draw(self.scroll)

            self.player_move = self.scroll.apply(self.player.rect)
            
            self.screen.display.blit(self.player.image, self.player_move)
            
            self.hud.draw(self.screen.display, self.player)

            self.screen.update()
            self.timer.tick(60)

        pg.quit();
        sys.exit();