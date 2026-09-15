from pathlib import Path
import pytmx
import pygame as pg
from screen import Screen

class Map:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.map = None

    def switch_map(self, map_name: str):
        map_path = "assets/maps/" + map_name + ".tmx"
        self.map = pytmx.load_pygame(map_path)

    def draw(self, layer_names=None, mur_bas_rects=None, draw_foreground=False):
        if not self.tmx_data:
            return
            
        display = self.screen.get_display()
        
        for layer in self.tmx_data.visible_layers:
            if layer_names is not None and layer.name not in layer_names:
                continue
                
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, img_id in layer:
                    tile = self.map.get_tile_image_by_gid(img_id)
                    if tile:
                        pos_x = x * (self.map.tilewidth) + scroll.x
                        pos_y = y * (self.map.tileheight) + scroll.y
                        zoom.blit(tile, (pos_x, pos_y))
                        
                        if mur_bas_rects:
                            tile_rect = pg.Rect(pos_x, pos_y, self.tmx_data.tilewidth, self.tmx_data.tileheight)
                            
                            is_mur_bas = any(tile_rect.colliderect(r) for r in mur_bas_rects)
                            
                            if draw_foreground and not is_mur_bas:
                                continue
                            if not draw_foreground and is_mur_bas:
                                continue



