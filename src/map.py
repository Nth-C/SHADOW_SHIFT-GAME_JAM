from pathlib import Path

import pygame as pg
import pytmx

from screen import Screen


class Map:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.map = None

    def switch_map(self, map_name: str):
        repo_root = Path(__file__).resolve().parent.parent
        map_path = (repo_root / "assets" / "maps" / f"{map_name}.tmx").resolve()

        if not map_path.exists():
            raise FileNotFoundError(f"TMX map not found at: {map_path}")

        self.tmx_data = pytmx.load_pygame(str(map_path))

    def draw(self, scroll, zoom, layer_names=None, mur_bas_rects=None, draw_foreground=False):
        if not self.tmx_data:
            return                      

        for layer in self.tmx_data.visible_layers:
            if layer_names is not None and layer.name not in layer_names:
                continue                              

            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, img_id in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(img_id)
                    if tile:
                        world_x = x * self.tmx_data.tilewidth
                        world_y = y * self.tmx_data.tileheight
                        
                        if mur_bas_rects is not None:
                            tile_rect = pg.Rect(world_x, world_y, self.tmx_data.tilewidth, self.tmx_data.tileheight)
                            is_mur_bas = any(tile_rect.colliderect(r) for r in mur_bas_rects)
                            
                            if draw_foreground and not is_mur_bas:
                                continue
                            if not draw_foreground and is_mur_bas:
                                continue

                        pos_x = world_x + scroll.x
                        pos_y = world_y + scroll.y
                        zoom.blit(tile, (pos_x, pos_y))