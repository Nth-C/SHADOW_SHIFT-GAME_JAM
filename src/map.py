from pathlib import Path

import pytmx

from screen import Screen

class Map:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.map = None

    def switch_map(self, map_name: str):
        map_path = "assets/maps/" + map_name + ".tmx"
        self.map = pytmx.load_pygame(map_path)

    def draw(self, scroll, zoom):
        if not self.map:
            return

        display = self.screen.get_display()

        for layer in self.map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, img_id in layer:
                    tile = self.map.get_tile_image_by_gid(img_id)
                    if tile:
                        pos_x = x * (self.map.tilewidth) + scroll.x
                        pos_y = y * (self.map.tileheight) + scroll.y
                        zoom.blit(tile, (pos_x, pos_y))
