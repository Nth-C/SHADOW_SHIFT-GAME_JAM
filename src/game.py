import sys
import pygame as pg
from player import Body
from constants import settings
from hud.hud import HudManager

class Game:
    def __init__(self):
        pg.display.set_caption("Shadow of PikPik");

        self.screen = pg.display.set_mode((settings.WIDTH_SCREEN, settings.HEIGHT_SCREEN));
        self.timer = pg.time.Clock();
        
        self.player = Body(400, 300);
        self.hud = HudManager()

    def run(self):
        # boucle de jeu
        running = True;

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False;
                    
                self.player.event_handler(event);
                
            self.player.move();
            
            self.screen.fill((30, 30, 30));
            self.screen.blit(self.player.image, self.player.rect);

            self.hud.draw(self.screen, self.player)
            
            pg.display.flip();
            self.timer.tick(60);

        pg.quit();
        sys.exit();