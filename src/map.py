from pathlib import Path

import pytmx

from screen import Screen

MAPS_DIR = Path(__file__).resolve().parent.parent / "assets" / "maps"


class Map:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.tmx_data = None

    def switch_map(self, map_name: str):
        map_path = MAPS_DIR / f"{map_name}.tmx"
        self.tmx_data = pytmx.load_pygame(str(map_path))

    def draw(self, scroll, zoom):
        if not self.tmx_data:
            return

        display = self.screen.get_display()

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        pos_x = x * (self.tmx_data.tilewidth) + scroll.x
                        pos_y = y * (self.tmx_data.tileheight) + scroll.y
                        zoom.blit(tile, (pos_x, pos_y))
