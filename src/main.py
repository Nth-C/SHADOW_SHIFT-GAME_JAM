import pygame as pg
import sys
from player import Body
from constants import settings

pg.init()
ecran = pg.display.set_mode((settings.WIDTH_SCREEN, settings.WIDTH_SCREEN))
horloge = pg.time.Clock()

joueur = Body(400, 300)

en_jeu = True
while en_jeu:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            en_jeu = False
            
        joueur.event_handler(event)
        
    joueur.move()
    
    ecran.fill((30, 30, 30))
    
    ecran.blit(joueur.image, joueur.rect)
    
    pg.display.flip()
    horloge.tick(60)

pg.quit()
sys.exit()