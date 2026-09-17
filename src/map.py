from pathlib import Path
import math

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

            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if hasattr(obj, 'image') and obj.image:
                        image = obj.image
                        
                        world_x = obj.x
                        world_y = obj.y

                        if hasattr(obj, 'rotation') and obj.rotation != 0:
                            # Tiled rotates objects around their bottom-left corner (obj.x, obj.y + obj.height)
                            rad = math.radians(obj.rotation)
                            cx = obj.width / 2
                            cy = -obj.height / 2  # y goes up relative to bottom-left
                            
                            # Rotate center clockwise (since y is down, positive angle is clockwise)
                            new_cx = cx * math.cos(rad) - cy * math.sin(rad)
                            new_cy = cx * math.sin(rad) + cy * math.cos(rad)
                            
                            center_x = obj.x + new_cx
                            center_y = (obj.y + obj.height) + new_cy
                            
                            image = pg.transform.rotate(image, -obj.rotation)
                            new_rect = image.get_rect(center=(center_x, center_y))
                            world_x = new_rect.x
                            world_y = new_rect.y
                        
                        if mur_bas_rects is not None:
                            obj_rect = pg.Rect(world_x, world_y, obj.width, obj.height)
                            is_mur_bas = any(obj_rect.colliderect(r) for r in mur_bas_rects)
                            if draw_foreground and not is_mur_bas:
                                continue
                            if not draw_foreground and is_mur_bas:
                                continue

                        pos_x = world_x + scroll.x
                        pos_y = world_y + scroll.y
                        zoom.blit(image, (pos_x, pos_y))