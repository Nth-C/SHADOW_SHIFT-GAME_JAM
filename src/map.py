from pathlib import Path
import pytmx
import pygame as pg
from screen import Screen

MAPS_DIR = Path(__file__).resolve().parent.parent / "assets" / "maps"

class Map:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.tmx_data = None

    def switch_map(self, map_name: str):
        map_path = MAPS_DIR / f"{map_name}.tmx"
        self.tmx_data = pytmx.load_pygame(str(map_path))

    def draw(self, layer_names=None, mur_bas_rects=None, draw_foreground=False):
        if not self.tmx_data:
            return
            
        display = self.screen.get_display()
        
        for layer in self.tmx_data.visible_layers:
            if layer_names is not None and layer.name not in layer_names:
                continue
                
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        pos_x = x * self.tmx_data.tilewidth
                        pos_y = y * self.tmx_data.tileheight
                        
                        # --- Logique pour utiliser votre objet "mur_bas" ---
                        if mur_bas_rects:
                            # On crée un rectangle autour de la tuile en cours de dessin
                            tile_rect = pg.Rect(pos_x, pos_y, self.tmx_data.tilewidth, self.tmx_data.tileheight)
                            
                            # On vérifie si la tuile touche l'un de vos rectangles "mur_bas"
                            is_mur_bas = any(tile_rect.colliderect(r) for r in mur_bas_rects)
                            
                            # Si on dessine l'avant-plan mais que la tuile n'est PAS un mur bas -> on ne dessine pas
                            if draw_foreground and not is_mur_bas:
                                continue
                            # Si on dessine l'arrière-plan mais que la tuile EST un mur bas -> on ne dessine pas
                            if not draw_foreground and is_mur_bas:
                                continue
                        # ---------------------------------------------------

                        display.blit(tile, (pos_x, pos_y))