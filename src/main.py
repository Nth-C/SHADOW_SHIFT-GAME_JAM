import pygame
import sys
from player import Body

pygame.init()
ecran = pygame.display.set_mode((800, 600))
horloge = pygame.time.Clock()

joueur = Body(400, 300)

en_jeu = True
while en_jeu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_jeu = False

    touches = pygame.key.get_pressed()
    
    joueur.move(touches)

    ecran.fill((30, 30, 30))
    
    ecran.blit(joueur.image, joueur.rect)
    
    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
sys.exit()